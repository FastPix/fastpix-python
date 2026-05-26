"""Shared helpers for the GET/non-GET validation harnesses and the link checker."""

from __future__ import annotations

import importlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "fixed.yaml"
ARTIFACTS_GET = REPO_ROOT / "tests" / "artifacts"
ARTIFACTS_NON_GET = REPO_ROOT / "tests" / "artifacts_non_get"
PLACEHOLDER_UUID = "00000000-0000-0000-0000-000000000000"
SDK_PACKAGE = "fastpix_python"


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def require_credentials() -> Tuple[str, str]:
    user = os.environ.get("FASTPIX_USERNAME")
    pwd = os.environ.get("FASTPIX_PASSWORD")
    if not user or not pwd:
        raise SystemExit(
            "FASTPIX_USERNAME and FASTPIX_PASSWORD must be set in the environment."
        )
    return user, pwd


# ---------------------------------------------------------------------------
# Spec loading + jsonschema integration
# ---------------------------------------------------------------------------


def load_spec(path: Path = SPEC_PATH) -> Dict[str, Any]:
    try:
        import yaml  # PyYAML
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required. Install with `pip install pyyaml`."
        ) from exc
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def spec_server_url(spec: Mapping[str, Any]) -> str:
    servers = spec.get("servers") or []
    if not servers:
        raise RuntimeError("Spec has no servers[] entry.")
    url = str(servers[0]["url"]).rstrip("/")
    return url


HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


def iter_operations(spec: Mapping[str, Any]):
    """Yield (path, method, operation_object) for every operation in the spec."""
    for path, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method.lower() in HTTP_METHODS and isinstance(op, dict):
                yield path, method.lower(), op


# ---------------------------------------------------------------------------
# OpenAPI sidecar: long-lived Node subprocess running openapi-response-validator
# ---------------------------------------------------------------------------


class OpenAPISidecar:
    """Wraps the Node sidecar that runs openapi-response-validator.

    The same validator (and ref-rewrite logic) the Node SDK harness uses, so
    response-schema verdicts match across SDKs exactly. Spec is loaded once,
    each request/response is a single line of JSON.
    """

    def __init__(self) -> None:
        import subprocess
        sidecar_path = REPO_ROOT / "tests" / "openapi_validator_sidecar.mjs"
        if not sidecar_path.exists():
            raise RuntimeError(f"sidecar script missing: {sidecar_path}")
        self._proc = subprocess.Popen(
            ["node", str(sidecar_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(REPO_ROOT),
            text=True,
            bufsize=1,
        )
        # Wait for the readiness signal.
        ready = self._proc.stdout.readline() if self._proc.stdout else ""
        try:
            obj = json.loads(ready)
            if not obj.get("ready"):
                raise RuntimeError(f"sidecar handshake failed: {ready!r}")
        except json.JSONDecodeError as exc:
            stderr = self._proc.stderr.read() if self._proc.stderr else ""
            raise RuntimeError(
                f"sidecar didn't return ready signal: stdout={ready!r} stderr={stderr!r}"
            ) from exc

    def validate(self, op_id: str, status: int, body: Any) -> Tuple[bool, List[Dict[str, Any]]]:
        """Returns (valid, errors).

        ``valid=True`` when the validator returns no errors.
        When no schema/validator is registered for this op, returns (True, []).
        ``errors`` is a list of ``{"path": "...", "message": "...", "keyword": "..."}``
        dicts (same shape the Node SDK's harness consumes).
        """
        req = {"op_id": op_id, "status": str(status), "body": body}
        line = json.dumps(req, default=str)
        assert self._proc.stdin is not None and self._proc.stdout is not None
        self._proc.stdin.write(line + "\n")
        self._proc.stdin.flush()
        raw = self._proc.stdout.readline()
        if not raw:
            stderr = self._proc.stderr.read() if self._proc.stderr else ""
            raise RuntimeError(f"sidecar died mid-stream: {stderr!r}")
        resp = json.loads(raw)
        if resp.get("valid") is True:
            return True, []
        if resp.get("valid") is None:
            return True, []  # no schema to validate against
        return False, resp.get("errors") or []

    def close(self) -> None:
        try:
            if self._proc.stdin and not self._proc.stdin.closed:
                self._proc.stdin.write(json.dumps({"command": "quit"}) + "\n")
                self._proc.stdin.flush()
        except (BrokenPipeError, ValueError):
            pass
        try:
            self._proc.wait(timeout=5)
        except Exception:
            self._proc.kill()


_sidecar_singleton: Optional[OpenAPISidecar] = None


def get_sidecar() -> OpenAPISidecar:
    global _sidecar_singleton
    if _sidecar_singleton is None:
        _sidecar_singleton = OpenAPISidecar()
    return _sidecar_singleton


def schema_with_components(schema: Mapping[str, Any], components: Mapping[str, Any]) -> Dict[str, Any]:
    """Wrap a per-response schema with the spec's component schemas so $ref resolves.

    jsonschema's RefResolver walks `definitions`, so we rewrite `#/components/schemas/X`
    to `#/definitions/X` and add a `definitions` block.

    PyYAML deserializes YAML dates into Python ``date`` objects, which ``json.dumps``
    can't handle natively — coerce to string at dump time.
    """
    text = json.dumps(schema, default=str)
    text = text.replace('"#/components/schemas/', '"#/definitions/')
    rewritten = json.loads(text)
    defs_text = json.dumps(components.get("schemas") or {}, default=str)
    defs_text = defs_text.replace('"#/components/schemas/', '"#/definitions/')
    rewritten_defs = json.loads(defs_text)
    rewritten["definitions"] = rewritten_defs
    return rewritten


def validate_response(
    body: Any,
    operation: Mapping[str, Any],
    status_code: int,
    components: Mapping[str, Any],
) -> Tuple[bool, List[Dict[str, Any]]]:
    """Validate ``body`` against the operation's response schema for ``status_code``.

    Delegates to the Node sidecar running ``openapi-response-validator`` — the
    same library the Node SDK harness uses, so verdicts match across SDKs.
    Returns (valid, errors_list). If the spec has no schema for the status
    code, returns (True, []) — we don't penalize the SDK for that.

    ``components`` is ignored here — the sidecar holds the full spec already.
    """
    op_id = operation.get("operationId")
    if not op_id:
        return True, []
    return get_sidecar().validate(op_id, status_code, body)


# ---------------------------------------------------------------------------
# Path-set diff (strict, case-sensitive, [] treated as missing)
# ---------------------------------------------------------------------------


def collect_paths(value: Any, prefix: str = "", include_empty_arrays: bool = False) -> Set[str]:
    """Collect every intermediate and leaf JSON path. Matches Node SDK's
    `collectJsonPaths` with `includeEmptyArrays=false`.

    Empty arrays are skipped (no path emitted) when ``include_empty_arrays=False``,
    matching how the SDK omits unset arrays during serialization. Arrays of
    objects are merged into a single ``[]`` index.
    """
    out: Set[str] = set()
    if value is None:
        return out
    if isinstance(value, dict):
        for k, v in value.items():
            if not include_empty_arrays and isinstance(v, list) and not v:
                continue
            p = f"{prefix}.{k}" if prefix else k
            out.add(p)
            out |= collect_paths(v, p, include_empty_arrays)
        return out
    if isinstance(value, list):
        if not include_empty_arrays and not value:
            return out
        arr_prefix = f"{prefix}[]" if prefix else "[]"
        out.add(arr_prefix)
        for item in value:
            out |= collect_paths(item, arr_prefix, include_empty_arrays)
        return out
    if prefix:
        out.add(prefix)
    return out


def collect_empty_array_paths(value: Any, prefix: str = "") -> Set[str]:
    """Collect paths whose value is an empty list ``[]``."""
    out: Set[str] = set()
    if value is None or not isinstance(value, (dict, list)):
        return out
    if isinstance(value, list):
        arr_prefix = f"{prefix}[]" if prefix else "[]"
        for item in value:
            out |= collect_empty_array_paths(item, arr_prefix)
        return out
    for k, v in value.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, list) and not v:
            out.add(p)
        out |= collect_empty_array_paths(v, p)
    return out


def path_diff(api: Any, sdk: Any) -> Tuple[List[str], List[str]]:
    a = collect_paths(api)
    s = collect_paths(sdk)
    missing_in_sdk = sorted(a - s)
    missing_in_api = sorted(s - a)
    return missing_in_sdk, missing_in_api


# ---------------------------------------------------------------------------
# Artifact sanitizer & writer
# ---------------------------------------------------------------------------


_FASTPIX_IO_RE = re.compile(r"fastpix\.io")


def sanitize_for_snapshot(text: str) -> str:
    return _FASTPIX_IO_RE.sub("fastpix.com", text)


_TOP_KEYS = ("success",)  # always emit these first, in this order
_BOTTOM_KEYS = ()


def _canonicalize_order(value: Any) -> Any:
    """Recursively reorder dict keys so ``success`` (and any other TOP_KEYS) come
    first, then the remaining keys alphabetically. Lists are walked element-wise.

    This gives us both:
      - ``success: true`` always at the top of each object (per user request)
      - Byte-equal diffs between API and SDK artifacts (no field-declaration-order
        noise from nested pydantic models vs API wire order)
    """
    if isinstance(value, dict):
        keys = list(value.keys())
        top = [k for k in _TOP_KEYS if k in value]
        bottom = [k for k in _BOTTOM_KEYS if k in value]
        middle = sorted(k for k in keys if k not in top and k not in bottom)
        ordered_keys = top + middle + bottom
        return {k: _canonicalize_order(value[k]) for k in ordered_keys}
    if isinstance(value, list):
        return [_canonicalize_order(v) for v in value]
    return value


def write_artifact(path: Path, data: Any) -> None:
    """Write the raw response payload with canonical key ordering.

    ``success`` is always first; remaining keys are sorted alphabetically. This
    makes API and SDK artifacts byte-identical for PASS endpoints regardless of
    nested-object field-declaration order in the pydantic models or wire order
    from the API.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    canonical = _canonicalize_order(data)
    text = json.dumps(canonical, indent=2, sort_keys=False, default=str)
    text = sanitize_for_snapshot(text)
    path.write_text(text + "\n", encoding="utf-8")


def cap_for_preview(value: Any, limit: int = 4096) -> str:
    text = json.dumps(value, indent=2, default=str)
    text = sanitize_for_snapshot(text)
    if len(text) <= limit:
        return text
    return text[:limit] + "\n... [truncated]"


# ---------------------------------------------------------------------------
# Pydantic model -> dict
# ---------------------------------------------------------------------------


def to_jsonable(value: Any) -> Any:
    """Coerce SDK return values to a JSON-comparable dict/list/scalar.

    Uses ``exclude_unset=True`` on pydantic models so the SDK output mirrors the
    actual API response shape — pydantic ``Optional`` fields that weren't in the
    API body are excluded from the diff (otherwise the SDK looks like it has
    extra ``None``-valued fields the API never returned).
    """
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [to_jsonable(v) for v in value]
    if isinstance(value, tuple):
        return [to_jsonable(v) for v in value]
    if hasattr(value, "model_dump"):
        try:
            return value.model_dump(mode="json", by_alias=True, exclude_unset=True)
        except TypeError:
            try:
                return value.model_dump(by_alias=True, exclude_unset=True)
            except TypeError:
                return value.model_dump(by_alias=True)
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    if hasattr(value, "__dict__"):
        return {k: to_jsonable(v) for k, v in value.__dict__.items() if not k.startswith("_")}
    try:
        return json.loads(json.dumps(value, default=str))
    except Exception:
        return str(value)


def normalize_exception(exc: BaseException) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "name": type(exc).__name__,
        "message": str(exc),
    }
    for attr in ("status_code", "body"):
        if hasattr(exc, attr):
            try:
                payload[attr] = getattr(exc, attr)
            except Exception:  # noqa: BLE001
                pass
    if "body" in payload and isinstance(payload["body"], str):
        try:
            payload["body"] = json.loads(payload["body"])
        except Exception:  # noqa: BLE001
            pass
    return payload


# ---------------------------------------------------------------------------
# SDK dispatch: scan modules for operation_ids
# ---------------------------------------------------------------------------

_SUB_SDK_MODULES = (
    "input_video",
    "manage_videos",
    "in_video_ai_features",
    "playback",
    "playlist",
    "drm_configurations",
    "start_live_stream",
    "manage_live_stream",
    "live_playback",
    "simulcast_stream",
    "signing_keys",
    "views_sdk",
    "dimensions",
    "metrics",
    "errors",
)

_SUB_SDK_ATTR = {
    "input_video": "input_video",
    "manage_videos": "manage_videos",
    "in_video_ai_features": "in_video_ai_features",
    "playback": "playback",
    "playlist": "playlist",
    "drm_configurations": "drm_configurations",
    "start_live_stream": "start_live_stream",
    "manage_live_stream": "manage_live_stream",
    "live_playback": "live_playback",
    "simulcast_stream": "simulcast_stream",
    "signing_keys": "signing_keys",
    "views_sdk": "views",
    "dimensions": "dimensions",
    "metrics": "metrics",
    "errors": "errors",
}

# Hard-coded fallback for irregular cases (e.g. spec uses kebab-case, method uses snake_case).
# Operation IDs that the harness can't resolve via _OPERATION_METHOD_PATTERN are looked up here.
_MANUAL_OVERRIDES: Dict[str, Tuple[str, str]] = {}

# Per-operation kwarg renames. Speakeasy occasionally renames path/query
# parameters (e.g. `mediaId` → `source_media_id`); the spec is authoritative
# for the wire-format name but the SDK method signature wins for the call.
KWARG_OVERRIDES: Dict[str, Dict[str, str]] = {
    "get-media-clips": {"media_id": "source_media_id"},
}


@dataclass
class SDKBinding:
    operation_id: str
    sub_sdk_attr: str  # the attribute on Fastpix, e.g. "manage_videos"
    method_name: str   # snake_case method name on the sub-SDK


def _op_method_pattern(source: str) -> Set[str]:
    """Read source and yield (method_name, operation_id) pairs."""
    return set(re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(', source))


_OP_ID_TO_METHOD_RE = re.compile(
    r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\((?:[^)]|\n)*?\)[^{]*?'
    r'operation_id="([^"]+)"',
    re.DOTALL,
)


def build_dispatch() -> Dict[str, SDKBinding]:
    """Scan every sub-SDK module and return operation_id -> SDKBinding."""
    bindings: Dict[str, SDKBinding] = {}
    pkg_root = REPO_ROOT / SDK_PACKAGE
    for mod_name in _SUB_SDK_MODULES:
        mod_path = pkg_root / f"{mod_name}.py"
        if not mod_path.exists():
            continue
        text = mod_path.read_text(encoding="utf-8")
        # walk methods and pair each `def name(...)` with the first
        # `operation_id="..."` that follows (within the same function body)
        for match in re.finditer(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(', text):
            method_name = match.group(1)
            if method_name.startswith("_") or method_name.endswith("_async"):
                continue
            # Search up to the next `def ` boundary (functions with very long
            # docstrings can push operation_id well past 8 KB).
            tail = text[match.end():]
            next_def = re.search(r'\n    (?:async\s+)?def\s+', tail)
            window = tail[: next_def.start()] if next_def else tail
            op_match = re.search(r'operation_id="([^"]+)"', window)
            if not op_match:
                continue
            op_id = op_match.group(1)
            # First binding wins (sync version comes before async)
            bindings.setdefault(
                op_id,
                SDKBinding(
                    operation_id=op_id,
                    sub_sdk_attr=_SUB_SDK_ATTR[mod_name],
                    method_name=method_name,
                ),
            )
    bindings.update(
        {op: SDKBinding(op, attr, m) for op, (attr, m) in _MANUAL_OVERRIDES.items()}
    )
    return bindings


# ---------------------------------------------------------------------------
# camelCase -> snake_case for top-level SDK kwargs
# ---------------------------------------------------------------------------


_CAMEL_RE_1 = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_RE_2 = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(name: str) -> str:
    s1 = _CAMEL_RE_1.sub(r"\1_\2", name)
    return _CAMEL_RE_2.sub(r"\1_\2", s1).lower()


def kwargs_to_snake(d: Mapping[str, Any]) -> Dict[str, Any]:
    """Top-level keys only. Nested dicts are passed verbatim (SDK TypedDicts use
    camelCase aliases that pydantic resolves at construction time)."""
    return {camel_to_snake(k): v for k, v in d.items()}


# ---------------------------------------------------------------------------
# SDK invocation
# ---------------------------------------------------------------------------


def import_sdk():
    """Import the Fastpix SDK class fresh."""
    sys.path.insert(0, str(REPO_ROOT))
    fastpix_python = importlib.import_module(SDK_PACKAGE)
    models = importlib.import_module(f"{SDK_PACKAGE}.models")
    return fastpix_python.Fastpix, models


def build_sdk(client: Optional[Any] = None) -> Any:
    Fastpix, models = import_sdk()
    user, pwd = require_credentials()
    security = models.Security(username=user, password=pwd)
    kwargs: Dict[str, Any] = {"security": security}
    if client is not None:
        kwargs["client"] = client
    return Fastpix(**kwargs)


def call_sdk_method(
    sdk: Any,
    binding: SDKBinding,
    invocation_kwargs: Mapping[str, Any],
) -> Any:
    sub_sdk = _resolve_sub_sdk(sdk, binding.sub_sdk_attr)
    method = getattr(sub_sdk, binding.method_name)
    rename = KWARG_OVERRIDES.get(binding.operation_id) or {}
    if rename:
        invocation_kwargs = {rename.get(k, k): v for k, v in invocation_kwargs.items()}
    return method(**invocation_kwargs)


_SHADOWED_SUB_SDK_PATHS: Dict[str, Tuple[str, str]] = {
    # The `errors/` exception package shadows `errors.py` at import resolution
    # time, so `sdk.errors` raises AttributeError. Load the SDK class directly
    # from the file. This is a real SDK packaging bug — flagged in pre-publish.
    "errors": ("fastpix_python/errors.py", "Errors"),
}


def _resolve_sub_sdk(sdk: Any, sub_sdk_attr: str) -> Any:
    try:
        return getattr(sdk, sub_sdk_attr)
    except AttributeError:
        if sub_sdk_attr not in _SHADOWED_SUB_SDK_PATHS:
            raise
        rel_path, class_name = _SHADOWED_SUB_SDK_PATHS[sub_sdk_attr]
        return _load_sub_sdk_by_path(sdk, sub_sdk_attr, rel_path, class_name)


def _load_sub_sdk_by_path(sdk: Any, attr: str, rel_path: str, class_name: str) -> Any:
    import importlib.util
    full_path = REPO_ROOT / rel_path
    module_name = f"fastpix_python._shadowed_{attr}"
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load shadowed sub-SDK from {full_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    klass = getattr(mod, class_name)
    inst = klass(sdk.sdk_configuration, parent_ref=sdk)
    return inst


# ---------------------------------------------------------------------------
# Path-param substitution for raw HTTP calls
# ---------------------------------------------------------------------------


_PATH_PARAM_RE = re.compile(r"\{([^}]+)\}")


def substitute_path(template: str, path_params: Mapping[str, Any]) -> str:
    def repl(m: re.Match[str]) -> str:
        key = m.group(1)
        return str(path_params.get(key, PLACEHOLDER_UUID))
    return _PATH_PARAM_RE.sub(repl, template)


# ---------------------------------------------------------------------------
# Report writing helpers
# ---------------------------------------------------------------------------


@dataclass
class EndpointResult:
    endpoint: str            # path template (e.g. /on-demand/{mediaId})
    method: str
    operation_id: str
    status: str              # PASS / FAIL  (matches Node SDK — no SKIP/SDK_MISSING bucket)
    openapi_valid: bool
    openapi_errors: List[Dict[str, Any]] = field(default_factory=list)
    sdk_parse_ok: bool = True
    sdk_parse_error: Optional[str] = None
    missing_in_sdk: List[str] = field(default_factory=list)
    missing_in_api: List[str] = field(default_factory=list)
    empty_arrays_omitted_in_sdk: List[str] = field(default_factory=list)
    empty_arrays_omitted_in_api: List[str] = field(default_factory=list)
    api_response_file: Optional[str] = None
    sdk_response_file: Optional[str] = None
    api_response_preview: Optional[str] = None
    sdk_response_preview: Optional[str] = None
    api_status: Optional[int] = None
    note: Optional[str] = None
    fix_suggestions: List[Dict[str, str]] = field(default_factory=list)


def count_statuses(rows: Iterable[EndpointResult]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1
    return counts

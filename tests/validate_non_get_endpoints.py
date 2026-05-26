#!/usr/bin/env python
"""Non-GET endpoints validator (POST / PUT / PATCH / DELETE).

Unlike the GET validator, these operations MUTATE live data, so we cannot hit
the raw API and the SDK separately (that would create/delete twice). Instead
this driver invokes the SDK once per operation and:
  - captures the SDK's deserialized return value (for the diff + artifact)
  - captures the raw HTTP status + raw JSON body from the SDK's underlying
    response (via an httpx event_hook) for OpenAPI response-schema validation

No fixtures are required. The driver runs a CREATE → UPDATE → DELETE lifecycle:

  1. CREATE phase (POST)        - creates real resources, captures their IDs
  2. UPDATE phase (PUT / PATCH) - exercises updates against the created IDs
  3. DELETE phase (DELETE)      - tears the resources down, LAST, so deletes
                                  only run after every POST/PUT/PATCH

A step whose required IDs were never captured (because an upstream create
failed) is reported as SKIP rather than called with nulls.

Run: ``FASTPIX_USERNAME=… FASTPIX_PASSWORD=… python -m tests.validate_non_get_endpoints``
"""

from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple

from tests._common import (
    ARTIFACTS_NON_GET,
    EndpointResult,
    REPO_ROOT,
    build_dispatch,
    call_sdk_method,
    cap_for_preview,
    collect_empty_array_paths,
    get_sidecar,
    import_sdk,
    iter_operations,
    kwargs_to_snake,
    load_spec,
    normalize_exception,
    path_diff,
    require_credentials,
    spec_server_url,
    to_jsonable,
    validate_response,
    write_artifact,
)
from tests._reporting import (
    generate_fix_suggestions,
    write_fix_suggestions,
    write_validation_report,
)

TESTS_DIR = REPO_ROOT / "tests"
REPORT_PATH = TESTS_DIR / "NON_GET_ENDPOINTS_OPENAPI_RESPONSE_VALIDATION_REPORT.md"
SUGGESTIONS_PATH = TESTS_DIR / "NON_GET_ENDPOINTS_OPENAPI_RESPONSE_FIX_SUGGESTIONS.md"
FIXTURES_PATH = TESTS_DIR / "non_get_endpoints_fixtures.json"

MEDIA_READY_TIMEOUT_S = 180
TRACK_READY_TIMEOUT_S = 300
POLL_INTERVAL_S = 5
NOT_READY_RETRY_TIMEOUT_S = 120
NOT_READY_RETRY_INTERVAL_S = 5
NOT_READY_SUBSTR = "not ready for updates"

# ---------------------------------------------------------------------------
# Declarative lifecycle steps
# ---------------------------------------------------------------------------


def _get(value: Any, path: str) -> Any:
    """Dotted-path getter with support for ``parent.field.0.subfield`` indexing."""
    cur = value
    for part in path.split("."):
        if cur is None:
            return None
        if part.isdigit() and isinstance(cur, list):
            i = int(part)
            cur = cur[i] if 0 <= i < len(cur) else None
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            cur = getattr(cur, part, None)
    return cur


@dataclass
class Step:
    """One step in the lifecycle. Mirrors the TS validator's Step type."""
    operation_id: str
    phase: str                  # CREATE | UPDATE | DELETE
    needs: Tuple[str, ...] = ()  # ctx keys required, else SKIP
    # Build call kwargs from ctx (already in snake_case)
    request: Callable[[Dict[str, Any]], Dict[str, Any]] = field(default=lambda c: {})
    # Extract IDs from successful response into ctx
    capture: Optional[Callable[[Any, Dict[str, Any]], None]] = None
    # Retry on transient error substring (e.g. "not ready for updates")
    retry_on: Optional[str] = None
    # Body fields (sent in the request body), merged with path-param kwargs
    body: Dict[str, Any] = field(default_factory=dict)


# Helper: build a CREATE request body for create-media that's resolvable from a
# public URL. We use a known-good MP4 so the resulting media reliably reaches
# "Ready" within the polling window.
_CREATE_MEDIA_BODY = {
    "inputs": [{"type": "video", "url": "https://static.fastpix.com/sample.mp4"}],
    "access_policy": "public",
    "max_resolution": "720p",
    "metadata": {"source": "non-get-validator"},
}

import uuid as _uuid_mod

_CREATE_PLAYLIST_BODY = {
    "name": "non-get-validator-playlist",
    "type_": "manual",  # Python keyword conflict — SDK exposes as `type_`
    "reference_id": "nonGetValidator" + _uuid_mod.uuid4().hex[:8],
    "description": "Created by validate-non-get-endpoints",
}

_CREATE_STREAM_BODY = {
    # SDK only takes playback_settings + input_media_settings; metadata nests inside.
    "playback_settings": {"accessPolicy": "public"},
    "input_media_settings": {
        "maxResolution": "1080p",
        "reconnectWindow": 60,
        "mediaPolicy": "public",
        "metadata": {"source": "non-get-validator"},
    },
}

_DIRECT_UPLOAD_BODY = {
    # SDK takes a single `request` kwarg of type DirectUploadVideoMediaRequest
    "request": {
        "corsOrigin": "*",
        "pushMediaSettings": {
            "accessPolicy": "public",
            "metadata": {"source": "non-get-validator"},
        },
    },
}


def _capture_signing_key(v, c):
    c["signing_key_id"] = _get(v, "data.id")


def _capture_playlist(v, c):
    c["playlist_id"] = _get(v, "data.id")


def _capture_stream(v, c):
    c["stream_id"] = _get(v, "data.streamId") or _get(v, "data.id")
    # Stream's first playback ID is created automatically with the stream
    c["stream_playback_id_from_create"] = _get(v, "data.playbackIds.0.id")


def _capture_media(v, c):
    c["media_id"] = _get(v, "data.id")
    c["media_playback_id"] = _get(v, "data.playbackIds.0.id")


def _capture_media_playback_id(v, c):
    # API can return either the new playback id directly or nested under playbackIds[0]
    c["created_playback_id"] = _get(v, "data.id") or _get(v, "data.playbackIds.0.id")


def _capture_track(v, c):
    c["track_id"] = _get(v, "data.id")


def _capture_stream_playback_id(v, c):
    c["stream_playback_id"] = _get(v, "data.id") or _get(v, "data.playbackIds.0.id")


def _capture_simulcast(v, c):
    c["simulcast_id"] = _get(v, "data.simulcastId") or _get(v, "data.id")


def _capture_upload(v, c):
    c["upload_id"] = _get(v, "data.uploadId") or _get(v, "data.id")


STEPS: List[Step] = [
    # ---------------- CREATE ----------------
    Step("create_signing_key", "CREATE", capture=_capture_signing_key),
    Step("create-a-playlist", "CREATE",
         body=_CREATE_PLAYLIST_BODY, capture=_capture_playlist),
    Step("create-new-stream", "CREATE",
         body=_CREATE_STREAM_BODY, capture=_capture_stream),
    Step("create-media", "CREATE",
         body=_CREATE_MEDIA_BODY, capture=_capture_media),
    Step("create-media-playback-id", "CREATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"access_policy": "public"},
         capture=_capture_media_playback_id),
    Step("Add-media-track", "CREATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={
             # SDK takes a single `tracks` kwarg (AddTrackRequest object)
             "tracks": {
                 "url": "https://static.fastpix.com/sample.vtt",
                 "type": "subtitle",
                 "languageCode": "en",
                 "languageName": "English",
                 "closedCaptions": True,
             },
         },
         capture=_capture_track),
    Step("create-playbackId-of-stream", "CREATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]},
         body={"access_policy": "public"},
         capture=_capture_stream_playback_id),
    Step("create-simulcast-of-stream", "CREATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]},
         body={"url": "rtmp://example.com/live", "stream_key": "non-get-validator-key"},
         capture=_capture_simulcast),
    Step("direct-upload-video-media", "CREATE",
         body=_DIRECT_UPLOAD_BODY, capture=_capture_upload),
    Step("Generate-subtitle-track", "CREATE",
         needs=("media_id", "track_id"),
         retry_on="track not found",
         request=lambda c: {"media_id": c["media_id"], "track_id": c["track_id"]},
         body={"language_code": "en-US", "language_name": "English"}),

    # ---------------- UPDATE (PUT / PATCH) ----------------
    Step("updated-media", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"metadata": {"updatedBy": "non-get-validator"}}),
    Step("updated-source-access", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"source_access": True}),
    Step("updated-mp4Support", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"mp4_support": "capped_4k"}),
    Step("update-media-summary", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"generate": True, "summary_length": 100}),
    Step("update-media-chapters", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"chapters": True}),
    Step("update-media-named-entities", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"named_entities": True}),
    Step("update-media-moderation", "UPDATE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]},
         body={"moderation": {"type": "video"}}),
    Step("update-media-track", "UPDATE",
         needs=("media_id", "track_id"),
         request=lambda c: {"media_id": c["media_id"], "track_id": c["track_id"]},
         body={
             "url": "https://static.fastpix.com/sample.vtt?u=" + __import__("uuid").uuid4().hex,
             "language_code": "en",
             "language_name": "English",
         }),
    Step("update-domain-restrictions", "UPDATE",
         needs=("media_id", "media_playback_id"),
         retry_on=NOT_READY_SUBSTR,
         request=lambda c: {"media_id": c["media_id"], "playback_id": c["media_playback_id"]},
         body={"default_policy": "allow", "allow": [], "deny": []}),
    Step("update-user-agent-restrictions", "UPDATE",
         needs=("media_id", "media_playback_id"),
         retry_on=NOT_READY_SUBSTR,
         request=lambda c: {"media_id": c["media_id"], "playback_id": c["media_playback_id"]},
         body={"default_policy": "allow", "allow": [], "deny": []}),
    Step("update-a-playlist", "UPDATE",
         needs=("playlist_id",),
         request=lambda c: {"playlist_id": c["playlist_id"]},
         body={"name": "Updated by non-get-validator", "description": "updated"}),
    Step("add-media-to-playlist", "UPDATE",
         needs=("playlist_id", "media_id"),
         request=lambda c: {"playlist_id": c["playlist_id"], "media_ids": [c["media_id"]]}),
    Step("change-media-order-in-playlist", "UPDATE",
         needs=("playlist_id", "media_id"),
         request=lambda c: {"playlist_id": c["playlist_id"], "media_ids": [c["media_id"]]}),
    Step("update-live-stream", "UPDATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]},
         body={"metadata": {"updatedBy": "non-get-validator"}, "reconnect_window": 120}),
    Step("update-specific-simulcast-of-stream", "UPDATE",
         needs=("stream_id", "simulcast_id"),
         request=lambda c: {"stream_id": c["stream_id"], "simulcast_id": c["simulcast_id"]},
         body={"is_enabled": False}),
    # Freshly-created streams are already enabled; disable first, then enable.
    Step("disable-live-stream", "UPDATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]}),
    Step("enable-live-stream", "UPDATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]}),
    # Expected to fail: needs an actively-streaming encoder, which we don't have.
    Step("complete-live-stream", "UPDATE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]}),
    Step("cancel-upload", "UPDATE",
         needs=("upload_id",),
         request=lambda c: {"upload_id": c["upload_id"]}),

    # ---------------- DELETE (last) ----------------
    Step("delete-media-from-playlist", "DELETE",
         needs=("playlist_id", "media_id"),
         request=lambda c: {"playlist_id": c["playlist_id"], "media_ids": [c["media_id"]]}),
    Step("delete-a-playlist", "DELETE",
         needs=("playlist_id",),
         request=lambda c: {"playlist_id": c["playlist_id"]}),
    Step("delete-media-track", "DELETE",
         needs=("media_id", "track_id"),
         request=lambda c: {"media_id": c["media_id"], "track_id": c["track_id"]}),
    Step("delete-media-playback-id", "DELETE",
         needs=("media_id", "created_playback_id"),
         request=lambda c: {"media_id": c["media_id"], "playback_id": c["created_playback_id"]}),
    Step("delete-simulcast-of-stream", "DELETE",
         needs=("stream_id", "simulcast_id"),
         request=lambda c: {"stream_id": c["stream_id"], "simulcast_id": c["simulcast_id"]}),
    Step("delete-playbackId-of-stream", "DELETE",
         needs=("stream_id", "stream_playback_id"),
         request=lambda c: {"stream_id": c["stream_id"], "playback_id": c["stream_playback_id"]}),
    Step("delete-live-stream", "DELETE",
         needs=("stream_id",),
         request=lambda c: {"stream_id": c["stream_id"]}),
    Step("delete-media", "DELETE",
         needs=("media_id",),
         request=lambda c: {"media_id": c["media_id"]}),
    Step("delete_signing_key", "DELETE",
         needs=("signing_key_id",),
         request=lambda c: {"signing_key_id": c["signing_key_id"]}),
]

# complete-live-stream is the one allowed failure in a credentials-only run.
EXPECTED_FAILS = {"complete-live-stream"}

# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------


def poll_media_ready(httpx_mod, base_url: str, media_id: str, auth) -> str:
    """Wait for media to reach 'Ready' (returns final observed status)."""
    deadline = time.monotonic() + MEDIA_READY_TIMEOUT_S
    last = "unknown"
    url = f"{base_url}/on-demand/{media_id}"
    while time.monotonic() < deadline:
        try:
            r = httpx_mod.get(url, auth=auth, timeout=30.0,
                              headers={"Accept": "application/json"})
            if r.status_code == 200:
                last = str(((r.json() or {}).get("data") or {}).get("status") or last)
                if last == "Ready":
                    return last
                if last in {"Errored", "Failed"}:
                    return last
        except Exception:
            pass  # transient
        time.sleep(POLL_INTERVAL_S)
    return last


def poll_track_ready(httpx_mod, base_url: str, media_id: str, track_id: str, auth) -> str:
    deadline = time.monotonic() + TRACK_READY_TIMEOUT_S
    last = "absent"
    url = f"{base_url}/on-demand/{media_id}"
    while time.monotonic() < deadline:
        try:
            r = httpx_mod.get(url, auth=auth, timeout=30.0,
                              headers={"Accept": "application/json"})
            if r.status_code == 200:
                tracks = ((r.json() or {}).get("data") or {}).get("tracks") or []
                for t in tracks:
                    if t.get("id") == track_id:
                        last = str(t.get("status") or "present")
                        if last in {"Ready", "available", "present"}:
                            return last
        except Exception:
            pass
        time.sleep(POLL_INTERVAL_S)
    return last


# ---------------------------------------------------------------------------
# httpx capture hook — same SDK-only-call pattern as the GET harness
# ---------------------------------------------------------------------------


def make_hook(state: Dict[str, Any]) -> Callable[[Any], None]:
    def hook(response):
        if "api.fastpix" not in str(response.request.url):
            return
        response.read()
        body_json: Any = None
        try:
            body_json = response.json()
        except Exception:
            body_json = None
        state.update(
            url=str(response.request.url),
            method=response.request.method,
            status=response.status_code,
            body_json=body_json,
        )
    return hook


# ---------------------------------------------------------------------------
# Spec index
# ---------------------------------------------------------------------------


def build_operation_index(spec: Mapping[str, Any]) -> Dict[str, Tuple[str, str, Dict[str, Any]]]:
    idx: Dict[str, Tuple[str, str, Dict[str, Any]]] = {}
    for path, method, op in iter_operations(spec):
        if method == "get":
            continue
        op_id = op.get("operationId")
        if op_id:
            idx[op_id] = (path, method, op)
    return idx


# ---------------------------------------------------------------------------
# Step runner
# ---------------------------------------------------------------------------


def run_step(
    *,
    step: Step,
    op_index: Mapping[str, Tuple[str, str, Dict[str, Any]]],
    dispatch,
    sdk,
    raw_state: Dict[str, Any],
    ctx: Dict[str, Any],
    components: Mapping[str, Any],
    httpx_mod,
    base_url: str,
    auth,
) -> EndpointResult:
    if step.operation_id not in op_index:
        return EndpointResult(
            endpoint="(unknown)", method="?", operation_id=step.operation_id,
            status="SKIP", openapi_valid=True, openapi_errors=[],
            sdk_parse_ok=False, sdk_parse_error="operationId not found in spec",
            note=f"[{step.phase}] operationId not found in spec",
        )
    path, method, op = op_index[step.operation_id]

    # Step dependencies — skip if upstream IDs missing
    missing = [k for k in step.needs if not ctx.get(k)]
    if missing:
        return EndpointResult(
            endpoint=path, method=method, operation_id=step.operation_id,
            status="SKIP", openapi_valid=True, openapi_errors=[],
            sdk_parse_ok=False,
            sdk_parse_error=f"missing dependency: {missing}",
            note=f"[{step.phase}] upstream CREATE did not produce: {missing}",
        )

    binding = dispatch.get(step.operation_id)
    if binding is None:
        return EndpointResult(
            endpoint=path, method=method, operation_id=step.operation_id,
            status="FAIL", openapi_valid=True, openapi_errors=[],
            sdk_parse_ok=False,
            sdk_parse_error="SDK does not expose a method for this operation",
            note=f"[{step.phase}] SDK regeneration required — no method bound",
        )

    # generate-subtitle-track needs the track to exist on the media first
    if step.operation_id == "Generate-subtitle-track" and ctx.get("media_id") and ctx.get("track_id"):
        poll_track_ready(httpx_mod, base_url, ctx["media_id"], ctx["track_id"], auth)

    invocation: Dict[str, Any] = {}
    invocation.update(step.request(ctx))
    invocation.update(kwargs_to_snake(step.body))

    expected_fail = step.operation_id in EXPECTED_FAILS

    # Retry loop for transient "not ready for updates" errors
    deadline = time.monotonic() + NOT_READY_RETRY_TIMEOUT_S
    attempt = 0
    sdk_value: Any = None
    sdk_ok = False
    sdk_err = ""
    while True:
        attempt += 1
        raw_state.clear()
        try:
            ret = call_sdk_method(sdk, binding, invocation)
            sdk_value = to_jsonable(ret)
            sdk_ok = True
            break
        except Exception as exc:
            err_payload = normalize_exception(exc)
            sdk_value = err_payload
            sdk_err = f"{type(exc).__name__}: {exc}"
            msg = (sdk_err + " " + json.dumps(err_payload.get("body") or {})).lower()
            if step.retry_on and step.retry_on.lower() in msg and time.monotonic() < deadline:
                time.sleep(NOT_READY_RETRY_INTERVAL_S)
                continue
            break

    api_status = raw_state.get("status")
    api_body = raw_state.get("body_json")

    # ID capture from successful response
    if sdk_ok and step.capture and api_status and 200 <= api_status < 300:
        try:
            step.capture(api_body, ctx)
        except Exception:
            pass

    # create-media → poll until Ready (otherwise dependent steps 400)
    if step.operation_id == "create-media" and sdk_ok and ctx.get("media_id"):
        poll_media_ready(httpx_mod, base_url, ctx["media_id"], auth)

    # OpenAPI validation
    openapi_valid = True
    openapi_errors: List[Dict[str, Any]] = []
    if isinstance(api_body, dict) and api_status:
        openapi_valid, openapi_errors = validate_response(api_body, op, api_status, components)

    # Path diff
    if (sdk_ok and api_status and 200 <= api_status < 300
            and isinstance(api_body, (dict, list))):
        miss_sdk, miss_api = path_diff(api_body, sdk_value)
        empty_sdk = sorted(collect_empty_array_paths(api_body) - collect_empty_array_paths(sdk_value))
        empty_api = sorted(collect_empty_array_paths(sdk_value) - collect_empty_array_paths(api_body))
    else:
        miss_sdk, miss_api, empty_sdk, empty_api = [], [], [], []

    # Status
    if expected_fail:
        status = "PASS" if not sdk_ok else "FAIL"
        note = (f"[{step.phase}] Expected to fail in a credentials-only run "
                "(no active RTMPS encoder) — SDK behaviour is correct."
                if not sdk_ok else
                f"[{step.phase}] Operation succeeded but was expected to fail — check SDK swallowing")
    elif (sdk_ok and api_status and 200 <= api_status < 300
          and openapi_valid and not miss_sdk and not miss_api):
        status, note = "PASS", f"[{step.phase}]"
    else:
        status, note = "FAIL", f"[{step.phase}]"

    if attempt > 1:
        note += f"  (retried {attempt}x on '{step.retry_on}')"

    # Artifacts
    api_file = f"tests/artifacts_non_get/{step.operation_id}.raw.json"
    sdk_file = f"tests/artifacts_non_get/{step.operation_id}.sdk.json"
    write_artifact(ARTIFACTS_NON_GET / f"{step.operation_id}.raw.json", api_body)
    write_artifact(ARTIFACTS_NON_GET / f"{step.operation_id}.sdk.json", sdk_value)

    return EndpointResult(
        endpoint=path, method=method, operation_id=step.operation_id,
        status=status, openapi_valid=openapi_valid, openapi_errors=openapi_errors,
        sdk_parse_ok=sdk_ok, sdk_parse_error=sdk_err or None,
        missing_in_sdk=miss_sdk, missing_in_api=miss_api,
        empty_arrays_omitted_in_sdk=empty_sdk,
        empty_arrays_omitted_in_api=empty_api,
        api_response_file=api_file, sdk_response_file=sdk_file,
        api_response_preview=cap_for_preview(api_body) if api_body is not None else None,
        sdk_response_preview=cap_for_preview(sdk_value) if sdk_value is not None else None,
        api_status=api_status, note=note,
    )


def main() -> int:
    user, pwd = require_credentials()
    spec = load_spec()
    base_url = spec_server_url(spec)
    components = spec.get("components") or {}
    dispatch = build_dispatch()
    op_index = build_operation_index(spec)

    try:
        import httpx
    except ImportError:
        print("httpx not installed. Run `pip install -e .` in the repo root.", file=sys.stderr)
        return 2

    get_sidecar()  # warm up

    Fastpix, models = import_sdk()
    auth = (user, pwd)
    raw_state: Dict[str, Any] = {}
    client = httpx.Client(
        follow_redirects=True,
        event_hooks={"response": [make_hook(raw_state)]},
        timeout=180.0,
    )
    security = models.Security(username=user, password=pwd)
    sdk = Fastpix(security=security, client=client)
    ctx: Dict[str, Any] = {}

    total = len(STEPS)
    results: List[EndpointResult] = []
    for idx, step in enumerate(STEPS, start=1):
        ep = op_index.get(step.operation_id)
        method = (ep[1].upper() if ep else "?")
        path = (ep[0] if ep else "?")
        print(f"[{idx}/{total}] ({step.phase}) {method:>6} {path}  ({step.operation_id})", flush=True)

        result = run_step(
            step=step, op_index=op_index, dispatch=dispatch,
            sdk=sdk, raw_state=raw_state, ctx=ctx, components=components,
            httpx_mod=httpx, base_url=base_url, auth=auth,
        )

        captured = ""
        if step.capture and result.status == "PASS":
            new_keys = [k for k in ("signing_key_id", "playlist_id", "stream_id",
                                     "media_id", "media_playback_id", "created_playback_id",
                                     "track_id", "stream_playback_id", "simulcast_id", "upload_id")
                        if ctx.get(k)]
            captured = f"  ctx-keys={new_keys}" if new_keys else ""

        if result.status == "FAIL" and result.sdk_parse_error:
            print(f"  ⚠️  FAIL — {result.sdk_parse_error[:200]}", flush=True)
            result.fix_suggestions = generate_fix_suggestions(result)
        elif result.status == "SKIP":
            print(f"  ⏭  SKIP — {result.note}", flush=True)
        else:
            print(f"  ✓ {result.status} (HTTP {result.api_status or '?'}){captured}", flush=True)

        results.append(result)

    counts = write_validation_report(
        results, REPORT_PATH,
        title="Non-GET Endpoints — OpenAPI Response Validation Report",
        label_total="Total non-GET endpoints",
    )
    write_fix_suggestions(
        results, SUGGESTIONS_PATH,
        title="Non-GET Endpoints — OpenAPI Response Fix Suggestions",
    )

    print(f"\nReport generated: {REPORT_PATH}")
    print(f"Fix suggestions generated: {SUGGESTIONS_PATH}")
    print(f"Summary: total={len(results)} "
          f"pass={counts.get('PASS', 0)} "
          f"fail={counts.get('FAIL', 0)} "
          f"skip={counts.get('SKIP', 0)}")
    print(f"\nCaptured resources:\n{json.dumps(ctx, indent=2)}")

    try:
        client.close()
    except Exception:
        pass

    return 0 if counts.get("FAIL", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

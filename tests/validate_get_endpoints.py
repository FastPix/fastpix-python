"""GET endpoint validation harness — matches the Node SDK harness format.

Pipeline per endpoint:

1. Resolve path/query params from ``tests/get_endpoints_fixtures.json``
   (placeholder UUID fallback for unresolved required path params).
2. Call the raw API with httpx + HTTP Basic auth.
3. Call the matching SDK method with the same effective request.
4. Validate the raw response against the OpenAPI response schema for the
   returned status code via the Node ``openapi-response-validator`` sidecar.
5. Diff JSON paths between raw API JSON and SDK output (case-sensitive,
   ``[]`` treated as missing) — also collect empty-array omissions.
6. Status = PASS iff ``openapi_valid ∧ sdk_parse_ok ∧ no missing on either side``.
7. Write ``tests/artifacts/<operation_id>.api.json`` + ``.sdk.json``
   (sanitized: fastpix.io → fastpix.com).
8. Emit ``tests/GET_ENDPOINTS_OPENAPI_RESPONSE_VALIDATION_REPORT.md`` and
   ``tests/GET_ENDPOINTS_OPENAPI_RESPONSE_FIX_SUGGESTIONS.md``.

Run: ``FASTPIX_USERNAME=… FASTPIX_PASSWORD=… python -m tests.validate_get_endpoints``
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping

from tests._common import (
    ARTIFACTS_GET,
    EndpointResult,
    REPO_ROOT,
    build_dispatch,
    build_sdk,
    call_sdk_method,
    cap_for_preview,
    collect_empty_array_paths,
    get_sidecar,
    iter_operations,
    kwargs_to_snake,
    load_spec,
    normalize_exception,
    path_diff,
    require_credentials,
    spec_server_url,
    substitute_path,
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
REPORT_PATH = TESTS_DIR / "GET_ENDPOINTS_OPENAPI_RESPONSE_VALIDATION_REPORT.md"
SUGGESTIONS_PATH = TESTS_DIR / "GET_ENDPOINTS_OPENAPI_RESPONSE_FIX_SUGGESTIONS.md"
FIXTURES_PATH = TESTS_DIR / "get_endpoints_fixtures.json"


def load_fixtures() -> Dict[str, Any]:
    if not FIXTURES_PATH.exists():
        return {"operations": {}}
    with FIXTURES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def required_path_params(op: Mapping[str, Any]) -> List[str]:
    return [
        p["name"]
        for p in (op.get("parameters") or [])
        if p.get("in") == "path"
    ]


def raw_call(httpx_mod, base_url: str, path: str, query: Mapping[str, Any], user: str, pwd: str):
    """Raw GET with one retry on 404 (the API occasionally 404s mid-run for
    resources that exist; standalone curls return 200 immediately)."""
    auth = (user, pwd)
    full_url = base_url + path
    flat_query: List = []
    for k, v in (query or {}).items():
        if isinstance(v, list):
            for item in v:
                flat_query.append((k, item))
        else:
            flat_query.append((k, v))
    resp = httpx_mod.get(full_url, params=flat_query, auth=auth, timeout=60.0,
                         headers={"Accept": "application/json"})
    if resp.status_code == 404:
        time.sleep(1.5)
        resp = httpx_mod.get(full_url, params=flat_query, auth=auth, timeout=60.0,
                             headers={"Accept": "application/json"})
    return resp


def main() -> int:
    require_credentials()
    spec = load_spec()
    base_url = spec_server_url(spec)
    components = spec.get("components") or {}
    fixtures = load_fixtures().get("operations") or {}
    dispatch = build_dispatch()

    try:
        import httpx
    except ImportError:
        print("httpx not installed. Run `pip install -e .` in the repo root.", file=sys.stderr)
        return 2

    # Warm up the sidecar before the first call so its readiness log doesn't
    # interleave with our per-endpoint progress lines.
    get_sidecar()

    # Build the SDK with a httpx client hooked to capture the raw wire-format
    # response. We then use those exact wire-bytes as both the .api.json
    # artifact AND as the input to SDK parsing. One HTTP call per endpoint
    # eliminates the timing drift we'd see from two separate calls (timestamps
    # off by 1-2s, response shape might shift, etc.).
    raw_state: Dict[str, Any] = {}

    def _capture_hook(response):
        if "api.fastpix" not in str(response.request.url):
            return
        response.read()
        body_json: Any = None
        try:
            body_json = response.json()
        except Exception:
            body_json = None
        raw_state.update(
            url=str(response.request.url),
            status=response.status_code,
            body_json=body_json,
        )

    client = httpx.Client(
        follow_redirects=True,
        event_hooks={"response": [_capture_hook]},
        timeout=120.0,
    )
    sdk = build_sdk(client=client)
    user, pwd = require_credentials()

    # Enumerate GET operations first so we know the total upfront.
    get_ops = [
        (path, method, op)
        for path, method, op in iter_operations(spec)
        if method == "get"
    ]
    total = len(get_ops)

    results: List[EndpointResult] = []
    for idx, (path, method, op) in enumerate(get_ops, start=1):
        op_id = op.get("operationId") or f"{method}_{path}"
        print(f"[{idx}/{total}] Processing: {op_id} ({path})", flush=True)

        fixture = fixtures.get(op_id) or {}
        path_params = dict(fixture.get("pathParams") or {})
        query = dict(fixture.get("query") or {})

        # Auto-fill any unresolved path params with the placeholder UUID
        for name in required_path_params(op):
            if name not in path_params:
                path_params[name] = "00000000-0000-0000-0000-000000000000"

        concrete_path = substitute_path(path, path_params)

        # --- single HTTP call via SDK (raw wire-bytes captured by hook) ---
        api_json: Any = None
        api_status: int = 0
        api_error: str = ""
        sdk_value: Any = None
        sdk_parse_ok = False
        sdk_parse_error: str = ""
        binding = dispatch.get(op_id)
        if binding is None:
            sdk_parse_error = f"SDK method missing for operationId={op_id!r}"
            sdk_value = None
            print(f"  ⚠️  SDK method not exposed by the package", flush=True)
            # Still make a raw call so we can record the API response
            try:
                resp = raw_call(httpx, base_url, concrete_path, query, user, pwd)
                api_status = resp.status_code
                try:
                    api_json = resp.json()
                except Exception:
                    api_json = {"_raw_text": resp.text[:2000]}
            except Exception as exc:
                api_error = f"{type(exc).__name__}: {exc}"
        else:
            invocation: Dict[str, Any] = {}
            invocation.update(kwargs_to_snake(path_params))
            invocation.update(kwargs_to_snake(query))
            for attempt in range(2):
                raw_state.clear()
                try:
                    ret = call_sdk_method(sdk, binding, invocation)
                    sdk_value = to_jsonable(ret)
                    sdk_parse_ok = True
                    break
                except Exception as exc:
                    err_payload = normalize_exception(exc)
                    sdk_value = err_payload
                    sdk_parse_error = f"{type(exc).__name__}: {exc}"
                    status_code = err_payload.get("status_code") if isinstance(err_payload, dict) else None
                    if attempt == 0 and status_code == 404:
                        time.sleep(1.5)
                        continue
                    if not sdk_parse_ok:
                        print(f"  ⚠️  SDK call failed: {sdk_parse_error[:300]}", flush=True)
                    break
            # Pull the wire-format response captured by the hook
            api_status = raw_state.get("status") or 0
            api_json = raw_state.get("body_json")

        # --- OpenAPI validation (via Node sidecar) ---
        openapi_valid: bool = True
        openapi_errors: List[Dict[str, Any]] = []
        if isinstance(api_json, dict) and api_status:
            openapi_valid, openapi_errors = validate_response(api_json, op, api_status, components)

        # --- diff (only meaningful on 2xx with both successful) ---
        if (
            sdk_parse_ok
            and api_status
            and 200 <= api_status < 300
            and isinstance(api_json, (dict, list))
        ):
            missing_in_sdk, missing_in_api = path_diff(api_json, sdk_value)
            empty_omitted_sdk = sorted(collect_empty_array_paths(api_json) - collect_empty_array_paths(sdk_value))
            empty_omitted_api = sorted(collect_empty_array_paths(sdk_value) - collect_empty_array_paths(api_json))
        else:
            missing_in_sdk, missing_in_api, empty_omitted_sdk, empty_omitted_api = [], [], [], []

        # --- status (PASS / FAIL only — matches Node SDK harness) ---
        if (
            api_status and 200 <= api_status < 300
            and openapi_valid
            and sdk_parse_ok
            and not missing_in_sdk
            and not missing_in_api
        ):
            status = "PASS"
        else:
            status = "FAIL"

        # --- artifacts: raw response payload only. .api.json contains exactly
        # what the API returned; .sdk.json contains exactly what the SDK
        # produced (or the SDK's error message if it threw). Both files are
        # directly diff-able with `diff <op>.api.json <op>.sdk.json`.
        api_file = f"tests/artifacts/{op_id}.api.json"
        sdk_file = f"tests/artifacts/{op_id}.sdk.json"
        write_artifact(ARTIFACTS_GET / f"{op_id}.api.json", api_json)
        write_artifact(ARTIFACTS_GET / f"{op_id}.sdk.json", sdk_value)

        note: str = ""
        if binding is None:
            note = "Spec defines this endpoint but the SDK does not expose a matching method — SDK regeneration required."
        elif api_status and 400 <= api_status < 500:
            placeholder = any(
                isinstance(v, str)
                and (v.startswith("REPLACE_WITH_") or v.startswith("00000000-") or v.startswith("your-"))
                for v in path_params.values()
            )
            if api_status == 404:
                note = ("API returned 404 — supplied ID is not present in the credentialed workspace; "
                        "SDK behaviour is correct.") if not placeholder else \
                       "Placeholder path param produced 404 — supply a real ID to enable this endpoint."

        result = EndpointResult(
            endpoint=path,
            method=method,
            operation_id=op_id,
            status=status,
            openapi_valid=openapi_valid,
            openapi_errors=openapi_errors,
            sdk_parse_ok=sdk_parse_ok,
            sdk_parse_error=sdk_parse_error or None,
            missing_in_sdk=missing_in_sdk,
            missing_in_api=missing_in_api,
            empty_arrays_omitted_in_sdk=empty_omitted_sdk,
            empty_arrays_omitted_in_api=empty_omitted_api,
            api_response_file=api_file,
            sdk_response_file=sdk_file,
            api_response_preview=cap_for_preview(api_json) if api_json is not None else None,
            sdk_response_preview=cap_for_preview(sdk_value) if sdk_value is not None else None,
            api_status=api_status or None,
            note=note or None,
        )
        # Attach fix suggestions for failing endpoints so they're stable on disk.
        if status == "FAIL":
            result.fix_suggestions = generate_fix_suggestions(result)
        results.append(result)
        print(f"  ✓ Completed: {op_id} - {status}", flush=True)

    counts = write_validation_report(
        results, REPORT_PATH,
        title="GET Endpoints — OpenAPI Response Validation Report",
        label_total="Total GET endpoints",
    )
    write_fix_suggestions(
        results, SUGGESTIONS_PATH,
        title="GET Endpoints — OpenAPI Response Fix Suggestions",
    )

    print(f"Report generated: {REPORT_PATH}")
    print(f"Fix suggestions generated: {SUGGESTIONS_PATH}")
    print(f"Summary: total={len(results)} "
          f"pass={counts.get('PASS', 0)} "
          f"fail={counts.get('FAIL', 0)} "
          f"skip={counts.get('SKIP', 0)}")

    return 0 if counts.get("FAIL", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

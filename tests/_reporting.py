"""Report + fix-suggestion writers — matches the Node SDK harness output format.

Two markdown files per harness invocation:

* ``<PREFIX>_OPENAPI_RESPONSE_VALIDATION_REPORT.md`` — summary + consolidated
  table + per-endpoint detail with API/SDK previews.
* ``<PREFIX>_OPENAPI_RESPONSE_FIX_SUGGESTIONS.md`` — heuristic suggestions for
  spec/SDK fixes for every failing endpoint.

The fix-suggestion heuristics are a port of those in
``../../node-sdk/tests/validate-get-endpoints.ts`` (search for
``generateFixSuggestions``).
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from tests._common import EndpointResult

_ERR_ONEOF = "must match exactly one schema in oneOf"
_ERR_ALLOWED_VALUES = "must be equal to one of the allowed values"
_NONE_BULLET = "- None"


# ---------------------------------------------------------------------------
# Fix-suggestion heuristics
# ---------------------------------------------------------------------------


def _has_openapi_error(r: EndpointResult, substring: str) -> bool:
    return any(substring in (e.get("message") or "") for e in r.openapi_errors)


def _openapi_error_paths(r: EndpointResult) -> List[str]:
    return [str(e.get("path") or "") for e in r.openapi_errors if e.get("path")]


def _suggest_enum_oneof(r: EndpointResult, paths: List[str]) -> List[Dict[str, str]]:
    """Heuristics 1-3: tracks oneOf overlap and enum mismatches."""
    out: List[Dict[str, str]] = []

    # 1) tracks oneOf overlap
    if _has_openapi_error(r, _ERR_ONEOF) and any(
        "tracks" in p for p in paths
    ):
        out.append({
            "title": "Fix `tracks[].oneOf` overlap by constraining `type` per track schema",
            "why": (
                "The current track schemas overlap (e.g. `type` is a free string and distinguishing "
                "fields are not required), so a single track object can match multiple branches. "
                "`oneOf` requires exactly one match."
            ),
            "where": (
                "In `openapi.yaml`: "
                "`components/schemas/{VideoTrack,VideoTrackForGetAll,AudioTrack,SubtitleTrack}.properties.type`"
            ),
            "paste_yaml": (
                "# Apply these changes inside each schema's `properties:` block:\n"
                "\n# VideoTrack (and VideoTrackForGetAll)\n"
                "type:\n  type: string\n  enum: [video]\n  example: video\n"
                "\n# AudioTrack\n"
                "type:\n  type: string\n  enum: [audio]\n  example: audio\n"
                "\n# SubtitleTrack\n"
                "type:\n  type: string\n  enum: [subtitle]\n  example: subtitle\n"
            ),
        })

    # 2) sourceResolution enum
    if _has_openapi_error(r, _ERR_ALLOWED_VALUES) and any(
        "sourceResolution" in p for p in paths
    ):
        out.append({
            "title": "Fix `sourceResolution` enum mismatch (API may return values without `p`)",
            "why": (
                "The API can return values like `\"480\"` but the spec constrains the enum to "
                "`\"480p\"`-style values."
            ),
            "where": (
                "In `openapi.yaml`: under the relevant media response schema(s) "
                "`sourceResolution:` field definition"
            ),
        })

    # 3) maxResolution enum
    if _has_openapi_error(r, _ERR_ALLOWED_VALUES) and any(
        "maxResolution" in p for p in paths
    ):
        out.append({
            "title": "Allow `\"NA\"` (or other API-returned values) in `maxResolution` enum",
            "why": (
                "The API can return values like `\"NA\"` for unprocessed media; the spec enum "
                "rejects them."
            ),
            "where": (
                "In `openapi.yaml`: media response schemas' `maxResolution:` field definition"
            ),
        })

    return out


def _suggest_schema_overlap(r: EndpointResult, paths: List[str]) -> List[Dict[str, str]]:
    """Heuristics 4-6: redundant/overlapping oneOf and nullable drift."""
    out: List[Dict[str, str]] = []

    # 4) /data/dimensions redundant oneOf
    if _has_openapi_error(r, _ERR_ONEOF) and (
        r.endpoint == "/data/dimensions" or any("dimensions" in p for p in paths)
    ):
        out.append({
            "title": "Remove redundant `oneOf` on `/data/dimensions` response schema",
            "why": (
                "`data` is defined as `oneOf: [array<string>, $ref: Dimensions]` and "
                "`Dimensions` itself is also `array<string>`, so valid responses can match "
                "multiple branches."
            ),
            "where": (
                "In `openapi.yaml`: "
                "`paths./data/dimensions.get.responses.200.content.application/json.schema.properties.data.oneOf`"
            ),
        })

    # 5) integer-vs-number oneOf overlap
    if _has_openapi_error(r, _ERR_ONEOF) and any(
        "value" in p for p in paths
    ):
        out.append({
            "title": "Avoid `oneOf: [integer, number]` overlaps (integers are also numbers)",
            "why": (
                "In JSON Schema, `integer` is a subset of `number`. A value like `0` matches both, "
                "causing oneOf validation errors."
            ),
            "where": "In `openapi.yaml`: metrics schemas that use `oneOf: [integer, number]`",
        })

    return out


def _suggest_field_issues(r: EndpointResult, paths: List[str]) -> List[Dict[str, str]]:
    """Heuristics 6-9: field-level drift (nullable, phantom, envelope, casing)."""
    out: List[Dict[str, str]] = []

    # 6) fpApiVersion nullable
    if _has_openapi_error(r, "must be string") and any("fpApiVersion" in p for p in paths):
        out.append({
            "title": "Make `fpApiVersion` nullable in the spec",
            "why": "The API can return `null` for fpApiVersion but the schema declares `string` only.",
            "where": "In `openapi.yaml`: `components/schemas/Views.properties.fpApiVersion`",
        })

    # 7) phantom Optional fields the API never returns
    if r.missing_in_api:
        out.append({
            "title": "Remove phantom Optional fields from response models",
            "why": (
                "The SDK's response model declares fields the API doesn't return — pydantic populates "
                "them as `None`, leaving end-users to filter them out. Either remove the fields from "
                "the spec (preferred) or surface them only when the API actually returns them."
            ),
            "where": (
                "In `openapi.yaml`: response schemas for `" + r.operation_id + "`; "
                "fields to inspect: " + ", ".join(f"`{p}`" for p in r.missing_in_api)
            ),
        })

    # 8) SDK response envelope drift (e.g. list_signing_keys flat vs wrapped)
    if any(p.startswith(("[]", "[].")) for p in r.missing_in_api):
        out.append({
            "title": "Fix response envelope: SDK is unwrapping `{success, data, pagination}` to a flat list",
            "why": (
                "The API returns a wrapped envelope but the SDK return type is a bare `List[...]`. "
                "End-users lose `success`/`pagination`. The response model needs the full envelope."
            ),
            "where": (
                "In the generated SDK: response model for `" + r.operation_id + "`. "
                "Update the operation's response schema in `openapi.yaml` to the full envelope and regenerate."
            ),
        })

    # 9) Wire-format casing (metadata vs metaData)
    if any(p in {"metadata", "metaData"} for p in r.missing_in_sdk + r.missing_in_api):
        out.append({
            "title": "Fix wire-format casing: the SDK uses `metaData`, the API uses `metadata`",
            "why": (
                "The Speakeasy-generated model declares the field as `metaData` (camelCase with capital D). "
                "The actual API response uses `metadata`. End-users get `None` for `meta_data` "
                "while the actual `metadata` payload is dropped."
            ),
            "where": (
                "Either fix `openapi.yaml` to spell the field `metadata` everywhere, "
                "or add a wire-format alias in the SDK's response model."
            ),
        })

    return out


def _suggest_fixture_issues(r: EndpointResult) -> List[Dict[str, str]]:
    """Heuristics 10-11: fixture data problems (missing param, stale ID)."""
    out: List[Dict[str, str]] = []

    # 10) Missing required query param fixture
    if r.sdk_parse_error and "missing 1 required keyword-only argument" in r.sdk_parse_error:
        m = re.search(r"argument:\s*'([^']+)'", r.sdk_parse_error)
        param = m.group(1) if m else "(unknown)"
        out.append({
            "title": f"Add required query param `{param}` to the fixture for this operation",
            "why": (
                "The SDK method requires this kwarg but the fixture didn't supply it, causing a "
                "TypeError before the API call could be made."
            ),
            "where": (
                "`tests/get_endpoints_fixtures.json` -> "
                f"`operations.{r.operation_id}.query.{param}`"
            ),
        })

    # 11) API returned 4xx for the supplied ID
    if r.api_status and 400 <= r.api_status < 500 and r.api_status not in (422,) and not _has_openapi_error(r, ""):
        # only suggest the fixture-ID swap if no openapi errors (otherwise other fixes apply)
        if r.api_status == 404:
            out.append({
                "title": "Supply a workspace-local ID for this operation's fixture",
                "why": (
                    f"API returned {r.api_status} — the supplied ID is not present in the credentialed workspace. "
                    "The SDK is behaving correctly; the fixture data is stale."
                ),
                "where": f"`tests/get_endpoints_fixtures.json` -> `operations.{r.operation_id}.pathParams`",
            })

    return out


def generate_fix_suggestions(r: EndpointResult) -> List[Dict[str, str]]:
    """Port of the Node SDK's heuristic suggestion engine."""
    paths = _openapi_error_paths(r)
    return (
        _suggest_enum_oneof(r, paths)
        + _suggest_schema_overlap(r, paths)
        + _suggest_field_issues(r, paths)
        + _suggest_fixture_issues(r)
    )


# ---------------------------------------------------------------------------
# Report writers
# ---------------------------------------------------------------------------


def _iso_now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _status_icon(status: str) -> str:
    if status == "PASS":
        return "✅ PASS"
    if status == "FAIL":
        return "❌ FAIL"
    return "⏭ SKIP"


def _append_bullet_section(lines: List[str], header: str, items: Sequence[Any]) -> None:
    """Append a '**Header — N**' section followed by a bullet list (or '- None')."""
    lines.append(f"{header} — {len(items)}**")
    lines.append("")
    if not items:
        lines.append(_NONE_BULLET)
    else:
        for p in items:
            lines.append(f"- `{p}`")
    lines.append("")


def _append_preview(lines: List[str], label: str, preview: Optional[str]) -> None:
    """Append a fenced JSON preview block, if a preview is present."""
    if not preview:
        return
    lines.append(f"**{label}**")
    lines.append("")
    lines.append("```json")
    lines.append(preview)
    lines.append("```")
    lines.append("")


def _append_openapi_errors(lines: List[str], r: EndpointResult, bullet: str) -> None:
    """Append observed OpenAPI errors using the given bullet prefix ('-' or '  -')."""
    for e in r.openapi_errors:
        loc = f"`{e['path']}`" if e.get("path") else ""
        msg = e.get("message") or ""
        lines.append(f"{bullet} {loc} {msg}".rstrip())


def _render_endpoint_detail(r: EndpointResult) -> List[str]:
    """Render the per-endpoint detail block for the validation report."""
    lines: List[str] = []
    lines.append(f"### {r.operation_id} (`{r.endpoint}`)")
    lines.append("")
    lines.append(f"- **Status**: {r.status}")
    if r.note:
        lines.append(f"- **Note**: {r.note}")
    lines.append(f"- **OpenAPI valid**: {'yes' if r.openapi_valid else 'no'}")
    if not r.openapi_valid and r.openapi_errors:
        lines.append("- **OpenAPI errors**:")
        _append_openapi_errors(lines, r, "  -")
    lines.append(f"- **SDK parse**: {'ok' if r.sdk_parse_ok else 'failed'}")
    if not r.sdk_parse_ok and r.sdk_parse_error:
        lines.append(f"- **SDK parse error**: {r.sdk_parse_error}")
    if r.api_status is not None:
        lines.append(f"- **API HTTP status**: `{r.api_status}`")
    if r.api_response_file:
        lines.append(f"- **API response file**: `{r.api_response_file}`")
    if r.sdk_response_file:
        lines.append(f"- **SDK response file**: `{r.sdk_response_file}`")
    lines.append("")
    _append_preview(lines, "API response (preview)", r.api_response_preview)
    _append_preview(lines, "SDK response (preview)", r.sdk_response_preview)
    _append_bullet_section(
        lines, "**Missing in SDK (present in API)", r.missing_in_sdk
    )
    _append_bullet_section(
        lines, "**Missing in API (present in SDK)", r.missing_in_api
    )
    _append_bullet_section(
        lines, "**Empty arrays omitted by SDK", r.empty_arrays_omitted_in_sdk
    )
    _append_bullet_section(
        lines, "**Empty arrays omitted by API", r.empty_arrays_omitted_in_api
    )
    return lines


def write_validation_report(
    results: Sequence[EndpointResult],
    out_path: Path,
    *,
    title: str,
    label_total: str,
) -> Dict[str, int]:
    """Write the main report. Returns counts dict."""
    counts = {"PASS": 0, "FAIL": 0, "SKIP": 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated: {_iso_now()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **{label_total}**: {len(results)}")
    lines.append(f"- **PASS**: {counts['PASS']}")
    lines.append(f"- **FAIL**: {counts['FAIL']}")
    lines.append(f"- **SKIP**: {counts['SKIP']}")
    lines.append("")
    lines.append("## Consolidated report")
    lines.append("")
    lines.append(
        "| Endpoint | OperationId | OpenAPI valid | SDK parse | "
        "Missing in SDK (present in API) | Missing in API (present in SDK) | "
        "Empty arrays omitted by SDK | Status |"
    )
    lines.append("|---|---|---:|---:|---|---|---|---|")
    for r in results:
        oa = "✅" if r.openapi_valid else "❌"
        sdk = "✅" if r.sdk_parse_ok else "❌"
        ms = ", ".join(f"`{p}`" for p in r.missing_in_sdk) or "None"
        ma = ", ".join(f"`{p}`" for p in r.missing_in_api) or "None"
        ea = ", ".join(f"`{p}`" for p in r.empty_arrays_omitted_in_sdk) or "None"
        status_icon = _status_icon(r.status)
        lines.append(
            f"| `{r.endpoint}` | `{r.operation_id}` | {oa} | {sdk} | {ms} | {ma} | {ea} | {status_icon} |"
        )
    lines.append("")
    lines.append("## Per-endpoint details (full missing parameter lists)")
    lines.append("")
    for r in results:
        lines.extend(_render_endpoint_detail(r))

    out_path.write_text("\n".join(lines))
    return counts


def _render_suggestions(suggestions: Sequence[Dict[str, str]]) -> List[str]:
    """Render the '### Suggested fixes' section for one endpoint."""
    lines: List[str] = ["### Suggested fixes", ""]
    if not suggestions:
        lines.append("- No heuristic suggestions available for this failure yet.")
        lines.append("")
        return lines
    for s in suggestions:
        lines.append(f"- **{s['title']}**")
        lines.append(f"  - **why**: {s.get('why', '')}")
        if s.get("where"):
            lines.append(f"  - **where**: {s['where']}")
        if s.get("paste_yaml"):
            lines.append("  - **paste**:")
            lines.append("")
            lines.append("```yaml")
            lines.append(s["paste_yaml"])
            lines.append("```")
        lines.append("")
    return lines


def _render_fix_entry(r: EndpointResult) -> List[str]:
    """Render one failing endpoint's section in the fix-suggestions report."""
    lines: List[str] = []
    lines.append(f"## {r.operation_id} (`{r.endpoint}`)")
    lines.append("")
    lines.append(f"- **Status**: {r.status}")
    lines.append(f"- **OpenAPI valid**: {'yes' if r.openapi_valid else 'no'}")
    lines.append(f"- **SDK parse**: {'ok' if r.sdk_parse_ok else 'failed'}")
    if r.api_response_file:
        lines.append(f"- **API artifact**: `{r.api_response_file}`")
    if r.sdk_response_file:
        lines.append(f"- **SDK artifact**: `{r.sdk_response_file}`")
    lines.append("")
    if not r.openapi_valid and r.openapi_errors:
        lines.append("### Observed OpenAPI errors")
        lines.append("")
        _append_openapi_errors(lines, r, "-")
        lines.append("")
    suggestions = r.fix_suggestions or generate_fix_suggestions(r)
    lines.extend(_render_suggestions(suggestions))
    return lines


def write_fix_suggestions(
    results: Sequence[EndpointResult],
    out_path: Path,
    *,
    title: str,
) -> int:
    """Write the fix-suggestions report. Returns count of failing endpoints."""
    failing = [r for r in results if r.status == "FAIL"]
    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated: {_iso_now()}")
    lines.append("")
    lines.append(f"Total failing endpoints: {len(failing)}")
    lines.append("")
    for r in failing:
        lines.extend(_render_fix_entry(r))
    out_path.write_text("\n".join(lines))
    return len(failing)

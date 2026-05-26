"""Broken-link checker for repository markdown.

Walks every ``*.md`` file (excluding ``node_modules``, ``.venv``, ``dist``,
``build``, ``__pycache__``, ``.git``), extracts URLs, HEADs each with a 15s
timeout, falls back to ``GET Range: bytes=0-0`` on 403/405/0. Concurrency 10.

Pass criterion: every ``fastpix.com/docs/*`` URL returns 2xx or 3xx. Acknowledged
expected-broken patterns (signed GCS URLs, example.com, placeholder thumbnails)
are reported but do not affect the exit code.

Run: ``python -m tests.check_broken_links``
"""

from __future__ import annotations

import asyncio
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = REPO_ROOT / "tests" / "BROKEN_LINKS_REPORT.md"

EXCLUDE_DIRS = {"node_modules", ".venv", ".venv-tests", "dist", "build", "__pycache__", ".git"}
# Generated artifacts that echo the broken URLs they describe — would create a
# self-referential cycle if scanned.
EXCLUDE_FILES = {"tests/BROKEN_LINKS_REPORT.md"}
URL_RE = re.compile(r"https?://[^\s\"'<>()\[\]`]+")
TRAILING_PUNCT = '.,;:!?)]}>"\''
CONCURRENCY = 10
TIMEOUT_S = 15.0

# Patterns we expect to fail and do not count toward exit-code failure
ACKNOWLEDGED_BROKEN_PATTERNS = [
    re.compile(r"^https?://example\.com"),
    re.compile(r"^https?://(?:[^/]+\.)?googleapis\.com/.*X-Goog-Signature="),
    re.compile(r"^https?://storage\.googleapis\.com/.*GoogleAccessId="),
    re.compile(r"^https?://images\.fastpix\.com/[^?\s]+\?[^\s]*placeholder", re.IGNORECASE),
    re.compile(r"^https?://[^/]+/REPLACE_WITH_"),
]


def is_acknowledged(url: str) -> bool:
    return any(p.search(url) for p in ACKNOWLEDGED_BROKEN_PATTERNS)


def walk_markdown_files(root: Path):
    for path in root.rglob("*.md"):
        rel = path.relative_to(root)
        if set(rel.parts) & EXCLUDE_DIRS:
            continue
        if str(rel) in EXCLUDE_FILES:
            continue
        yield path


def extract_urls(text: str) -> List[str]:
    urls: List[str] = []
    for raw in URL_RE.findall(text):
        u = raw.rstrip(TRAILING_PUNCT)
        # Balance trailing parens — useful for markdown like (https://x.com/foo).
        if u.endswith(")") and u.count("(") < u.count(")"):
            u = u.rstrip(")")
        if u:
            urls.append(u)
    return urls


async def check_one(client, url: str, semaphore: asyncio.Semaphore) -> Tuple[str, int, str]:
    async with semaphore:
        try:
            r = await client.head(url, follow_redirects=True, timeout=TIMEOUT_S)
            if r.status_code in (0, 403, 405) or r.status_code >= 500:
                r = await client.get(url, follow_redirects=True, timeout=TIMEOUT_S,
                                     headers={"Range": "bytes=0-0"})
            return url, r.status_code, ""
        except Exception as exc:  # noqa: BLE001
            return url, 0, f"{type(exc).__name__}: {exc}"


async def run() -> int:
    try:
        import httpx
    except ImportError:
        print("httpx not installed. Run `pip install httpx`.", file=sys.stderr)
        return 2

    url_to_files: Dict[str, Set[Path]] = defaultdict(set)
    for md in walk_markdown_files(REPO_ROOT):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        for u in extract_urls(text):
            url_to_files[u].add(md)

    all_urls = sorted(url_to_files)
    print(f"Scanning {len(all_urls)} unique URLs across "
          f"{len({f for files in url_to_files.values() for f in files})} markdown files...",
          flush=True)

    semaphore = asyncio.Semaphore(CONCURRENCY)
    # A browser-like User-Agent is required: docs sites and CDNs commonly 403
    # the default httpx UA, which would mask working URLs as broken.
    async with httpx.AsyncClient(
        http2=False,
        verify=True,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    ) as client:
        results = await asyncio.gather(*(check_one(client, u, semaphore) for u in all_urls))

    rows: List[Tuple[str, int, str, List[str], bool]] = []
    fail_real = 0
    fail_acknowledged = 0
    ok = 0
    for url, status, err in results:
        is_ack = is_acknowledged(url)
        files = sorted(str(p.relative_to(REPO_ROOT)) for p in url_to_files[url])
        ok_status = 200 <= status < 400
        if not ok_status:
            if is_ack:
                fail_acknowledged += 1
            else:
                fail_real += 1
        else:
            ok += 1
        rows.append((url, status, err, files, is_ack))

    lines: List[str] = []
    lines.append("# Broken Links Report\n")
    lines.append(f"- Total URLs: **{len(all_urls)}**")
    lines.append(f"- OK (2xx/3xx): **{ok}**")
    lines.append(f"- Broken (real): **{fail_real}**")
    lines.append(f"- Broken (acknowledged patterns): **{fail_acknowledged}**\n")

    fastpix_docs_broken = [
        (url, status, err, files)
        for url, status, err, files, ack in rows
        if not (200 <= status < 400) and "fastpix.com/docs" in url and not ack
    ]
    lines.append(f"## fastpix.com/docs broken ({len(fastpix_docs_broken)})\n")
    if not fastpix_docs_broken:
        lines.append("_None._\n")
    else:
        lines.append("| URL | Status | Files |\n|---|---:|---|")
        for url, status, err, files in fastpix_docs_broken:
            files_str = ", ".join(f"`{f}`" for f in files)
            lines.append(f"| {url} | {status or 'ERR'} | {files_str} |")
        lines.append("")

    lines.append("## All broken URLs\n")
    lines.append("| URL | Status | Acknowledged | Files | Error |\n|---|---:|---|---|---|")
    for url, status, err, files, ack in rows:
        if 200 <= status < 400:
            continue
        files_str = ", ".join(f"`{f}`" for f in files)
        lines.append(
            f"| {url} | {status or 'ERR'} | {'yes' if ack else 'no'} | "
            f"{files_str} | {err} |"
        )
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {REPORT_PATH.relative_to(REPO_ROOT)}")

    # Exit-code policy: only real fastpix.com/docs failures fail the run.
    return 0 if not fastpix_docs_broken else 1


def main() -> int:
    return asyncio.run(run())


if __name__ == "__main__":
    raise SystemExit(main())

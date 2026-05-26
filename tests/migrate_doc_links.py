"""Rewrite every stale FastPix doc URL in the repo to match ``fixed.yaml``.

Background: ``old-yaml.yaml`` shipped doc links pointing at
``https://docs.fastpix.io/...``. A naive ``.io → .com`` host swap landed across
the repo, producing dead ``https://docs.fastpix.com/...`` URLs. The docs team
then restructured the doc site — the working URLs now live under
``https://fastpix.com/docs/<section>/<slug>`` in ``fixed.yaml``.

Strategy (text-link pairing, not URL pairing):

* Build an anchor-text → new-URL index from ``fixed.yaml`` (authoritative).
  We accept both ``<a href="URL">TEXT</a>`` and markdown ``[TEXT](URL)``.
* Walk every source file (.md, .py, .yaml — excluding the two spec files
  themselves and generated harness reports). For each stale link found
  (anchor or markdown form), look up its TEXT in the fixed.yaml index and
  substitute the stale URL with the new URL.
* Also build the bare URL→URL substitution from old-yaml↔fixed.yaml pairings
  (covers cases where the URL appears free-standing, with no link wrapper).

Python docstrings escape quotes (``href=\\\"URL\\\"``); we accept both escaped
and unescaped forms.

URLs that have no anchor-text match in ``fixed.yaml`` are reported and left
alone — those are out of scope for this migration (per user instruction).

Run: ``python -m tests.migrate_doc_links``         (writes changes)
     ``python -m tests.migrate_doc_links --check`` (dry-run, non-zero exit if changes pending)
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
OLD_YAML = REPO_ROOT / "old-yaml.yaml"
NEW_YAML = REPO_ROOT / "fixed.yaml"

EXCLUDE_DIRS = {"node_modules", ".venv", ".venv-tests", "dist", "build", "__pycache__", ".git"}
EXCLUDE_FILES = {
    "tests/BROKEN_LINKS_REPORT.md",
    "tests/GET_ENDPOINTS_VALIDATION_REPORT.md",
    "tests/NON_GET_ENDPOINTS_VALIDATION_REPORT.md",
    "old-yaml.yaml",
    "fixed.yaml",
    # The script's own URL maps contain stale URLs as dict keys — must not be
    # rewritten by its own walk, or future re-runs would no longer match.
    "tests/migrate_doc_links.py",
}
SCAN_EXTENSIONS = (".md", ".py", ".yaml", ".yml")

# Manual mappings for URLs that exist in the Node SDK but not in fixed.yaml.
# Source of truth: ../node-sdk/README.md (anchor-text matched between repos).
MANUAL_URL_MAP: Dict[str, str] = {
    "https://docs.fastpix.com/docs/basic-authentication":
        "https://fastpix.com/docs/getting-started/activate-your-account#authentication-format",
    "https://docs.fastpix.com/docs/live-stream-overview":
        "https://fastpix.com/docs/get-started/live-overview",
    "https://docs.fastpix.com/docs/video-data-overview":
        "https://fastpix.com/docs/concepts/what-video-data-do-we-capture",
    "https://docs.fastpix.com/reference/signingkeys-overview":
        "https://fastpix.com/docs/video-security/secure-media-access-with-jwts",
}
# URLs that the Node SDK chose to remove rather than redirect. The wrapping
# `<a href="STALE">TEXT</a>` is unwrapped to just `TEXT`.
ANCHOR_REMOVALS: Set[str] = {
    "https://docs.fastpix.com/reference/create-playbackid-of-stream",
}

STALE_HOST_RE = re.compile(r"https?://docs\.fastpix\.(?:io|com)/[^\s\"'<>()\[\]`\\]+")
# Accept both real and escaped quotes around URL.
ANCHOR_RE = re.compile(
    r'<a\s+href=\\?"(https?://[^"\\]+)\\?"[^>]*>([^<]+)</a>'
)
MARKDOWN_RE = re.compile(
    r'\[([^\]]+)\]\((https?://docs\.fastpix\.(?:io|com)/[^)\s]+)\)'
)


def extract_fixed_anchor_index(yaml_path: Path) -> Dict[str, str]:
    """anchor_text -> new URL, taken from fixed.yaml."""
    text = yaml_path.read_text(encoding="utf-8")
    idx: Dict[str, Set[str]] = defaultdict(set)
    for url, label in ANCHOR_RE.findall(text):
        idx[label.strip()].add(url)
    for label, url in re.findall(
        r'\[([^\]]+)\]\((https?://(?:www\.)?fastpix\.com/[^)\s]+)\)', text
    ):
        idx[label.strip()].add(url)
    # Only keep unambiguous pairings.
    return {label: next(iter(urls)) for label, urls in idx.items() if len(urls) == 1}


def extract_text_to_url(yaml_path: Path) -> Dict[str, Set[str]]:
    text = yaml_path.read_text(encoding="utf-8")
    out: Dict[str, Set[str]] = defaultdict(set)
    for url, label in ANCHOR_RE.findall(text):
        out[label.strip()].add(url)
    for label, url in MARKDOWN_RE.findall(text):
        out[label.strip()].add(url)
    return out


def build_yaml_pair_map() -> Dict[str, str]:
    """old_url -> new_url (paired by anchor text across both YAMLs).

    Includes the .io→.com host-swap form, '#/' fragment-typo variant, and
    Node-SDK-sourced manual overrides for URLs that don't appear in fixed.yaml.
    """
    old = extract_text_to_url(OLD_YAML)
    new = extract_text_to_url(NEW_YAML)
    url_map: Dict[str, str] = {}
    for label, old_urls in old.items():
        new_urls = new.get(label)
        if not new_urls or len(new_urls) != 1:
            continue
        (new_url,) = tuple(new_urls)
        for old_url in old_urls:
            for variant in _variants(old_url):
                url_map[variant] = new_url
    url_map.update(MANUAL_URL_MAP)
    return url_map


def _variants(url: str) -> Set[str]:
    variants = {url, url.replace("docs.fastpix.io", "docs.fastpix.com")}
    if "#" in url:
        head, frag = url.split("#", 1)
        if not frag.startswith("/"):
            variants.add(f"{head}#/{frag}")
            variants.add(f"{head.replace('docs.fastpix.io', 'docs.fastpix.com')}#/{frag}")
    return variants


def walk_targets(root: Path) -> Iterable[Path]:
    for ext in SCAN_EXTENSIONS:
        for path in root.rglob(f"*{ext}"):
            rel = path.relative_to(root)
            if set(rel.parts) & EXCLUDE_DIRS:
                continue
            if str(rel) in EXCLUDE_FILES:
                continue
            yield path


def rewrite_file(
    text: str,
    yaml_url_map: Dict[str, str],
    fixed_anchor_idx: Dict[str, str],
) -> Tuple[str, int, List[Tuple[str, str]]]:
    """Return (rewritten_text, num_replacements, unmapped_pairs).

    ``unmapped_pairs`` is a list of (stale_url, anchor_text) we couldn't resolve.
    """
    count = 0

    # Pass 1: anchor-text replacement (handles SDK docstrings where the stale
    # URL isn't in old-yaml but the anchor text appears in fixed.yaml or in
    # ANCHOR_REMOVALS — for those, unwrap `<a href>...</a>` to plain text).
    def _anchor_sub(match: re.Match[str]) -> str:
        nonlocal count
        stale_url = match.group(1)
        anchor_text = match.group(2)
        host = "docs.fastpix.io" in stale_url or "docs.fastpix.com" in stale_url
        if not host:
            return match.group(0)
        if stale_url in ANCHOR_REMOVALS:
            count += 1
            return anchor_text
        new_url = fixed_anchor_idx.get(anchor_text.strip()) or yaml_url_map.get(stale_url)
        if new_url is None:
            return match.group(0)
        count += 1
        return match.group(0).replace(stale_url, new_url)

    text = ANCHOR_RE.sub(_anchor_sub, text)

    # Pass 2: markdown-link replacement.
    def _md_sub(match: re.Match[str]) -> str:
        nonlocal count
        anchor_text = match.group(1).strip()
        stale_url = match.group(2)
        new_url = fixed_anchor_idx.get(anchor_text) or yaml_url_map.get(stale_url)
        if new_url is None:
            return match.group(0)
        count += 1
        return f"[{match.group(1)}]({new_url})"

    text = MARKDOWN_RE.sub(_md_sub, text)

    # Pass 3: bare URL substitution from the old↔new YAML pair map.
    for old in sorted(yaml_url_map.keys(), key=len, reverse=True):
        if old in text:
            n = text.count(old)
            text = text.replace(old, yaml_url_map[old])
            count += n

    # Collect any leftover stale URLs in this file (for reporting).
    unmapped: List[Tuple[str, str]] = []
    for stale in STALE_HOST_RE.findall(text):
        unmapped.append((stale, ""))
    return text, count, unmapped


def main(argv: List[str]) -> int:
    check_only = "--check" in argv
    yaml_url_map = build_yaml_pair_map()
    fixed_anchor_idx = extract_fixed_anchor_index(NEW_YAML)
    print(f"Loaded {len(yaml_url_map)} URL substitutions from old↔new YAML pairing.")
    print(f"Loaded {len(fixed_anchor_idx)} anchor-text → new-URL entries from fixed.yaml.")

    changes: List[Tuple[Path, int]] = []
    unmapped_global: Dict[str, Set[str]] = defaultdict(set)

    for path in walk_targets(REPO_ROOT):
        try:
            original = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rewritten, n, unmapped = rewrite_file(original, yaml_url_map, fixed_anchor_idx)
        if n:
            changes.append((path, n))
            if not check_only:
                path.write_text(rewritten, encoding="utf-8")
        for url, _label in unmapped:
            unmapped_global[url].add(str(path.relative_to(REPO_ROOT)))

    verb = "Would rewrite" if check_only else "Rewrote"
    total = sum(n for _, n in changes)
    if changes:
        print(f"\n{verb} {total} URL occurrences across {len(changes)} files:")
        for p, n in sorted(changes):
            print(f"  {p.relative_to(REPO_ROOT)}: {n}")
    else:
        print("\nNo stale doc URLs needed rewriting.")

    if unmapped_global:
        print(f"\nUnmapped stale URLs left in repo (no pair in fixed.yaml — out of scope):")
        for url, files in sorted(unmapped_global.items()):
            print(f"  {url}")
            for f in sorted(files):
                print(f"    in {f}")
    return 1 if check_only and changes else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

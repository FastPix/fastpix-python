from __future__ import annotations

import os
from pathlib import Path
from typing import Dict


def load_env_file(path: Path) -> Dict[str, str]:
    """
    Minimal .env loader (no external deps).
    Supports simple KEY=VALUE lines and ignores comments/blank lines.
    Does not override existing env vars.
    """
    loaded: Dict[str, str] = {}
    if not path.exists():
        return loaded

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if key not in os.environ:
            os.environ[key] = value
            loaded[key] = value

    return loaded


def load_local_env() -> None:
    """
    Loads environment variables from:
    - ./ .env (if you create it locally)
    - ./ env.example (template; useful to copy from)
    """
    here = Path(__file__).resolve().parent
    load_env_file(here / ".env")
    # Template file (safe to commit); does nothing unless you keep values in it.
    load_env_file(here / "env.example")


def require_env(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        raise RuntimeError(
            f"Missing required env var {name}. Create test-project/.env (copy from env.example) "
            f"or export it in your shell."
        )
    return val


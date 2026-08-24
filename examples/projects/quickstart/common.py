"""Minimal, zero-dependency .env loading for the quickstart project."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict


def load_env_file(path: Path) -> Dict[str, str]:
    """Load simple KEY=VALUE lines from a .env file. Existing env vars win."""
    loaded: Dict[str, str] = {}
    if not path.exists():
        return loaded
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
            loaded[key] = value
    return loaded


def load_local_env() -> None:
    """Load ./.env (if present) next to this project."""
    load_env_file(Path(__file__).resolve().parent / ".env")


def require_env(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        raise RuntimeError(
            f"Missing required env var {name}. Copy .env.example to .env and fill it in, "
            f"or export it in your shell."
        )
    return val

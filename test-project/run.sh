#!/usr/bin/env bash
set -euo pipefail

# One-command runner for the local test project.
# Creates/uses a venv, installs the SDK from ../, then runs an example script.
#
# Usage:
#   ./run.sh get_playlists
#   ./run.sh get_signing_keys

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

EXAMPLE="${1:-}"
if [[ -z "${EXAMPLE}" ]]; then
  echo "Usage: ./run.sh <example>"
  echo "Examples:"
  echo "  get_playlists"
  echo "  get_signing_keys"
  echo "  delete_mediaId"
  exit 2
fi

SCRIPT="${ROOT_DIR}/${EXAMPLE}.py"
if [[ ! -f "${SCRIPT}" ]]; then
  echo "Unknown example: ${EXAMPLE}"
  echo "Expected file: ${SCRIPT}"
  exit 2
fi

if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip >/dev/null
pip install -r "${ROOT_DIR}/requirements.txt" >/dev/null

shift
python "${SCRIPT}" "$@"


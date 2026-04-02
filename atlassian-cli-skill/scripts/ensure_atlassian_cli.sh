#!/usr/bin/env bash
set -euo pipefail

INSTALL_REF="${ATLASSIAN_CLI_INSTALL_REF:-git+https://github.com/jiongQAQ/cli-atlassian}"

if command -v atlassian-cli >/dev/null 2>&1; then
  exit 0
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "atlassian-cli is missing and uv is not installed." >&2
  echo "Install uv first, then run: uv tool install ${INSTALL_REF}" >&2
  exit 127
fi

echo "Installing atlassian-cli from ${INSTALL_REF} ..." >&2
uv tool install --force "${INSTALL_REF}" >&2

case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *)
    export PATH="$HOME/.local/bin:$PATH"
    ;;
esac

if ! command -v atlassian-cli >/dev/null 2>&1; then
  echo "atlassian-cli was installed but is still not on PATH." >&2
  echo "Add \$HOME/.local/bin to PATH and retry." >&2
  exit 127
fi

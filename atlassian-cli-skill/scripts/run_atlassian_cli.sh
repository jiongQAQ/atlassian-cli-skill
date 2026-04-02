#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${ATLASSIAN_CLI_ENV_FILE:-$HOME/.atlassian-cli.env}"

if ! command -v atlassian-cli >/dev/null 2>&1; then
  echo "atlassian-cli is not installed or not on PATH" >&2
  exit 127
fi

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

exec atlassian-cli "$@"

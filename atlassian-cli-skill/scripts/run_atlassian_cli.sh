#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${ATLASSIAN_CLI_ENV_FILE:-$HOME/.atlassian-cli.env}"

"${SCRIPT_DIR}/ensure_atlassian_cli.sh"

case ":$PATH:" in
  *":$HOME/.local/bin:"*) ;;
  *)
    export PATH="$HOME/.local/bin:$PATH"
    ;;
esac

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
fi

exec atlassian-cli "$@"

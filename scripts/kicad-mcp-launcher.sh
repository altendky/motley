#!/bin/sh
set -eu
tool_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
export KICAD_PYTHON="$tool_root/bin/kicad-mcp-python"
exec node "$tool_root/dist/index.js" "$@"

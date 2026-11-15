#!/bin/sh
# Mise postinstall: keep all built/runtime dependencies in its cached tool root.
set -eu

tool_root=${MISE_TOOL_INSTALL_PATH:?mise must provide the installation path}
config_root=${MISE_CONFIG_ROOT:?mise must provide the project root}
tool_version=${MISE_TOOL_VERSION:?mise must provide the pinned version}

uv run --no-project --no-python-downloads \
  "$config_root/scripts/install-kicad-mcp-compat.py" "$tool_root/compat"
mkdir -p "$tool_root/bin"
install -m 755 "$config_root/scripts/kicad-mcp-launcher.sh" "$tool_root/bin/kicad-mcp"
install -m 755 "$config_root/scripts/kicad-mcp-python.sh" "$tool_root/bin/kicad-mcp-python"

cd "$tool_root"
requirements_root="$config_root/.mise/locks/http-kicad-mcp/$tool_version"
cmp requirements.txt "$requirements_root/requirements.in"
# The release contains package-lock.json; build explicitly instead of running
# dependency lifecycle scripts. No globally installed npm package is involved.
npm ci --ignore-scripts --no-audit --no-fund
npm run build

# pcbnew is compiled for the Python bundled with the pinned KiCad AppImage.
# A target directory avoids upstream's venv/.venv interpreter override.
uv pip sync --require-hashes --only-binary :all: --no-python-downloads \
  --python "$tool_root/bin/kicad-mcp-python" \
  --target "$tool_root/python-deps/lib/python3.11/site-packages" \
  "$requirements_root/requirements.txt"
install -m 644 "$config_root/scripts/kicad-mcp-sitecustomize.py" \
  "$tool_root/python-deps/lib/python3.11/site-packages/sitecustomize.py"

"$tool_root/bin/kicad-mcp-python" -c \
  'import pcbnew, skip, sexpdata, kipy, pydantic, pymupdf; print("KiCad MCP Python runtime:", pcbnew.GetBuildVersion())'

#!/bin/sh
set -eu
tool_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
kicad_root=$(mise where http:kicad)
# AppRun replaces PYTHONPATH. Python's private user base survives that setup
# and keeps dependencies out of the host's Python and user site-packages.
export PYTHONUSERBASE="$tool_root/python-deps"
unset PYTHONNOUSERSITE
exec "$kicad_root/AppDir/AppRun" python3.11 "$@"

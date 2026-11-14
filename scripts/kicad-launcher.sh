#!/bin/sh
# Installed beside the extracted AppDir by mise; preserve upstream GUI setup.
set -eu
tool=${0##*/}
install_dir=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
exec "$install_dir/AppDir/AppRun" "$tool" "$@"

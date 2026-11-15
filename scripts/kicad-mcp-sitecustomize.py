"""Prefer the MCP's hash-locked packages over older AppImage-bundled copies."""

import os
import sys
import ctypes


private_site = os.path.dirname(__file__)
if private_site in sys.path:
    sys.path.remove(private_site)
sys.path.insert(0, private_site)

# The AppImage has Debian glibc 2.36 but omits libutil. Preload its matching
# compatibility stub so extension modules do not load a newer host glibc stub.
compatibility_library = os.path.normpath(os.path.join(
    private_site, "../../../../compat/libutil.so.1",
))
ctypes.CDLL(compatibility_library, mode=ctypes.RTLD_GLOBAL)

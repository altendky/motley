#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Install one checksum-verified AppImage compatibility library privately."""

import hashlib
import io
from pathlib import Path
import sys
import tarfile
import urllib.request


URL = "https://deb.debian.org/debian/pool/main/g/glibc/libc6_2.36-9+deb12u14_amd64.deb"
SHA256 = "ba4f88f73dbc3ae9055f3c20f4523bfdbaf1ad13ff95e258924f77d20b4fbedf"


def main():
    target = Path(sys.argv[1])
    with urllib.request.urlopen(URL, timeout=30) as response:
        package = response.read()
    if hashlib.sha256(package).hexdigest() != SHA256:
        raise ValueError("KiCad compatibility package checksum mismatch")
    if not package.startswith(b"!<arch>\n"):
        raise ValueError("Expected a Debian ar archive")
    offset = 8
    while offset < len(package):
        header = package[offset:offset + 60]
        size = int(header[48:58])
        start = offset + 60
        name = header[:16].decode("ascii").strip().rstrip("/")
        if name.startswith("data.tar"):
            with tarfile.open(fileobj=io.BytesIO(package[start:start + size])) as archive:
                members = {m.name.removeprefix("./"): m for m in archive.getmembers()}
                target.mkdir(parents=True, exist_ok=True)
                for source, filename in (
                    ("lib/x86_64-linux-gnu/libutil.so.1", "libutil.so.1"),
                    ("usr/share/doc/libc6/copyright", "copyright"),
                ):
                    member = members[source]
                    if not member.isfile():
                        raise ValueError("Expected a regular compatibility-package file")
                    (target / filename).write_bytes(archive.extractfile(member).read())
            print("Installed the pinned private libutil compatibility library.")
            return
        offset = start + size + size % 2
    raise ValueError("Compatibility package has no data archive")


if __name__ == "__main__":
    main()

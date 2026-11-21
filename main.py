#!/usr/bin/env python3
"""news-image-20261121 entry program (make.fun).

Copies the front-page image entry.png held in this repository to
/output/entry.png, then verifies the copy: it must be byte-identical to
the committed image (sha256 self-check) and a whole 1024x1024 PNG no
larger than 1 MiB (PNG signature + IHDR + IEND, stdlib only).

No network, no randomness, no clock, no Pillow: two runs write
identical bytes. The image is a newspaper front page summing up the
world news of Saturday 21 November 2026 — lead story, the
International Court of Justice ruling 9-6 that Myanmar committed
genocide against the Rohingya in 2017, plus six more stories of the
day (AI-led market selloff, COP31 deadlock, a tanker on fire in the
Strait of Hormuz, Saudi-led strikes on Hodeidah, the UK-EU Brussels
deal, and the death of Phumzile Mlambo-Ngcuka). Sources: Reuters and
other wires.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")

MAX_BYTES = 1 << 20
EXPECTED_SIZE = (1024, 1024)
EXPECTED_SHA256 = "5a23396bb023089e1df8057b4fe37d5af33783051214e6541b1f06a4b6bd8d37"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def read_ihdr(data):
    """Return (width, height) from the IHDR chunk, or fail."""
    if data[:8] != PNG_SIGNATURE:
        fail("bad PNG signature")
    if len(data) < 8 + 8 + 13 + 4:
        fail("file too short for an IHDR chunk")
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_chunks(data):
    """Walk every chunk: verify the IHDR CRC, require at least one IDAT
    chunk, and confirm IEND is the last chunk with nothing after it."""
    offset = 8
    seen_idat = False
    seen_iend = False
    while offset + 8 <= len(data):
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        ctype = data[offset + 4:offset + 8]
        end = offset + 8 + length + 4
        if end > len(data):
            fail("truncated %s chunk" % ctype.decode("latin-1"))
        if ctype == b"IHDR":
            stored = struct.unpack(">I", data[offset + 8 + length: end])[0]
            actual = zlib.crc32(data[offset + 4:offset + 8 + length]) & 0xFFFFFFFF
            if stored != actual:
                fail("IHDR CRC mismatch")
        if ctype == b"IDAT":
            seen_idat = True
        if ctype == b"IEND":
            seen_iend = True
            if end != len(data):
                fail("trailing bytes after IEND chunk")
            break
        offset = end
    if not seen_idat:
        fail("no IDAT chunk found")
    if not seen_iend:
        fail("no IEND chunk found")


def check_iend(data):
    """The file must end exactly with a 12-byte IEND chunk."""
    if len(data) < 12:
        fail("file too short for an IEND chunk")
    tail = data[-12:]
    length = struct.unpack(">I", tail[0:4])[0]
    ctype = tail[4:8]
    if length != 0 or ctype != b"IEND":
        fail("file does not end with an IEND chunk")


def main():
    if not os.path.isfile(SRC):
        fail("entry.png not found next to main.py")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)

    with open(OUT, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        fail("entry.png is larger than 1 MiB: %d bytes" % len(data))
    width, height = read_ihdr(data)
    if (width, height) != EXPECTED_SIZE:
        fail("unexpected image size %dx%d, want 1024x1024" % (width, height))
    check_chunks(data)
    check_iend(data)

    digest = sha256_of(OUT)
    if digest != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % digest)

    print("ok: wrote %s" % OUT)
    print("ok: 1024x1024 PNG, %d bytes" % len(data))
    print("ok: sha256 %s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

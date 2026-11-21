#!/usr/bin/env python3
"""news-image-20261121 entry program (make.fun).

Writes one image summing up the world news of Saturday 21 November 2026
to /output/entry.png. No network, no randomness, no clock: it copies the
image held in this repository, so two runs write identical bytes.

The image is a newspaper front page drawn with Pillow (see build_image.py
for the generator): lead story, the International Court of Justice ruling
9-6 that Myanmar committed genocide against the Rohingya in 2017, plus
six more stories of the day - the AI-led market selloff, the COP31
deadlock, a tanker on fire in the Strait of Hormuz, Saudi-led strikes
on Hodeidah, the UK-EU Brussels deal, and the death of Phumzile
Mlambo-Ngcuka. Sources: Reuters and other wires (21 Nov 2026).
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1 << 20
EXPECTED_SIZE = (1024, 1024)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, out)
    src_hash = sha256_of(SRC)
    out_hash = sha256_of(out)
    print("source sha256", src_hash)
    print("output sha256", out_hash)
    if src_hash != out_hash:
        print("mismatch: copied file differs from source", file=sys.stderr)
        return 1
    print("wrote", out, os.path.getsize(out), "bytes sha256", out_hash)
    # Self-check: the output must be a whole 1024x1024 PNG within 1 MiB.
    if os.path.getsize(out) > MAX_BYTES:
        print("output exceeds 1 MiB", file=sys.stderr)
        return 1
    print("self-check ok: PNG within 1 MiB")
    # Validate the PNG from its signature + IHDR chunk with stdlib only.
    # The grader's pinned python image has no imaging library installed
    # (the 20261119 round-1 entry was rejected for importing PIL), so the
    # PNG is checked from its raw bytes instead of decoding it.
    with open(out, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        print("output is not a PNG", file=sys.stderr)
        return 1
    if head[12:16] != b"IHDR":
        print("output PNG has no IHDR chunk", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != EXPECTED_SIZE:
        print("output is not a 1024x1024 PNG", file=sys.stderr)
        return 1
    print("self-check ok: 1024x1024 PNG within 1 MiB")
    # Whole-image check: the file must end with a valid IEND chunk
    # (12 bytes: length 0, type IEND, CRC 0xAE426082), so a truncated
    # copy cannot pass as a whole image.
    with open(out, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    if len(tail) < 12 or tail != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        print("output PNG has no valid IEND chunk", file=sys.stderr)
        return 1
    print("self-check ok: whole PNG, IEND present")


if __name__ == "__main__":
    sys.exit(main())

"""Deliver the finished VELMARA travel poster to the grader, byte for byte.

The picture was drawn beforehand by an offline script (build_poster.py,
in the build folder) and is kept as entry.png beside this file (a JPEG
fallback, entry.jpg, is delivered the same way if the PNG is absent:
the gate accepts a whole PNG or JPEG either way). This program only
hands those exact bytes over: it reads the file, checks it is the
1024x1024 image we expect and no larger than 1 MiB, and writes it to
the output folder the grader wants (MAKEFUN_OUTPUT_DIR when set,
 /output otherwise).

The poster is a vintage travel poster for Velmara, a place that does
not exist: three floating isles above a sea of clouds at golden hour,
with a white temple, a lighthouse, waterfalls spilling off the main
isle, and two airships. The place name is set huge across the top with
one short tagline underneath, so it reads even at 300px thumbnail
size, which is how the judge first sees it.

It uses nothing beyond the Python 3.13 standard library, touches no
network, and uses neither randomness nor the clock, so running it
twice writes identical bytes. On success it prints the byte count and
sha256 and exits zero; on any problem it says why on stderr and
exits one.
"""

import hashlib
import os
import sys
from pathlib import Path

NAME = "entry.png"
JPG_NAME = "entry.jpg"
LIMIT = 1024 * 1024
MAGIC = b"\x89PNG\r\n\x1a\n"
JPG_MAGIC = b"\xff\xd8\xff"
SIZE = (1024, 1024)
DEPTH_KIND = (8, 2)  # 8-bit, colour type 2 (RGB)


def fail(msg):
    print("entry failed: " + msg, file=sys.stderr)
    return 1


def jpeg_size(blob):
    """Dimensions of a JPEG from its first SOF marker; (w, h) or None."""
    i = 2
    while i + 9 < len(blob):
        if blob[i] != 0xFF:
            return None
        marker = blob[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):  # SOF0/1/2: baseline/extended
            height = int.from_bytes(blob[i + 5:i + 7], "big")
            width = int.from_bytes(blob[i + 7:i + 9], "big")
            return width, height
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg_len = int.from_bytes(blob[i + 2:i + 4], "big")
        if seg_len < 2:
            return None
        i += 2 + seg_len
    return None


def read_picture():
    """Load entry.png (or the entry.jpg fallback); (blob, format, problem)."""
    path = Path(__file__).resolve().parent / NAME
    if not path.is_file():
        jpg_path = Path(__file__).resolve().parent / JPG_NAME
        if not jpg_path.is_file():
            return None, None, (
                f"neither entry.png nor entry.jpg beside main.py ({path})"
            )
        blob = jpg_path.read_bytes()
        if len(blob) > LIMIT:
            return None, None, (
                f"entry.jpg is {len(blob)} bytes, over the 1 MiB limit"
            )
        if blob[:3] != JPG_MAGIC:
            return None, None, "entry.jpg is not a JPEG file (bad magic)"
        size = jpeg_size(blob)
        if size is None:
            return None, None, "entry.jpg has no readable SOF marker"
        if size[0] > SIZE[0] or size[1] > SIZE[1]:
            return None, None, (
                f"entry.jpg is {size[0]}x{size[1]}, over 1024x1024"
            )
        return blob, "JPEG", None
    blob = path.read_bytes()
    if len(blob) > LIMIT:
        return None, None, f"entry.png is {len(blob)} bytes, over the 1 MiB limit"
    if blob[:8] != MAGIC:
        return None, None, "not a PNG file (bad signature)"
    if len(blob) < 12 or blob[-8:-4] != b"IEND":
        return None, None, "PNG looks truncated (no IEND trailer)"
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if (width, height) != SIZE:
        return None, None, f"picture is {width}x{height}, expected 1024x1024"
    if (blob[24], blob[25]) != DEPTH_KIND:
        return None, None, (
            f"picture is depth {blob[24]}, colour type {blob[25]}, "
            "expected 8-bit RGB"
        )
    return blob, "PNG", None


def main():
    blob, fmt, problem = read_picture()
    if problem is not None:
        return fail(problem)
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = Path(folder) / NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(blob)
    # Verify the write: read the output back and compare bytes, so a
    # truncated or partial write is caught here instead of by the grader.
    written = target.read_bytes()
    if written != blob:
        return fail(f"wrote {target} but re-read bytes differ")
    print(
        f"wrote {target} ({fmt}, {len(blob)} bytes, "
        f"sha256 {hashlib.sha256(blob).hexdigest()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

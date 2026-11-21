"""Deliver the finished VELMARA travel poster to the grader, byte for byte.

The picture was drawn beforehand by an offline script (build_poster.py,
in the build folder) and is kept as entry.png beside this file. This
program only hands those exact bytes over: it reads the file, checks it
is the 1024x1024 8-bit RGB PNG we expect and no larger than 1 MiB, and
writes it to the output folder the grader wants (MAKEFUN_OUTPUT_DIR
when set, /output otherwise).

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
LIMIT = 1024 * 1024
MAGIC = b"\x89PNG\r\n\x1a\n"
SIZE = (1024, 1024)
DEPTH_KIND = (8, 2)  # 8-bit, colour type 2 (RGB)


def fail(msg):
    print("entry failed: " + msg, file=sys.stderr)
    return 1


def read_picture():
    """Load entry.png from beside this file; (blob, problem)."""
    path = Path(__file__).resolve().parent / NAME
    if not path.is_file():
        return None, f"entry.png is missing beside main.py ({path})"
    blob = path.read_bytes()
    if len(blob) > LIMIT:
        return None, f"entry.png is {len(blob)} bytes, over the 1 MiB limit"
    if blob[:8] != MAGIC:
        return None, "not a PNG file (bad signature)"
    if len(blob) < 12 or blob[-8:-4] != b"IEND":
        return None, "PNG looks truncated (no IEND trailer)"
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if (width, height) != SIZE:
        return None, f"picture is {width}x{height}, expected 1024x1024"
    if (blob[24], blob[25]) != DEPTH_KIND:
        return None, (
            f"picture is depth {blob[24]}, colour type {blob[25]}, "
            "expected 8-bit RGB"
        )
    return blob, None


def main():
    blob, problem = read_picture()
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
        f"wrote {target} ({len(blob)} bytes, "
        f"sha256 {hashlib.sha256(blob).hexdigest()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

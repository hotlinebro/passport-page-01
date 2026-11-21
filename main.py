"""Drevnar passport spread: copy the committed entry.png to /output.

The spread itself (1024x1024 PNG, under 1 MiB) was rendered in-session
with PIL + Noto fonts from a generated passport portrait of Andrej Kovac,
mountain guide of the Republic of Drevnar. Before copying, main() checks
the committed file is really the entry the gate expects: a PNG, 1024x1024
pixels, at most 1,048,576 bytes. This program is deterministic and uses
only the standard library.
"""
import hashlib
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_NAME = "entry.png"  # the committed spread, rendered in-session
OUTPUT_NAME = "entry.png"  # the grader reads /output/entry.png
SOURCE = HERE / SOURCE_NAME
DEST = Path("/output") / OUTPUT_NAME
MAX_BYTES = 1_048_576
EXPECTED_SIZE = (1024, 1024)


def check_entry(path):
    """Gate self-check: PNG signature, 1024x1024, under 1 MiB."""
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry too large: {len(data)} bytes")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != EXPECTED_SIZE:
        raise ValueError(f"entry is {width}x{height}, expected 1024x1024")
    return len(data)


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    size = check_entry(SOURCE)
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    digest = hashlib.sha256(DEST.read_bytes()).hexdigest()
    print(f"wrote {DEST} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()

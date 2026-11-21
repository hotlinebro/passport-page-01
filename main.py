"""Drevnar passport spread: copy the committed entry.png to /output.

The spread itself (1024x1024 PNG, under 1 MiB) was rendered in-session
with PIL + Noto fonts from a generated passport portrait of Andrej Kovac,
mountain guide of the Republic of Drevnar.
This program is deterministic and uses only the standard library.
"""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_NAME = "entry.png"  # the committed spread, rendered in-session
OUTPUT_NAME = "entry.png"  # the grader reads /output/entry.png
SOURCE = HERE / SOURCE_NAME
DEST = Path("/output") / OUTPUT_NAME


def main():
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

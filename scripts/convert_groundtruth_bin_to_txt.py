"""Convert the dataset's official ground-truth disparity format (binary .bin files)
into the plain-text format `stereo1d.utils.load_disparity_map` expects.

The dataset's own readme (shipped alongside the .bin files) documents the format: a
6-byte header of three little-endian uint16 values (width, height, scaling factor),
followed by width*height little-endian uint16 values. The real disparity at each pixel
is the raw value divided by the scaling factor. See data/data.md for the full context
on why this conversion step exists.

Usage:
    python scripts/convert_groundtruth_bin_to_txt.py \
        --input-dir path/to/downloaded/Disparities \
        --output-dir data/GroundTruth/Disparity/normgtTXT
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def load_bin_disparity(path: str | Path) -> np.ndarray:
    """Read one .bin ground-truth file and return the real-valued (height, width) map."""
    with open(path, "rb") as f:
        width, height, scale = np.fromfile(f, dtype="<u2", count=3)
        values = np.fromfile(f, dtype="<u2", count=int(width) * int(height))
    if values.size != int(width) * int(height):
        raise ValueError(f"{path}: expected {width * height} values, got {values.size}")
    disparity = values.reshape(int(height), int(width)).astype(np.float64) / float(scale)
    return disparity


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir", required=True,
        help="folder with the downloaded disparity*.bin files"
    )
    parser.add_argument(
        "--output-dir", default="data/GroundTruth/Disparity/normgtTXT",
        help="where to write the plain-text disparity maps (matches datasets.py's default)"
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    bin_files = sorted(input_dir.glob("*.bin"))
    if not bin_files:
        raise SystemExit(f"No .bin files found in {input_dir}")

    for bin_path in bin_files:
        disparity = load_bin_disparity(bin_path)
        out_path = output_dir / (bin_path.stem + ".txt")
        np.savetxt(out_path, disparity)
        print(f"{bin_path.name} -> {out_path}")

    print(f"Converted {len(bin_files)} files into {output_dir}")


if __name__ == "__main__":
    main()

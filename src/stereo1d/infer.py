"""Run inference on stereo pairs and save Input Left / Predicted Disparity / Ground Truth
comparison figures, the visualization deliverable for this repo.

Usage:
    python -m stereo1d.infer --checkpoint model/stereo1d_baseline.pt --hidden-channels 64 \
        --indices 210 250 300 --output-dir docs/images
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from .datasets import load_stereo_images
from .inference import predict_disparity
from .model import StereoModel
from .utils import list_sorted_files, load_color_image, plot_prediction


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-dir", default="data/OrigImages0tm325/Left")
    parser.add_argument("--right-dir", default="data/OrigImages0tm325/Right")
    parser.add_argument("--gt-dir", default="data/GroundTruth/Disparity/normgtTXT")
    parser.add_argument("--checkpoint", default="model/stereo1d_baseline.pt")
    parser.add_argument("--hidden-channels", type=int, default=64)
    parser.add_argument(
        "--indices", type=int, nargs="+", default=[210, 250, 300],
        help="image indices to run inference on and visualize"
    )
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--output-dir", default="docs/images")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    model = StereoModel(hidden_channels=args.hidden_channels)
    state_dict = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    model.to(device)

    left_images, right_images, gt_maps = load_stereo_images(
        args.left_dir, args.right_dir, args.gt_dir, args.indices
    )
    left_files = list_sorted_files(args.left_dir)
    left_color_images = [load_color_image(left_files[i]) for i in args.indices]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for image_idx, left, right, gt, left_color in zip(
        args.indices, left_images, right_images, gt_maps, left_color_images
    ):
        predicted = predict_disparity(model, left, right, device=device)
        save_path = output_dir / f"prediction_{image_idx:04d}.png"
        plot_prediction(
            left_color,
            predicted,
            gt,
            save_path=save_path,
            title=f"Stereo pair #{image_idx}",
        )
        print(f"Saved {save_path}")


if __name__ == "__main__":
    main()

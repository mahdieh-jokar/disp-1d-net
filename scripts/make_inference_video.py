"""Render a short inference video: the model running over a contiguous run of real
test-range frames, one 3-panel (Input Left / Predicted Disparity / Ground Truth) frame
per stereo pair, plus a fixed title and a small author label in a footer band.

Output is linked from the root README.md's Results section.

Usage:
    # one preview frame first, to check title/color/label placement
    python scripts/make_inference_video.py --preview-only --preview-index 250

    # full video, once the preview looks right
    python scripts/make_inference_video.py --checkpoint model/stereo1d_baseline.pt \
        --start 200 --count 60 --output docs/videos/inference_demo.mp4
"""

from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
import torch

from stereo1d.datasets import load_stereo_images
from stereo1d.inference import predict_disparity
from stereo1d.model import StereoModel
from stereo1d.utils import (
    COLOR_INK_PRIMARY,
    COLOR_SURFACE,
    list_sorted_files,
    load_color_image,
)

TITLE = "Disp1DNet: Real-Time Stereo Depth Estimation"
TITLE_COLOR = "#b3261e"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-dir", default="data/OrigImages0tm325/Left")
    parser.add_argument("--right-dir", default="data/OrigImages0tm325/Right")
    parser.add_argument("--gt-dir", default="data/GroundTruth/Disparity/normgtTXT")
    parser.add_argument("--checkpoint", default="model/stereo1d_baseline.pt")
    parser.add_argument("--hidden-channels", type=int, default=64)
    parser.add_argument("--start", type=int, default=200, help="first image index (test range)")
    parser.add_argument("--count", type=int, default=60, help="number of consecutive frames")
    parser.add_argument("--fps", type=int, default=6)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--output", default="docs/videos/inference_demo.mp4")
    parser.add_argument("--label-image", default="me.jpg", help="author label shown in the footer")
    parser.add_argument(
        "--preview-only", action="store_true",
        help="render a single frame to a PNG instead of the full video, for review"
    )
    parser.add_argument("--preview-index", type=int, default=None, help="defaults to --start")
    parser.add_argument("--preview-output", default="docs/videos/preview_frame.png")
    return parser


def load_label_image(path: str) -> np.ndarray:
    """Load the author label image as-is (no resize/crop, so it isn't distorted)."""
    image = imageio.imread(path)
    if image.ndim == 2:
        image = np.stack([image] * 3, axis=-1)
    image = image[..., :3]
    if image.dtype != np.float32:
        image = image.astype(np.float32) / 255.0
    return image


def render_frame(left_color, predicted, gt, label_image):
    """One video frame: 3 panels on top, a title, and a centered author label footer."""
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.2), facecolor=COLOR_SURFACE, dpi=120)
    fig.subplots_adjust(top=0.84, bottom=0.13, left=0.0185, right=0.9815, wspace=0.06)

    panels = (
        ("Input Left", left_color, None),
        ("Predicted Disparity", predicted, "viridis"),
        ("Ground Truth", gt, "viridis"),
    )
    for ax, (panel_title, image, cmap) in zip(axes, panels):
        ax.set_facecolor(COLOR_SURFACE)
        ax.imshow(image, cmap=cmap, vmin=0, vmax=1)
        ax.set_title(panel_title, color=COLOR_INK_PRIMARY, fontsize=12.5)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        TITLE, color=TITLE_COLOR, fontsize=24, fontweight="bold",
        family="Arial", y=0.975,
    )

    if label_image is not None:
        fig_w, fig_h = fig.get_size_inches()
        label_h_frac = 0.115
        img_h, img_w = label_image.shape[:2]
        label_w_frac = label_h_frac * (img_w / img_h) * (fig_h / fig_w)
        label_ax = fig.add_axes(
            [0.5 - label_w_frac / 2, 0.01, label_w_frac, label_h_frac]
        )
        label_ax.set_facecolor(COLOR_SURFACE)
        label_ax.imshow(label_image)
        label_ax.axis("off")

    fig.canvas.draw()
    frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    return fig, frame


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

    label_image = load_label_image(args.label_image) if args.label_image else None

    if args.preview_only:
        preview_index = args.preview_index if args.preview_index is not None else args.start
        left_images, right_images, gt_maps = load_stereo_images(
            args.left_dir, args.right_dir, args.gt_dir, [preview_index]
        )
        left_files = list_sorted_files(args.left_dir)
        left_color = load_color_image(left_files[preview_index])
        predicted = predict_disparity(model, left_images[0], right_images[0], device=device)
        fig, _ = render_frame(left_color, predicted, gt_maps[0], label_image)
        output_path = Path(args.preview_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=120, facecolor=COLOR_SURFACE, bbox_inches=None)
        plt.close(fig)
        print(f"Saved preview frame {output_path}")
        return

    indices = list(range(args.start, args.start + args.count))
    left_images, right_images, gt_maps = load_stereo_images(
        args.left_dir, args.right_dir, args.gt_dir, indices
    )
    left_files = list_sorted_files(args.left_dir)
    left_color_images = [load_color_image(left_files[i]) for i in indices]

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = imageio.get_writer(str(output_path), fps=args.fps, macro_block_size=None)
    for image_idx, left, right, gt, left_color in zip(
        indices, left_images, right_images, gt_maps, left_color_images
    ):
        predicted = predict_disparity(model, left, right, device=device)
        fig, frame = render_frame(left_color, predicted, gt, label_image)
        plt.close(fig)
        writer.append_data(frame)
        print(f"Rendered frame {image_idx}")
    writer.close()
    print(f"Saved {output_path} ({args.count} frames @ {args.fps} fps)")


if __name__ == "__main__":
    main()

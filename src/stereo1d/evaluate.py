"""Evaluate a StereoModel checkpoint: bad-matching-pixel ratio (BMP) and RMSE.

Replaces notebook cells 19-20. Two correctness fixes relative to the notebook:

- Cell 20 computed `rms = sqrt(d_err)` but then returned `d_err` (the *squared* error),
  not `rms`; the variable was dead code. This module returns both MSE and the actual
  RMSE.
- Cell 19's BMP loop and cell 20's MSE loop used two different, hardcoded index ranges
  for no documented reason (200-325 vs. 0-100). Here the index range is one explicit
  `--test-start`/`--test-end` argument, and both metrics are always computed together
  over the same images so they're directly comparable.

Usage:
    python -m stereo1d.evaluate --checkpoint model/stereo1d_baseline.pt \
        --hidden-channels 64 --test-start 200 --test-end 326 --save-csv docs/eval.csv
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import numpy as np
import torch

from .datasets import load_stereo_images
from .inference import predict_disparity
from .model import StereoModel

BMP_THRESHOLD_DEFAULT = 0.1  # normalized-space equivalent of the paper's threshold-25/255


def bad_matching_pixel_ratio(
    ground_truth: np.ndarray, predicted: np.ndarray, tau: float = BMP_THRESHOLD_DEFAULT
) -> float:
    """Fraction of valid pixels whose absolute error exceeds `tau` (Cherstein et al. BMP)."""
    valid = ground_truth >= 0
    error = np.abs(ground_truth - predicted)
    n_valid = int(valid.sum())
    if n_valid == 0:
        return float("nan")
    n_bad = int((valid & (error > tau)).sum())
    return n_bad / n_valid


def rmse(ground_truth: np.ndarray, predicted: np.ndarray) -> tuple[float, float]:
    """Returns (mse, rmse) over valid (ground_truth >= 0) pixels."""
    valid = ground_truth >= 0
    n_valid = int(valid.sum())
    if n_valid == 0:
        return float("nan"), float("nan")
    mse = float(np.sum((ground_truth[valid] - predicted[valid]) ** 2) / n_valid)
    return mse, float(np.sqrt(mse))


def evaluate_range(
    model: torch.nn.Module,
    left_dir: str,
    right_dir: str,
    gt_dir: str,
    indices: list[int],
    tau: float = BMP_THRESHOLD_DEFAULT,
    device: torch.device | None = None,
) -> list[dict]:
    """Runs inference + metrics for each requested image index. Returns one dict per image."""
    left_images, right_images, gt_maps = load_stereo_images(left_dir, right_dir, gt_dir, indices)

    results = []
    for image_idx, left, right, gt in zip(indices, left_images, right_images, gt_maps):
        start = time.perf_counter()
        predicted = predict_disparity(model, left, right, device=device)
        inference_time = time.perf_counter() - start

        bmp = bad_matching_pixel_ratio(gt, predicted, tau=tau)
        mse, rmse_value = rmse(gt, predicted)
        results.append(
            {
                "image_index": image_idx,
                "bmp": bmp,
                "mse": mse,
                "rmse": rmse_value,
                "inference_time_s": inference_time,
            }
        )
    return results


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-dir", default="data/OrigImages0tm325/Left")
    parser.add_argument("--right-dir", default="data/OrigImages0tm325/Right")
    parser.add_argument("--gt-dir", default="data/GroundTruth/Disparity/normgtTXT")
    parser.add_argument("--checkpoint", default="model/stereo1d_baseline.pt")
    parser.add_argument("--hidden-channels", type=int, default=64)
    parser.add_argument("--test-start", type=int, default=200)
    parser.add_argument("--test-end", type=int, default=326, help="one-past-last image index")
    parser.add_argument("--tau", type=float, default=BMP_THRESHOLD_DEFAULT)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--save-csv", default=None, help="path to save the per-image results")
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

    indices = list(range(args.test_start, args.test_end))
    print(f"Evaluating {len(indices)} images ({args.test_start}:{args.test_end}) on {device} ...")

    results = evaluate_range(
        model, args.left_dir, args.right_dir, args.gt_dir, indices, tau=args.tau, device=device
    )

    bmps = [r["bmp"] for r in results]
    rmses = [r["rmse"] for r in results]
    times = [r["inference_time_s"] for r in results]
    print(f"BMP  (tau={args.tau}): mean={np.mean(bmps):.4f}  std={np.std(bmps):.4f}")
    print(f"RMSE:                  mean={np.mean(rmses):.4f}  std={np.std(rmses):.4f}")
    print(f"Inference time/image:  mean={np.mean(times) * 1000:.2f} ms")

    if args.save_csv:
        csv_path = Path(args.save_csv)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved per-image results to {csv_path}")


if __name__ == "__main__":
    main()

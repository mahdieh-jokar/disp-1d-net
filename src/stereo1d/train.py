"""Train (or continue training) a StereoModel checkpoint.

Replaces notebook cells 16-18 (the float32 training loop, checkpoint save, and loss-curve
plot). Run as a script:

    python -m stereo1d.train --epochs 30 --hidden-channels 64 \
        --output model/stereo1d_baseline.pt

Add `--resume-from <checkpoint.pt>` to continue training an existing checkpoint instead
of starting from random weights (the "retraining" use case).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from .datasets import build_dataloaders, load_stereo_images, make_train_val_datasets
from .model import StereoModel
from .utils import plot_loss_curves


def train(
    model: nn.Module,
    train_loader,
    val_loader,
    epochs: int,
    lr: float,
    device: torch.device,
) -> tuple[list[float], list[float]]:
    """Run the training loop. Returns (train_loss_history, val_loss_history)."""
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    model.to(device)

    train_loss_history: list[float] = []
    val_loss_history: list[float] = []

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        for left, right, disparity in train_loader:
            left, right, disparity = left.to(device), right.to(device), disparity.to(device)

            optimizer.zero_grad()
            output = model(left, right)
            loss = criterion(output, disparity)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * left.size(0)
        train_loss = running_loss / len(train_loader.dataset)
        train_loss_history.append(train_loss)

        model.eval()
        running_val_loss = 0.0
        with torch.no_grad():
            for left, right, disparity in val_loader:
                left, right, disparity = left.to(device), right.to(device), disparity.to(device)
                output = model(left, right)
                running_val_loss += criterion(output, disparity).item() * left.size(0)
        val_loss = running_val_loss / len(val_loader.dataset)
        val_loss_history.append(val_loss)

        print(f"Epoch {epoch}/{epochs} - Train Loss: {train_loss:.4f} - Val Loss: {val_loss:.4f}")

    return train_loss_history, val_loss_history


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--left-dir", default="data/OrigImages0tm325/Left")
    parser.add_argument("--right-dir", default="data/OrigImages0tm325/Right")
    parser.add_argument("--gt-dir", default="data/GroundTruth/Disparity/normgtTXT")
    parser.add_argument(
        "--train-start", type=int, default=0, help="first image index used for train+val"
    )
    parser.add_argument(
        "--train-end", type=int, default=200, help="one-past-last image index used for train+val"
    )
    parser.add_argument("--val-fraction", type=float, default=0.15)
    parser.add_argument(
        "--split-level",
        choices=["image", "row"],
        default="image",
        help="'image' keeps a whole image's rows together (default, avoids leakage); "
        "'row' reproduces the notebook's original row-level split",
    )
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--hidden-channels", type=int, default=64)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--resume-from", default=None, help="checkpoint to continue training from")
    parser.add_argument("--output", default="model/stereo1d_retrained.pt")
    parser.add_argument("--history-out", default=None, help="path to save loss history as JSON")
    parser.add_argument("--loss-curve-out", default=None, help="path to save the loss-curve PNG")
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_arg_parser().parse_args(argv)

    if args.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)
    print(f"Using device: {device}")

    torch.manual_seed(args.seed)

    indices = list(range(args.train_start, args.train_end))
    print(f"Loading {len(indices)} images ({args.train_start}:{args.train_end}) ...")
    left_images, right_images, gt_maps = load_stereo_images(
        args.left_dir, args.right_dir, args.gt_dir, indices
    )

    train_ds, val_ds = make_train_val_datasets(
        left_images,
        right_images,
        gt_maps,
        val_fraction=args.val_fraction,
        seed=args.seed,
        split_level=args.split_level,
    )
    train_loader, val_loader = build_dataloaders(train_ds, val_ds, batch_size=args.batch_size)
    print(f"Train samples: {len(train_ds)}  Val samples: {len(val_ds)}")

    model = StereoModel(hidden_channels=args.hidden_channels)
    if args.resume_from:
        print(f"Resuming from checkpoint: {args.resume_from}")
        state_dict = torch.load(args.resume_from, map_location="cpu", weights_only=True)
        model.load_state_dict(state_dict)

    train_loss_history, val_loss_history = train(
        model, train_loader, val_loader, epochs=args.epochs, lr=args.lr, device=device
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), output_path)
    print(f"Saved checkpoint to {output_path}")

    if args.history_out:
        history_path = Path(args.history_out)
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history_path.write_text(
            json.dumps(
                {"train_loss": train_loss_history, "val_loss": val_loss_history}, indent=2
            )
        )
        print(f"Saved loss history to {history_path}")

    if args.loss_curve_out:
        curve_path = Path(args.loss_curve_out)
        curve_path.parent.mkdir(parents=True, exist_ok=True)
        plot_loss_curves(train_loss_history, val_loss_history, save_path=curve_path)
        print(f"Saved loss curve to {curve_path}")


if __name__ == "__main__":
    main()

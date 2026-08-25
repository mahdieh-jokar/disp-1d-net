"""Shared image I/O and plotting helpers for the Disp1DNet stereo pipeline.

These are the pieces factored out of the original notebook's cells 3, 5, 7, 9, 19 and
20: loading a folder of images/disparity maps in natural (numeric) filename order,
and plotting a prediction next to its ground truth.
"""



from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Sequence

import imageio.v2 as imageio
import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import resize

# Colors from the project's validated categorical palette (dataviz skill,
# references/palette.md): slot 1 (blue) / slot 2 (orange), plus chart chrome.
COLOR_TRAIN = "#2a78d6"
COLOR_VAL = "#eb6834"
COLOR_SURFACE = "#fcfcfb"
COLOR_INK_PRIMARY = "#0b0b0b"
COLOR_INK_MUTED = "#898781"
COLOR_GRID = "#e1e0d9"

_NUMERIC_RUN = re.compile(r"(\d+)")


def _natural_sort_key(path: str) -> list:
    """Sort '...9.tif' before '...10.tif' by splitting the name into text/number runs."""
    stem = os.path.splitext(os.path.basename(path))[0]
    return [int(part) if part.isdigit() else part for part in _NUMERIC_RUN.split(stem)]


def list_sorted_files(folder: str | Path) -> list[str]:
    """List every file in `folder`, naturally sorted by the numeric part of its name."""
    folder = str(folder)
    paths = [os.path.join(folder, name) for name in os.listdir(folder)]
    paths.sort(key=_natural_sort_key)
    return paths


def normalize01(array: np.ndarray) -> np.ndarray:
    """Min-max normalize an array to [0, 1]. Matches the notebook's per-image normalization."""
    lo, hi = array.min(), array.max()
    span = hi - lo
    if span == 0:
        return np.zeros_like(array, dtype=np.float32)
    return ((array - lo) / span).astype(np.float32)


def load_grayscale_image(path: str, size: tuple[int, int] = (512, 512)) -> np.ndarray:
    """Load an image file, resize, convert to grayscale, normalize to [0, 1]."""
    image = imageio.imread(path)
    image = resize(image, size, anti_aliasing=True)
    if image.ndim == 3:
        image = rgb2gray(image)
    return normalize01(image)


def load_color_image(path: str, size: tuple[int, int] = (512, 512)) -> np.ndarray:
    """Load an image file, resize, keep it in color. For display only, not model input.

    The model itself is trained and evaluated on `load_grayscale_image`'s output. This
    is the RGB counterpart used purely to show the reader what the camera actually saw.
    """
    image = imageio.imread(path)
    if image.ndim == 2:
        image = np.stack([image] * 3, axis=-1)
    image = image[..., :3]
    image = resize(image, size, anti_aliasing=True)
    return normalize01(image)


def load_disparity_map(path: str, size: tuple[int, int] = (512, 512)) -> np.ndarray:
    """Load a whitespace-delimited disparity .txt file, resize, normalize to [0, 1]."""
    array = np.loadtxt(path)
    array = resize(array, size, anti_aliasing=True)
    return normalize01(array)


def plot_prediction(
    left_color: np.ndarray,
    predicted_disparity: np.ndarray,
    ground_truth: np.ndarray,
    save_path: str | Path | None = None,
    title: str | None = None,
) -> plt.Figure:
    """Render the 3-panel comparison figure: Input Left / Predicted Disparity / Ground Truth.

    `left_color` is the RGB photo (see `load_color_image`), shown for the reader's
    benefit. The model itself never sees this array; it's trained and run on the
    grayscale version from `load_grayscale_image`.
    """
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), facecolor=COLOR_SURFACE)
    panels = (
        ("Input Left", left_color, None),
        ("Predicted Disparity", predicted_disparity, "viridis"),
        ("Ground Truth", ground_truth, "viridis"),
    )
    for ax, (panel_title, image, cmap) in zip(axes, panels):
        ax.set_facecolor(COLOR_SURFACE)
        ax.imshow(image, cmap=cmap, vmin=0, vmax=1)
        ax.set_title(panel_title, color=COLOR_INK_PRIMARY, fontsize=11)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(COLOR_GRID)

    if title:
        fig.suptitle(title, color=COLOR_INK_PRIMARY, fontsize=12, y=1.02)
    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=200, facecolor=COLOR_SURFACE, bbox_inches="tight")
    return fig


def plot_loss_curves(
    train_loss_history: Sequence[float],
    val_loss_history: Sequence[float],
    save_path: str | Path | None = None,
) -> plt.Figure:
    """Render the training/validation MSE loss curves (replaces notebook cell 18)."""
    epochs = range(1, len(train_loss_history) + 1)
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor=COLOR_SURFACE)
    ax.set_facecolor(COLOR_SURFACE)
    ax.plot(epochs, train_loss_history, color=COLOR_TRAIN, linewidth=2, label="Training loss")
    ax.plot(epochs, val_loss_history, color=COLOR_VAL, linewidth=2, label="Validation loss")
    ax.set_xlabel("Epoch", color=COLOR_INK_MUTED)
    ax.set_ylabel("MSE loss", color=COLOR_INK_MUTED)
    ax.set_title("Training and validation loss", color=COLOR_INK_PRIMARY)
    ax.tick_params(colors=COLOR_INK_MUTED)
    ax.grid(True, color=COLOR_GRID, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color(COLOR_GRID)
    legend = ax.legend(frameon=False, labelcolor=COLOR_INK_PRIMARY)
    fig.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=200, facecolor=COLOR_SURFACE, bbox_inches="tight")
    return fig

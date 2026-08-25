"""Core inference helper shared by evaluate.py and infer.py.

The notebook processed a whole image in one forward pass by treating its 512 rows as
a batch dimension (cell 19). That's efficient and correct, so it's kept as-is here,
just factored into one function instead of being duplicated inline in every evaluation
cell.
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn

from .utils import normalize01


def predict_disparity(
    model: nn.Module,
    left_image: np.ndarray,
    right_image: np.ndarray,
    device: torch.device | None = None,
) -> np.ndarray:
    """Run the model over every row of one stereo pair at once.

    `left_image`/`right_image` are (H, W) grayscale arrays. Returns a (H, W) disparity
    map, min-max normalized to [0, 1] (matching how the ground-truth maps are
    normalized, so the two are directly comparable).
    """
    model.eval()
    if device is None:
        device = next(model.parameters()).device

    left_rows = torch.from_numpy(left_image).float().unsqueeze(1).to(device)  # (H, 1, W)
    right_rows = torch.from_numpy(right_image).float().unsqueeze(1).to(device)

    with torch.no_grad():
        predicted_rows = model(left_rows, right_rows)  # (H, 1, W)

    disparity = predicted_rows.squeeze(1).cpu().numpy()  # (H, W)
    return normalize01(disparity)

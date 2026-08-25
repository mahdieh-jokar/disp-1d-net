"""Disp1DNet baseline architecture: a dual-path 1D-CNN stereo disparity model.

Ported from the "1.3 Training a PyTorch model" section of
notebooks/disp1dnet_training_and_finn_synthesis.ipynb
(cell 14), with the hidden channel width promoted to a constructor argument instead of a
module-level global. Each stereo row (a length-512 signal) is processed independently by
two Conv1d encoders (left, right), concatenated, and decoded back to a length-512 disparity
row. See Jokar, "Disp1DNet: Rapid 1D Stereo Network for Efficient Disparity Map Estimation"
(IEEE, https://ieeexplore.ieee.org/document/10887522/) for the model description (Fig. 1)
and the channel-width ablation (Table I).

The checkpoint shipped in model/stereo1d_baseline.pt was trained with hidden_channels=64
(the default here); see model/README.md.
"""

from __future__ import annotations

import torch
import torch.nn as nn


def _encoder(hidden_channels: int) -> nn.Sequential:
    """One Conv1d encoder branch: two conv+relu+maxpool stages, then one more conv+relu."""
    h = hidden_channels
    return nn.Sequential(
        nn.Conv1d(1, h, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool1d(kernel_size=2),
        nn.Conv1d(h, h, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool1d(kernel_size=2),
        nn.Conv1d(h, h, kernel_size=3, padding=1),
        nn.ReLU(),
    )


class StereoModel(nn.Module):
    """Dual-path 1D CNN that predicts a disparity row from a pair of left/right rows.

    Input: two tensors of shape (batch, 1, row_length), one image row each, single
    grayscale channel. Output: (batch, 1, row_length), the predicted disparity row.
    """

    def __init__(self, hidden_channels: int = 64):
        super().__init__()
        self.hidden_channels = hidden_channels
        h = hidden_channels

        self.path1_combined = _encoder(h)  # left branch
        self.path2_combined = _encoder(h)  # right branch

        self.combined = nn.Sequential(
            nn.Conv1d(2 * h, h, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(h, h, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
            nn.Conv1d(h, h, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Upsample(scale_factor=2),
        )
        self.output = nn.Conv1d(h, 1, kernel_size=3, padding=1)

    def forward(self, left_input: torch.Tensor, right_input: torch.Tensor) -> torch.Tensor:
        left_features = self.path1_combined(left_input)
        right_features = self.path2_combined(right_input)
        combined = torch.cat((left_features, right_features), dim=1)
        decoded = self.combined(combined)
        return self.output(decoded)

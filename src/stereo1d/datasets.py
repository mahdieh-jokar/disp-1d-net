"""Stereo image/disparity loading and the row-level PyTorch Dataset.

Replaces notebook cells 3, 5, 7 (three near-identical load/resize/grayscale/normalize
loops for Right, Left, and the disparity .txt files) and cell 12 (the dataset/dataloader
setup). Two deliberate efficiency/correctness changes relative to the notebook:

1. `load_stereo_images` only loads the image indices you ask for. The notebook always
   loaded all 326 images into memory up front and sliced afterwards, even when a given
   cell only needed a 200-image training range or a 125-image test range.
2. `StereoRowDataset` builds row-level samples lazily via `__getitem__` instead of
   `np.concatenate`-ing every image's rows into one big (N*512, 512) array first. Same
   samples, no extra full-dataset copy sitting in memory.
3. `make_train_val_datasets` defaults to an **image-level** train/val split (a whole
   image's 512 rows go entirely to one side) rather than the notebook's row-level
   `train_test_split`, which could put different rows of the same image on both sides
   of the split. Since neighboring rows of one scene are highly correlated, that
   leaks information from train into validation. Pass `split_level="row"` to reproduce
   the notebook's original behavior exactly.
"""

from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, random_split

from .utils import list_sorted_files, load_disparity_map, load_grayscale_image

Size = tuple[int, int]


def load_stereo_images(
    left_dir: str,
    right_dir: str,
    gt_dir: str,
    indices: list[int],
    size: Size = (512, 512),
) -> tuple[list[np.ndarray], list[np.ndarray], list[np.ndarray]]:
    """Load only the requested image indices (naturally sorted) from the three folders."""
    left_files = list_sorted_files(left_dir)
    right_files = list_sorted_files(right_dir)
    gt_files = list_sorted_files(gt_dir)

    left_images = [load_grayscale_image(left_files[i], size) for i in indices]
    right_images = [load_grayscale_image(right_files[i], size) for i in indices]
    gt_maps = [load_disparity_map(gt_files[i], size) for i in indices]
    return left_images, right_images, gt_maps


class StereoRowDataset(Dataset):
    """Treats each row of each stereo image as one training sample.

    Rows are the natural unit here because rectified stereo pairs share epipolar lines
    row-by-row (see the paper's motivation for 1D, row-wise convolution instead of full
    2D/3D convolution). Sample `i` maps to image `i // rows_per_image`, row
    `i % rows_per_image`.
    """

    def __init__(
        self,
        left_images: list[np.ndarray],
        right_images: list[np.ndarray],
        gt_maps: list[np.ndarray],
    ):
        if not (len(left_images) == len(right_images) == len(gt_maps)):
            raise ValueError("left_images, right_images, and gt_maps must be the same length")
        if len(left_images) == 0:
            raise ValueError("no images given")

        self.left_images = left_images
        self.right_images = right_images
        self.gt_maps = gt_maps
        self.rows_per_image = left_images[0].shape[0]

    def __len__(self) -> int:
        return len(self.left_images) * self.rows_per_image

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        img_idx, row = divmod(index, self.rows_per_image)
        left_row = torch.from_numpy(self.left_images[img_idx][row]).float().unsqueeze(0)
        right_row = torch.from_numpy(self.right_images[img_idx][row]).float().unsqueeze(0)
        gt_row = torch.from_numpy(self.gt_maps[img_idx][row]).float().unsqueeze(0)
        return left_row, right_row, gt_row


def make_train_val_datasets(
    left_images: list[np.ndarray],
    right_images: list[np.ndarray],
    gt_maps: list[np.ndarray],
    val_fraction: float = 0.15,
    seed: int = 42,
    split_level: str = "image",
) -> tuple[Dataset, Dataset]:
    """Split into train/val datasets. See module docstring for `split_level` semantics."""
    if split_level == "image":
        n = len(left_images)
        rng = np.random.default_rng(seed)
        order = rng.permutation(n)
        n_val = int(round(n * val_fraction))
        val_idx, train_idx = order[:n_val], order[n_val:]

        def subset(idx: np.ndarray) -> StereoRowDataset:
            return StereoRowDataset(
                [left_images[i] for i in idx],
                [right_images[i] for i in idx],
                [gt_maps[i] for i in idx],
            )

        return subset(train_idx), subset(val_idx)

    if split_level == "row":
        full_dataset = StereoRowDataset(left_images, right_images, gt_maps)
        n_val = int(round(len(full_dataset) * val_fraction))
        n_train = len(full_dataset) - n_val
        generator = torch.Generator().manual_seed(seed)
        return random_split(full_dataset, [n_train, n_val], generator=generator)

    raise ValueError(f"split_level must be 'image' or 'row', got {split_level!r}")


def build_dataloaders(
    train_dataset: Dataset,
    val_dataset: Dataset,
    batch_size: int = 128,
    num_workers: int = 0,
) -> tuple[DataLoader, DataLoader]:
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    return train_loader, val_loader

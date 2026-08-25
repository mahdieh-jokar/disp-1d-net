"""stereo1d: the pre-quantization baseline pipeline for the Disp1DNet stereo model.

This package reimplements notebook sections 1.1-1.3 of
notebooks/disp1dnet_training_and_finn_synthesis.ipynb (data loading, dataloaders,
float32 PyTorch training) as reusable, efficient modules:

- `stereo1d.model`      the StereoModel architecture
- `stereo1d.datasets`   image loading + the row-level Dataset
- `stereo1d.inference`  shared predict_disparity() helper
- `stereo1d.train`      training / retraining CLI
- `stereo1d.evaluate`   BMP / RMSE evaluation CLI
- `stereo1d.infer`      inference visualization CLI

Brevitas quantization and the FINN/FPGA synthesis stages are not reimplemented here.
They remain in the notebook only (see
notebooks/disp1dnet_training_and_finn_synthesis.ipynb and
resources/finn_build_output_w2a1_64ch/), since the FINN toolchain used to build them is
no longer available to re-run.
"""

from .model import StereoModel

__all__ = ["StereoModel"]

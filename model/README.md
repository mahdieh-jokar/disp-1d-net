# Baseline checkpoint

`stereo1d_baseline.pt` is a PyTorch `state_dict` for `stereo1d.model.StereoModel`,
trained with **`hidden_channels=64`**: the float32 baseline before Brevitas
quantization (notebook section 1.3 / cell 17, originally saved as
`new_model_scripted.pt`; the name is historical, it's a plain state_dict, not a
TorchScript module).

## Loading it

```python
import torch
from stereo1d.model import StereoModel

model = StereoModel(hidden_channels=64)
model.load_state_dict(torch.load("model/stereo1d_baseline.pt", map_location="cpu", weights_only=True))
model.eval()
```

## Validated results

Running `stereo1d.evaluate` with this checkpoint over the paper's test split (image
indices 200–325, 126 images) on the real dataset:

| Metric | Value |
|---|---|
| BMP (τ=0.1) | 0.189 mean (σ=0.049) |
| RMSE | 0.111 mean (σ=0.022) |
| Inference time/image | ~31 ms (GPU) |

This lines up with the published BMP of 22% (see root `README.md` for the citation).
Full per-image numbers: `docs/eval_test_range.csv`.

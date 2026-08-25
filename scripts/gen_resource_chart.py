"""One-off helper: render the per-layer LUT usage chart for docs/results.md from the
FINN build's report/estimate_layer_resources.json. Not part of the package's public
CLI surface -- run directly, not imported.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt

COLOR_BAR = "#2a78d6"
COLOR_SURFACE = "#fcfcfb"
COLOR_INK_PRIMARY = "#0b0b0b"
COLOR_INK_MUTED = "#898781"
COLOR_GRID = "#e1e0d9"

report_path = Path("resources/finn_build_output_w2a1_64ch/report/estimate_layer_resources.json")
data = json.loads(report_path.read_text())
data.pop("total", None)

layers = list(data.keys())
lut_values = [data[layer]["LUT"] for layer in layers]

# drop zero-LUT layers (FMPadding stages) to keep the chart legible
layers, lut_values = zip(*[(l, v) for l, v in zip(layers, lut_values) if v > 0])

fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=COLOR_SURFACE)
ax.set_facecolor(COLOR_SURFACE)
bars = ax.barh(layers, lut_values, color=COLOR_BAR, height=0.6)
ax.invert_yaxis()
ax.set_xlabel("LUTs", color=COLOR_INK_MUTED)
ax.set_title("Per-layer LUT usage (FINN estimate, w2a1, 64ch)", color=COLOR_INK_PRIMARY)
ax.tick_params(colors=COLOR_INK_MUTED)
ax.grid(True, axis="x", color=COLOR_GRID, linewidth=0.8)
for spine in ax.spines.values():
    spine.set_visible(False)
for bar, value in zip(bars, lut_values):
    ax.text(
        bar.get_width() + max(lut_values) * 0.01,
        bar.get_y() + bar.get_height() / 2,
        f"{value:,}",
        va="center",
        color=COLOR_INK_PRIMARY,
        fontsize=9,
    )
fig.tight_layout()

out_path = Path("docs/images/layer_resource_usage.png")
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=200, facecolor=COLOR_SURFACE, bbox_inches="tight")
print(f"Saved {out_path}")

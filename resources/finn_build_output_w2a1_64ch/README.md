# FINN `build_dataflow` output

This directory is the untouched output of `finn.builder.build_dataflow.build_dataflow_cfg`
(notebook cell 54-55, section "3. Building the Network"). It's the quantized,
FPGA-synthesized version of the stereo model, produced by the FINN compiler and Vivado.
It is kept as a
**historical build artifact**, not a reproducible pipeline: the FINN Docker toolchain
itself is still real and available, but I no longer have access to the specific system
it was set up on (see the root `README.md`'s Reproducibility & limitations section).

Build config (from the notebook): target `xc7a200t` (Xilinx Artix-7), 10 ns synthesis
clock period (100 MHz), `target_fps=1,000,000`, `mvau_wwidth_max=80`.

## Layout

| Path | What it is |
|---|---|
| `report/*.json` | The numbers; see `docs/results.md` for the summarized version |
| `intermediate_models/*.onnx` | The model snapshot after each FINN build step (tidy-up, streamlining, HLS conversion, folding, …) |
| `stitched_ip/` | The Vivado project for the stitched IP: Verilog sources, `.xci`/`.xdc` constraints, `make_project.tcl`, and the Vivado run logs (`vivado.log`, `vivado.jou`) |
| `build_dataflow.log` | Full build log |
| `auto_folding_config.json`, `final_hw_config.json`, `time_per_step.json` | FINN's folding/hardware config and per-step timing |

## Key numbers (from `report/*.json`)

| Metric | Value |
|---|---|
| rtlsim throughput | 840,336 images/s |
| Estimated throughput (pre-synthesis) | ~1.49M FPS |
| fmax (out-of-context synthesis) | 171.6 MHz |
| LUT | 229,534 |
| BRAM (18K) | 50 |
| DSP / URAM | 0 / 0 |

The folder name `finn_build_output_w2a1_64ch` records the quantization config this
build used: weights/activations quantized per the notebook's `b64_w2_a1.onnx` export
(64 channels wide, 2-bit weights / 1-bit activations).

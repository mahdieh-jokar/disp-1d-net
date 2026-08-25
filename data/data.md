# Dataset

**Synthetic Stereo Image Data for Algorithm Evaluation**: synthetic driving-scene
stereo pairs generated in 2006 with a prototype of the TNO MARS/PRESCAN vehicle-sensor
simulator. 325 stereo pairs, each with a left image, a right image, and a ground-truth
disparity map.

- **Download:** https://www.cs.auckland.ac.nz/~wvan185/StereoVisionMarsPrescan
- **Citation:** W. van der Mark and D. M. Gavrila, "Real-time dense stereo for
  intelligent vehicles," *IEEE Trans. Intell. Transp. Syst.*, vol. 7, no. 1,
  pp. 38–50, 2006.
- **License:** third-party dataset, not redistributed in this repo. Download it
  yourself from the link above.
- **Split used by this project:** images 1–200 (indices `0`–`199`) for training,
  201–325 (indices `200`–`324`) for testing, matching the paper (see root `README.md`
  for the citation).

## Expected folder layout

Download and extract the dataset into `data/` so it matches what
`src/stereo1d/datasets.py` expects by default:

```
data/
├── OrigImages0tm325/
│   ├── Left/            <- left0000.tif, left0001.tif, ...
│   └── Right/           <- right0000.tif, right0001.tif, ...
└── GroundTruth/
    └── Disparity/
        └── normgtTXT/   <- disparity0000.txt, disparity0001.txt, ...
```

Filenames are matched in natural numeric order (`left0000` before `left0001` before
`left0010`), not left/right/ground-truth by index correspondence. As long as each
folder's files sort into the same pairing order as the original dataset, any consistent
naming works.

If your copy lives elsewhere, pass `--left-dir`, `--right-dir`, `--gt-dir` to
`stereo1d.train`, `stereo1d.evaluate`, or `stereo1d.infer` instead of moving it.

## Ground truth: convert the official download first

The official download's ground truth is **not** plain text. It ships as binary
`disparity####.bin` files: a 6-byte header of three little-endian `uint16` values
(width, height, a scaling factor of 1000), followed by width*height little-endian
`uint16` values. The real disparity at each pixel is the raw value divided by the
scaling factor (the dataset's own bundled readme documents this format).

`src/stereo1d/utils.py`'s `load_disparity_map` reads plain text via `numpy.loadtxt`, so
the `.bin` files need converting once before use. Run:

```bash
python scripts/convert_groundtruth_bin_to_txt.py \
    --input-dir path/to/downloaded/Disparities \
    --output-dir data/GroundTruth/Disparity/normgtTXT
```

This produces exactly the `normgtTXT/` folder the layout above expects. Verified
against this project's own reference conversion: byte-for-byte identical output.

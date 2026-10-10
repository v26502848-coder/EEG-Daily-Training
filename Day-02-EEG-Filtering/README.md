# Day 2 — EEG Filtering

## Objective
Learn how band-pass filtering changes an EEG signal using MNE-Python.

## Dataset
- Dataset: Sleep-EDF Expanded
- File: `SC4001E0-PSG.edf`
- Sampling frequency: 100 Hz
- Channels: EEG Fpz-Cz and EEG Pz-Oz
- Duration analyzed: 60 seconds

## Methods
1. Loaded the original EDF recording using MNE-Python.
2. Selected the two EEG channels.
3. Extracted the first 60 seconds.
4. Created a copy of the EEG data.
5. Applied a 0.5–40 Hz FIR band-pass filter to the copy.
6. Plotted the original and filtered signals for comparison.

## Observations
- The filtered signal retained much of the original waveform.
- The filter attenuates frequency components outside its selected passband.
- Large fluctuations remained after filtering.
- Visual inspection alone cannot establish whether a fluctuation is a neural event or an artifact.

## Limitations
- The EDF metadata generated inconsistent filter warnings when loaded.
- The filter settings used here are for learning and are not automatically appropriate for every EEG research question.
- The 60-second segment is a training example, not a complete sleep analysis.

## Files
- `day2_filtering.py` — Python script for loading and filtering EEG.
- `original_vs_filtered.png` — Comparison plot.

## Tools
- Python
- MNE-Python
- NumPy
- Matplotlib
## Quantitative Comparison

| Channel | Original SD (µV) | Filtered SD (µV) | Reduction |
|---|---:|---:|---:|
| EEG Fpz-Cz | 31.77 | 29.93 | 5.8% |
| EEG Pz-Oz | 7.91 | 7.40 | 6.4% |

Standard deviation decreased in both channels after filtering. This indicates a reduction in overall signal variability, but does not independently establish that noise was removed or that signal quality improved.
# Day 3 — Sleep Stages and Hypnogram

## Objective
Load sleep-stage annotations from Sleep-EDF Expanded, inspect their timing and labels, and visualize the annotated intervals against the PSG recording duration.

## Dataset
- PSG file: `SC4001E0-PSG.edf`
- Annotation file: `SC4001EC-Hypnogram.edf`
- PSG channels: EEG Fpz-Cz, EEG Pz-Oz, EOG horizontal, Resp oro-nasal, EMG submental, Temp rectal, Event marker
- Sampling frequency: 100 Hz

## Methods
1. Loaded the PSG metadata with MNE-Python without preloading all signal samples.
2. Loaded the hypnogram separately using `mne.read_annotations()`.
3. Inspected the first and last annotation intervals.
4. Plotted the original sleep-stage labels, clipping intervals at the PSG recording boundary.
5. Saved the plot as `hypnogram.png`.

## Observations
- PSG duration: 79,500 seconds (22 hours, 5 minutes).
- Hypnogram annotation span: 86,400 seconds (24 hours).
- Number of annotation intervals: 154.
- The first annotation is `Sleep stage W`, from 0 to 30,630 seconds.
- The final annotation is `Sleep stage ?`, from 79,500 to 86,400 seconds.
- The plot preserves the original labels, including separate stages 3 and 4.

## Limitations
- The annotation file extends 6,900 seconds beyond the PSG recording.
- The long wake-labelled intervals require investigation before interpreting the plot as a typical sleep episode.
- Matching filenames and durations do not independently establish correct temporal alignment.
- The hypnogram is a visualization of the annotation timeline clipped to the PSG duration; alignment has not yet been independently verified.
- No sleep-stage classifier or physiological interpretation was performed.

## Files
- `day3_sleep_stages.py` — annotation inspection and hypnogram plotting script.
- `hypnogram.png` — generated hypnogram.

## Tools
- Python
- MNE-Python
- Matplotlib
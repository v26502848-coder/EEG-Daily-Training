# Day 4 — EEG and Sleep-Stage Alignment

## Objective
Inspect the timing relationship between the Sleep-EDF PSG recording and its corresponding hypnogram, then plot a short EEG segment with its recorded sleep-stage annotation.

## Dataset
- PSG file: `SC4001E0-PSG.edf`
- Hypnogram file: `SC4001EC-Hypnogram.edf`
- EEG sampling frequency: 100 Hz
- EEG duration: 79,500 seconds
- Hypnogram duration: 86,400 seconds

## Work completed
- Loaded the EEG recording and hypnogram using MNE.
- Compared recording duration and annotation boundaries.
- Attached the hypnogram annotations to the EEG recording.
- Plotted 60 seconds from 30,630 to 30,690 seconds using EEG Fpz-Cz and EEG Pz-Oz.
- Displayed the recorded sleep-stage annotation alongside both EEG channels.
- Saved the figure as `eeg_sleep_alignment.png`.

## Observations
The selected segment is labelled `Sleep stage 1` in the hypnogram. The EEG channels show fluctuating voltage signals with several larger deflections. Their causes have not been established.

## Data-quality and interpretation caveats
- The hypnogram extends 6,900 seconds beyond the EEG recording. MNE reports that one annotation extending outside the data range was limited when annotations were attached.
- The hypnogram contains long intervals, including a 120-second Stage 1 interval and long wake intervals. The annotation structure requires further investigation.
- Matching recording start times does not independently establish that every sleep-stage label is physiologically correct.
- No sleep-stage classification, artifact diagnosis, or clinical interpretation was performed.

## Output
- `day4_eeg_sleep_alignment.py`
- `eeg_sleep_alignment.png`
- `README.md`

## Next step
Investigate the original annotation structure and scoring epochs before making physiological interpretations or conducting sleep-stage-specific analyses.
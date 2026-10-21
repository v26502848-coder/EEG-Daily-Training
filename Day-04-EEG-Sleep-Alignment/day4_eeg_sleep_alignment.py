from pathlib import Path

import mne 
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

# Locate the project and EEG data
project_path = Path(__file__).resolve().parent.parent
data_folder = project_path / "Day-01-First-EEG" / "data"

psg_path = data_folder / "SC4001E0-PSG.edf"
hypnogram_path = data_folder / "SC4001EC-Hypnogram.edf"

# Load the EEG recording and sleep-stage annotations
raw = mne.io.read_raw_edf(
    psg_path,
    preload=False,
    verbose="ERROR",
)

annotations = mne.read_annotations(hypnogram_path)
# Attach sleep-stage annotations to the EEG recording.
raw.set_annotations(annotations)
print("\nLast 5 annotations in the original hypnogram:")

for onset, duration, stage in zip(
    annotations.onset[-5:],
    annotations.duration[-5:],
    annotations.description[-5:],
):
    print(
        f"{onset:8.1f}–{onset + duration:8.1f} s"
        f" | {duration:6.1f} s | {stage}"
    )

print(f"\nEEG ends at: {raw.n_times / raw.info['sfreq']:.1f} s")
print(
    "Original hypnogram ends at:",
    f"{max(annotations.onset + annotations.duration):.1f} s",
)

print("\nAfter attaching annotations to the EEG:")
print("EEG measurement date:", raw.info["meas_date"])
print("Annotation reference time:", raw.annotations.orig_time)

print("\nAnnotations around the beginning of sleep:")
for onset, duration, stage in zip(
    raw.annotations.onset,
    raw.annotations.duration,
    raw.annotations.description,
):
    if 30600 <= onset <= 30750:
        print(
            f"{onset:8.1f}–{onset + duration:8.1f} s"
            f" | {duration:6.1f} s | {stage}"
        )

# Calculate recording and annotation timing
sfreq = raw.info["sfreq"]
eeg_duration = raw.n_times / sfreq

print("DAY 4: EEG–SLEEP TIMING CHECK")
print("-" * 40)
print(f"EEG sampling frequency: {sfreq} Hz")
print(f"EEG recording duration: {eeg_duration:.1f} seconds")
print(f"EEG recording start: {raw.info['meas_date']}")
print(f"Hypnogram annotations: {len(annotations)}")

print("\nFirst 10 sleep-stage annotations:")
for onset, duration, stage in zip(
    annotations.onset[:10],
    annotations.duration[:10],
    annotations.description[:10],
):
    print(
        f"{onset:8.1f}–{onset + duration:8.1f} s"
        f" | {duration:6.1f} s | {stage}"
    )

print("\nTiming check:")
print(
    "Annotation onset range:",
    f"{annotations.onset.min():.1f} to "
    f"{annotations.onset.max():.1f} seconds",
)
# Select a 60-second segment at the start of Sleep stage 1.
start_time = 30630.0
duration = 60.0
sfreq = raw.info["sfreq"]

picks = ["EEG Fpz-Cz", "EEG Pz-Oz"]

start_sample = int(start_time * sfreq)
stop_sample = int((start_time + duration) * sfreq)

eeg_data = raw.get_data(
    picks=picks,
    start=start_sample,
    stop=stop_sample,
) * 1e6  # Convert volts to microvolts

times = start_time + np.arange(eeg_data.shape[1]) / sfreq

# Find the sleep-stage annotations overlapping this segment.
segment_end = start_time + duration
overlapping_stages = []

for onset, annotation_duration, stage in zip(
    raw.annotations.onset,
    raw.annotations.duration,
    raw.annotations.description,
):
    annotation_end = onset + annotation_duration

    if onset < segment_end and annotation_end > start_time:
        overlapping_stages.append(
            (max(onset, start_time),
             min(annotation_end, segment_end),
             stage)
        )

# Plot EEG signals and their sleep-stage label.
fig, axes = plt.subplots(
    3, 1,
    figsize=(13, 8),
    sharex=True,
    gridspec_kw={"height_ratios": [3, 3, 1]},
)

for i, channel in enumerate(picks):
    axes[i].plot(times - start_time, eeg_data[i], linewidth=0.6)
    axes[i].set_ylabel("µV")
    axes[i].set_title(channel)
    axes[i].grid(alpha=0.3)

stage_ax = axes[2]

for onset, end, stage in overlapping_stages:
    stage_ax.barh(
        0,
        end - onset,
        left=onset - start_time,
        height=0.6,
    )
    stage_ax.text(
        (onset + end) / 2 - start_time,
        0,
        stage,
        ha="center",
        va="center",
        fontsize=8,
    )

stage_ax.set_yticks([])
stage_ax.set_ylabel("Sleep stage")
stage_ax.set_xlabel("Seconds from segment start")
stage_ax.set_xlim(0, duration)

fig.suptitle("Day 4: EEG and Sleep-Stage Alignment")
fig.tight_layout()

output_path = Path(__file__).resolve().parent / "eeg_sleep_alignment.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)

print("\nCombined plot saved to:", output_path)
print("Selected segment:", start_time, "to", segment_end, "seconds")
print("Overlapping labels:", overlapping_stages)
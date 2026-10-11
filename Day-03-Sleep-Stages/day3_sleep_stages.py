
from pathlib import Path

import mne
import matplotlib.pyplot as plt

project_path = Path(__file__).resolve().parent.parent
data_folder = project_path / "Day-01-First-EEG" / "data"

psg_path = data_folder / "SC4001E0-PSG.edf"
hypnogram_path = data_folder / "SC4001EC-Hypnogram.edf"

raw = mne.io.read_raw_edf(psg_path, preload=False, verbose="ERROR")
annotations = mne.read_annotations(hypnogram_path)

recording_duration = raw.n_times / raw.info["sfreq"]
annotation_end = max(
    onset + duration
    for onset, duration in zip(
        annotations.onset, annotations.duration
    )
)

print("PSG duration:", recording_duration, "seconds")
print("Hypnogram end:", annotation_end, "seconds")
print("PSG start:", raw.info["meas_date"])
print("Annotation intervals:", len(annotations))

print("\nFirst 5 annotations:")
for onset, duration, stage in zip(
    annotations.onset[:5],
    annotations.duration[:5],
    annotations.description[:5],
):
    print(f"{onset:8.1f}–{onset + duration:8.1f} s: {stage}")

print("\nLast 5 annotations:")
for onset, duration, stage in zip(
    annotations.onset[-5:],
    annotations.duration[-5:],
    annotations.description[-5:],
):
    print(f"{onset:8.1f}–{onset + duration:8.1f} s: {stage}")

# Preserve the original annotation labels.
stages = [
    "Sleep stage W",
    "Sleep stage 1",
    "Sleep stage 2",
    "Sleep stage 3",
    "Sleep stage 4",
    "Sleep stage R",
    "Sleep stage ?",
]
stage_y = {stage: i for i, stage in enumerate(stages)}

fig, ax = plt.subplots(figsize=(14, 5))

for onset, duration, stage in zip(
    annotations.onset,
    annotations.duration,
    annotations.description,
):
    if onset >= recording_duration:
        continue

    end = min(onset + duration, recording_duration)
    if end <= onset or stage not in stage_y:
        continue

    ax.broken_barh(
        [(onset / 3600, (end - onset) / 3600)],
        (stage_y[stage] - 0.35, 0.7),
    )

ax.set_yticks(range(len(stages)))
ax.set_yticklabels(stages)
ax.invert_yaxis()
ax.set_xlim(0, recording_duration / 3600)
ax.set_xlabel("Time from recording start (hours)")
ax.set_ylabel("Scored stage")
ax.set_title("Sleep-EDF Hypnogram — SC4001")
ax.grid(axis="x", alpha=0.3)

fig.tight_layout()
output_path = Path(__file__).resolve().parent / "hypnogram.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)

print("\nHypnogram saved to:", output_path)

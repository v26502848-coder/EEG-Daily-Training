from pathlib import Path
import mne
import numpy as np
import matplotlib.pyplot as plt

# Locate the original EEG recording
project_path = Path(__file__).resolve().parent.parent
data_path = project_path / "Day-01-First-EEG" / "data" / "SC4001E0-PSG.edf"

# Load the recording
raw = mne.io.read_raw_edf(data_path, preload=True)

# Select the two EEG channels and copy them
eeg = raw.copy().pick(["EEG Fpz-Cz", "EEG Pz-Oz"])

# Keep the first 60 seconds for our exercise
eeg.crop(tmin=0, tmax=60)

print("Channels:", eeg.ch_names)
print("Sampling frequency:", eeg.info["sfreq"], "Hz")
print("Duration:", eeg.times[-1], "seconds")
print("Data shape:", eeg.get_data().shape)
# Create a separate copy for filtering
filtered = eeg.copy()

# Apply a 0.5–40 Hz band-pass filter
filtered.filter(
    l_freq=0.5,
    h_freq=40.0,
    picks=["EEG Fpz-Cz", "EEG Pz-Oz"]
)

print("\n--- After Filtering ---")
print("Channels:", filtered.ch_names)
print("Sampling frequency:", filtered.info["sfreq"], "Hz")
print("Data shape:", filtered.get_data().shape)
# Compare original and filtered EEG
original_data_uv = eeg.get_data() * 1e6
filtered_data_uv = filtered.get_data() * 1e6
times = eeg.times

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

for i, ax in enumerate(axes):
    ax.plot(
        times,
        original_data_uv[i],
        label="Original",
        linewidth=0.5,
        alpha=0.7
    )
    ax.plot(
        times,
        filtered_data_uv[i],
        label="Filtered",
        linewidth=0.5
    )
    ax.set_ylabel(f"{eeg.ch_names[i]}\n(µV)")
    ax.legend()
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel("Time (seconds)")
fig.suptitle("Original vs Filtered EEG — First 60 Seconds")
fig.tight_layout()

output_path = Path(__file__).resolve().parent / "original_vs_filtered.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)

print("Comparison plot saved to:", output_path)
print("\n--- Quantitative Comparison ---")

original_data_uv = eeg.get_data() * 1e6
filtered_data_uv = filtered.get_data() * 1e6

for i, channel in enumerate(eeg.ch_names):
    original_std = np.std(original_data_uv[i])
    filtered_std = np.std(filtered_data_uv[i])

    print(f"\nChannel: {channel}")
    print(f"Original standard deviation: {original_std:.2f} µV")
    print(f"Filtered standard deviation: {filtered_std:.2f} µV")
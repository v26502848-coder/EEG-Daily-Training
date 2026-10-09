from pathlib import Path
import mne
import matplotlib.pyplot as plt

data_path = Path(__file__).resolve().parent / "data" / "SC4001E0-PSG.edf"
output_path = Path(__file__).resolve().parent / "first_eeg_plot.png"

raw = mne.io.read_raw_edf(data_path, preload=True)

# Select the first 60 seconds of the two EEG channels
eeg = raw.copy().pick(["EEG Fpz-Cz", "EEG Pz-Oz"])
eeg.crop(tmin=0, tmax=60)
data = eeg.get_data()

print("EEG data shape:", data.shape)
print("Minimum value:", data.min())
print("Maximum value:", data.max())
print("Any NaN values:", __import__("numpy").isnan(data).any())

import numpy as np

times = eeg.times
data_uv = eeg.get_data() * 1e6

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

for i, ax in enumerate(axes):
    ax.plot(times, data_uv[i], linewidth=0.5)
    ax.set_ylabel(f"{eeg.ch_names[i]}\n(µV)")
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel("Time (seconds)")
fig.suptitle("EEG — First 60 Seconds")
fig.tight_layout()

fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)

print(f"EEG plot saved to: {output_path}")
print("Sampling frequency:", eeg.info["sfreq"], "Hz")
print("Number of samples:", eeg.n_times)
print("Duration:", eeg.times[-1], "seconds")
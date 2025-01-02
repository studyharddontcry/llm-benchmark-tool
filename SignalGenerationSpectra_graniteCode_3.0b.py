import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import argrelextrema, welch, butter, lfilter

# Read the CSV file into a DataFrame
df = pd.read_csv('noisy_sinusoidal.csv')

# Extract time and signal columns from the DataFrame
time = df['Time'].to_numpy()
signal = df['Signal'].to_numpy()

# Perform FFT on the signal to obtain the frequency domain representation
fft_result = fft(signal)

# Compute the magnitude spectrum of the FFT output using SciPy's welch function or similar technique
freq, spec = welch(signal, fs=1/time[1], nperseg=len(signal))

# Apply spectral analysis techniques (e.g., peak picking, smoothing, filtering) to extract estimated frequency components from the magnitude spectrum
peak_indices = argrelextrema(spec, np.greater)[0]
peak_freqs = freq[peak_indices]
peak_specs = spec[peak_indices]

# Plot the original signal versus time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.sca(ax1)
plt.plot(time, signal)
plt.title('Original Signal vs. Time')
plt.xlabel('Time')
plt.ylabel('Signal')

plt.sca(ax2)
plt.plot(freq, spec)
plt.title('Magnitude Spectrum')
plt.xlim(0, 40)
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.show()

# # Read the CSV file into a DataFrame
# df = pd.read_csv('noisy_sinusoidal.csv')

# # Extract time and signal columns from the DataFrame
# time = df['Time'].to_numpy()
# signal = df['Signal'].to_numpy()

# # Perform FFT on the signal to obtain the frequency domain representation
# fft_result = fft(signal)

# # Compute the magnitude spectrum of the FFT output using SciPy's welch function or similar technique
# freq, spec = welch(signal, fs=1/time[1], nperseg=len(signal))

# # Apply spectral analysis techniques (e.g., peak picking, smoothing, filtering) to extract estimated frequency components from the magnitude spectrum
# peak_indices = argrelextrema(spec, np.greater)[0]
# peak_freqs = freq[peak_indices]
# peak_specs = spec[peak_indices]

# # Clean the original signal using extracted frequency components and apply a low-pass filter
# clean_signal = [signal[int(i)] for i in peak_indices]
# filtered_signal = lfilter([1], [1, 30], signal)

# # Plot the original signal versus time
# fig, ax = plt.subplots(figsize=(10, 8))
# plt.plot(time, signal)
# plt.title('Original Signal vs. Time')
# plt.xlabel('Time')
# plt.ylabel('Signal')

# # Plot the filtered signal without Gaussian white noise
# ax2 = ax.twinx()
# ax2.plot(time, filtered_signal, color='red')
# ax2.set_ylabel('Clean Signal', color='red')

# plt.show()
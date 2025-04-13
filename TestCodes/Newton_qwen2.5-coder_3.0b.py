import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Parameters for the signal generation
length = 1000  # Number of samples
sampling_freq = 10  # Sampling frequency in Hz (100 samples per second)
signal_mean = 0  # Mean of the random sine wave
signal_amplitude = 1  # Amplitude of the random sine wave

# Generate a random sine wave signal
t = np.linspace(0, length / sampling_freq, length, endpoint=False)  # Time vector
np.random.seed(0)  # For reproducibility
random_signal = signal_amplitude * np.sin(2 * np.pi * t)

# Parameters for adding noise
noise_stddev = 0.5  # Standard deviation of the Gaussian white noise

# Generate random noise and add it to the signal
np.random.seed(1)  # For reproducibility
noisy_signal = random_signal + noise_stddev * np.random.randn(length)

# Parameters for filtering
cutoff_freq = 2  # Cutoff frequency in Hz
filter_order = 3  # Filter order
btype = 'low'  # Low-pass filter

# Design the low-pass filter
nyquist_freq = 0.5 * sampling_freq
normal_cutoff = cutoff_freq / nyquist_freq
b, a = butter(filter_order, normal_cutoff, btype=btype)

# Apply the filter to the noisy signal
filtered_signal = lfilter(b, a, noisy_signal)

# Plotting the signals
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(t, random_signal, label='Original Sine Wave')
plt.title('Original Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, noisy_signal, label='Noisy Signal')
plt.title('Noisy Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, filtered_signal, label='Filtered Signal')
plt.title('Filtered Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
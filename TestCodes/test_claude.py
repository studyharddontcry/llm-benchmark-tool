import numpy as np
import matplotlib.pyplot as plt

# Create a sample signal
def create_signal(t):
    return np.sin(2 * np.pi * 4 * t) + 0.5 * np.sin(2 * np.pi * 35 * t) + 0.2 * np.random.randn(len(t))

# Generate time array
t = np.linspace(0, 1, 1000)

# Generate the signal
signal = create_signal(t)

# Perform FFT
fft_result = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(t), t[1] - t[0])

# Calculate the magnitude spectrum
magnitude_spectrum = np.abs(fft_result)

# Plot the results
plt.figure(figsize=(12, 8))

# Time domain plot
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Frequency domain plot (spectrum)
plt.subplot(2, 1, 2)
plt.plot(frequencies[:len(frequencies)//2], magnitude_spectrum[:len(frequencies)//2])
plt.title('Frequency Domain (Magnitude Spectrum)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim(0, 50)  # Limit x-axis to 0-50 Hz for better visibility

plt.tight_layout()
plt.show()
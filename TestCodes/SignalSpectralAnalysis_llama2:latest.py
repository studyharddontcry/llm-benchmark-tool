import numpy as np
import pandas as pd
from scipy import fft
import matplotlib.pyplot as plt
from scipy.signal import welch

data = pd.read_csv('noisy_sinusoidal.csv')
time = data['Time']
signal = data['Signal']

fft_result = fft(signal)
magnitude_spectrum = welch(fft_result, signal.size // 2)

# Peak picking
frequencies, amplitudes = [], []
for i in range(len(magnitude_spectrum)):
    if abs(magnitude_spectrum[i]) > 0.5 * max(abs(magnitude_spectrum)):
        frequencies.append(i / len(magnitude_spectrum))
        amplitudes.append(amplitudes[i])
    
# Smoothing
smoothed_frequencies = np.convolve(frequencies, np.ones(len(frequencies)), mode='same')
smoothed_amplitudes = np.convolve(amplitudes, np.ones(len(amplitudes)), mode='same')
    
# Filtering
filtered_frequencies = np.array([])
for i in range(len(smoothed_frequencies)):
    if smoothed_amplitudes[i] > 0.1 * max(smoothed_amplitudes):
        filtered_frequencies = np.vstack((filtered_frequencies, smoothed_frequencies[i]))
        filtered_amplitudes = np.vstack((filtered_amplitudes, smoothed_amplitudes[i]))
    
# Plot the results
plt.plot(filtered_frequencies, filtered_amplitudes)
plt.xlabel('Frequency')
plt.ylabel('Amplitude')
plt.title('Estimated Frequency Components')
plt.show()

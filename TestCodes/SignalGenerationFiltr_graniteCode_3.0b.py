import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import butter, lfilter, welch, argrelextrema

# Read the CSV file into a DataFrame
df = pd.read_csv('noisy_sinusoidal.csv')

# Extract time and signal columns from the DataFrame
time = df['Time'].to_numpy()
signal = df['Signal'].to_numpy()

# Perform FFT on the signal to obtain the frequency domain representation
fft_result = fft(signal)

# Compute the magnitude spectrum of the FFT output using SciPy's welch function or similar technique
freq, spec = welch(signal, fs=1/time[1]) # freq, spec = welch(signal, fs=1/time[1], nperseg=len(signal))

# Analyze the FFT output to identify the frequencies of interest and non-interesting components
# peak_indices = argrelextrema(spec, np.greater)[0]
# peak_freqs = freq[peak_indices]
# non_peak_indices = np.delete(np.arange(len(signal)), peak_indices)
# non_peak_freqs = freq[non_peak_indices]

# Apply a band-pass filter to remove the non-interesting frequencies from the signal
filtered_signal = butter(2, [5, 30], 'bandpass')
filtered_fft_result = lfilter(*filtered_signal, fft_result)

# Plot the original and filtered signals together in one figure
fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax1.plot(time, signal)
ax1.set_title('Original Signal')
ax2.plot(time, filtered_fft_result)
ax2.set_title('Filtered Signal')
ax2.legend(['Original', 'Filtered'])
plt.show()
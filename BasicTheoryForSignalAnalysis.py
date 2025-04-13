import numpy as np
import matplotlib.pyplot as plt

# Create figure with multiple subplots
plt.figure(figsize=(15, 12))

# 1. Demonstrate sampling and aliasing
t = np.linspace(0, 1, 1000)
f_original = 5  # Original frequency
signal_original = np.sin(2*np.pi*f_original*t)

# Different sampling rates
t_undersampled = t[::50]  # Under-sampling
t_adequate = t[::20]      # Adequate sampling
signal_undersampled = np.sin(2*np.pi*f_original*t_undersampled)
signal_adequate = np.sin(2*np.pi*f_original*t_adequate)

plt.subplot(3, 1, 1)
plt.plot(t, signal_original, 'b-', label='Original Signal', alpha=0.5)
plt.plot(t_undersampled, signal_undersampled, 'ro', label='Under-sampled')
plt.plot(t_adequate, signal_adequate, 'go', label='Adequately sampled')
plt.title('Sampling Theory Demonstration')
plt.legend()
plt.grid(True)

# 2. Demonstrate spectral leakage
t_window = np.linspace(0, 3, 1000)
signal_window = np.sin(2*np.pi*2*t_window)

# Apply different windows
rectangular = signal_window[:750]  # Rectangular window (abrupt cutoff)
hanning = signal_window[:750] * np.hanning(750)  # Hanning window

# Calculate FFT
def plot_spectrum(signal, fs=1000):
    spectrum = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1/fs)
    return freqs, np.abs(spectrum)

plt.subplot(3, 1, 2)
freqs_rect, spec_rect = plot_spectrum(rectangular)
freqs_hann, spec_hann = plot_spectrum(hanning)

plt.plot(freqs_rect[freqs_rect>0], spec_rect[freqs_rect>0], 'b-', 
         label='Rectangular Window', alpha=0.7)
plt.plot(freqs_hann[freqs_hann>0], spec_hann[freqs_hann>0], 'r-', 
         label='Hanning Window', alpha=0.7)
plt.title('Spectral Leakage Demonstration')
plt.legend()
plt.grid(True)
plt.xlim(0, 10)

# 3. Demonstrate interpolation effects
t_sparse = np.linspace(0, 1, 20)
t_dense = np.linspace(0, 1, 1000)
signal_sparse = np.sin(2*np.pi*5*t_sparse) + 0.5*np.sin(2*np.pi*10*t_sparse)

# Linear interpolation
from scipy.interpolate import interp1d
interpolator = interp1d(t_sparse, signal_sparse, kind='linear')
signal_interpolated = interpolator(t_dense)

plt.subplot(3, 1, 3)
plt.plot(t_sparse, signal_sparse, 'ro', label='Original Samples')
plt.plot(t_dense, signal_interpolated, 'b-', label='Linear Interpolation', alpha=0.7)
plt.plot(t_dense, np.sin(2*np.pi*5*t_dense) + 0.5*np.sin(2*np.pi*10*t_dense), 'g-', label='Original Signal', alpha=0.5)
plt.title('Linear Interpolation Demonstration')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
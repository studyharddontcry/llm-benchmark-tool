import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.signal import welch  # Use welch instead of psd
import matplotlib.pyplot as plt

def main():
    # Load or generate your signal data here
    # For example:
    # signal_values = np.random.normal(0, 1, 1000)  # Example Gaussian noise

    # Calculate the frequency array using fftfreq
    fs = 1 / time_step
    freqs = fftfreq(len(signal_values), d=fs)

    # Compute the PSD using welch
    mag_spectrum, freqs_welch = welch(signal_values, fs=fs)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(freqs, abs(fft(signal_values)))
    plt.title('FFT of Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    plt.subplot(2, 1, 2)
    plt.semilogy(freqs_welch, mag_spectrum)
    plt.title('PSD of Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density (dB/Hz)')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
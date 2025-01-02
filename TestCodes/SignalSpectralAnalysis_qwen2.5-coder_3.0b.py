import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
import pandas as pd

def read_noisy_signal(file_path):
    """Reads the noisy sinusoidal signal from the CSV file."""
    data = pd.read_csv(file_path)
    time = data['Time'].values
    signal_values = data['Signal'].values
    return time, signal_values

def apply_fft(signal_values):
    """Applies FFT to the signal using SciPy's fft function."""
    return fft.fft(signal_values)

def perform_spectral_analysis(fourier_transform):
    """Performs spectral analysis on the Fourier transform output."""
    freqs = np.fft.fftfreq(len(fourier_transform), d=1.0)
    psd = 2 * np.abs(fourier_transform) ** 2 / len(fourier_transform)

    # Plotting optional
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, psd, label='Power Spectral Density')
    # plt.xscale('log')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Power Spectral Density')
    plt.legend()
    plt.show()

    # Determine which frequencies are not of interest
    # For simplicity, let's assume we want to remove low-frequency drift and high-frequency harmonics.
    # You can adjust these thresholds based on your specific requirements.
    low_frequency_threshold = 0.5  # Hz
    high_frequency_threshold = 200  # Hz

    # Filter out unwanted frequencies
    filtered_fft = np.zeros_like(fourier_transform)
    for i in range(len(freqs)):
        if low_frequency_threshold <= freqs[i] <= high_frequency_threshold:
            filtered_fft[i] = fourier_transform[i]

    return filtered_fft, freqs

def clean_signal(filtered_fft):
    """Reconstructs the cleaned signal from the Fourier transform."""
    return fft.ifft(filtered_fft)

def main(file_path, time_step=1.0):
    """Main function to execute the analysis and cleaning process."""
    # Step 1: Read the noisy sinusoidal signal
    time, signal_values = read_noisy_signal(file_path)

    # Step 2: Apply FFT
    fourier_transform = apply_fft(signal_values)

    # Step 3: Perform spectral analysis
    filtered_fft, freqs = perform_spectral_analysis(fourier_transform)

    # Step 4: Clean the signal
    cleaned_signal_values = clean_signal(filtered_fft)

    # Output the cleaned signal in a suitable format (e.g., NumPy array)
    print("Cleaned Signal:", cleaned_signal_values)

if __name__ == "__main__":
    file_path = "noisy_sinusoidal.csv"
    main(file_path)
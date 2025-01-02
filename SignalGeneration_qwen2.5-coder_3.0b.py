import numpy as np
from scipy import fft, signal
import pandas as pd

def read_noisy_signal(file_path):
    """Reads the noisy sinusoidal signal from the CSV file."""
    data = pd.read_csv(file_path)
    time = data['Time'].values
    signal_values = data['Signal'].values
    return time, signal_values

def perform_fft(signal_values):
    """Applies FFT to the signal using SciPy's fft function."""
    return fft.fft(signal_values)

def analyze_and_filter(fourier_transform, f1=4.0, f2=35.0):
    """Analyze and filter the Fourier transform output."""
    data = pd.read_csv('noisy_sinusoidal.csv')
    time = data['Time'].values
    freqs = np.fft.fftfreq(len(fourier_transform), d=1.0 / len(time))
    
    # Create a mask to identify frequencies of interest
    freq_mask = (freqs >= f1) & (freqs <= f2)
    
    # Apply the frequency mask to the FFT result
    filtered_fft = fourier_transform * freq_mask
    
    return filtered_fft

def clean_signal(filtered_fft):
    """Reconstructs the cleaned signal from the filtered FFT."""
    return fft.ifft(filtered_fft)

def plot_signals(time, original_signal, cleaned_signal):
    """Plots the original and cleaned signals for visualization."""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(time, original_signal, label='Original Signal')
    plt.title('Original Signal with Noise')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(time, cleaned_signal.real, label='Cleaned Signal')
    plt.title('Cleaned Signal (4.0 Hz and 35.0 Hz)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def main(file_path):
    # Assuming the CSV file contains the correct data
    time, signal_values = read_noisy_signal(file_path)
    fourier_transform = perform_fft(signal_values)
    
    filtered_fft = analyze_and_filter(fourier_transform, f1=4.0, f2=35.0)
    cleaned_signal = clean_signal(filtered_fft)
    
    plot_signals(time, signal_values, cleaned_signal)

# Example usage
file_path = "noisy_sinusoidal.csv"
main(file_path)
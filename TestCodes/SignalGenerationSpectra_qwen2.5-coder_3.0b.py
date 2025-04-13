import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.signal import welch
import matplotlib.pyplot as plt

def main(file_path):
    # Load the data from the CSV file
    df = pd.read_csv(file_path)
    
    # Extract the time and signal columns
    time_values = df['Time'].values
    signal_values = df['Signal'].values
    time_step = 1.0 / len(time_values)
    fs = 1 / time_step
    
    # Perform FFT on the signal
    fft_result = fft(signal_values)
    
    # Compute the frequency array
    frequencies = fftfreq(len(time_values), d=time_step).real  # d is the sampling interval
    
    # Compute the magnitude spectrum
    mag_spectrum, freqs_welch = welch(signal_values, fs=fs)
    
    # Peak picking to extract estimated frequency components
    peak_indices = np.where(mag_spectrum > 0.5)[0]  # Threshold for peak detection
    peak_frequencies = frequencies[peak_indices]
    
    # Output the estimated frequency components with their corresponding amplitude values
    print("Estimated Frequency Components:")
    for freq, amp in zip(peak_frequencies, mag_spectrum[peak_indices]):
        print(f"Frequency: {freq:.2f} Hz, Amplitude: {amp:.2f}")
    
    # Plot the original signal vs. time
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_values, signal_values, label='Original Signal')
    plt.title('Noisy Sinusoidal Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    # Plot the magnitude spectrum
    plt.subplot(2, 1, 2)
    plt.semilogy(freqs_welch, mag_spectrum, label='Magnitude Spectrum')
    plt.title('Magnitude Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    
    # Show the plots
    plt.tight_layout()
    plt.show()

# Example usage
file_path = "noisy_sinusoidal.csv"
main(file_path)
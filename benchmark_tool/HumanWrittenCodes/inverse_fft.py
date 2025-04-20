import numpy as np
import matplotlib.pyplot as plt

def plot_inverse_fft(freq_data, fs):
    """
    Reconstruct and plot a real time-domain signal from its complex
    frequency-domain representation using the inverse Fast Fourier Transform.

    Parameters
    ----------
    freq_data : 1-D array_like
        Complex FFT bins (full spectrum, as returned by ``np.fft.fft``).
    fs : float
        Sampling frequency in hertz.
    """

    freq_data = np.asarray(freq_data, dtype=complex)
    n_samples = freq_data.size

    time_signal = np.fft.ifft(freq_data).real

    t = np.arange(n_samples) / fs

    plt.plot(t, time_signal)
    plt.title("Signal Reconstructed via Inverse FFT")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
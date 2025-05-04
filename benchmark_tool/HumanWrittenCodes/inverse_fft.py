import numpy as np
import matplotlib.pyplot as plt

def plot_inverse_fft(freq_data, fs):
    """
    Reconstruct a real time-domain signal from its complex
    frequency-domain representation using the inverse Fast Fourier Transform.

    Parameters
    ----------
    freq_data : 1-D array_like
        Complex FFT bins (full spectrum, as returned by ``np.fft.fft``).
    """

    freq_data = np.asarray(freq_data, dtype=complex)
    n_samples = freq_data.size

    time_signal = np.fft.ifft(freq_data).real

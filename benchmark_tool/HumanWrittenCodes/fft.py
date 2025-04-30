import numpy as np

def fft_function(signal):
    """
    Perform FFT on a given signal and return the frequency and amplitude spectrum.

    Parameters
    ----------
    signal : 1-D array_like
        Input signal to be transformed.
    sampling_rate : float
        Sampling rate of the input signal.

    Returns
    -------
    fft_result : ndarray
        FFT of the input signal.
    """
    signal = np.asarray(signal, dtype=float)

    n = len(signal)
    fft_result = np.fft.fft(signal)

    return fft_result

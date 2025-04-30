import numpy as np

def fft_function(signal, sampling_rate):
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
    freq : ndarray
        Frequencies corresponding to the FFT result.
    amplitude : ndarray
        Amplitude spectrum of the input signal.
    """
    signal = np.asarray(signal, dtype=float)

    n = len(signal)
    fft_result = np.fft.fft(signal)

    return fft_result

test_signal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fft_result = fft_function(test_signal, 1000)
print(f"fft result: {fft_result}")
import numpy as np
from scipy.signal import butter, lfilter

def low_pass_filter(signal, fs, cutoff_freq=10, order=4):
    """
    Applies a low-pass Butterworth filter to the input signal.
    
    Args:
        signal (numpy.array): The input signal.
        fs (float): Sampling frequency of the signal.
        cutoff_freq (float): Cutoff frequency for the low-pass filter.
        order (int): Order of the filter.
    
    Returns:
        numpy.array: Filtered signal.
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, signal)
    return y

import numpy as np
from scipy.signal import resample

def resample_signal(input_signal, n_samples):
    """
    Resample a signal to a specified number of points.

    Parameters
    ----------
    input_signal : 1-D array_like
        Signal samples to be resampled.
    n_samples : int
        Desired number of samples after resampling.

    Returns
    -------
    resampled : ndarray
        Resampled signal.
    """
    input_signal = np.asarray(input_signal, dtype=float)

    # Resample
    resampled = resample(input_signal, n_samples)

    return resampled

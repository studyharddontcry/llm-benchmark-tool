import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample

def plot_resampled_signal(time, signal, n_samples):
    """
    Resample a signal to a specified number of points and plot
    both the original and resampled waveforms.

    Parameters
    ----------
    time : 1-D array_like
        Original time axis.
    signal : 1-D array_like
        Samples corresponding to `time`.
    n_samples : int
        Desired number of samples after resampling.

    Returns
    -------
    new_time : ndarray
        Time axis for the resampled signal.
    resampled : ndarray
        Resampled signal.
    """
    time = np.asarray(time, dtype=float)
    signal = np.asarray(signal, dtype=float)

    # Resample
    resampled = resample(signal, n_samples)

    # New time axis spans the same total duration
    new_time = np.linspace(time[0], time[-1], n_samples, endpoint=False)

    # Plot original vs. resampled
    plt.plot(time, signal, "b", label="Original")
    plt.plot(new_time, resampled, "or-", label=f"Resampled ({n_samples} pts)")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Signal Resampling")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return new_time, resampled

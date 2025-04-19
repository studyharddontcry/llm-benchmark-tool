def plot_fft_spectrum(signal, fs):
    """Plot the one-sided magnitude spectrum of a real signal.

    Parameters
    ----------
    signal : 1-D array_like
        Time-domain samples.
    fs : float
        Sampling frequency in hertz.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.fftpack
    
    signal = np.asarray(signal, dtype=float)
    n_samples = signal.size

    # Fast Fourier Transform
    yf = scipy.fftpack.fft(signal)

    # Frequency axis (positive half only)
    xf = np.linspace(0.0, fs / 2, n_samples // 2, endpoint=False)

    # One‑sided magnitude spectrum
    mag = 2.0 / n_samples * np.abs(yf[: n_samples // 2])

    fig, ax = plt.subplots()
    ax.plot(xf, mag)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_title("Magnitude Spectrum (FFT Output)")
    plt.tight_layout()
    plt.show()
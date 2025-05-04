import numpy as np

def generate_sine_wave(frequency, sample_rate, duration):
    """
    Generate a sine wave with specified parameters.
    
    This function creates a sinusoidal signal commonly used in digital signal
    processing for testing and analysis purposes.
    
    Args:
        frequency (float): Frequency of the sine wave in Hz
        sample_rate (float): Sampling rate in Hz
        duration (float): Duration of the signal in seconds
    
    Returns:
        np.ndarray: Array containing the generated sine wave samples
    """
    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Generate sine wave
    signal = np.sin(2 * np.pi * frequency * t)
    
    return signal
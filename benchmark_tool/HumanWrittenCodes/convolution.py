import numpy as np

def convolve_signals(signal, kernel):
    """
    Performs convolution of a signal and a kernel using numpy's convolve function.
    
    Args:
        signal: Input signal array to be convolved
        kernel: Convolution kernel array
    
    Returns:
        np.ndarray: Result of the convolution operation
        
    """
    signal = np.asarray(signal)
    kernel = np.asarray(kernel)
    
    result = np.convolve(signal, kernel, mode='full')
    
    return result
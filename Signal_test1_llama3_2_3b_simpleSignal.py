import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Generate time array from 0 to 1 second with 10000 samples
t = np.linspace(0, 1, 10000)

# Define the frequencies for each component (in Hz)
f1 = 80
f2 = 50
f3 = 150

# Calculate the corresponding amplitudes and phases
a1, a2, a3 = 1.0, 0.5, 0.25
phi1, phi2, phi3 = 0, np.pi/4, np.pi/2

# Generate each frequency component as a sine wave with the correct amplitude and phase
x1 = a1 * np.sin(2*np.pi*f1*t + phi1)
x2 = a2 * np.sin(2*np.pi*f2*t + phi2)
x3 = a3 * np.sin(2*np.pi*f3*t + phi3)

# Add the three frequency components together
signal_x = x1 + x2 + x3

# Generate some random noise with a mean of 0 and standard deviation of 0.1
noise = np.random.normal(0, 0.1, len(t))

# Combine the signal and noise by adding them together
x_with_noise = signal_x + noise

# Plot the result
plt.figure(figsize=(10,6))
plt.plot(x_with_noise)
plt.title("Signal with Noise")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()
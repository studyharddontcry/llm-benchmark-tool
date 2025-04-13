import numpy as np
import matplotlib.pyplot as plt

def normal_equation_approximator(x, y):
    """
    Approximate a sequence of values using the normal equations for a polynomial of degree 2.

    Parameters:
    x (array-like): An array of x-coordinates.
    y (array-like): An array of corresponding y-values.

    Returns:
    tuple: A tuple containing the coefficients [a, b, c] of the polynomial function f(x) = ax^2 + bx + c.
    """
    # Ensure input arrays are NumPy arrays
    x = np.array(x)
    y = np.array(y)

    # Number of data points
    n = len(x)

    # Construct matrices A and b for the normal equations Ax = b
    A = np.zeros((n, 3))  # Correct shape to (n, 3)
    b = np.zeros(n)

    for i in range(n):
        A[i, 0] = x[i]**2  # Coefficient of x^2
        A[i, 1] = x[i]     # Coefficient of x
        A[i, 2] = 1        # Constant term (coefficient of x^0)
        b[i] = y[i]

    # Solve the normal equations Ax = b
    a = np.linalg.solve(A, b)

    return a

# Sample usage with the given sequence of values
x_sample = [0, 0.2, 0.5, 0.7, 0.8, 1, 1.2, 1.6, 1.9, 2]
y_sample = [5.2, 4.3, 4.4, 4.9, 5.5, 6, 6.1, 7, 7.8, 8]

# Compute the coefficients
coefficients = normal_equation_approximator(x_sample, y_sample)

# Print the computed coefficients
print("Computed Coefficients:", coefficients)

# Plotting
plt.scatter(x_sample, y_sample, label='Data Points')
x_fit = np.linspace(min(x_sample), max(x_sample), 100)
y_fit = coefficients[0] * x_fit**2 + coefficients[1] * x_fit + coefficients[2]
plt.plot(x_fit, y_fit, color='red', label='Fitted Curve')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data Approximation using Normal Equations')
plt.legend()
plt.show()
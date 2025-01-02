import numpy as np

# Example 12.2: Gauss-Jordan method
A = np.array([[4, -1, 1],
              [1, 6, 2],
              [-1, -2, 5]], dtype=np.float64)
b = np.array([[4], [9], [2]], dtype=np.float64)

# Combine A and b into a single augmented matrix
AB = np.hstack((A, b))

# Initialize S with zeros of the same shape as AB
# S = np.zeros_like(AB)

## Iterate over each column of the augmented matrix
for i in range(AB.shape[0]):
    # Localization of the maximum element of i-th column
    max_val = abs(AB[i, :]).argmax()
    
    if max_val < AB.shape[0]:
        # Row exchange
        AB[[i, max_val], :] = AB[[max_val, i], :]
    
    # Division of the i-th row by the diagonal element
    AB[i, :] /= AB[i, i]
    
    # Elimination
    for ii in range(i + 1, AB.shape[0]):
        if ii < AB.shape[0]:
            AB[ii, :] -= AB[ii, i] * AB[i, :]

# Extract the solution from the last column of the augmented matrix
x = AB[:, -1]

print("Solution:", x)
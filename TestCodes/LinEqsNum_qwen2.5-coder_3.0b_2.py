import numpy as np

def gauss_jordan_solver(A, b):
    """
    Solve a system of linear equations using the Gauss-Jordan method.

    Parameters:
    A (list of lists): 2D list representing the matrix of coefficients on the left side.
    b (list): List representing the vector of numbers on the right side.

    Returns:
    list: List containing the solution to the system of linear equations.
    """
    # Convert inputs to NumPy arrays for efficient computation
    A = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64)

    # Combine A and b into an augmented matrix [A | b]
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

    # Perform row operations to transform the augmented matrix into reduced row echelon form
    for i in range(len(augmented_matrix)):
        # Ensure the pivot element is non-zero
        if augmented_matrix[i, i] == 0:
            # Find a row below that has a non-zero pivot element and swap rows
            for j in range(i + 1, len(augmented_matrix)):
                if augmented_matrix[j, i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    break

        # Scale the current row so that the pivot element is 1
        augmented_matrix[i] /= augmented_matrix[i, i]

        # Eliminate all other elements in the current column
        for j in range(len(augmented_matrix)):
            if j != i:
                augmented_matrix[j] -= augmented_matrix[j, i] * augmented_matrix[i]

    # Extract the solution from the last column of the transformed matrix
    x = augmented_matrix[:, -1].flatten()

    return x.tolist()

# Example usage:
A = [[3, 2], [1, -4]]
b = [9, -14]
solution = gauss_jordan_solver(A, b)
print("Solution:", solution) 
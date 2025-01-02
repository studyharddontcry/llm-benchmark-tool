import numpy as np

def gauss_jordan_elimination(A, b):
    """
    Solve a system of linear equations using the Gauss-Jordan elimination method.
    
    Parameters:
        A (numpy.ndarray): The coefficient matrix of the system of equations.
        b (numpy.ndarray): The vector representing the constants on the right side of the equations.
        
    Returns:
        numpy.ndarray: A numpy array containing the solutions to the system of equations in [x, y] format.
        
    Raises:
        ValueError: If the matrix is not square (more equations than variables) or if there's an issue during elimination.
    """
    # Convert inputs to np.float64
    A = np.array(A).astype(np.float64)
    b = np.array(b).reshape(-1, 1).astype(np.float64)
    
    # Check if A is square
    if A.shape[0] != A.shape[1]:
        raise ValueError("The matrix must be square for Gauss-Jordan elimination.")
    
    try:
        # Augment the coefficient matrix and vector with zeros
        augmented_matrix = np.hstack((A, b))
        
        # Perform Gaussian elimination
        for i in range(augmented_matrix.shape[0]):
            # Find the pivot row
            max_row = i
            for j in range(i + 1, augmented_matrix.shape[0]):
                if abs(augmented_matrix[j, i]) > abs(augmented_matrix[max_row, i]):
                    max_row = j
            
            # Swap rows to make the pivot element non-zero
            augmented_matrix[[i, max_row]] = augmented_matrix[[max_row, i]]
            
            # Check if the pivot value is zero or not a float
            pivot_value = augmented_matrix[i, i]
            if np.isclose(pivot_value, 0.0) or not isinstance(pivot_value, (float, np.float64)):
                raise ValueError("Matrix is singular; no unique solution exists.")
            
            # Scale the current row to make the pivot element 1
            augmented_matrix[i] /= pivot_value
            
            # Eliminate the current column from other rows
            for j in range(augmented_matrix.shape[0]):
                if j != i:
                    multiplier = augmented_matrix[j, i]
                    augmented_matrix[j] -= multiplier * augmented_matrix[i]
        
        # Extract the solutions
        solution = augmented_matrix[:, -1]
    
    except ZeroDivisionError:
        raise ValueError("Matrix is singular; no unique solution exists.")
    
    return solution

# Example usage:
A = [[4, -1, 1], [1, 6, 2], [-1, -2, 5]]

b = [4, 9, 2]
print(gauss_jordan_elimination(A, b))
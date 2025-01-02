import numpy as np 
def solve_system_linear_equations(A, b):
    """
    Solves a system of linear equations using the Gauss-Jordan method.
    """
    # Check if the input matrices are square and have the same number of rows as the number of equations
    if not np.shape(A) == (A.shape[0], A.shape[1]) or A.shape[1] != len(b):
        raise ValueError("Invalid input matrix size")

    # Convert matrix A to upper triangular form
    U = np.linalg.inv(A)

    # Find solution by multiplying U and b
    x = np.dot(U, b)

    return x

A = np.array([[4, -1, 1],
              [1, 6, 2],
              [-1, -2, 5]], dtype=np.float64)
b = np.array([[4], [9], [2]], dtype=np.float64)

sol = solve_system_linear_equations(A, b)
print(sol)
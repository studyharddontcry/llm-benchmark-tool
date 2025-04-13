import numpy as np

def gauss_jordan(A, b):
    n = len(A)
    A = np.array(A, dtype=np.float64)
    b = np.array(b, dtype=np.float64).reshape(-1, 1)

    if A.shape != (n, n) or b.shape != (n, 1):
        raise ValueError("Invalid dimensions of input arrays")

    if not np.issubdtype(A.dtype, np.number) or not np.issubdtype(b.dtype, np.number):
        raise ValueError("Invalid data types of input arrays")

    for i in range(n):
        pivot_index = -1
        max_pivot = 0

        for j in range(n):
            if A[j, i] != 0:
                if abs(A[j, i]) > max_pivot:
                    pivot_index = j
                    max_pivot = abs(A[j, i])

        if pivot_index == -1:
            raise ValueError("System of equations is underdetermined or has no solution")

        A[[i, pivot_index]] = A[[pivot_index, i]]
        b[[i, pivot_index]] = b[[pivot_index, i]]

        for j in range(n):
            if j != i and A[j, i] != 0:
                factor = A[j, i] / A[i, i]
                A[j, :] -= factor * A[i, :]
                b[j] -= factor * b[i]

    x = np.linalg.solve(A, b)
    return x.flatten().tolist()

A = [[4, -1, 1], [1, 6, 2], [-1, -2, 5]]

b = [4, 9, 2]

print(gauss_jordan(A, b))
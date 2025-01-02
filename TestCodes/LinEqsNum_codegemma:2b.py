import numpy as np
import math


def gauss_jordan(A, b):
    A = np.array(A)
    b = np.array(b)
    if A.shape[0] != A.shape[1]:
        return False
    if A.shape[0] != b.shape[0]:
        return False
    n = A.shape[0]
    for i in range(n):
        A_i = A[i, :]
        b_i = b[i]
        if A_i.sum() == 0:
            return False
        elif A_i[i] != 1:
            A_i = A_i / A_i[i]
            b_i = b_i / A_i[i]
        for j in range(n):
            if i != j:
                A_j = A[j, :]
                b_j = b[j]
                a_ij = A_j[i]
                b_ij = b_j
                A_j = A_j - a_ij * A_i
                b_j = b_j - a_ij * b_i
                A[j, :] = A_j
                b[j] = b_j
    return A, b


def gauss_jordan_method(A, b):
    if gauss_jordan(A, b):
        A, b = gauss_jordan(A, b)
        return np.round(b, 2)
    else:
        return False

A = [[4, -1, 1],
    [1, 6, 2],
    [-1, -2, 5]]

b = [4, 9, 2]

print(gauss_jordan_method(A, b))
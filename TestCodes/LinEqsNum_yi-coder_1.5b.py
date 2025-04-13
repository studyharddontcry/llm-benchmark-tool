import numpy as np
def solve_system(A,b):
    # Augment matrix A with b on the right side
    Ab = np.column_stack((A, b)) 
    
    for i in range(max(np.shape(A))):
        # Find the row with maximum pivot element
        max_elem = abs(Ab[i:, i]).argmax() + i
        if Ab[max_elem, i] == 0.0:  
            raise ValueError('Matrix is singular or does not have a unique solution')
        # Swap the max row with current row (either row i or row j)
        Ab[[i, max_elem]] = Ab[[max_elem, i]]
        # Make all other elements in this column zero 
        for k in range(i+1, np.shape(A)[0]):
            multiplier = -Ab[k, i] / float(Ab[i, i])
            # Subtract multiples of the current row from the others
            Ab[k, :] += multiplier * Ab[i, :] 
    
    # Obtain solution with columns of the result matrix:
    solution = np.diagonal(Ab)
    return solution

A = np.array([[4, -1, 1],
              [1, 6, 2],
              [-1, -2, 5]], dtype=np.float64)
b = np.array([[4], [9], [2]], dtype=np.float64)

print(solve_system(A,b))
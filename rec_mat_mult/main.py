#
# Standard Recursive Matrix Multiplication (RecMatMult)
#
# Input: n x n integer matrices X and Y
# Output: Z = X * Y
# Assumption: n is a power of 2
# Complexity: O(n^3) - T(n) = 8T(n/2) + O(n^2)
#
import numpy as np

def go(X, Y):
    n = X.shape[0]

    # Base case: 1x1 matrix
    if n == 1:
        return X * Y

    # Divide: Partition A and B into n/2 x n/2 submatrices
    k = n // 2

    A, B = X[:k, :k], X[:k, k:]
    C, D = X[k:, :k], X[k:, k:]

    E, F = Y[:k, :k], Y[:k, k:]
    G, H = Y[k:, :k], Y[k:, k:]

    # Combine: Reconstruct the full matrix from quadrants
    Z = np.zeros((n, n), dtype=X.dtype)
    Z[:k, :k], Z[:k, k:] = go(A, E) + go(B, G), go(A, F) + go(B, H)
    Z[k:, :k], Z[k:, k:] = go(C, E) + go(D, G), go(C, F) + go(D, H)

    return Z

# Example Usage
# n = 4 # n must be a power of 2 for this simple implementation
# A = np.random.randint(0, 10, (n, n))
# B = np.random.randint(0, 10, (n, n))

A = np.array([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
])

B = np.array([
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
    [1, 2, 3, 4],
])

expect = A @ B
actual = go(A, B)
print("Expect:\n", expect)
print("Actual:\n", actual)
assert(np.array_equal(expect, actual))

# ➜  Algorithms-Illuminated git:(main) ✗ source ./.venv/bin/activate
# (.venv) ➜  Algorithms-Illuminated git:(main) ✗ python3 ./rec_mat_mult/main.py
# Expect:
#  [[10 20 30 40]
#  [10 20 30 40]
#  [10 20 30 40]
#  [10 20 30 40]]
# Actual:
#  [[10 20 30 40]
#  [10 20 30 40]
#  [10 20 30 40]
#  [10 20 30 40]]

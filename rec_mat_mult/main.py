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

def pretty_print(A, label=''):
    col_width = max(len(str(x)) for x in A.flat)
    if len(label):
        print(label)
        n = A.shape[0]
        spaces = n - 1
        print('-' * (n * col_width + spaces))

    fmt = f'{{:>{col_width}d}}'
    for row in A:
        print(' '.join(fmt.format(x) for x in row))
    print()

def main():
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
    pretty_print(A, 'A')
    pretty_print(B, 'B')
    pretty_print(expect, 'A * B (expect)')
    pretty_print(actual, 'A * B (actual)')
    assert(np.array_equal(expect, actual))

if __name__ == "__main__":
    main()

# ➜  rec_mat_mult git:(main) ✗ uv run ./main.py
# A
# -------
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4

# B
# -------
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4
# 1 2 3 4

# A * B (expect)
# -----------
# 10 20 30 40
# 10 20 30 40
# 10 20 30 40
# 10 20 30 40

# A * B (actual)
# -----------
# 10 20 30 40
# 10 20 30 40
# 10 20 30 40
# 10 20 30 40

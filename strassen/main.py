#
# Strassen's Recursive Matrix Multiplication
#
# Input: n x n integer matrices X and Y
# Output: Z = X * Y
# Assumption: n is a power of 2
# Complexity: O(n^log2(7))
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
    P1 = go(A, F - H)
    P2 = go(A + B, H)
    P3 = go(C + D, E)
    P4 = go(D, G - E)
    P5 = go(A + D, E + H)
    P6 = go(B - D, G + H)
    P7 = go(A - C, E + F)
    Z[:k, :k], Z[:k, k:] = (P5 + P4 - P2 + P6), (P1 + P2)
    Z[k:, :k], Z[k:, k:] = (P3 + P4), (P1 + P5 - P3 - P7)
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
    n = 4 # n must be a power of 2 for this simple implementation
    A = np.random.randint(0, 10, (n, n))
    B = np.random.randint(0, 10, (n, n))

    expect = A @ B
    actual = go(A, B)
    pretty_print(A, 'A')
    pretty_print(B, 'B')
    pretty_print(expect, 'A * B (expect)')
    pretty_print(actual, 'A * B (actual)')
    assert(np.array_equal(expect, actual))

if __name__ == "__main__":
    main()

# ➜  strassen git:(main) ✗ uv run ./main.py
# A
# -------
# 3 8 3 3
# 9 2 9 6
# 1 8 4 8
# 1 2 8 4

# B
# -------
# 7 3 1 9
# 1 7 9 2
# 6 7 7 8
# 0 1 5 8

# A * B (expect)
# ---------------
#  47  89 111  91
# 119 110 120 205
#  39  95 141 121
#  57  77  95 109

# A * B (actual)
# ---------------
#  47  89 111  91
# 119 110 120 205
#  39  95 141 121
#  57  77  95 109

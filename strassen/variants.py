#
# Strassen-family Recursive Matrix Multiplication (2x2 block form)
#
# Methods:
#   - "strassen"  : classical Strassen scheme (7 recursive multiplies)
#   - "winograd"  : Winograd rearrangement of Strassen (7 multiplies, fewer additions)
#   - "basis2017" : alternative-basis 7-multiply scheme (basis change + recombination)
#
# All methods:
#   - Recursively split X and Y into 2x2 blocks
#   - Perform 7 recursive multiplications
#   - Recombine into result blocks
#
# Assumption: n is a power of 2
#
import numpy as np


def go(X: np.ndarray, Y: np.ndarray, method: str = "strassen") -> np.ndarray:
    n = X.shape[0]

    # Base case: 1x1 matrix multiply
    if n == 1:
        return X * Y

    k = n // 2

    # Partition X into 2x2 block matrix
    # X = [[A11 A12]
    #      [A21 A22]]
    A11, A12 = X[:k, :k], X[:k, k:]
    A21, A22 = X[k:, :k], X[k:, k:]

    # Partition Y into 2x2 block matrix
    # Y = [[B11 B12]
    #      [B21 B22]]
    B11, B12 = Y[:k, :k], Y[:k, k:]
    B21, B22 = Y[k:, :k], Y[k:, k:]

    # Allocate result matrix
    Z = np.zeros((n, n), dtype=X.dtype)

    # ============================================================
    # Classical Strassen scheme
    # ============================================================
    if method == "strassen":

        # 7 recursive multiplications
        M1 = go(A11 + A22, B11 + B22, method)
        M2 = go(A21 + A22, B11, method)
        M3 = go(A11, B12 - B22, method)
        M4 = go(A22, B21 - B11, method)
        M5 = go(A11 + A12, B22, method)
        M6 = go(A21 - A11, B11 + B12, method)
        M7 = go(A12 - A22, B21 + B22, method)

        # Recombine into C blocks
        C11 = M1 + M4 - M5 + M7
        C12 = M3 + M5
        C21 = M2 + M4
        C22 = M1 - M2 + M3 + M6

        Z[:k, :k] = C11
        Z[:k, k:] = C12
        Z[k:, :k] = C21
        Z[k:, k:] = C22
        return Z

    # ============================================================
    # Winograd rearrangement of Strassen
    # Same 7 multiplies, different additive structure
    # ============================================================
    if method == "winograd":

        # Core recursive products
        t = go(A11, B11, method)
        u = go(A21 - A11, B12 - B22, method)
        v = go(A21 + A22, B12 - B11, method)

        # w reuses t to reduce total additions
        w = t + go(A21 + A22 - A11, B11 + B22 - B12, method)

        # Recombine result blocks
        C11 = t + go(A12, B21, method)
        C12 = w + v + go(A11 + A12 - A21 - A22, B22, method)
        C21 = w + u + go(A22, B21 + B12 - B11 - B22, method)
        C22 = w + u + v

        Z[:k, :k] = C11
        Z[:k, k:] = C12
        Z[k:, :k] = C21
        Z[k:, k:] = C22
        return Z

    # ============================================================
    # 2017 alternative-basis 7-multiply scheme
    # Performs a basis change on A22 and B22 blocks
    # ============================================================
    if method == "basis2017":

        # Basis transformation of lower-right blocks
        A22p = A12 - A21 + A22
        B22p = B12 - B21 + B22

        # Linear combinations used by recursive multiplies
        t1 = A21 + A22p
        t2 = A22p - A12
        t3 = A22p - A11
        t4 = B22p - B11
        t5 = B21 + B22p
        t6 = B22p - B12

        # 7 recursive multiplications
        M1 = go(A11, B11, method)
        M2 = go(A12, B21, method)
        M3 = go(A21, t4, method)
        M4 = go(A22p, B22p, method)
        M5 = go(t1, t5, method)
        M6 = go(t2, t6, method)
        M7 = go(t3, B12, method)

        # Initial recombination
        C11 = M1 + M2
        C12 = M5 - M7
        C21 = M3 + M6
        C22 = M5 + M6 - M2 - M4

        # Final correction step required by basis change
        C12 = C12 - C22
        C21 = C22 - C21

        Z[:k, :k] = C11
        Z[:k, k:] = C12
        Z[k:, :k] = C21
        Z[k:, k:] = C22
        return Z

    raise ValueError(
        f"Unknown method: {method!r}. Use 'strassen', 'winograd', or 'basis2017'."
    )

def pretty_print(A, label=''):
    col_width = max(len(str(int(x))) for x in A.flat)
    if label:
        print(label)
        n = A.shape[0]
        print('-' * (n * col_width + (n - 1)))
    fmt = f'{{:>{col_width}d}}'
    for row in A:
        print(' '.join(fmt.format(int(x)) for x in row))
    print()

def main():
    n = 4  # power of 2
    X = np.random.randint(0, 10, (n, n), dtype=int)
    Y = np.random.randint(0, 10, (n, n), dtype=int)

    expect = X @ Y

    for method in ["strassen", "winograd", "basis2017"]:
        actual = go(X, Y, method=method)
        print(f"=== {method} ===")
        assert np.array_equal(expect, actual), f"Mismatch for {method}"

    pretty_print(X, "X")
    pretty_print(Y, "Y")
    pretty_print(expect, "X * Y (expect)")
    pretty_print(go(X, Y, "strassen"), "X * Y (strassen)")
    pretty_print(go(X, Y, "winograd"), "X * Y (winograd)")
    pretty_print(go(X, Y, "basis2017"), "X * Y (basis2017)")

if __name__ == "__main__":
    main()

# ➜  strassen git:(main) ✗ uv run strassen.py
# === strassen ===
# === winograd ===
# === basis2017 ===
# X
# -------
# 0 1 6 6
# 4 9 0 4
# 8 2 4 0
# 1 9 7 7

# Y
# -------
# 5 3 4 0
# 7 2 8 0
# 5 9 3 2
# 0 1 3 8

# X * Y (expect)
# ---------------
#  37  62  44  60
#  83  34 100  32
#  74  64  60   8
# 103  91 118  70

# X * Y (strassen)
# ---------------
#  37  62  44  60
#  83  34 100  32
#  74  64  60   8
# 103  91 118  70

# X * Y (winograd)
# ---------------
#  37  62  44  60
#  83  34 100  32
#  74  64  60   8
# 103  91 118  70

# X * Y (basis2017)
# ---------------
#  37  62  44  60
#  83  34 100  32
#  74  64  60   8
# 103  91 118  70

#
# Recursive Matrix Multiplication
#
# Input: n x n integer matrices X and Y
# Output: Z = X * Y
# Assumption: n is a power of 2
#

N = 2

X = [[1, 2],
     [3, 4]]

Y = [[5, 6],
     [7, 8]]

def sub_matrix(A):
    return [[A[0][0]]], [[A[0][1]]], [[A[1][0]]], [[A[1][1]]]

def go(X, Y):
    N = len(X)
    if N == 1:
        return X[0][0] * Y[0][0]

    #
    # X = | A B |    Y = | E F |
    #     | C D |        | G H |
    #
    A, B, C, D = sub_matrix(X)
    E, F, G, H = sub_matrix(Y)

    #
    # X * Y = | AE + BG    AF + BH |
    #         | CE + DG    CF + DH |
    #
    AE, BG = go(A, E), go(B, G); AF, BH = go(A, F), go(B, H)
    CE, DG = go(C, E), go(D, G); CF, DH = go(C, F), go(D, H)
    return [[AE + BG, AF + BH],
            [CE + DG, CF + DH]]

def pretty_print(A):
    for row in A:
        print(row)
    print()

pretty_print(go(X, Y))

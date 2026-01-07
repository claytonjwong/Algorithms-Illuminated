#
# Straightforward Matrix Multiplication
#
# Input: n x n integer matrices X and Y
#
# Output: Z = X * Y
#

N = 2

X = [[1, 2],
     [3, 4]]

Y = [[5, 6],
     [7, 8]]

Z = [[0] * N for _ in range(N)]

for i in range(N):
    for j in range(N):
        for k in range(N):
            Z[i][j] += X[i][k] * Y[k][j]

pretty_print = lambda A: [print(row) for row in A] and print()

pretty_print(X)
pretty_print(Y)
pretty_print(Z)

# ➜  matrix_multiplication git:(main) ✗ python3 ./main.py
# [1, 2]
# [3, 4]

# [5, 6]
# [7, 8]

# [19, 22]
# [43, 50]

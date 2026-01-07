#
# Straightforward Matrix Multiplication
#
# Input: n x n integer matrices X and Y
#
# Output: Z = X * Y
#

N = 2

X = [1 2
     3 4]

Y = [5 6
     7 8]

Z = zeros(Int64, N, N)

for i in 1:N
    for j in 1:N
        for k in 1:N
            Z[i, j] += X[i, k] * Y[k, j]
        end
    end
end

function pretty_print(A)
    for row in eachrow(A)
        println(row)
    end
    println()
end

pretty_print(X)
pretty_print(Y)
pretty_print(Z)

# ➜  matrix_multiplication git:(main) ✗ julia ./main.jl
# [1, 2]
# [3, 4]

# [5, 6]
# [7, 8]

# [19, 22]
# [43, 50]

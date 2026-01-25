# You are given a sorted (from smallest to largest) array A of N distinct integers which can be positive, negative, or zero.  Design the fastest algorithm you can for deciding whether there is an index i such that A[i] = i.

# use case: if the value is less-than the index, search right half

#    -3 -2 -1  0  4
#     0  1  2  3  4
#                 ^

# use case: if the value is greater than the index, search left half

#     0  2  3  4  5
#     0  1  2  3  4
#     ^

def same(A):
    i, j = 0, len(A) - 1
    while i < j:
        k = (i + j) // 2
        if A[k] < k:
            i = k + 1
        else:
            j = k
    return A[i] == i

def run(A, ok=False):
    assert(same(A) == ok)

run([0, 2, 3, 4, 5], True)
run([-3, -2, -1, 0, 4], True)

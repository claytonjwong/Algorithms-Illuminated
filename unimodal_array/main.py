
# Problem: You are given a unimodal array of n distinct elemnts, meaning that its entries are in increasing order up until its maximum element, after which its elemnets are in decreasing order.  Give an algorithm to compute the maximum element of a unimodal array that runs in O(logN) time.

def best(A):
    i, j = 0, len(A) - 1
    while i < j:
        k = (i + j) // 2
        if A[k] < A[k + 1]:
            i = k + 1
        else:
            j = k
    return A[i]

def run(A):
    error = f'NOT ({best(A)} == {max(A)})'
    assert best(A) == max(A), error

# small inputs to test edge cases
run([0, 1, 0])
run([1, 3, 1])
run([2, 5, 4])

# mediuim inputs
run([0, 2, 4, 6, 8, 6, 4, 2])
run([1, 4, 7, 9, 8, 3])
run([3, 5, 9, 12, 10, 6, 2])

# peak near beginning/end
run([1, 5, 4, 3, 2])
run([0, 2, 4, 6, 5])

# larger inputs
run([0, 1, 3, 6, 10, 15, 21, 18, 14, 9, 5, 2])
run([2, 4, 6, 8, 11, 14, 17, 16, 13, 9, 5, 1])
run([1, 5, 10, 20, 35, 50, 49, 30, 15, 7, 2])
run([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
run([0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 34, 21, 13, 8, 5, 3, 2, 1, 0])

import random
def random_unimodal(seed=0):
    A = []
    random.seed(seed)
    while len(A) < int(1e4):
        A.append(random.randint(0, int(1e9)))
    A.sort()
    L = A[:len(A) // 2]
    R = A[len(A) // 2:]
    return L + list(reversed(R))

for _ in range(10):
    run(random_unimodal())

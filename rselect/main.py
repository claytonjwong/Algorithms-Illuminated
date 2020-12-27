from random import uniform
from math import floor

def partition(A, L, R):
    i = L + 1
    j = L + 1
    k = floor(uniform(L, R))
    A[L], A[k] = A[k], A[L]          # swap pivot A[k] with first element of subarray A[L]
    while j <= R:
        if A[j] < A[L]:              # maintain loop invariant A[i] < pivot < A[j]
            A[i], A[j] = A[j], A[i]
            i += 1
        j += 1
    A[L], A[i - 1] = A[i - 1], A[L]  # swap pivot A[L] with last value less-than pivot A[i - 1]
    return i - 1

def rselect(A, i, L, R):
    k = partition(A, L, R)
    if i == k:
        return A[k]  # 🎯 lucky guess
    if i < k:
        R = k - 1
    else:
        L = k + 1
    return rselect(A, i, L, R)

def run(filename, i):
    A = []
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            A.append(int(line))
    N = len(A)
    return rselect(A, i - 1, 0, N - 1)  # -1 for 0-based indexing

print('problem6.5test1.txt:', run('problem6.5test1.txt', 5))   # problem6.5test1.txt: 5469
print('problem6.5test2.txt:', run('problem6.5test2.txt', 50))  # problem6.5test2.txt: 4715

from math import floor

def sort(A):
    def go(A):
        N = len(A)
        if N < 2:
            return [A, 0]
        half = floor(N / 2)
        first,  inv1 = go(A[:half])
        second, inv2 = go(A[half:])
        third,  inv3 = merge(first, second)
        return [third, inv1 + inv2 + inv3]
    def merge(A, B, inv = 0):
        C = []
        i = 0
        j = 0
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                C.append(A[i]); i += 1
            else:
                inv += len(A) - i        # ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.append(B[j]); j += 1
        C.extend(A[i:])
        C.extend(B[j:])
        return [C, inv]
    return go(A)

def run(filename):
    A = []
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            A.append(int(line))
    _, inv = sort(A)
    return inv

print(f"problem3.5test.txt: {run('problem3.5test.txt')}")  # problem3.5test.txt: 28
print(f"problem3.5.txt: {run('problem3.5.txt')}")          # problem3.5.txt: 2407905288

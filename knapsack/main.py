from functools import lru_cache

def top_down(A, K):
    N = len(A)
    total = [0] * N
    @lru_cache(maxsize = None)                                                          # 🤔 memo
    def go(i = 0, k = K):
        if i == N:                                                                      # 🛑 empty set
            return 0
        value, weight = A[i]
        include = go(i + 1, k - weight) + value if 0 <= k - weight else float('-inf')  # ✅ include A[i]
        exclude = go(i + 1, k)                                                         # 🚫 exclude A[i]
        return max(include, exclude)                                                   # 🎯 best
    return go()

def bottom_up(A, K):
    N = len(A)
    dp = [[float('-inf')] * (K + 1) for _ in range(N + 1)]                                 # 🤔 memo
    for j in range(K):                                                                     # 🛑 empty set
        dp[0][j] = 0
    for i in range(1, N + 1):
        for k in range(1, K + 1):
            value, weight = A[i - 1]
            include = dp[i - 1][k - weight] + value if 0 <= k - weight else float('-inf')  # ✅ include A[i]
            exclude = dp[i - 1][k]                                                         # 🚫 exclude A[i]
            dp[i][k] = max(include, exclude)                                               # 🎯 best
    return dp[N][K]

def run(filename):
    A = []
    with open(filename) as fin:
        line = fin.readline()
        [K, N] = [int(word) for word in line.split()]  # K capacity, N items
        while True:
            line = fin.readline()
            if not line:
                break
            value, weight = [int(word) for word in line.split()]
            A.append([value, weight])
    a = top_down(A, K)
    b = bottom_up(A, K)
    assert(a == b)
    print(f'{filename}: {a}')

run('problem16.7test.txt')  # problem16.7test.txt: 2493893

#
# Programming Problem 18.8: All-Pairs Shortest Paths
#
# In this problem, each file describes a directed graph. The first line of the file indicates the number
# of vertices and edges, respectively. Each subsequent line describes an edge (the first two numbers are its tail
# and head, respectively) and its length (the third number). NOTE: edge lengths might be negative, and the graphs
# may or may not be negative cycles.
#
# Test cases: (contributed by Matt Davis) What is the shortest shortest path in the graphs described in this file
# and in this file? (I.e., the minimum, over choices of an origin s and a destination t, of a shortest s-t path in the graph.)
# (If the graph has a negative cycle, your algorithm should detect that fact.) (Answer: -2 and "contains a negative cycle," respectively.)
#
# Challenge data set: Repeat the previous problem for the graphs described in the following files: graph #1, graph #2, graph #3, and graph #4.
#

key = lambda i, j: f'{i},{j}'

def floyd_warshall(E, N):
    dp = [[[float('inf')] * (N + 1) for _ in range(N + 1)] for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i == j:
                dp[0][i][j] = 0
            elif key(i, j) in E:
                dp[0][i][j] = E[key(i, j)]
    for k in range(1, N + 1):
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                dp[k][i][j] = min(dp[k - 1][i][j], dp[k - 1][i][k] + dp[k - 1][k][j])
    return dp[N]

def floyd_warshall_memopt(E, N):
    pre = [[float('inf')] * (N + 1) for _ in range(N + 1)]
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i == j:
                pre[i][j] = 0
            elif key(i, j) in E:
                pre[i][j] = E[key(i, j)]
    for k in range(1, N + 1):
        cur = [[float('inf')] * (N + 1) for _ in range(N + 1)]
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                cur[i][j] = min(pre[i][j], pre[i][k] + pre[k][j])
        pre, cur = cur, pre
    return pre

def run(filename):
    E = {}
    N = 0
    first = True
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            if not first:
                u, v, w = [int(x) for x in line.strip().split(' ')]
                E[key(u, v)] = w
            else:
                N = [int(x) for x in line.strip().split(' ')][0]
                first = False
    a = floyd_warshall_memopt(E, N)
    # b = floyd_warshall(E, N)
    # for i in range(1, N + 1):
    #     for j in range(1, N + 1):
    #         assert(a[i][j] == b[i][j])  # 💩 sanity check
    cycle = False
    for i in range(1, N + 1):
        if a[i][i] < 0:
            cycle = True
    if cycle:
        print(f'{filename}: contains a negative cycle')
        return
    best = float('inf')
    for row in a:
        best = min(best, *row)
    print(f'{filename}: {best}')

run('problem18.8test1.txt')  # problem18.8test1.txt: -2
run('problem18.8test2.txt')  # problem18.8test2.txt: contains a negative cycle
run('problem18.8file1.txt')  # problem18.8file1.txt: contains a negative cycle
run('problem18.8file2.txt')  # problem18.8file2.txt: contains a negative cycle
run('problem18.8file3.txt')  # problem18.8file3.txt: -19
# run('problem18.8file4.txt')
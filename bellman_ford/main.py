from collections import deque

# bellman-ford: N - 1 edge relaxations (u -> v of cost w) [ie. attempting to relax M edges N - 1 times] given N vertices
def bell(E, N, start = 1, INF = int(1e6)):
    dist = [INF] * N
    dist[start] = 0
    k = N - 1
    while k:
        for u, v, w in E:
            dist[v] = min(dist[v], dist[u] + w)
        k -= 1
    return dist

# shortest-paths faster algorithm: only attempt to relax candidate edges (note: adjacency list needed)
def spfa(E, N, start = 1, INF = int(1e6)):
    dist = [INF] * N
    dist[start] = 0
    adj = {i: [] for i in range(N)}
    for u, v, w in E:
        adj[u].append([v, w])
    q = deque([start])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w; q.append(v)
    return dist

def run(filename):
    E = []
    N = 0
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            line = line.strip()
            A = [word for word in line.split('\t') if len(word)]
            u = int(A[0])
            for i in range(1, len(A)):
                v, w = [int(x) for x in A[i].split(',')]
                E.append([u, v, w])
            N += 1
    a = bell(E, N + 1)  # +1 for 1-based indexing
    b = spfa(E, N + 1)
    assert(a == b)
    return b

dist = run('test.txt')
print(','.join(str(dist[x]) for x in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]))  # 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068

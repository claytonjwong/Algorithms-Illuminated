from random import randint
from heapq import heappush, heappop

def prim(N, adj, total = 0):
    q = []
    seen = set()
    start = randint(1, N); seen.add(start)
    for w, v in adj[start]:
        heappush(q, [w, v])
    while q:
        cost, u = heappop(q)
        if u in seen:
            continue
        total += cost; seen.add(u)
        for w, v in adj[u]:
            if v not in seen:
                heappush(q, [w, v])
    return total

def run(filename):
    adj = {}
    first = True
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            words = line.split()
            if not first:
                u, v, w = [int(x) for x in words]
                if u not in adj: adj[u] = []
                if v not in adj: adj[v] = []
                adj[u].append([w, v])
                adj[v].append([w, u])
            else:
                N, M = [int(x) for x in words]
                first = False
    cost = prim(N, adj)
    print(f'{filename}: {cost}')

run('problem15.9test.txt') # problem15.9test.txt: 14
run('problem15.9.txt')     # problem15.9.txt: -3612829

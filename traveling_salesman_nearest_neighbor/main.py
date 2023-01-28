from collections import defaultdict

N, M = -1, -1
adj = defaultdict(list)
cost, key = {}, lambda u, v: f'{u},{v}'
with open('input.txt') as input:
    for line in input:
        A = [int(x) for x in line.strip().split(' ')]
        if len(A) == 3:
            u, v, w = A
            adj[u].append(v); cost[key(u, v)] = w
            adj[v].append(u); cost[key(v, u)] = w
        elif len(A) == 2:
            N, M = A

start = 1
u, seen, path = start, set([start]), [start]
while len(seen) < N:
    best, best_v = float('inf'), -1
    for v in adj[u]:
        if v not in seen:
            cand = cost[key(u, v)]
            if best > cand:
                best = cand; best_v = v
    u = best_v; seen.add(best_v); path.append(best_v)
path.append(start) # add last edge to complete the tour
t = sum(cost[key(path[i - 1], path[i])] for i in range(1, len(path)))
print(f'total: {t}  path: {path}')
# total: 29  path: [1, 2, 3, 4, 5, 1]
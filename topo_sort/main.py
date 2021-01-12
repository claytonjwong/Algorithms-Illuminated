from collections import deque

class Solution:
    def __init__(self, adj):
        self.adj = adj
        self.N = len(adj)
        self.seen = set()
        self.m = {}

    def init(self, start):
        self.color = start
        self.seen.clear()
        self.m.clear()

    def topo_sort_bfs(self):
        self.init(1)         # 👉 color forward from 1..N
        self.bfs()
        return self.to_string()

    def topo_sort_dfs(self):
        self.init(self.N)  # 👈 color reverse from N..1 (as the recursive stack unwinds)
        for u, _ in self.adj.items():
            self.dfs(u)
        return self.to_string()

    def bfs(self):
        degree = {}
        for _, neighbors in self.adj.items():
            for v in neighbors:
                degree[v] = 1 + (degree[v] if v in degree else 0)
        q = deque(u for u, _ in self.adj.items() if u not in degree)
        self.seen.update(*q)
        while q:
            u = q.popleft()
            self.m[u] = self.color; self.color += 1
            for v in adj[u]:
                degree[v] -= 1
                if not degree[v] and v not in self.seen:
                    q.append(v); self.seen.add(v)

    def dfs(self, u):
        if u in self.seen:
            return
        self.seen.add(u)
        for v in adj[u]:
            self.dfs(v)
        self.m[u] = self.color; self.color -= 1

    def to_string(self):
        s = []
        for u, color in self.m.items():
            s.append(f'{u}: {color}')
        return '\n'.join(s)

#
# graph from Quiz 8.3 on page 45 of Algorithms Illuminated: Part 2
#
adj = {
    's': ['v', 'w'],
    'v': ['t'],
    'w': ['t'],
    't': []
}
solution = Solution(adj)

print(f'BFS:\n{solution.topo_sort_bfs()}\n\nDFS:\n{solution.topo_sort_dfs()}')

#    BFS:
#    s: 1
#    v: 2
#    w: 3
#    t: 4

#    DFS:
#    t: 4
#    v: 3
#    w: 2
#    s: 1

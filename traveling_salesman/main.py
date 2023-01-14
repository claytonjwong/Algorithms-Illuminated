import os
os.chdir('/Users/claytonjwong/sandbox/Algorithms-Illuminated/traveling_salesman')

from random import randint
from collections import defaultdict

class Solution():
    def init(self, input_file):
        self.best = int(1e9 + 7)
        self.best_path = []
        self.M = 0
        self.N = 0
        self.adj = defaultdict(set)
        self.cost = defaultdict(int)
        with open(input_file) as input:
            for i, line in enumerate(input):
                A = [int(x) for x in line.strip().split(' ')]
                if 0 < i:
                    u, v, w = A
                    self.adj[u].add(v); self.cost[(u, v)] = w
                    self.adj[v].add(u); self.cost[(v, u)] = w
                else:
                    self.N, self.M = A
    def run(self, input_file):
        self.init(input_file)
        self.start = 1
        self.go(self.start, [self.start], set([self.start]))
        return self.best, self.best_path

    def go(self, u, path, seen, t = 0):
        if len(seen) == self.N:
            t += self.cost[(u, self.start)] # connect ultimate edge of tour
            if self.start in self.adj[u] and t < self.best:
                self.best = t
                self.best_path = path[:]
            return
        for v in self.adj[u]:
            if v not in seen:
                path.append(v); seen.add(v)
                self.go(v, path, seen, t + self.cost[(u, v)])
                path.pop(); seen.remove(v)

s = Solution()
for input_file in ['quiz19.2.txt', 'quiz20.7.txt']:
    best, path = s.run(input_file)
    print(f'{input_file}  best: {best}  path: {path}')
# quiz19.2.txt  best: 13  path: [1, 2, 4, 3]
# quiz20.7.txt  best: 23  path: [1, 3, 2, 5, 4]
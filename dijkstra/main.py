from abc import ABC, abstractmethod
from heapq import heappush, heappop

INF = int(1e9 + 7)

class BaseSolution(ABC):
    @abstractmethod
    def run(self, filename, queries):
        raise NotImplementedError

class NaiveSolution(BaseSolution):
    def dijkstra(self, E):
        dist = {}
        seen = set()
        start = 1
        dist[start] = 0; seen.add(start)
        while True:
            found = False
            best_v = INF
            best_w = INF
            for u, v, w in E:
                if u not in seen or v in seen:
                    continue
                found = True
                if best_w > dist[u] + w:
                    best_v = v
                    best_w = dist[u] + w
            if not found:
                break
            v, w = best_v, best_w
            dist[v] = w; seen.add(v)
        return dist
    def run(self, filename, queries):
        E = []
        with open(filename) as fin:
            while True:
                line = fin.readline()
                if not line:
                    break
                words = line.split()
                u = int(words[0])
                for i in range(1, len(words)):
                    v, w = map(int, words[i].split(','))
                    E.append([ u, v, w ])
        dist = self.dijkstra(E)
        return ' '.join(str(dist[x]) for x in queries)

class HeapSolution(BaseSolution):
    def dijkstra(self, adj, start = 1):
        dist = {}
        seen = set()
        q = [[ 0, start ]]
        while len(q):
            cost, u = heappop(q)
            if u in seen:
                continue
            dist[u] = cost; seen.add(u)
            for w, v in adj[u]:
                if v not in seen:
                    heappush(q, [ dist[u] + w, v ])
        return dist
    def run(self, filename, queries):
        adj = {}
        with open(filename) as fin:
            while True:
                line = fin.readline()
                if not line:
                    break
                words = line.split()
                u = int(words[0])
                if u not in adj:
                    adj[u] = []
                for i in range(1, len(words)):
                    v, w = map(int, words[i].split(','))
                    adj[u].append([ w, v ])
        dist = self.dijkstra(adj)
        return ' '.join(str(dist[x]) for x in queries)

def run(solution):
    print(solution.run('problem9.8test.txt', [1, 2, 3, 4, 5, 6, 7, 8]))
    print(solution.run('problem9.8.txt', [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]))

run(NaiveSolution())
#    0 1 2 3 4 4 3 2
#    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068

run(HeapSolution())
#    0 1 2 3 4 4 3 2
#    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068

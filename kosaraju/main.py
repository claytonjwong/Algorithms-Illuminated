from collections import deque
from functools import cmp_to_key

class BaseSolution:
    def __init__(self, adj, rev):
        self.adj = adj
        self.rev = rev

class RecursiveSolution(BaseSolution):
    def topo_sort(self):
        list = deque()
        seen = set()
        def go(u):
            if u in seen:
                return
            seen.add(u)
            for v in self.rev[u]:
                go(v)
            list.appendleft(u)
        for u in self.rev.keys():
            go(u)
        return list

    def kosaraju(self):
        lists = []
        seen = set()
        def go(u, list):
            if u in seen:
                return
            seen.add(u)
            list.append(u)
            for v in self.adj[u]:
                go(v, list)
        for u in self.topo_sort():
            list = []
            go(u, list)
            lists.append(list.copy())
        lists.sort(key = cmp_to_key(lambda a, b: len(b) - len(a)))
        return lists

class IterativeSolution(BaseSolution):
    def topo_sort(self):
        list = deque()
        seen = set()
        for u in self.rev.keys():
            if u in seen:
                continue
            stack = [ u ]; seen.add(u)
            while len(stack):
                u = stack[-1]
                for v in self.rev[u]:
                    if v not in seen:
                        stack.append(v); seen.add(v)
                if u == stack[-1]:
                    list.appendleft(stack.pop())
        return list

    def kosaraju(self):
        lists = []
        seen = set()
        for u in self.topo_sort():
            if u in seen:
                continue
            list = deque()
            stack = [ u ]; seen.add(u)
            while len(stack):
                u = stack[-1]
                for v in self.adj[u]:
                    if v not in seen:
                        stack.append(v); seen.add(v)
                if u == stack[-1]:
                    list.appendleft(stack.pop())
            lists.append(list.copy())
        lists.sort(key = cmp_to_key(lambda a, b: len(b) - len(a)))
        return lists

def run(filename):
    adj, rev = {}, {}
    with open(filename) as fin:
        while True:
            line = fin.readline().strip()
            if not line:
                break
            u, v = [int(x) for x in line.split()]
            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            if u not in rev: rev[u] = []
            if v not in rev: rev[v] = []
            adj[u].append(v)
            rev[v].append(u)
    # solution = RecursiveSolution(adj, rev)
    solution = IterativeSolution(adj, rev)
    A = solution.kosaraju()
    print(filename + ': ' + ' '.join(str(len(scc)) for scc in A[:5]))

run('section8.6.5page64.txt')  # Graph from section 8.6.5 on page 64 of Algorithms Illuminated: Part 2
run('problem8.10test1.txt')    # Test case #1: A 9-vertex 11-edge graph. Top 5 SCC sizes: 3,3,3,0,0
run('problem8.10test2.txt')    # Test case #2: An 8-vertex 14-edge graph. Top 5 SCC sizes: 3,3,2,0,0
run('problem8.10test3.txt')    # Test case #3: An 8-vertex 9-edge graph. Top 5 SCC sizes: 3,3,1,1,0
run('problem8.10test4.txt')    # Test case #4: An 8-vertex 11-edge graph. Top 5 SCC sizes: 7,1,0,0,0
run('problem8.10test5.txt')    # Test case #5: A 12-vertex 20-edge graph. Top 5 SCC sizes: 6,3,2,1,0
run('problem8.10.txt')         # Challenge data set: Vertices are labeled as positive integers from 1 to 875714

#    section8.6.5page64.txt: 4 3 3 1
#    problem8.10test1.txt: 3 3 3
#    problem8.10test2.txt: 3 3 2
#    problem8.10test3.txt: 3 3 1 1
#    problem8.10test4.txt: 7 1
#    problem8.10test5.txt: 6 3 2 1
#    problem8.10.txt: 434821 968 459 313 211

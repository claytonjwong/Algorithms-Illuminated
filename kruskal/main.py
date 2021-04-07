from functools import cmp_to_key

def kruskal(E, total = 0):
    M = len(E)
    P = [i for i in range(M)] # 🙂 parent representatives of 1..M disjoint sets
    def find(x):
        P[x] = P[x] if P[x] == x else find(P[x])
        return P[x]
    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return False
        P[a] = b # 🎲 arbitary choice
        return True
    E.sort(key = cmp_to_key(lambda first, second: first[2] - second[2])) # sort edges by nondecreasing weight
    for u, v, w in E:
        if union(u, v):
            total += w
    return total

def run(filename):
    E = []
    first = True
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            values = [int(x) for x in line.strip().split()]
            if not first:
                u, v, w = values # edge u -> v of weight w
                E.append([ u, v, w ])
            else:
                first = False # ignore first line with N vertices and M edges
    cost = kruskal(E)
    print(f'{filename}: {cost}')

run('problem15.9test.txt') # problem15.9test.txt: 14
run('problem15.9.txt')     # problem15.9.txt: -3612829

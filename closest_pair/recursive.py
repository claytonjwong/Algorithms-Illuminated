P = [(1, 8), (2, 5), (4, 7), (6, 3)]
N = len(P)
INF = 1234567890  # arbitary choice for infinity

def dist(first, second):
    x1, y1 = first
    x2, y2 = second
    return (x1 - x2) ** 2 \
         + (y1 - y2) ** 2

def split(Px, Py):
    return Px[0] # TODO: implement me

def best(P):
    best_dist = 123456789
    best_pair = None
    for a in P:
        for b in P:
            if a != b:
                cand = dist(a, b)
                if best_dist >= cand:
                    best_dist = cand
                    best_pair = (a, b)
    return best_pair

def go(Px, Py):
    # Base case
    if len(Px) <= 3:
        return best(Px)

    print(f'Px: {Px}')
    print(f'Py: {Py}')

    n = len(Px)
    k = n // 2
    Lx, Rx = Px[:k], Px[k:]
    Ly, Ry = [], []
    for x, y in Py:
        if x < Rx[0][0]:
            Ly.append((x, y))
        else:
            Ry.append((x, y))

    print(f'Lx: {Lx}')
    print(f'Ly: {Ly}')

    print(f'Rx: {Rx}')
    print(f'Ry: {Ry}')

    # # best left pair
    # best_left = go(Lx, Ly)

    # # best right pair
    # best_right = go(Rx, Ry)

    # # best split pair
    # best_split = split(Px, Py)

    # return best([best_left, best_right, best_split])  # return best of the best
    return None

Px = sorted(P, key=lambda it: it[0])
Py = sorted(P, key=lambda it: it[1])

best_pair = go(Px, Py)
print(f'best_pair: {best_pair}')

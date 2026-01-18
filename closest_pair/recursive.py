# initial example
# P = [(1, 8), (2, 5), (4, 7), (6, 3)]
# expected_best_pair = (2, 5), (4, 7)

# simple, obvious nearest neighbors
# P = [(0, 0), (3, 4), (7, 1), (10, 6)]
# expected_best_pair = ((0, 0), (3, 4))

# closest pair not adjacent in sorted-by-x
# P = [(1, 1), (4, 10), (7, 4), (9, 8)]
# expected_best_pair = ((7, 4), (9, 8))

# tight cluster inside larger spread
# P = [(2, 9), (5, 3), (6, 5), (11, 1)]
# expected_best_pair = ((5, 3), (6, 5))

# stress: diagonal-ish
P = [(1, 10), (4, 7), (8, 3), (13, 6)]
# expected_best_pair = ((1, 10), (4, 7))

N = len(P)
INF = 1234567890  # arbitary choice for infinity

def dist(first, second):
    x1, y1 = first
    x2, y2 = second
    return (x1 - x2) ** 2 \
         + (y1 - y2) ** 2

def split(Px, Py, d):
    # median x-coordinate
    median = Px[-1][0]

    # identify points near left/right boundary
    Sy = [(x, y) for x, y in Py if median - d <= x <= median + d]

    # return the best split pair (if it exists)
    best_dist = INF
    best_pair = None
    for i in range(len(Sy) - 1):
        for j in range(i + 1, min(i + 7, len(Sy))):
            cand = dist(Sy[i], Sy[j])
            if best_dist > cand:
                best_dist = cand
                best_pair = (Sy[i], Sy[j])
    return best_pair

def best(P):
    best_dist = INF
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

    # best left pair
    best_left = go(Lx, Ly)

    # best right pair
    best_right = go(Rx, Ry)

    # best distance to beat with a split pair
    d = min(dist(*best_left), dist(*best_right))

    # best split pair
    best_split = split(Px, Py, d)

    # return best of the best
    order = [
        [dist(*best_left), best_left],
        [dist(*best_right), best_right]
    ]
    if best_split:
        order.append([dist(*best_split), best_split])
    order.sort(key=lambda it: it[0])
    return order[0][1]

Px = sorted(P, key=lambda it: it[0])
Py = sorted(P, key=lambda it: it[1])

best_pair = go(Px, Py)
print(f'best_pair: {best_pair}')

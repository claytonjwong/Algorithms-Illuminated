INF = 1234567890  # arbitary choice for infinity

def dist(a, b):
    x1, y1 = a
    x2, y2 = b
    return (x1 - x2) ** 2 \
         + (y1 - y2) ** 2

def split(Px, Py, d):
    # median x-coordinate
    n = len(Px)
    k = n // 2
    median = Px[k][0]

    # identify points near left/right boundary
    Sy = [(x, y) for x, y in Py if median - d <= x <= median + d]

    # return the best split pair (if it exists)
    best_dist = INF
    best_pair = None
    for i in range(len(Sy) - 1):
        for j in range(i + 1, min(i + 1 + 7, len(Sy))):
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
            cand = dist(a, b) if a != b else INF
            if best_dist >= cand:
                best_dist = cand
                best_pair = (a, b)
    return best_pair

def go(Px, Py):
    if len(Px) <= 3:  # Base case
        return best(Px)

    n = len(Px)
    k = n // 2
    Lx, Rx = Px[:k], Px[k:]
    Ly, Ry = [], []
    for x, y in Py:
        if x <= Lx[-1][0]:
            Ly.append((x, y))
        else:
            Ry.append((x, y))

    best_left = go(Lx, Ly)   # best left pair
    best_right = go(Rx, Ry)  # best right pair

    d = min(dist(*best_left), dist(*best_right))  # best distance to beat with split pair
    best_split = split(Px, Py, d)                 # best split pair

    # return best of the best
    order = sorted([
        [dist(*best_left), best_left],
        [dist(*best_right), best_right],
        [dist(*best_split) if best_split else INF, best_split]], key=lambda it: it[0])
    return order[0][1]

def run(points, expected_best_pair):
    Px = sorted(points, key=lambda it: it[0])
    Py = sorted(points, key=lambda it: it[1])
    best_pair = go(Px, Py)

    print(f'points: {points}')
    print(f'actual: {sorted(best_pair)}')
    print(f'expect: {sorted(expected_best_pair)}')
    print()
    assert(sorted(best_pair) == sorted(expected_best_pair))

# initial example
run(points=[(1, 8), (2, 5), (4, 7), (6, 3)], expected_best_pair=((2, 5), (4, 7)))

# simple, obvious nearest neighbors
run(points=[(0, 0), (3, 4), (7, 1), (10, 6)], expected_best_pair=((0, 0), (3, 4)))

# closest pair not adjacent in sorted-by-x
run(points=[(1, 1), (4, 10), (7, 4), (9, 8)], expected_best_pair=((7, 4), (9, 8)))

# tight cluster inside larger spread
run(points=[(2, 9), (5, 3), (6, 5), (11, 1)], expected_best_pair=((5, 3), (6, 5)))

# stress: diagonal-ish
run(points=[(1, 10), (4, 7), (8, 3), (13, 6)], expected_best_pair=((1, 10), (4, 7)))

# larger input: 10 points
run(points=[(1, 17), (3, 4), (6, 14), (8, 9), (11, 2), (14, 7), (17, 12), (19, 5), (22, 15), (25, 1)], expected_best_pair=((6, 14), (8, 9)))

# larger input: 12 points more spread out
run(points=[(2, 21), (4, 6), (7, 15), (9, 2), (12, 18), (14, 9), (16, 4), (19, 13), (21, 7), (24, 16), (27, 1), (30, 11)], expected_best_pair= ((14, 9), (16, 4)))

# same x-coordinate (vertical stack)
run(points=[(5, 1), (5, 4), (5, 9), (8, 20), (12, 30)], expected_best_pair=((5, 1), (5, 4)))

# same y-coordinate (horizontal line)
run(points=[(1, 7), (4, 7), (9, 7), (20, 2), (25, 11)], expected_best_pair=((1, 7), (4, 7)))

# redundant x-coordinate to test split pairs
run(points=[(10, 1), (10, 4), (10, 8), (10, 13), (11, 7), (20, 50)], expected_best_pair=((10, 8), (11, 7)))

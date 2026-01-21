INF = 1234567890  # arbitary choice for infinity

def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return (x1 - x2) ** 2 \
         + (y1 - y2) ** 2

def split(Px, Py, d):
    # median x-coordinate
    median = Px[len(Px) // 2][0]

    # identify points near left/right boundary
    Sy = [(x, y) for x, y in Py if median - d <= x <= median + d]

    # return the best split pair (if it exists)
    best_dist, best_pairs = INF, set()
    for i in range(len(Sy) - 1):
        for j in range(i + 1, min(i + 1 + 7, len(Sy))):
            cand = distance(Sy[i], Sy[j])
            if best_dist > cand:
                best_dist = cand
                best_pairs = set()
            if best_dist == cand:
                best_pairs.add((Sy[i], Sy[j]))
    return best_dist, best_pairs

def best(P):
    best_dist, best_pairs = INF, set()
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            cand = distance(P[i], P[j]) if P[i] != P[j] else INF
            if best_dist > cand:
                best_dist = cand
                best_pairs = set()
            if best_dist == cand:
                best_pairs.add((P[i], P[j]))
    return best_dist, best_pairs

def go(Px, Py):
    if len(Px) <= 3:  # Base case
        return best(Px)

    Lx, Rx = Px[:len(Px) // 2], Px[len(Px) // 2:]
    Ly, Ry = [], []
    for x, y in Py:
        if x <= Lx[-1][0]:
            Ly.append((x, y))
        else:
            Ry.append((x, y))

    dist_left, best_left = go(Lx, Ly)
    dist_right, best_right = go(Rx, Ry)
    dist_split, best_split = split(Px, Py, min(dist_left, dist_right))

    cands = sorted([(dist_left, best_left), (dist_right, best_right), (dist_split, best_split)], key=lambda it: it[0])
    best_dist, best_pairs = cands[0][0], set()
    for dist, pairs in cands:
        if dist == best_dist:
            for a, b in pairs:
                best_pairs.add((a, b) if a < b else (b, a))
    return best_dist, best_pairs

def run(points, expected_best_pair):
    Px = sorted(points, key=lambda it: it[0])
    Py = sorted(points, key=lambda it: it[1])
    _, best_pair = go(Px, Py)
    print(f'points: {points}')
    print(f'actual: {sorted(best_pair)}')
    print(f'expect: {sorted(expected_best_pair)}')
    print()
    assert(sorted(best_pair) == sorted(expected_best_pair))

# initial example
run(points=[(1, 8), (2, 5), (4, 7), (6, 3)], expected_best_pair=set([((2, 5), (4, 7))]))

# simple, obvious nearest neighbors
run(points=[(0, 0), (3, 4), (7, 1), (10, 6)], expected_best_pair=set([((0, 0), (3, 4)), ((3, 4), (7, 1))]))

# closest pair not adjacent in sorted-by-x
run(points=[(1, 1), (4, 10), (7, 4), (9, 8)], expected_best_pair=set([((7, 4), (9, 8))]))

# tight cluster inside larger spread
run(points=[(2, 9), (5, 3), (6, 5), (11, 1)], expected_best_pair=set([((5, 3), (6, 5))]))

# stress: diagonal-ish
run(points=[(1, 10), (4, 7), (8, 3), (13, 6)], expected_best_pair=set([((1, 10), (4, 7))]))

# larger input: 10 points
run(points=[(1, 17), (3, 4), (6, 14), (8, 9), (11, 2), (14, 7), (17, 12), (19, 5), (22, 15), (25, 1)], expected_best_pair=set([((6, 14), (8, 9)), ((14, 7), (19, 5))]))

# larger input: 12 points more spread out
run(points=[(2, 21), (4, 6), (7, 15), (9, 2), (12, 18), (14, 9), (16, 4), (19, 13), (21, 7), (24, 16), (27, 1), (30, 11)], expected_best_pair=set([((14, 9), (16, 4))]))

# same x-coordinate (vertical stack)
run(points=[(5, 1), (5, 4), (5, 9), (8, 20), (12, 30)], expected_best_pair=set([((5, 1), (5, 4))]))

# same y-coordinate (horizontal line)
run(points=[(1, 7), (4, 7), (9, 7), (20, 2), (25, 11)], expected_best_pair=set([((1, 7), (4, 7))]))

# redundant x-coordinate to test split pairs
run(points=[(10, 1), (10, 4), (10, 8), (10, 13), (11, 7), (20, 50)], expected_best_pair=set([((10, 8), (11, 7))]))

# redundant x-coordinate to test split pairs
run(points=[(0, 0), (0, 1000), (0, 2000), (0, 3000), (0, 4000), (0, 5000), (0, 6000), (0, 7000), (5, 1), (5, 7002)], expected_best_pair=set([((0, 0), (5, 1))]))

# tie for best
run(points=[(0, 0), (0, 1), (1, 0)], expected_best_pair=set([((0, 0), (0, 1)), ((0, 0), (1, 0))]))

# ➜  closest_pair git:(main) ✗ python3 recursive.py
# points: [(1, 8), (2, 5), (4, 7), (6, 3)]
# actual: [((2, 5), (4, 7))]
# expect: [((2, 5), (4, 7))]

# points: [(0, 0), (3, 4), (7, 1), (10, 6)]
# actual: [((0, 0), (3, 4)), ((3, 4), (7, 1))]
# expect: [((0, 0), (3, 4)), ((3, 4), (7, 1))]

# points: [(1, 1), (4, 10), (7, 4), (9, 8)]
# actual: [((7, 4), (9, 8))]
# expect: [((7, 4), (9, 8))]

# points: [(2, 9), (5, 3), (6, 5), (11, 1)]
# actual: [((5, 3), (6, 5))]
# expect: [((5, 3), (6, 5))]

# points: [(1, 10), (4, 7), (8, 3), (13, 6)]
# actual: [((1, 10), (4, 7))]
# expect: [((1, 10), (4, 7))]

# points: [(1, 17), (3, 4), (6, 14), (8, 9), (11, 2), (14, 7), (17, 12), (19, 5), (22, 15), (25, 1)]
# actual: [((6, 14), (8, 9)), ((14, 7), (19, 5))]
# expect: [((6, 14), (8, 9)), ((14, 7), (19, 5))]

# points: [(2, 21), (4, 6), (7, 15), (9, 2), (12, 18), (14, 9), (16, 4), (19, 13), (21, 7), (24, 16), (27, 1), (30, 11)]
# actual: [((14, 9), (16, 4))]
# expect: [((14, 9), (16, 4))]

# points: [(5, 1), (5, 4), (5, 9), (8, 20), (12, 30)]
# actual: [((5, 1), (5, 4))]
# expect: [((5, 1), (5, 4))]

# points: [(1, 7), (4, 7), (9, 7), (20, 2), (25, 11)]
# actual: [((1, 7), (4, 7))]
# expect: [((1, 7), (4, 7))]

# points: [(10, 1), (10, 4), (10, 8), (10, 13), (11, 7), (20, 50)]
# actual: [((10, 8), (11, 7))]
# expect: [((10, 8), (11, 7))]

# points: [(0, 0), (0, 1000), (0, 2000), (0, 3000), (0, 4000), (0, 5000), (0, 6000), (0, 7000), (5, 1), (5, 7002)]
# actual: [((0, 0), (5, 1))]
# expect: [((0, 0), (5, 1))]

# points: [(0, 0), (0, 1), (1, 0)]
# actual: [((0, 0), (0, 1)), ((0, 0), (1, 0))]
# expect: [((0, 0), (0, 1)), ((0, 0), (1, 0))]

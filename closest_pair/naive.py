P = [(1, 8), (2, 5), (4, 7), (6, 3)]
N = len(P)
INF = 1234567890  # arbitary choice for infinity

def dist(i, j):
    x1, y1 = P[i]
    x2, y2 = P[j]
    return (x1 - x2) ** 2 \
         + (y1 - y2) ** 2

best_dist = 123456789
best_pair = None

D = [[INF] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        D[i][j] = dist(i, j)
        if i != j:  # candidates for best pair cannot be the same point
            if best_dist >= D[i][j]:
                best_dist = D[i][j]
                best_pair = (i, j)

i, j = best_pair
print(f'best pair: {P[i]}, {P[j]}')

# ➜  closest_pair git:(main) ✗ python3 ./naive.py
# best pair: (4, 7), (2, 5)

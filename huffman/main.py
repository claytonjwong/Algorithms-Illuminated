#
# Programming Problem 14.6: Huffman Codes
#
# In this problem the file format is:
# [number_of_symbols]
# [weight of symbol #1]
# [weight of symbol #2]
# ...
#

from heapq import heappush
from heapq import heappop

class Tree:
    def __init__(self, weight, left = None, right = None):
        self.weight = weight
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.weight < other.weight

def encode(A):
    T = []
    for weight in A:
        heappush(T, Tree(weight))
    while 1 < len(T):
        a, b = heappop(T), heappop(T)
        c = Tree(a.weight + b.weight, a, b)
        heappush(T, c)
    return T[0]

def run(filename):
    A = []
    with open(filename) as fin:
        N = int(fin.readline())
        while True:
            line = fin.readline()
            if not line:
                break
            weight = int(line.strip())
            A.append(weight)
    tree = encode(A)
    lo, hi = float('inf'), float('-inf')
    def go(root = tree, depth = 0):
        nonlocal lo, hi
        if not root:
            return
        isLeaf = lambda root: not root.left and not root.right
        if isLeaf(root):
            lo = min(lo, depth)
            hi = max(hi, depth)
        else:
            go(root.left, depth + 1)
            go(root.right, depth + 1)
    go()
    return [ lo, hi ]

for filename in [ 'problem14.6test1.txt', 'problem14.6test2.txt', 'problem14.6.txt' ]:
    lo, hi = run(filename)
    print(f'{filename}: {lo}, {hi}') # min, max encoding length in the corresponding optimal prefix-free tree

#    problem14.6test1.txt: 2, 5
#    problem14.6test2.txt: 3, 6
#    problem14.6.txt: 9, 19

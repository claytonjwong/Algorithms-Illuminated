#
# Programming Problem 14.6: Huffman Codes
#
# In this problem the file format is:
# [number_of_symbols]
# [weight of symbol #1]
# [weight of symbol #2]
# ...
#

class Tree:
    def __init__(self, weight, left = None, right = None):
        self.weight = weight
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.weight < other.weight

#
# priority queue
#

# from heapq import heappush
# from heapq import heappop
# def encode(A):
#     T = []
#     for weight in A:
#         heappush(T, Tree(weight))
#     while 1 < len(T):
#         a, b = heappop(T), heappop(T)
#         c = Tree(a.weight + b.weight, a, b)
#         heappush(T, c)
#     return heappop(T)

#
# Problem 14.5: Give an implementation of Huffman's greedy algorithm that uses a single invocation
# of a sorting subroutine, followed by a linear amount of additional work.
#
from collections import deque
def encode(A):
    A.sort()
    first, second = deque([Tree(weight) for weight in A]), deque()
    while 1 < len(first) + len(second):
        next = []
        while len(next) < 2:
            if len(first) and len(second):
                next.append(first.popleft() if first[0].weight < second[0].weight else second.popleft())
            elif len(first): next.append(first.popleft())
            elif len(second): next.append(second.popleft())
        a, b = next
        c = Tree(a.weight + b.weight, a, b)
        second.append(c)
    return second.popleft()

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

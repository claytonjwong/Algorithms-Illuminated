from functools import cmp_to_key

class Job:
    def __init__(self, weight, length):
        self.weight = weight
        self.length = length

class Solution:
    def minSum(self, jobs):
        def diff(a, b):
            first = a.weight - a.length
            second = b.weight - b.length
            return b.weight - a.weight if first == second else second - first
        def ratio(a, b):
            first = a.weight / a.length
            second = b.weight / b.length
            return b.weight - a.weight if first == second else second - first
        return [ self._calcSum(jobs, diff), self._calcSum(jobs, ratio) ]
    def _calcSum(self, jobs, comp, time = 0, total = 0):
        jobs.sort(key = cmp_to_key(lambda a, b: comp(a, b)))
        for job in jobs:
            time += job.length
            total += job.weight * time
        return total

def run(filename):
    jobs = []
    with open(filename) as fin:
        line = fin.readline() # N
        while True:
            line = fin.readline().strip()
            if not line:
                break
            words = line.split()
            weight, length = [int(x) for x in words]
            jobs.append(Job(weight, length))
    diff, ratio = Solution().minSum(jobs)
    print(f'{diff}, {ratio}') # sub-optimal, optimal

run('problem13.4test1.txt') # 23, 22
run('problem13.4test2.txt') # 68615, 67247
run('problem13.4.txt')      # 69119377652, 67311454237

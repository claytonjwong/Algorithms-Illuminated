import java.io.File

data class Job(val weight: Long, val length: Long)

class Solution {
    fun minSum(jobs: Array<Job>): Pair<Long, Long> {
        class Diff: Comparator<Job> {
            override fun compare(a: Job?, b: Job?): Int {
                if (a == null || b == null)
                    return 0
                var first = a.weight - a.length
                var second = b.weight - b.length
                return if (first == second) b.weight.compareTo(a.weight) else second.compareTo(first) // sort by descending difference, break ties in favor of jobs with larger weights
            }
        }
        class Ratio: Comparator<Job> {
            override fun compare(a: Job?, b: Job?): Int {
                if (a == null || b == null)
                    return 0
                var first = a.weight.toDouble() / a.length
                var second = b.weight.toDouble() / b.length
                return if (first == second) b.weight.compareTo(a.weight) else second.compareTo(first) // sort by descending difference, break ties in favor of jobs with larger weights
            }
        }
        return Pair(calcSum(jobs, Diff()), calcSum(jobs, Ratio()))
    }
    private fun calcSum(jobs: Array<Job>, comp: Comparator<Job>): Long {
        jobs.sortWith(comp)
        var time: Long = 0
        var total: Long = 0
        jobs.forEach { job ->
            time += job.length
            total += job.weight * time
        }
        return total
    }
}

fun run(filename: String) {
    var jobs = mutableListOf<Job>()
    var first = true
    File(filename).forEachLine {
        if (!first) {
            var words = it.trim().split(" ").map{ it.toLong() }
            var (weight, length) = words
            jobs.add(Job(weight, length))
        } else {
            first = false
        }
    }
    var (diff, ratio) = Solution().minSum(jobs.toTypedArray())
    println("$diff, $ratio") // sub-optimal, optimal
}

fun main() {
    run("problem13.4test1.txt") // 23, 22
    run("problem13.4test2.txt") // 68615, 67247
    run("problem13.4.txt")      // 69119377652, 67311454237
}

import java.io.File

class Solution() {
    private var best = (1e9 + 7).toInt()
    private var best_path = listOf<Int>()
    private var start = 0
    private var M = 0
    private var N = 0
    private var adj = mutableMapOf<Int, MutableSet<Int>>()
    private var cost = mutableMapOf<String, Int>()
    private var key = { u: Int, v: Int -> "$u,$v" }
    private fun init(input_file: String) {
        best = (1e9 + 7).toInt()
        best_path = mutableListOf<Int>()
        adj = mutableMapOf<Int, MutableSet<Int>>()
        cost = mutableMapOf<String, Int>()
        var i = 0
        File(input_file).forEachLine { line ->
            var A = line.trim().split(" ").map{ it.toInt() }
            if (0 < i++) {
                var (u, v, w) = A
                if (!adj.contains(u)) adj[u] = mutableSetOf<Int>()
                if (!adj.contains(v)) adj[v] = mutableSetOf<Int>()
                adj[u]!!.add(v); cost[key(u, v)] = w
                adj[v]!!.add(u); cost[key(v, u)] = w
            } else {
                N = A[0]
                M = A[1]
            }
        }
    }
    fun run(input_file: String): Pair<Int, List<Int>> {
        init(input_file)
        start = 1
        go(start, mutableListOf<Int>(start), mutableSetOf<Int>(start))
        return Pair<Int, List<Int>>(best, best_path)
    }
    fun go(u: Int, path: MutableList<Int>, seen: MutableSet<Int>, t_: Int = 0) {
        if (seen.size == N) {
            var t = t_ + (cost[key(u, start)] ?: 0)
            if (adj[u]!!.contains(start) && t < best) {
                best = t; best_path = path.toList()
            }
            return
        }
        for (v in adj[u]!!) {
            if (seen.contains(v))
                continue
            path.add(v); seen.add(v)
            go(v, path, seen, t_ + cost[key(u, v)]!!)
            path.removeLast(); seen.remove(v)
        }
    }
}

fun main() {
    var s = Solution()
    for (input_file in listOf("quiz19.2.txt", "quiz20.7.txt")) {
        var (best, path) = s.run(input_file)
        println("$input_file  best: $best  path: ${path.joinToString()}")
    }
}
// quiz19.2.txt  best: 13  path: 1, 2, 4, 3
// quiz20.7.txt  best: 23  path: 1, 3, 2, 5, 4
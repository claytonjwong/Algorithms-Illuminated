import java.io.File
import java.util.PriorityQueue

var INF = (1e9 + 7).toInt()

interface BaseSolution {
    fun run(filename: String, queries: Array<Int>): String
}

class NaiveSolution : BaseSolution {
    fun dijkstra(E: List<Triple<Int, Int, Int>>): MutableMap<Int, Int> {
        var dist = mutableMapOf<Int, Int>()
        var seen = mutableSetOf<Int>()
        var start = 1
        dist[start] = 0; seen.add(start)
        var found: Boolean;
        do {
            found = false
            var best_v = INF
            var best_w = INF
            for ((u, v, w) in E) {
                if (!seen.contains(u) || seen.contains(v))
                    continue
                found = true
                if (best_w > dist[u]!! + w) {
                    best_v = v
                    best_w = dist[u]!! + w
                }
            }
            var v = best_v
            var w = best_w
            dist[v] = w; seen.add(v)
        } while (found)
        return dist
    }
    override fun run(filename: String, queries: Array<Int>): String {
        var E = mutableListOf<Triple<Int, Int, Int>>()
        File(filename).forEachLine {
            var words = it.trim().split("\t")
            var u = words[0].toInt()
            for (i in 1 until words.size) {
                var (v, w) = words[i].split(",").map{ it.toInt() }
                E.add(Triple(u, v, w))
            }
        }
        var dist = dijkstra(E.toList())
        return queries.map{ dist[it] }.joinToString(" ")
    }
}

class HeapSolution : BaseSolution {
    fun dijkstra(adj: MutableMap<Int, MutableList<Pair<Int, Int>>>): MutableMap<Int, Int> {
        var dist = mutableMapOf<Int, Int>()
        var seen = mutableSetOf<Int>()
        var start = 1
        dist[start] = 0
        var q = PriorityQueue<Pair<Int, Int>>(Comparator{ a: Pair<Int, Int>, b: Pair<Int, Int> -> a.first.compareTo(b.first) })
        q.add(Pair(0, start))
        while (0 < q.size) {
            var (cost, u) = q.poll()
            if (seen.contains(u))
                continue
            dist[u] = cost; seen.add(u)
            for ((w, v) in adj[u]!!) {
                if (seen.contains(v))
                    continue
                q.add(Pair(cost + w, v))
            }
        }
        return dist
    }
    override fun run(filename: String, queries: Array<Int>): String {
        var adj = mutableMapOf<Int, MutableList<Pair<Int, Int>>>()
        File(filename).forEachLine {
            var words = it.trim().split("\t")
            var u = words[0].toInt()
            if (!adj.contains(u))
                adj[u] = mutableListOf()
            for (i in 1 until words.size) {
                var (v, w) = words[i].split(",").map{ it.toInt() }
                adj[u]!!.add(Pair(w, v))
            }
        }
        var dist = dijkstra(adj)
        return queries.map{ dist[it] }.joinToString(" ")
    }
}

fun run(solution: BaseSolution) {
    println(solution.run("problem9.8test.txt", arrayOf(1, 2, 3, 4, 5, 6, 7, 8)))
    println(solution.run("problem9.8.txt", arrayOf(7, 37, 59, 82, 99, 115, 133, 165, 188, 197)))
}

fun main() {
    run(NaiveSolution())
    //    0 1 2 3 4 4 3 2
    //    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068
    run(HeapSolution())
    //    0 1 2 3 4 4 3 2
    //    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068
}

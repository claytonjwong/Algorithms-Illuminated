import java.io.File
import java.util.PriorityQueue
import java.util.Random

fun prim(N: Int, adj: MutableMap<Int, MutableList<Pair<Int, Int>>>): Int {
    var total: Int = 0
    var start = Random().nextInt(N) + 1
    var q = PriorityQueue<Pair<Int, Int>>(Comparator{ a: Pair<Int, Int>, b: Pair<Int, Int> -> a.first.compareTo(b.first) })
    var seen = mutableSetOf<Int>(start)
    for ((w, v) in adj[start]!!)
        q.add(Pair(w, v))
    while (0 < q.size) {
        var (cost, u) = q.poll()
        if (seen.contains(u))
            continue
        total += cost; seen.add(u)
        for ((w, v) in adj[u]!!)
            if (!seen.contains(v))
                q.add(Pair(w, v))
    }
    return total
}

fun run(filename: String) {
    var N: Int = 0
    var adj = mutableMapOf<Int, MutableList<Pair<Int, Int>>>()
    var first = true
    File(filename).forEachLine { line ->
        if (!first) {
            var (u, v, w) = line.split(" ").map{ it.toInt() }
            if (!adj.contains(u)) adj[u] = mutableListOf<Pair<Int, Int>>()
            if (!adj.contains(v)) adj[v] = mutableListOf<Pair<Int, Int>>()
            adj[u]!!.add(Pair(w, v))
            adj[v]!!.add(Pair(w, u))
        } else {
            var (numVertex, _) = line.split(" ").map{ it.toInt() }
            N = numVertex
            first = false
        }
    }
    var cost = prim(N, adj)
    println("$filename: $cost")
}

fun main() {
    run("problem15.9test.txt") // problem15.9test.txt: 14
    run("problem15.9.txt")     // problem15.9.txt: -3612829
}

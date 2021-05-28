import java.io.File
import java.util.LinkedList
import java.util.Queue

// bellman-ford: N - 1 edge relaxations (u -> v of cost w) [ie. attempting to relax M edges N - 1 times] given N vertices
fun bell(E: Array<Triple<Int, Int, Int>>, N: Int, start: Int = 1, INF: Int = (1e6).toInt()): IntArray {
    var dist = IntArray(N) { INF }
    dist[start] = 0
    var K = N - 1
    while (0 < K--)
        E.forEach{ (u, v, w) -> dist[v] = Math.min(dist[v], dist[u] + w)}
    return dist
}

// shortest-paths faster algorithm: only attempt to relax candidate edges (note: adjacency list needed)
fun spfa(E: Array<Triple<Int, Int, Int>>, N: Int, start: Int = 1, INF: Int = (1e6).toInt()): IntArray {
    var dist = IntArray(N) { INF }
    dist[start] = 0
    var adj = Array<MutableList<Pair<Int, Int>>>(N) { mutableListOf<Pair<Int, Int>>() }
    for ((u, v, w) in E)
        adj[u].add(Pair(v, w))
    var q: Queue<Int> = LinkedList<Int>(listOf(start))
    while (0 < q.size) {
        var u = q.poll()
        for ((v, w) in adj[u]) {
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w; q.add(v)
            }
        }
    }
    return dist
}

fun run(filename: String): IntArray {
    var N = 0
    var E = mutableListOf<Triple<Int, Int, Int>>()
    File(filename).forEachLine {
        var A = ArrayDeque(it.trim().split("\t"))
        var u = A.removeFirst().toInt()
        for ((v, w) in A.map{ it.split(",").map{ it.toInt() } })
            E.add(Triple(u, v, w))
        ++N;
    }
    var A = E.toTypedArray()
    var a = bell(A, N + 1)  // +1 for 1-based indexing
    var b = spfa(A, N + 1)
    assert(a == b)          // 💩 sanity check: single source shortest paths are the same
    return b
}

fun main() {
    var dist = run("test.txt")
    println(listOf(7, 37, 59, 82, 99, 115, 133, 165, 188, 197).map{ dist[it] }.joinToString(","))  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068
}

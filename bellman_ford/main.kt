import java.io.File

fun bellman_ford(E: Array<Triple<Int, Int, Int>>, N: Int, start: Int = 1, INF: Int = (1e6).toInt()): IntArray {
    var dist = IntArray(N) { INF }
    dist[start] = 0
    var K = N - 1
    while (0 < K--)
        E.forEach{ (u, v, w) -> dist[v] = Math.min(dist[v], dist[u] + w)}
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
    return bellman_ford(E.toTypedArray(), N + 1)  // +1 for 1-based indexing
}

fun main() {
    var dist = run("test.txt")
    println(listOf(7, 37, 59, 82, 99, 115, 133, 165, 188, 197).map{ dist[it] }.joinToString(","))  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068
}

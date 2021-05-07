import java.io.File

var INF = (1e9 + 7).toInt()

fun top_down(A: List<Pair<Int, Int>>, K: Int): Int {
    var N = A.size
    var m = mutableMapOf<String, Int>()
    fun go(i: Int = 0, k: Int = K): Int {
        if (i == N)                                                                 // 🛑 empty set
            return 0
        var key = "$i,$k"
        if (m.contains(key))                                                        // 🤔 memo
            return m[key]!!
        var (value, weight) = A[i]
        var include = if (0 <= k - weight) go(i + 1, k - weight) + value else -INF  // ✅ include A[i]
        var exclude = go(i + 1, k)                                                  // 🚫 exclude A[i]
        m[key] = Math.max(include, exclude)                                         // 🎯 best
        return m[key]!!
    }
    return go()
}

fun bottom_up(A: List<Pair<Int, Int>>, K: Int): Int {
    var N = A.size
    var dp = Array(N + 1){ Array(K + 1){ -INF } }                                       // 🤔 memo
    for (k in 0..K)                                                                     // 🛑 empty set
        dp[0][k] = 0
    for (i in 1..N) {
        for (k in 0..K) {
            var (value, weight) = A[i - 1]
            var include = if (0 <= k - weight) dp[i - 1][k - weight] + value else -INF  // ✅ include A[i]
            var exclude = dp[i - 1][k]                                                  // 🚫 exclude A[i]
            dp[i][k] = Math.max(include, exclude)                                       // 🎯 best
        }
    }
    return dp[N][K]
}

fun bottom_up_memopt(A: List<Pair<Int, Int>>, K: Int): Int {
    var N = A.size
    var pre = Array(K + 1) { 0 }                                                  // 🤔 memo + 🛑 empty set
    for (i in 1..N) {
        var cur = Array(K + 1) { -INF }
        for (k in 0..K) {
            var (value, weight) = A[i - 1]
            var include = if (0 <= k - weight) pre[k - weight] + value else -INF  // ✅ include A[i]
            var exclude = pre[k]                                                  // 🚫 exclude A[i]
            cur[k] = Math.max(include, exclude)                                   // 🎯 best
        }
        pre = cur.also { cur = pre }
    }
    return pre[K]
}

fun run(filename: String) {
    var A = mutableListOf<Pair<Int, Int>>()
    var K = 0
    var N = 0
    var first = true
    File(filename).forEachLine { line ->
        if (!first) {
            var (value, weight) = line.trim().split(" ").map{ it -> it.toInt() }
            A.add(Pair(value, weight))
        } else {
            var (a, b) = line.trim().split(" ").map{ it -> it.toInt() }
            K = a
            N = b
            first = false
        }
    }
    var a = top_down(A, K)
    var b = bottom_up(A, K)
    var c = bottom_up_memopt(A, K)
    assert(a == b && b == c) // 💩 sanity check
    println("$filename: $a")
}

fun main() {
    run("problem16.7test.txt")  // problem16.7test.txt: 2493893
}

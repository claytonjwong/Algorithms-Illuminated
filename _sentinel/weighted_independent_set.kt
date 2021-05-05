/*
 * In this problem, each file describes the weights of vertices in a path graph and has the format:
 * [number_of_vertices_in_path_graph]
 * [weight of first vertex]
 * [weight of second vertex]
 * ...
 * Test case: (contributed by Logan Travis) What is the value of a maximum-weight independent set of the 10-vertex path graph described in this file, and which vertices belong to the MWIS? (Answer: 2617, and the vertices 2, 4, 7, and 10).
 * Challenge data set: Repeat the previous problem for the 1000-vertex path graph described in this file.
 */

import java.io.File

fun topDown(A: MutableList<Long>): Long {
    var N = A.size
    var m = mutableMapOf<Int, Long>()
    fun go(i: Int = N - 1): Long {
        if (m.contains(i))                    // 🤔 memo
            return m[i]!!
        if (i < 0) {                          // 🛑 empty set
            m[i] = 0
            return 0
        }
        if (i == 0) {                         // 🛑 single set
            m[i] = A[0]
            return A[0]
        }
        var include = go(i - 2) + A[i]        // ✅ include A[i]
        var exclude = go(i - 1)               // 🚫 exclude A[i]
        m[i] = Math.max(include, exclude)     // 🎯 best
        return m[i]!!
    }
    return go()
}

fun bottomUp(A: MutableList<Long>): Long {
    var N = A.size
    var dp = LongArray(N + 1)                 // 🤔 memo
    dp[0] = 0                                 // 🛑 empty set
    dp[1] = A[0]                              // 🛑 single set
    for (i in 2..N) {
        var include = dp[i - 2] + A[i - 1]    // ✅ include A[i] (use A[i - 1] since dp[i] is offset by 1 for explicit 🛑 empty set at index 0, ie. index -1 doesn't exist)
        var exclude = dp[i - 1]               // 🚫 exclude A[i]
        dp[i] = Math.max(include, exclude)    // 🎯 best
    }
    return dp[N]
}

fun run(filename: String) {
    var A = mutableListOf<Long>()
    var first = true
    File(filename).forEachLine { line ->
        if (!first) {
            A.add(line.toLong())
        } else {
            first = false
        }
    }
    var a = topDown(A)
    var b = bottomUp(A)
    assert(a == b) // 💩 sanity check
    println("$filename: $a")
}

fun main() {
    run("problem16.6test.txt")  // problem16.6test.txt: 2617
    run("problem16.6.txt")      // problem16.6.txt: 2955353732
}

/*
 * Programming Problem 18.8: All-Pairs Shortest Paths
 *
 * In this problem, each file describes a directed graph. The first line of the file indicates the number
 * of vertices and edges, respectively. Each subsequent line describes an edge (the first two numbers are its tail
 * and head, respectively) and its length (the third number). NOTE: edge lengths might be negative, and the graphs
 * may or may not be negative cycles.
 *
 * Test cases: (contributed by Matt Davis) What is the shortest shortest path in the graphs described in this file
 * and in this file? (I.e., the minimum, over choices of an origin s and a destination t, of a shortest s-t path in the graph.)
 * (If the graph has a negative cycle, your algorithm should detect that fact.) (Answer: -2 and "contains a negative cycle," respectively.)
 *
 * Challenge data set: Repeat the previous problem for the graphs described in the following files: graph #1, graph #2, graph #3, and graph #4.
 */

import java.io.File

var key = { i: Int, j: Int -> "$i,$j" }
var INF = (1e9 + 7).toInt()

fun floyd_warshall(E: MutableMap<String, Int>, N: Int): Array<IntArray> {
    var dp = Array(N + 1) { Array(N + 1) { IntArray(N + 1) { INF } } }
    for (i in 0..N)
        for (j in 0..N)
            if (i == j)
                dp[0][i][j] = 0
            else
            if (E.contains(key(i, j)))
                dp[0][i][j] = E[key(i, j)]!!
    for (k in 1..N)
        for (i in 1..N)
            for (j in 1..N)
                dp[k][i][j] = Math.min(dp[k - 1][i][j], dp[k - 1][i][k] + dp[k - 1][k][j])
    return dp[N]
}

fun floyd_warshall_memopt(E: MutableMap<String, Int>, N: Int): Array<IntArray> {
    var pre = Array(N + 1) { IntArray(N + 1) { INF } }
    for (i in 0..N)
        for (j in 0..N)
            if (i == j)
                pre[i][j] = 0
            else
            if (E.contains(key(i, j)))
                pre[i][j] = E[key(i, j)]!!
    for (k in 1..N) {
        var cur = Array(N + 1) { IntArray(N + 1) { INF } }
        for (i in 1..N)
            for (j in 1..N)
                cur[i][j] = Math.min(pre[i][j], pre[i][k] + pre[k][j])
        pre = cur.also{ cur = pre }
    }
    return pre
}

fun run(filename: String) {
    var N = 0
    var E = mutableMapOf<String, Int>()
    var first = true
    File(filename).forEachLine {
        if (!first) {
            var (u, v, w) = it.trim().split(" ").map{ it.toInt() }
            E[key(u, v)] = w
        } else {
            N = it.trim().split(" ").map{ it.toInt() }[0]
            first = false
        }
    }
    var a = floyd_warshall_memopt(E, N)
    // var b = floyd_warshall(E, N)
    // for (i in 1..N)
    //     for (j in 1..N)
    //         assert(a[i][j] == b[i][j])  // 💩 sanity check
    var cycle = false
    for (i in 1..N)
        if (a[i][i] < 0)
            cycle = true
    if (cycle) {
        println("$filename: contains a negative cycle")
        return
    }
    var best = INF
    for (i in 1..N)
        for (j in 1..N)
            best = Math.min(best, a[i][j])
    println("$filename: $best")
}

fun main() {
    run("problem18.8test1.txt");  // problem18.8test1.txt: -2
    run("problem18.8test2.txt");  // problem18.8test2.txt: contains a negative cycle
    run("problem18.8file1.txt");  // problem18.8file1.txt: contains a negative cycle
    run("problem18.8file2.txt");  // problem18.8file2.txt: contains a negative cycle
    run("problem18.8file3.txt");  // problem18.8file3.txt: -19
    // run("problem18.8file4.txt");
}
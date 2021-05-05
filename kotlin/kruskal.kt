import java.io.File

fun kruskal(E: MutableList<Triple<Int, Int, Int>>): Int {
    var total: Int = 0
    var M = E.size
    var P = IntArray(M) { it } // 🙂 parent representatives of 1..M disjoint sets
    fun find(x: Int): Int {
        P[x] = if (P[x] == x) x else find(P[x])
        return P[x]
    }
    fun union(a: Int, b: Int): Boolean {
        var x = find(a)
        var y = find(b)
        if (x == y)
            return false
        P[x] = y // 🎲 arbitrary choice
        return true
    }
    E.sortWith(Comparator{ a, b -> a.third.compareTo(b.third) }) // sort edges by nondecreasing weight
    for ((u, v, w) in E)
        if (union(u, v))
            total += w
    return total
}

fun run(filename: String) {
    var E = mutableListOf<Triple<Int, Int, Int>>()
    var first = true
    File(filename).forEachLine { line ->
        if (!first) {
            var (u, v, w) = line.trim().split(" ").map{ it.toInt() }
            E.add(Triple(u, v, w))
        } else {
            first = false // ignore first line with N vertices and M edges
        }
    }
    var cost = kruskal(E)
    println("$filename: $cost")
}

fun main() {
    run("problem15.9test.txt") // problem15.9test.txt: 14
    run("problem15.9.txt")     // problem15.9.txt: -3612829
}

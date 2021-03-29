import java.io.File
import java.util.PriorityQueue

var INF = (1e9 + 7).toInt()

data class Tree(val weight: Int, val left: Tree? = null, val right: Tree? = null)

fun encode(A: List<Int>): Tree {
    var q = PriorityQueue<Tree>(Comparator{ a: Tree, b: Tree -> a.weight.compareTo(b.weight) })
    for (weight in A)
        q.add(Tree(weight))
    while (1 < q.size) {
        var a = q.poll()
        var b = q.poll()
        var c = Tree(a.weight + b.weight, a, b)
        q.add(c)
    }
    return q.poll()
}

fun run(filename: String): Pair<Int, Int> {
    var A = mutableListOf<Int>()
    var first = true
    File(filename).forEachLine {
        if (!first) {
            var weight = it.trim().toInt()
            A.add(weight)
        } else {
            first = false
        }
    }
    var tree = encode(A.toList())
    var lo = INF
    var hi = -INF
    fun go(root: Tree? = tree, depth: Int = 0) {
        if (root == null)
            return
        var isLeaf = { node: Tree? -> node?.left == null && node?.right == null }
        if (isLeaf(root)) {
            lo = Math.min(lo, depth)
            hi = Math.max(hi, depth)
        } else {
            go(root.left, depth + 1)
            go(root.right, depth + 1)
        }
    }
    go()
    return Pair(lo, hi)
}

fun main() {
    for (filename in listOf("problem14.6test1.txt", "problem14.6test2.txt", "problem14.6.txt")) {
        var (lo, hi) = run(filename)
        println("$filename: $lo, $hi") // min, max encoding length in the corresponding optimal prefix-free tree
    }
}

//    problem14.6test1.txt: 2, 5
//    problem14.6test2.txt: 3, 6
//    problem14.6.txt: 9, 19

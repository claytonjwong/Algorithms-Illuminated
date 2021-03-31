/*
 * Programming Problem 14.6: Huffman Codes
 *
 * In this problem the file format is:
 * [number_of_symbols]
 * [weight of symbol #1]
 * [weight of symbol #2]
 * ...
 */

import java.io.File
import java.util.PriorityQueue
import java.util.Queue
import java.util.LinkedList

var INF = (1e9 + 7).toInt()

data class Tree(val weight: Int, val left: Tree? = null, val right: Tree? = null)

/*
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
*/

/*
 * Problem 14.5: Give an implementation of Huffman's greedy algorithm that uses a single invocation
 * of a sorting subroutine, followed by a linear amount of additional work.
 */
fun encode(A: MutableList<Int>): Tree {
    A.sort()
    var first: Queue<Tree> = LinkedList<Tree>(A.map{ weight -> Tree(weight) }.toList())
    var second: Queue<Tree> = LinkedList<Tree>()
    var next = mutableListOf<Tree>()
    while (1 < first.size + second.size) {
        next.clear()
        do {
            if (0 < first.size && 0 < second.size) {
                if (first.peek().weight < second.peek().weight) next.add(first.poll()) else next.add(second.poll())
            }
            else if (0 < first.size) next.add(first.poll())
            else if (0 < second.size) next.add(second.poll())
        } while (next.size < 2)
        var (a, b) = next
        var c = Tree(a.weight + b.weight, a, b)
        second.add(c)
    }
    return second.poll()
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
    var tree = encode(A.toMutableList())
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

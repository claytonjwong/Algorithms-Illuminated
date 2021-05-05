import java.util.Stack
import java.io.File

class RecursiveSolution(var adj: MutableMap<Int, MutableList<Int>>, var rev: MutableMap<Int, MutableList<Int>>) {
    fun topo_sort(): MutableList<Int> {
        var list = mutableListOf<Int>()
        var seen = mutableSetOf<Int>()
        fun go(u: Int) {
            if (seen.contains(u))
                return
            seen.add(u)
            for (v in rev[u]!!)
                go(v)
            list.add(0, u)
        }
        for ((u, _) in rev)
            go(u)
        return list
    }
    fun kosaraju(): MutableList<List<Int>> {
        var lists = mutableListOf<List<Int>>()
        var seen = mutableSetOf<Int>()
        fun go(u: Int, list: MutableList<Int>) {
            if (seen.contains(u))
                return
            list.add(u); seen.add(u)
            for (v in adj[u]!!)
                go(v, list)
        }
        for (u in topo_sort()) {
            if (seen.contains(u))
                continue
            var list = mutableListOf<Int>()
            go(u, list)
            lists.add(list.toList())
        }
        return lists
    }
}

class IterativeSolution(var adj: MutableMap<Int, MutableList<Int>>, var rev: MutableMap<Int, MutableList<Int>>) {
    fun topo_sort(): MutableList<Int> {
        var list = mutableListOf<Int>()
        var seen = mutableSetOf<Int>()
        for ((u, _) in rev) {
            if (seen.contains(u))
                continue
            var stack = Stack<Int>()
            stack.push(u); seen.add(u)
            while (!stack.empty()) {
                var u = stack.last()
                for (v in rev[u]!!) {
                    if (!seen.contains(v)) {
                        stack.push(v); seen.add(v)
                    }
                }
                if (u == stack.last())
                    list.add(0, stack.pop())
            }
        }
        return list
    }
    fun kosaraju(): MutableList<List<Int>> {
        var lists = mutableListOf<List<Int>>()
        var seen = mutableSetOf<Int>()
        for (u in topo_sort()) {
            if (seen.contains(u))
                continue
            var list = mutableListOf<Int>()
            var stack = Stack<Int>()
            stack.push(u); seen.add(u)
            while (!stack.empty()) {
                var u = stack.last()
                for (v in adj[u]!!) {
                    if (!seen.contains(v)) {
                        stack.push(v); seen.add(v)
                    }
                }
                if (u == stack.last())
                    list.add(stack.pop())
            }
            lists.add(list.toList())
        }
        return lists
    }
}

fun run(filename: String) {
    var adj = mutableMapOf<Int, MutableList<Int>>()
    var rev = mutableMapOf<Int, MutableList<Int>>()
    File(filename).forEachLine {
        var (u, v) = it.trim().split(" ").map{ it.toInt() }
        if (!adj.contains(u)) adj[u] = mutableListOf(); if (!adj.contains(v)) adj[v] = mutableListOf()
        if (!rev.contains(u)) rev[u] = mutableListOf(); if (!rev.contains(v)) rev[v] = mutableListOf()
        adj[u]!!.add(v)
        rev[v]!!.add(u)
    }
    // var solution = RecursiveSolution(adj, rev)
    var solution = IterativeSolution(adj, rev)
    var A = solution.kosaraju()
    A.sortWith(Comparator{ a: List<Int>, b: List<Int> -> b.size - a.size })
    println(filename + ": " + A.map{ it.size }.slice(0 until Math.min(A.size, 5)).joinToString(" "))
}

fun main() {
    run("section8.6.5page64.txt");  // Graph from section 8.6.5 on page 64 of Algorithms Illuminated: Part 2
    run("problem8.10test1.txt");    // Test case #1: A 9-vertex 11-edge graph. Top 5 SCC sizes: 3,3,3,0,0
    run("problem8.10test2.txt");    // Test case #2: An 8-vertex 14-edge graph. Top 5 SCC sizes: 3,3,2,0,0
    run("problem8.10test3.txt");    // Test case #3: An 8-vertex 9-edge graph. Top 5 SCC sizes: 3,3,1,1,0
    run("problem8.10test4.txt");    // Test case #4: An 8-vertex 11-edge graph. Top 5 SCC sizes: 7,1,0,0,0
    run("problem8.10test5.txt");    // Test case #5: A 12-vertex 20-edge graph. Top 5 SCC sizes: 6,3,2,1,0
    run("problem8.10.txt");         // Challenge data set: Vertices are labeled as positive integers from 1 to 875714

//    section8.6.5page64.txt: 4 3 3 1
//    problem8.10test1.txt: 3 3 3
//    problem8.10test2.txt: 3 3 2
//    problem8.10test3.txt: 3 3 1 1
//    problem8.10test4.txt: 7 1
//    problem8.10test5.txt: 6 3 2 1
//    problem8.10.txt: 434821 968 459 313 211

}

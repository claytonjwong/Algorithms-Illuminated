import java.util.Queue
import java.util.LinkedList

class Solution(val adj: MutableMap<Char, List<Char>>) {

    var N: Int
    var color: Int
    var m = mutableMapOf<Char, Int>()
    var seen = mutableSetOf<Char>()

    init {
        N = adj.size
        color = 0
    }

    fun init(start: Int) {
        color = start
        m.clear()
        seen.clear()
    }

    fun topoSortBFS(): String {
        init(1)  // 👉 color forward from 1..N
        bfs()
        return toString()
    }

    fun topoSortDFS(): String {
        init(N)  // 👈 color reverse from N..1 (as the recursive stack unwinds)
        adj.forEach{ (u, _) -> dfs(u) }
        return toString()
    }

    fun bfs() {
        var degree = mutableMapOf<Char, Int>()
        adj.forEach{ (_, neighbors) ->
            neighbors.forEach{ v ->
                degree[v] = 1 + degree.getOrDefault(v, 0)
            }
        }
        var q: Queue<Char> = LinkedList(adj.map{ (u, _) -> u }.filter{ !degree.contains(it) })
        while (0 < q.size) {
            var u = q.poll()
            m[u] = color++
            adj[u]!!.forEach{ v ->
                degree[v] = degree[v]!!.minus(1)
                if (degree[v] == 0 && !seen.contains(v)) {
                    q.add(v); seen.add(v)
                }
            }
        }
    }

    fun dfs(u: Char) {
        if (seen.contains(u))
            return
        seen.add(u)
        adj[u]!!.forEach{ v ->
            dfs(v)
        }
        m[u] = color--
    }

    override fun toString(): String {
        var s = mutableListOf<String>()
        adj.forEach{ (u, _) ->
            s.add("$u: ${m[u]}")
        }
        return s.joinToString("\n")
    }
}

fun main() {
    var adj = mutableMapOf<Char, List<Char>>(
        's' to listOf<Char>('v', 'w'),
        'v' to listOf<Char>('t'),
        'w' to listOf<Char>('t'),
        't' to listOf<Char>()
    )
    var solution = Solution(adj)
    println("BFS:\n${solution.topoSortBFS()}\n\nDFS:\n${solution.topoSortDFS()}")

//    BFS:
//    s: 1
//    v: 2
//    w: 3
//    t: 4

//    DFS:
//    s: 1
//    v: 3
//    w: 2
//    t: 4

}

import java.io.File

typealias PivotFunc = (A: MutableList<Int>, L: Int, R: Int) -> (Int)
var pivotLeft: PivotFunc = { _: MutableList<Int>, L: Int, _: Int -> L }
var pivotRight: PivotFunc = { _: MutableList<Int>, _: Int, R: Int -> R }
fun _pivotMedian(A: MutableList<Int>, L: Int, R: Int): Int {
    var M = L + (R - L) / 2
    var cand = intArrayOf(A[L], A[M], A[R])
    cand.sort()
    var target = cand[1]
    if (target == A[L]) return L
    if (target == A[M]) return M
    if (target == A[R]) return R
    return -1
}
var pivotMedian: PivotFunc = { A: MutableList<Int>, L: Int, R: Int -> _pivotMedian(A, L, R) }

fun partition(A: MutableList<Int>, L: Int, R: Int, choosePivot: (A: MutableList<Int>, L: Int, R: Int) -> (Int)): Int {
    var i = L + 1
    var j = L + 1
    var k = choosePivot(A, L, R)
    A[k] = A[L].also { A[L] = A[k] }          // swap pivot A[k] with first element of subarray A[L]
    while (j <= R) {
        if (A[j] < A[L]) {                    // maintain loop invariant A[i] < pivot < A[j]
            A[i] = A[j].also { A[j] = A[i] }
            ++i
        }
        ++j
    }
    A[L] = A[i - 1].also { A[i - 1] = A[L] }  // swap pivot A[L] with last value less-than pivot A[i - 1]
    return i - 1
}

fun quicksort(A: MutableList<Int>, L: Int, R: Int, choosePivot: (A: MutableList<Int>, L: Int, R: Int) -> (Int)): Int {
    if (R <= L)
        return 0
    var k = partition(A, L, R, choosePivot)
    return (R - L) + quicksort(A, L, k - 1, choosePivot) + quicksort(A, k + 1, R, choosePivot)
}

fun run(filename: String, choosePivot: (A: MutableList<Int>, L: Int, R: Int) -> (Int)): Int {
    var A = mutableListOf<Int>()
    File(filename).forEachLine { A.add(it.toInt()) }
    return quicksort(A, 0, A.size - 1, choosePivot)
}

fun main() {
    var filename = "problem5.6.txt"
    println("  left: ${run(filename, pivotLeft)}")    //   left: 162085
    println(" right: ${run(filename, pivotRight)}")   //  right: 164123
    println("median: ${run(filename, pivotMedian)}")  // median: 138382
}

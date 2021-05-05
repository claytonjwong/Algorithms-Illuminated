import java.io.File
import kotlin.random.Random

fun partition(A: MutableList<Int>, L: Int, R: Int): Int {
    var i = L + 1
    var j = L + 1
    var k = Random.nextInt(L, R + 1)          // +1 for L..R inclusive
    A[L] = A[k].also { A[k] = A[L] }          // swap pivot A[k] with first element of subarray A[L]
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

fun rselect(A: MutableList<Int>, i: Int, L_: Int, R_: Int): Int {
    var L = L_
    var R = R_
    var k = partition(A, L, R)
    if (i == k)
        return A[k]  // 🎯 lucky guess
    if (i < k)
        R = k - 1
    else
        L = k + 1
    return rselect(A, i, L, R)
}

fun run(filename: String, i: Int): Int {
    var A = mutableListOf<Int>()
    File(filename).forEachLine { A.add(it.toInt()) }
    var N = A.size
    return rselect(A, i - 1, 0 , N - 1)  // -1 for 0-based indexing
}

fun main() {
    println("problem6.5test1.txt: " + run("problem6.5test1.txt", 5))   // problem6.5test1.txt: 5469
    println("problem6.5test2.txt: " + run("problem6.5test2.txt", 50))  // problem6.5test2.txt: 4715
}

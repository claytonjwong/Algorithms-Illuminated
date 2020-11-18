# Algorithms Illuminated

* http://www.algorithmsilluminated.org/

## Divide and Conquer

### Merge Sort

<details><summary>Videos</summary>
<br/>

* [MergeSort: Motivation and Example](https://www.youtube.com/watch?v=kiyRJ7GVWro&list=PLEGCF-WLh2RLHqXx6-GZr_w7LgqKDXxN_&index=4) (Section 1.4, part 1)
* [MergeSort: Pseudocode](https://www.youtube.com/watch?v=rBd5w0rQaFo&list=PLEGCF-WLh2RLHqXx6-GZr_w7LgqKDXxN_&index=5) (Section 1.4, part 2)
* [MergeSort: Analysis](https://www.youtube.com/watch?v=8ArtRiTkYEw&list=PLEGCF-WLh2RLHqXx6-GZr_w7LgqKDXxN_&index=6) (Section 1.5)

</details>

<details><summary>Implementations</summary>
<br/>

*Kotlin*
```kotlin
fun sort(A: IntArray): IntArray {
    fun merge(A: IntArray, B: IntArray): IntArray {
        var C = mutableListOf<Int>()
        var i = 0
        var j = 0
        while (i < A.size && j < B.size)
            if (A[i] < B[j])
                C.add(A[i++])
            else
                C.add(B[j++])
        A.slice(i..A.lastIndex).forEach { C.add(it) }
        B.slice(j..B.lastIndex).forEach { C.add(it) }
        return C.toIntArray()
    }
    fun go(A: IntArray): IntArray {
        var N = A.size
        if (N < 2)
            return A
        var half = Math.floor(N / 2.0).toInt()
        var first  = go(A.slice(0 until half).toIntArray())
        var second = go(A.slice(half until N).toIntArray())
        return merge(first, second)
    }
    return go(A)
}

fun main(args: Array<String>) {
    sort(intArrayOf(5,3,8,9,1,7,0,2,6,4)).forEach { print("$it ") }  // 0 1 2 3 4 5 6 7 8 9
    println()
}
```

*Javascript*
```javascript
let sort = A => {
    let go = A => {
        let N = A.length;
        if (N < 2)
            return A;
        let half = Math.floor(N / 2);
        let first  = go([...A.slice(0, half)]),
            second = go([...A.slice(half, N)]);
        return merge(first, second);
    };
    let merge = (A, B, C = []) => {
        let M = A.length,
            N = B.length;
        let i = 0,
            j = 0;
        while (i < M && j < N)
            C.push(A[i] < B[j] ? A[i++] : B[j++]);
        C.push(...A.slice(i, M));
        C.push(...B.slice(j, N));
        return C;
    };
    return go(A);
};

console.log(sort([5,3,8,9,1,7,0,2,6,4]));  // (10) [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

*Python3*
```python
from math import floor

def sort(A):
    def go(A):
        N = len(A)
        if N < 2:
            return A
        half = floor(N / 2)
        first =  go(A[:half])
        second = go(A[half:])
        return merge(first, second)
    def merge(A, B):
        C = []
        i = 0
        j = 0
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                C.append(A[i]); i += 1
            else:
                C.append(B[j]); j += 1
        C.extend(A[i:])
        C.extend(B[j:])
        return C
    return go(A)

print(sort([5,3,8,9,1,7,0,2,6,4]))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

*C++*
```cpp
#include <iostream>
#include <vector>

using namespace std;

class Solution {
public:
    using VI = vector<int>;
    VI mergesort(VI& A) {
        return go(move(A));
    }
private:
    VI go(VI&& A) {
        auto N = A.size();
        if( N < 2 )
            return A;
        auto half = A.begin() + (N / 2);
        auto first = go({ A.begin(), half }),
             second = go({ half, A.end() });
        return merge(first, second);
    }
    VI merge(VI& A, VI& B, VI C = {}) {
        auto i{ 0 },
             j{ 0 };
        while (i < A.size() && j < B.size())
            C.push_back(A[i] < B[j] ? A[i++] : B[j++]);
        C.insert(C.end(), A.begin() + i, A.end());
        C.insert(C.end(), B.begin() + j, B.end());
        return C;
    }
};

int main() {
    Solution::VI A{ 3,5,7,1,3,9,2,0 };
    auto ans = Solution().mergesort(A);
    copy(ans.begin(), ans.end(), ostream_iterator<int>(cout, " ")), cout << endl;  // 0 1 2 3 4 5 6 7 8 9
    return 0;
}
```

</details>


### Counting Inversions (via Merge Sort)

<details><summary>Videos</summary>
<br/>

* [The Divide-and-Conquer Paradigm](https://www.youtube.com/watch?v=7_AJfusC6UQ&list=PLEGCF-WLh2RLHqXx6-GZr_w7LgqKDXxN_&index=13) (Section 3.1; part 1 of Section 3.2)
* [Counting Inversions in O(n log n)](https://www.youtube.com/watch?v=I6ygiW8xN7Y&list=PLEGCF-WLh2RLHqXx6-GZr_w7LgqKDXxN_&index=14) Time (Section 3.2, part 2)

</details>

<details><summary>Implementations</summary>
<br/>

*Kotlin*
```kotlin
import java.io.File

fun sort(A: IntArray): Pair<IntArray, Long> {
    fun merge(A: IntArray, B: IntArray): Pair<IntArray, Long> {
        var C = mutableListOf<Int>()
        var inv: Long = 0
        var i = 0
        var j = 0
        while (i < A.size && j < B.size)
            if (A[i] < B[j]) {
                C.add(A[i++])
            } else {
                inv += A.size - i  // ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.add(B[j++])
            }
        A.slice(i..A.lastIndex).forEach { C.add(it) }
        B.slice(j..B.lastIndex).forEach { C.add(it) }
        return Pair(C.toIntArray(), inv)
    }
    fun go(A: IntArray): Pair<IntArray, Long> {
        var N = A.size
        if (N < 2)
            return Pair(A, 0)
        var half = Math.floor(N / 2.0).toInt()
        var (first,  inv1) = go(A.slice(0 until half).toIntArray())
        var (second, inv2) = go(A.slice(half until N).toIntArray())
        var (third,  inv3) = merge(first, second)
        return Pair(third, inv1 + inv2 + inv3)
    }
    return go(A)
}

fun run(filename: String): Long {
    var A = mutableListOf<Int>()
    File(filename).forEachLine { A.add(it.toInt()) }
    var (_, inv) = sort(A.toIntArray())
    return inv
}

fun main() {
    println("problem3.5test.txt: " + run("problem3.5test.txt"))  // problem3.5test.txt: 28
    println("problem3.5.txt: "     + run("problem3.5.txt"))      // problem3.5.txt: 2407905288
}
```

*Javascript*
```javascript
let sort = A => {
    let go = A => {
        let N = A.length;
        if (N < 2)
            return [A, 0];
        let half = Math.floor(N / 2);
        let [first,  inv1] = go([...A.slice(0, half)]),
            [second, inv2] = go([...A.slice(half, N)]),
            [third,  inv3] = merge(first, second);
        return [third, inv1 + inv2 + inv3];
    };
    let merge = (A, B, C = [], inv = 0) => {
        let M = A.length,
            N = B.length;
        let i = 0,
            j = 0;
        while (i < M && j < N)
            if (A[i] < B[j])
                C.push(A[i++]);
            else
                inv += M - i,      // ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.push(B[j++]);
        C.push(...A.slice(i, M));
        C.push(...B.slice(j, N));
        return [C, inv];
    };
    return go(A);
};

let run = filename => {
    let A = [];
    require('fs').readFileSync(filename, 'utf-8').split(/\r?\n/).forEach(line => A.push(Number(line)));
    let [_, inv] = sort(A);
    return inv;
}

console.log(`problem3.5test.txt: ${run('problem3.5test.txt')}`);  // problem3.5test.txt: 28
console.log(`problem3.5.txt: ${run('problem3.5.txt')}`);          // problem3.5.txt: 2407905288
```

*Python3*
```python
from math import floor

def sort(A):
    def go(A):
        N = len(A)
        if N < 2:
            return [A, 0]
        half = floor(N / 2)
        first,  inv1 = go(A[:half])
        second, inv2 = go(A[half:])
        third,  inv3 = merge(first, second)
        return [third, inv1 + inv2 + inv3]
    def merge(A, B, inv = 0):
        C = []
        i = 0
        j = 0
        while i < len(A) and j < len(B):
            if A[i] < B[j]:
                C.append(A[i]); i += 1
            else:
                inv += len(A) - i        # ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.append(B[j]); j += 1
        C.extend(A[i:])
        C.extend(B[j:])
        return [C, inv]
    return go(A)

def run(filename):
    A = []
    with open(filename) as fin:
        while True:
            line = fin.readline()
            if not line:
                break
            A.append(int(line))
    _, inv = sort(A)
    return inv

print(f"problem3.5test.txt: {run('problem3.5test.txt')}")  # problem3.5test.txt: 28
print(f"problem3.5.txt: {run('problem3.5.txt')}")          # problem3.5.txt: 2407905288
```

*C++*
```cpp
#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

class Solution {
public:
    using VL = vector<long>;
    using Pair = pair<VL, long>;
    using fun = function<Pair(VL&&)>;
    Pair merge(VL& A, VL& B, VL C = {}, long inv = 0) {
        auto i = 0,
             j = 0;
        while (i < A.size() && j < B.size()) {
            if (A[i] < B[j]) {
                C.push_back(A[i++]);
            } else {
                inv += A.size() - i; // ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.push_back(B[j++]);
            }
        }
        C.insert(C.end(), A.begin() + i, A.end());
        C.insert(C.end(), B.begin() + j, B.end());
        return { C, inv };
    }
    Pair inversions(VL& A) {
        fun go = [&](VL&& A) -> Pair {
            int N = A.size();
            if (N < 2)
                return { A, 0 };
            int half = N / 2;
            auto [first,  inv1] = go({ A.begin(), A.begin() + half });
            auto [second, inv2] = go({ A.begin() + half, A.end() });
            auto [third,  inv3] = merge(first, second);
            return { third, inv1 + inv2 + inv3 };
        };
        return go(move(A));
    }
};

long run(string filename) {
    Solution solution;
    Solution::VL A;
    fstream fin{ filename };
    for (string line; fin >> line; A.push_back(stol(line)));
    auto [_, inv] = solution.inversions(A);
    return inv;
}

int main() {
    cout << "problem3.5test.txt: " << run("problem3.5test.txt") << endl   // problem3.5test.txt: 28
         << "problem3.5.txt: "     << run("problem3.5.txt")     << endl;  // problem3.5.txt: 2407905288
    return 0;
}
```

</details>

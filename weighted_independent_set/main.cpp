/*
 * In this problem, each file describes the weights of vertices in a path graph and has the format:
 * [number_of_vertices_in_path_graph]
 * [weight of first vertex]
 * [weight of second vertex]
 * ...
 * Test case: (contributed by Logan Travis) What is the value of a maximum-weight independent set of the 10-vertex path graph described in this file, and which vertices belong to the MWIS? (Answer: 2617, and the vertices 2, 4, 7, and 10).
 * Challenge data set: Repeat the previous problem for the 1000-vertex path graph described in this file.
 */

#include <cassert>
#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>

using namespace std;
using LL = long long;
using List = vector<LL>;
using Map = unordered_map<int, LL>;

namespace TopDown {
    LL best(List& A, Map m = {}) {
        int N = A.size();
        using fun = function<LL(int)>;
        fun go = [&](auto i) {
            if (m[i]) return m[i];                // 🤔 memo
            if (i < 0) return m[i] = 0LL;         // 🛑 empty set
            if (!i) return m[i] = A[0];           // 🛑 single set
            auto include = go(i - 2) + A[i],      // ✅ include A[i]
                 exclude = go(i - 1);             // 🚫 exclude A[i]
            return m[i] = max(include, exclude);  // 🎯 best
        };
        return go(N - 1);
    }
}
namespace BottomUp {
    LL best(List& A, Map m = {}) {
        int N = A.size();
        List dp(N + 1);                           // 🤔 memo
        dp[0] = 0LL;                              // 🛑 empty set
        dp[1] = A[0];                             // 🛑 single set
        for (auto i{ 2 }; i <= N; ++i) {
            auto include = dp[i - 2] + A[i - 1],  // ✅ include A[i] (use A[i - 1] since dp[i] is offset by 1 for explicit 🛑 empty set at index 0, ie. index -1 doesn't exist)
                 exclude = dp[i - 1];             // 🚫 exclude A[i]
            dp[i] = max(include, exclude);        // 🎯 best
        }
        return dp[N];
    }
}

void run(const string& filename) {
    List A;
    fstream fin{ filename };
    int N; fin >> N;
    copy_n(istream_iterator<LL>(fin), N, back_inserter(A));
    auto a = TopDown::best(A),
         b = BottomUp::best(A);
    assert(a == b); // 💩 sanity check
    cout << filename << ": " << a << endl;
}

int main() {
    run("problem16.6test.txt");  // problem16.6test.txt: 2617
    run("problem16.6.txt");      // problem16.6.txt: 2955353732
    return 0;
}

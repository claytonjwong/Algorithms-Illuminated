#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>

using namespace std;
using Pair = pair<int, int>;  // value, weight
using Pairs = vector<Pair>;
using fun = function<int(int, int)>;
using Map = unordered_map<string, int>;

int INF = 1e9 + 7;

int top_down(Pairs& A, int K, Map m = {}) {
    auto N = A.size();
    fun go = [&](auto i, auto k) {
        if (i == N)                                                             // 🛑 empty set
            return 0;
        stringstream key; key << i << "," << k;
        if (m.find(key.str()) != m.end())                                       // 🤔 memo
            return m[key.str()];
        auto [value, weight] = A[i];
        auto include = 0 <= k - weight ? go(i + 1, k - weight) + value : -INF,  // ✅ include A[i]
             exclude = go(i + 1, k);                                            // 🚫 exclude A[i]
        return m[key.str()] = max(include, exclude);                            // 🎯 best
    };
    return go(0, K);
}

int bottom_up(Pairs& A, int K) {
    auto N = A.size();
    using VI = vector<int>;
    using VVI = vector<VI>;
    VVI dp(N + 1, VI(K + 1, -INF));                                                 // 🤔 memo
    for (auto k{ 0 }; k < K; dp[0][k++] = 0);                                      // 🛑 empty set
    for (auto i{ 1 }; i <= N; ++i) {
        for (auto k{ 0 }; k <= K; ++k) {
            auto [value, weight] = A[i - 1];
            auto include = 0 <= k - weight ? dp[i - 1][k - weight] +value : -INF,  // ✅ include A[i]
                 exclude = dp[i - 1][k];                                           // 🚫 exclude A[i]
            dp[i][k] = max(include, exclude);                                      // 🎯 best
        }
    }
    return dp[N][K];
}

void run(const string& filename) {
    Pairs A;
    fstream fin{ filename };
    int K, N;                // K capacity, N items
    fin >> K >> N;
    for (int value, weight; fin >> value >> weight; A.emplace_back(value, weight));
    auto a = top_down(A, K),
         b = bottom_up(A, K);
    assert(a == b);
    cout << filename << ": " << a << endl;
}

int main() {
    run("problem16.7test.txt");  // problem16.7test.txt: 2493893
    return 0;
}

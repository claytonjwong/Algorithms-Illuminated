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

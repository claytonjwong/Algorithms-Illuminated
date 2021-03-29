/*
 * Programming Problem 14.6: Huffman Codes
 *
 * In this problem the file format is:
 * [number_of_symbols]
 * [weight of symbol #1]
 * [weight of symbol #2]
 * ...
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <queue>

using namespace std;
using LL = long long;
using Weight = LL;
using Weights = vector<Weight>;

struct Tree;
using TreePtr = shared_ptr<Tree>;
struct Tree {
    Weight weight;
    TreePtr left, right;
    Tree(Weight weight, TreePtr left = nullptr, TreePtr right = nullptr) :
            weight{ weight }, left{ left }, right{ right } {}
};
using TreePtrs = vector<TreePtr>;

struct Comp {
    size_t operator()(const TreePtr& a, const TreePtr& b) const {
        return b->weight < a->weight;
    }
};
using Queue = priority_queue<TreePtr, TreePtrs, Comp>;

TreePtr encode(const Weights& A, Queue q = {}) {
    for (auto weight: A)
        q.emplace(make_shared<Tree>(weight));
    while (1 < q.size()) {
        auto a = q.top(); q.pop();
        auto b = q.top(); q.pop();
        q.emplace(make_shared<Tree>(a->weight + b->weight, a, b));
    }
    return q.top();
}

using MinMax = pair<LL, LL>;
constexpr auto Min = numeric_limits<LL>::min();
constexpr auto Max = numeric_limits<LL>::max();
MinMax run(const string& filename) {
    Weights A; // weight of each symbol
    fstream fin{ filename };
    LL N, weight;
    for (fin >> N; fin >> weight; A.push_back(weight));
    auto tree = encode(A);
    LL lo = Max,
       hi = Min;
    using fun = function<void(TreePtr, int)>;
    fun go = [&](auto root, LL depth) {
        if (!root)
            return;
        auto isLeaf = [](auto root) { return !root->left && !root->right; };
        if (isLeaf(root))
            lo = min(lo, depth),
            hi = max(hi, depth);
        else
            go(root->left, depth + 1),
            go(root->right, depth + 1);
    };
    go(tree, 0);
    return make_pair(lo, hi);
}

int main() {
    for (auto& filename: { "problem14.6test1.txt", "problem14.6test2.txt", "problem14.6.txt" }) {
        auto [lo, hi] = run(filename);
        cout << filename << ": " << lo << ", " << hi << endl; // min, max encoding length in the corresponding optimal prefix-free tree
    }
//    problem14.6test1.txt: 2, 5
//    problem14.6test2.txt: 3, 6
//    problem14.6.txt: 9, 19
    return 0;
}

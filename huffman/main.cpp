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
#include <list>

#define PRIORITY_QUEUE    // O(N * logN)
#ifndef PRIORITY_QUEUE
#define TWO_QUEUES        // O(N)
#endif

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

#ifdef PRIORITY_QUEUE
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
        auto c = make_shared<Tree>(a->weight + b->weight, a, b);
        q.emplace(c);
    }
    return q.top();
}
#else // TWO_QUEUES
/*
 * Problem 14.5: Give an implementation of Huffman's greedy algorithm that uses a single invocation
 * of a sorting subroutine, followed by a linear amount of additional work.
 */
using Queue = queue<TreePtr>;
TreePtr encode(Weights& A, Queue first = {}, Queue second = {}) {
    sort(A.begin(), A.end());
    for (auto weight: A)
        first.push(make_shared<Tree>(weight));
    TreePtrs next;
    auto takeFirst = [&]() { next.push_back(first.front()), first.pop(); };
    auto takeSecond = [&]() { next.push_back(second.front()), second.pop(); };
    while (1 < first.size() + second.size()) {
        next.clear();
        do {
            if (first.size() && second.size()) {
                if (first.front()->weight < second.front()->weight) takeFirst(); else takeSecond();
            }
            else if (first.size()) takeFirst();
            else if (second.size()) takeSecond();
        } while (next.size() < 2);
        auto [a, b] = tie(next[0], next[1]);
        auto c = make_shared<Tree>(a->weight + b->weight, a, b);
        second.emplace(c);
    }
    return second.front();
}
#endif

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

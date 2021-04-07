#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <numeric>

using namespace std;
using Edge = tuple<int, int, int>;
using Edges = vector<Edge>;
using Parents = vector<int>;
using fun = function<int(int)>;

int kruskal(Edges& E, int total = 0) {
    auto M = E.size();
    Parents P(M); iota(P.begin(), P.end(), 0); // 🙂 parent representatives of 1..M disjoint sets 
    fun find = [&](auto x) {
         return P[x] = P[x] == x ? x : find(P[x]);
    };
    auto join = [&](auto a, auto b) {
        a = find(a);
        b = find(b);
        if (a == b)
            return false;
        P[a] = b; // 🎲 arbitrary choice
        return true;
    };
    sort(E.begin(), E.end(), [](auto& first, auto& second) { // sort edges by nondecreasing weight
        auto [u1, v1, w1] = first;
        auto [u2, v2, w2] = second;
        return w1 < w2;
    });
    for (auto [u, v, w]: E)
        if (join(u, v))
            total += w;
    return total;
}

void run(const string& filename, Edges E = {}) {
    fstream fin{ filename };
    int N, M; fin >> N >> M; // ignore first line with N vertices and M edges
    int u, v, w;             // edge u -> v of weight w
    while (fin >> u >> v >> w)
        E.emplace_back(u, v, w);
    auto cost = kruskal(E);
    cout << filename << ": " << cost << endl;
}

int main() {
    run("problem15.9test.txt"); // problem15.9test.txt: 14
    run("problem15.9.txt");     // problem15.9.txt: -3612829
    return 0;
}

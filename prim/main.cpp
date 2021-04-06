#include <iostream>
#include <fstream>
#include <unordered_set>
#include <unordered_map>
#include <queue>
#include <random>

using namespace std;
using Pair = pair<int, int>;
using Pairs = vector<Pair>;
using AdjList = unordered_map<int, Pairs>;
using Queue = priority_queue<Pair, Pairs, std::greater<Pair>>;
using Set = unordered_set<int>;

constexpr auto INF = int(1e9 + 7);

int getRandom(int N) {
    default_random_engine generator;
    uniform_int_distribution<int> distribution(1, N);
    return distribution(generator);
}

int prim(int N, AdjList& adj, Queue q = {}, Set seen = {}, int total = 0) {
    auto start = getRandom(N);
    seen.insert(start);
    for (auto [w, v]: adj[start])
        q.push({ w, v });
    while (q.size()) {
        auto [cost, u] = q.top(); q.pop();
        if (!seen.insert(u).second)
            continue;
        total += cost;
        for (auto [w, v]: adj[u])
            if (seen.find(v) == seen.end())
                q.push({ w, v });
    }
    return total;
}

void run(const string& filename) {
    AdjList adj;
    fstream fin{ filename };
    int N, M; fin >> N >> M; // N vertices and M edges
    int u, v, w;             // edge u -> v of weight w
    while (fin >> u >> v >> w) {
        adj[u].emplace_back(w, v);
        adj[v].emplace_back(w, u);
    }
    auto cost = prim(N, adj);
    cout << filename << ": " << cost << endl;
}

int main() {
    run("problem15.9test.txt"); // problem15.9test.txt: 14
    run("problem15.9.txt");     // problem15.9.txt: -3612829
    return 0;
}

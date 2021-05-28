#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <queue>

using namespace std;
using VI = vector<int>;
using VS = vector<string>;
using Edge = tuple<int, int, int>;
using Edges = vector<Edge>;
using Pair = pair<int, int>;
using Pairs = vector<Pair>;
using AdjList = unordered_map<int, Pairs>;
using Queue = queue<int>;

// bellman-ford: N - 1 edge relaxations (u -> v of cost w) [ie. attempting to relax M edges N - 1 times] given N vertices
VI bell(Edges& E, int N, int start = 1, int INF = 1e6) {
    VI dist(N, INF);
    dist[start] = 0;
    auto K = N - 1;
    while (K--)
        for (auto [u, v, w]: E)
            dist[v] = min(dist[v], dist[u] + w);
    return dist;
}

// shortest-paths faster algorithm: only attempt to relax candidate edges (note: adjacency list needed)
VI spfa(Edges& E, int N, int start = 1, int INF = 1e6, AdjList adj = {}) {
    VI dist(N, INF);
    dist[start] = 0;
    for (auto [u, v, w]: E)
        adj[u].emplace_back(v, w);
    Queue q{{ start }};
    while (q.size()) {
        auto u = q.front(); q.pop();
        for (auto [v, w]: adj[u])
            if (dist[v] > dist[u] + w)
                dist[v] = dist[u] + w, q.push(v);
    }
    return dist;
}

VI run(const string& filename) {
    auto N = 0;
    Edges E;
    fstream fin{ filename };
    VS A;
    for (string line; getline(fin, line); A.emplace_back(line));
    for (auto& s: A) {
        transform(s.begin(), s.end(), s.begin(), [](auto c) { return c == ',' ? ' ' : c; });
        stringstream ss{ s };
        auto [u, v, w] = make_tuple(0, 0, 0);
        ss >> u;
        while (ss >> v >> w)
            E.emplace_back(u, v, w);
        ++N;
    }
    auto a = bell(E, N + 1),  // +1 for 1-based indexing
         b = spfa(E, N + 1);
    assert(a == b);
    return b;
}

int main() {
    auto dist = run("test.txt");
    VI A{ 7, 37, 59, 82, 99, 115, 133, 165, 188, 197 };
    transform(A.begin(), A.end(), A.begin(), [&](auto x) { return dist[x]; });
    copy(A.begin(), A.end(), ostream_iterator<int>(cout, ","));  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068,
    return 0;
}

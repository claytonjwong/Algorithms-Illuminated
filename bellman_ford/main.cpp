#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

using namespace std;
using VI = vector<int>;
using VS = vector<string>;
using Edge = tuple<int, int, int>;
using Edges = vector<Edge>;

VI bellman_ford(Edges& E, int N, int start = 1, int INF = 1e6) {
    VI dist(N, INF);
    dist[start] = 0;
    auto K = N - 1;
    while (K--)
        for (auto [u, v, w]: E)
            dist[v] = min(dist[v], dist[u] + w);
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
    return bellman_ford(E, N + 1);  // +1 for 1-based indexing
}

int main() {
    auto dist = run("test.txt");
    VI A{ 7, 37, 59, 82, 99, 115, 133, 165, 188, 197 };
    transform(A.begin(), A.end(), A.begin(), [&](auto x) { return dist[x]; });
    copy(A.begin(), A.end(), ostream_iterator<int>(cout, ","));  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068,
    return 0;
}

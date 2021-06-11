/*
 * Programming Problem 18.8: All-Pairs Shortest Paths
 *
 * In this problem, each file describes a directed graph. The first line of the file indicates the number
 * of vertices and edges, respectively. Each subsequent line describes an edge (the first two numbers are its tail
 * and head, respectively) and its length (the third number). NOTE: edge lengths might be negative, and the graphs
 * may or may not be negative cycles.
 *
 * Test cases: (contributed by Matt Davis) What is the shortest shortest path in the graphs described in this file
 * and in this file? (I.e., the minimum, over choices of an origin s and a destination t, of a shortest s-t path in the graph.)
 * (If the graph has a negative cycle, your algorithm should detect that fact.) (Answer: -2 and "contains a negative cycle," respectively.)
 *
 * Challenge data set: Repeat the previous problem for the graphs described in the following files: graph #1, graph #2, graph #3, and graph #4.
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>

#define PERF_TEST

using namespace std;

using LL = long long;
using VL = vector<LL>;
using VVL = vector<VL>;
using VVVL = vector<VVL>;
using Edges = unordered_map<string, LL>;

LL INF = 1e9 + 7;

string key(int i, int j) {
    stringstream ss; ss << i << "," << j;
    return ss.str();
}

VVL floyd_warshall(Edges& E, int N) {
    VVVL dp(N + 1, VVL(N + 1, VL(N + 1, INF)));
    for (auto i{ 1 }; i <= N; ++i)
        for (auto j{ 1 }; j <= N; ++j)
            if (i == j)
                dp[0][i][j] = 0;
            else
            if (E.find(key(i, j)) != E.end())
                dp[0][i][j] = E[key(i, j)];
    for (auto k{ 1 }; k <= N; ++k)
        for (auto i{ 1 }; i <= N; ++i)
            for (auto j{ 1 }; j <= N; ++j)
                dp[k][i][j] = min(dp[k - 1][i][j], dp[k - 1][i][k] + dp[k - 1][k][j]);
    return dp[N];
}

VVL floyd_warshall_memopt(Edges& E, int N) {
    VVL pre(N + 1, VL(N + 1, INF));
    for (auto i{ 1 }; i <= N; ++i)
        for (auto j{ 1 }; j <= N; ++j)
            if (i == j)
                pre[i][j] = 0;
            else
            if (E.find(key(i, j)) != E.end())
                pre[i][j] = E[key(i, j)];
    for (auto k{ 1 }; k <= N; ++k) {
        VVL cur(N + 1, VL(N + 1, INF));
        for (auto i{ 1 }; i <= N; ++i)
            for (auto j{ 1 }; j <= N; ++j)
                cur[i][j] = min(pre[i][j], pre[i][k] + pre[k][j]);
        swap(pre, cur);
    }
    return pre;
}

void run(const string& filename) {
    Edges E;
    fstream fin{ filename };
    int N, M; fin >> N >> M;
    for (int u, v, w; fin >> u >> v >> w; E[key(u, v)] = w);
#ifdef PERF_TEST
    auto a = floyd_warshall_memopt(E, N);
#else
    auto a = floyd_warshall_memopt(E, N),
         b = floyd_warshall(E, N);
    assert(a == b);  // 💩 sanity check
#endif
    auto cycle = false;
    for (auto i{ 1 }; i <= N && !cycle; ++i)
        cycle = a[i][i] < 0;
    if (cycle) {
        cout << filename << ": contains a negative cycle" << endl;
        return;
    }
    auto best = INF;
    for (auto& row: a)
        best = min(best, *min_element(row.begin(), row.end()));
    cout << filename << ": " << best << endl;
}

int main() {
    run("problem18.8test1.txt");  // problem18.8test1.txt: -2
    run("problem18.8test2.txt");  // problem18.8test2.txt: contains a negative cycle
    run("problem18.8file1.txt");  // problem18.8file1.txt: contains a negative cycle
    run("problem18.8file2.txt");  // problem18.8file2.txt: contains a negative cycle
    run("problem18.8file3.txt");  // problem18.8file3.txt: -19
//    run("problem18.8file4.txt");
    return 0;
}

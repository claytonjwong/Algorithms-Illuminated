#include <iostream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>

using namespace std;

using VI = vector<int>;
using AdjList = unordered_map<char, VI>;
using Set = unordered_set<char>;
using Map = unordered_map<char, int>;
using Queue = queue<char>;
using fun = function<void(char)>;

class Solution {
private:
    AdjList adj;
    const int N;
    Map m;
    Set seen;
    int color;
public:
    Solution(AdjList& adj) : adj{ adj }, N{ int(adj.size()) } {
    }
    void init(int start) {
        m.clear();
        seen.clear();
        color = start;
    }
    string topo_sort_bfs() {
        init(1);  // 👉 color forward from 1..N
        bfs();
        return to_string();
    }
    string topo_sort_dfs() {
        init(N);  // 👈 color reverse from N..1 (as the recursive stack unwinds)
        for (auto [u, _]: adj)
            dfs(u);
        return to_string();
    }
    void bfs() {
        Map degree;
        for (auto [_, neighbors]: adj)
            for (auto v: neighbors)
                ++degree[v];
        Queue q;
        for (auto [u, _]: adj)
            if (!degree[u] && seen.insert(u).second)
                q.push(u);
        while (q.size()) {
            auto u = q.front(); q.pop();
            m[u] = color++;
            for (auto v: adj[u])
                if (!--degree[v] && seen.insert(v).second)
                    q.push(v);
        }
    }
    void dfs(char start) {
        fun go = [&](auto u) {
            if (!seen.insert(u).second)
                return;
            for (auto v: adj[u])
                go(v);
            m[u] = color--;
        };
        go(start);
    }
    string to_string() {
        ostringstream os;
        for (auto [u, color]: m)
            os << u << ": " << color << endl;
        return os.str();
    }
};

int main() {
    //
    // graph from Quiz 8.3 on page 45 of Algorithms Illuminated: Part 2
    //
    AdjList adj{
        { 's', { 'v', 'w' } },
        { 'v', { 't' } },
        { 'w', { 't' } },
        { 't', {} }
    };
    Solution solution{ adj };

    cout << "BFS:" << endl << solution.topo_sort_bfs() << endl
         << "DFS:" << endl << solution.topo_sort_dfs() << endl;

//    BFS:
//    t: 4
//    w: 3
//    v: 2
//    s: 1
//
//    DFS:
//    s: 1
//    w: 2
//    v: 3
//    t: 4

    return 0;
}

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>

using namespace std;

using Queries = vector<int>;
using Distance = unordered_map<int, int>;
using Set = unordered_set<int>;

class BaseSolution {
protected:
    static constexpr auto INF = int(1e9 + 7);
public:
    virtual string run(string filename, Queries&& queries) = 0;
};

class NaiveSolution : public BaseSolution {
    using Edge = tuple<int, int, int>;
    using Edges = vector<Edge>;
public:
    Distance dijkstra(Edges& E) {
        Distance dist;
        Set seen;
        auto start{ 1 };
        dist[start] = 0, seen.insert(start);
        for (;;) {
            auto found = false;
            auto best_v = INF,
                 best_w = INF;
            for (auto [u, v, w]: E) {
                if (seen.find(u) == seen.end() || seen.find(v) != seen.end())
                    continue;
                found = true;
                if (best_w > dist[u] + w)
                    best_v = v,
                    best_w = dist[u] + w;
            }
            if (!found)
                break;
            auto [v, w] = tie(best_v, best_w);
            dist[v] = w, seen.insert(v);
        }
        return dist;
    }
    string run(string filename, Queries&& queries) {
        Edges E;
        fstream fin{ filename };
        string line;
        int u, v, w;
        char _;
        while (getline(fin, line)) {
            istringstream is{ line };
            for (is >> u; is >> v >> _ >> w; E.push_back({ u, v, w }));
        }
        auto dist = dijkstra(E);
        ostringstream os;
        transform(queries.begin(), queries.end(), ostream_iterator<int>(os, " "), [&](auto x) { return dist[x]; });
        return os.str();
    }
};

class HeapSolution : public BaseSolution {
    using Pair = pair<int, int>;
    using Pairs = vector<Pair>;
    using AdjList = unordered_map<int, Pairs>;
    priority_queue<Pair, Pairs, std::greater<Pair>> q;
public:
    Distance dijkstra(AdjList& adj) {
        Distance dist;
        Set seen;
        for (auto [u, _]: adj)
            dist[u] = INF;
        auto start{ 1 };
        q.push({ 0, start });
        while (q.size()) {
            auto [cost, u] = q.top(); q.pop();
            if (!seen.insert(u).second)
                continue;
            dist[u] = cost;
            for (auto [w, v]: adj[u])
                if (seen.find(v) == seen.end())
                    q.push({ dist[u] + w, v });
        }
        return dist;
    }
    string run(string filename, Queries&& queries) {
        AdjList adj;
        fstream fin{ filename };
        string line;
        int u, v, w;
        char _;
        while (getline(fin, line)) {
            istringstream is{ line };
            for (is >> u; is >> v >> _ >> w; adj[u].push_back({ w, v }));
        }
        auto dist = dijkstra(adj);
        ostringstream os;
        transform(queries.begin(), queries.end(), ostream_iterator<int>(os, " "), [&](auto x) { return dist[x]; });
        return os.str();
    }
};

void run(BaseSolution&& solution) {
    cout << "problem9.8test.txt: " << solution.run("problem9.8test.txt", Queries{1, 2, 3, 4, 5, 6, 7, 8 }) << endl
         << "problem9.8.txt      " << solution.run("problem9.8.txt", Queries{7, 37, 59, 82, 99, 115, 133, 165, 188, 197 }) << endl;
}

int main() {
    run(NaiveSolution());
//    problem9.8test.txt: 0 1 2 3 4 4 3 2
//    problem9.8.txt      2599 2610 2947 2052 2367 2399 2029 2442 2505 3068

    run(HeapSolution());
//    problem9.8test.txt: 0 1 2 3 4 4 3 2
//    problem9.8.txt      2599 2610 2947 2052 2367 2399 2029 2442 2505 3068
    return 0;
}

#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using namespace std;
using VI = vector<int>;
using Pair = pair<int, VI>;
using Set = unordered_set<int>;
using Adj = unordered_map<int, Set>;
using Cost = unordered_map<string, int>;

class Solution {
    int best, start, M, N;
    VI best_path;
    Adj adj;
    Cost cost;
    string key(int u, int v) {
        stringstream ss;
        ss << u << "," << v;
        return ss.str();
    }
    void init(const string& input_file, string line = {}) {
        best = 1e9 + 7; start = M = N = 0;
        best_path.clear();
        adj.clear();
        cost.clear();
        auto i = 0;
        fstream fin{ input_file };
        while (getline(fin, line)) {
            VI A;
            istringstream is{ line };
            copy(istream_iterator<int>(is), istream_iterator<int>(), back_inserter(A));
            if (0 < i++) {
                auto [u, v, w] = tie(A[0], A[1], A[2]);
                adj[u].insert(v); cost[key(u, v)] = w;
                adj[v].insert(u); cost[key(v, u)] = w;
            } else {
                N = A[0];
                M = A[1];
            }
        }
    }
    void go(int u, VI&& path, Set&& seen, int t = 0) {
        if (seen.size() == N) {
            t += cost[key(u, start)]; // connect ultimate edge of tour
            if (adj[u].find(start) != adj[u].end() && t < best)
                best = t, best_path = path;
            return;
        }
        for (auto v: adj[u]) {
            if (seen.find(v) != seen.end())
                continue;
            path.push_back(v), seen.insert(v);
            go(v, move(path), move(seen), t + cost[key(u, v)]);
            path.pop_back(), seen.erase(v);
        }
    }
public:
    Pair run(const string& input_file) {
        init(input_file);
        start = 1;
        go(start, {start}, {start});
        return {best, best_path};
    }
};

int main() {
    auto s = Solution();
    for (auto& input_file: {"quiz19.2.txt", "quiz20.7.txt"}) {
        auto [best, path] = s.run(input_file);
        cout << input_file << "  best: " << best << "  path: ";
        copy(path.begin(), path.end(), ostream_iterator<int>(cout, " "));
        cout << endl;
    }
    // quiz19.2.txt  best: 13  path: 1 3 4 2
    // quiz20.7.txt  best: 23  path: 1 4 5 2 3
    return 0;
}

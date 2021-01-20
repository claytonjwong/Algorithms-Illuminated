#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>

using namespace std;

using List = deque<int>;
using Lists = deque<List>;
using AdjList = unordered_map<int, List>;
using Set = unordered_set<int>;
using Map = unordered_map<int, int>;

namespace Base {
    class Solution {
    protected:
        AdjList adj, rev;
    public:
        Solution(AdjList& adj, AdjList& rev) : adj{ adj }, rev{ rev } {}
    };
}
namespace Recursive {
    struct Solution : public Base::Solution {
        Solution(AdjList& adj, AdjList& rev) : Base::Solution{ adj, rev } {}
        Lists kosaraju() {
            Lists lists;
            Set seen;
            auto order = topo_sort();
            using fun = function<void(int, List&)>;
            fun go = [&](auto u, auto& list) {
                if (!seen.insert(u).second)
                    return;
                list.push_back(u);
                for (auto v: adj[u])
                    go(v, list);
            };
            for (auto u: order) {
                List list;
                go(u, list);
                lists.emplace_back(list);
            }
            sort(lists.begin(), lists.end(), [](auto& a, auto& b) { return b.size() < a.size(); });
            return lists;
        }
        List topo_sort() {
            List list;
            Set seen;
            using fun = function<void(int)>;
            fun go = [&](auto u) {
                if (!seen.insert(u).second)
                    return;
                for (auto v: rev[u])
                    go(v);
                list.push_front(u);
            };
            for (auto [u, _]: rev)
                go(u);
            return list;
        }
    };
}
namespace Iterative {
    struct Solution : public Base::Solution {
        Solution(AdjList& adj, AdjList& rev) : Base::Solution{ adj, rev } {}
        Lists kosaraju() {
            Lists lists;
            Set seen;
            for (auto u: topo_sort()) {
                if (seen.find(u) != seen.end())
                    continue;
                List list;
                List stack{ u }; seen.insert(u);
                while (stack.size()) {
                    auto u = stack.back();
                    for (auto v: adj[u])
                        if (seen.insert(v).second)
                            stack.push_back(v);
                    if (u == stack.back())
                        list.push_back(u), stack.pop_back();
                }
                lists.emplace_back(list);
            }
            sort(lists.begin(), lists.end(), [](auto& a, auto& b) { return b.size() < a.size(); });
            return lists;
        }
        List topo_sort() {
            List list;
            Set seen;
            for (auto [u, _]: rev) {
                if (seen.find(u) != seen.end())
                    continue;
                List stack{ u }; seen.insert(u);
                while (stack.size()) {
                    auto u = stack.back();
                    for (auto v: rev[u])
                        if (seen.insert(v).second)
                            stack.push_back(v);
                    if (u == stack.back())
                        list.push_front(stack.back()), stack.pop_back();
                }
            }
            return list;
        }
    };
}

void run(string filename) {
    int u, v;
    AdjList adj, rev;
    fstream fin{ filename };
    for (string line; fin >> u >> v;) {
        adj[u].push_back(v);
        rev[v].push_back(u);
    }
    auto A = Iterative::Solution{ adj, rev }.kosaraju();
    A.resize(min(A.size(), size_t(5)));
    cout << filename << ": ";
    for (auto i{ 0 }; i < A.size(); cout << A[i++].size() << " ");
    cout << endl;
}

int main() {
    run("section8.6.5page64.txt");  // Graph from section 8.6.5 on page 64 of Algorithms Illuminated: Part 2
    run("problem8.10test1.txt");    // Test case #1: A 9-vertex 11-edge graph. Top 5 SCC sizes: 3,3,3,0,0
    run("problem8.10test2.txt");    // Test case #2: An 8-vertex 14-edge graph. Top 5 SCC sizes: 3,3,2,0,0
    run("problem8.10test3.txt");    // Test case #3: An 8-vertex 9-edge graph. Top 5 SCC sizes: 3,3,1,1,0
    run("problem8.10test4.txt");    // Test case #4: An 8-vertex 11-edge graph. Top 5 SCC sizes: 7,1,0,0,0
    run("problem8.10test5.txt");    // Test case #5: A 12-vertex 20-edge graph. Top 5 SCC sizes: 6,3,2,1,0
    run("problem8.10.txt");         // Challenge data set: Vertices are labeled as positive integers from 1 to 875714

//    section8.6.5page64.txt: 4 3 3 1
//    problem8.10test1.txt: 3 3 3
//    problem8.10test2.txt: 3 3 2
//    problem8.10test3.txt: 3 3 1 1
//    problem8.10test4.txt: 7 1
//    problem8.10test5.txt: 6 3 2 1
//    problem8.10.txt: 434821 968 459 313 211

    return 0;
}

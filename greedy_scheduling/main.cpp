#include <iostream>
#include <fstream>
#include <vector>
#include <numeric>

using namespace std;

using LL = long long;
struct Job {
    LL weight, length;
    Job(LL weight, LL length) : weight{ weight }, length{ length } {}
};
using Jobs = vector<Job>;

class Solution {
public:
    using Pair = pair<LL, LL>; // sub-optimal, optimal
    Pair minSum(Jobs& jobs) {
        auto diff = [](auto& a, auto& b) {
            auto first = a.weight - a.length,
                 second = b.weight - b.length;
            return first == second ? b.weight < a.weight : second < first; // sort by descending difference, break ties in favor of jobs with larger weights
        };
        auto ratio = [](auto& a, auto& b) {
            auto first = double(a.weight) / a.length,
                 second = double(b.weight) / b.length;
            return first == second ? b.weight < a.weight : second < first; // sort by descending ratio, break ties in favor of jobs with larger weights
        };
        return { calcSum(jobs, diff), calcSum(jobs, ratio) };
    }
private:
    template<typename Comp>
    LL calcSum(Jobs& jobs, Comp comp, LL time = 0LL) {
        sort(jobs.begin(), jobs.end(), comp);
        return accumulate(jobs.begin(), jobs.end(), 0LL, [&](LL total, auto& job) {
            return total += job.weight * (time += job.length);
        });
    }
};

void run(const string& filename) {
    Jobs jobs;
    LL N, weight, length;
    fstream fin{ filename };
    for (fin >> N; fin >> weight >> length; jobs.emplace_back(Job{ weight, length }));
    auto [diff, ratio] = Solution().minSum(jobs);
    cout << diff << ", " << ratio << endl;
}

int main() {
    run("problem13.4test1.txt"); // 23, 22
    run("problem13.4test2.txt"); // 68615, 67247
    run("problem13.4.txt");      // 69119377652, 67311454237
    return 0;
}

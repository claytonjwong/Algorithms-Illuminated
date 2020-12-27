#include <iostream>
#include <fstream>
#include <vector>
#include <random>

using namespace std;
using VI = vector<int>;

int random(int L, int R) {
    random_device rd;
    mt19937 gen{ rd() };
    uniform_int_distribution dist(L, R);
    return dist(gen);
}

int partition(VI& A, int L, int R) {
    auto i = L + 1,
         j = L + 1,
         k = random(L, R);
    swap(A[L], A[k]);            // swap pivot A[k] with first element of the subarray A[L]
    while (j <= R) {
        if (A[j] < A[L])         // maintain loop invariant A[i] < pivot < A[j]
            swap(A[i++], A[j]);
        ++j;
    }
    swap(A[L], A[i - 1]);        // swap pivot A[L] with last value less-than pivot A[i - 1]
    return i - 1;
}

int rselect(VI& A, int i, int L, int R) {
    auto k = partition(A, L, R);
    if (i == k)
        return A[k];  // 🎯 lucky guess
    if (i < k)
        R = k - 1;
    else
        L = k + 1;
    return rselect(A, i, L, R);
}

int run(string filename, int i, VI A = {}) {
    fstream fin{ filename };
    for (string line; fin >> line; A.push_back(stoi(line)));
    int N = A.size();
    return rselect(A, i - 1, 0, N - 1);  // -1 for 0-based indexing
}

int main() {
    cout << "problem6.5test1.txt: " << run("problem6.5test1.txt", 5)  << endl;  // problem6.5test1.txt: 5469
    cout << "problem6.5test2.txt: " << run("problem6.5test2.txt", 50) << endl;  // problem6.5test2.txt: 4715
    return 0;
}

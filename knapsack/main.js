const assert = require('assert');
const LineByLine = require('n-readlines');

let top_down = (A, K, m = new Map()) => {
    let N = A.length;
    let go = (i = 0, k = K) => {
        if (i == N)                                                                 // 🛑 empty set
            return 0;
        let key = `${i},${k}`;
        if (m.has(key))                                                             // 🤔 memo
            return m.get(key);
        let [value, weight] = A[i];
        let include = 0 <= k - weight ? go(i + 1, k - weight) + value : -Infinity,  // ✅ include A[i]
            exclude = go(i + 1, k);                                                 // 🚫 exclude A[i]
        return m.set(key, Math.max(include, exclude))                               // 🎯 best
                .get(key);
    };
    return go();
};

let bottom_up = (A, K) => {
    let N = A.length;
    let dp = [...Array(N + 1)].map(_ => Array(K + 1).fill(-Infinity));                  // 🤔 memo
    for (let k = 0; k < K; dp[0][k++] = 0);                                             // 🛑 empty set
    for (let i = 1; i <= N; ++i) {
        for (let k = 0; k <= K; ++k) {
            let [value, weight] = A[i - 1];
            let include = 0 <= k - weight ? dp[i - 1][k - weight] + value : -Infinity,  // ✅ include A[i]
                exclude = dp[i - 1][k];                                                 // 🚫 exclude A[i]
            dp[i][k] = Math.max(include, exclude);                                      // 🎯 best
        }
    }
    return dp[N][K];
};

let run = filename => {
    let A = [];
    const input = new LineByLine(filename)
    let [K, N] = input.next().toString().split(' ').map(Number);  // K capacity, N items
    let line;
    while (line = input.next()) {
        let [value, weight] = line.toString().split(' ').map(Number);
        A.push([value, weight]);
    }
    let a = top_down(A, K),
        b = bottom_up(A, K);
    assert(a == b); // 💩 sanity check
    console.log(`${filename}: ${a}`);
};

run('problem16.7test.txt')  // problem16.7test.txt: 2493893

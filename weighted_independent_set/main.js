/*
 * In this problem, each file describes the weights of vertices in a path graph and has the format:
 * [number_of_vertices_in_path_graph]
 * [weight of first vertex]
 * [weight of second vertex]
 * ...
 * Test case: (contributed by Logan Travis) What is the value of a maximum-weight independent set of the 10-vertex path graph described in this file, and which vertices belong to the MWIS? (Answer: 2617, and the vertices 2, 4, 7, and 10).
 * Challenge data set: Repeat the previous problem for the 1000-vertex path graph described in this file.
 */

const assert = require('assert');
const LineByLine = require('n-readlines');

let top_down = (A, m = {}) => {
    let N = A.length;
    let go = (i = N - 1) => {
        if (m[i])                                     // 🤔 memo
            return m[i];
        if (i < 0) return m[i] = 0;                   // 🛑 empty set
        if (!i) return m[i] = A[0];                   // 🛑 single set
        let include = go(i - 2) + A[i],               // ✅ include A[i]
            exclude = go(i - 1);                      // 🚫 exclude A[i]
        return m[i] = Math.max(include, exclude);     // 🎯 best
    };
    return go();
};

let bottom_up = A => {
    let N = A.length;
    let dp = Array(N + 1);                    // 🤔 memo
    dp[0] = 0;                                // 🛑 empty set
    dp[1] = A[0];                             // 🛑 single set
    for (let i = 2; i <= N; ++i) {
        let include = dp[i - 2] + A[i - 1],   // ✅ include A[i] (use A[i - 1] since dp[i] is offset by 1 for explicit 🛑 empty set at index 0, ie. index -1 doesn't exist)
            exclude = dp[i - 1];              // 🚫 exclude A[i]
        dp[i] = Math.max(include, exclude);   // 🎯 best
    }
    return dp[N];
};

let run = filename => {
    let A = [];
    let input = new LineByLine(filename);
    let line;
    let first = true;
    while (line = input.next()) {
        if (!first) {
            A.push(Number(line.toString('ascii')));
        } else {
            first = false;
        }
    }
    let a = top_down(A),
        b = bottom_up(A);
    assert(a == b); // 💩 sanity check
    console.log(`${filename}: ${a}`);
};

run('problem16.6test.txt');  // problem16.6test.txt: 2617
run('problem16.6.txt');      // problem16.6.txt: 2955353732

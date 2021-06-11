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

const LineByLine = require('n-readlines');
const assert = require('assert');

let key = (i, j) => `${i},${j}`;

let floyd_warshall = (E, N) => {
    let dp = [...Array(N + 1)].map(_ => [...Array(N + 1)].map(_ => Array(N + 1).fill(Infinity)));
    for (let i = 1; i <= N; ++i)
        for (let j = 1; j <= N; ++j)
            if (i == j)
                dp[0][i][j] = 0;
            else
            if (E.has(key(i, j)))
                dp[0][i][j] = E.get(key(i, j));
    for (let k = 1; k <= N; ++k)
        for (let i = 1; i <= N; ++i)
            for (let j = 1; j <= N; ++j)
                dp[k][i][j] = Math.min(dp[k - 1][i][j], dp[k - 1][i][k] + dp[k - 1][k][j]);
    return dp[N];
};

let floyd_warshall_memopt = (E, N) => {
    let pre = [...Array(N + 1)].map(_ => Array(N + 1).fill(Infinity));
    for (let i = 1; i <= N; ++i)
        for (let j = 1; j <= N; ++j)
            if (i == j)
                pre[i][j] = 0;
            else
            if (E.has(key(i, j)))
                pre[i][j] = E.get(key(i, j));
    for (let k = 1; k <= N; ++k) {
        let cur = [...Array(N + 1)].map(_ => Array(N + 1).fill(Infinity));
        for (let i = 1; i <= N; ++i)
            for (let j = 1; j <= N; ++j)
                cur[i][j] = Math.min(pre[i][j], pre[i][k] + pre[k][j]);
        [pre, cur] = [cur, pre];
    }
    return pre;
};

let run = filename => {
    let E = new Map();
    let input = new LineByLine(filename);
    let [N, _] = input.next().toString('ascii').split(' ').map(Number);
    let line;
    while (line = input.next()) {
        let [u, v, w] = line.toString('ascii').split(' ').map(Number);
        E.set(key(u, v), w);
    }
    let a = floyd_warshall_memopt(E, N);
    // let b = floyd_warshall(E, N);
    // for (let i = 1; i <= N; ++i)
    //     for (let j = 1; j <= N; ++j)
    //         assert(a[i][j] == b[i][j]);
    let cycle = false;
    for (let i = 1; i <= N; ++i)
        if (a[i][i] < 0)
            cycle = true;
    if (cycle) {
        console.log(`${filename}: contains a negative cycle`);
        return;
    }
    var best = Infinity;
    for (row of a)
        best = Math.min(best, ...row);
    console.log(`${filename}: ${best}`);
};

run('problem18.8test1.txt');  // problem18.8test1.txt: -2
run('problem18.8test2.txt');  // problem18.8test2.txt: contains a negative cycle
run('problem18.8file1.txt');  // problem18.8file1.txt: contains a negative cycle
run('problem18.8file2.txt');  // problem18.8file2.txt: contains a negative cycle
run('problem18.8file3.txt');  // problem18.8file3.txt: -19
// run('problem18.8file4.txt');
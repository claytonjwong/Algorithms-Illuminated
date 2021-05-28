const assert = require('assert');
const zip = require('lodash/zip');
const LineByLine = require('n-readlines');

// bellman-ford: N - 1 edge relaxations (u -> v of cost w) [ie. attempting to relax M edges N - 1 times] given N vertices
let bell = (E, N, start = 1, INF = Number(1e6)) => {
    let dist = Array(N).fill(INF);
    dist[start] = 0;
    let K = N - 1;
    while (K--)
        E.forEach(([u, v, w]) => dist[v] = Math.min(dist[v], dist[u] + w));
    return dist;
};

// shortest-paths faster algorithm: only attempt to relax candidate edges (note: adjacency list needed)
let spfa = (E, N, start = 1, INF = Number(1e6)) => {
    let dist = Array(N).fill(INF);
    dist[start] = 0;
    let adj = [...Array(N)].map(_ => []);
    E.forEach(([u, v, w]) => adj[u].push([v, w]));
    let q = [start];
    while (q.length) {
        let u = q.shift();
        for (let [v, w] of adj[u])
            if (dist[v] > dist[u] + w)
                dist[v] = dist[u] + w, q.push(v);
    }
    return dist;
};

let run = filename => {
    let N = 0;
    let E = [];
    let input = new LineByLine(filename);
    let line;
    while (line = input.next()) {
        let A = line.toString('ascii').split('\t').filter(it => it.length);
        let u = Number(A.shift());
        A.map(pair => pair.split(',').map(Number)).forEach(([v, w]) => E.push([u, v, w]));
        ++N;
    }
    let a = bell(E, N + 1),  // +1 for 1-based indexing
        b = spfa(E, N + 1);
    zip(a, b).forEach(([x, y]) => assert(x == y));  // 💩 sanity check: single source shortest paths are the same
    return a;
};

let dist = run('test.txt');
console.log([7, 37, 59, 82, 99, 115, 133, 165, 188, 197].map(x => dist[x]).join(','));  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068

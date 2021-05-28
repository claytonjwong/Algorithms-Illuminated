const LineByLine = require('n-readlines');

let bellman_ford = (E, N, start = 1, INF = Number(1e9)) => {
    let dist = Array(N).fill(INF);
    dist[start] = 0;
    let K = N - 1;
    while (K--)
        E.forEach(([u, v, w]) => dist[v] = Math.min(dist[v], dist[u] + w));
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
    return bellman_ford(E, N + 1);  // +1 for 1-based indexing
};

let dist = run('test.txt');
console.log([7, 37, 59, 82, 99, 115, 133, 165, 188, 197].map(x => dist[x]).join(','));  // 2599,2610,2947,2052,2367,2399,2029,2442,2505,3068

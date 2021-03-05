let LineByLine = require('n-readlines');

let INF = Number(1e9 + 7);

class NaiveSolution {
    dijkstra(E) {
        let dist = new Map();
        let seen = new Set();
        let start = 1;
        dist[start] = 0; seen.add(start);
        for (;;) {
            let found = false;
            let best_v = INF,
                best_w = INF;
            for (let [u, v, w] of E) {
                if (!seen.has(u) || seen.has(v))
                    continue;
                found = true;
                if (best_w > dist[u] + w)
                    best_v = v,
                    best_w = dist[u] + w;
            }
            if (!found)
                break;
            let [v, w] = [best_v, best_w];
            dist[v] = w; seen.add(v);
        }
        return dist;
    }
    run(filename, queries) {
        let E = [];
        let input = new LineByLine(filename);
        let line;
        while (line = input.next()) {
            let words = String.fromCharCode(...line).trim().split(/\s+/);
            let u = Number(words[0]);
            for (let i = 1; i < words.length; ++i) {
                let [v, w] = words[i].split(',').map(Number);
                E.push([ u, v, w ]);
            }
        }
        let dist = this.dijkstra(E);
        return queries.map(x => dist[x]).join(' ');
    }
}

let heapkey = x => Array.isArray(x) ? x[0] : x;
let heappush = (A, x, f = Math.min) => {
    let P = i => Math.floor((i - 1) / 2);  // parent
    A.push(x);
    let N = A.length,
        i = N - 1;
    while (0 < i && heapkey(A[i]) == f(heapkey(A[i]), heapkey(A[P(i)]))) {
        [A[i], A[P(i)]] = [A[P(i)], A[i]];
        i = P(i);
    }
};
let heappop = (A, f = Math.min) => {
    let L = i => 2 * i + 1,  // children
        R = i => 2 * i + 2;
    let N = A.length,
        i = 0;
    let top = A[0];
    [A[0], A[N - 1]] = [A[N - 1], A[0]], A.pop(), --N;
    let ok;
    do {
        ok = true;
        let left = f == Math.min ? Infinity : -Infinity,
            right = left;
        if (L(i) < N && heapkey(A[i]) != f(heapkey(A[i]), heapkey(A[L(i)]))) ok = false, left  = heapkey(A[L(i)]);
        if (R(i) < N && heapkey(A[i]) != f(heapkey(A[i]), heapkey(A[R(i)]))) ok = false, right = heapkey(A[R(i)]);
        if (!ok) {
            let j = left == f(left, right) ? L(i) : R(i);
            [A[i], A[j]] = [A[j], A[i]];
            i = j;
        }
    } while (!ok);
    return top;
};

class HeapSolution {
    dijkstra(adj) {
        let dist = {};
        let seen = new Set();
        let start = 1;
        let q = [[ 0, start ]];
        while (q.length) {
            let [cost, u] = heappop(q);
            if (seen.has(u))
                continue;
            dist[u] = cost, seen.add(u);
            for (let [w, v] of (adj[u] || []))
                heappush(q, [ dist[u] + w, v ]);
        }
        return dist;
    }
    run(filename, queries) {
        let adj = {};
        let input = new LineByLine(filename);
        let line;
        while (line = input.next()) {
            let words = String.fromCharCode(...line).trim().split('\t');
            let u = Number(words[0]);
            if (!(u in adj))
                adj[u] = [];
            for (let i = 1; i < words.length; ++i) {
                let [v, w] = words[i].split(',').map(Number);
                adj[u].push([ w, v ]);
            }
        }
        let dist = this.dijkstra(adj);
        return queries.map(x => dist[x]).join(' ');
    }
}

let run = solution => {
    console.log(solution.run('problem9.8test.txt', [1, 2, 3, 4, 5, 6, 7, 8]));
    console.log(solution.run('problem9.8.txt', [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]));
};

run(new NaiveSolution());
//    0 1 2 3 4 4 3 2
//    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068

run(new HeapSolution());
//    0 1 2 3 4 4 3 2
//    2599 2610 2947 2052 2367 2399 2029 2442 2505 3068

let LineByLine = require('n-readlines');

let key = x => Array.isArray(x) ? x[0] : x;
let heappush = (A, x, f = Math.min) => {
    let P = i => Math.floor((i - 1) / 2);  // parent
    A.push(x);
    let N = A.length,
        i = N - 1;
    while (0 < i && key(A[i]) == f(key(A[i]), key(A[P(i)]))) {
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
        if (L(i) < N && key(A[i]) != f(key(A[i]), key(A[L(i)]))) ok = false, left  = key(A[L(i)]);
        if (R(i) < N && key(A[i]) != f(key(A[i]), key(A[R(i)]))) ok = false, right = key(A[R(i)]);
        if (!ok) {
            let j = left == f(left, right) ? L(i) : R(i);
            [A[i], A[j]] = [A[j], A[i]];
            i = j;
        }
    } while (!ok);
    return top;
};

let prim = (N, adj, q = [], seen = new Set(), total = 0) => {
    let start = Math.ceil(N * Math.random());
    seen.add(start);
    for (let [w, v] of adj.get(start))
        heappush(q, [w, v]);
    while (q.length) {
        let [cost, u] = heappop(q);
        if (seen.has(u))
            continue;
        total += cost; seen.add(u);
        for (let [w, v] of adj.get(u))
            if (!seen.has(v))
                heappush(q, [w, v]);
    }
    return total;
};

let run = filename => {
    let adj = new Map();
    let input = new LineByLine(filename);
    let line = input.next();
    let [N, M] = String.fromCharCode(...line).trim().split(' ').map(Number);
    while (line = input.next()) {
        let [u, v, w] = String.fromCharCode(...line).trim().split(' ').map(Number);
        if (!adj.has(u)) adj.set(u, []);
        if (!adj.has(v)) adj.set(v, []);
        adj.get(u).push([w, v]);
        adj.get(v).push([w, u]);
    }
    let cost = prim(N, adj);
    console.log(`${filename}: ${cost}`);
}

run('problem15.9test.txt') // problem15.9test.txt: 14
run('problem15.9.txt')     // problem15.9.txt: -3612829

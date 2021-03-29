/*
 * Programming Problem 14.6: Huffman Codes
 *
 * In this problem the file format is:
 * [number_of_symbols]
 * [weight of symbol #1]
 * [weight of symbol #2]
 * ...
 */

let LineByLine = require('n-readlines');

class Tree {
    constructor(weight, left = null, right = null) {
        this.weight = weight;
        this.left = left;
        this.right = right;
    }
}

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

let encode = A => {
    let T = [];
    for (let weight of A)
        heappush(T, [ weight, new Tree(weight) ]);
    while (1 < T.length) {
        let [ a, b ] = [ heappop(T), heappop(T) ];
        let c = [ a[0] + b[0], new Tree(a[0] + b[0], a[1], b[1]) ];
        heappush(T, c);
    }
    return T[0][1];
};

let run = filename => {
    let A = [];
    let input = new LineByLine(filename);
    let line;
    line = input.next(); // N
    while (line = input.next()) {
        let weight = Number(String.fromCharCode(...line).trim());
        A.push(weight);
    }
    let tree = encode(A);
    let [ lo, hi ] = [ Infinity, -Infinity ];
    let go = (root = tree, depth = 0) => {
        if (!root)
            return;
        let isLeaf = root => !root.left && !root.right;
        if (isLeaf(root))
            lo = Math.min(lo, depth),
            hi = Math.max(hi, depth);
        else
            go(root.left, depth + 1),
            go(root.right, depth + 1);
    };
    go();
    return [ lo, hi ];
}

for (let filename of [ 'problem14.6test1.txt', 'problem14.6test2.txt', 'problem14.6.txt' ]) {
    let [lo, hi] = run(filename);
    console.log(`${filename}: ${lo}, ${hi}`); // min, max encoding length in the corresponding optimal prefix-free tree
}

//    problem14.6test1.txt: 2, 5
//    problem14.6test2.txt: 3, 6
//    problem14.6.txt: 9, 19

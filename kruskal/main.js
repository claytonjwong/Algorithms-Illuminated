let LineByLine = require('n-readlines');

let kruskal = E => {
    let total = 0;
    let M = E.length;
    let P = [...Array(M).keys()]; // 🙂 parent representatives of 1..M disjoint sets
    let find = x => P[x] = P[x] == x ? x : find(P[x]);
    let union = (a, b) => {
        a = find(a);
        b = find(b);
        if (a == b)
            return false;
        P[a] = b; // 🎲 arbitrary choice
        return true;
    };
    E.sort((first, second) => { // sort edges by nondecreasing weight
        let [u1, v1, w1] = first,
            [u2, v2, w2] = second;
        return w1 - w2;
    });
    for (let [u, v, w] of E)
        if (union(u, v))
            total += w;
    return total;
};

let run = filename => {
    let E = [];
    let input = new LineByLine(filename);
    let line = input.next(); // ignore first line with N vertices and M edges
    while (line = input.next()) {
        let [u, v, w] = String.fromCharCode(...line).trim().split(' ').map(Number);
        E.push([ u, v, w ]);
    }
    let cost = kruskal(E);
    console.log(`${filename}: ${cost}`);
};

run('problem15.9test.txt'); // problem15.9test.txt: 14
run('problem15.9.txt');     // problem15.9.txt: -3612829

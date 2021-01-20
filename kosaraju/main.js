class BaseSolution {
    constructor(adj, rev) {
        this.adj = adj;
        this.rev = rev;
    }
}

class RecursiveSolution extends BaseSolution {
    constructor(adj, rev) {
        super(adj, rev);
    }
    topo_sort() {
        let list = [];
        let seen = new Set();
        let go = u => {
            if (seen.has(u))
                return;
            seen.add(u);
            for (let v of [...this.rev.get(u)])
                go(v);
            list.unshift(u);
        };
        for (let [u, _] of [...this.rev])
            go(u);
        return list;
    }
    kosaraju() {
        let lists = [];
        let seen = new Set();
        let go = (u, list) => {
            if (seen.has(u))
                return;
            seen.add(u);
            list.push(u);
            for (let v of [...this.adj.get(u)])
                go(v, list);
        };
        for (let u of this.topo_sort()) {
            let list = [];
            go(u, list);
            lists.push([...list]);
        }
        lists.sort((a, b) => b.length - a.length);
        return lists;
    }
}

class IterativeSolution extends BaseSolution {
    constructor(adj, rev) {
        super(adj, rev);
    }
    topo_sort() {
        let list = [];
        let seen = new Set();
        for (let [u, _] of [...this.rev]) {
            if (seen.has(u))
                continue;
            let stack = [ u ]; seen.add(u);
            stack.back = () => stack[stack.length - 1];
            while (stack.length) {
                let u = stack.back();
                for (let v of [...this.rev.get(u)])
                    if (!seen.has(v))
                        stack.push(v), seen.add(v);
                if (u == stack.back())
                    list.unshift(stack.pop());
            }
        }
        return list;
    }
    kosaraju() {
        let lists = [];
        let seen = new Set();
        for (let u of this.topo_sort()) {
            if (seen.has(u))
                continue;
            let list = [];
            let stack = [ u ]; seen.add(u);
            stack.back = () => stack[stack.length - 1];
            while (stack.length) {
                let u = stack.back();
                for (let v of [...this.adj.get(u)])
                    if (!seen.has(v))
                        stack.push(v), seen.add(v);
                if (u == stack.back())
                    list.push(stack.pop());
            }
            lists.push([...list]);
        }
        lists.sort((a, b) => b.length - a.length);
        return lists;
    }
}

let run = filename => {
    let adj = new Map(),
        rev = new Map();
    let LineByLine = require('n-readlines');
    let input = new LineByLine(filename);
    let line;
    while (line = input.next()) {
        let [u, v] = String.fromCharCode(...line).split(' ').map(Number);
        if (!adj.has(u)) adj.set(u, []); if (!adj.has(v)) adj.set(v, []);
        if (!rev.has(u)) rev.set(u, []); if (!rev.has(v)) rev.set(v, []);
        adj.get(u).push(v);
        rev.get(v).push(u);
    }
    // let A = new RecursiveSolution(adj, rev).kosaraju();
    let A = new IterativeSolution(adj, rev).kosaraju();
    console.log(`${filename}: ${A.slice(0, Math.min(A.length, 5)).map(scc => scc.length).join(' ')}`);
};

run('section8.6.5page64.txt')  // Graph from section 8.6.5 on page 64 of Algorithms Illuminated: Part 2
run('problem8.10test1.txt')    // Test case #1: A 9-vertex 11-edge graph. Top 5 SCC sizes: 3,3,3,0,0
run('problem8.10test2.txt')    // Test case #2: An 8-vertex 14-edge graph. Top 5 SCC sizes: 3,3,2,0,0
run('problem8.10test3.txt')    // Test case #3: An 8-vertex 9-edge graph. Top 5 SCC sizes: 3,3,1,1,0
run('problem8.10test4.txt')    // Test case #4: An 8-vertex 11-edge graph. Top 5 SCC sizes: 7,1,0,0,0
run('problem8.10test5.txt')    // Test case #5: A 12-vertex 20-edge graph. Top 5 SCC sizes: 6,3,2,1,0
run('problem8.10.txt')         // Challenge data set: Vertices are labeled as positive integers from 1 to 875714


//    section8.6.5page64.txt: 4 3 3 1
//    problem8.10test1.txt: 3 3 3
//    problem8.10test2.txt: 3 3 2
//    problem8.10test3.txt: 3 3 1 1
//    problem8.10test4.txt: 7 1
//    problem8.10test5.txt: 6 3 2 1
//    problem8.10.txt: 434821 968 459 313 211

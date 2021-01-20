class Solution {
    constructor(adj) {
        this.adj = adj;
        this.N = this.adj.size;
    }
    init(start) {
        this.color = start;
        this.seen = new Set();
        this.m = new Map();
    }
    topo_sort_bfs() {
        this.init(1);       // 👉 color forward from 1..N
        this.bfs();
        return this.to_string();
    }
    topo_sort_dfs() {
        this.init(this.N);  // 👈 color reverse from N..1 (as the recursive stack unwinds)
        for (let [u, _] of [...this.adj])
            this.dfs(u);
        return this.to_string();
    }
    bfs() {
        let degree = new Map();
        for (let [u, _] of [...this.adj]) {
            degree.set(u, (degree.get(u) || 0));
            for (let v of this.adj.get(u))
                degree.set(v, 1 + (degree.get(v) || 0));
        }
        let q = [...this.adj].map(([u, _]) => u).filter(u => !degree.get(u));
        let seen = new Set(q);
        while (q.length) {
            let u = q.shift();
            this.m.set(u, this.color++);
            for (let v of this.adj.get(u)) {
                degree.set(v, -1 + degree.get(v));
                if (!degree.get(v) && !seen.has(v))
                    q.push(v), seen.add(v);
            }
        }
    }
    dfs(u) {
        if (this.seen.has(u))
            return;
        this.seen.add(u);
        for (let v of this.adj.get(u))
            if (!this.seen.has(v))
                this.dfs(v);
        this.m.set(u, this.color--);
    }
    to_string() {
        let s = [];
        for (let [u, color] of [...this.m])
            s.push(`${u}: ${color}`);
        return s.join('\n');
    }
}

let adj = new Map();
adj.set('s', ['v', 'w']);
adj.set('v', ['t']);
adj.set('w', ['t']);
adj.set('t', []);
let solution = new Solution(adj);
console.log(`BFS:\n${solution.topo_sort_bfs()}\n\nDFS:\n${solution.topo_sort_dfs()}`);

//    BFS:
//    s: 1
//    v: 2
//    w: 3
//    t: 4

//    DFS:
//    t: 4
//    v: 3
//    w: 2
//    s: 1

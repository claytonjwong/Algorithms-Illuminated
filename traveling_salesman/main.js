let LineByLine = require('n-readlines');

class Solution {
    key = (u, v) => `${u},${v}`;
    init(input_file) {
        this.best = Number(1e9 + 7);
        this.best_path = [];
        this.M = 0;
        this.N = 0;
        this.adj = new Map();
        this.cost = new Map();
        let [A, line, i] = [[], '', 0];
        let input = new LineByLine(input_file);
        while (line = input.next()) {
            let A = String.fromCharCode(...line).trim().split(' ').map(Number);
            if (0 < i++) {
                let [u, v, w] = A;
                if (!this.adj.has(u)) this.adj.set(u, new Set());
                if (!this.adj.has(v)) this.adj.set(v, new Set());
                this.adj.get(u).add(v), this.cost.set(this.key(u, v), w);
                this.adj.get(v).add(u), this.cost.set(this.key(v, u), w);
            } else {
                [this.N, this.M] = A;
            }
        }
    }
    run(input_file) {
        this.init(input_file);
        this.start = 1;
        this.go(this.start, [this.start], new Set([this.start]));
        return [this.best, this.best_path];
    }
    go(u, path, seen, t = 0) {
        if (seen.size == this.N) {
            t += this.cost.get(this.key(u, this.start)) || 0;
            if (this.adj.get(u).has(this.start) && t < this.best)
                this.best = t, this.best_path = [...path];
            return;
        }
        for (let v of this.adj.get(u)) {
            if (seen.has(v))
                continue;
            path.push(v), seen.add(v);
            this.go(v, path, seen, t + this.cost.get(this.key(u, v)));
            path.pop(), seen.delete(v);
        }
    }
}

let s = new Solution();
for (let input_file of ['quiz19.2.txt', 'quiz20.7.txt']) {
    let [best, path] = s.run(input_file);
    console.log(`${input_file}  best: ${best}  path: ${path}`);
}
// quiz19.2.txt  best: 13  path: 1,2,4,3
// quiz20.7.txt  best: 23  path: 1,3,2,5,4
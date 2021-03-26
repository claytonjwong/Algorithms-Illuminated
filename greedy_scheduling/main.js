let LineByLine = require('n-readlines');

class Job {
    constructor(weight, length) {
        this.weight = weight;
        this.length = length;
    }
}

class Solution {
    minSum(jobs) {
        let diff = (a, b) => {
            let first = a.weight - a.length,
                second = b.weight - b.length;
            return first == second ? b.weight - a.weight : second - first; // sort by descending difference, break ties in favor of jobs with larger weights
        };
        let ratio = (a, b) => {
            let first = a.weight / a.length,
                second = b.weight / b.length;
            return first == second ? b.weight - a.weight : second - first; // sort by descending ratio, break ties in favor of jobs with larger weights
        };
        return [ this._calcSum(jobs, diff), this._calcSum(jobs, ratio) ];
    }
    _calcSum(jobs, comp, time = 0) {
        jobs.sort((a, b) => comp(a, b));
        return jobs.reduce((total, job) => total + job.weight * (time += job.length), 0);
    }
}

let run = filename => {
    let jobs = [];
    let input = new LineByLine(filename);
    let line = input.next(); // N
    while (line = input.next()) {
        let words = String.fromCharCode(...line).trim().split(' ');
        let [weight, length] = words.map(Number);
        jobs.push(new Job(weight, length));
    }
    let [diff, ratio] = new Solution().minSum(jobs);
    console.log(`${diff}, ${ratio}`); // sub-optimal, optimal
};

run('problem13.4test1.txt'); // 23, 22
run('problem13.4test2.txt'); // 68615, 67247
run('problem13.4.txt');      // 69119377652, 67311454237

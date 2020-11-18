let sort = A => {
    let go = A => {
        let N = A.length;
        if (N < 2)
            return [A, 0];
        let half = Math.floor(N / 2);
        let [first,  inv1] = go([...A.slice(0, half)]),
            [second, inv2] = go([...A.slice(half, N)]),
            [third,  inv3] = merge(first, second);
        return [third, inv1 + inv2 + inv3];
    };
    let merge = (A, B, C = [], inv = 0) => {
        let M = A.length,
            N = B.length;
        let i = 0,
            j = 0;
        while (i < M && j < N)
            if (A[i] < B[j])
                C.push(A[i++]);
            else
                inv += M - i,      // ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
                C.push(B[j++]);
        C.push(...A.slice(i, M));
        C.push(...B.slice(j, N));
        return [C, inv];
    };
    return go(A);
};

let run = filename => {
    let A = [];
    require('fs').readFileSync(filename, 'utf-8').split(/\r?\n/).forEach(line => A.push(Number(line)));
    let [_, inv] = sort(A);
    return inv;
}

console.log(`problem3.5test.txt: ${run('problem3.5test.txt')}`);  // problem3.5test.txt: 28
console.log(`problem3.5.txt: ${run('problem3.5.txt')}`);          // problem3.5.txt: 2407905288

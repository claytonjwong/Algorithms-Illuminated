let random = (L, R) => Math.floor(Math.random() * (R + 1 - L) + L);  // +1 for L..R inclusive

let partition = (A, L, R) => {
    let i = L + 1,
        j = L + 1,
        k = random(L, R);
    [A[L], A[k]] = [A[k], A[L]];          // swap pivot A[k] with first element of subarray A[L]
    while (j <= R) {
        if (A[j] < A[L]) {                // maintain loop invariant A[i] < pivot < A[j]
            [A[i], A[j]] = [A[j], A[i]];
            ++i;
        }
        ++j;
    }
    [A[L], A[i - 1]] = [A[i - 1], A[L]];  // swap pivot A[L] with last value less-than pivot A[i - 1]
    return i - 1;
};

let rselect = (A, i, L, R) => {
    let k = partition(A, L, R);
    if (i == k)
        return A[k];  // 🎯 lucky guess
    if (i < k)
        R = k - 1;
    else
        L = k + 1;
    return rselect(A, i, L, R);
}

let run = (filename, i) => {
    let A = [];
    let LineByLine = require("n-readlines");
    let input = new LineByLine(filename);
    for (let line; line = input.next(); A.push(Number(line)));
    let N = A.length;
    return rselect(A, i - 1, 0, N - 1);  // -1 for 0-based indexing
};

console.log(`problem6.5test1.txt: ${run('problem6.5test1.txt', 5)}`);   // problem6.5test1.txt: 5469
console.log(`problem6.5test2.txt: ${run('problem6.5test2.txt', 50)}`);  // problem6.5test2.txt: 4715

#
# Merge Sort Inversions
#
# Input: array A of n distinct integers
# Output: the number of inversions of A
#
function go(A)
  N = length(A)
  if N < 2
    return A, 0
  end
  half = div(N, 2)
  first, inv1 = go(A[begin:half])
  second, inv2 = go(A[half+1:end])
  third, inv3 = merge(first, second)
  return third, inv1 + inv2 + inv3
end

function merge(A, B)
  C, inv = [], 0
  i, j, k = 1, 1, 1
  while i <= length(A) && j <= length(B)
    if A[i] < B[j]
      push!(C, A[i])
      i += 1
    else
      push!(C, B[j]); inv += length(A) - i + 1  # ⭐️ B[j] comes before all remaining A[i...], thus all remaining A[i...] are inversions
      j += 1
    end
    k += 1
  end
  append!(C, @view A[i:end])
  append!(C, @view B[j:end])
  return C, inv
end

function run(filename)
  input = Int[]
  open(filename, "r") do file
    for line in eachline(file)
      push!(input, parse(Int, strip(line)))
    end
  end
  _, inv = go(input)
  return inv
end

println(run("problem3.5test.txt"))  # 28
println(run("problem3.5.txt"))      # 2407905288

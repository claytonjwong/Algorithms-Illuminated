#
# Merge Sort
#
# Input: array A of n distinct integers
# Output: array with the same integers, sorted from smallest to largest
#
function go(A)
  N = length(A)
  if N < 2
    return A
  end
  half = div(N, 2)
  first = go(A[begin:half])
  second = go(A[half+1:end])
  return merge(first, second)
end

function merge(A, B)
  C = []
  i, j, k = 1, 1, 1
  while i <= length(A) && j <= length(B)
    if A[i] < B[j]
      push!(C, A[i])
      i += 1
    else
      push!(C, B[j])
      j += 1
    end
    k += 1
  end
  append!(C, @view A[i:end])
  append!(C, @view B[j:end])
  return C
end

println(go([5, 3, 8, 9, 1, 7, 0, 2, 6, 4]))  # Any[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# ➜  merge_sort git:(main) ✗ julia ./merge_sort.jl
# Any[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

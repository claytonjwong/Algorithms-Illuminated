#
# Recursive Integer Multiplication
#
# Input: two n-digit positive integers x and y
# Output: the product x * y
# Assumption: n is a power of 2
#
function go(x, y)
  n = length(string(x)) # assume the length of x and y is the same
  if n == 1
    return x * y
  end
  m = 10 ^ div(n, 2) # middle decimal value
  a, b = div(x, m), mod(x, m)
  c, d = div(y, m), mod(y, m)
  return 10^n * go(a, c) + 10^div(n, 2) * (go(a, d) + go(b, c)) + go(b, d)
end

x = 5678
y = 1234
println(go(x, y))

# ➜  rec_int_mult git:(main) ✗ julia ./main.jl
# 7006652

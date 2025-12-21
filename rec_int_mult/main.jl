#
# Recursive Integer Multiplication
#
# Input: two n-digit positive integers x and y
# Output: the product x * y
# Assumption: n is a power of 2
#
function go(x, y)
  n = min(length(string(x)), length(string(y)))
  if n == 1
    return x * y
  end
  m = 10 ^ div(n, 2) # middle decimal value
  a, b = div(x, m), mod(x, m)
  c, d = div(y, m), mod(y, m)
  ac = go(a, c)
  ad = go(a, d)
  bc = go(b, c)
  bd = go(b, d)
  return 10^n * ac + 10^div(n, 2) * (ad + bc) + bd
end

x = 5678
y = 1234
println(go(x, y))

# ➜  rec_int_mult git:(main) ✗ julia ./main.jl
# 7006652

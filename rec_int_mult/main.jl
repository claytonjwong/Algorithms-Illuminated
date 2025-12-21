#
# Recursive Integer Multiplication
#
# Input: two n-digit positive integers x and y
# Output: the product x * y
# Assumption: n is a power of 2
#
using Test, Random

function go(x, y)
  if x < 10 || y < 10
    return x * y
  end

  n = max(length(string(x)), length(string(y)))
  if isodd(n)
    n += 1
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

Random.seed!(123456789)

@testset "Recursive Integer Multiplication tests" begin
    for _ in 1:100
        n = rand((1, 2, 4, 8, 16))

        lo = 10^(n-1)
        hi = 10^n - 1

        x = rand(lo:hi)
        y = rand(lo:hi)

        expect, actual = x * y, go(x, y)
        @test expect == actual
        println("($x x $y)\nexpect: $expect\nactual: $actual\n")
    end
end

import math

# Compute prime factors
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

# grouping of 2x2s into 4
def fours(n):
    if n == 1:
        return [1]
    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4

    return factors + prime_factors(n)


# Compute radius of a point
def radius(n):
    # n = number of small circles
    if n == 1:
        return 1
    s = math.sin(math.pi / n)
    return s / (s + 1)


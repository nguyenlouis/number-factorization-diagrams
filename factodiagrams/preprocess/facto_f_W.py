#%%
def fermat(n):
    """Fermat decomposition method

    Let n be the number to factorize and q = E (\sqrt{N}). The idea is to find a and b such that n = a^2 - b^2 then N = (a+b)(ab) and if a exists then a \geqslant q + 1. We successively choose a = q + 1, a = q + 2, a = q + 3,… until there is an a such that a^2 - N is a square. If we find a decomposition as a difference of two squares, in other words if N = a^2 - b^2 then, a \geqslant E (\sqrt {N})+1 where E (\sqrt{N}) is the integer part of \sqrt{N}.

    :param n: number to decompose
    :type n: int

    :return: list of prime factors
    :rtype: list
    """
    if n&1==0:
        return [n>>1, 2]  # if n is even, return the solution
    x = lsqrt(n)
    if x*x==n:
        return [x, x]  #if n is already a perfect square, return the solution
    x += 1  # because we want the integer value immediately above the real square root
    while True:
        y2 = x*x-n
        y = lsqrt(y2)
        if y*y==y2:
            break  #if y2 is a perfect square, we have found a "good" y that goes with the x
        else:
            x += 1
    return [x-y, x+y]
#%%
from math import factorial
#%%
def wilson_factor(n):
    """Wilson decomposition method

    :param n: number to decompose
    :type n: int
    """
    return n > 1 and bool(n == 2 or
                          (n % 2 and (factorial(n - 1) + 1) % n == 0))
 


# %%

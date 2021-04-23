def fermat_factors(x):
    fermat_factors = []
    i = 2
    s = int(x ** 0.5)
    while i < s:
        if x % i == 0:
            fermat_factors.append(i)
            x = int(x / i)
            s = int(x ** 0.5)
        i += 1
    fermat_factors.append(x)
    return fermat_factors
#%%
from math import factorial
 
def wilson_factor(n):
    return n > 1 and bool(n == 2 or
                          (n % 2 and (factorial(n - 1) + 1) % n == 0))
 


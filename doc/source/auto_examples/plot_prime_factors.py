"""
Factorization examples
=========================

This page provides examples using the methods prime factors and Pollard Rho.
"""
# %%
# prime factors method
# ------------------------
import factodiagrams
factorisation = factodiagrams.preprocess.Factorisation.Factorization()
print(factorisation.prime_factors(70))

###############################################################################

# %%
# Pollard Rho  method
# ------------------------
import factodiagrams
factorisation = factodiagrams.preprocess.Factorisation.Factorization()
print(factorisation.pollardrho(70))
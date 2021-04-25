"""
Diagrams generating example
===========================

"""
# %%
# Diagram generating using Prime factors
# ------------------------

import factodiagrams

factorisation = factodiagrams.preprocess.Factorisation.Factorization()
factorisation.draw_factor(70,"prime_factors",True,True)


# %%
# Diagram generating using Pollard Rho
# ------------------------

import factodiagrams

factorisation = factodiagrams.preprocess.Factorisation.Factorization()
factorisation.draw_factor(70,"pollardrho",True,True)

"""
Poster Generator
=========================

"""

import factodiagrams

factorisation = factodiagrams.preprocess.Factorisation.Factorization()
factorisation.draw_factor_poster(list(range(1,129)),"prime_factors",10)
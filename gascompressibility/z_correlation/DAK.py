import numpy as np

"""
Dranchuk, P.M., and Abou-Kassem, J.H.: "Calculation of z-Factors for Natural Gases Using Equations of State," 
Journal of Canadian Petroleum Technology (1975)

https://onepetro.org/JCPT/article-abstract/doi/10.2118/75-03-03
"""


def DAK(z=None, Pr=None, Tr=None):
    A1 = 0.3265
    A2 = -1.0700
    A3 = -0.5339
    A4 = 0.01569
    A5 = -0.05165
    A6 = 0.5475
    A7 = -0.7361
    A8 = 0.1844
    A9 = 0.1056
    A10 = 0.6134
    A11 = 0.7210

    return 1 + (
            A1 +
            A2 / Tr +
            A3 / Tr ** 3 +
            A4 / Tr ** 4 +
            A5 / Tr ** 5
    ) * (0.27 * Pr) / (z * Tr) + (
            A6 +
            A7 / Tr +
            A8 / Tr ** 2
    ) * ((0.27 * Pr) / (z * Tr)) ** 2 - A9 * (
            A7 / Tr +
            A8 / Tr ** 2
    ) * ((0.27 * Pr) / (z * Tr)) ** 5 + A10 * (
            1 +
            A11 * ((0.27 * Pr) / (z * Tr)) ** 2
    ) * (
            ((0.27 * Pr) / (z * Tr)) ** 2 /
            Tr ** 3
    ) * np.exp(-A11 * ((0.27 * Pr) / (z * Tr)) ** 2) - z

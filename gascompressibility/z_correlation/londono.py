import numpy as np

"""
Londono, F.E., Archer, R.A., and Blasingame, T.A.: "Simplified Correlations for Hydrocarbon Gas Viscosity and Gas 
Density — Validation and Correlation of Behavior Using a Large-Scale Database," paper SPE 75721 ()

https://onepetro.org/SPEGTS/proceedings/02GTS/All-02GTS/SPE-75721-MS/135705
"""


def londono(z=None, Pr=None, Tr=None):

    A1 = 0.3024696
    A2 = -1.046964
    A3 = -0.1078916
    A4 = -0.7694186
    A5 = 0.1965439
    A6 = 0.6527819
    A7 = -1.118884
    A8 = 0.3951957
    A9 = 0.09313593
    A10 = 0.8483081
    A11 = 0.7880011

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
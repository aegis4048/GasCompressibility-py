import numpy as np

"""
Kareem, L.A., Iwalewa, T.M., and Marhoun, M.al-.,: "CNew explicit correlation for the compressibility factor of natural gas: linearized z-factor isotherms," 
Journal of Petroleum Exploration and Production Technology (2016)

https://link.springer.com/article/10.1007/s13202-015-0209-3
"""


def kareem(Pr=None, Tr=None):

    a1 = 0.317842
    a2 = 0.382216
    a3 = -7.768354
    a4 = 14.290531
    a5 = 0.000002
    a6 = -0.004693
    a7 = 0.096254
    a8 = 0.166720
    a9 = 0.966910
    a10 = 0.063069
    a11 = -1.966847
    a12 = 21.0581
    a13 = -27.0246
    a14 = 16.23
    a15 = 207.783
    a16 = -488.161
    a17 = 176.29
    a18 = 1.88453
    a19 = 3.05921

    t = 1 / Tr

    A = a1 * t * np.exp(a2 * (1 - t) ** 2) * Pr
    B = a3 * t + a4 * t ** 2 + a5 * t ** 6 * Pr ** 6
    C = a9 + a8 * t * Pr + a7 * t ** 2 * Pr ** 2 + a6 * t ** 3 * Pr ** 3
    D = a10 * t * np.exp(a11 * (1 - t) ** 2)
    """
    Notes: 
    When Pr = 3.0153, Tr = 1.6155, the calulated values for E, F, and G does not agree with the sample calculation
    presented in the original paper. 
    
    Python codes:        Paper sample calculation:
    E =  6.52959         E = 6.56232
    F =  -16.61537       F = -17.08860
    G =  3.77819         G = 3.80545
    
    After many checks and hand-calculation, I concluded that the author made some mistakes while writing up his sample
    calculation steps. 
    
    Long-story short: this python implementation of the model is safe to use. 
    """
    E = a12 * t + a13 * t ** 2 + a14 * t ** 3
    F = a15 * t + a16 * t ** 2 + a17 * t ** 3
    G = a18 + a19 * t

    y = (D * Pr) / (
            (1 + A ** 2) / C - (A ** 2 * B) / C ** 3
    )

    return (D * Pr * (1 + y + y ** 2 - y ** 3)) / ((D * Pr + E * y ** 2 - F * y ** G) * (1 - y) ** 3)

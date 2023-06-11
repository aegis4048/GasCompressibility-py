import numpy as np

"""
Hall, K.R., and Yarborough, L.: "A new equation of state for Z-factor calculations," Oil and Gas Journal (1973)

https://www.researchgate.net/publication/284299884_A_new_equation_of_state_for_Z-factor_calculations
"""


def hall_yarborough(z=None, Pr=None, Tr=None):

    t = 1 / Tr

    A1 = 0.06125 * t * np.exp(-1.2 * (1 - t) ** 2)
    A2 = 14.76 * t - 9.76 * t ** 2 + 4.58 * t ** 3
    A3 = 90.7 * t - 242.2 * t ** 2 + 42.4 * t ** 3
    A4 = 2.18 + 2.82 * t

    ((A1 * Pr) / z)

    return -A1 * Pr \
        + (((A1 * Pr) / z) + ((A1 * Pr) / z) ** 2 + ((A1 * Pr) / z) ** 3 - ((A1 * Pr) / z) ** 4)/(1 - ((A1 * Pr) / z)) ** 3 \
        - A2 * ((A1 * Pr) / z) ** 2 + A3 * ((A1 * Pr) / z) ** A4


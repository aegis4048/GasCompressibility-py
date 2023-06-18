def calc_Fahrenheit_to_Rankine(T):
    if T is None:
        raise TypeError("Missing a required argument, 'T' (gas temperature, °F)")
    return T + 459.67


def calc_psig_to_psia(P):
    if P is None:
        raise TypeError("Missing a required argument, 'P' (gas pressure, psig)")
    return P + 14.7


def calc_Fahrenheit_to_Rankine(T):
    if T is None:
        raise TypeError("Missing a required argument, 'T' (gas temperature, °F)")
    return T + 459.67
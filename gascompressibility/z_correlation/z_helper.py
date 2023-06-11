from scipy import optimize

from gascompressibility.z_correlation.DAK import DAK
from gascompressibility.z_correlation.hall_yarborough import hall_yarborough
from gascompressibility.z_correlation.londono import londono
from gascompressibility.z_correlation.kareem import kareem


models = {
    'DAK': DAK,
    'hall_yarborough': hall_yarborough,
    'londono': londono,
    'kareem': kareem,
}
models_ks = '["DAK", "hall_yarborough", "londono", "kareem"]'


def get_z_model(model='DAK'):

    if model not in models.keys():
        raise KeyError(
            'model "%s" is not implemented. Choose from the list of available models: %s' % (model, models_ks)
        )

    return models[model]


def calc_Z(Pr=None, Tr=None, model='DAK', guess=0.9123676532, newton_kwargs=None):

    z_model = get_z_model(model=model)

    # Explicit models
    if model in ['kareem']:

        if guess != 0.9123676532:
            raise TypeError('calc_Z(model="%s") got an unexpected argument "guess"' % model)
        if newton_kwargs is not None:
            raise TypeError('calc_Z(model="%s") got an unexpected argument "newton_kwargs"' % model)

        Z = z_model(Pr=Pr, Tr=Tr)

    # Implicit models
    else:
        if newton_kwargs is None:
            Z = optimize.newton(z_model, guess, args=(Pr, Tr))
        else:
            Z = optimize.newton(z_model, guess, args=(Pr, Tr), **newton_kwargs)

    return Z


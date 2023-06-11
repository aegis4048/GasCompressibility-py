from scipy import optimize

from gascompressibility.z_correlation.DAK import DAK
from gascompressibility.z_correlation.hall_yarborough import hall_yarborough
from gascompressibility.z_correlation.londono import londono


models = {
    'DAK': DAK,
    'hall_yarborough': hall_yarborough,
    'londono': londono,
}
models_ks = '["DAK", "hall_yarborough", "londono"]'


def get_z_model(model='DAK'):

    if model not in models.keys():
        raise KeyError(
            'model "%s" is not implemented. Choose from the list of available models: %s' % (model, models_ks))

    return models[model]


def calc_Z(Pr=None, Tr=None, guess=0.9, model='DAK', newton_kwargs=None):

    z_model = get_z_model(model=model)

    if newton_kwargs is None:
        Z = optimize.newton(z_model, guess, args=(Pr, Tr))
    else:
        Z = optimize.newton(z_model, guess, args=(Pr, Tr), **newton_kwargs)

    return Z


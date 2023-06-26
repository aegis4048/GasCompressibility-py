from scipy import optimize

from gascompressibility.z_correlation.DAK import DAK
from gascompressibility.z_correlation.hall_yarborough import hall_yarborough
from gascompressibility.z_correlation.londono import londono
from gascompressibility.z_correlation.kareem import kareem
from gascompressibility.pseudocritical import piper
from gascompressibility.pseudocritical import sutton


models = {
    'DAK': DAK,
    'hall_yarborough': hall_yarborough,
    'londono': londono,
    'kareem': kareem,
}

zmodels_ks = '["DAK", "hall_yarborough", "londono", "kareem"]'
pmodels_ks = '["sutton", "piper"]'


def get_guess_constant():
    return 0.900000765321234598723486


def get_z_model(model='DAK'):

    if model not in models.keys():
        raise KeyError(
            'Z-factor model "%s" is not implemented. Choose from the list of available models: %s' % (model, zmodels_ks)
        )

    return models[model]


def calc_Z(sg=None, P=None, T=None, H2S=None, CO2=None, N2=None, Pr=None, Tr=None, pmodel='piper', zmodel='DAK',
           guess=get_guess_constant(), newton_kwargs=None, ps_props=False, ignore_conflict=False, **kwargs):

    z_model = get_z_model(model=zmodel)

    # Pr and Tr are already provided:
    if Pr is not None and Tr is not None:

        # Explicit models
        if zmodel in ['kareem']:
            if guess != get_guess_constant():
                raise KeyError('calc_Z(model="%s") got an unexpected argument "guess"' % zmodel)
            if newton_kwargs is not None:
                raise KeyError('calc_Z(model="%s") got an unexpected argument "newton_kwargs"' % zmodel)
            Z = z_model(Pr=Pr, Tr=Tr)

        # Implicit models: they require iterative convergence
        else:
            if newton_kwargs is None:
                Z = optimize.newton(z_model, guess, args=(Pr, Tr))
            else:
                Z = optimize.newton(z_model, guess, args=(Pr, Tr), **newton_kwargs)

        if ps_props is True:
            return {'z': Z, 'Pr': Pr, 'Tr': Tr}
        else:
            return Z





    # calculate Pr and Tr with pseudo-critical models if they are not provided
    if pmodel == 'piper':

        pc_instance = piper.piper()
        Tr, Pr = pc_instance._initialize_Tr_and_Pr(sg=sg, P=P, T=T, Tr=Tr, Pr=Pr, H2S=H2S, CO2=CO2, N2=N2, ignore_conflict=ignore_conflict, **kwargs)

        #Pr = pc_instance.calc_Pr(sg=sg, P=P, H2S=H2S, CO2=CO2, N2=N2, **kwargs)
        #Tr = pc_instance.calc_Tr(sg=sg, T=T, H2S=H2S, CO2=CO2, N2=N2, **kwargs)

    elif pmodel == 'sutton':

        if N2 is not None:
            raise KeyError('pmodel="sutton" does not support N2 as input. Set N2=None')

        pc_instance = sutton.sutton()
        Tr, Pr = pc_instance._initialize_Tr_and_Pr(sg=sg, P=P, T=T, Tr=Tr, Pr=Pr, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict, **kwargs)

        #Pr = pc_instance.calc_Pr(sg=sg, P=P, H2S=H2S, CO2=CO2, **kwargs)
        #Tr = pc_instance.calc_Tr(sg=sg, T=T, H2S=H2S, CO2=CO2, **kwargs)

    else:
        raise KeyError(
            'Pseudo-critical model "%s" is not implemented. Choose from the list of available models: %s' % (pmodel, pmodels_ks)
        )

    # Explicit models
    if zmodel in ['kareem']:
        if guess != get_guess_constant():
            raise KeyError('calc_Z(model="%s") got an unexpected argument "guess"' % zmodel)
        if newton_kwargs is not None:
            raise KeyError('calc_Z(model="%s") got an unexpected argument "newton_kwargs"' % zmodel)
        Z = z_model(Pr=Pr, Tr=Tr)

    # Implicit models: they require iterative convergence
    else:
        if newton_kwargs is None:
            Z = optimize.newton(z_model, guess, args=(Pr, Tr))
        else:
            Z = optimize.newton(z_model, guess, args=(Pr, Tr), **newton_kwargs)

    if ps_props is True:

        ps_props = {'z': Z}
        ps_props.update(pc_instance.ps_props)
        ps_props['Tr'] = Tr
        ps_props['Pr'] = Pr

        return ps_props
    else:
        return Z



from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

from gascompressibility.z_correlation.DAK import DAK
from gascompressibility.z_correlation.hall_yarborough import hall_yarborough
from gascompressibility.z_correlation.londono import londono
from gascompressibility.z_correlation.kareem import kareem
from gascompressibility.pseudocritical import Piper
from gascompressibility.pseudocritical import Sutton


models = {
    'DAK': DAK,
    'hall_yarborough': hall_yarborough,
    'londono': londono,
    'kareem': kareem,
}
MODEL_RANGES = {
    'DAK': {
        'Tr': (1, 3),
        'Pr': (0.2, 30)
    },
    'hall_yarborough': {
        'Tr': (1, 3),
        'Pr': (0.2, 20.5)
    },
    'londono': {
        'Tr': (1, 3),
        'Pr': (0.2, 30)
    },
    'kareem': {
        'Tr': (1, 3),
        'Pr': (0.2, 15)
    },
}


def _check_working_Pr_Tr_range(Pr, Tr, zmodel_str):
    Pr_is_in_range = np.logical_and(Pr >= MODEL_RANGES[zmodel_str]['Pr'][0], Pr <= MODEL_RANGES[zmodel_str]['Pr'][1]).all()
    Tr_is_in_range = np.logical_and(Tr >= MODEL_RANGES[zmodel_str]['Tr'][0], Tr <= MODEL_RANGES[zmodel_str]['Tr'][1]).all()

    #print(Pr >= MODEL_RANGES[zmodel_str]['Pr'][0], Pr <= MODEL_RANGES[zmodel_str]['Pr'][1])

    return Pr_is_in_range and Tr_is_in_range


zmodels_ks = '["DAK", "hall_yarborough", "londono", "kareem"]'
pmodels_ks = '["Sutton", "Piper"]'


def _get_guess_constant():
    return 0.900000765321234598723486


def _get_z_model(model='DAK'):

    if model not in models.keys():
        raise KeyError(
            'Z-factor model "%s" is not implemented. Choose from the list of available models: %s' % (model, zmodels_ks)
        )

    return models[model]


def _construct_guess_list_order(guess):
    """reorder t in an order closest to the provided guess"""
    t = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    reordered = [guess]
    count = 0
    while len(t) > 0:
        match = min(t, key=lambda x: abs(x - guess))
        t.pop(t.index(match))
        reordered.append(match)
        count += 1
    return list(set(reordered))

def _calc_z_explicit_implicit_helper(Pr, Tr, zmodel_func, zmodel_str, guess, newton_kwargs, smart_guess):

    if guess is None:
        if Pr < 15:
            guess = 0.9
        else:
            # Todo: z-factor after Pr shows linear trend. So fit a linear regression model for each TR and get better estimate of initial guess for Pr range greater than 15, which is the working range of the explicit "kareem" model
            guess = 2

    maxiter = 50
    Z = None
    smart_guess_model = 'kareem'

    # Explicit models
    if zmodel_str in ['kareem']:
        Z = zmodel_func(Pr=Pr, Tr=Tr)

    # Implicit models: they require iterative convergence
    else:

        worked = False

        if smart_guess:
            if _check_working_Pr_Tr_range(Pr, Tr, smart_guess_model):
                guess_zmodel_func = _get_z_model(model=smart_guess_model)
                guess_ = guess_zmodel_func(Pr=Pr, Tr=Tr)
                guesses = [guess_] + [guess] + _construct_guess_list_order(guess)
            else:
                guesses = [guess] + _construct_guess_list_order(guess)
                #print('Pr=', Pr, 'Tr=', Tr)
                #print(guesses)

        else:
            guesses = _construct_guess_list_order(guess)

        for guess_ in guesses:
            try:
                if newton_kwargs is None:  # apply default value of max iteration if newton_kwargs is not provided
                    Z = optimize.newton(zmodel_func, guess_, args=(Pr, Tr), maxiter=maxiter)
                else:
                    if 'maxiter' in newton_kwargs:
                        Z = optimize.newton(zmodel_func, guess_, args=(Pr, Tr), **newton_kwargs)
                    else:
                        newton_kwargs.pop('maxiter', None)
                        Z = optimize.newton(zmodel_func, guess_, args=(Pr, Tr), maxiter=maxiter, **newton_kwargs)
                worked = True
            except:
                pass
            if worked:
                break

        if not worked:
            raise RuntimeError("Failed to converge")

    return Z



def calc_z(sg=None, P=None, T=None, H2S=None, CO2=None, N2=None, Pr=None, Tr=None, pmodel='Piper', zmodel='DAK',
           guess=None, newton_kwargs=None, smart_guess=None, ps_props=False, ignore_conflict=False, **kwargs):
    """
    Calculates the gas compressibility factor, :math:`Z`.

    **Basic (most common) usage:**

    >>> import gascompressibility as gc
    >>>
    >>> gc.calc_z(sg=0.7, T=75, P=2010)
    0.7366562810878984


    **In presence of significant non-hydrocarbon impurities:**

    >>> gc.calc_z(sg=0.7, T=75, P=2010, CO2=0.1, H2S=0.07, N2=0.05)
    0.7765149771306533

    **When pseudo-critical properties are known (not common):**

    >>> gc.calc_z(Pr=1.5, Tr=1.5)
    0.859314380561347

    **Picking correlation models of your choice**

    >>> gc.calc_z(sg=0.7, T=75, P=2010, zmodel='kareem', pmodel='Sutton')
    0.7150183342641309

    **Returning all associated pseudo-critical properties computed**

    >>> gc.calc_z(sg=0.7, T=75, P=2010, ps_props=True)
    {'z': 0.7366562810878984, 'Tpc': 371.4335560823552, 'Ppc': 660.6569792741872, 'J': 0.56221847, 'K': 14.450840999999999, 'Tr': 1.4394768357478496, 'Pr': 3.0646766226921294}



    Parameters
    ----------
    sg : float
        specific gravity of gas (dimensionless)
    P : float
        pressure of gas (psig)
    T : float
        temperature of gas (°F)
    H2S : float
        mole fraction of H2S (dimensionless)
    CO2 : float
        mole fraction of CO2 (dimensionless)
    N2 : float
        mole fraction of N2 (dimensionless). Available only when ``pmodel='Piper'`` (default)
    Pr : float
        pseudo-reduced pressure, Pr (psia)
    Tr : float
        pseudo-reduced temperature, Tr (°R)
    pmodel : str
        choice of a pseudo-critical model. Accepted inputs: ``'Sutton'`` | ``'Piper'``.

        See Also
        --------
        :doc:`pseudocritical`
        ~sutton.Sutton
        ~piper.Piper

    zmodel : str
        choice of a z-correlation model. Accepted inputs are: ``'DAK'`` | ``'hall_yarborough'`` | ``'londono'`` |``'kareem'``
    guess : float
        initial guess of z-value for z-correlation models using iterative convergence (``'DAK'`` | ``'hall_yarborough'`` | ``'londono'``).
    newton_kwargs :dict
        dictonary of keyword-arguments used by ``scipy.optimize.newton`` method for z-correlation models that use
        iterative convergence (``'DAK'`` | ``'hall_yarborough'`` | ``'londono'``).

        >>> gc.calc_z(sg=0.7, P=2010, T=75, newton_kwargs={'maxiter': 10000})
        0.7366562810878984

        See Also
        ----------
        `scipy.optimize.newton <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.newton.html>`_.

    ps_props : bool
        set this to `True` to return a dictionary of all associated pseudo-critical properties computed during calculation
        of the z-factor.
    ignore_conflict : bool
        set this to True to override calculated variables with input keyword arguments.
    **kwargs
        optional kwargs used by psueodo-critical models (``'Sutton'`` | ``'Piper'``) that allow direct calculation of
        z-factor from pseudo-critical properties instead of specific gravity correlation. Consider the below code example
        that uses ``pmodel='Sutton'``:

        >>> gc.calc_z(Ppc=663, e_correction=21, Tpc=377.59, P=2010, T=75, pmodel='Sutton', ignore_conflict=True)
        0.7720015496503527

        ``Ppc``, ``e_correction``, ``Tpc`` aren't default parameters defined in ``gascompressibility.calc_z``,
        but they can be optionally passed into Sutton's :ref:`calc_Pr <Sutton.calc_Pr>` and :ref:`calc_Tr <Sutton.calc_Tr>`
        methods if you already know these values (not common) and would like to compute the z-factor from these instead
        of using specific gravity correlation.

        Danger
        -------
        It is not recommended to the pass optional ``**kwargs`` unless you really know what you are doing. 99.9% of the users
        should not be using this feature.

    Returns
    -------
    float
        gas compressibility factor, :math:`Z` (dimensionless)

    """

    if zmodel in ['kareem']:
        if guess is not None:
            raise KeyError('calc_z(model="%s") got an unexpected argument "guess"' % zmodel)
        if newton_kwargs is not None:
            raise KeyError('calc_z(model="%s") got an unexpected argument "newton_kwargs"' % zmodel)
        if smart_guess is not None:
            raise KeyError('calc_z(model="%s") got an unexpected argument "smart_guess"' % zmodel)
    else:
        if guess is None:
            if Pr < 15:
                guess = 0.9
            else:
                # Todo: z-factor after Pr shows linear trend. So fit a linear regression model for each TR and get better estimate of initial guess for Pr range greater than 15, which is the working range of the explicit "kareem" model
                guess = 2
        if smart_guess is None:
            smart_guess = True

    z_model = _get_z_model(model=zmodel)

    # Pr and Tr are already provided:
    if Pr is not None and Tr is not None:
        Z = _calc_z_explicit_implicit_helper(Pr, Tr, z_model, zmodel, guess, newton_kwargs, smart_guess)
        if ps_props is True:
            ps_props = {'z': Z, 'Pr': Pr, 'Tr': Tr}
            return ps_props
        else:
            return Z

    # Pr and Tr are NOT provided:
    if pmodel == 'Piper':
        pc_instance = Piper()
        Tr, Pr = pc_instance._initialize_Tr_and_Pr(sg=sg, P=P, T=T, Tr=Tr, Pr=Pr, H2S=H2S, CO2=CO2, N2=N2, ignore_conflict=ignore_conflict, **kwargs)
    elif pmodel == 'Sutton':
        if N2 is not None:
            raise KeyError('pmodel="Sutton" does not support N2 as input. Set N2=None')
        pc_instance = Sutton()
        Tr, Pr = pc_instance._initialize_Tr_and_Pr(sg=sg, P=P, T=T, Tr=Tr, Pr=Pr, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict, **kwargs)
    else:
        raise KeyError(
            'Pseudo-critical model "%s" is not implemented. Choose from the list of available models: %s' % (pmodel, pmodels_ks)
        )

    Z = _calc_z_explicit_implicit_helper(Pr, Tr, z_model, zmodel, guess, newton_kwargs, smart_guess)

    if ps_props is True:
        ps_props = {'z': Z}
        ps_props.update(pc_instance.ps_props)
        ps_props['Tr'] = Tr
        ps_props['Pr'] = Pr
        return ps_props
    else:
        return Z


def quickstart(zmodel='DAK', xmax=30, smart_guess=None, guess=None):

    """
    Generates a plot

    Returns
    -------
    fig : `Figure <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html>`_
        Matplotlib figure object
    ax : `Axis <https://matplotlib.org/stable/api/axis_api.html#axis-objects>`_

    """

    xmax = xmax
    Prs = np.linspace(0.1, xmax, xmax * 10 + 1)
    Prs = np.array([round(Pr, 1) for Pr in Prs])

    Trs = np.array([1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0])

    results = {Tr: {
        'Pr': np.array([]),
        'Z': np.array([])
    } for Tr in Trs}

    for Tr in Trs:
        for Pr in Prs:
            if zmodel == 'kareem':
                z = calc_z(Tr=Tr, Pr=Pr, zmodel=zmodel, smart_guess=smart_guess, guess=guess)
            else:
                z = calc_z(Tr=Tr, Pr=Pr, zmodel=zmodel, newton_kwargs={'maxiter': 50}, smart_guess=smart_guess, guess=guess)
            results[Tr]['Z'] = np.append(results[Tr]['Z'], [z], axis=0)
            results[Tr]['Pr'] = np.append(results[Tr]['Pr'], [Pr], axis=0)

    label_fontsize = 12

    fig, ax = plt.subplots(figsize=(8, 5))
    for Tr in Trs:

        Zs = results[Tr]['Z']
        idx_min = np.where(Zs == min(Zs))

        p = ax.plot(Prs, Zs)
        if Tr == 1.05:
            t = ax.text(Prs[idx_min] - 0.5, min(Zs) - 0.005, '$T_{r}$ = 1.05', color=p[0].get_color())
            t.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white', pad=1))
        else:
            t = ax.text(Prs[idx_min] - 0.2, min(Zs) - 0.005, Tr, color=p[0].get_color())
            t.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white', pad=1))

    ax.set_xlim(0, xmax)
    #ax.set_ylim(0, 2.5)
    ax.minorticks_on()
    ax.grid(alpha=0.5)
    ax.grid(visible=True, which='minor', alpha=0.1)
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)

    ax.set_ylabel('Compressibility Factor, $Z$', fontsize=label_fontsize)
    ax.set_xlabel('Pseudo-Reduced Pressure, $P_{r}$', fontsize=label_fontsize)
    ax.text(0.57, 0.08, '$T_{r}$ = Pseudo-Reduced Temperature', fontsize=11, transform=ax.transAxes,
            bbox=dict(facecolor='white'))
    ax.text(0.05, 0.9, "zmodel = '%s'" % zmodel, fontsize=11, transform=ax.transAxes,
            bbox=dict(facecolor='white'), va='center', ha='left')

    def setbold(txt):
        return ' '.join([r"$\bf{" + item + "}$" for item in txt.split(' ')])

    ax.set_title(setbold('Real Gas Law Compressibility Factor - Z') + ", computed with GasCompressiblityFactor-py ",
                 fontsize=12, pad=10, x=0.445, y=1.06)
    ax.annotate('', xy=(-0.09, 1.05), xycoords='axes fraction', xytext=(1.05, 1.05),
                arrowprops=dict(arrowstyle="-", color='k'))

    fig.tight_layout()

    return results, fig, ax


#  gc.calc_z(Pr=2.1, Tr=1.05, zmodel='londono', newton_kwargs={'maxiter': 100000}, guess=0.5)
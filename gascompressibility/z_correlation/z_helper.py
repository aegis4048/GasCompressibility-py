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


def _calc_z_explicit_implicit_helper(Pr, Tr, zmodel_func, zmodel_str, guess, newton_kwargs, ps_props):

    maxiter = 1000

    # Explicit models
    if zmodel_str in ['kareem']:
        if guess != _get_guess_constant():
            raise KeyError('calc_z(model="%s") got an unexpected argument "guess"' % zmodel_str)
        if newton_kwargs is not None:
            raise KeyError('calc_z(model="%s") got an unexpected argument "newton_kwargs"' % zmodel_str)
        Z = zmodel_func(Pr=Pr, Tr=Tr)

    # Implicit models: they require iterative convergence
    else:
        if newton_kwargs is None:
            Z = optimize.newton(zmodel_func, guess, args=(Pr, Tr), maxiter=maxiter)
        else:
            # work around to set default maxiter = 1000, unless use specifies it
            if newton_kwargs.pop('maxiter', None) is None:
                Z = optimize.newton(zmodel_func, guess, args=(Pr, Tr), maxiter=1000, **newton_kwargs)
            else:
                Z = optimize.newton(zmodel_func, guess, args=(Pr, Tr), **newton_kwargs)

    return Z


def calc_z(sg=None, P=None, T=None, H2S=None, CO2=None, N2=None, Pr=None, Tr=None, pmodel='Piper', zmodel='DAK',
           guess=_get_guess_constant(), newton_kwargs=None, ps_props=False, ignore_conflict=False, **kwargs):
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
        choice of a pseudo-critical model. Accepted inputs are: ``'Sutton'`` and ``'Piper'``.

        See Also
        --------
        :doc:`pseudocritical`
        Sutton.Sutton
        Piper.Piper

    zmodel : str
        choice of a z-correlation model. Accepted inputs are: ``'DAK'``, ``'hall_yarborough'``, ``'londono'``, and ``'kareem'``
    guess : float
        initial guess of z-value for z-correlation models using iterative convergence (``'DAK'``, ``'hall_yarborough'``,
        and ``'londono'``).
    newton_kwargs
    ps_props
    ignore_conflict
    kwargs

    Returns
    -------
    bool
        True if successful, False otherwise.

        The return type is not optional. The ``Returns`` section may span
        multiple lines and paragraphs. Following lines should be indented to
        match the first line of the description.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises
    ------
    AttributeError
        The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
    ValueError
        If `param2` is equal to `param1`.


    """
    z_model = _get_z_model(model=zmodel)

    # Pr and Tr are already provided:
    if Pr is not None and Tr is not None:

        # Explicit models
        Z = _calc_z_explicit_implicit_helper(Pr, Tr, z_model, zmodel, guess, newton_kwargs, ps_props)
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

    Z = _calc_z_explicit_implicit_helper(Pr, Tr, z_model, zmodel, guess, newton_kwargs, ps_props)

    if ps_props is True:
        ps_props = {'z': Z}
        ps_props.update(pc_instance.ps_props)
        ps_props['Tr'] = Tr
        ps_props['Pr'] = Pr
        return ps_props
    else:
        return Z

def quickstart():

    xmax = 8
    Prs = np.linspace(0, xmax, xmax * 10 + 1)
    Prs = np.array([round(Pr, 1) for Pr in Prs])

    Trs = np.array([1.05, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0])

    results = {Tr: {
        'Pr': np.array([]),
        'Z': np.array([])
    } for Tr in Trs}

    for Tr in Trs:
        for Pr in Prs:
            z = calc_z(Tr=Tr, Pr=Pr)
            results[Tr]['Z'] = np.append(results[Tr]['Z'], [z], axis=0)
            results[Tr]['Pr'] = np.append(results[Tr]['Pr'], [Pr], axis=0)

    label_fontsize = 12

    fig, ax = plt.subplots(figsize=(8, 5))
    for Tr in Trs:

        Zs = results[Tr]['Z']
        idx_min = np.where(Zs == min(Zs))

        p = ax.plot(Prs, Zs)
        if Tr == 1.05:
            t = ax.text(Prs[idx_min] - 0.5, min(Zs) - 0.005, '$T_{r}$ = 1.2', color=p[0].get_color())
            t.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white', pad=1))
        else:
            t = ax.text(Prs[idx_min] - 0.2, min(Zs) - 0.005, Tr, color=p[0].get_color())
            t.set_bbox(dict(facecolor='white', alpha=0.9, edgecolor='white', pad=1))

    ax.set_xlim(0, xmax)
    ax.minorticks_on()
    ax.grid(alpha=0.5)
    ax.grid(visible=True, which='minor', alpha=0.1)
    ax.spines.top.set_visible(False)
    ax.spines.right.set_visible(False)

    ax.set_ylabel('Compressibility Factor, $Z$', fontsize=label_fontsize)
    ax.set_xlabel('Pseudo-Reduced Pressure, $P_{r}$', fontsize=label_fontsize)
    ax.text(0.57, 0.08, '$T_{r}$ = Pseudo-Reduced Temperature', fontsize=11, transform=ax.transAxes,
            bbox=dict(facecolor='white'))

    def setbold(txt):
        return ' '.join([r"$\bf{" + item + "}$" for item in txt.split(' ')])

    ax.set_title(setbold('Real Gas Law Compressibility Factor - Z') + ", computed with GasCompressiblityFactor-py ",
                 fontsize=12, pad=10, x=0.445, y=1.06)
    ax.annotate('', xy=(-0.09, 1.05), xycoords='axes fraction', xytext=(1.05, 1.05),
                arrowprops=dict(arrowstyle="-", color='k'))

    fig.tight_layout()

    return results, fig, ax

quickstart()
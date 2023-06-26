import numpy as np
import matplotlib.pyplot as plt
import inspect

from gascompressibility.utilities.utilities import calc_Fahrenheit_to_Rankine
from gascompressibility.utilities.utilities import calc_psig_to_psia

"""
This is a piper module
"""


class piper(object):
    """
    An example docstring for a class definition.
    """

    def __init__(self):

        self.mode = 'piper'
        self._check_invalid_mode(self.mode)  # prevent user modification of self.mode

        self.sg = None
        self.T_f = None
        self.T = None
        self.P = None
        self.H2S = None
        self.CO2 = None
        self.N2 = None

        self.Pc_H2S = 1306
        self.Tc_H2S = 672.3
        self.Pc_CO2 = 1071
        self.Tc_CO2 = 547.5
        self.Pc_N2 = 492.4
        self.Tc_N2 = 227.16

        self.Tpc = None
        self.Ppc = None
        self.J = None
        self.K = None
        self.Tr = None
        self.Pr = None

        self.ps_props = {
            'Tpc': self.Tpc,
            'Ppc': self.Ppc,
            'J': self.J,
            'K': self.K,
            'Tr': self.Tr,
            'Pr': self.Pr,
        }

        self._first_caller_name = None
        self._first_caller_keys = {}
        self._first_caller_kwargs = {}
        self._first_caller_is_saved = False

    def __str__(self):
        return str(self.ps_props)

    def __repr__(self):
        return str(self.ps_props)

    def calc_J(self, sg=None, H2S=None, CO2=None, N2=None):

        """
        Calculates the Stewart-Burkhardt-VOO parameter J, (°R/psia)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)

        Returns
        -------
        float
            SBV parameter, J, (°R/psia)
        """


        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self._initialize_H2S(H2S)
        self._initialize_CO2(CO2)
        self._initialize_N2(N2)
        self.J = 0.11582 \
                 - 0.45820 * self.H2S * (self.Tc_H2S / self.Pc_H2S) \
                 - 0.90348 * self.CO2 * (self.Tc_CO2 / self.Pc_CO2) \
                 - 0.66026 * self.N2 * (self.Tc_N2 / self.Pc_N2) \
                 + 0.70729 * self.sg \
                 - 0.099397 * self.sg ** 2
        self.ps_props['J'] = self.J
        return self.J

    def calc_K(self, sg=None, H2S=None, CO2=None, N2=None):
        """
        Calculates the Stewart-Burkhardt-VOO parameter K, (°R/psia^0.5)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)

        Returns
        -------
        float
            SBV parameter, K, (°R/psia^0.5)
        """

        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self._initialize_H2S(H2S)
        self._initialize_CO2(CO2)
        self._initialize_N2(N2)
        self.K = 3.8216 \
                 - 0.06534 * self.H2S * (self.Tc_H2S / np.sqrt(self.Pc_H2S)) \
                 - 0.42113 * self.CO2 * (self.Tc_CO2 / np.sqrt(self.Pc_CO2)) \
                 - 0.91249 * self.N2 * (self.Tc_N2 / np.sqrt(self.Pc_N2)) \
                 + 17.438 * self.sg \
                 - 3.2191 * self.sg ** 2
        self.ps_props['K'] = self.K
        return self.K

    """pseudo-critical temperature (°R)"""
    def calc_Tpc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """
        Calculates pseudo-critical temperature, Tpc (°R)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)
        J : float
            SBV parameter, J, (°R/psia)
        K : float
            SBV parameter, K, (°R/psia^0.5)
        ignore_conflict : bool
            set this to True to force usage of input variables instead of calculated variables.
        Returns
        -------
        float
            Pseudo-critical temperature, Tpc (°R)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2, ignore_conflict=ignore_conflict)
        self._initialize_K(K, sg=sg, H2S=H2S, CO2=CO2, N2=N2, ignore_conflict=ignore_conflict)
        self.Tpc = self.K ** 2 / self.J
        self.ps_props['Tpc'] = self.Tpc
        return self.Tpc

    def calc_Ppc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None, ignore_conflict=False):
        """
        Calculates pseudo-critical pressure, Ppc (psia)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)
        J : float
            SBV parameter, J, (°R/psia)
        K : float
            SBV parameter, K, (°R/psia^0.5)
        Tpc : float
            pseudo-critical temperature, Tpc (°R)
        ignore_conflict : bool
            set this to True to force usage of input variables instead of calculated variables.

        Returns
        -------
        float
            pseudo-critical pressure, Ppc (psia)
        """

        self._set_first_caller_attributes(inspect.stack()[0][3], locals())

        if Tpc is not None:
            if K is not None:
                raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % (self._first_caller_name, 'Tpc', 'K'))
            self.Tpc = Tpc  # skips self._check_conflicting_arguments() when initializing Tpc
        else:
            self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)

        self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2, ignore_conflict=ignore_conflict)
        self.Ppc = self.Tpc / self.J
        self.ps_props['Ppc'] = self.Ppc
        return self.Ppc

    def calc_Tr(self, T=None, sg=None, Tpc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """
        Calculates pseudo-reduced temperature, Tr (°R)

        Parameters
        ----------
        T : float
            temperature of gas (°F)
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)
        J : float
            SBV parameter, J, (°R/psia)
        K : float
            SBV parameter, K, (°R/psia^0.5)
        ignore_conflict : bool
            set this to True to force usage of input variables instead of calculated variables.

        Returns
        -------
        float
            pseudo-reduced temperature, Tr (°R)

        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_T(T)
        self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        self.Tr = self.T / self.Tpc
        self.ps_props['Tr'] = self.Tr
        return self.Tr

    """pseudo-reduced pressure (psi)"""
    def calc_Pr(self, P=None, sg=None, Tpc=None, Ppc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        """
        Calculates pseudo-reduced pressure, Pr (psia)

        Parameters
        ----------
        P : float
            pressure of gas (psig)
        sg : float
            specific gravity of gas (dimensionless)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        N2 : float
            mole fraction of N2 (dimensionless)
        J : float
            SBV parameter, J, (°R/psia)
        K : float
            SBV parameter, K, (°R/psia^0.5)
        ignore_conflict : bool
            set this to True to force usage of input variables instead of calculated variables.

        Returns
        -------
        float
            pseudo-reduced pressure, Pr (psia)
        """

        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_P(P)
        self._initialize_Ppc(Ppc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, Tpc=Tpc, ignore_conflict=ignore_conflict)
        self.Pr = self.P / self.Ppc
        self.ps_props['Pr'] = self.Pr
        return self.Pr

    """This function is used by z_helper.py's calc_Z function to check redundant arguments for Pr and Tr"""
    def _initialize_Tr_and_Pr(self, sg=None, P=None, T=None, Tpc=None, Ppc=None, H2S=None, CO2=None, N2=None, Tr=None, Pr=None, J=None, K=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tr(Tr, T=T, sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        self._initialize_Pr(Pr, P=P, sg=sg, Tpc=Tpc, Ppc=Ppc, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        return self.Tr, self.Pr

    def _set_first_caller_attributes(self, func_name, func_kwargs):
        """
        Helper function to set properties related to the first function called (first in the call stack).
        This function doesn't do anything for 'calc_...()' functions called inside the first function.
        For exmaple, if `calc_Pr()' is called, this function is skipped for 'calc_Ppc()' function which is
        triggered inside `calc_Pr()`.
        :param func_name: string
            ex1) func_name= "calc_Tr",
            ex2) func_name = "calc_Pr",
        :param func_kwargs: dictionary kwarg parameters passed to 'func_name'
            ex1) func_kwargs = {'self': ...some_string, 'sg': None, 'Tpc': 377.59, 'H2S': 0.07, 'CO2': 0.1}
            ex2) func_kwargs = {'self': ...some_string, 'sg': 0.6, 'Tpc': None, 'H2S': 0.07, 'CO2': 0.1}
        """
        if not self._first_caller_is_saved:
            func_kwargs = {key: value for key, value in func_kwargs.items() if key != 'self'}
            if 'ignore_conflict' in func_kwargs:

                if func_kwargs['ignore_conflict'] is False:
                    """
                    This modification is needed for self._check_conflicting_arguments(). 
                    The exception in self._check_conflicting_arguments() compares if "kwarg is not None"
                    The default 'ignore_conflict' is a boolean object, so comparing if "ignore_conflict is not None"
                    will raise type error 
                    """
                    func_kwargs['ignore_conflict'] = None

            self._first_caller_name = func_name
            self._first_caller_kwargs = func_kwargs
            self._first_caller_is_saved = True
        else:
            pass

    def _check_conflicting_arguments(self, func, calculated_var):
        """
        :param func: string
            ex1) func_name = "calc_Tpc",
            ex2) func_name = "calc_J",
        :param calculated_var: string
            ex1) calculated_var = 'Tpc'
            ex1) calculated_var = 'J'
        """
        args = inspect.getfullargspec(func).args[1:]  # arg[0] = 'self', args = arguments defined in "func"
        for arg in args:
            if self._first_caller_kwargs[arg] is not None:

                if self._first_caller_name == '_initialize_Tr_and_Pr':
                    raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % ('calc_Z', calculated_var, arg))

                raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % (self._first_caller_name, calculated_var, arg))

    def _initialize_sg(self, sg):
        if sg is None:
            if self._first_caller_name == 'calc_J' or self._first_caller_name == 'calc_K':
                raise TypeError("Missing a required argument, sg (specific gravity, dimensionless)")
            else:
                raise TypeError("Missing a required arguments, sg (specific gravity, dimensionless), or Tpc "
                                "(pseudo-critical temperature, °R) or Ppc (pseudo-critical pressure, psia). "
                                "Either both Tpc and Ppc must be inputted, or only sg needs to be inputted. "
                                "Both Tpc and Ppc can be computed from sg")
        else:
            self.sg = sg

    def _initialize_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, P (gas pressure, psig)")
        else:
            self.P_a = P  # psia
            self.P = calc_psig_to_psia(P)

    def _initialize_T(self, T):
        if T is None:
            raise TypeError("Missing a required argument, T (gas temperature, °F)")
        else:
            self.T_f = T  # °F
            self.T = calc_Fahrenheit_to_Rankine(T)

    def _initialize_H2S(self, H2S):
        if H2S is None:
            self.H2S = 0
        else:
            self.H2S = H2S

    def _initialize_CO2(self, CO2):
        if CO2 is None:
            self.CO2 = 0
        else:
            self.CO2 = CO2

    def _initialize_N2(self, N2):
        if N2 is None:
            self.N2 = 0
        else:
            self.N2 = N2

    def _initialize_J(self, J, sg=None, H2S=None, CO2=None, N2=None, ignore_conflict=None):
        if J is None:
            self.calc_J(sg=sg, H2S=H2S, CO2=CO2, N2=N2)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_J, 'J')
            self.J = J

    def _initialize_K(self, K, sg=None, H2S=None, CO2=None, N2=None, ignore_conflict=None):
        if K is None:
            self.calc_K(sg=sg, H2S=H2S, CO2=CO2, N2=N2)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_K, 'K')
            self.K = K

    def _initialize_Tpc(self, Tpc, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        if Tpc is None:
            self.calc_Tpc(sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tpc, 'Tpc')
            self.Tpc = Tpc

    def _initialize_Ppc(self, Ppc, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None, ignore_conflict=False):
        if Ppc is None:
            self.calc_Ppc(sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, Tpc=Tpc, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Ppc, 'Ppc')
            self.Ppc = Ppc

    def _initialize_Pr(self, Pr, P=None, sg=None, Tpc=None, Ppc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        if Pr is None:
            self.calc_Pr(P=P, sg=sg, Tpc=Tpc, Ppc=Ppc, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Pr, 'Pr')
            self.Pr = Pr

    def _initialize_Tr(self, Tr, T, sg=None, Tpc=None, H2S=None, CO2=None, N2=None, J=None, K=None, ignore_conflict=False):
        if Tr is None:
            self.calc_Tr(T=T, sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tr, 'Tr')
            self.Tr = Tr

    def _check_invalid_mode(self, mode):
        if mode != 'sutton' and mode != 'piper':
            raise TypeError("Invalid optional argument, mode (calculation method), input either 'sutton', 'piper'")
        self.mode = mode


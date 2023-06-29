import inspect

from gascompressibility.utilities.utilities import calc_Fahrenheit_to_Rankine
from gascompressibility.utilities.utilities import calc_psig_to_psia


class Sutton():

    """
    Class object to calculate pseudo-critical properties.

    Based on Sutton's specific gravity correlation [1]_ and Wichert & Aziz correction for acid gases (:math:`H_2S` and :math:`CO_2`) [2]_.

    """

    def __init__(self):

        self.sg = None
        """specific gravity (dimensionless)"""
        self.T_f = None
        """temperature (°F)"""
        self.T = None
        """temperature (°R)"""
        self.P_g = None
        """pressure (psig)"""
        self.P = None
        """pressure (psia)"""
        self.H2S = None
        """mole fraction of H2S (dimensionless)"""
        self.CO2 = None
        """mole fraction of CO2 (dimensionless)"""

        self.Tpc = None
        """pseudo-critical temperature, Tpc (°R)"""
        self.Ppc = None
        """pseudo-critical pressure, Ppc (psia)"""
        self.A = None
        self.B = None
        self.e_correction = None
        """temperature-correction factor for acid gases, ε (°R)"""
        self.Tpc_corrected = None
        """corrected pseudo-critical temperature, T'pc (°R)"""
        self.Ppc_corrected = None
        """corrected pseudo-critical pressure, P'pc (psia)"""
        self.Tr = None
        """pseudo-reduced temperature, Tr (°R)"""
        self.Pr = None
        """pseudo-reduced pressure, Pr (psia)"""

        self.ps_props = {
            'Tpc': None,
            'Ppc': None,
            'e_correction': None,
            'Tpc_corrected': None,
            'Ppc_corrected': None,
            'Tr': None,
            'Pr': None,
        }
        """dictionary of pseudo-critical properties."""

        self._first_caller_name = None
        self._first_caller_kwargs = {}
        self._first_caller_is_saved = False

    def __str__(self):
        return str(self.ps_props)

    def __repr__(self):
        description = '<gascompressibility.pseudocritical.Sutton> class object with the following calculated attributes:\n{'
        items = '\n   '.join('%s: %s' % (k, v) for k, v in self.ps_props.items())
        return description + '\n   ' +items + '\n}'

    """sum of the mole fractions of CO2 and H2S in a gas mixture"""
    def _calc_A(self, H2S=None, CO2=None):
        self._initialize_H2S(H2S)
        self._initialize_CO2(CO2)
        self.A = self.H2S + self.CO2
        return self.A

    """mole fraction of H2S in a gas mixture"""
    def _calc_B(self, H2S=None):
        self._initialize_H2S(H2S)
        self.B = self.H2S
        return self.B

    def calc_Tpc(self, sg=None):
        """
        Calculates pseudo-critical temperature, Tpc (°R)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)

        Returns
        -------
        float
            pseudo-critical temperature, Tpc (°R)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self.Tpc = 169.2 + 349.5 * self.sg - 74.0 * self.sg ** 2
        self.ps_props['Tpc'] = self.Tpc
        return self.Tpc

    def calc_Ppc(self, sg=None):
        """
        Calculates pseudo-critical pressure, Ppc (psia)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)

        Returns
        -------
        float
            pseudo-critical pressure, Ppc (psia)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_sg(sg)
        self.Ppc = 756.8 - 131.07 * self.sg - 3.6 * self.sg ** 2
        self.ps_props['Ppc'] = self.Ppc
        return self.Ppc

    def calc_e_correction(self, H2S=None, CO2=None):
        """
        Calculates the temperature-correction factor for acid gases, ε (°R)

        Parameters
        ----------
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)

        Returns
        -------
        float
            temperature-correction factor for acid gases, ε (°R)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_A(A=None, H2S=H2S, CO2=CO2)
        self._initialize_B(B=None, H2S=H2S)
        self.e_correction = 120 * (self.A ** 0.9 - self.A ** 1.6) + 15 * (self.B ** 0.5 - self.B ** 4)
        self.ps_props['e_correction'] = self.e_correction
        return self.e_correction

    def calc_Tpc_corrected(self, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        """
        Calculates the corrected pseudo-critical temperature, T'pc (°R)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        Tpc : float
            pseudo-critical temperature, Tpc (°R)
        e_correction : float
            temperature-correction factor for acid gases, ε (°R)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        ignore_conflict : bool
            set this to True to override calculated variables with input keyword arguments.

        Returns
        -------
        float
            corrected pseudo-critical temperature, T'pc (°R)

        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tpc(Tpc, sg=sg, ignore_conflict=ignore_conflict)

        # Correction is not needed if no sour gas is present
        if e_correction is None and H2S is None and CO2 is None:
            self.Tpc_corrected = self.Tpc
            self.ps_props['Tpc_corrected'] = self.Tpc_corrected
            return self.Tpc_corrected

        self._initialize_e_correction(e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Tpc_corrected = self.Tpc - self.e_correction
        self.ps_props['Tpc_corrected'] = self.Tpc_corrected
        return self.Tpc_corrected

    def calc_Ppc_corrected(self, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        """
        Calculates the corrected pseudo-critical pressure, P'pc (psia)

        Parameters
        ----------
        sg : float
            specific gravity of gas (dimensionless)
        Tpc : float
            pseudo-critical temperature, Tpc (°R)
        Ppc : float
            pseudo-critical pressure, Ppc (psia)
        e_correction : float
            temperature-correction factor for acid gases, ε (°R)
        Tpc_corrected : float
            corrected pseudo-critical temperature, T'pc (°R)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        ignore_conflict : bool
            set this to True to override calculated variables with input keyword arguments.

        Returns
        -------
        float
            corrected pseudo-critical pressure, P'pc (psia)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Ppc(Ppc, sg=sg, ignore_conflict=ignore_conflict)

        # Correction is not needed if no sour gas is present
        if e_correction is None and H2S is None and CO2 is None and Tpc is None and Tpc_corrected is None:
            self.Ppc_corrected = self.Ppc
            self.ps_props['Ppc_corrected'] = self.Ppc_corrected
            return self.Ppc_corrected

        self._initialize_Tpc(Tpc, sg=sg, ignore_conflict=ignore_conflict)
        self._initialize_B(B=None, H2S=H2S)
        self._initialize_e_correction(e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Ppc_corrected = (self.Ppc * self.Tpc_corrected) / (self.Tpc - self.B * (1 - self.B) * self.e_correction)
        self.ps_props['Ppc_corrected'] = self.Ppc_corrected
        return self.Ppc_corrected

    def calc_Tr(self, T=None, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        """
        Calculates pseudo-reduced temperature, Tr (°R)

        Parameters
        ----------
        T : float
            temperature of gas (°F)
        Tpc_corrected : float
            corrected pseudo-critical temperature, T'pc (°R)
        sg : float
            specific gravity of gas (dimensionless)
        Tpc : float
            pseudo-critical temperature, Tpc (°R)
        e_correction : float
            temperature-correction factor for acid gases, ε (°R)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        ignore_conflict : bool
            set this to True to override calculated variables with input keyword arguments.

        Returns
        -------
        float
            pseudo-reduced temperature, Tr (°R)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_T(T)
        self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Tr = self.T / self.Tpc_corrected
        self.ps_props['Tr'] = self.Tr
        return self.Tr

    """pseudo-reduced pressure (psi)"""
    def calc_Pr(self, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        """
        Calculates pseudo-reduced pressure, Pr (psia)

        Parameters
        ----------
        P : float
            pressure of gas (psig)
        Ppc_corrected : float
            corrected pseudo-critical pressure, P'pc (psia)
        sg : float
            specific gravity of gas (dimensionless)
        Tpc : float
            pseudo-critical temperature, Tpc (°R)
        Ppc : float
            pseudo-critical pressure, Ppc (psia)
        e_correction : float
            temperature-correction factor for acid gases, ε (°R)
        Tpc_corrected : float
            corrected pseudo-critical temperature, T'pc (°R)
        H2S : float
            mole fraction of H2S (dimensionless)
        CO2 : float
            mole fraction of CO2 (dimensionless)
        ignore_conflict : bool
            set this to True to override calculated variables with input keyword arguments.

        Returns
        -------
        float
            pseudo-reduced pressure, Pr (psia)
        """
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_P(P)
        self._initialize_Ppc_corrected(Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        self.Pr = self.P / self.Ppc_corrected
        self.ps_props['Pr'] = self.Pr
        return self.Pr

    """This function is used by z_helper.py's calc_z function to check redundant arguments for Pr and Tr"""
    def _initialize_Tr_and_Pr(self, sg=None, P=None, T=None, Tpc=None, Ppc=None, Tpc_corrected=None, Ppc_corrected=None,
               H2S=None, CO2=None, Tr=None, Pr=None, e_correction=None, ignore_conflict=False):
        self._set_first_caller_attributes(inspect.stack()[0][3], locals())
        self._initialize_Tr(Tr, T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S,
                            CO2=CO2, ignore_conflict=ignore_conflict)
        self._initialize_Pr(Pr, P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                            Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        return self.Tr, self.Pr


    def _set_first_caller_attributes(self, func_name, func_kwargs):
        """
        Helper function to set properties related to the first function called (first in the call stack).
        This function doesn't do anything for 'calc_...()' functions called inside the first function.
        For exmaple, if `calc_Ppc_corrected()' is called, this function is skipped for 'calc_Ppc()' function which is
        triggered inside `calc_Ppc_corrected()`.
        :param func_name: string
            ex1) func_name= "calc_Tpc_corrected",
            ex2) func_name = "calc_Ppc_corrected",
        :param func_kwargs: kwarg parameters passed to 'func_name'
            ex1) func_kwargs = {'self': ...some_string, 'sg': None, 'Tpc': 377.59, 'e_correction': None, 'H2S': 0.07, 'CO2': 0.1}
            ex2) func_kwargs = {'self': ...some_string, 'sg': 0.6, 'Tpc': None, 'e_correction': None, 'H2S': 0.07, 'CO2': 0.1}
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
                # this is triggered in z_helper.py's calc_z() function
                if self._first_caller_name == '_initialize_Tr_and_Pr':
                    raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % ('calc_z', calculated_var, arg))

                raise TypeError('%s() has conflicting keyword arguments "%s" and "%s"' % (self._first_caller_name, calculated_var, arg))

    def _initialize_sg(self, sg):
        if sg is None:
            if self._first_caller_name == 'calc_Ppc' or self._first_caller_name == 'calc_Tpc':
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
            self.T_f = T
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

    # The first argument A will always be None when called. However, still defining it for structural consistency
    def _initialize_A(self, A, H2S=None, CO2=None):
        if A is None:
            self._calc_A(H2S=H2S, CO2=CO2)
        else:
            self.A = A

    # The first argument B will always be None when called. However, still defining it for structural consistency
    def _initialize_B(self, B, H2S=None):
        if B is None:
            self._calc_B(H2S=H2S)
        else:
            self.B = B

    def _initialize_Tpc(self, Tpc, sg=None, ignore_conflict=None):
        if Tpc is None:
            self.calc_Tpc(sg=sg)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tpc, 'Tpc')
            self.Tpc = Tpc

    def _initialize_Ppc(self, Ppc, sg=None, ignore_conflict=None):
        if Ppc is None:
            self.calc_Ppc(sg=sg)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Ppc, 'Ppc')
            self.Ppc = Ppc

    def _initialize_e_correction(self, e_correction, H2S=None, CO2=None, ignore_conflict=False):
        if e_correction is None:
            self.calc_e_correction(H2S=H2S, CO2=CO2)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_e_correction, 'e_correction')
            self.e_correction = e_correction

    def _initialize_Tpc_corrected(self, Tpc_corrected, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        if Tpc_corrected is None:
            self.calc_Tpc_corrected(sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tpc_corrected, 'Tpc_corrected')
            self.Tpc_corrected = Tpc_corrected

    def _initialize_Ppc_corrected(self, Ppc_corrected, sg=None, Tpc=None, Ppc=None, e_correction=None,
                                  Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        if Ppc_corrected is None:
            self.calc_Ppc_corrected(sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Ppc_corrected, 'Ppc_corrected')
            self.Ppc_corrected = Ppc_corrected

    def _initialize_Pr(self, Pr, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, H2S=None, CO2=None, ignore_conflict=False):
        if Pr is None:
            self.calc_Pr(P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Pr, 'Pr')
            self.Pr = Pr

    def _initialize_Tr(self, Tr, T, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, H2S=None, CO2=None, ignore_conflict=False):
        if Tr is None:
            self.calc_Tr(T=T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, H2S=H2S, CO2=CO2, ignore_conflict=ignore_conflict)
        else:
            if ignore_conflict is False:
                self._check_conflicting_arguments(self.calc_Tr, 'Tr')
            self.Tr = Tr





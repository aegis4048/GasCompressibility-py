import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


class zfactor(object):
    def __init__(
            self,
            mode='sutton',
            Pc_H2S=1306,
            Tc_H2S=672.3,
            Pc_CO2=1071,
            Tc_CO2=547.5,
            Pc_N2=492.4,
            Tc_N2=227.16,
            A1=0.3265,
            A2=-1.0700,
            A3=-0.5339,
            A4=0.01569,
            A5=-0.05165,
            A6=0.5475,
            A7=-0.7361,
            A8=0.1844,
            A9=0.1056,
            A10=0.6134,
            A11=0.7210,
    ):
        self._check_invalid_mode(mode)
        self.mode = mode

        self.T = None
        self.sg = None
        self._T = None
        self.P = None
        self.H2S = None
        self.CO2 = None
        self.N2 = None

        self.Pc_H2S = Pc_H2S
        self.Tc_H2S = Tc_H2S
        self.Pc_CO2 = Pc_CO2
        self.Tc_CO2 = Tc_CO2
        self.Pc_N2 = Pc_N2
        self.Tc_N2 = Tc_N2

        self.Tpc = None
        self.Ppc = None
        self.A = None
        self.B = None
        self.e_correction = None
        self.Tpc_corrected = None
        self.Ppc_corrected = None
        self.J = None
        self.K = None
        self.Tr = None
        self.Pr = None

        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.A5 = A5
        self.A6 = A6
        self.A7 = A7
        self.A8 = A8
        self.A9 = A9
        self.A10 = A10
        self.A11 = A11

        self.Z = None

        self._calc_from = None

    def __str__(self):
        return str(self.Z)

    def __repr__(self):
        return '<GasCompressibilityFactor object. Mixing Rule = %s>' % self.mode

    def calc_Fahrenheit_to_Rankine(self, _T):
        self._calc_from = 'calc_Fahrenheit_to_Rankine()'
        if _T is None:
            raise TypeError("Missing a required argument, 'T' (gas temperature, °F)")
        self._T = _T  # Fahrenheit
        self.T = _T + 459.67  # Rankine, Rankine is used for calculation below
        return self.T

    """pseudo-critical temperature (°R)"""
    def calc_Tpc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        self._calc_from = 'calc_Tpc()'
        if self.mode == 'sutton':
            self._initialize_sg(sg)
            self.Tpc = 169.2 + 349.5 * self.sg - 74.0 * self.sg ** 2
        else:  # mode == 'piper'
            self._redundant_argument_check_J_or_K(sg=sg, J=J, K=K, H2S=H2S, CO2=CO2, N2=N2)
            self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
            self._initialize_K(K, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
            self.Tpc = self.K ** 2 / self.J
        return self.Tpc

    """pseudo-critical pressure (psi)"""
    def calc_Ppc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None):
        self._calc_from = 'calc_Ppc()'
        if self.mode == 'sutton':
            self._initialize_sg(sg)
            self.Ppc = 756.8 - 131.07 * self.sg - 3.6 * self.sg ** 2
        else:  # mode = 'piper'
            self._redundant_argument_check_J_or_K(sg=sg, J=J, K=K, H2S=H2S, CO2=CO2, N2=N2)
            if Tpc is not None:
                if K is not None:
                    raise TypeError("Redundant arguments 'Tpc' and 'K', input only one of them")
            self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
            self.Ppc = self.Tpc / self.J
        return self.Ppc

    """sum of the mole fractions of CO2 and H2S in a gas mixture"""
    def calc_A(self, H2S=None, CO2=None):
        self._calc_from = 'calc_A()'
        self._initialize_H2S(H2S)
        self._initialize_CO2(CO2)
        self.A = self.H2S + self.CO2
        return self.A

    """mole fraction of H2S in a gas mixture"""
    def calc_B(self, H2S=None):
        self._calc_from = 'calc_B()'
        self._initialize_H2S(H2S)
        self.B = self.H2S
        return self.B

    """correction for CO2 and H2S (°R)"""
    def calc_e_correction(self, A=None, B=None, H2S=None, CO2=None):
        self._calc_from = 'calc_e_correction()'
        if A is not None:
            if CO2 is not None:
                raise TypeError("Redundant arguments 'A' and 'CO2', input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments 'A' and 'H2S', input only one of them")
        if B is not None:
            if H2S is not None:
                raise TypeError("Redundant arguments 'B' and 'H2S', input only one of them")
            if CO2 is not None:
                H2S = B

        self._initialize_A(A, H2S=H2S, CO2=CO2)
        self._initialize_B(B, H2S=H2S)
        self.e_correction = 120 * (self.A ** 0.9 - self.A ** 1.6) + 15 * (self.B ** 0.5 - self.B ** 4)
        return self.e_correction

    def calc_Tpc_corrected(self, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None, CO2=None):
        self._calc_from = 'calc_Tpc_corrected()'
        self._initialize_Tpc(Tpc, sg=sg)
        self._initialize_e_correction(e_correction, A=A, B=B, H2S=H2S, CO2=CO2)
        self.Tpc_corrected = self.Tpc - self.e_correction
        return self.Tpc_corrected

    """ corrected pseudo-critical pressure (psi)"""
    def calc_Ppc_corrected(self, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None,
                           A=None, B=None, H2S=None, CO2=None):
        self._calc_from = 'calc_Ppc_corrected()'
        if e_correction is not None:
            if B is None and H2S is None:
                raise TypeError("Missing a required argument, 'H2S', (mole fraction of H2S, dimensionless)")

        self._initialize_Ppc(Ppc, sg=sg)
        self._initialize_B(B, H2S=H2S)
        self._initialize_e_correction(e_correction, A=A, B=B, H2S=H2S, CO2=CO2)
        if Tpc_corrected is None:
            self._initialize_Tpc(Tpc, sg=sg)
            self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, A=A, B=B, H2S=H2S, CO2=CO2)
        self.Ppc_corrected = (self.Ppc * self.Tpc_corrected) / (self.Tpc - self.B * (1 - self.B) * self.e_correction)
        return self.Ppc_corrected

    def calc_J(self, sg=None, H2S=None, CO2=None, N2=None):
        self._calc_from = 'calc_J()'
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
        return self.J

    def calc_K(self, sg=None, H2S=None, CO2=None, N2=None):
        self._calc_from = 'calc_K()'
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
        return self.K

    """pseudo-reduced temperature (°R)"""
    def calc_Tr(self, T=None, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        self._calc_from = 'calc_Tr()'
        self._initialize_T(T)
        if self.mode == 'sutton':
            self._redundant_argument_check_Tpc_corrected(sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, A=A, B=B, e_correction=e_correction)
            self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, A=A, B=B, H2S=H2S, CO2=CO2)
            self.Tr = self.T / self.Tpc_corrected
        else:  # mode == 'piper'
            self._redundant_argument_check_Tpc(Tpc=Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self.Tr = self.T / self.Tpc
        return self.Tr

    """pseudo-reduced pressure (psi)"""
    def calc_Pr(self, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        self._calc_from = 'calc_Pr()'
        self._initialize_P(P)
        if self.mode == 'sutton':
            self._redundant_argument_check_Ppc_corrected(sg=sg, Ppc=Ppc, Tpc_corrected=Tpc_corrected, Tpc=Tpc, H2S=H2S, CO2=CO2, A=None, B=None, e_correction=e_correction)
            self._initialize_Ppc_corrected(Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, A=A, B=B, H2S=H2S, CO2=CO2)
            self.Pr = self.P / self.Ppc_corrected
        else:  # mode == 'piper'
            self._redundant_argument_check_Ppc(Ppc=Ppc, Tpc=Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_Ppc(Ppc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, Tpc=Tpc)
            self.Pr = self.P / self.Ppc
        return self.Pr

    """
    Objective function to be minimized for the Newton-Raphson non-linear solver.
    Wichert-Azis correlation for z-factor. 
    
    Source: Wichert, E. and Aziz, K. 1972. Calculate Z's for Sour Gases. Hydrocarbon Processing 51 (May): 119–122
    """
    def _calc_Z(self, z):

        self.A1 = 0.3265
        self.A2 = -1.0700
        self.A3 = -0.5339
        self.A4 = 0.01569
        self.A5 = -0.05165
        self.A6 = 0.5475
        self.A7 = -0.7361
        self.A8 = 0.1844
        self.A9 = 0.1056
        self.A10 = 0.6134
        self.A11 = 0.7210

        return 1 + (
                self.A1 +
                self.A2 / self.Tr +
                self.A3 / self.Tr ** 3 +
                self.A4 / self.Tr ** 4 +
                self.A5 / self.Tr ** 5
        ) * (0.27 * self.Pr) / (z * self.Tr) + (
                self.A6 +
                self.A7 / self.Tr +
                self.A8 / self.Tr ** 2
        ) * ((0.27 * self.Pr) / (z * self.Tr)) ** 2 - self.A9 * (
                self.A7 / self.Tr +
                self.A8 / self.Tr ** 2
        ) * ((0.27 * self.Pr) / (z * self.Tr)) ** 5 + self.A10 * (
                1 +
                self.A11 * ((0.27 * self.Pr) / (z * self.Tr)) ** 2
        ) * (
                ((0.27 * self.Pr) / (z * self.Tr)) ** 2 /
                self.Tr ** 3
        ) * np.exp(-self.A11 * ((0.27 * self.Pr) / (z * self.Tr)) ** 2) - z

    """Newton-Raphson nonlinear solver"""
    def calc_Z(self, guess=0.9, sg=None, P=None, T=None, Tpc=None, Ppc=None, Tpc_corrected=None, Ppc_corrected=None,
               A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tr=None, Pr=None, e_correction=None, **kwargs):
        self._calc_from = 'calc_Z()'
        self._initialize_Pr(Pr, P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction, Tpc_corrected=Tpc_corrected, A=A, B=B, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
        self._initialize_Tr(Tr, T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, A=A, B=B, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
        self.Z = optimize.newton(self._calc_Z, guess, **kwargs)
        return self.Z

    def _initialize_sg(self, sg):
        if sg is None:
            if self._calc_from == 'calc_Ppc()' or self._calc_from == 'calc_Tpc()':
                raise TypeError("Missing a required argument, 'sg' (specific gravity, dimensionless)")
            elif self._calc_from == 'calc_J()' or self._calc_from == 'calc_K()':
                raise TypeError("Missing a required argument, 'sg' (specific gravity, dimensionless), or 'J' "
                                "(Stewart-Burkhardt-VOO parameter, °R/psia), or "
                                "'K' (Stewart-Burkhardt-VOO parameter, °R/psia^0.5). "
                                "The calculation requires either "
                                "1) both 'J' and 'K' provided without 'sg', or "
                                "2) only 'sg' provided without both 'J' and 'K'")
            else:
                raise TypeError("Missing a required arguments, 'sg' (specific gravity, dimensionless), or 'Tpc' "
                                "(pseudo-critical temperature, °R) or 'Ppc' (pseudo-critical pressure, psia). "
                                "Either both 'Tpc' and 'Ppc' must be inputted, or 'sg' needs to be inputted. "
                                "Both 'Tpc' and 'Ppc' can be computed from 'sg'")
        else:
            self.sg = sg

    def _initialize_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, 'P' (gas pressure, psia)")
        else:
            self.P = P

    def _initialize_T(self, T):
        if T is None:
            raise TypeError("Missing a required argument, 'T' (gas temperature, °F)")
        else:
            self.T = self.calc_Fahrenheit_to_Rankine(T)

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

    def _initialize_Tpc(self, Tpc, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if Tpc is None:
            self.calc_Tpc(sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
        else:
            self.Tpc = Tpc

    def _initialize_Ppc(self, Ppc, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None):
        if Ppc is None:
            self.calc_Ppc(sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, Tpc=Tpc)
        else:
            self.Ppc = Ppc

    def _initialize_e_correction(self, e_correction, A=None, B=None, H2S=None, CO2=None):
        if e_correction is None:
            self.calc_e_correction(A, B, H2S, CO2)
        else:
            self.e_correction = e_correction

    def _initialize_Tpc_corrected(self, Tpc_corrected, sg=None, Tpc=None, e_correction=None,
                                  A=None, B=None, H2S=None, CO2=None):
        if Tpc_corrected is None:
            self.calc_Tpc_corrected(sg, Tpc, e_correction, A, B, H2S, CO2)
        else:
            self.Tpc_corrected = Tpc_corrected

    def _initialize_Ppc_corrected(self, Ppc_corrected, sg=None, Tpc=None, Ppc=None, e_correction=None,
                                  Tpc_corrected=None, A=None, B=None, H2S=None, CO2=None):
        if Ppc_corrected is None:
            self.calc_Ppc_corrected(sg, Tpc, Ppc, e_correction, Tpc_corrected, A, B, H2S, CO2)
        else:
            self.Ppc_corrected = Ppc_corrected

    def _initialize_J(self, J, sg=None, H2S=None, CO2=None, N2=None):
        if J is None:
            self.calc_J(sg, H2S, CO2, N2)
        else:
            self.J = J

    def _initialize_K(self, K, sg=None, H2S=None, CO2=None, N2=None):
        if K is None:
            self.calc_K(sg, H2S, CO2, N2)
        else:
            self.K = K

    def _initialize_Pr(self, Pr, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None,
                       A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if Pr is None:
            self.calc_Pr(P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                         Tpc_corrected=Tpc_corrected, A=A, B=B, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
        else:
            self.Pr = Pr

    def _initialize_Tr(self, Tr, T, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if Tr is None:
            self.calc_Tr(T, Tpc_corrected, sg, Tpc, e_correction, A, B, H2S, CO2, N2, J, K)
        else:
            self.Tr = Tr

    def _initialize_A(self, A, H2S=None, CO2=None):
        if A is None:
            self.calc_A(H2S, CO2)
        else:
            self.A = A

    def _initialize_B(self, B, H2S=None):
        if B is None:
            self.calc_B(H2S)
        else:
            self.B = B

    def _check_missing_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, 'P' (gas pressure, psia)")
        self.P = P

    def _check_missing_T(self, _T):
        if _T is None:
            raise TypeError("Missing a required argument, 'T' (gas temperature, °F)")
        self._T = _T

    def _check_invalid_mode(self, mode):
        if mode != 'sutton' and mode != 'piper':
            raise TypeError("Invalid optional argument, 'mode' (calculation method), input either 'sutton', 'piper', or None (default='sutton')")
        self.mode = mode

    def _redundant_argument_check_Tpc_corrected(self, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None, CO2=None):
        if Tpc_corrected is not None:
            if sg is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'sg', input only one of them")
            if Tpc is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'Tpc', input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'H2S', input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'CO2', input only one of them")
            if A is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'A', input only one of them")
            if B is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'B', input only one of them")
            if e_correction is not None:
                raise TypeError("Redundant arguments 'Tpc_corrected' and 'e_correction', input only one of them")

    def _redundant_argument_check_Ppc_corrected(self, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None, A=None, B=None, H2S=None, CO2=None):
        if Ppc_corrected is not None:
            if Ppc is not None:
                raise TypeError("Redundant arguments 'Ppc_corrected' and 'Ppc', input only one of them")
            if Tpc_corrected is not None:
                raise TypeError("Redundant arguments 'Ppc_corrected' and 'Tpc_corrected', input only one of them")
            self._redundant_argument_check_Tpc_corrected(sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, A=A, B=B, e_correction=e_correction)

    def _redundant_argument_check_J_or_K(self, sg=None, J=None, K=None, H2S=None, CO2=None, N2=None):
        if J is not None:
            if sg is not None:
                raise TypeError("Redundant arguments 'J' and 'sg', input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments 'J' and 'H2S', input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments 'J' and 'CO2', input only one of them")
            if N2 is not None:
                raise TypeError("Redundant arguments 'J' and 'N2', input only one of them")
        if K is not None:
            if sg is not None:
                raise TypeError("Redundant arguments 'K' and 'sg', input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments 'K' and 'H2S', input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments 'K' and 'CO2', input only one of them")
            if N2 is not None:
                raise TypeError("Redundant arguments 'K' and 'N2', input only one of them")

    def _redundant_argument_check_Tpc(self, Tpc=None, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if self.mode == 'piper':
            if Tpc is not None:
                if sg is not None:
                    raise TypeError("Redundant arguments 'Tpc' and 'sg', input only one of them")
                if J is not None and self._calc_from != 'calc_Z()':
                    raise TypeError("Redundant arguments 'Tpc' and 'J', input only one of them")
                if K is not None:
                    raise TypeError("Redundant arguments 'Tpc' and 'K', input only one of them")
                self._redundant_argument_check_J_or_K(J=J, K=K, H2S=H2S, CO2=CO2, N2=N2)

    def _redundant_argument_check_Ppc(self, Ppc=None, Tpc=None, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if self.mode == 'piper':
            if Ppc is not None:
                if Tpc is not None and self._calc_from != 'calc_Z()':
                    raise TypeError("Redundant arguments 'Ppc' and 'Tpc', input only one of them")
                if sg is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'sg', input only one of them")
                if J is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'J', input only one of them")
                if K is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'K', input only one of them")
                if H2S is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'H2S', input only one of them")
                if CO2 is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'CO2', input only one of them")
                if N2 is not None:
                    raise TypeError("Redundant arguments 'Ppc' and 'N2', input only one of them")

    def _unused_argument_check(self, sg=None, P=None, T=None, Tpc=None, Ppc=None, Tpc_corrected=None, Ppc_corrected=None,
               A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tr=None, Pr=None, e_correction=None):
        if self.mode == 'sutton':
            if K is not None:
                raise TypeError("Redundant arguments 'Ppc' and 'N2', input only one of them")


    def quickstart(self):

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
                z_obj = zfactor()
                z = z_obj.calc_Z(Tr=Tr, Pr=Pr, **{'maxiter': 1000})
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
        ax.grid(b=True, which='minor', alpha=0.1)
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

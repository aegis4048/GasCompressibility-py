import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import inspect

try:
    from gascompressibility.utilities.utilities import calc_Fahrenheit_to_Rankine
except:
    pass


class piper(object):
    def __init__(
            self,
            Pc_H2S=1306,
            Tc_H2S=672.3,
            Pc_CO2=1071,
            Tc_CO2=547.5,
            Pc_N2=492.4,
            Tc_N2=227.16,
    ):
        self.mode = 'piper'
        self._check_invalid_mode(self.mode)  # prevent user modification of self.mode

        self.sg = None
        self._T = None
        self.T = None
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
        self.J = None
        self.K = None
        self.Tr = None
        self.Pr = None

        self.Z = None

        self._calc_from = None

    def __str__(self):
        return str(self.Z)

    def __repr__(self):
        return '<GasCompressibilityFactor object. Mixing Rule = %s>' % self.mode

    def _store_first_caller_name(self, func_name):
        if self._calc_from is None:
            self._calc_from = func_name

    """pseudo-critical temperature (°R)"""
    def calc_Tpc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._redundant_argument_check_J_or_K(sg=sg, J=J, K=K, H2S=H2S, CO2=CO2, N2=N2)
        self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
        self._initialize_K(K, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
        self.Tpc = self.K ** 2 / self.J
        return self.Tpc

    """pseudo-critical pressure (psi)"""
    def calc_Ppc(self, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None, Tpc=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        if self.mode == 'sutton':
            self._initialize_sg(sg, calc_from='Ppc')
            self.Ppc = 756.8 - 131.07 * self.sg - 3.6 * self.sg ** 2
        else:  # mode = 'piper'
            self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_J(J, sg=sg, H2S=H2S, CO2=CO2, N2=N2)
            self.Ppc = self.Tpc / self.J
        return self.Ppc

    """Stewart-Burkhardt-VOO parameter J, (°R/psia)"""
    def calc_J(self, sg=None, H2S=None, CO2=None, N2=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._initialize_sg(sg, calc_from='J')
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

    """Stewart-Burkhardt-VOO parameter K, (°R/psia^0.5)"""
    def calc_K(self, sg=None, H2S=None, CO2=None, N2=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._initialize_sg(sg, calc_from='K')
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

    def calc_Tr(self, T=None, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None,
                CO2=None, N2=None, J=None, K=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._initialize_T(T)
        if self.mode == 'sutton':
            self._redundant_argument_check_Tpc_corrected(sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, A=A, B=B,
                                                         e_correction=e_correction)
            self._initialize_Tpc_corrected(Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, A=A, B=B, H2S=H2S,
                                           CO2=CO2)
            self.Tr = self.T / self.Tpc_corrected
        else:  # mode == 'piper'
            self._redundant_argument_check_Tpc(Tpc=Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_Tpc(Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self.Tr = self.T / self.Tpc
        return self.Tr

    """pseudo-reduced pressure (psi)"""

    def calc_Pr(self, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None, Tpc_corrected=None,
                A=None, B=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._initialize_P(P)
        if self.mode == 'sutton':
            self._redundant_argument_check_Ppc_corrected(sg=sg, Ppc=Ppc, Tpc_corrected=Tpc_corrected, Tpc=Tpc, H2S=H2S,
                                                         CO2=CO2, A=None, B=None, e_correction=e_correction)
            self._initialize_Ppc_corrected(Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                                           Tpc_corrected=Tpc_corrected, A=A, B=B, H2S=H2S, CO2=CO2)
            self.Pr = self.P / self.Ppc_corrected
        else:  # mode == 'piper'
            self._redundant_argument_check_Ppc(Ppc=Ppc, Tpc=Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)
            self._initialize_Ppc(Ppc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K, Tpc=Tpc)
            self.Pr = self.P / self.Ppc
        return self.Pr

    """
    Objective function to miminize for Newton-Raphson nonlinear solver - Z factor calculation
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
               A=None, B=None, H2S=None, CO2=None, N2=None, Tr=None, Pr=None, e_correction=None, **kwargs):
        self._store_first_caller_name(inspect.stack()[0][3])
        self._initialize_Pr(Pr, P=P, Ppc_corrected=Ppc_corrected, sg=sg, Tpc=Tpc, Ppc=Ppc, e_correction=e_correction,
                            Tpc_corrected=Tpc_corrected, A=A, B=B, H2S=H2S, CO2=CO2)
        self._initialize_Tr(Tr, T, Tpc_corrected=Tpc_corrected, sg=sg, Tpc=Tpc, e_correction=e_correction, A=A, B=B,
                            H2S=H2S, CO2=CO2)
        self.Z = optimize.newton(self._calc_Z, guess, **kwargs)

        return self.Z

    def _initialize_sg(self, sg, calc_from=None):
        if sg is None:
            if calc_from == 'Ppc' or calc_from == 'Tpc':
                raise TypeError("Missing a required argument, sg (specific gravity, dimensionless)")
            elif calc_from == 'J' or calc_from == 'K':
                raise TypeError("Missing a required argument, sg (specific gravity, dimensionless), or J "
                                "(Stewart-Burkhardt-VOO parameter, °R/psia), or "
                                "K (Stewart-Burkhardt-VOO parameter, °R/psia^0.5). "
                                "The calculation requires either "
                                "1) both J and K provided without sg, or "
                                "2) only sg provided without both J and K")
            else:
                raise TypeError("Missing a required arguments, sg (specific gravity, dimensionless), or Tpc "
                                "(pseudo-critical temperature, °R) or Ppc (pseudo-critical pressure, psia). "
                                "Either both Tpc and Ppc must be inputted, or sg needs to be inputted. "
                                "Both Tpc and Ppc can be computed from sg")
        else:
            self.sg = sg

    def _initialize_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, P (gas pressure, psia)")
        else:
            self.P = P

    def _initialize_T(self, T):
        if T is None:
            raise TypeError("Missing a required argument, T (gas temperature, °F)")
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

    def _initialize_Pr(self, Pr, P=None, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None, e_correction=None,
                       Tpc_corrected=None,
                       A=None, B=None, H2S=None, CO2=None, N2=None):
        if Pr is None:
            self.calc_Pr(P, Ppc_corrected, sg, Tpc, Ppc, e_correction, Tpc_corrected, A, B, H2S, CO2)
        else:
            self.Pr = Pr

    def _initialize_Tr(self, Tr, T, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None, B=None, H2S=None,
                       CO2=None, N2=None):
        if Tr is None:
            self.calc_Tr(T, Tpc_corrected, sg, Tpc, e_correction, A, B, H2S, CO2)
        else:
            self.Tr = Tr

    def _check_missing_P(self, P):
        if P is None:
            raise TypeError("Missing a required argument, P (gas pressure, psia)")
        self.P = P

    def _check_missing_T(self, _T):
        if _T is None:
            raise TypeError("Missing a required argument, T (gas temperature, °F)")
        self._T = _T

    def _check_invalid_mode(self, mode):
        if mode != 'sutton' and mode != 'piper':
            raise TypeError("Invalid optional argument, mode (calculation method), input either 'sutton', 'piper'")
        self.mode = mode

    def _redundant_argument_check_Tpc_corrected(self, Tpc_corrected=None, sg=None, Tpc=None, e_correction=None, A=None,
                                                B=None, H2S=None, CO2=None):
        if Tpc_corrected is not None:
            if sg is not None:
                raise TypeError("Redundant arguments Tpc_corrected and sg, input only one of them")
            if Tpc is not None:
                raise TypeError("Redundant arguments Tpc_corrected and Tpc, input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments Tpc_corrected and H2S, input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments Tpc_corrected and CO2, input only one of them")
            if A is not None:
                raise TypeError("Redundant arguments Tpc_corrected and A, input only one of them")
            if B is not None:
                raise TypeError("Redundant arguments Tpc_corrected and B, input only one of them")
            if e_correction is not None:
                raise TypeError("Redundant arguments Tpc_corrected and e_correction, input only one of them")

    def _redundant_argument_check_Ppc_corrected(self, Ppc_corrected=None, sg=None, Tpc=None, Ppc=None,
                                                e_correction=None, Tpc_corrected=None, A=None, B=None, H2S=None,
                                                CO2=None):
        if Ppc_corrected is not None:
            if Ppc is not None:
                raise TypeError("Redundant arguments Ppc_corrected and Ppc, input only one of them")
            if Tpc_corrected is not None:
                raise TypeError("Redundant arguments Ppc_corrected and Tpc_corrected, input only one of them")
            self._redundant_argument_check_Tpc_corrected(sg=sg, Tpc=Tpc, H2S=H2S, CO2=CO2, A=A, B=B,
                                                         e_correction=e_correction)

    def _redundant_argument_check_J_or_K(self, sg=None, J=None, K=None, H2S=None, CO2=None, N2=None):
        if J is not None:
            if sg is not None:
                raise TypeError("Redundant arguments J and sg, input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments J and H2S, input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments J and CO2, input only one of them")
            if N2 is not None:
                raise TypeError("Redundant arguments J and N2, input only one of them")
        if K is not None:
            if sg is not None:
                raise TypeError("Redundant arguments K and sg, input only one of them")
            if H2S is not None:
                raise TypeError("Redundant arguments K and H2S, input only one of them")
            if CO2 is not None:
                raise TypeError("Redundant arguments K and CO2, input only one of them")
            if N2 is not None:
                raise TypeError("Redundant arguments K and N2, input only one of them")

    def _redundant_argument_check_Tpc(self, Tpc=None, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if self.mode == 'piper':
            if Tpc is not None:
                if sg is not None:
                    raise TypeError("Redundant arguments Tpc and sg, input only one of them")
                if J is not None:
                    raise TypeError("Redundant arguments Tpc and J, input only one of them")
                if K is not None:
                    raise TypeError("Redundant arguments Tpc and K, input only one of them")
                self._redundant_argument_check_J_or_K(J=J, K=K, H2S=H2S, CO2=CO2, N2=N2)

    def _redundant_argument_check_Ppc(self, Ppc=None, Tpc=None, sg=None, H2S=None, CO2=None, N2=None, J=None, K=None):
        if self.mode == 'piper':
            if Ppc is not None:
                self._redundant_argument_check_Tpc(Tpc=Tpc, sg=sg, H2S=H2S, CO2=CO2, N2=N2, J=J, K=K)

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
                z_obj = piper()
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

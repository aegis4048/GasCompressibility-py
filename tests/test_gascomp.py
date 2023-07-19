import unittest
import sys

sys.path.append('.')
from gascompressibility.pseudocritical import Sutton
from gascompressibility.pseudocritical import Piper
from gascompressibility import calc_z

# Documents\GasCompressibiltiyFactor-py>python -m unittest tests.test_gascomp
# python -m unittest discover .

""" Test print script
def tround(a, n):
    if a is not None:
        return round(a, n)
    return None  
n = 4

        instance = Piper()
        result = instance.calc_K(sg=0.7)
        a = 'self.assertAlmostEqual(instance.P, %s, places=3)' % tround(instance.P, n)
        b = 'self.assertAlmostEqual(instance.T, %s, places=3)' % tround(instance.T, n)
        c = 'self.assertAlmostEqual(instance.J, %s, places=3)' % tround(instance.J, n)
        d = 'self.assertAlmostEqual(instance.K, %s, places=3)' % tround(instance.K, n)
        e = 'self.assertAlmostEqual(instance.Ppc, %s, places=3)' % tround(instance.Ppc, n)
        f = 'self.assertAlmostEqual(instance.Tpc, %s, places=3)' % tround(instance.Tpc, n)
        g = 'self.assertAlmostEqual(instance.Pr, %s, places=3)' % tround(instance.Pr, n)
        h = 'self.assertAlmostEqual(instance.Tr, %s, places=3)' % tround(instance.Tr, n)
        i = 'self.assertAlmostEqual(instance.Z, %s, places=3)' % tround(instance.Z, n)
        temp = [a, b, c, d, e, f, g, h, i]
        for item in temp:
            if 'None' in item:
                pass
            else:
                print(item)
"""


class Test_Sutton(unittest.TestCase):

    def test_calc_Ppc(self):
        instance = Sutton()
        result = instance.calc_Ppc(sg=0.7)
        self.assertAlmostEqual(result, 663.2869, places=3)
        self.assertAlmostEqual(instance.Ppc, 663.287, places=3)

        print('calc_Ppc passed (mode="Sutton")')

        instance = Piper()
        result = instance.calc_Ppc(Tpc=373.6, J=0.4995)
        self.assertEqual(instance.Tpc, 373.6)
        self.assertEqual(instance.J, 0.4995)
        self.assertAlmostEqual(instance.Ppc, 747.9479, places=3)
        self.assertAlmostEqual(result, 747.9479, places=3)

        instance = Piper()
        result = instance.calc_Ppc(K=13.661, J=0.4995)
        self.assertEqual(instance.K, 13.661)
        self.assertEqual(instance.J, 0.4995)
        self.assertAlmostEqual(instance.Ppc, 747.9869, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6195, places=3)
        self.assertAlmostEqual(result, 747.9869, places=3)

        instance = Piper()
        result = instance.calc_Ppc(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(instance.J, 0.4995, places=3)
        self.assertAlmostEqual(instance.K, 13.6612, places=3)
        self.assertAlmostEqual(instance.Ppc, 747.9468, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6153, places=3)
        self.assertAlmostEqual(result, 747.9468, places=3)

        print('calc_Ppc passed (mode="Piper")')

    def test_calc_Tpc(self):
        instance = Sutton()
        result = instance.calc_Tpc(sg=0.7)
        self.assertAlmostEqual(result, 377.59, places=1)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        print('calc_Tpc passed (mode="Sutton")')

        instance = Piper()
        result = instance.calc_Tpc(K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 373.6194, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6195, places=3)
        self.assertEqual(instance.K, 13.661)
        self.assertEqual(instance.J, 0.4995)

        instance = Piper()
        result = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 373.6152, places=3)
        self.assertAlmostEqual(instance.J, 0.4995, places=3)
        self.assertAlmostEqual(instance.K, 13.6612, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6153, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0)

        instance = Piper()
        result = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0.5)
        self.assertAlmostEqual(result, 232.7950, places=3)
        self.assertAlmostEqual(instance.J, 0.3472, places=3)
        self.assertAlmostEqual(instance.K, 8.9906, places=3)
        self.assertAlmostEqual(instance.Tpc, 232.795, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0.5)

        print('calc_Tpc passed (mode="Piper")')

    def test_calc_J(self):
        instance = Piper()
        result = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 0.4995, places=3)
        self.assertAlmostEqual(instance.J, 0.4995, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0)

        instance = Piper()
        result = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result, 0.4690, places=3)
        self.assertAlmostEqual(instance.J, 0.4691, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0.1)

        instance = Piper()
        result = instance.calc_J(sg=0.7)
        self.assertAlmostEqual(result, 0.5622, places=3)
        self.assertAlmostEqual(instance.J, 0.5622, places=3)
        self.assertEqual(instance.sg, 0.7)

        print('calc_J passed')

    def test_calc_K(self):
        instance = Piper()
        result = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 13.6612, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0)

        instance = Piper()
        result = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result, 12.7270, places=3)
        self.assertAlmostEqual(instance.K, 12.7271, places=3)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.N2, 0.1)

        instance = Piper()
        result = instance.calc_K(sg=0.7)
        self.assertAlmostEqual(result, 14.4508, places=3)
        self.assertAlmostEqual(instance.K, 14.4508, places=3)
        self.assertEqual(instance.sg, 0.7)

        print('calc_K passed')

    def test_calc_A(self):
        instance = Sutton()
        result = instance._calc_A(H2S=0.07, CO2=0.1)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(result, 0.17)

        instance = Sutton()
        result = instance._calc_A(H2S=0, CO2=0)
        self.assertEqual(instance.H2S, 0)
        self.assertEqual(instance.CO2, 0)
        self.assertEqual(result, 0)

        instance = Sutton()
        result = instance._calc_A()
        self.assertEqual(result, 0)

        print('calc_A passed')

    def test_calc_B(self):
        instance = Sutton()
        result = instance._calc_B(H2S=0.07)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(result, 0.07)

        instance = Sutton()
        result = instance._calc_B(H2S=0)
        self.assertEqual(instance.H2S, 0)
        self.assertEqual(result, 0)

        instance = Sutton()
        result = instance._calc_B()
        self.assertEqual(result, 0)

        print('calc_B passed')

    def test_calc_e_correction(self):
        instance = Sutton()
        result = instance.calc_e_correction()
        self.assertEqual(instance.A, 0)
        self.assertEqual(instance.B, 0)
        self.assertEqual(result, 0)

        instance = Sutton()
        result = instance.calc_e_correction(H2S=0.07, CO2=0.1)
        self.assertEqual(instance.A, 0.17)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result, 21.277, places=2)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)

        instance = Sutton()
        result = instance.calc_e_correction(CO2=0.1)
        self.assertEqual(instance.A, 0.1)
        self.assertEqual(instance.B, 0)
        self.assertAlmostEqual(result, 12.092, places=2)
        self.assertAlmostEqual(instance.e_correction, 12.0928, places=3)

        instance = Sutton()
        result = instance.calc_e_correction(H2S=0.07)
        self.assertEqual(instance.A, 0.07)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result, 13.223, places=2)
        self.assertAlmostEqual(instance.e_correction, 13.2237, places=3)

        print('calc_e_correction passed')

    def test_calc_Tpc_corrected(self):
        instance = Sutton()
        result = instance.calc_Tpc_corrected(sg=0.7)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 377.59, places=1)
        self.assertAlmostEqual(instance.Tpc_corrected, 377.59, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 356.31, places=1)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.3122, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, H2S=0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 364.36, places=1)
        self.assertAlmostEqual(instance.e_correction, 13.2237, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 364.3663, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, e_correction=21.278)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 356.31, places=1)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.312, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Tpc_corrected(Tpc=377.59, e_correction=21.278)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 356.31, places=1)
        self.assertAlmostEqual(instance.e_correction, 21.278, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.312, places=3)

        instance = Sutton()
        result = instance.calc_Tpc_corrected(Tpc=300)
        self.assertEqual(instance.Tpc, 300)
        self.assertEqual(result, 300)
        self.assertAlmostEqual(instance.Tpc_corrected, 300, places=3)

        with self.assertRaises(TypeError):
            Sutton().calc_Tpc_corrected(sg=0.7, Tpc=1)

        print('calc_Tpc_corrected passed')

    def test_calc_Ppc_corrected(self):
        instance = Sutton()
        result = instance.calc_Ppc_corrected(sg=0.7)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 663.289, places=2)
        self.assertAlmostEqual(instance.Ppc_corrected, 663.287, places=3)
        self.assertAlmostEqual(instance.Ppc, 663.287, places=3)

        instance = Sutton()
        result = instance.calc_Ppc_corrected(sg=0.7, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 628.214, places=2)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2143, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.3122, places=3)
        self.assertAlmostEqual(instance.Ppc, 663.287, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Ppc_corrected(sg=0.7, e_correction=21.27, H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.e_correction, 21.27)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 628.227, places=2)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2272, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.32, places=3)
        self.assertAlmostEqual(instance.Ppc, 663.287, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Ppc_corrected(Ppc=663.29, e_correction=21.278, Tpc_corrected=356.31, Tpc=377.59,
                                             H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertEqual(instance.Tpc_corrected, 356.31)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 628.213, places=2)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2133, places=3)

        instance = Sutton()
        result = instance.calc_Ppc_corrected(Ppc=663.29, Tpc_corrected=356.31, sg=0.7, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.Tpc_corrected, 356.31)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.B, 0)
        self.assertEqual(instance.H2S, 0)
        self.assertAlmostEqual(result, 625.908, places=2)
        self.assertAlmostEqual(instance.e_correction, 0.0, places=3)
        self.assertAlmostEqual(instance.Ppc_corrected, 625.9087, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)

        instance = Sutton()
        result = instance.calc_Ppc_corrected(Ppc=300)
        self.assertEqual(instance.Ppc_corrected, 300)
        self.assertEqual(result, 300)
        self.assertAlmostEqual(instance.Ppc_corrected, 300, places=3)
        self.assertAlmostEqual(instance.Ppc, 300, places=3)
        self.assertAlmostEqual(result, 300, places=2)

        print('calc_Ppc_corrected passed')

    def test_calc_Tr(self):
        instance = Sutton()
        result = instance.calc_Tr(sg=0.7, T=75, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 1.5005, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.3122, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)
        self.assertAlmostEqual(instance.Tr, 1.5006, places=3)

        instance = Sutton()
        result = instance.calc_Tr(Tpc=377.59, T=75)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.T_f, 75)
        self.assertAlmostEqual(result, 1.4160, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 377.59, places=3)
        self.assertAlmostEqual(instance.Tr, 1.416, places=3)

        instance = Sutton()
        result = instance.calc_Tr(Tpc=377.59, T=75, e_correction=21.278)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 1.5005, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.312, places=3)
        self.assertAlmostEqual(instance.Tr, 1.5006, places=3)

        instance = Sutton()
        result = instance.calc_Tr(Tpc_corrected=10, T=10)
        self.assertEqual(instance.T_f, 10)
        self.assertEqual(instance.Tpc_corrected, 10)
        self.assertAlmostEqual(result, 46.967, places=2)
        self.assertAlmostEqual(instance.T, 469.67, places=3)
        self.assertAlmostEqual(instance.Tr, 46.967, places=3)

        print('calc_Tr passed (mode="Sutton")')

        instance = Piper()
        result = instance.calc_Tr(T=75, sg=0.7, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 1.4310, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.J, 0.4995, places=3)
        self.assertAlmostEqual(instance.K, 13.6612, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6153, places=3)
        self.assertAlmostEqual(instance.Tr, 1.4311, places=3)

        instance = Piper()
        result = instance.calc_Tr(T=75, K=13.661, J=0.4995)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.K, 13.661)
        self.assertEqual(instance.J, 0.4995)
        self.assertAlmostEqual(result, 1.4310, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.Tpc, 373.6195, places=3)
        self.assertAlmostEqual(instance.Tr, 1.4311, places=3)

        instance = Piper()
        result = instance.calc_Tr(T=75, Tpc=373.6)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.Tpc, 373.6)
        self.assertAlmostEqual(result, 1.4311, places=3)
        self.assertAlmostEqual(instance.T, 534.67, places=3)
        self.assertAlmostEqual(instance.Tr, 1.4311, places=3)

        print('calc_Tr passed (mode="Piper")')

    def test_calc_Pr(self):
        instance = Sutton()
        result = instance.calc_Pr(sg=0.7, P=1995.3, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 3.1995, places=3)
        self.assertAlmostEqual(instance.P, 2010, places=3)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2143, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.3122, places=3)
        self.assertAlmostEqual(instance.Ppc, 663.287, places=3)
        self.assertAlmostEqual(instance.Tpc, 377.59, places=3)
        self.assertAlmostEqual(instance.Pr, 3.1995, places=3)

        instance = Sutton()
        result = instance.calc_Pr(Ppc=663.29, Tpc=377.59, P=1995.3, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 3.1995, places=3)
        self.assertAlmostEqual(instance.P, 2010, places=3)
        self.assertAlmostEqual(instance.e_correction, 21.2778, places=3)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2171, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.3122, places=3)
        self.assertAlmostEqual(instance.Pr, 3.1995, places=3)

        instance = Sutton()
        result = instance.calc_Pr(Ppc_corrected=628.21, P=1995.3)
        self.assertEqual(instance.Ppc_corrected, 628.21)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 3.1995, places=3)
        self.assertAlmostEqual(instance.Pr, 3.1996, places=3)

        instance = Sutton()
        result = instance.calc_Pr(Ppc=663.29, P=1995.3, e_correction=21.278, H2S=0.07, Tpc=377.59, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertAlmostEqual(result, 3.1995, places=3)
        self.assertAlmostEqual(instance.Ppc_corrected, 628.2168, places=3)
        self.assertAlmostEqual(instance.Tpc_corrected, 356.312, places=3)
        self.assertAlmostEqual(instance.Pr, 3.1995, places=3)

        print('calc_Pr passed (mode="Sutton")')

        instance = Piper()
        result = instance.calc_Pr(Tpc=373.6, sg=0.7, P=1995.3, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.Tpc, 373.6)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 2.6874, places=3)
        self.assertAlmostEqual(instance.J, 0.4995, places=3)
        self.assertAlmostEqual(instance.Ppc, 747.9162, places=3)
        self.assertAlmostEqual(instance.Pr, 2.6875, places=3)

        instance = Piper()
        result = instance.calc_Pr(Ppc=747.9, P=1995.3)
        self.assertEqual(instance.Ppc, 747.9)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 2.6875, places=3)
        self.assertAlmostEqual(instance.Pr, 2.6875, places=3)

        instance = Piper()
        result = instance.calc_Pr(P=1995.3, K=4, J=2)
        self.assertEqual(instance.K, 4)
        self.assertEqual(instance.J, 2)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 502.5, places=1)
        self.assertAlmostEqual(instance.Ppc, 4.0, places=3)
        self.assertAlmostEqual(instance.Tpc, 8.0, places=3)
        self.assertAlmostEqual(instance.Pr, 502.5, places=3)

        instance = Piper()
        result = instance.calc_Pr(P=1995.3, sg=2)
        self.assertEqual(instance.sg, 2)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 3.8686, places=3)
        self.assertAlmostEqual(instance.J, 1.1328, places=3)
        self.assertAlmostEqual(instance.K, 25.8212, places=3)
        self.assertAlmostEqual(instance.Ppc, 519.5617, places=3)
        self.assertAlmostEqual(instance.Tpc, 588.5658, places=3)
        self.assertAlmostEqual(instance.Pr, 3.8686, places=3)

        instance = Piper()
        result = instance.calc_Pr(P=1995.3, Tpc=373.6, J=0.4995)
        self.assertEqual(instance.Tpc, 373.6)
        self.assertEqual(instance.J, 0.4995)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 2.6873, places=3)
        self.assertAlmostEqual(instance.Ppc, 747.9479, places=3)
        self.assertAlmostEqual(instance.Pr, 2.6874, places=3)

        print('calc_Pr passed (mode="Piper")')

    def test_calc_z(self):

        ps_props = calc_z(P=1995.3, T=75, CO2=0.1, H2S=0.07, sg=0.7, ps_props=True, zmodel='DAK', pmodel='sutton')

        self.assertAlmostEqual(ps_props['z'], 0.7730, places=3)
        self.assertAlmostEqual(ps_props['e_correction'], 21.2778, places=3)
        self.assertAlmostEqual(ps_props['Ppc_corrected'], 628.2143, places=3)
        self.assertAlmostEqual(ps_props['Tpc_corrected'], 356.3122, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 663.287, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 377.59, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 3.1995, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.5006, places=3)

        ps_props = calc_z(P=1995.3, T=75, Ppc=747.9, Tpc=373.6, ps_props=True, zmodel='DAK', pmodel='sutton')

        self.assertAlmostEqual(ps_props['z'], 0.7418, places=3)
        self.assertEqual(ps_props['Ppc'], None)
        self.assertEqual(ps_props['Tpc'], None)
        self.assertAlmostEqual(ps_props['e_correction'], 0.0, places=3)
        self.assertAlmostEqual(ps_props['Ppc_corrected'], 747.9, places=3)
        self.assertAlmostEqual(ps_props['Tpc_corrected'], 373.6, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 2.6875, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.4311, places=3)

        ps_props = calc_z(Pr=3.1995, T=75, Tpc=377.59, e_correction=21.278, ignore_conflict=True, ps_props=True, zmodel='DAK', pmodel='sutton')

        self.assertAlmostEqual(ps_props['z'], 0.7730, places=3)
        self.assertAlmostEqual(ps_props['Tpc_corrected'], 356.312, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.5006, places=3)

        ps_props = calc_z(Tpc_corrected=356.31, sg=0.7, P=1995.3, T=75, H2S=0.07, CO2=0.1, ignore_conflict=True, ps_props=True, zmodel='DAK', pmodel='sutton')

        self.assertAlmostEqual(ps_props['z'], 0.7730, places=3)
        self.assertAlmostEqual(ps_props['e_correction'], 21.2778, places=3)
        self.assertAlmostEqual(ps_props['Ppc_corrected'], 628.2104, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 663.287, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 377.59, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 3.1996, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.5006, places=3)

        print('calc_z passed (mode="Sutton")')

        ps_props = calc_z(P=1995.3, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.7418, places=3)
        self.assertAlmostEqual(ps_props['J'], 0.4995, places=3)
        self.assertAlmostEqual(ps_props['K'], 13.6612, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 747.9468, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 373.6153, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 2.6874, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.4311, places=3)

        ps_props = calc_z(P=1995.3, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0.1, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.8093, places=3)
        self.assertAlmostEqual(ps_props['J'], 0.4691, places=3)
        self.assertAlmostEqual(ps_props['K'], 12.7271, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 736.2064, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 345.3259, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 2.7302, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.5483, places=3)

        ps_props = calc_z(P=1995.3, T=75, K=13.661, J=0.4995, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.7418, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 747.9869, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 373.6195, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 2.6872, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.4311, places=3)

        ps_props = calc_z(P=1995.3, T=75, Tpc=373.6, J=0.4995, ignore_conflict=True, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.7418, places=3)
        self.assertAlmostEqual(ps_props['Ppc'], 747.9479, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 2.6874, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.4311, places=3)

        ps_props = calc_z(T=75, Pr=2.687, K=13.661, J=0.4995, ignore_conflict=True, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.7418, places=3)
        self.assertAlmostEqual(ps_props['Tpc'], 373.6195, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.4311, places=3)

        ps_props = calc_z(P=1995.3, T=75, Ppc=663.28, Tpc=377.59, ignore_conflict=True, ps_props=True, zmodel='DAK', pmodel='piper')

        self.assertAlmostEqual(ps_props['z'], 0.7207, places=3)
        self.assertAlmostEqual(ps_props['Pr'], 3.0304, places=3)
        self.assertAlmostEqual(ps_props['Tr'], 1.416, places=3)

        print('calc_z passed (mode="Piper")')

    def test_calc_z_models(self):

        result = calc_z(zmodel="hall_yarborough", Pr=3.1995, Tr=1.5006, guess=0.9)
        self.assertAlmostEqual(result, 0.7714, places=3)
        print('calc_z_models passed (model="hall_yarborough")')

        result = calc_z(zmodel="DAK", Pr=3.1995, Tr=1.5006, guess=0.9)
        self.assertAlmostEqual(result, 0.7730, places=3)
        print('calc_z_models passed (model="DAK")')

        result = calc_z(zmodel="londono", Pr=3.1995, Tr=1.5006, guess=0.9)
        self.assertAlmostEqual(result, 0.7754, places=3)
        print('calc_z_models passed (model="londono")')

        result = calc_z(zmodel="kareem", Pr=3.1995, Tr=1.5006)
        self.assertAlmostEqual(result, 0.7667, places=3)
        print('calc_z_models passed (model="kareem")')

        result = calc_z(sg=0.7, H2S=0.07, CO2=0.1, P=2010-14.7, T=75, guess=0.9, zmodel='DAK', pmodel='sutton')
        self.assertAlmostEqual(result, 0.7730, places=3)

        result = calc_z(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1, P=2010-14.7, guess=0.9, T=75, zmodel='DAK', pmodel='piper')
        self.assertAlmostEqual(result, 0.8093, places=3)

        result = calc_z(sg=0.7, H2S=0.07, CO2=0.1, P=2010-14.7, T=75, zmodel='kareem', pmodel='piper')
        self.assertAlmostEqual(result, 0.7319, places=3)

        result = calc_z(sg=0.7, H2S=0.07, CO2=0.1, P=2010-14.7, T=75, N2=0.1, zmodel='hall_yarborough', pmodel='piper')
        self.assertAlmostEqual(result, 0.8084, places=3)

        with self.assertRaises(TypeError):
            calc_z(sg=0.7, H2S=0.07, CO2=0.1, P=2010 - 14.7, Ppc=135, T=75, zmodel='DAK', pmodel='piper')

        with self.assertRaises(TypeError):
            calc_z(sg=0.7, H2S=0.07, CO2=0.1, P=2010 - 14.7, Pr=1.5, T=75, zmodel='DAK', pmodel='sutton')

        with self.assertRaises(KeyError):
            calc_z(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1, P=2010 - 14.7, T=75, guess=0.9, zmodel='kareem', pmodel='piper')





if __name__ == '__main__':
    unittest.main()


# Documents\GasCompressibiltiyFactor-py>python -m unittest tests.test_gascomp
# python -m unittest discover .
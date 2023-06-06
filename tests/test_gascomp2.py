import unittest
import sys
sys.path.append('.')
from gascompressibility import sutton
from gascompressibility import piper




print('------------ Sutton"s Pseuodo-critical property ------------')

class Test_sutton(unittest.TestCase):

    def test_calc_Ppc(self):
        
        instance = sutton()
        result = instance.calc_Ppc(sg=0.7)
        self.assertAlmostEqual(result, 663.2869, places=3)

        print('calc_Ppc passed (mode="sutton")')

        instance = piper()
        result = instance.calc_Ppc(Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result, 747.9479, places=3)

        instance = piper()
        result = instance.calc_Ppc(K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 747.9869, places=3)

        instance = piper()
        result = instance.calc_Ppc(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertAlmostEqual(result, 747.9468, places=3)

        print('calc_Ppc passed (mode="piper")')

    def test_calc_Tpc(self):
        
        instance = sutton()
        result = instance.calc_Tpc(sg=0.7)
        self.assertAlmostEqual(result, 377.59, places=1)

        print('calc_Tpc passed (mode="sutton")')
        
        instance = piper()
        result = instance.calc_Tpc(K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 373.6194, places=3)

        instance = piper()
        result = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 373.6152, places=3)

        instance = piper()
        result = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0.5)
        self.assertAlmostEqual(result, 232.7950, places=3)

        print('calc_Tpc passed (mode="piper")')
        
    def test_calc_J(self):
        
        instance = piper()
        result = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 0.4995, places=3)

        instance = piper()
        result = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result, 0.4690, places=3)

        instance = piper()
        result = instance.calc_J(sg=0.7)
        self.assertAlmostEqual(result, 0.5622, places=3)

        print('calc_J passed')

    def test_calc_K(self):
        
        instance = piper()
        result = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result, 13.6612, places=3)

        instance = piper()
        result = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result, 12.7270, places=3)

        instance = piper()
        result = instance.calc_K(sg=0.7)
        self.assertAlmostEqual(result, 14.4508, places=3)

        print('calc_K passed')

    def test_calc_A(self):
        
        instance = sutton()
        result = instance._calc_A(H2S=0.07, CO2=0.1)
        self.assertEqual(result, 0.17)

        instance = sutton()
        result = instance._calc_A(H2S=0, CO2=0)
        self.assertEqual(result, 0)

        instance = sutton()
        result = instance._calc_A()
        self.assertEqual(result, 0)

        print('calc_A passed')

    def test_calc_B(self):
        
        instance = sutton()
        result = instance._calc_B(H2S=0.07)
        self.assertEqual(result, 0.07)

        instance = sutton()
        result = instance._calc_B(H2S=0)
        self.assertEqual(result, 0)

        instance = sutton()
        result = instance._calc_B()
        self.assertEqual(result, 0)

        print('calc_B passed')

    def test_calc_e_correction(self):

        instance = sutton()
        result = instance.calc_e_correction()
        self.assertEqual(instance.A, 0)
        self.assertEqual(instance.B, 0)
        self.assertEqual(result, 0)

        instance = sutton()
        result = instance.calc_e_correction(H2S=0.07, CO2=0.1)
        self.assertEqual(instance.A, 0.17)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result, 21.277, places=2)

        instance = sutton()
        result = instance.calc_e_correction(CO2=0.1)
        self.assertEqual(instance.A, 0.1)
        self.assertEqual(instance.B, 0)
        self.assertAlmostEqual(result, 12.092, places=2)

        instance = sutton()
        result = instance.calc_e_correction(H2S=0.07)
        self.assertEqual(instance.A, 0.07)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result, 13.223, places=2)

        print('calc_e_correction passed')

    def test_calc_Tpc_corrected(self):

        instance = sutton()
        result = instance.calc_Tpc_corrected(sg=0.7)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 377.59, places=1)

        instance = sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 356.31, places=1)

        instance = sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, H2S=0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 364.36, places=1)

        instance = sutton()
        result = instance.calc_Tpc_corrected(sg=0.7, e_correction=21.278)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 356.31, places=1)

        instance = sutton()
        result = instance.calc_Tpc_corrected(Tpc=377.59, e_correction=21.278)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 356.31, places=1)

        instance = sutton()
        result = instance.calc_Tpc_corrected(Tpc=300)
        self.assertEqual(instance.Tpc, 300)
        self.assertEqual(result, 300)

        print('calc_Tpc_corrected passed')

    def test_calc_Ppc_corrected(self):

        instance = sutton()
        result = instance.calc_Ppc_corrected(sg=0.7)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 663.289, places=2)

        instance = sutton()
        result = instance.calc_Ppc_corrected(sg=0.7, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 628.214, places=2)

        instance = sutton()
        result = instance.calc_Ppc_corrected(sg=0.7, e_correction=21.27, H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.e_correction, 21.27)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 628.227, places=2)

        instance = sutton()
        result = instance.calc_Ppc_corrected(Ppc=663.29, e_correction=21.278, Tpc_corrected=356.31, Tpc=377.59, H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertEqual(instance.Tpc_corrected, 356.31)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.H2S, 0.07)
        self.assertAlmostEqual(result, 628.213, places=2)

        instance = sutton()
        result = instance.calc_Ppc_corrected(Ppc=663.29, Tpc_corrected=356.31, sg=0.7, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.Tpc_corrected, 356.31)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 625.908, places=2)

        instance = sutton()
        result = instance.calc_Ppc_corrected(Ppc=300)
        self.assertEqual(instance.Ppc_corrected, 300)
        self.assertEqual(result, 300)

        print('calc_Ppc_corrected passed')

    def test_calc_Tr(self):

        instance = sutton()
        result = instance.calc_Tr(sg=0.7, T=75, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 1.5005, places=3)

        instance = sutton()
        result = instance.calc_Tr(Tpc=377.59, T=75)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.T_f, 75)
        self.assertAlmostEqual(result, 1.4160, places=3)

        instance = sutton()
        result = instance.calc_Tr(Tpc=377.59, T=75, e_correction=21.278)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 1.5005, places=3)

        instance = sutton()
        result = instance.calc_Tr(Tpc_corrected=10, T=10)
        self.assertEqual(instance.T_f, 10)
        self.assertEqual(instance.Tpc_corrected, 10)
        self.assertAlmostEqual(result, 46.967, places=2)

        print('calc_Tr passed (mode="sutton")')
        
        instance = piper()
        result = instance.calc_Tr(T=75, sg=0.7, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result, 1.4310, places=3)

        instance = piper()
        result = instance.calc_Tr(T=75, K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 1.4310, places=3)

        instance = piper()
        result = instance.calc_Tr(T=75, Tpc=373.6)
        self.assertAlmostEqual(result, 1.4311, places=3)

        print('calc_Tr passed (mode="piper")')
    def test_calc_Pr(self):

        instance = sutton()
        result = instance.calc_Pr(sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.sg, 0.7)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 3.1995, places=3)

        instance = sutton()
        result = instance.calc_Pr(Ppc=663.29, Tpc=377.59, P=2010, H2S=0.07, CO2=0.1)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.CO2, 0.1)
        self.assertAlmostEqual(result, 3.1995, places=3)

        instance = sutton()
        result = instance.calc_Pr(Ppc_corrected=628.21, P=2010)
        self.assertEqual(instance.Ppc_corrected, 628.21)
        self.assertEqual(instance.P, 2010)
        self.assertAlmostEqual(result, 3.1995, places=3)

        instance = sutton()
        result = instance.calc_Pr(Ppc=663.29, P=2010, e_correction=21.278, H2S=0.07, Tpc=377.59, ignore_conflict=True)
        self.assertEqual(instance.Ppc, 663.29)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertAlmostEqual(result, 3.1995, places=3)

        print('calc_Pr passed (mode="sutton")')
        
        instance = piper()
        result = instance.calc_Pr(Tpc=373.6, sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result, 2.6874, places=3)

        instance = piper()
        result = instance.calc_Pr(Ppc=747.9, P=2010)
        self.assertAlmostEqual(result, 2.6875, places=3)

        instance = piper()
        result = instance.calc_Pr(P=2010, K=4, J=2)
        self.assertAlmostEqual(result, 502.5, places=1)

        instance = piper()
        result = instance.calc_Pr(P=2010, sg=2)
        self.assertAlmostEqual(result, 3.8686, places=3)

        instance = piper()
        result = instance.calc_Pr(P=2010, Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result, 2.6873, places=3)

        print('calc_Pr passed (mode="piper")')

    def test_calc_Z(self):

        instance = sutton()
        result = instance.calc_Z(P=2010, T=75, CO2=0.1, H2S=0.07, sg=0.7)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.CO2, 0.1)
        self.assertEqual(instance.H2S, 0.07)
        self.assertEqual(instance.sg, 0.7)
        self.assertAlmostEqual(result, 0.7730, places=3)

        instance = sutton()
        result = instance.calc_Z(P=2010, T=75, Ppc=747.9, Tpc=373.6)
        self.assertEqual(instance.P, 2010)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.Ppc, 747.9)
        self.assertEqual(instance.Tpc, 373.6)
        self.assertAlmostEqual(result, 0.7418, places=3)

        instance = sutton()
        result = instance.calc_Z(Pr=3.1995, T=75, Tpc=377.59, e_correction=21.278, ignore_conflict=True)
        self.assertEqual(instance.Pr, 3.1995)
        self.assertEqual(instance.T_f, 75)
        self.assertEqual(instance.Tpc, 377.59)
        self.assertEqual(instance.e_correction, 21.278)
        self.assertAlmostEqual(result, 0.7730, places=3)

        print('calc_Z passed (mode="sutton")')

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result, 0.8093, places=3)

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, sg=0.7, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result, 0.7418, places=3)

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 0.7418, places=3)

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result, 0.7418, places=3)

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, Pr=2.687, K=13.661, J=0.4995)
        self.assertAlmostEqual(result, 0.7418, places=3)

        instance = piper()
        result = instance.calc_Z(P=2010, T=75, Ppc=663.28, Tpc=377.59)
        self.assertAlmostEqual(result, 0.7207, places=3)

        print('calc_Z passed (mode="piper")')


if __name__ == '__main__':
    unittest.main()

# Documents\GasCompressibiltiyFactor-py>python -m unittest tests.test_gascomp2

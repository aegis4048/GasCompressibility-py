import unittest
import sys
sys.path.append('.')
from gascompressibility import sutton


class Test_sutton(unittest.TestCase):

    def test_calc_Ppc(self):

        result1 = sutton().calc_Ppc(sg=0.7)
        self.assertAlmostEqual(result1, 663.2869, places=3)

        print('calc_Ppc passed (mode="sutton")')

    def test_calc_Tpc(self):

        result1 = sutton().calc_Tpc(sg=0.7)
        self.assertAlmostEqual(result1, 377.59, places=1)

        print('calc_Tpc passed (mode="sutton")')

    def test_calc_A(self):

        result1 = sutton()._calc_A(H2S=0.07, CO2=0.1)
        self.assertEqual(result1, 0.17)

        result2 = sutton()._calc_A(H2S=0, CO2=0)
        self.assertEqual(result2, 0)

        result3 = sutton()._calc_A()
        self.assertEqual(result3, 0)

        print('calc_A passed')

    def test_calc_B(self):

        result1 = sutton()._calc_B(H2S=0.07)
        self.assertEqual(result1, 0.07)

        result2 = sutton()._calc_B(H2S=0)
        self.assertEqual(result2, 0)

        result3 = sutton()._calc_B()
        self.assertEqual(result3, 0)

        print('calc_B passed')

    def test_calc_e_correction(self):

        instance1 = sutton()
        result1 = instance1.calc_e_correction()
        self.assertEqual(instance1.A, 0)
        self.assertEqual(instance1.B, 0)
        self.assertEqual(result1, 0)

        instance2 = sutton()
        result2 = instance2.calc_e_correction(H2S=0.07, CO2=0.1)
        self.assertEqual(instance2.A, 0.17)
        self.assertEqual(instance2.B, 0.07)
        self.assertAlmostEqual(result2, 21.277, places=2)

        instance3 = sutton()
        result3 = instance3.calc_e_correction(CO2=0.1)
        self.assertEqual(instance3.A, 0.1)
        self.assertEqual(instance3.B, 0)
        self.assertAlmostEqual(result3, 12.092, places=2)

        instance4 = sutton()
        result4 = instance4.calc_e_correction(H2S=0.07)
        self.assertEqual(instance4.A, 0.07)
        self.assertEqual(instance4.B, 0.07)
        self.assertAlmostEqual(result4, 13.223, places=2)

        print('calc_e_correction passed')

    def test_calc_Tpc_corrected(self):

        instance1 = sutton()
        result1 = instance1.calc_Tpc_corrected(sg=0.7)
        self.assertEqual(instance1.sg, 0.7)
        self.assertAlmostEqual(result1, 377.59, places=1)

        instance2 = sutton()
        result2 = instance2.calc_Tpc_corrected(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertEqual(instance2.sg, 0.7)
        self.assertEqual(instance2.CO2, 0.1)
        self.assertEqual(instance2.H2S, 0.07)
        self.assertAlmostEqual(result2, 356.31, places=1)

        instance3 = sutton()
        result3 = instance3.calc_Tpc_corrected(sg=0.7, H2S=0.07)
        self.assertEqual(instance3.sg, 0.7)
        self.assertEqual(instance3.H2S, 0.07)
        self.assertAlmostEqual(result3, 364.36, places=1)

        instance4 = sutton()
        result4 = instance4.calc_Tpc_corrected(sg=0.7, e_correction=21.278)
        self.assertEqual(instance4.sg, 0.7)
        self.assertEqual(instance4.e_correction, 21.278)
        self.assertAlmostEqual(result4, 356.31, places=1)

        instance5 = sutton()
        result5 = instance5.calc_Tpc_corrected(Tpc=377.59, e_correction=21.278)
        self.assertEqual(instance5.Tpc, 377.59)
        self.assertEqual(instance5.e_correction, 21.278)
        self.assertAlmostEqual(result5, 356.31, places=1)

        instance6 = sutton()
        result6 = instance6.calc_Tpc_corrected(Tpc=300)
        self.assertEqual(instance6.Tpc, 300)
        self.assertEqual(result6, 300)

        print('calc_Tpc_corrected passed')

    def test_calc_Ppc_corrected(self):

        instance1 = sutton()
        result1 = instance1.calc_Ppc_corrected(sg=0.7)
        self.assertEqual(instance1.sg, 0.7)
        self.assertAlmostEqual(result1, 663.289, places=2)

        instance2 = sutton()
        result2 = instance2.calc_Ppc_corrected(sg=0.7, H2S=0.07, CO2=0.1)
        self.assertEqual(instance2.sg, 0.7)
        self.assertEqual(instance2.H2S, 0.07)
        self.assertEqual(instance2.CO2, 0.1)
        self.assertAlmostEqual(result2, 628.214, places=2)

        instance3 = sutton()
        result3 = instance3.calc_Ppc_corrected(sg=0.7, e_correction=21.27, H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance3.sg, 0.7)
        self.assertEqual(instance3.e_correction, 21.27)
        self.assertEqual(instance3.H2S, 0.07)
        self.assertAlmostEqual(result3, 628.227, places=2)

        instance4 = sutton()
        result4 = instance4.calc_Ppc_corrected(Ppc=663.29, e_correction=21.278, Tpc_corrected=356.31, Tpc=377.59, H2S=0.07, ignore_conflict=True)
        self.assertEqual(instance4.Ppc, 663.29)
        self.assertEqual(instance4.e_correction, 21.278)
        self.assertEqual(instance4.Tpc_corrected, 356.31)
        self.assertEqual(instance4.Tpc, 377.59)
        self.assertEqual(instance4.H2S, 0.07)
        self.assertAlmostEqual(result4, 628.213, places=2)

        instance5 = sutton()
        result5 = instance5.calc_Ppc_corrected(Ppc=663.29, Tpc_corrected=356.31, sg=0.7, ignore_conflict=True)
        self.assertEqual(instance5.Ppc, 663.29)
        self.assertEqual(instance5.Tpc_corrected, 356.31)
        self.assertEqual(instance5.sg, 0.7)
        self.assertAlmostEqual(result5, 625.908, places=2)

        instance6 = sutton()
        result6 = instance6.calc_Ppc_corrected(Ppc=300)
        self.assertEqual(instance6.Ppc_corrected, 300)
        self.assertEqual(result6, 300)

        print('calc_Ppc_corrected passed')

    def test_calc_Tr(self):

        instance1 = sutton()
        result1 = instance1.calc_Tr(sg=0.7, T=75, H2S=0.07, CO2=0.1)
        self.assertEqual(instance1.sg, 0.7)
        self.assertEqual(instance1.T_f, 75)
        self.assertEqual(instance1.H2S, 0.07)
        self.assertEqual(instance1.CO2, 0.1)
        self.assertAlmostEqual(result1, 1.5005, places=3)

        instance2 = sutton()
        result2 = instance2.calc_Tr(Tpc=377.59, T=75)
        self.assertEqual(instance2.Tpc, 377.59)
        self.assertEqual(instance2.T_f, 75)
        self.assertAlmostEqual(result2, 1.4160, places=3)

        instance3 = sutton()
        result3 = instance3.calc_Tr(Tpc=377.59, T=75, e_correction=21.278)
        self.assertEqual(instance3.Tpc, 377.59)
        self.assertEqual(instance3.T_f, 75)
        self.assertEqual(instance3.e_correction, 21.278)
        self.assertAlmostEqual(result3, 1.5005, places=3)

        instance4 = sutton()
        result4 = instance4.calc_Tr(Tpc_corrected=10, T=10)
        self.assertEqual(instance4.T_f, 10)
        self.assertEqual(instance4.Tpc_corrected, 10)
        self.assertAlmostEqual(result4, 46.967, places=2)

        print('calc_Tr passed (mode="sutton")')
    def test_calc_Pr(self):

        instance1 = sutton()
        result1 = instance1.calc_Pr(sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertEqual(instance1.sg, 0.7)
        self.assertEqual(instance1.P, 2010)
        self.assertEqual(instance1.H2S, 0.07)
        self.assertEqual(instance1.CO2, 0.1)
        self.assertAlmostEqual(result1, 3.1995, places=3)

        instance2 = sutton()
        result2 = instance2.calc_Pr(Ppc=663.29, Tpc=377.59, P=2010, H2S=0.07, CO2=0.1)
        self.assertEqual(instance2.Ppc, 663.29)
        self.assertEqual(instance2.Tpc, 377.59)
        self.assertEqual(instance2.P, 2010)
        self.assertEqual(instance2.H2S, 0.07)
        self.assertEqual(instance2.CO2, 0.1)
        self.assertAlmostEqual(result2, 3.1995, places=3)

        instance3 = sutton()
        result3 = instance3.calc_Pr(Ppc_corrected=628.21, P=2010)
        self.assertEqual(instance3.Ppc_corrected, 628.21)
        self.assertEqual(instance3.P, 2010)
        self.assertAlmostEqual(result3, 3.1995, places=3)

        instance4 = sutton()
        result4 = instance4.calc_Pr(Ppc=663.29, P=2010, e_correction=21.278, H2S=0.07, Tpc=377.59, ignore_conflict=True)
        self.assertEqual(instance4.Ppc, 663.29)
        self.assertEqual(instance4.P, 2010)
        self.assertEqual(instance4.e_correction, 21.278)
        self.assertEqual(instance4.H2S, 0.07)
        self.assertEqual(instance4.Tpc, 377.59)
        self.assertAlmostEqual(result4, 3.1995, places=3)

        print('calc_Pr passed (mode="sutton")')

    def test_calc_Z(self):

        instance1 = sutton()
        result1 = instance1.calc_Z(P=2010, T=75, CO2=0.1, H2S=0.07, sg=0.7)
        self.assertEqual(instance1.P, 2010)
        self.assertEqual(instance1.T_f, 75)
        self.assertEqual(instance1.CO2, 0.1)
        self.assertEqual(instance1.H2S, 0.07)
        self.assertEqual(instance1.sg, 0.7)
        self.assertAlmostEqual(result1, 0.7730, places=3)

        instance2 = sutton()
        result2 = instance2.calc_Z(P=2010, T=75, Ppc=747.9, Tpc=373.6)
        self.assertEqual(instance2.P, 2010)
        self.assertEqual(instance2.T_f, 75)
        self.assertEqual(instance2.Ppc, 747.9)
        self.assertEqual(instance2.Tpc, 373.6)
        self.assertAlmostEqual(result2, 0.7418, places=3)

        instance3 = sutton()
        result3 = instance3.calc_Z(Pr=3.1995, T=75, Tpc=377.59, e_correction=21.278, ignore_conflict=True)
        self.assertEqual(instance3.Pr, 3.1995)
        self.assertEqual(instance3.T_f, 75)
        self.assertEqual(instance3.Tpc, 377.59)
        self.assertEqual(instance3.e_correction, 21.278)
        self.assertAlmostEqual(result3, 0.7730, places=3)

        print('calc_Z passed (mode="sutton")')


if __name__ == '__main__':
    unittest.main()

# Documents\GasCompressibiltiyFactor-py>python -m unittest tests.test_gascomp2

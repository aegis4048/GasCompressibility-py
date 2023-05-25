import unittest

from gascompressibility import zfactor


class Test_zfactor(unittest.TestCase):

    def test_calc_Ppc(self):
        instance = zfactor()

        result = instance.calc_Ppc(sg=0.7)

        self.assertAlmostEqual(result, 663.2869, places=3)

        print('calc_Ppc passed')

    def test_calc_Tpc(self):
        instance = zfactor()
        result = instance.calc_Tpc(sg=0.7)
        self.assertAlmostEqual(result, 377.59, places=1)
        print('calc_Tpc passed')

    def test_calc_A(self):
        instance = zfactor()

        result1 = instance.calc_A(H2S=0.07, CO2=0.1)
        self.assertEqual(result1, 0.17)

        result2 = instance.calc_A(H2S=0, CO2=0)
        self.assertEqual(result2, 0)

        result3 = instance.calc_A()
        self.assertEqual(result3, 0)

        print('calc_A passed')

    def test_calc_B(self):
        instance = zfactor()

        result1 = instance.calc_B(H2S=0.07)
        self.assertEqual(result1, 0.07)

        result2 = instance.calc_B(H2S=0)
        self.assertEqual(result2, 0)

        result3 = instance.calc_B()
        self.assertEqual(result3, 0)

        print('calc_B passed')

    def test_calc_e_correction(self):
        instance = zfactor()

        result1 = instance.calc_e_correction()
        self.assertEqual(instance.A, 0)
        self.assertEqual(instance.B, 0)
        self.assertEqual(result1, 0)

        result2 = instance.calc_e_correction(H2S=0.07, CO2=0.1)
        self.assertEqual(instance.A, 0.17)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result2, 21.277, places=2)

        result3 = instance.calc_e_correction(CO2=0.1, B=0.07)
        self.assertEqual(instance.A, 0.17)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result3, 21.277, places=2)

        result4 = instance.calc_e_correction(A=0.17, B=0.07)
        self.assertEqual(instance.A, 0.17)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result4, 21.277, places=2)

        result5 = instance.calc_e_correction(CO2=0.1)
        self.assertEqual(instance.A, 0.1)
        self.assertEqual(instance.B, 0)
        self.assertAlmostEqual(result5, 12.092, places=2)

        result6 = instance.calc_e_correction(H2S=0.07)
        self.assertEqual(instance.A, 0.07)
        self.assertEqual(instance.B, 0.07)
        self.assertAlmostEqual(result6, 13.223, places=2)

        print('calc_e_correction passed')

    def test_calc_Tpc_corrected(self):
        instance = zfactor()

        result1 = instance.calc_Tpc_corrected(sg=0.7)
        self.assertAlmostEqual(result1, 377.59, places=1)

        result2 = instance.calc_Tpc_corrected(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertAlmostEqual(result2, 356.31, places=1)

        result3 = instance.calc_Tpc_corrected(sg=0.7, H2S=0.07)
        self.assertAlmostEqual(result3, 364.36, places=1)

        result4 = instance.calc_Tpc_corrected(sg=0.7, e_correction=21.278)
        self.assertAlmostEqual(result4, 356.31, places=1)

        result5 = instance.calc_Tpc_corrected(Tpc=377.59, e_correction=21.278)
        self.assertAlmostEqual(result5, 356.31, places=1)

        print('calc_Tpc_corrected passed')

    def test_calc_Ppc_corrected(self):
        instance = zfactor()

        result1 = instance.calc_Ppc_corrected(sg=0.7)
        self.assertAlmostEqual(result1, 663.289, places=2)

        result2 = instance.calc_Ppc_corrected(sg=0.7, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result2, 628.214, places=2)

        result3 = instance.calc_Ppc_corrected(sg=0.7, e_correction=21.27, H2S=0.07)
        self.assertAlmostEqual(result3, 628.227, places=2)

        result4 = instance.calc_Ppc_corrected(Ppc=663.29, e_correction=21.278, B=0.07, Tpc_corrected=356.31)
        self.assertAlmostEqual(result4, 628.230, places=2)

        print('calc_Ppc_corrected passed')

    def test_calc_Tr(self):
        instance = zfactor()

        result1 = instance.calc_Tr(sg=0.7, T=75, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result1, 1.5005, places=3)

        result2 = instance.calc_Tr(Tpc=377.59, T=75)
        self.assertAlmostEqual(result2, 1.4160, places=3)

        result3 = instance.calc_Tr(Tpc=377.59, T=75, e_correction=21.278)
        self.assertAlmostEqual(result3, 1.5005, places=3)

        result4 = instance.calc_Tr(Tpc_corrected=10, T=10)
        self.assertAlmostEqual(result4, 46.967, places=2)

        print('calc_Pr passed')

    def test_calc_Pr(self):
        instance = zfactor()

        result1 = instance.calc_Pr(sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result1, 3.1995, places=3)

        result2 = instance.calc_Pr(Ppc=663.29, Tpc=377.59, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result2, 3.1995, places=3)

        result3 = instance.calc_Pr(Ppc_corrected=628.21, P=2010)
        self.assertAlmostEqual(result3, 3.1995, places=3)



if __name__ == '__main__':
    unittest.main()


import unittest

from gascompressibility import zfactor


class Test_zfactor(unittest.TestCase):

    def test_calc_Ppc(self):
        instance = zfactor()

        result1 = instance.calc_Ppc(sg=0.7)
        self.assertAlmostEqual(result1, 663.2869, places=3)

        print('calc_Ppc passed (mode="sutton")')

        instance = zfactor('piper')

        result2 = instance.calc_Ppc(Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result2, 747.9479, places=3)

        result3 = instance.calc_Ppc(K=13.661, J=0.4995)
        self.assertAlmostEqual(result3, 747.9869, places=3)

        result4 = instance.calc_Ppc(sg=0.7, CO2=0.1, H2S=0.07)
        self.assertAlmostEqual(result4, 747.9468, places=3)

        print('calc_Ppc passed (mode="piper")')

    def test_calc_Tpc(self):
        instance = zfactor()

        result1 = instance.calc_Tpc(sg=0.7)
        self.assertAlmostEqual(result1, 377.59, places=1)

        print('calc_Tpc passed (mode="sutton")')

        instance = zfactor('piper')

        result2 = instance.calc_Tpc(K=13.661, J=0.4995)
        self.assertAlmostEqual(result2, 373.6194, places=3)

        result3 = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result3, 373.6152, places=3)

        result4 = instance.calc_Tpc(sg=0.7, H2S=0.07, CO2=0.1, N2=0.5)
        self.assertAlmostEqual(result4, 232.7950, places=3)

        print('calc_Tpc passed (mode="piper")')

    def test_calc_J(self):
        instance = zfactor(mode='piper')

        result1 = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result1, 0.4995, places=3)

        result2 = instance.calc_J(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result2, 0.4690, places=3)

        result3 = instance.calc_J(sg=0.7)
        self.assertAlmostEqual(result3, 0.5622, places=3)

        print('calc_J passed')

    def test_calc_K(self):
        instance = zfactor(mode='piper')

        result1 = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0)
        self.assertAlmostEqual(result1, 13.6612, places=3)

        result2 = instance.calc_K(sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result2, 12.7270, places=3)

        result3 = instance.calc_K(sg=0.7)
        self.assertAlmostEqual(result3, 14.4508, places=3)

        print('calc_K passed')

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

        print('calc_Tr passed (mode="sutton")')

        instance = zfactor(mode='piper')

        result5 = instance.calc_Tr(T=75, sg=0.7, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result5, 1.4310, places=3)

        result6 = instance.calc_Tr(T=75, K=13.661, J=0.4995)
        self.assertAlmostEqual(result6, 1.4310, places=3)

        result7 = instance.calc_Tr(T=75, Tpc=373.6)
        self.assertAlmostEqual(result7, 1.4311, places=3)

        print('calc_Tr passed (mode="piper")')

    def test_calc_Pr(self):
        instance = zfactor()

        result1 = instance.calc_Pr(sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result1, 3.1995, places=3)

        result2 = instance.calc_Pr(Ppc=663.29, Tpc=377.59, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result2, 3.1995, places=3)

        result3 = instance.calc_Pr(Ppc_corrected=628.21, P=2010)
        self.assertAlmostEqual(result3, 3.1995, places=3)

        result4 = instance.calc_Pr(Ppc=663.29, P=2010, e_correction=21.278, H2S=0.07, Tpc=377.59)
        self.assertAlmostEqual(result4, 3.1995, places=3)

        print('calc_Pr passed (mode="sutton")')

        instance = zfactor(mode='piper')

        result5 = instance.calc_Pr(Tpc=373.6, sg=0.7, P=2010, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result5, 2.6874, places=3)

        result6 = instance.calc_Pr(Ppc=747.9, P=2010)
        self.assertAlmostEqual(result6, 2.6875, places=3)

        result7 = instance.calc_Pr(P=2010, K=4, J=2)
        self.assertAlmostEqual(result7, 502.5, places=1)

        result8 = instance.calc_Pr(P=2010, sg=2)
        self.assertAlmostEqual(result8, 3.8686, places=3)

        result9 = instance.calc_Pr(P=2010, Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result9, 2.6873, places=3)

        print('calc_Pr passed (mode="piper")')

    def test_calc_Z(self):
        instance = zfactor()

        result1 = instance.calc_Z(P=2010, T=75, CO2=0.1, H2S=0.07, sg=0.7)
        self.assertAlmostEqual(result1, 0.7730, places=3)

        result2 = instance.calc_Z(P=2010, T=75, Ppc=747.9, Tpc=373.6)
        self.assertAlmostEqual(result2, 0.7418, places=3)

        print('calc_Z passed (mode="sutton")')

        instance = zfactor(mode='piper')

        result3 = instance.calc_Z(P=2010, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)
        self.assertAlmostEqual(result3, 0.8093, places=3)

        result4 = instance.calc_Z(P=2010, T=75, sg=0.7, H2S=0.07, CO2=0.1)
        self.assertAlmostEqual(result4, 0.7418, places=3)

        result5 = instance.calc_Z(P=2010, T=75, K=13.661, J=0.4995)
        self.assertAlmostEqual(result5, 0.7418, places=3)

        result6 = instance.calc_Z(P=2010, T=75, Tpc=373.6, J=0.4995)
        self.assertAlmostEqual(result6, 0.7418, places=3)

        result7 = instance.calc_Z(P=2010, T=75, Pr=2.687, K=13.661, J=0.4995)
        self.assertAlmostEqual(result7, 0.7418, places=3)

        result8 = instance.calc_Z(P=2010, T=75, Ppc=663.28, Tpc=377.59)
        self.assertAlmostEqual(result8, 0.7207, places=3)

        print('calc_Z passed (mode="piper")')


if __name__ == '__main__':
    unittest.main()

# Documents\GasCompressibiltiyFactor-py>python -m unittest tests.test_gascomp

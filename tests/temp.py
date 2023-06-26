def test_calc_Z(self):
    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, CO2=0.1, H2S=0.07, sg=0.7)
    self.assertEqual(ps_prop['P'], 2010)
    
    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, CO2=0.1, H2S=0.07, sg=0.7, ps_prop=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7730, places=3)
    self.assertAlmostEqual(ps_prop['e_correction'], 21.2778, places=3)
    self.assertAlmostEqual(ps_prop['Ppc_corrected'], 628.2143, places=3)
    self.assertAlmostEqual(ps_prop['Tpc_corrected'], 356.3122, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 663.287, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 377.59, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 3.1995, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.5006, places=3)

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, Ppc=747.9, Tpc=373.6)

    self.assertAlmostEqual(ps_prop['z'], 0.7418, places=3)
    self.assertAlmostEqual(ps_prop['e_correction'], 0.0, places=3)
    self.assertAlmostEqual(ps_prop['Ppc_corrected'], 747.9, places=3)
    self.assertAlmostEqual(ps_prop['Tpc_corrected'], 373.6, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 2.6875, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.4311, places=3)

    
    ps_prop = gascomp.calc_Z(Pr=3.1995, T=75, Tpc=377.59, e_correction=21.278, ignore_conflict=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7730, places=3)
    self.assertAlmostEqual(ps_prop['T'], 534.67, places=3)
    self.assertAlmostEqual(ps_prop['Tpc_corrected'], 356.312, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.5006, places=3)
    self.assertAlmostEqual(ps_prop['Z'], 0.7731, places=3)

    
    ps_prop = gascomp.calc_Z(Tpc_corrected=356.31, sg=0.7, P=1995.3, T=75, H2S=0.07, CO2=0.1, ignore_conflict=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7730, places=3)
    self.assertAlmostEqual(ps_prop['e_correction'], 21.2778, places=3)
    self.assertAlmostEqual(ps_prop['Ppc_corrected'], 628.2104, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 663.287, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 377.59, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 3.1996, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.5006, places=3)

    print('calc_Z passed (mode="sutton")')

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0)

    self.assertAlmostEqual(ps_prop['z'], 0.7418, places=3)
    self.assertAlmostEqual(ps_prop['J'], 0.4995, places=3)
    self.assertAlmostEqual(ps_prop['K'], 13.6612, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 747.9468, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 373.6153, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 2.6874, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.4311, places=3)

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, sg=0.7, H2S=0.07, CO2=0.1, N2=0.1)

    self.assertAlmostEqual(ps_prop['z'], 0.8093, places=3)
    self.assertAlmostEqual(ps_prop['J'], 0.4691, places=3)
    self.assertAlmostEqual(ps_prop['K'], 12.7271, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 736.2064, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 345.3259, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 2.7302, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.5483, places=3)

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, K=13.661, J=0.4995)

    self.assertAlmostEqual(ps_prop['z'], 0.7418, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 747.9869, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 373.6195, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 2.6872, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.4311, places=3)

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, Tpc=373.6, J=0.4995, ignore_conflict=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7418, places=3)
    self.assertAlmostEqual(ps_prop['Ppc'], 747.9479, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 2.6874, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.4311, places=3)

    
    ps_prop = gascomp.calc_Z(T=75, Pr=2.687, K=13.661, J=0.4995, ignore_conflict=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7418, places=3)
    self.assertAlmostEqual(ps_prop['T'], 534.67, places=3)
    self.assertAlmostEqual(ps_prop['Tpc'], 373.6195, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.4311, places=3)

    
    ps_prop = gascomp.calc_Z(P=1995.3, T=75, Ppc=663.28, Tpc=377.59, ignore_conflict=True)

    self.assertAlmostEqual(ps_prop['z'], 0.7207, places=3)
    self.assertAlmostEqual(ps_prop['T'], 534.67, places=3)
    self.assertAlmostEqual(ps_prop['Pr'], 3.0304, places=3)
    self.assertAlmostEqual(ps_prop['Tr'], 1.416, places=3)

    print('calc_Z passed (mode="piper")')
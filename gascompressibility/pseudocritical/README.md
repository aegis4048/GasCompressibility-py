


# Pseudo-Critical Property Models Explained

This section explains the equations used for each correlation models implemented in the following files:

* piper.py
* sutton.py

## 1. Basic Theory

The goal of the pseudo-critical property models implemented in *GasCompressibility-py* is to derive the values of reduced pressure ($P_{r}$) and reduced temperature ($T_{r}$), which can be used as an input to obtain the gas compressibility factor (z-factor) through the visual inspection of the famous [Standing-Katz (SK) chart](https://github.com/aegis4048/GasCompressibiltiy-py/blob/progress/misc/SK_chart_comparison.png), or by using various [z-factor correlation models](https://github.com/aegis4048/GasCompressibiltiy-py/tree/progress/gascompressibility/z_correlation). In the other words, z-factor is a function of pseudo-reduced pressure and temperature:

$$
Z = f(P_{r}, T_{r})
$$

$P_{r}$ and $T_{r}$ are defined as the pressure and temperature divided by the mixture's pseudo-critical pressure ($P_{pc}$) and and temperature ($T_{pc}$):

$$
P_{r} = \frac{P}{P_{pc}}, ~~~~~~~ T_{r} = \frac{T}{T_{pc}}
$$

Kay (1936)<sup><a href="#ref-1">[1]</sup> stated that $P_{pc}$ and $T_{pc}$ of a gas mixture can be expressed as the mole fraction ($x$) weighted average of the critical pressure ($P_c$) and temperature ($T_c$) of the mixture's individual component ($i$):

$$
P_{pc}=\sum x_{i} P_{c_{i}}, ~~~~~~~T_{pc}=\sum x_{i} T_{c_{i}}
$$

However, this method is too inconvenient because you have to manually input individual component's $P_c$, $T_c$, and $x$, which can be time-consuming. Furthermore, this isn't practical for oil field applications in which the lab analysis of the "heavy-ends" are often lumped up together and reported as $C_{6}^{+}$ or $C_{7}^{+}$. This makes it impossible to know the mole fractions of the components heavier than $C_{6}$ or $C_{7}$. 

This section introduces various pseudo-critical property models that correlates a gas mixture's specific gravity ($\gamma_{g}$) to its corresponding $P_{pc}$ and $T_{pc}$. 


## 2. Caveats to note

**1) The models work only for "naturally occurring" hydrocarbon gases**

The models implemented in this library correlates $\gamma_{g}$ to the corresponding $P_{pc}$ and $T_{pc}$ by using the fitted regression coefficients. This means that the working range of the models will be limited by the range of the data points used to fit the coefficients. All pseudo-critical models (that I know of) are developed using only the naturally occurring gas samples. Therefore, it is not recommended to use these models for synthetic gases. If you are dealing with synthetic gases, I recommend using Kay's (1936)<sup>[[1]](#ref-1)</sup> method. 

**2) Correction is necessary in presence of significant impurities fractions**

Sutton's method (1985)<sup>[[2]](#ref-2)</sup> can apply correction for $H_{2}S$ and $CO_2$:

```python
>>> import gascompressibility as gascomp

>>> gascomp.sutton().calc_Tr(sg=0.7, T=75, CO2=0.1, H2S=0.07) 
1.5005661019949397
```

Piper's method (1993)<sup>[[3]](#ref-3)</sup> can apply correction for $H_{2}S$, $CO_2$, and $N_2$:
```python
>>> gascomp.piper().calc_Tr(sg=0.7, T=75, CO2=0.1, H2S=0.07, N2=0.1)  
1.5483056093175225
```

## 3. Equations used

This section shows the equations used for each pseudo-critical property models.

### 3.1. Sutton (1985)<sup>[[2]](#ref-2)</sup> 

Sutton (1985) fitted the following regression model for a gas mixture with unknown component composition that that take $\gamma_{g}$ as input:
 
$$
P_{pc} = 756.8 - 131.07\gamma_{g} - 3.6\gamma^{2}_{g}
$$

$$
T_{pc} = 169.2 - 349.5\gamma_{g} - 74.0\gamma^{2}_{g}
$$

The above correlations are valid over the ranges of specific gravities with which Sutton worked: $0.57 < \gamma_{g} < 1.68$.  He also recommends to apply Wichert-Aziz<sup>[[4]](#ref-4)</sup> correction for significant $H_2S$ and $CO_2$ fractions:

$$
\epsilon = 120 (A^{0.9} - A^{1.6}) + 15(B^{0.5} - B^{4})
$$

$$
T_{pc}^{'} = T_{pc} - \epsilon
$$

$$
P_{pc}^{'} = \frac{P_{pc}T_{pc}^{'}}{T_{pc} - B(1 - B)\epsilon} 
$$

where:

$\epsilon$ = temperature-correction factor for acid gases [°R]

$A$ = sum of the mole fractions of $CO_2$ and $H_2S$ in the gas mixture [dimensionless]

$B$ = mole fraction of $H_2S$ in the gas mixture [dimensionless]

$T^{'}_{pc}$ = corrected pseudo-critical temperature [°R]

$P^{'}_{pc}$ = corrected pseudo-critical pressure [psia]

The correction correlation is applicable to concentration ranges of $CO_2 < 54.4 \space mol$**%** and $H_2S < 73.8 \space mol$**%**. Using the Dranchuk and Abu-Kassem (DAK) method<sup>[[5]](#ref-5)</sup> as a z-factor correlation model, Sutton's correlation model reported an average absolute error of 1.418%. The regression coefficients were fitted with 289 points.

**Code usage example:**

```python
import gascompressibility as gascomp
 
instance = gascomp.sutton() 

z = instance.calc_Z(sg=0.7, CO2=0.1, H2S=0.07, T=75, P=2010)   # Input: T[°F], P[psig]

print('Z             =', round(instance.Z, 2), '   [dimensionless]')
print('Tpc           =', round(instance.Tpc, 2), ' [°R]')
print('Ppc           =', round(instance.Ppc, 2), ' [psia]')
print('e_correction  =', round(instance.e_correction, 2), '  [°R]')
print('Tpc_corrected =', round(instance.Tpc_corrected, 2), ' [°R]')
print('Ppc_corrected =', round(instance.Ppc_corrected, 2), ' [psia]')
print('Tr            =', round(instance.Tr, 2), '    [dimensionless]')
print('Pr            =', round(instance.Pr, 2), '    [dimensionless]')
```
*Output:*
```python
Z             = 0.77    [dimensionless]
Ppc           = 663.29  [psia]
Tpc           = 377.59  [°R]
e_correction  = 21.28   [°R]
Ppc_corrected = 628.21  [psia]
Tpc_corrected = 628.21  [°R]
Pr            = 3.2     [dimensionless]
Tr            = 1.5     [dimensionless]
```

Alternatively:
```python
>>> import gascompressibility as gascomp

>>> gascomp.sutton().calc_Z(sg=0.7, CO2=0.1, H2S=0.07, P=2010, T=75)  # Input: T[°F],  P[psig]
0.7727976174884119

>>> gascomp.sutton().calc_Tpc(sg=0.7) 
377.59

>>> gascomp.sutton().calc_Tpc_corrected(sg=0.7, CO2=0.1, H2S=0.07) 
356.31219397078127

>>> gascomp.sutton().calc_Tr(sg=0.7, CO2=0.1, H2S=0.07, T=75) # Input: T[°F]
1.5005661019949397
```


### 3.2. Piper et al. (1993)<sup>[[3]](#ref-3)</sup>

Piper et al. (1993) adapted the method of Stewart et al. (1959) to calculate the pseudo-critical properties of gas mixtures with nitrogen ($N_2$), $CO_2$, and $H_2S$ fractions:

$$
T_{pc} = \frac{K^{2}}{J}, ~~~~~~~P_{pc} = \frac{T_{pc}}{J}
$$

and


$$
\begin{align}
J &= 0.11582  - 0.45820 x_{H_2S}\left(\frac{T_c}{P_c}\right)\_{H_2S} - 0.90348 x_{CO_2}\left(\frac{T_c}{P_c}\right)\_{CO_2} - 0.66026 x_{N_2}\left(\frac{T_c}{P_c}\right)\_{N_2} \\
\\
&~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ + 0.70729\gamma_{g} - 0.099397 \gamma^{2}\_{g}\\
\\
K &= 3.8216 -0.06534 x_{H_2S}\left(\frac{T_c}{\sqrt{P_c}}\right)\_{H_2S} - 0.42113 x_{CO_2}\left(\frac{T_c}{\sqrt{P_c}}\right)\_{CO_2} - 0.91249 x_{N_2}\left(\frac{T_c}{\sqrt{P_c}}\right)\_{N_2} \\
\\
&~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ + 17.438\gamma_{g} - 3.2191 \gamma^{2}\_{g}\\
\end{align}
$$


where:

$J$ =  Steward, Burkhardt, and Voo (SBV) parameter [°R/psia]

$K$ = SBV parameter [°R/psia^0.5]

$x_{H_2S}$ = mole fraction of $H_2S$ [dimensionless]

$x_{CO_2}$ = mole fraction of $CO_2$ [dimensionless]

$x_{N2}$ = mole fraction of $N_2$ [dimensionless]

Piper's correction for non-hydrocarbon impurities have working ranges of $H_2S < 51.37 \space mol$**%**,  $CO_2 < 67.16 \space mol$**%**, and $N_2 < 15.68  \space mol$**%**. Using the DAK method as a z-factor correlation model, Piper's crrelation model reported an average absolute error of 1.304%. The regression coefficients were fitted with 896 points.


**Code usage example:**

```python
import gascompressibility as gascomp
 
instance = gascomp.piper() 

z = instance.calc_Z(sg=0.7, CO2=0.1, H2S=0.07, N2=0.1, T=75, P=2010)   # Input: T[°F], P[psig]

print('Z   =', round(instance.Z, 2), '   [dimensionless]')
print('J   =', round(instance.J, 2), '   [°R/psia]')
print('K   =', round(instance.K, 2), '  [°R/psia^0.5]')
print('Ppc =', round(instance.Ppc, 2), ' [psia]')
print('Tpc =', round(instance.Tpc, 2), ' [°R]')
print('Pr  =', round(instance.Pr, 2), '   [dimensionless]')
print('Tr  =', round(instance.Tr, 2), '   [dimensionless]')
```
*Output:*
```python
Z   = 0.81    [dimensionless]
J   = 0.47    [°R/psia]
K   = 12.73   [°R/psia^0.5]
Ppc = 736.21  [psia]
Tpc = 345.33  [°R]
Pr  = 2.75    [dimensionless]
Tr  = 1.55    [dimensionless]
```
Alternatively, 

```python
>>> import gascompressibility as gascomp

>>> gascomp.piper().calc_Z(sg=0.7, CO2=0.1, H2S=0.07, N2=0.1, P=2010, T=75)  # Input: T[°F],  P[psig]
0.8086927073843273

>>> gascomp.piper().calc_Tpc(sg=0.7, CO2=0.1, H2S=0.07, N2=0.1)  # Input: T[°F],  P[psig]
345.325881907563

>>> gascomp.piper().calc_Tr(sg=0.7, CO2=0.1, H2S=0.07, N2=0.1, T=75)  # Input: T[°F],  P[psig]
1.5483056093175225
```

## 4. Units

### 5.1. Z-factor function

## 5. Z-factor calculation from pseudo-critical properties

## 6. Nomenclature

# References


<a id="ref-1" name="ref-1">[1]</a> Kay, W.B:  "Density of Hydrocarbon Gases and Vapors at High Temperature and Pressure," *Industrial Engineering Chemistry* (1936)

<a name="ref-2">[2]</a> Sutton, R.P.:  "Compressibility Factor for High-Molecular Weight Reservoir Gases," paper SPE 14265 (1985). [(link)](https://onepetro.org/SPEATCE/proceedings-abstract/85SPE/All-85SPE/SPE-14265-MS/61651)

<a name="ref-3">[3]</a> Piper, L.D., McCain Jr., W.D., and Corredor J.H.:  "Compressibility Factors for Naturally Occurring Petroleum Gases," paper SPE 26668 (1993). [(link)](https://onepetro.org/SPEATCE/proceedings/93SPE/All-93SPE/SPE-26668-MS/55401) 

<a name="ref-4">[4]</a> Wichert, E.:  "Compressibility Factor of Sour Natural Gases," MEng Thesis, The University of Calgary, Alberta (1970) 

<a id="ref-5" name="ref-5">[5]</a> Dranchuk, P.M., and Abou-Kassem, J.H.: "Calculation of z-Factors for Natural Gases Using Equations of State,"  *Journal of Canadian Petroleum Technology* (1975). [(link)](https://onepetro.org/JCPT/article-abstract/doi/10.2118/75-03-03)

<a id="ref-6" name="ref-6">[6]</a> Stewart, W.F., Burkhardt, S.F., and Voo, D.: "Prediction of Pseudocritical Parameters for Mixtures," paper presented at the AIChE Meeting, Kansas City, MO (May 18, 1959).


---------------
<a id="ref-1" name="ref-1">[1]</a> Dranchuk, P.M., and Abou-Kassem, J.H.: "Calculation of z-Factors for Natural Gases Using Equations of State,"  *Journal of Canadian Petroleum Technology* (1975). [(link)](https://onepetro.org/JCPT/article-abstract/doi/10.2118/75-03-03)

<a id="ref-2" name="ref-2">[2]</a> Hall, K.R., and Yarborough, L.: "A new equation of state for Z-factor calculations," *Oil and Gas Journal* (1973). [(link)](https://www.researchgate.net/publication/284299884_A_new_equation_of_state_for_Z-factor_calculations)

<a id="ref-3" name="ref-3">[3]</a> Londono, F.E., Archer, R.A., and Blasingame, T.A.: "Simplified Correlations for Hydrocarbon Gas Viscosity and Gas  Density — Validation and Correlation of Behavior Using a Large-Scale Database," paper SPE 75721 (2005). [(link)](https://onepetro.org/SPEGTS/proceedings/02GTS/All-02GTS/SPE-75721-MS/135705) 

<a id="ref-4" name="ref-4">[4]</a> Kareem, L.A., Iwalewa, T.M., and Marhoun, M.al-.: "New explicit correlation for the compressibility factor of natural gas: linearized z-factor isotherms,"  *Journal of Petroleum Exploration and Production Technology* (2016).    [(link)](https://link.springer.com/article/10.1007/s13202-015-0209-3)

<a id="ref-5" name="ref-5">[5]</a> Elsharkawy, A.M., Aladwani, F., Alostad, N.: "Uncertainty in sour gas viscosity estimation and its impact on inflow performance and production forecasting,"  *Journal of Natural Gas Science and Engineering* (2015).    [(link)](https://link.springer.com/article/10.1007/s13202-015-0209-3)


<a id="ref-6" name="ref-6">[6]</a> Elsharkawy, A.M.: "Predicting the Properties of Sour Gases and Condensates: Equations of State and Empirical Correlations,"  paper SPE 74369 (2002). [(link)](https://onepetro.org/SPEIOCEM/proceedings-abstract/02IPCEM/All-02IPCEM/SPE-74369-MS/136841)

<a name="ref-7">[7]</a> Sutton, R.P.:  "Compressibility Factor for High-Molecular Weight Reservoir Gases," paper SPE 14265 (1985). [(link)](https://onepetro.org/SPEATCE/proceedings-abstract/85SPE/All-85SPE/SPE-14265-MS/61651)

<a name="ref-8">[8]</a> Wichert, E.:  "Compressibility Factor of Sour Natural Gases," MEng Thesis, The University of Calgary, Alberta (1970) 

<a name="ref-9">[9]</a> Piper, L.D., McCain Jr., W.D., and Corredor J.H.:  "Compressibility Factors for Naturally Occurring Petroleum Gases," paper SPE 26668 (1993). [(link)](https://onepetro.org/SPEATCE/proceedings/93SPE/All-93SPE/SPE-26668-MS/55401) 







<a id="ref-10" name="ref-10">[10]</a> Elsharkawy, A.M., and Elsharkawy, L.:  "Predicting the compressibility factor of natural gases containing various amounts of CO2 at high temperatures and pressures," *Journal of Petroleum and Gas Engineering* (2020). [(link)](https://www.researchgate.net/publication/343309900_Predicting_the_compressibility_factor_of_natural_gases_containing_various_amounts_of_CO2_at_high_temperatures_and_pressures)
  




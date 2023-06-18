[![Build Status](https://app.travis-ci.com/aegis4048/GasCompressibiltiy-py.svg?branch=master)](https://app.travis-ci.com/aegis4048/GasCompressibiltiy-py)

<img src="https://raw.githubusercontent.com/aegis4048/GasCompressibiltiy-py/master/misc/intro_image.png" alt="Alt text" title="Optional title">

# GasCompressibility-py
GasCompressibility-py is a Python library for calculating the gas compressibility factor, $`Z`$, based on real gas law. 

It is designed with practical oil field application in mind, in which the required inputs ($`T`$, $`P`$, and $`\gamma_{g}`$) can be readily obtained from the surface facility. 

The packages is under [MIT License](https://github.com/aegis4048/GasCompressibiltiy-py/blob/main/LICENSE).

# 1. Installation
The package is hosted on the [PyPi](https://pypi.org/project/gascompressibility/) page. You can remotely install it with the `pip` command:
```
pip install gascompressibility
```
If you are a chemical or petroleum engineer who doesn't know what `pip` is, read [below](#pip).

# 2. Quickstart
```python
import gascompressibility as gascomp

z_obj = gascomp.zfactor()

results, fig, ax = z_obj.quickstart()
```
<img src="https://raw.githubusercontent.com/aegis4048/GasCompressibiltiy-py/progress/misc/quickstart.png" alt="Alt text" title="Optional title">

# 3. Usage


```python
import gascompressibility as gascomp
 
z_obj = gascomp.zfactor()  # default mode = 'sutton'

Z = z_obj.calc_Z(sg=0.7, P=2010, T=75, H2S=0.07, CO2=0.1)

print('Z =', round(Z, 2))
```
*output:*

```
Z = 0.77
```

# 4. More Detailed Usage

### 4.1. Accessing "middle-step variables"

The 'middle step variables' created during the calculation steps can be accessed in a form of class object attributes. For example, `z_obj` class object is instantiated. Executing `.calc_Z()` function on `z_obj` computes middle step variables that are required for `Z` calculation, and saves them as class attributes. For example, the reduced temperature, $`T_{r}`$, and the reduced pressure, $`P_{r}`$, can be access by `z_obj.Tr` and `z_obj.Pr`. For the list and descriptions of all middle step variables, check [below](#middlestep-list).

```python
import gascompressibility as gascomp
 
z_obj = gascomp.zfactor()  # default mode = 'sutton'

Z = z_obj.calc_Z(sg=0.7, P=2010, T=75, H2S=0.07, CO2=0.1)

print('Z             =', z_obj.Z)
print('Ppc           =', z_obj.Ppc)
print('Tpc           =', z_obj.Tpc)
print('e_correction  =', z_obj.e_correction)
print('Ppc_corrected =', z_obj.Ppc_corrected)
print('Tpc_corrected =', z_obj.Ppc_corrected)
print('Pr            =', z_obj.Pr)
print('Tr            =', z_obj.Tr)
```
*output:*
```
Z             = 0.7730732979666094
Ppc           = 663.2869999999999
Tpc           = 377.59
e_correction  = 21.277806029218723
Ppc_corrected = 628.2143047814683
Tpc_corrected = 628.2143047814683
Pr            = 3.1995450990234966
Tr            = 1.5005661019949397
```

### 4.2. Calculation modes

The package currently supports 2 ways to compute pseudo-critical properties:

* `zfactor(mode='sutton)` : Sutton's gas specific gravity correlation<sup>[[1]](#ref-1)</sup> and Wichert-Aziz correction for $`H_{2}S`$ and $`CO_{2}`$ fractions<sup>[[2]](#ref-2)</sup> (default mode)

* `zfactor(mode='piper')` : Piper's gas specific gravity correlation for naturally occuring petroleum gases with  $`H_{2}S`$, $`CO_{2}`$ and $`N_{2}`$ fractions<sup>[[3]](#ref-3)</sup>

These two modes can be specified with the keyward argument `mode=` when instantiating the class object `zfactor()`.

```python
z_obj_sutton = gascomp.zfactor('sutton')  # mode='sutton', default
z_obj_piper = gascomp.zfactor('piper')    # mode='piper'
```

Different calculation modes involve different inputs and middle step variables. Piper's method additionally considers nitrogen gas fraction whereas Sutton's method doesn't. All input variables can be provided in a form of keyward arguments (ex: `z_obj.calc_Z(sg=0.7, P=2010, T=75)`). All middle-step variables can be accessed in a form of class attributes (ex: `z_obj.Ppc_corrected`).

**Inputs:**
- `zfactor(mode='sutton)` 
	- `sg`: gas specific gravity, $`\gamma_{g}`$ (dimensionless)
	- `P`: gas pressure, $`P`$ (psia)
	- `T`: gas temperature,  $`T`$ (°F)
	- `H2S`: $`H_{2}S`$ gas fraction (dimensionless)
	- `CO2`: $`CO_{2}`$ gas fraction (dimensionless)
- `zfactor(mode='piper')`
	- `sg`, `P`, `T`, `H2S`, and `CO2`
	- `N2`: $`N_{2}`$ gas fraction (dimensionless)

<a name="middlestep-list"></a>
**Middle-step variables:**
- `zfactor(mode='sutton)` 
	- `Ppc`: pseudo-critical pressure, $`P_{pc}`$ (psia)
	- `Tpc`: pseudo-critical temperature, $`T_{pc}`$ (°R)
	- `e_correction`: DAK deviation parameter, $`\epsilon`$ (°R)
	- `Ppc_corrected`: sour-gas-corrected pseudo-critical pressure, $`P^{'}_{pc}`$ (psia)
	- `Tpc_corrected`: sour-gas-corrected pseudo-critical temperature, $`T^{'}_{pc}`$ (°R)
	- `Pr`: reduced pressure, $`P_{r}`$ (psia)
	- `Tr`: reduced temperature, $`T_{r}`$ (°R)
	- `Z`: gas compressibility factor, $`Z`$ (dimensionless)
- `zfactor(mode='piper')`
	- `Ppc`, `Tpc`, `Pr`, `Tr`, and `Z`
	- `J`: Sutton-Burkhardt-VOO (SBV) parameter, $`J`$ (°R/psia)
	- `K`: SBV parameter, $`K`$ (°R/psia^0.5)

### 4.3. Additional functions

The packages also supports separate calculation of all middle step variables. Let's say you want to get the z-factor by looking up the famous [Standing-Katz chart](https://github.com/aegis4048/GasCompressibiltiy-py/blob/master/misc/zfactor_textbook_plot.png) by using $`P_{r}`$ for the x-axis and $`T_{r}`$ for different lines. If you know your gas sample's $`P`$, $`T`$ and $`\gamma_{g}`$, you can compute it's reduced properties by:

```python
Tr = gascomp.zfactor().calc_Tr(T=75, sg=0.7)
Pr = gascomp.zfactor().calc_Pr(P=2010, sg=0.7)
print(Tr)
print(Pr)
```
*Output:*
```
1.416006779840568
3.0303624222998495
```

The below is the list of the additional functions supported:


* `gascompressibility.zfactor.calc_Tpc()`
* `gascompressibility.zfactor.calc_Ppc()`
* `gascompressibility.zfactor.calc_e_correction()`
* `gascompressibility.zfactor.calc_Tpc_corrected()`
* `gascompressibility.zfactor.calc_Ppc_corrected()`
* `gascompressibility.zfactor.calc_J()`
* `gascompressibility.zfactor.calc_K()`
* `gascompressibility.zfactor.calc_Tr()`
* `gascompressibility.zfactor.calc_Pr()`
* `gascompressibility.zfactor.calc_Z()`

Each function takes different inputs in a form of keyword arguments. For more detailed information about input types for each function, refer to the documentation (work in progress). Also note that some functions aren't supported depending on whether if its `zfactor(mode='sutton')` or `zfactor(mode='piper')`.


### 4.4. "Alternative" calculations

### 4.5. "Guided" calculations


# References

<a name="ref-1">[1]</a> Sutton, R.P.:  "Compressibility Factor for High-Molecular Weight Reservoir Gases," paper SPE 14265 (1985). [(link)](https://onepetro.org/SPEATCE/proceedings-abstract/85SPE/All-85SPE/SPE-14265-MS/61651)

<a name="ref-2">[2]</a> Wichert, E.:  "Compressibility Factor of Sour Natural Gases," MEng Thesis, The University of Calgary, Alberta (1970) 

<a name="ref-3">[3]</a> Piper, L.D., McCain Jr., W.D., and Corredor J.H.:  "Compressibility Factors for Naturally Occurring Petroleum Gases," paper SPE 26668 (1993). [(link)](https://onepetro.org/SPEATCE/proceedings/93SPE/All-93SPE/SPE-26668-MS/55401) 

<a name="ref-4">[4]</a> Elsharkawy, A.M., and Elsharkawy, L.:  "Predicting the compressibility factor of natural gases containing various amounts of CO2 at high temperatures and pressures," *Journal of Petroleum and Gas Engineering* (2020) [(link)](https://www.researchgate.net/publication/343309900_Predicting_the_compressibility_factor_of_natural_gases_containing_various_amounts_of_CO2_at_high_temperatures_and_pressures)


# Requirements
1. Numpy
2. Scipy
3. Matplotlib

# Authors

* __[Eric 'Soobin' Kim](https://github.com/aegis4048)__ - Petroleum engineer with the gas compressor company, [Flogistix](https://flogistix.com/). Primary author of the package. (Contact | aegis4048@gmail.com, Website | [PythonicExcursions](https://aegis4048.github.io/))

# Tips

<a name="pip"></a>
**What does 'pip' mean?**

If you are asking this question, you are probably a petroleum or chemical engineer with minimal programming knowledge. It's basically a command-line program that helps you download & install any open-source library with minimal hassle. Here I offer some practical tips for engineers not proficient in Python (yet...!):

1. Download Anaconda from [here](https://www.anaconda.com/download).
2. Run the downloaded file. It's filename will look something like this: "Anaconda3-2023.03-1-Windows-x86_64.exe"
3. It will ask you to select destination folder. By default, its "C:\ProgramData\Anaconda3"
4. If it asks you to check if you want to add Codna to the environtment PATH variable, check yes. It will say that it is not recommended, but trust me - this will make your life easier if you don't know what you are doing.
5. Once installation is finished, go to windows search tab (bottom left corner of your screen). Type "cmd" and launch.
6. If installation is done correctly, you should have `(base)` next to your current directory, like this: `(base) C:\Users\EricKim>`. If you don't see `(base)`, go to windows search tab again. Type "Anaconda". Click "Anaconda Prompt (Anaconda 3)" and launch it. If you still don't see `(base)`, you are about to do dive into some painful troubleshooting. Ask your friends who are good at Python to help you with it.
7. If the Anaconda installation is done correctly, make your command line look like the following and press enter: `(base) C:\Users\EricKim>pip install gascompressibility`. 
8. Congrats! Installation is finished
9. Type `(base) C:\Users\EricKim>Jupyter Notebook` and try the package on Jupyter Notebook.

# Work in Progress
Currently working on
* Making documentations
* Theory exlanations
d
gascompressibility.pseudocritical.Piper
======================================================

.. autoclass:: piper.Piper
   :undoc-members:
   :show-inheritance:

Basic Usage
------------
``Piper`` class object uses instance method that requires instantiation. This means you first have to initiate the
object like this:

>>> from gascompressibility.pseudocritical import Piper
>>>
>>> obj = Piper()
>>> obj
<gascompressibility.pseudocritical.Piper> class object with the following calculated attributes:
{
   Tpc: None
   Ppc: None
   J: None
   K: None
   Tr: None
   Pr: None
}

Once a class instance is instantiated, you can run methods from the instantiated object:

>>> obj.calc_Pr(sg=0.7, P=2010)
3.0646766226921294

Running a method from the instantiated object updates the associated variables computed during the calculation process:

>>> obj
<gascompressibility.pseudocritical.Piper> class object with the following calculated attributes:
{
   Tpc: 371.4335560823552
   Ppc: 660.6569792741872
   J: 0.56221847
   K: 14.450840999999999
   Tr: None
   Pr: 3.0646766226921294
}

You can access the computed variables in a form of class attributes:

>>> obj.Ppc
660.6569792741872
>>> obj.Pr
3.0646766226921294

Examples
--------
.. raw:: html

   <hr class="gascomp-methods mb3">

**Import**

>>> from gascompressibility.pseudocritical import Piper

**Direct calculation**

>>> Piper().calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1, N2=0.05)
2.7143160585360255

**Instantiaing an object and retrieving its attribute**

>>> obj = Piper()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1, N2=0.05)
>>> obj.Pr
2.7143160585360255

:code:`.ps_props` **attribute to retrieve all associated calculated pseudo-critical properties**

>>> obj = Piper()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1, N2=0.05)
>>> obj.ps_props
{'Tpc': 359.4649612886111,
 'Ppc': 742.249596786689,
 'J': 0.48429121800104624,
 'K': 13.194154915384328,
 'Tr': None,
 'Pr': 2.7143160585360255}

**More examples**

>>> # pseudo-critical pressure, Ppc (psia)
>>> Piper().calc_Ppc(sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
730.6830493485268

>>> # pseudo-critical temperature, Tpc (°R)
>>> Piper().calc_Tpc(sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
357.31032650971184

>>> # Stewart-Burkhardt-VOO parameter J, (°R/psia)
>>> Piper().calc_J(sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
0.48900864311590075

>>> # Stewart-Burkhardt-VOO parameter K, (°R/psia^0.5)
>>> Piper().calc_K(sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
13.218465793646919

>>> # reduced pseudo-critical pressure, Pr (dimensionless)
>>> Piper().calc_Pr(P=2010, sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
2.770968892470151

>>> # reduced pseudo-critical temperature, Tr (dimensionless)
>>> Piper().calc_Tr(T=75, sg=0.7, N2=0.05, H2S=0.05, CO2=0.1)
1.496374328788025

Methods
--------

.. raw:: html

   <hr class="gascomp-methods">

.. autosummary::
   :nosignatures:
   :toctree: functions/

   ~piper.Piper.calc_J
   ~piper.Piper.calc_K
   ~piper.Piper.calc_Tpc
   ~piper.Piper.calc_Ppc
   ~piper.Piper.calc_Tr
   ~piper.Piper.calc_Pr

Attributes
-----------
.. raw:: html

   <hr class="gascomp-methods references">

.. rubric:: Attributes

.. autosummary::
   ~piper.Piper.sg
   ~piper.Piper.T_f
   ~piper.Piper.T
   ~piper.Piper.P_g
   ~piper.Piper.P
   ~piper.Piper.H2S
   ~piper.Piper.CO2
   ~piper.Piper.N2
   ~piper.Piper.Tpc
   ~piper.Piper.Ppc
   ~piper.Piper.J
   ~piper.Piper.K
   ~piper.Piper.Tr
   ~piper.Piper.Pr
   ~piper.Piper.ps_props

References
-----------

.. raw:: html

   <hr class="gascomp-methods">

.. [1] Piper, L.D., McCain Jr., W.D., and Corredor J.H.: “Compressibility Factors for Naturally Occurring Petroleum Gases,” paper SPE 26668 (1993). `(link) <https://onepetro.org/SPEATCE/proceedings/93SPE/All-93SPE/SPE-26668-MS/55401>`__

.. disqus::
gascompressibility.pseudocritical.Sutton
======================================================

.. autoclass:: sutton.Sutton
   :undoc-members:
   :show-inheritance:

Basic Usage
------------
``Sutton`` class object uses instance method that requires instantiation. This means you first have to initiate the
object like this:

>>> from gascompressibility.pseudocritical import Sutton
>>>
>>> obj = Sutton()
>>> obj
<gascompressibility.pseudocritical.Sutton> class object with the following calculated attributes:
{
   Tpc: None
   Ppc: None
   e_correction: None
   Tpc_corrected: None
   Ppc_corrected: None
   Tr: None
   Pr: None
}

Once a class instance is instantiated, you can run methods from the instantiated object:

>>> obj.calc_Pr(sg=0.7, P=2010)
3.052524774343535

Running a method from the instantiated object updates the associated variables computed during the calculation process:

>>> obj
<gascompressibility.pseudocritical.Sutton> class object with the following calculated attributes:
{
   Tpc: None
   Ppc: 663.2869999999999
   e_correction: None
   Tpc_corrected: None
   Ppc_corrected: 663.2869999999999
   Tr: None
   Pr: 3.052524774343535
}

You can access the computed variables in a form of class attributes:

>>> obj.Ppc
663.2869999999999
>>> obj.Pr
3.052524774343535

Examples
--------
.. raw:: html

   <hr class="gascomp-methods mb3">

**Import**

>>> from gascompressibility.pseudocritical import Sutton

**Direct calculation**

>>> Sutton().calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
3.2070266223893724

**Instantiaing an object and retrieving its attribute**

>>> obj = Sutton()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
>>> obj.Pr
3.2070266223893724

:code:`.ps_props` **attribute to retrieve all associated calculated pseudo-critical properties**

>>> obj = Sutton()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
>>> obj.ps_props
{'Tpc': 377.59,
 'Ppc': 663.2869999999999,
 'e_correction': 21.277806029218723,
 'Tpc_corrected': 356.31219397078127,
 'Ppc_corrected': 628.2143047814683,
 'Tr': None,
 'Pr': 3.2070266223893724}

**More examples**

>>> # pseudo-critical pressure, Ppc (psia)
>>> Sutton().calc_Ppc(sg=0.7)
663.2869999999999

>>> # pseudo-critical temperature, Tpc (°R)
>>> Sutton().calc_Tpc(sg=0.7)
377.59

>>> # temperature correction factor for acid gases ε (°R)
>>> Sutton().calc_e_correction(H2S=0.05, CO2=0.1)
>>> 19.34753439832438

>>> # corrected pseudo-critical pressure, Ppc_corrected (psia)
>>> Sutton().calc_Ppc_corrected(sg=0.7, H2S=0.05, CO2=0.1)
630.8358627422825

>>> # corrected pseudo-critical temperature, Tpc_corrected (°R)
>>> Sutton().calc_Tpc_corrected(sg=0.7, H2S=0.05, CO2=0.1)
358.2424656016756

>>> # reduced pseudo-critical pressure, Pr (dimensionless)
>>> Sutton().calc_Pr(sg=0.7, H2S=0.05, CO2=0.1, P=2010)
3.2095511995759147

>>> # reduced pseudo-critical temperature, Tr (dimensionless)
>>> Sutton().calc_Tr(sg=0.7, H2S=0.05, CO2=0.1, T=75)
1.4924807953797739

Methods
--------

.. raw:: html

   <hr class="gascomp-methods">

.. autosummary::
   :nosignatures:
   :toctree: functions/

   ~sutton.Sutton.calc_Tpc
   ~sutton.Sutton.calc_Ppc
   ~sutton.Sutton.calc_e_correction
   ~sutton.Sutton.calc_Tpc_corrected
   ~sutton.Sutton.calc_Ppc_corrected
   ~sutton.Sutton.calc_Tr
   ~sutton.Sutton.calc_Pr

Attributes
-----------
.. raw:: html

   <hr class="gascomp-methods">

.. rubric:: Attributes

.. autosummary::
   ~sutton.Sutton.sg
   ~sutton.Sutton.T_f
   ~sutton.Sutton.T
   ~sutton.Sutton.P_g
   ~sutton.Sutton.P
   ~sutton.Sutton.H2S
   ~sutton.Sutton.CO2
   ~sutton.Sutton.Tpc
   ~sutton.Sutton.Ppc
   ~sutton.Sutton.Tpc_corrected
   ~sutton.Sutton.Ppc_corrected
   ~sutton.Sutton.Tr
   ~sutton.Sutton.Pr
   ~sutton.Sutton.ps_props

References
-----------

.. raw:: html

   <hr class="gascomp-methods mb4">

.. [1] Sutton, R.P.: “Compressibility Factor for High-Molecular Weight Reservoir Gases,” paper SPE 14265 (1985). `(link) <https://onepetro.org/SPEATCE/proceedings-abstract/85SPE/All-85SPE/SPE-14265-MS/61651>`__

.. [2] Wichert, E.: “Compressibility Factor of Sour Natural Gases,” MEng Thesis, The University of Calgary, Alberta (1970)

.. disqus::
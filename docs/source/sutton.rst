gascompressibility.pseudocritical.Sutton
======================================================

.. autoclass:: Sutton.Sutton
   :undoc-members:
   :show-inheritance:

Examples
--------
.. raw:: html

   <hr class="gascomp-methods mb3">

**Import**

>>> import gascompressibility.pseudocritical.Sutton

**Direct calculation**

>>> Sutton().calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
3.2070266223893724

**Instantiaing an object and retrieving its attribute**

>>> obj = Sutton()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
>>> obj.Pr
3.2070266223893724

:code:`.ps_props` **attribute: Retrieve all associated calculated pseudo-critical properties**

>>> obj = Sutton()
>>> _ = obj.calc_Pr(sg=0.7, P=2000, H2S=0.07, CO2=0.1)
>>> obj.ps_props
{
    'Tpc': 377.59,
    'Ppc': 663.28,
    'e_correction': 21.27,
    'Tpc_corrected': 356.31,
    'Ppc_corrected': 628.21,
    'Tr': None,
    'Pr': 3.20
}

**More examples**

>>> # pseudo-critical pressure, Ppc (psia)
>>> Sutton().calc_Ppc(sg=0.7)
663.2869999999999

>>> # pseudo-critical temperature, Tpc (°R)
>>> Sutton().calc_Tpc(sg=0.7)
377.59

>>> d = {'col1': [1, 2], 'col2': [3, 4]}
>>> df = pd.DataFrame(data=d)
>>> df
   col1  col2
0     1     3
1     2     4


Methods
--------

.. raw:: html

   <hr class="gascomp-methods">

.. autosummary::
   :nosignatures:
   :toctree: functions/

   ~Sutton.Sutton.calc_Tpc
   ~Sutton.Sutton.calc_Ppc
   ~Sutton.Sutton.calc_e_correction
   ~Sutton.Sutton.calc_Tpc_corrected
   ~Sutton.Sutton.calc_Ppc_corrected
   ~Sutton.Sutton.calc_Tr
   ~Sutton.Sutton.calc_Pr

Attributes
-----------
.. raw:: html

   <hr class="gascomp-methods">

.. rubric:: Attributes

.. autosummary::
   ~Sutton.Sutton.sg
   ~Sutton.Sutton.T_f
   ~Sutton.Sutton.T
   ~Sutton.Sutton.P_g
   ~Sutton.Sutton.P
   ~Sutton.Sutton.H2S
   ~Sutton.Sutton.CO2
   ~Sutton.Sutton.Tpc
   ~Sutton.Sutton.Ppc
   ~Sutton.Sutton.Tpc_corrected
   ~Sutton.Sutton.Ppc_corrected
   ~Sutton.Sutton.Tr
   ~Sutton.Sutton.Pr
   ~Sutton.Sutton.ps_props

References
-----------

.. raw:: html

   <hr class="gascomp-methods mb4">

.. [1] Sutton, R.P.: “Compressibility Factor for High-Molecular Weight Reservoir Gases,” paper SPE 14265 (1985). `(link) <https://onepetro.org/SPEATCE/proceedings-abstract/85SPE/All-85SPE/SPE-14265-MS/61651>`__

.. [2] Wichert, E.: “Compressibility Factor of Sour Natural Gases,” MEng Thesis, The University of Calgary, Alberta (1970)
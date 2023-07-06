gascompressibility.pseudocritical.Sutton
======================================================

.. autoclass:: sutton.Sutton
   :undoc-members:
   :show-inheritance:

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
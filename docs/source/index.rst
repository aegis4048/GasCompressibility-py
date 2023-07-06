.. GasCompressibility-py documentation master file, created by
   sphinx-quickstart on Mon Jun 19 10:39:50 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: /_static/intro_image.png

GasCompressibility-py
=================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   modules
   Temp<API/api_index>
   Theories<theories/theory>

GasCompressibility-py is a Python library for calculating the gas
compressibility factor, :math:`Z`, based on real gas law.

It is designed with practical oil field application in mind, in which
the required inputs (:math:`T`, :math:`P`, and :math:`\gamma_{g}`)
can be readily obtained from the surface facility.

The packages is under `MIT
License <https://github.com/aegis4048/GasCompressibiltiy-py/blob/main/LICENSE>`__.

1. Installation
===============

The package is hosted on the
`PyPi <https://pypi.org/project/gascompressibility/>`__ page. You can
remotely install it with the ``pip`` command:

::

   pip install gascompressibility

To download the most recent version:

::

   pip install gascompressibility --upgrade

If you are a chemical or petroleum engineer who doesn’t know what
``pip`` is, read `below <#pip>`__.

2. Quickstart
=============

.. code:: python

   import gascompressibility as gascomp

   z_obj = gascomp.zfactor()

   results, fig, ax = z_obj.quickstart()

3. Usage
========

.. code:: python

   import gascompressibility as gascomp

   z_obj = gascomp.zfactor()  # default mode = 'Sutton'

   Z = z_obj.calc_z(sg=0.7, P=2010, T=75, H2S=0.07, CO2=0.1)

   print('Z =', round(Z, 2))

*output:*

::

   Z = 0.77

4. More Detailed Usage
======================

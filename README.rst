=================================
Structure Manager (structmanager)
=================================

Structural Manager is intented to help in GFEM-type of analysis, where the
finite elment discretization is at a global level and detailed analysis is
performed using analytical or semi-analytical methods.

The structure is mapped onto the finite element model using two mapping files
and additional data is usually required to define for example exact beam
profiles that will be used in the real structures.

Documentation
-------------

The documentation is available on: http://compmech.github.io/structmanager/

Roadmap
-------

.. literalinclude:: ../../../ROADMAP.rst

Requirements
------------
- numpy
- scipy
- pyNastran

Licensing
---------

The new BSD License (`see the LICENSE file for details
<https://raw.github.com/compmech/structmanager/master/LICENSE>`_)
covers all files in the structmanager repository unless stated otherwise.


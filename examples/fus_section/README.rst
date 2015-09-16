Fuselage Section
================

This example model clearly shows how to use :mod:`.structMan` functions in
order to set a sizing optimization problem with the desired constraints.

The optimization will focus on the stiffened panels, stringers and frames.

Model
-----
Part of a fuselage consisting of many stiffened panels.


.. image:: ../../../examples/fus_section/model.png
    :height: 400px

Mapping files
-------------

MappingSE2FE.txt
................

Mapping structural elements to the finite element ids:

.. literalinclude:: ../../../examples/fus_section/MappingSE2FE.txt

MappingSEA2SE.txt
.................

Mapping structural assemblies to the structural elements:

.. literalinclude:: ../../../examples/fus_section/MappingSEA2SE.txt

Create Optimization Cards
-------------------------

.. literalinclude:: ../../../examples/fus_section/create_optimization_cards.py



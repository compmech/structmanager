"""
Sizing data (:mod:`structMan.sol200.sizing_data`)
=================================================

.. currentmodule:: structMan.sol200.sizing_data

In this module it is defined the dictionary ``SDATA`` containing the definition
of the sizing variables for each property accordingly to GENESIS Analysis
Manual (vol01).

It should be used as ``SDATA[ptype][etype]``, where:

- ``ptype`` is ``'PSHELL'``, ``'PBARL'``, etc
- ``etype`` for a shell is ``'SOLID'``, ``'SAND'``, etc
- ``etype`` for a bar is ``'SQUARE'``, ``'TUBE'``, ``'Z'``, etc

The currently available values are:

.. literalinclude:: ../../structMan/sol200/sizing_data.py
    :language: python
    :lines: 22-

"""
SDATA = {}
SDATA['PSHELL'] = {}
SDATA['PSHELL']['SOLID'] = []
SDATA['PSHELL']['SOLID'].append(['t','PSHELL thickness'])
# line below commented because this desvar is a constant
#SDATA['PSHELL']['SOLID'].append(['h','PSHELL length'])
SDATA['PSHELL']['SAND'] = []
SDATA['PSHELL']['SAND'].append(['t','PCOMP sandwich, outer ply thickness'])
SDATA['PSHELL']['SAND'].append(['h','PCOMP sandwich, core thickness'])
SDATA['PSHELL']['SAND2'] = []
SDATA['PSHELL']['SAND2'].append(['t1','PCOMP sandwich, outer bot thickness'])
SDATA['PSHELL']['SAND2'].append(['t2','PCOMP sandwich, outer top thickness'])
SDATA['PSHELL']['SAND2'].append(['h','PCOMP sandwich, core thickness'])

SDATA['PBARL'] = {}
# CSLIB1
SDATA['PBARL']['SQUARE'] = [['d1','PBARL, square base']]
SDATA['PBARL']['RECT'] = []
SDATA['PBARL']['RECT'].append(['d1', 'PBARL, rectangle base', 'CSLIB1'])
SDATA['PBARL']['RECT'].append(['d2', 'PBARL, rectangle height', 'CSLIB1'])
SDATA['PBARL']['CIRCLE'] = [['d1', 'PBARL, circle diameter', 'CSLIB1']]
SDATA['PBARL']['TUBE'] = []
SDATA['PBARL']['TUBE'].append(['d1', 'PBARL, tube internal diameter', 'CSLIB1'])
SDATA['PBARL']['TUBE'].append(['d2', 'PBARL, tube thickness', 'CSLIB1'])
SDATA['PBARL']['BOX3'] = []
SDATA['PBARL']['BOX3'].append(['d1', 'PBARL, box base-top width', 'CSLIB1'])
SDATA['PBARL']['BOX3'].append(['d2', 'PBARL, box thickness', 'CSLIB1'])
SDATA['PBARL']['BOX3'].append(['d3', 'PBARL, box left-right width', 'CSLIB1'])
SDATA['PBARL']['BOX4'] = []
SDATA['PBARL']['BOX4'].append(['d1', 'PBARL, box base-top width', 'CSLIB1'])
SDATA['PBARL']['BOX4'].append(['d2', 'PBARL, box base-top thickness', 'CSLIB1'])
SDATA['PBARL']['BOX4'].append(['d3', 'PBARL, box left-right width', 'CSLIB1'])
SDATA['PBARL']['BOX4'].append(['d4', 'PBARL, box left-right thickness', 'CSLIB1'])
SDATA['PBARL']['IBEAM'] = []
SDATA['PBARL']['IBEAM'].append(['d1', 'PBARL, ibeam base-top half-width', 'CSLIB1'])
SDATA['PBARL']['IBEAM'].append(['d2', 'PBARL, ibeam base-top thickness', 'CSLIB1'])
SDATA['PBARL']['IBEAM'].append(['d3', 'PBARL, ibeam web width', 'CSLIB1'])
SDATA['PBARL']['IBEAM'].append(['d4', 'PBARL, ibeam web thickness', 'CSLIB1'])
SDATA['PBARL']['RAIL'] = []
SDATA['PBARL']['RAIL'].append(['d1', 'PBARL, rail base half-width', 'CSLIB1'])
SDATA['PBARL']['RAIL'].append(['d2', 'PBARL, rail base thickness', 'CSLIB1'])
SDATA['PBARL']['RAIL'].append(['d3', 'PBARL, rail top half-width', 'CSLIB1'])
SDATA['PBARL']['RAIL'].append(['d4', 'PBARL, rail top thickness', 'CSLIB1'])
SDATA['PBARL']['RAIL'].append(['d5', 'PBARL, rail web width', 'CSLIB1'])
SDATA['PBARL']['RAIL'].append(['d6', 'PBARL, rail web thickness', 'CSLIB1'])
SDATA['PBARL']['SPAR'] = []
SDATA['PBARL']['SPAR'].append(['d1', 'PBARL, spar base-top diameter', 'CSLIB1'])
SDATA['PBARL']['SPAR'].append(['d2', 'PBARL, spar width', 'CSLIB1'])
SDATA['PBARL']['SPAR'].append(['d3', 'PBARL, spar thickness', 'CSLIB1'])
SDATA['PBARL']['TEE'] = []
SDATA['PBARL']['TEE'].append(['d1', 'PBARL, tee cap half-width', 'CSLIB1'])
SDATA['PBARL']['TEE'].append(['d2', 'PBARL, tee cap thickness', 'CSLIB1'])
SDATA['PBARL']['TEE'].append(['d3', 'PBARL, tee web width', 'CSLIB1'])
SDATA['PBARL']['TEE'].append(['d4', 'PBARL, tee web thickness', 'CSLIB1'])
SDATA['PBARL']['ANGLE'] = []
SDATA['PBARL']['ANGLE'].append(['d1', 'PBARL, angle cap_y width', 'CSLIB1'])
SDATA['PBARL']['ANGLE'].append(['d2', 'PBARL, angle cap_y thickness', 'CSLIB1'])
SDATA['PBARL']['ANGLE'].append(['d3', 'PBARL, angle cap_z width', 'CSLIB1'])
SDATA['PBARL']['ANGLE'].append(['d4', 'PBARL, angle cap_z thickness', 'CSLIB1'])
# CSLIB2
SDATA['PBARL']['I'] = []
SDATA['PBARL']['I'].append(['d1', 'PBARL, I height', 'CSLIB2'])
SDATA['PBARL']['I'].append(['d2', 'PBARL, I cap base width', 'CSLIB2'])
SDATA['PBARL']['I'].append(['d3', 'PBARL, I cap top width', 'CSLIB2'])
SDATA['PBARL']['I'].append(['d4', 'PBARL, I web thickness', 'CSLIB2'])
SDATA['PBARL']['I'].append(['d5', 'PBARL, I cap base thickness', 'CSLIB2'])
SDATA['PBARL']['I'].append(['d6', 'PBARL, I cap top thickness', 'CSLIB2'])
SDATA['PBARL']['I1'] = []
SDATA['PBARL']['I1'].append(['d1', 'PBARL, I1 cap base-top width', 'CSLIB2'])
SDATA['PBARL']['I1'].append(['d2', 'PBARL, I1 web thickness', 'CSLIB2'])
SDATA['PBARL']['I1'].append(['d3', 'PBARL, I1 web width', 'CSLIB2'])
SDATA['PBARL']['I1'].append(['d4', 'PBARL, I1 total width', 'CSLIB2'])
SDATA['PBARL']['H'] = []
SDATA['PBARL']['H'].append(['d1', 'PBARL, H web width', 'CSLIB2'])
SDATA['PBARL']['H'].append(['d2', 'PBARL, H cap 2*thickness', 'CSLIB2'])
SDATA['PBARL']['H'].append(['d3', 'PBARL, H cap width', 'CSLIB2'])
SDATA['PBARL']['H'].append(['d4', 'PBARL, H web thickness', 'CSLIB2'])
SDATA['PBARL']['Z'] = []
SDATA['PBARL']['Z'].append(['d1', 'PBARL, Z cap bot width', 'CSLIB2'])
SDATA['PBARL']['Z'].append(['d2', 'PBARL, Z web thickness', 'CSLIB2'])
SDATA['PBARL']['Z'].append(['d3', 'PBARL, Z web width', 'CSLIB2'])
SDATA['PBARL']['Z'].append(['d4', 'PBARL, Z total width', 'CSLIB2'])
#TODO add more sections from CSLIB2

SDATA['PBAR'] = SDATA['PBARL']

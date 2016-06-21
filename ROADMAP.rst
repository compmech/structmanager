Roadmap
=======

Version 0.4.0
-------------
- finish new program structure with simplified read of OP2 using newest
  PyNastran
- add ATD Worksheet methods
- figure out best way to pass properties

Version 0.5.0
-------------
- add SA called WingBay, constituted by many stiffened panels. From this
  assembly we can build a constraint to calculate the global buckling on each
  bay
- what about structural assemblies like a SuperStringer, taking into account two
  adjacent panels in order to calculate the redistributed load for the
  post-buckled panels? This would probably be better achieved using three
  pockets for diagonal tension.
- add a base class called "Plate" which can be the base class for Web,
  ShearClipFrame and similar ones...
- create a class OptimizationModel which will do what SOL200 currently does,
  but automatically selecting which optimization card should be used depending
  on which optimization solver the user chooses
- compatibility with Optistruct. This will require re-writing many scripts from
  FORTRAN to HyperMath

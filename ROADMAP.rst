Roadmap
-------

- add PBARL for Stringers
- add crippling methods
- add buckling methods for curved panels
- run an optimization example
- diagonal tension analysis for stiffened panels (considering three pockets
- add SA called WingBay, constituted by many stiffened panels. From this
  assembly we can build a constraint to calculate the global buckling on each
  bay
- what about structural assemblies like SuperStringer, taking into account two
  adjacent panels in order to calculate the redistributed load for the
  post-buckled panels? This would probably be better achieved using three
  pockets for diagonal tension.
- add a base class called "Plate" which can be the base class for Web,
  ShearClipFrame and similar ones...
- create a class OptimizationModel which will do what SOL200 currently does,
  but automatically selecting which optimization card should be used depending
  on which optimization solver the user chooses
- It seems much better to invest time working with Optistruct + Hypermath than
  with Nastran's SOL200 + FORTRAN, due to the higher complexity for creating
  the DRESP3 responses.

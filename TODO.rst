-> lire transformations.py + doctests vers pytests

********* comment utiliser la matrice sur des shapes ccad?
  ******** _gp.gp_Trsf()
    ******** cf. _translate() for example

Deplacement des anchors lors des déplacements dus au contraintes
  -> fonctions de transformation sur les nodes

******** rotation et translation autour des ancres

Custom serialization and deserialization

******** Format for STEP + anchors

Show car graph from BU's reverse engineering
  Utiliser Gephi
  Strategie reconstitution
    Start with 'black boxes'

-> Assemblies in assemblies in assemblies ...
      Document the code
      Clean
      More complex case -> rc car?
      ******** GeometryNode -> One class with multiple constructors

New anchors concept (normal + tangent)

Class diagram

Naming of assemblies and nodes that are translatable in various languages

Avoid duplication of STEP/STEPZIP loading


-----


******** rename shape on nodes to node_shape for clarity
******** shape returned by an assembly? -> ccad Solid(compound)

is it useful to keep the initial placement of nodes?

******** separate examples for assemblies of each part of the car, and for assemblies of assemblies

******** move _transform_anchors from nodes to geometry

wx viewer should be part of osvcad (coming from aocutils)

nicer graph presentation

really global assembly of Tabby as an example
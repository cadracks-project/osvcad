****** Separer visu du code 'core' dans nodes.py. nodes.py ne devrait pas utiliser wx
MAJ examples

-> lire transformations.py + doctests vers pytests

Apply correction for GetHandle() returns 0 on Linux to examples not using the display_3d() function of AssemblyGeometryNode (nodes.py)

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

---- >  Naming of assemblies and nodes that are translatable in various languages

******** Avoid duplication of STEP/STEPZIP loading


-----


******** rename shape on nodes to node_shape for clarity
******** shape returned by an assembly? -> ccad Solid(compound)

is it useful to keep the initial placement of nodes?

******** separate examples for assemblies of each part of the car, and for assemblies of assemblies

******** move _transform_anchors from nodes to geometry

******** wx viewer should be part of osvcad (coming from aocutils)
  ******** AUI or split window for UI (shelf + 3d + graph)
  Remove dependency of osvcad.ui.topology on aocutils
  integrate the graph viewer
  Set the assembly in the model to do the first tests
  callbacks for selections in the ui
  * MVC pattern using Atom + move away from calling the UI in nodes or assemblies
  Anchors display (and selectable)
    How to display a relationship that is not made of 2 vectors ??
  Live part coding (editor and viewer side by side)

---- >  nicer graph presentation

really global assembly of Tabby as an example

include some parts (motor) in the car example that are created from python scripts


-------
**** Nomenclature pieces
  ******** Ajouter la version de la nomenclature dans la nomenclature? -> Non, un peu lourd
  ******** Distinguer la nomenclature du plan de celle de l'instance
  ******** Possibilité de mettre des dimensions fonctionelles dans le champ 4 (d, r, l)
  ******** Add a field called "Subsystem" after sectorial to determine where the part is intended to be used.

Appliquer nomenclature pieces et ancres aux exemples
  Prioritaire car impacte la documentation

  ******** Nomenclature pièces supensions
  Nomenclature ancres suspensions
  ******** Nomenclatures pièces chassis
  Nomenclature ancres chassis
  ******** Nomenclature pièces roue
  ******** Nomenclature ancres roue

Packaging
  First, remove any dependency on aocutils or clean aocutils

Documentation
  10 minutes example

******** Matrice Business plan

******** Code review

Pub
 libremechanics.com

Notion of Assembly in ccad should disappear?

Not a priority
--------------
transformations.py cleanup
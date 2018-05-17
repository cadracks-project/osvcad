Todo Examples
-------------

Example with nested assemblies

really global assembly of Tabby as an example

include some parts (motor) in the car example that are created from python scripts

Appliquer nomenclature pieces et ancres aux exemples
  Prioritaire car impacte la documentation

  Nomenclature ancres suspensions
  Nomenclature ancres chassis

Todo UI
-------

Launcher must be executable

Better graph display
  Selectable nodes, coordinated with 3d view
  Different color based on origin/node type
  https://bokeh.pydata.org/en/latest/docs/user_guide/graph.html
  OR
  Vue 3D du graphe en fonction de critères (volume = f(volume piece), volume = f(prix), couleur=f(createur))
  Boule = pièce, boite = assemblage ....

  -> selection sync between 3D and graph

Gérer DataFrame général? -> ne pas parcourir le graphe à chaque requête!


-> Extend stepzip concept to igeszip and stlzip
  More complex than expected. ccad limits us to solid, compound and compsolid for imports
  Real cad projects may have to import shells/surfaces

-> Use a correct nomenclature for everything in sample projects
     Re-read docs nomenclature
     Correct problems in sample projects

Resizing problems of 3d viewer

Pre-compute simple representations of files that take a long time to load

Save button for code Enable/Disable depending on what is loaded

Undo/Redo

Core osvcad
-----------

-> lire transformations.py + doctests vers pytests

Apply correction for GetHandle() returns 0 on Linux to examples not using the display_3d() function of AssemblyGeometryNode (nodes.py)

Deplacement des anchors lors des déplacements dus au contraintes
  -> fonctions de transformation sur les nodes

-> Assemblies in assemblies in assemblies ...
      Document the code
      Clean
      More complex case -> rc car?
      ******** GeometryNode -> One class with multiple constructors

New anchors concept (normal + tangent)

---- >  Naming of assemblies and nodes that are translatable in various languages

Notion of Assembly in ccad should disappear?

is it useful to keep the initial placement of nodes?
Appliquer nomenclature pieces et ancres aux exemples
  Prioritaire car impacte la documentation

  Nomenclature ancres suspensions
  Nomenclature ancres chassis
Misc
----

Packaging
  First, remove any dependency on aocutils or clean aocutils

Documentation
  10 minutes example

Not a priority
--------------
transformations.py cleanup
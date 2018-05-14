Todo UI
-------

Better graph display
  Selectable nodes, coordinated with 3d view
  Different color based on origin/node type
  https://bokeh.pydata.org/en/latest/docs/user_guide/graph.html
  OR
  3D display with nodes position based on barycentre

-> Extend stepzip concept to igeszip and stlzip
  More complex than expected. ccad limits us to solid, compound and compsolid for imports
  Real cad projects may have to import shells/surfaces

-> Use a correct nomenclature for everything in sample projects
     Re-read docs nomenclature
     Correct problems in sample projects

Appliquer nomenclature pieces et ancres aux exemples
  Prioritaire car impacte la documentation

  Nomenclature ancres suspensions
  Nomenclature ancres chassis

-> Launch with command line
     ****** create bin that launches ui
     ****** conda package (0.6.0)
     ****** bin defined in setup
    needs sys.exit() to exit process when closed (does not return to command prompt when closed otherwise)

Resizing problems of 3d viewer

Pre-compute simple representations of files that take a long time to load

Save button for code Enable/Disable depending on what is loaded

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


Examples
--------

really global assembly of Tabby as an example

include some parts (motor) in the car example that are created from python scripts


Misc
----

Packaging
  First, remove any dependency on aocutils or clean aocutils

Documentation
  10 minutes example



Not a priority
--------------
transformations.py cleanup
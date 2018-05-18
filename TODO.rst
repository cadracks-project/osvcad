Pbs majeurs pour adoption
-------------------------

Ancres à 2 vecteurs (New anchors concept (normal + tangent))
  minimal : p, v1, v2
  extras : tolerance, dimension ...
  anchor files should be json, not flat text

Laisons méca = 10 liaisons élémentaires + liaison nulle + liaison complète

      Laison complète ou encastrement               tout                                        rien
      Liaison nulle ou libre                        rien                                        tout

    10 liaisons méca                                Liaisons                                    Libertés
      simples (6)
      -----------
      Liaison ponctuelle ou sphere/plan             Tz = 0                                      Tx, Ty, Rx, Ry, Rz
      Liaison linéaire rectiligne ou cylindre/plan  Tz = Z, Ry = M                              Tx, Ty, Rx, Rz
      Liaison linéaire annulaire ou sphère/cylindre Ty = 0, Tx = 0                              Tz, Rx, Ry, Rz          aka gouttière
      Liaison rotule, sphérique ou sphère/sphère    Tx = 0, Ty = 0, Tz = 0                      Rx, Ry, Rz                                          e.g. attache caravane
      Liaison pivot glissant ou cylindre/cylindre   Ty = 0, Tz = 0, Ry = 0, Rz = 0              Tx, Rx                  aka current anchor system   e.g. barre baby-foot
      Liaison appui plan ou plan/plan               Tz = 0, Rx = 0, Ry = 0                      Tx, Ty, Rz                                          e.g. tabouret à 3 pieds

      composées (4)
      -------------
      Laison pivot                                  Tx = 0, Ty = 0, Tz = 0, Rx = 0, Ry = 0      Rz                                                  e.g. pedale de velo
      Laison glissière                              Ty = 0, Tz = 0, Rx = 0, Ry = 0, Rz = 0      Tx                                                  e.g. queue d'aronde
      Liaison hélicoïdale                           x = u·θx, Ty = 0, Tz = 0, Ry = 0, Rz = 0    [u·θx, 0, 0, θx, 0, 0]                              e.g. ecrou et vis
      Liaison rotule à doigt                        Tx = 0, Ty = 0, Tz = 0, Rz = 0              Rx, Ry                                              e.g. joystick

Perfs / Caching

Joindre des assemblages entre eux -> exemple nested assemblies

Install facile

Projects hosting + visu + BOM etc ...

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

******** Launcher must be executable

Better graph display
  Selectable nodes, coordinated with 3d view
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
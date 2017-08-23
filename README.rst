Osvcad
======

.. figure:: img/cubes.png
   :scale: 100 %
   :alt: Current state

Warning : work in progress. Very very early stage of development

**Osvcad** is a CAD system that models systems using Acyclic Directed Graphs of heterogeneous geometrical entities.

Geometry
--------

The geometry of a product in **Osvcad** is handled by 2 classes: *GeometryNode* and *Assembly* (see `nodes.py <https://github.com/osv-team/osvcad/blob/master/osvcad/nodes.py>`_).

The *Assembly* is a child class of both *GeometryNode* and *networkx.DiGraph*). The consequence is that an *Assembly* can be used in a graph of GeometryNode(s) and Assembly(s) since an
*Assembly* is also a *GeometryNode*.



The geometrical entities representing parts and assemblies can come from:

- Python scripts

- STEP files

- JSON part library files

The edges of the graph handle the positioning of the entities using and *anchor* system.
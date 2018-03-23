# coding: utf-8

from atom.api import Atom
# from atom.enum import Enum
# from atom.list import List
# from atom.scalars import Str, Bool, Float, Range
# from atom.tuple import Tuple
from atom.typed import Typed

from osvcad.nodes import AssemblyGeometryNode


class Model(Atom):
    assembly = Typed(AssemblyGeometryNode)

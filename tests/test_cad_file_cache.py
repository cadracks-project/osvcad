#!/usr/bin/env python
# coding: utf-8

r"""transformations.py tests"""

from time import time
from osvcad.nodes import PartGeometryNode


def test_cache():
    r"""Test the angle_between vectors of transformations.py"""

    t0 = time()
    n1 = PartGeometryNode.from_stepzip("cad_files/rim.stepzip")
    t1 = time()
    n2 = PartGeometryNode.from_stepzip("cad_files/rim.stepzip")
    t2 = time()

    assert 100 * (t2 - t1) < (t1 - t0)

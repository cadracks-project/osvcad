#!/usr/bin/env python
# coding: utf-8

r"""transformations.py tests"""

from time import time
from corelib.core.files import path_from_file
from osvcad.nodes import Part


def test_cache():
    r"""Test the angle_between vectors of transformations.py"""

    t0 = time()
    _ = Part.from_stepzip(path_from_file(__file__,
                                                     "./cad_files/rim.stepzip"))
    t1 = time()
    _ = Part.from_stepzip(path_from_file(__file__,
                                                     "./cad_files/rim.stepzip"))
    t2 = time()

    assert 100 * (t2 - t1) < (t1 - t0)

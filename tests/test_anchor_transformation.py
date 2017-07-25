#!/usr/bin/env python
# coding: utf-8

r"""Anchor transformation tests"""

import numpy as np

from osvcad.nodes import _transform_anchor

# TODO : add more tests


def test_anchor_translation():
    r"""Test a translation matrix applied to an anchor"""
    # anchor at origin, pointing in X+ direction
    anchor = {"position": [0, 0, 0], "direction": [1, 0, 0]}

    # translation [1, 1, 1] matrix
    transformation_matrix = np.array([[1, 0, 0, 1],
                                      [0, 1, 0, 1],
                                      [0, 0, 1, 1]])

    anchor_1 = _transform_anchor(anchor, transformation_matrix)

    assert anchor_1["position"] == (1, 1, 1)
    assert anchor_1["direction"] == (1, 0, 0)


def test_anchor_combined_translation_rotation():
    r"""Test a transformation combining a translation 
    and a rotation on an anchor"""
    # anchor at origin, pointing in X+ direction
    anchor = {"position": [0, 0, 0], "direction": [1, 0, 0]}

    # rotate 90 deg around z axis
    transformation_matrix = np.array([[0, -1, 0, 1],
                                      [1, 0, 0, 1],
                                      [0, 0, 1, 1]])

    anchor_1 = _transform_anchor(anchor, transformation_matrix)

    assert anchor_1["position"] == (1, 1, 1)
    assert anchor_1["direction"] == (0, 1, 0)

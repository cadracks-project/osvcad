#!/usr/bin/env python
# coding: utf-8

r"""Affine transformation so that the Y set of points matches the X set of
points"""

import numpy as np
from numpy.linalg import pinv


def affine(X, Y):
    """ find affine transformation

    Parameters
    ----------

    X  : np.array
        3xN
    Y
        3xN

    Returns
    -------

    A : np.array
        3x3
    B : np.array
        3x1

    Notes
    -----

    Given X and Y find the affine transformation

    Y = A X + B

    """

    B = Y[:, 0][:, np.newaxis]
    Yc = Y - B
    pX = pinv(X)
    A = np.dot(Yc, pX)
    return A, B

if __name__ == "__main__":
    X = np.array([[0, 0, 1],
                  [0, 1, 0],
                  [1, 0, 0]])
    Y = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]])
    a, b = affine(X, Y)
    print(a)
    print("----")
    print(b)

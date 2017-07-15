# coding: utf-8

r"""Graph edges"""

import abc

import ccad.model as cm


class Constraint(object):
    r"""Abstract base class for constraints"""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.tx = 0.
        self.ty = 0.
        self.tz = 0.

        self.rx = 0.
        self.ry = 0.
        self.rz = 0.

        self.quaternion = None

    @abc.abstractmethod
    def transform(self, shape):
        r"""Shape placement function to respect the constraint"""
        raise NotImplementedError


class ConstraintCoaxial(Constraint):
    r"""Coaxiality constraint"""
    def __init__(self, obj1, obj2, axis1, axis2):
        super(ConstraintCoaxial, self).__init__()
        self.obj1 = obj1
        self.obj2 = obj2
        self.axis1 = axis1
        self.axis2 = axis2
        # solve constraint and affect t, r and quaternion

    def transform(self, shape):
        raise NotImplementedError


class ConstraintAbsolutePositioning(Constraint):
    r"""Positioning relative to the origin (of an assembly)
    
    Parameters
    ----------
    t : tuple
    r : tuple

    """
    def __init__(self, t, r):
        super(ConstraintAbsolutePositioning, self).__init__()
        self.tx, self.ty, self.tz = t
        self.rx, self.ry, self.rz = r

    def transform(self, shape):
        return cm.translated(
            cm.rotatedx(cm.rotatedy(cm.rotatedz(shape, self.rz), self.ry), self.rx),
            (self.tx, self.ty, self.tz))

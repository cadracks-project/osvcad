# coding: utf-8

r"""Decorators for code description"""


def overrides(func):
    r"""Decorator that signals that a method overrides a parent method.

    Does nothing, only there to help informing the developer
    """
    return func

#!/usr/bin/env python
# coding: utf-8

r"""Tabby rear suspension assembly"""

from car_assemblies import make_front_suspension_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    front_suspension_assembly_ = make_front_suspension_assembly()
    view_assembly(front_suspension_assembly_)
    view_assembly_graph(front_suspension_assembly_)

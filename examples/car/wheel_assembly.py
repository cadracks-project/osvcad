# coding: utf-8

r"""Tabby wheel assembly"""

from car_assemblies import make_wheel_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    wheel_assembly = make_wheel_assembly()
    view_assembly(wheel_assembly)
    view_assembly_graph(wheel_assembly)

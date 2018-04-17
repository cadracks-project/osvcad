# coding: utf-8

r"""Tabby rear suspension assembly"""

from car_assemblies import make_rear_suspension_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    rear_suspension_assembly_ = make_rear_suspension_assembly()
    view_assembly(rear_suspension_assembly_)
    view_assembly_graph(rear_suspension_assembly_)

#!/usr/bin/env python
# coding: utf-8

r"""Tabby global assembly of partial assemblies"""

from osvcad.nodes import Assembly
from osvcad.edges import ConstraintAnchor
from car_assemblies import make_wheel_assembly, make_rear_suspension_assembly
# from car_assemblies import  make_front_suspension_assembly, \
#                             make_chassis_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    # chassis_assembly_ = make_chassis_assembly()
    # front_suspension_assembly_ = make_front_suspension_assembly()
    rear_suspension_assembly_ = make_rear_suspension_assembly()
    wheel_assembly = make_wheel_assembly()

    rear_suspension_and_wheel_assembly = \
        Assembly(root=rear_suspension_assembly_)

    rear_suspension_and_wheel_assembly.add_edge(
        rear_suspension_assembly_,
        wheel_assembly,
        object=ConstraintAnchor(
            anchor_name_master="P7_Rear/outside",
            anchor_name_slave="rim/axle",
            distance=0,
            angle=0))

    view_assembly(rear_suspension_and_wheel_assembly)
    view_assembly_graph(rear_suspension_and_wheel_assembly)

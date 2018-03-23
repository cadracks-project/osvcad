#!/usr/bin/env python
# coding: utf-8

r"""Tabby global assembly of partial assemblies"""

import logging

from osvcad.nodes import AssemblyGeometryNode
from osvcad.edges import ConstraintAnchor
from car_assemblies import make_wheel_assembly, make_rear_suspension_assembly
# from car_assemblies import  make_front_suspension_assembly, \
#                             make_chassis_assembly

if __name__ == "__main__":
    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        _ = [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.INFO,
                        format='%(relativeCreated)6d :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    # chassis_assembly_ = make_chassis_assembly()
    # front_suspension_assembly_ = make_front_suspension_assembly()
    rear_suspension_assembly_ = make_rear_suspension_assembly()
    wheel_assembly = make_wheel_assembly()

    rear_suspension_and_wheel_assembly = \
        AssemblyGeometryNode(root=rear_suspension_assembly_)

    rear_suspension_and_wheel_assembly.add_edge(
        rear_suspension_assembly_,
        wheel_assembly,
        object=ConstraintAnchor(
            anchor_name_master="P7_Rear/outside",
            anchor_name_slave="rim/axle",
            distance=0,
            angle=0))

    # rear_suspension_and_wheel_assembly.display_3d()
    rear_suspension_and_wheel_assembly.display_3d()
    rear_suspension_and_wheel_assembly.show_plot()

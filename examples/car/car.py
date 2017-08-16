# coding: utf-8

r"""Example of a car model"""

import logging

from osvcad.nodes import GeometryNode, Assembly
from osvcad.edges import ConstraintAnchor


def make_chassis_assembly():
    r"""Chassis assembly creation"""

    p1_base = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P1-Base.stepzip")
    p2_l = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P2-L.stepzip")
    p2_r = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P2-R.stepzip")
    p4 = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P4.stepzip")
    p5 = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P5.stepzip")
    p6 = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P6.stepzip")
    p7_l = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P7-L.stepzip")
    p7_r = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P7-R.stepzip")
    p8 = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P8.stepzip")
    p9 = GeometryNode.from_stepzip(stepzip_file="shelf/chassis/P9.stepzip")

    chassis_assembly = Assembly(root=p1_base)

    chassis_assembly.add_edge(p1_base, p2_l, object=ConstraintAnchor(
        anchor_name_master="A2-L",
        anchor_name_slave="D3",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p2_r, object=ConstraintAnchor(
        anchor_name_master="A2-R",
        anchor_name_slave="D3",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p2_r, p4, object=ConstraintAnchor(
        anchor_name_master="B2",
        anchor_name_slave="B4",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p5, object=ConstraintAnchor(
        anchor_name_master="F2-R",
        anchor_name_slave="F1",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p6, object=ConstraintAnchor(
        anchor_name_master="G3-L",
        anchor_name_slave="A1",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p7_l, object=ConstraintAnchor(
        anchor_name_master="K3-L",
        anchor_name_slave="A4",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p7_r, object=ConstraintAnchor(
        anchor_name_master="K3-R",
        anchor_name_slave="A4",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p7_l, p8, object=ConstraintAnchor(
        anchor_name_master="B1",
        anchor_name_slave="A1",
        distance=0,
        angle=0))

    chassis_assembly.add_edge(p1_base, p9, object=ConstraintAnchor(
        anchor_name_master="H2",
        anchor_name_slave="A1",
        distance=0,
        angle=0))

    return chassis_assembly


def make_front_suspension_assembly():
    r"""Front suspension assembly creation"""
    pass


def make_rear_suspension_assembly():
    r"""Rear suspension assembly creation"""
    p1 = [GeometryNode.from_stepzip("shelf/suspension/common/P1.stepzip") for _ in range(4)]
    p2 = GeometryNode.from_stepzip("shelf/suspension/arr/P2.stepzip")
    p5 = GeometryNode.from_stepzip("shelf/suspension/arr/P5.stepzip")
    p8 = GeometryNode.from_stepzip("shelf/suspension/common/P8.stepzip")
    p9 = GeometryNode.from_stepzip("shelf/suspension/common/P9.stepzip")

    rear_suspension_assembly = Assembly(root=p2)

    rear_suspension_assembly.add_edge(p2, p1[0], object=ConstraintAnchor(
        anchor_name_master="out1",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p2, p1[1], object=ConstraintAnchor(
        anchor_name_master="out2",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p2, p1[2], object=ConstraintAnchor(
        anchor_name_master="in1",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p2, p1[3], object=ConstraintAnchor(
        anchor_name_master="in2",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p1[3], p5, object=ConstraintAnchor(
        anchor_name_master="narrow_out",
        anchor_name_slave="bottom2",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p5, p8, object=ConstraintAnchor(
        anchor_name_master="side1_top",
        anchor_name_slave="side1_top",
        distance=0,
        angle=14.566))

    rear_suspension_assembly.add_edge(p8, p9, object=ConstraintAnchor(
        anchor_name_master="top",
        anchor_name_slave="bottom",
        distance=-216.148,
        angle=0))

    return rear_suspension_assembly


def make_wheel_assembly():
    r"""Wheel assembly creation"""
    rim = GeometryNode.from_stepzip(stepzip_file="shelf/wheel/rim.stepzip")
    tyre = GeometryNode.from_stepzip(stepzip_file="shelf/wheel/tyre.stepzip")

    wheel_assembly = Assembly(root=rim)

    wheel_assembly.add_edge(rim, tyre, object=ConstraintAnchor(
        anchor_name_master="tyre",
        anchor_name_slave="side",
        distance=0,
        angle=0))

    return wheel_assembly


if __name__ == "__main__":
    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)6d :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    # chassis_assembly_ = make_chassis_assembly()
    # chassis_assembly_.display_3d()

    rear_suspension_assembly_ = make_rear_suspension_assembly()
    rear_suspension_assembly_.display_3d()

    # wheel_assembly = make_wheel_assembly()
    # wheel_assembly.display_3d()
    # wheel_assembly.show_plot()

# coding: utf-8

r"""Example of a car model"""

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
    pass


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
    chassis_assembly = make_chassis_assembly()
    chassis_assembly.display_3d()

    # wheel_assembly = make_wheel_assembly()
    # wheel_assembly.display_3d()
    # wheel_assembly.show_plot()

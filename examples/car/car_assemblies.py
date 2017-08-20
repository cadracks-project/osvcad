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
    p1 = [GeometryNode.from_stepzip("shelf/suspension/common/P1.stepzip") for _ in range(2)]
    p2 = GeometryNode.from_stepzip("shelf/suspension/av/P2.stepzip")
    p3 = GeometryNode.from_stepzip("shelf/suspension/av/P3.stepzip")
    p4 = GeometryNode.from_stepzip("shelf/suspension/av/P4.stepzip")
    p5 = GeometryNode.from_stepzip("shelf/suspension/av/P5.stepzip")
    p6 = GeometryNode.from_stepzip("shelf/suspension/common/P6.stepzip")
    p7 = GeometryNode.from_stepzip("shelf/suspension/common/P7.stepzip",
                                   instance_id="P7_Front")
    p8 = GeometryNode.from_stepzip("shelf/suspension/common/P8.stepzip")
    p9 = GeometryNode.from_stepzip("shelf/suspension/common/P9.stepzip")
    p10 = GeometryNode.from_stepzip("shelf/suspension/common/P10.stepzip")
    p11 = GeometryNode.from_stepzip("shelf/suspension/common/P11.stepzip")
    p12 = GeometryNode.from_stepzip("shelf/suspension/common/P12.stepzip")

    front_suspension_assembly = Assembly(root=p2)

    front_suspension_assembly.add_edge(p2, p1[0], object=ConstraintAnchor(
        anchor_name_master="out1",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    front_suspension_assembly.add_edge(p2, p1[1], object=ConstraintAnchor(
        anchor_name_master="out2",
        anchor_name_slave="wide_out",
        distance=0,
        angle=0))

    front_suspension_assembly.add_edge(p2, p3, object=ConstraintAnchor(
        anchor_name_master="in_inside",
        anchor_name_slave="main",
        distance=-71.396,
        angle=0))

    front_suspension_assembly.add_edge(p3, p4, object=ConstraintAnchor(
        anchor_name_master="perp",
        anchor_name_slave="cone",
        distance=6.2,
        angle=0))

    front_suspension_assembly.add_edge(p4, p5, object=ConstraintAnchor(
        anchor_name_master="ball",
        anchor_name_slave="ball",
        distance=0,
        angle=0))

    front_suspension_assembly.add_edge(p5, p8, object=ConstraintAnchor(
        anchor_name_master="side1_top",
        anchor_name_slave="side2_top",
        distance=0,
        angle=-14.566))

    front_suspension_assembly.add_edge(p8, p9, object=ConstraintAnchor(
        anchor_name_master="top",
        anchor_name_slave="bottom",
        distance=-216.148,
        angle=0))

    front_suspension_assembly.add_edge(p9, p12, object=ConstraintAnchor(
        anchor_name_master="top",
        anchor_name_slave="bottom",
        distance=1.24,
        angle=0))

    front_suspension_assembly.add_edge(p12, p11, object=ConstraintAnchor(
        anchor_name_master="bottom",
        anchor_name_slave="bottom",
        distance=0,
        angle=0))

    front_suspension_assembly.add_edge(p11, p10, object=ConstraintAnchor(
        anchor_name_master="wide_flat",
        anchor_name_slave="axis_bottom",
        distance=0,
        angle=0))

    # TODO : create a way to position p6 on p5 and p7 on p6 so that the
    #        holes are in front of one another without requiring
    #        a 'magic' angle value

    front_suspension_assembly.add_edge(p5, p6, object=ConstraintAnchor(
        anchor_name_master="wheel_axis",
        anchor_name_slave="axis_drive",
        distance=0,
        angle=0))

    front_suspension_assembly.add_edge(p6, p7, object=ConstraintAnchor(
        anchor_name_master="axis_disc",
        anchor_name_slave="inside",
        distance=0,
        angle=0))

    return front_suspension_assembly


def make_rear_suspension_assembly():
    r"""Rear suspension assembly creation"""
    p1 = [GeometryNode.from_stepzip("shelf/suspension/common/P1.stepzip") for _ in range(4)]
    p2 = GeometryNode.from_stepzip("shelf/suspension/arr/P2.stepzip")
    p5 = GeometryNode.from_stepzip("shelf/suspension/arr/P5.stepzip")
    p7 = GeometryNode.from_stepzip("shelf/suspension/common/P7.stepzip", instance_id="P7_Rear")
    p8 = GeometryNode.from_stepzip("shelf/suspension/common/P8.stepzip")
    p9 = GeometryNode.from_stepzip("shelf/suspension/common/P9.stepzip")
    p10 = GeometryNode.from_stepzip("shelf/suspension/common/P10.stepzip")
    p11 = GeometryNode.from_stepzip("shelf/suspension/common/P11.stepzip")
    p12 = GeometryNode.from_stepzip("shelf/suspension/common/P12.stepzip")

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

    rear_suspension_assembly.add_edge(p5, p7, object=ConstraintAnchor(
        anchor_name_master="wheel_axis",
        anchor_name_slave="inside",
        distance=62,
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

    rear_suspension_assembly.add_edge(p9, p12, object=ConstraintAnchor(
        anchor_name_master="top",
        anchor_name_slave="bottom",
        distance=1.24,
        angle=0))

    rear_suspension_assembly.add_edge(p12, p11, object=ConstraintAnchor(
        anchor_name_master="bottom",
        anchor_name_slave="bottom",
        distance=0,
        angle=0))

    rear_suspension_assembly.add_edge(p11, p10, object=ConstraintAnchor(
        anchor_name_master="wide_flat",
        anchor_name_slave="axis_bottom",
        distance=0,
        angle=0))

    return rear_suspension_assembly


def make_wheel_assembly():
    r"""Wheel assembly creation"""
    rim = GeometryNode.from_stepzip(stepzip_file="shelf/wheel/rim.stepzip",
                                    instance_id="rim")
    tyre = GeometryNode.from_stepzip(stepzip_file="shelf/wheel/tyre.stepzip")

    wheel_assembly = Assembly(root=rim)

    wheel_assembly.add_edge(rim, tyre, object=ConstraintAnchor(
        anchor_name_master="tyre",
        anchor_name_slave="side",
        distance=0,
        angle=0))

    return wheel_assembly

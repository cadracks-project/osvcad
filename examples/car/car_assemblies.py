# coding: utf-8

r"""Example of a car model"""

import logging

from osvcad.nodes import PartGeometryNode, AssemblyGeometryNode
from osvcad.edges import ConstraintAnchor


def make_chassis_assembly():
    r"""Chassis assembly creation"""

    p1_base = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/CAR_CHASSIS_BASE_2.38#0.179#1.18_STEEL__.stepzip")
    p2_l = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_ARCHLEFT_705#515#184#mm_STEEL__.stepzip")
    p2_r = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_ARCHRIGHT_705#515#184#mm_STEEL__.stepzip")
    p4 = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_ARCHSTRUT_127#126#796#mm_STEEL__.stepzip")
    p5 = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_SEATSSUPPORT_410#151#1174#mm_STEEL__.stepzip")
    p6 = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_DASHBOARDSUPPORT_107#535#1184#mm_STEEL__.stepzip")
    p7_l = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_SUSPENSION_ARCHLEFT_526#535#284#mm_STEEL__.stepzip")
    p7_r = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_SUSPENSION_ARCHRIGHT_526#535#284#mm_STEEL__.stepzip")
    p8 = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_ARCHSTRUT_111#130#746#mm_STEEL__.stepzip")
    p9 = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/chassis/"
                     "CAR_CHASSIS_DASHBOARDSUPPORTREINFORCEMENT_205#525#75#mm_STEEL__.stepzip")

    chassis_assembly = AssemblyGeometryNode(root=p1_base)

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
    p1 = [PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_BEARING_l54.7#d37#mm___.stepzip") for _ in range(2)]

    p2 = PartGeometryNode.from_stepzip(
        "shelf/suspension/front/"
        "CAR_SUSPENSION_FORK_320#44#270#mm___.stepzip")
    p3 = PartGeometryNode.from_stepzip(
        "shelf/suspension/front/"
        "CAR_SUSPENSION_LINK_28#23#124#mm___.stepzip")
    p4 = PartGeometryNode.from_stepzip(
        "shelf/suspension/front/"
        "CAR_DIRECTION_BALLHEAD_D23#d10#l70#mm___.stepzip")
    p5 = PartGeometryNode.from_stepzip(
        "shelf/suspension/front/"
        "CAR_SUSPENSION_HUB_107#212#84#mm___.stepzip")

    p6 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_DISCSUPPORT_117#117#70#mm___.stepzip")
    p7 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_AXLE_DISC_d227#h46#mm_STEEL__.stepzip",
        instance_id="P7_Front")
    p8 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_CYLINDER_l320#d42___.stepzip")
    p9 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_PISTON_l381#d33#d16_STEEL__.stepzip")
    p10 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_HAT_102#40#70#mm___.stepzip")
    p11 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_HEAD_60#48#67#mm___.stepzip")
    p12 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_NECK_d28#l51#mm___.stepzip")

    front_suspension_assembly = AssemblyGeometryNode(root=p2)

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
    p1 = [PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_BEARING_l54.7#d37#mm___.stepzip") for _ in range(4)]
    p2 = PartGeometryNode.from_stepzip(
        "shelf/suspension/rear/"
        "CAR_SUSPENSION_FRAME_320#49#327#mm___.stepzip")
    p5 = PartGeometryNode.from_stepzip(
        "shelf/suspension/rear/"
        "CAR_SUSPENSION_HUB_200#240#82#mm___.stepzip")
    p7 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_AXLE_DISC_d227#h46#mm_STEEL__.stepzip",
        instance_id="P7_Rear")
    p8 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_CYLINDER_l320#d42___.stepzip")
    p9 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_PISTON_l381#d33#d16_STEEL__.stepzip")
    p10 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_HAT_102#40#70#mm___.stepzip")
    p11 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_HEAD_60#48#67#mm___.stepzip")
    p12 = PartGeometryNode.from_stepzip(
        "shelf/suspension/common/"
        "CAR_SUSPENSION_NECK_d28#l51#mm___.stepzip")

    rear_suspension_assembly = AssemblyGeometryNode(root=p2)

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
    rim = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/wheel/"
                     "CAR_WHEEL_RIM_D416#l174#mm___.stepzip",
        instance_id="rim")
    tyre = PartGeometryNode.from_stepzip(
        stepzip_file="shelf/wheel/CAR_WHEEL_TYRE_D575#l178#mm_RUBBER__.stepzip")

    wheel_assembly = AssemblyGeometryNode(root=rim)

    wheel_assembly.add_edge(rim, tyre, object=ConstraintAnchor(
        anchor_name_master="AXIS_TYRE_d412#mm_",
            anchor_name_slave="AXIS_SIDE_d383#mm_",
        distance=0,
        angle=0))

    return wheel_assembly

#!/usr/bin/env python
# coding: utf-8

r"""Visual testing for a situation similar to the car suspension issue"""

import logging

import wx
#
from osvcad.nodes import PartGeometryNode, AssemblyGeometryNode
from osvcad.edges import ConstraintAnchor
from ccad.model import cylinder, box
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ
from OCC.gp import gp_Vec, gp_Pnt

logger = logging.getLogger(__name__)


def main():
    r"""Main function of the example"""
    logger.debug("**** Creating cube GeometryNode ****")
    cube_node = PartGeometryNode(box(10, 10, 10), anchors={
        "midface": {"position": (5, 10, 5), "direction": (0, 1, 0)}})

    logger.debug("**** Creating cylinder GeometryNode ****")
    n1 = PartGeometryNode(cylinder(10, 50), anchors={
        "bottom": {"position": (0, 0, 0), "direction": (0, 0, -1)},
        "top": {"position": (0, 0, 50), "direction": (0, 0, 1)},
        "side": {"position": (0, -10, 0), "direction": (0, -1, 0)}
    })

    n2 = PartGeometryNode(cylinder(10, 50), anchors={
        "bottom": {"position": (0, 0, 0), "direction": (0, 0, -1)},
        "top": {"position": (0, 0, 50), "direction": (0, 0, 1)},
        "side": {"position": (0, -10, 0), "direction": (0, -1, 0)}
    })

    logger.debug("**** Creating Assembly ****")
    a = AssemblyGeometryNode(root=cube_node)

    logger.debug("**** Adding edge to assembly****")
    a.add_edge(cube_node, n1, object=ConstraintAnchor(
        anchor_name_master="midface",
        anchor_name_slave="side",
        distance=0,
        angle=45))

    a.add_edge(n1, n2, object=ConstraintAnchor(
        anchor_name_master="top",
        anchor_name_slave="bottom",
        distance=0,
        angle=0))

    logger.debug("**** Done adding edges to assembly****")

    # a.build()

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            self.Show()

    app = wx.App()
    frame = MyFrame()

    # for k in cube_node.anchors.keys():
    #     frame.p.display_vector(gp_Vec(*cube_node.anchors[k]["direction"]),
    #                                gp_Pnt(*cube_node.anchors[k]["position"]))
    # frame.p.display_shape(cube_node.shape.shape,
    #                           color=colour_wx_to_occ((255, 0, 0)),
    #                           transparency=0.5)
    #
    # for k in n1.anchors.keys():
    #     frame.p.display_vector(gp_Vec(*n1.anchors[k]["direction"]),
    #                                gp_Pnt(*n1.anchors[k]["position"]))
    # frame.p.display_shape(n1.shape.shape,
    #                           color=colour_wx_to_occ((255, 0, 0)),
    #                           transparency=0.5)

    for k in a.anchors.keys():
        logger.debug("**** Displaying anchor %s of assembly****" % k)
        frame.p.display_vector(gp_Vec(*a.anchors[k]["direction"]),
                                   gp_Pnt(*a.anchors[k]["position"]))

    frame.p.display_shape(a.node_shape.shape)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":

    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    logging.info("Starting")
    main()
    logging.info("Ending")

#!/usr/bin/env python
# coding: utf-8

r"""Placing a cube over another cube using anchors"""

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                           ':: %(lineno)3d :: %(message)s')

from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ
from OCC.gp import gp_Pnt, gp_Vec
import wx
from osvcad.nodes import GeometryNodeDirect
from ccad.model import box, translated


def main():
    r"""Main example function"""
    # Create nodes
    node_1 = GeometryNodeDirect(box(10, 10, 10),
                                anchors={"only_anchor": {"position": (5, 5, 10),
                                                         "direction": (0, 0, 20)
                                                         }})

    node_2 = GeometryNodeDirect(translated(box(20, 20, 20), (100, 0, 0)),
                                anchors={"only_anchor": {"position": (110,
                                                                      10,
                                                                      20),
                                                         "direction": (0, 0, 20)
                                                         }})

    node_3 = node_1.place(self_anchor="only_anchor",
                          other=node_2,
                          other_anchor="only_anchor")

    px1, py1, pz1 = node_1.anchors["only_anchor"]["position"]
    dx1, dy1, dz1 = node_1.anchors["only_anchor"]["direction"]

    px2, py2, pz2 = node_2.anchors["only_anchor"]["position"]
    dx2, dy2, dz2 = node_2.anchors["only_anchor"]["direction"]

    px3, py3, pz3 = node_3.anchors["only_anchor"]["position"]
    dx3, dy3, dz3 = node_3.anchors["only_anchor"]["direction"]

    # box3 = transformed(node_2.shape, transformation_mat_)

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            self.Show()

    app = wx.App()
    frame = MyFrame()
    # RED
    frame.p.display_shape(node_1.shape.shape,
                          color=colour_wx_to_occ((255, 0, 0)),
                          transparency=0.5)

    # frame.p.display_shape(gp_Pnt(px1, py1, pz1))
    frame.p.display_vector(gp_Vec(dx1, dy1, dz1), gp_Pnt(px1, py1, pz1))
    # GREEN
    frame.p.display_shape(node_2.shape.shape,
                          color=colour_wx_to_occ((0, 255, 0)),
                          transparency=0.2)

    # frame.p.display_shape(gp_Pnt(px2, py2, pz2))
    frame.p.display_vector(gp_Vec(dx2, dy2, dz2), gp_Pnt(px2, py2, pz2))
    # BLUE
    frame.p.display_shape(node_3.shape.shape,
                          color=colour_wx_to_occ((0, 0, 255)),
                          transparency=0.8)
    frame.p.display_shape(gp_Pnt(px3, py3, pz3))
    frame.p.display_vector(gp_Vec(dx3, dy3, dz3), gp_Pnt(px3, py3, pz3))
    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":

    main()

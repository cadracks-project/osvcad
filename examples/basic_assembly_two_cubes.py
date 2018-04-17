#!/usr/bin/env python
# coding: utf-8

r"""Placing a cube over another cube using anchors"""

import logging

import wx
from osvcad.nodes import PartGeometryNode
from ccad.model import box, translated

from osvcad.view import OsvCadFrame


def main():
    r"""Main example function"""
    # Create nodes
    node_1 = PartGeometryNode(box(10, 10, 10),
                              anchors={"only_anchor": {"position": (5, 5, 10),
                                                       "direction": (0, 0, 20)
                                                       }})

    node_2 = PartGeometryNode(translated(box(20, 20, 20), (100, 0, 0)),
                              anchors={"only_anchor": {"position": (110, 10, 20),
                                                       "direction": (0, 0, 20)
                                                       }})

    node_3 = node_1.place(self_anchor="only_anchor",
                          other=node_2,
                          other_anchor="only_anchor")

    # box3 = transformed(node_2.shape, transformation_mat_)

    app = wx.App()
    frame = OsvCadFrame()

    # RED
    frame.display_part(node_1, color_255=(255, 0, 0), transparency=0.5)

    # GREEN
    frame.display_part(node_2, color_255=(0, 255, 0), transparency=0.2)

    # BLUE
    frame.display_part(node_3, color_255=(0, 0, 255), transparency=0.8)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                               ':: %(lineno)3d :: %(message)s')
    main()

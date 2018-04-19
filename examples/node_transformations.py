#!/usr/bin/env python
# coding: utf-8

r"""Node transformations visual tests"""

from __future__ import division

import wx
from osvcad.nodes import Part
from ccad.model import box, translated

from osvcad.view import OsvCadFrame

node_1 = Part(translated(box(30, 20, 10),
                         (0, 0, 0)),
              anchors={"a1": {"position": (5, 5, 10),
                              "direction": (0, 0, 1)},
                       "a2": {"position": (30, 10, 5),
                              "direction": (1, 0, 1)}})

node_2 = node_1.translate((0, 0, 15))

node_3 = node_1.rotate(45, (0, 1, 0), (0, 0, 0))

node_4 = node_1.rotate(45, (0, 1, 0), (-30, 0, 0))


def main():
    r"""Main function of the example"""
    app = wx.App()
    frame = OsvCadFrame()

    frame.display_part(node_1, (255, 0, 0), transparency=0.5)
    frame.display_part(node_2, (128, 0, 0), transparency=0.5)
    frame.display_part(node_3, (255, 0, 255), transparency=0.5)
    frame.display_part(node_4, (255, 128, 255), transparency=0.5)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    main()

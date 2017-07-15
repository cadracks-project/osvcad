#!/usr/bin/env python
# coding: utf-8

r"""Organising (initially) randomly placed cubes using anchors"""

from random import randint
import wx
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ
from osvcad.nodes import GeometryNodeDirect
from ccad.model import box, translated


def main():
    r"""Main example function"""
    # Create n cubes with anchors
    random_range = 800

    nb_cubes = 200

    cubes = list()
    new_cubes = list()

    for _ in range(nb_cubes):
        randx = randint(-random_range, random_range)
        randy = randint(-random_range, random_range)
        randz = randint(-random_range, random_range)
        cubes.append(GeometryNodeDirect(translated(box(10, 10, 10),
                                                   (randx, randy, randz)),
                                        anchors={
                                            "top": {"position": (5 + randx,
                                                                 5 + randy,
                                                                 10 + randz),
                                                    "direction": (0, 0, 1)},
                                            "bottom": {"position": (5 + randx,
                                                                    5 + randy,
                                                                    0+randz),
                                                       "direction": (0, 0, -1)}}))
    new_cubes.append(cubes[0])

    for i, cube in enumerate(cubes[:-1]):
        new_cubes.append(new_cubes[i].place(self_anchor="top",
                                            other=cubes[i + 1],
                                            other_anchor="bottom"))

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            self.Show()

    app = wx.App()
    frame = MyFrame()
    frame.p.display_shape(cubes[0].shape.shape,
                          color=colour_wx_to_occ((255, 0, 255)),
                          transparency=0.5)

    # Initial cubes in red
    for c in cubes[1:]:
        frame.p.display_shape(c.shape.shape,
                              color=colour_wx_to_occ((255, 0, 0)),
                              transparency=0.5)

    # New cubes placed using anchors in green
    for new_cube in new_cubes[1:]:
        frame.p.display_shape(new_cube.shape.shape,
                              color=colour_wx_to_occ((0, 255, 0)),
                              transparency=0.5)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    main()

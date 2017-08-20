#!/usr/bin/env python
# coding: utf-8

r"""Organising (initially) randomly placed cubes using anchors"""

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)8s :: %(module)20s '
                           ':: %(lineno)3d :: %(message)s')

from random import randint
import wx
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ
from osvcad.nodes import GeometryNode
from ccad.model import box, translated

logger = logging.getLogger(__name__)


def main():
    r"""Main example function"""
    # Create n cubes with anchors
    random_range = 200

    nb_cubes = 100

    cubes = list()
    new_cubes = list()

    for _ in range(nb_cubes):
        randx = randint(-random_range, random_range)
        randy = randint(-random_range, random_range)
        randz = randint(-random_range, random_range)
        cubes.append(GeometryNode(
            box(30, 20, 10),
            anchors={"top": {"position": (15, 10, 10), "direction": (0, 0, 1)},
                     "bottom": {"position": (15, 10, 0), "direction": (0, 0, -1)}
                     }).translate((randx, randy, randz))
                     .rotate(30., (1., 1., 1.), (0., 0., 0.))
        )

    new_cubes.append(cubes[0])

    for i, cube in enumerate(cubes[:-1]):
        logger.debug("CUBE %i" % i)
        new_cubes.append(new_cubes[i].place(self_anchor="top",
                                            other=cubes[i + 1],
                                            other_anchor="bottom",
                                            angle=11. + 11. * i,
                                            distance=0.))

    class MyFrame(wx.Frame):
        r"""Frame for testing"""
        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            self.Show()

    app = wx.App()
    frame = MyFrame()
    frame.p.display_shape(cubes[0].node_shape.shape,
                          color=colour_wx_to_occ((255, 255, 255)),
                          transparency=0.)

    # Initial cubes in orange
    for c in cubes[1:]:
        frame.p.display_shape(c.node_shape.shape,
                              color=colour_wx_to_occ((255, 136, 64)),
                              transparency=0.)

    # New cubes placed using anchors in shades of blue (changing every
    # 10 cubes)
    colors = ((61, 79, 153), (0, 184, 255))
    color = colors[0]
    for i, new_cube in enumerate(new_cubes[1:], 1):
        if i % 10 == 0:
            if (i/10) % 2 == 0:
                color = colors[0]
            else:
                color = colors[1]
        frame.p.display_shape(new_cube.node_shape.shape,
                              color=colour_wx_to_occ(color),
                              transparency=0.)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# coding: utf-8

r"""Visual testing of placing a cube relative to another cube

The example is designed to test many cases visually

"""

from __future__ import division

import wx
from osvcad.nodes import PartGeometryNode
from ccad.model import box, translated

from osvcad.view import OsvCadFrame


def make_case(case_offset,
              internal_offset,
              cube_1_dimensions,
              cube_2_dimensions,
              anchor_1,
              anchor_2):
    r"""Create a visual test case

    Parameters
    ----------
    case_offset : Tuple[float, float, float]
        Case offset so that all cases can be visualized
        without overlapping each other
    internal_offset : Tuple[float, float, float]
        Offset of the 2nd cube that will be positioned relative
        to the first cube
    cube_1_dimensions : Tuple[float, float, float]
    cube_2_dimensions : Tuple[float, float, float]
    anchor_1 : str
        Anchor position on first cube
        Must be in 'top', 'bottom', 'north', 'east', 'south', 'west'
    anchor_2 : str
        Anchor position on second cube
        Must be in 'top', 'bottom', 'north', 'east', 'south', 'west'

    Returns
    -------
    Tuple[GeometryNode, GeometryNode, GeometryNode]
        Cubes 1, 2 and 3 (3 is transformed 2) as GeometryNode(s)

    """
    cox, coy, coz = case_offset
    iox, ioy, ioz = internal_offset
    total_offset = cox + iox, coy + ioy, coz + ioz

    node_1 = PartGeometryNode(translated(box(*cube_1_dimensions), case_offset),
                              anchors={"only_anchor": _compute_anchor_position(case_offset,
                                                                               cube_1_dimensions,
                                                                               anchor_1)})

    node_2 = PartGeometryNode(translated(translated(box(*cube_2_dimensions),
                                                    internal_offset),
                                         case_offset),
                              anchors={"only_anchor": _compute_anchor_position(total_offset,
                                                                               cube_2_dimensions,
                                                                               anchor_2)})

    node_3 = node_1.place(self_anchor="only_anchor",
                          other=node_2,
                          other_anchor="only_anchor")

    return node_1, node_2, node_3


def _compute_anchor_position(offset, cube_dimensions, anchor_pos):
    r"""Position and direction of a cube anchor depending on the cube
    position and dimensions

    Parameters
    ----------
    offset : Tuple[float, float, float]
    cube_dimensions : Tuple[float, float, float]
    anchor_pos : str
        Anchor position on cube
        Must be in 'top', 'bottom', 'north', 'east', 'south', 'west'

    """
    tox, toy, toz = offset
    dx, dy, dz = cube_dimensions
    d = {"top": {"position": (tox + dx / 2, toy + dy / 2, toz + dz),
                 "direction": (0, 0, 1)},
         "bottom": {"position": (tox + dx / 2, toy + dy / 2, toz),
                    "direction": (0, 0, -1)},
         "north": {"position": (tox + dx, toy + dy/2, toz + dz / 2),
                   "direction": (1, 0, 0)},
         "east": {"position": (tox + dx / 2, toy, toz + dz / 2),
                  "direction": (0, -1, 0)},
         "south": {"position": (tox, toy + dy / 2, toz + dz / 2),
                   "direction": (-1, 0, 0)},
         "west": {"position": (tox + dx / 2, toy + dy, toz + dz / 2),
                  "direction": (0, 1, 0)}}

    return d[anchor_pos]


def main():
    r"""Main function of the example"""
    app = wx.App()
    frame = OsvCadFrame()

    cube1_possibilities = ["top", "south"]
    cube2_possibilities = ["top", "bottom", "north", "east", "south", "west"]

    cases = list()
    for i, cube_1_possibility in enumerate(cube1_possibilities):
        for j, cube2_possibility in enumerate(cube2_possibilities):
            cases.append(make_case(case_offset=(0.,
                                                (i * len(cube2_possibilities) + j) * 50.,
                                                 0.),
                                   internal_offset=(100., 0., 0.),
                                   cube_1_dimensions=(20., 10., 10.),
                                   cube_2_dimensions=(20., 20., 20.),
                                   anchor_1=cube_1_possibility,
                                   anchor_2=cube2_possibility))

    for (n1, n2, n3) in cases:

        # Node 1 : RED
        frame.display_part(n1, color_255=(255, 0, 0), transparency=0.5)

        # Node 2 : GREY
        frame.display_part(n2, color_255=(64, 64, 64), transparency=0.2)

        # Node 3 : BLUE
        frame.display_part(n3, color_255=(0, 0, 255), transparency=0.8)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    main()

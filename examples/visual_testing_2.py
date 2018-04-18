#!/usr/bin/env python
# coding: utf-8

r"""Visual testing for a situation similar to the car suspension issue"""

import logging

import wx

from osvcad.nodes import Part, Assembly
from osvcad.edges import ConstraintAnchor
from ccad.model import cylinder, box

from osvcad.view import OsvCadFrame

logger = logging.getLogger(__name__)


def main():
    r"""Main function of the example"""
    logger.debug("**** Creating cube GeometryNode ****")
    cube_node = Part(box(10, 10, 10),
                     anchors={"midface": {"position": (5, 10, 5),
                                                      "direction": (0, 1, 0)}})

    logger.debug("**** Creating cylinder GeometryNode ****")
    n1 = Part(cylinder(10, 50),
              anchors={"bottom": {"position": (0, 0, 0),
                                              "direction": (0, 0, -1)},
                                   "top": {"position": (0, 0, 50),
                                           "direction": (0, 0, 1)},
                                   "side": {"position": (0, -10, 0),
                                            "direction": (0, -1, 0)}
    })

    n2 = Part(cylinder(10, 50),
              anchors={"bottom": {"position": (0, 0, 0),
                                              "direction": (0, 0, -1)},
                                   "top": {"position": (0, 0, 50),
                                           "direction": (0, 0, 1)},
                                   "side": {"position": (0, -10, 0),
                                            "direction": (0, -1, 0)}
    })

    logger.debug("**** Creating Assembly ****")
    a = Assembly(root=cube_node)

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

    app = wx.App()
    frame = OsvCadFrame()

    frame.display_part(cube_node, transparency=0.5)
    frame.display_part(n1, transparency=0.5)
    frame.display_part(n2, transparency=0.5)

    frame.display_assembly(a)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":

    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        _ = [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)s :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')
    logging.info("Starting")
    main()
    logging.info("Ending")

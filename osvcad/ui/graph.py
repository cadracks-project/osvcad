# coding: utf-8

r"""3D visualization of geometry"""

from __future__ import division

import imp
from os.path import isdir, splitext
import logging

import wx
from OCC.Core.gp import gp_Pnt, gp_Vec

from corelib.core.python_ import is_valid_python
from corelib.core.memoize import memoize
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ

from osvcad.ui.sequences import color_from_sequence

logger = logging.getLogger(__name__)


class GraphPanel(Wx3dViewer):
    r"""Panel containing topology information about the loaded shape"""
    def __init__(self,
                 parent,
                 model,
                 viewer_background_color=(50., 50., 50.),
                 object_transparency=0.2, text_height=20,
                 text_colour=(0., 0., 0.)):
        super(GraphPanel, self).__init__(parent=parent,
                                         viewer_background_color=viewer_background_color,
                                         show_topology_menu=False)
        self.model = model
        self.model.observe("selected_changed", self.on_selected_change)

        self.viewer_display.View.SetBackgroundColor(colour_wx_to_occ(viewer_background_color))

        self.objects_transparency = object_transparency
        self.text_height = text_height
        self.text_colour = text_colour

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self.Layout()

    def on_selected_change(self, change):
        """Callback function for listener"""

        # TODO: investigate why importing Part
        # at top of file causes an app crash
        from osvcad.nodes import Part

        logger.debug("Selection changed")

        sel = self.model.selected

        if not isdir(sel):
            # what extension ?
            ext = splitext(sel)[1].lower()

            logger.info("File extension : %s" % ext)

            if ext == ".py":
                with open(sel) as f:
                    content = f.read()

                if is_valid_python(content) is True:
                    with wx.BusyInfo("Loading Python defined geometry ...") as _:
                        module_ = imp.load_source(sel, sel)
                    # has_part = hasattr(module_, "part")
                    has_assembly = hasattr(module_, "assembly")
                    # has_anchors = hasattr(module_, "anchors")

                    self.erase_all()

                    if has_assembly is True:
                        logger.info("%s has assembly" % sel)
                        try:
                            self.display_assembly(module_.assembly, transparency=0.4)
                        except KeyError as ke:
                            self.erase_all()
                            logger.exception(ke)
                    else:
                        self.erase_all()
                        logger.warning("Nothing to display in graph panel")
                else:  # the file is not a valid Python file
                    logger.warning("Not a valid python file")
                    self.erase_all()

            elif ext in [".step", ".stp", ".iges", ".igs", ".stl", ".json",
                         ".stepzip", ".anchors"]:
                self.erase_all()

        else:  # a directory is selected
            self.erase_all()

        self.Layout()

        logger.debug("code change detected in 3D panel")

    def display_part(self, part, color_255=None, transparency=0.):
        r"""Display a single Part (shape + anchors)

        Parameters
        ----------
        part : PartGeometryNode
        color_255 : tuple of integers from 0 to 255
        transparency : float from 0 to 1

        """
        pass

    def display_assembly(self, assembly, transparency=0.):
        r"""Display an assembly of parts and assemblies

        Parameters
        ----------
        assembly : AssemblyGeometryNode
        transparency : float from 0 to 1

        """
        assembly.build()

        for i, node in enumerate(assembly.nodes()):

            # display a sphere at the barycentre
            from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
            sphere = BRepPrimAPI_MakeSphere(_centre_of_mass(node.node_shape.shape),
                                            _characteristic_dimension(node.node_shape.shape) / 10.)
            sphere.Build()
            self.display_shape(sphere.Shape(),
                               # color_=colour_wx_to_occ((randint(0, 255),
                               #                          randint(0, 255),
                               #                          randint(0, 255))),
                               color_=colour_wx_to_occ(color_from_sequence(i, "colors")),
                               transparency=transparency)

            # self._display_anchors(assembly.anchors)

        for edge in assembly.edges(data=True):
            start = _centre_of_mass(edge[0].node_shape.shape)  # gp_Pnt
            end = _centre_of_mass(edge[1].node_shape.shape)  # gp_Pnt

            vec = gp_Vec(end.X() - start.X(),
                         end.Y() - start.Y(),
                         end.Z() - start.Z())
            from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
            e = BRepBuilderAPI_MakeEdge(start, end)

            self.display_shape(e.Shape())

            edge_constraint = assembly.get_edge_data(edge[0],
                                                 edge[1])["object"]

            self.display_message(gp_Pnt((start.X() + 2 * end.X()) / 3,
                                        (start.Y() + 2 * end.Y()) / 3,
                                        (start.Z() + 2 * end.Z()) / 3),
                                 text_to_write=edge_constraint.__class__.__name__,
                                 height=13,
                                 message_color=(0, 0, 0))  # black
        self.viewer_display.FitAll()


@memoize
def _centre_of_mass(shape):
    r"""
    
    Parameters
    ----------
    shape : OCC Shape

    Returns
    -------
    gp_Pnt

    """
    from OCC.Core.BRepGProp import brepgprop_VolumeProperties
    from OCC.Core.GProp import GProp_GProps
    g = GProp_GProps()
    brepgprop_VolumeProperties(shape, g)
    return g.CentreOfMass()


def _characteristic_dimension(shape):
    from aocutils.analyze.bounds import BoundingBox
    bb = BoundingBox(shape)
    return (bb.x_span + bb.y_span + bb.z_span) / 3.

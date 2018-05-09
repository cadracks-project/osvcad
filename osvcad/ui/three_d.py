# coding: utf-8

r"""3D visualization of geometry"""

from __future__ import division

import imp
from os.path import isdir, splitext
from random import randint
import logging
import json
import math

import wx
from OCC.Core.gp import gp_Pnt, gp_Vec

from corelib.core.python_ import is_valid_python
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ
from aocutils.analyze.bounds import BoundingBox
from aocutils.brep.edge_make import edge
from aocxchange.step import StepImporter
from aocxchange.iges import IgesImporter
from aocxchange.stl import StlImporter

logger = logging.getLogger(__name__)


class ThreeDPanel(Wx3dViewer):
    r"""Panel containing topology information about the loaded shape"""
    def __init__(self,
                 parent,
                 model,
                 viewer_background_color=(50., 50., 50.),
                 object_transparency=0.2, text_height=20,
                 text_colour=(0., 0., 0.)):
        super(ThreeDPanel, self).__init__(parent=parent,
                                          viewer_background_color=viewer_background_color)
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
                    has_part = hasattr(module_, "part")
                    has_assembly = hasattr(module_, "assembly")
                    has_anchors = hasattr(module_, "anchors")

                    self.erase_all()

                    if has_assembly is True:
                        logger.info("%s has assembly" % sel)
                        try:
                            self.display_assembly(module_.assembly)
                        except KeyError as ke:
                            self.erase_all()
                            logger.exception(ke)
                    else:
                        if has_part is True:
                            logger.info("%s has part" % sel)
                            if has_anchors:
                                p = Part.from_py_script(sel)
                                self.display_part(p, transparency=0.3)
                            else:
                                self.display_part(module_.part)
                        else:
                            self.erase_all()
                            logger.warning("Nothing to display")
                else:  # the file is not a valid Python file
                    logger.warning("Not a valid python file")
                    self.erase_all()

            elif ext in [".step", ".stp"]:
                self.erase_all()
                with wx.BusyInfo("Loading STEP ...") as _:
                    shapes = StepImporter(sel).shapes
                    logger.info("%i shapes in %s" % (len(shapes), sel))
                    for shape in shapes:
                        color_255 = (255, 255, 255)
                        self.display_shape(shape,
                                           color_=colour_wx_to_occ(color_255),
                                           transparency=0.1)

            elif ext in [".iges", ".igs"]:
                self.erase_all()
                with wx.BusyInfo("Loading IGES ...") as _:
                    shapes = IgesImporter(sel).shapes
                    logger.info("%i shapes in %s" % (len(shapes), sel))
                    for shape in shapes:
                        color_255 = (51, 255, 255)
                        self.display_shape(shape,
                                           color_=colour_wx_to_occ(color_255),
                                           transparency=0.1)

            elif ext == ".stl":
                self.erase_all()
                with wx.BusyInfo("Loading STL ...") as _:
                    shape = StlImporter(sel).shape
                    color_255 = (0, 255, 0)
                    self.display_shape(shape,
                                       color_=colour_wx_to_occ(color_255),
                                       transparency=0.1)

            elif ext == ".json":  # parts library
                self.erase_all()

                with wx.BusyInfo("Loading parts library ...") as _:
                    with open(sel) as json_file:
                        json_file_content = json.load(json_file)
                        print(json_file_content["data"].keys())
                        # find the biggest bounding box
                        biggest_bb = [0, 0, 0]
                        # smallest_bb = [0, 0, 0]
                        for i, k in enumerate(json_file_content["data"].keys()):
                            library_part = Part.from_library_part(sel, k)
                            bb = BoundingBox(library_part.node_shape.shape)
                            if bb.x_span > biggest_bb[0]:
                                biggest_bb[0] = bb.x_span
                            # if bb.x_span < smallest_bb[0]:
                            #     smallest_bb[0] = bb.x_span
                            if bb.y_span > biggest_bb[1]:
                                biggest_bb[1] = bb.y_span
                            # if bb.y_span < smallest_bb[1]:
                            #     smallest_bb[1] = bb.y_span
                            if bb.z_span > biggest_bb[2]:
                                biggest_bb[2] = bb.z_span
                            # if bb.z_span < smallest_bb[2]:
                            #     smallest_bb[2] = bb.y_span
                        biggest_dimension = max(biggest_bb)
                        # smallest_dimension = min(smallest_bb)

                        nb_per_row = int(math.sqrt(len(json_file_content["data"].keys())))

                        for i, k in enumerate(json_file_content["data"].keys()):
                            library_part = Part.from_library_part(sel, k)
                            x_pos = biggest_dimension*2 * (i % nb_per_row)
                            y_pos = biggest_dimension*2 * (i // nb_per_row)
                            library_part = library_part.translate((x_pos, y_pos, 0))
                            self.display_part(library_part, transparency=0.3)
                            self.display_message(gp_Pnt(x_pos + biggest_dimension / 5, y_pos + biggest_dimension / 5, 0),
                                                 k,
                                                 message_color=(1, 1, 1),
                                                 height=10)
            elif ext == ".stepzip":
                self.erase_all()
                with wx.BusyInfo("Loading STEPZIP ...") as _:
                    self.display_part(Part.from_stepzip(sel), transparency=0.3)
            elif ext == ".anchors":
                self.erase_all()
            else:
                logger.error("File has an extension %s that is not "
                             "handled by the 3D panel" % ext)
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
        if color_255 is None:
            # color_255 = (randint(0, 255), randint(0, 255), randint(0, 255))

            # by default, always use the same color to view a part
            color_255 = (102, 0, 102)

        for k, _ in part.anchors.items():
            vec_direction = gp_Vec(*part.anchors[k]["direction"])
            vec_direction.Multiply(100. / vec_direction.Magnitude())

            to_arrow_cone_start = gp_Vec(vec_direction.X(), vec_direction.Y(), vec_direction.Z())
            to_arrow_cone_start.Multiply(4./5.)

            arrow_cone = gp_Vec(vec_direction.X(), vec_direction.Y(), vec_direction.Z())
            arrow_cone.Multiply(1./5.)

            edge_start = gp_Pnt(*part.anchors[k]["position"])
            edge_end = edge_start.Translated(vec_direction)

            # Display the line in yellow
            self.display_shape(edge(edge_start, edge_end),
                               color_=colour_wx_to_occ((255, 255, 51)))

            self.display_vector(
                arrow_cone,
                gp_Pnt(*part.anchors[k]["position"]).Translated(to_arrow_cone_start))
            self.display_message(gp_Pnt(*part.anchors[k]["position"]),
                                 k,
                                 height=20,
                                 message_color=(0, 0, 0))
        self.display_shape(part.node_shape.shape,
                           color_=colour_wx_to_occ(color_255),
                           transparency=transparency)

    def display_assembly(self, assembly, transparency=0.):
        r"""Display an assembly of parts and assemblies

        Parameters
        ----------
        assembly : AssemblyGeometryNode
        transparency : float from 0 to 1

        """
        assembly.build()

        for node in assembly.nodes():
            # for k, v in node.anchors.items():
            #     frame.p.display_vector(gp_Vec(*node.anchors[k]["direction"]),
            #                            gp_Pnt(*node.anchors[k]["position"]))
            self.display_shape(node.node_shape.shape,
                                            color_=colour_wx_to_occ(
                                                (randint(0, 255),
                                                 randint(0, 255),
                                                 randint(0, 255))),
                                            transparency=transparency)

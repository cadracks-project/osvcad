# coding: utf-8

r"""3D visualization of geometry"""

from __future__ import division

import wx

from random import randint

from corelib.core.python_ import is_valid_python
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ


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
        print("Selection changed")
        from os.path import isdir
        import imp
        if not isdir(self.model.selected):
            with open(self.model.selected) as f:
                content = f.read()
                if is_valid_python(content):
                    module = imp.load_source("selected", self.model.selected)
                    self.erase_all()
                    try:
                        self.display_assembly(module.assembly)
                    except AttributeError:
                        try:
                            self.display_part(module.part)
                        except AttributeError:
                            print("Nothing to display")

        else:
            pass

        self.Layout()

        print("code change detected in 3D panel")

    def display_part(self, part, color_255=None, transparency=0.):
        r"""Display a single Part (shape + anchors)

        Parameters
        ----------
        part : PartGeometryNode
        color_255 : tuple of integers from 0 to 255
        transparency : float from 0 to 1

        """
        if color_255 is None:
            color_255 = (randint(0, 255), randint(0, 255), randint(0, 255))
        for k, _ in part.anchors.items():
            self.display_vector(
                gp_Vec(*part.anchors[k]["direction"]),
                gp_Pnt(*part.anchors[k]["position"]))
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

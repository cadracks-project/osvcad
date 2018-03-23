#!/usr/bin/env python
# coding: utf-8

r"""3D visualization of geometry"""

from osvcad.ui.wx_viewer import Wx3dViewer, colour_wx_to_occ


class ThreeDPanel(Wx3dViewer):
    r"""Panel containing topology information about the loaded shape"""
    def __init__(self,
                 parent,
                 model,
                 viewer_background_color=(50., 50., 50.),
                 object_transparency=0.2,
                 text_height=20,
                 text_colour=(0., 0., 0.)):
        super(ThreeDPanel, self).__init__(parent=parent,
                                          viewer_background_color=viewer_background_color)
        self.model = model
        self.model.observe("assembly_changed", self.on_model_change)

        self.viewer_display.View.SetBackgroundColor(colour_wx_to_occ(viewer_background_color))

        self.objects_transparency = object_transparency
        self.text_height = text_height
        self.text_colour = text_colour

    def on_model_change(self, change):
        """Callback function for listener"""

        self.erase_all()

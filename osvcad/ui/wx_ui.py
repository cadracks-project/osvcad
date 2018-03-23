#!/usr/bin/env python
# coding: utf-8

r"""Osvcad UI"""

import wx
import wx.aui
import wx.lib.agw.aui

from osvcad.ui.three_d import ThreeDPanel
from osvcad.ui.graph import GraphPanel
from osvcad.ui.shelf import ShelfPanel
from osvcad.ui.model import Model


class OsvcadUiFrame(wx.Frame):
    PANE_SHELF_NAME = "Shelf"
    PANE_3D_NAME = "3D"
    PANE_GRAPH_NAME = "Graph"

    def __init__(self, parent, model, frame_maximize=True):
        wx.Frame.__init__(self, parent, -1, "osvcad",
                          style=wx.DEFAULT_FRAME_STYLE,
                          size=(640, 480))

        self._model = model

        self.three_d_panel = ThreeDPanel(self, model)
        self.shelf_panel = ShelfPanel(self, model)
        self.graph_panel = GraphPanel(self, model)

        # AUI manager
        self._mgr = wx.lib.agw.aui.AuiManager()
        self._mgr.SetManagedWindow(self)  # notify AUI which frame to use

        self._mgr.AddPane(self.shelf_panel, wx.lib.agw.aui.AuiPaneInfo().Left().
                          Name(OsvcadUiFrame.PANE_SHELF_NAME).Caption("Shelf").
                          MinSize(wx.Size(200, 200)).MaximizeButton(True))
        self._mgr.AddPane(self.three_d_panel, wx.lib.agw.aui.AuiPaneInfo().CenterPane())
        self._mgr.AddPane(self.graph_panel, wx.lib.agw.aui.AuiPaneInfo().Right().
                          Name(OsvcadUiFrame.PANE_GRAPH_NAME).Caption("Graph").
                          MinSize(wx.Size(100, 100)).MaximizeButton(True))

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        # Show and maximize the frame
        self.Show(True)
        if frame_maximize is True:
            self.Maximize(True)  # Use the full screen
        else:
            self.CenterOnScreen()

if __name__ == "__main__":
    app = wx.App()
    model = Model()
    frame = OsvcadUiFrame(parent=None, model=model)
    frame.Show(True)
    app.SetTopWindow(frame)
    app.MainLoop()
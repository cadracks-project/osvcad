#!/usr/bin/env python
# coding: utf-8

r"""Viewer for the test_xcaf_read.py example
"""

import wx
import os

from OCC.Display.wxDisplay import wxViewer3d
from OCC.Core import TPrsStd, XCAFPrs

os.environ['CSF_GraphicShr'] = "/usr/local/lib/libTKOpenGl.so"

app = wx.App()


def view(*shapeList):
    frame = wx.Frame(None, -1, "OCC frame", size=(600, 400))
    v = wxViewer3d(frame)
    v.InitDriver()
    canvas = v._display
    frame.Show()
    wx.SafeYield()

    canvas.Init3dViewer()
    # viewer = canvas._3dDisplay

    for shape in shapeList:
        canvas.DisplayShape(shape)

    app.MainLoop()


def viewXDE(doc, aLabel, shape):
    frame = wx.Frame(None, -1, "OCC frame", size=(600, 400))

    canvas = wxViewer3d(frame)
    frame.Show()
    wx.SafeYield()

    canvas.InitDriver()
    viewer = canvas._display
    context = viewer.Context
    aisView = TPrsStd.TPrsStd_AISViewer().New(aLabel,
                                              viewer.Viewer.GetHandle())
    print(aisView)
    # aisView.SetInteractiveContext(context.GetHandle())

    # viewer.DisplayShape(shape)

    aisPres = TPrsStd.TPrsStd_AISPresentation().Set(aLabel,
                                                    XCAFPrs.XCAFPrs_Driver.GetID())
    aisPres.GetObject().Display(True)
    context.UpdateCurrentViewer()

    app.MainLoop()


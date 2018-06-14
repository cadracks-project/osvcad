#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import os

from OCC.Core.TCollection import *

from OCC.Core import XCAFApp, TDocStd, TCollection, XCAFDoc, BRepPrimAPI, \
    Quantity, TopLoc, gp, TPrsStd, XCAFPrs
from OCC.Display.SimpleGui import *
from OCC.Core.STEPCAFControl import *
from OCC.Core.XSControl import *
from OCC.Core.STEPControl import *

display, start_display, add_menu, add_function_to_menu = init_display()


def step_export_layers_and_colors(event=None):
    r"""
    demo showing how to export step files with layers & colors.
    adapted from Bryan's names_shape_demo
    """

    # Create the TDocStd document
    h_doc = TDocStd.Handle_TDocStd_Document()
    print("Empty Doc?", h_doc.IsNull())

    # Create the application
    # app = XCAFApp.GetApplication().GetObject()
    app = XCAFApp.XCAFApp_Application.GetApplication().GetObject()
    app.NewDocument(TCollection.TCollection_ExtendedString("MDTV-CAF"), h_doc)

    # Get root assembly
    doc = h_doc.GetObject()
    h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())
    l_colors = XCAFDoc.XCAFDoc_DocumentTool().ColorTool(doc.Main())
    l_layers = XCAFDoc.XCAFDoc_DocumentTool().LayerTool(doc.Main())

    shape_tool = h_shape_tool.GetObject()
    colors = l_colors.GetObject()
    layers = l_layers.GetObject()

    # this is the "root" label for the assembly
    top_label = shape_tool.NewShape()

    # not yet, 'cos it's empty)
    print("Is Assembly", shape_tool.IsAssembly(top_label))

    # Add some shapes
    box = BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()
    box_label = shape_tool.AddShape(box, False)

    cyl = BRepPrimAPI.BRepPrimAPI_MakeCylinder(25, 50).Shape()
    cyl_label = shape_tool.AddShape(cyl, False)

    # Add components as references to our shape
    tr = gp.gp_Trsf()
    tr.SetTranslation(gp.gp_Vec(100, 100, 100))
    loc = TopLoc.TopLoc_Location(tr)
    box_comp1 = shape_tool.AddComponent(top_label, box_label, loc)

    tr = gp.gp_Trsf()
    tr.SetTranslation(gp.gp_Vec(200, 200, 200))
    loc = TopLoc.TopLoc_Location(tr)
    box_comp2 = shape_tool.AddComponent(top_label, box_label, loc)

    tr = gp.gp_Trsf()
    tr.SetTranslation(gp.gp_Vec(150, 200, 100))
    loc = TopLoc.TopLoc_Location(tr)
    cyl_comp = shape_tool.AddComponent(top_label, cyl_label, loc)

    print("Is Assembly", shape_tool.IsAssembly(top_label))  # it is now...

    # Add some colors
    red = Quantity.Quantity_Color(Quantity.Quantity_NOC_RED)
    green = Quantity.Quantity_Color(Quantity.Quantity_NOC_GREEN)
    colors.SetColor(cyl_comp, red, XCAFDoc.XCAFDoc_ColorGen)
    colors.SetColor(box_comp2, green, XCAFDoc.XCAFDoc_ColorGen)

    # Set the box on the 'box' layer, the cylinder on the 'cylinder' layer
    layers.SetLayer(box_comp1, TCollection_ExtendedString('BOX'))
    layers.SetLayer(cyl_comp, TCollection_ExtendedString('CYLINDER'))

    # Set up AIS Presentation stuff
    # (I don't understand this, but it kinda works)
    aisView = TPrsStd.TPrsStd_AISViewer().New(top_label,
                                              display.Context.GetHandle())
    aisPres = TPrsStd.TPrsStd_AISPresentation().Set(top_label,
                                                    XCAFPrs.XCAFPrs_Driver.GetID())
    aisPres.GetObject().Display(True)
    display.FitAll()

    # write the stuff to STEP, with layers & colors
    work_session = XSControl_WorkSession()
    writer = STEPCAFControl_Writer(work_session.GetHandle(), False)
    writer.Transfer(h_doc, STEPControl_AsIs)
    pth = '.'
    print('writing STEP file')
    status = writer.Write(os.path.join(pth, 'step_layers_colors.step'))
    print('status:', status)


def exit(event=None):
    sys.exit()

if __name__ == '__main__':
    add_menu('step ocaf export')
    add_function_to_menu('step ocaf export', step_export_layers_and_colors)
    add_function_to_menu('step ocaf export', exit)
    start_display()

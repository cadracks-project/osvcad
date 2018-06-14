#!/usr/bin/env python
# coding: utf-8

r"""XDE test"""

from OCC.Core import XCAFApp, STEPCAFControl, TDocStd, TCollection,\
        XCAFDoc, BRepPrimAPI, Quantity, STEPControl,\
        TopLoc, gp, TDF, TColStd

# Create the TDocStd document
h_doc = TDocStd.Handle_TDocStd_Document()
print("Empty Doc?", h_doc.IsNull())

# Create the application
app = XCAFApp.XCAFApp_Application_GetApplication().GetObject()
app.NewDocument(TCollection.TCollection_ExtendedString("MDTV-CAF"), h_doc)

# Get root assembly
doc = h_doc.GetObject()
h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())
l_Colors = XCAFDoc.XCAFDoc_DocumentTool().ColorTool(doc.Main())

shape_tool = h_shape_tool.GetObject()
colors = l_Colors.GetObject()

top_label = shape_tool.NewShape()  # this is the "root" label for the assembly

# not an assembly yet, 'cos it's empty
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

# it is now...
print("Is Assembly", shape_tool.IsAssembly(top_label))

# Add some colors
red = Quantity.Quantity_Color(Quantity.Quantity_NOC_RED)
green = Quantity.Quantity_Color(Quantity.Quantity_NOC_GREEN)
colors.SetColor(cyl_comp, red, XCAFDoc.XCAFDoc_ColorGen)
colors.SetColor(box_comp2, green, XCAFDoc.XCAFDoc_ColorGen)

tag_tool = TDF.TDF_Tool()
tagList = TColStd.TColStd_ListOfInteger()
tag_tool.TagList(cyl_comp, tagList)
iterTagList = TColStd.TColStd_ListIteratorOfListOfInteger(tagList)
while iterTagList.More():
    v = iterTagList.GetValue()
    iterTagList.Next()

asc = TCollection.TCollection_AsciiString()
tag_tool.Entry(cyl_comp, asc)
print(asc.ToCString())

# for a in dir(v):
#     print(a)

mode = STEPControl.STEPControl_AsIs
writer = STEPCAFControl.STEPCAFControl_Writer()
writer.Transfer(h_doc, mode)
writer.Write("XDE_test.step")


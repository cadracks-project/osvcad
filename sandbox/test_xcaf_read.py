#!/usr/bin/env python
# coding: utf-8

r"""Read a STEP file create with XDE"""

from OCC.Core import XCAFApp, STEPCAFControl, TDocStd, TCollection,\
        XCAFDoc, TDF

from viewer import viewXDE

reader = STEPCAFControl.STEPCAFControl_Reader()

reader.ReadFile('XDE_test.step')

# Create the TDocStd document
h_doc = TDocStd.Handle_TDocStd_Document()
print(h_doc.IsNull())

# Create the application
app = XCAFApp.XCAFApp_Application.GetApplication().GetObject()
app.NewDocument(TCollection.TCollection_ExtendedString("MDTV-CAF"), h_doc)

# Transfer
print(h_doc.IsNull())
if not reader.Transfer(h_doc):
    print("Error")

# Get root assembly
doc = h_doc.GetObject()

h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())
shape_tool = h_shape_tool.GetObject()

# get the top level shapes
l_LabelShapes = TDF.TDF_LabelSequence()
shape_tool.GetShapes(l_LabelShapes)

count = l_LabelShapes.Length()

root_label = l_LabelShapes.Value(1)

shape = shape_tool.GetShape(root_label)
viewXDE(doc, root_label, shape)

#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

from OCC.Core import BRepPrimAPI, TNaming, TDocStd, AppStd, TCollection, TDF, \
    AIS, XCAFDoc
from OCC.Display.SimpleGui import *

from aocutils.topology import Topo


display, start_display, add_menu, add_function_to_menu = init_display()


app = AppStd.AppStd_Application()

h_doc = TDocStd.Handle_TDocStd_Document()
schema = TCollection.TCollection_ExtendedString("MyFormat")
app.NewDocument(schema, h_doc)

doc = h_doc.GetObject()

root = doc.Main()

ts = TDF.TDF_TagSource()

box = BRepPrimAPI.BRepPrimAPI_MakeBox(20.0, 20.0, 20.0).Shape()

h_shape_tool = XCAFDoc.XCAFDoc_DocumentTool().ShapeTool(doc.Main())
shape_tool = h_shape_tool.GetObject()

# box_label = ts.NewChild(root)
box_label = shape_tool.AddShape(box, False)
ns_builder = TNaming.TNaming_Builder(box_label)
ns_builder.Generated(box)

topo = Topo(box, return_iter=True)

# Name all the subshape we *might* want to refer to later
for edge in list(topo.edges):
    # sub_label = ts.NewChild(box_label)
    sub_label = shape_tool.AddShape(edge, False)
    ns_builder = TNaming.TNaming_Builder(sub_label)
    ns_builder.Generated(edge)

# Find and Name an edge
an_edge = topo.edges.__next__()

# s_label = ts.NewChild(root)
s_label = shape_tool.AddShape(an_edge, False)
selector = TNaming.TNaming_Selector(s_label)
ret = selector.Select(an_edge, box)
print("selected", ret)

# now modify the box
box2 = BRepPrimAPI.BRepPrimAPI_MakeBox(5.0, 10.0, 15.0).Shape()

# Update the naming with the new box shape
ns_builder = TNaming.TNaming_Builder(box_label)
ns_builder.Generated(box2)

h_a = TNaming.Handle_TNaming_NamedShape()
ns_id = TNaming.TNaming_NamedShape().ID()
for i, edge in enumerate(Topo(box2).edges):
    sub_label = box_label.FindChild(i+1)
    ns_builder = TNaming.TNaming_Builder(sub_label)
    ns_builder.Generated(edge)

# Need to build a map covering all the OCAF nodes
# which might contain relevant shapes
aMap = TDF.TDF_LabelMap()
aMap.Add(box_label)
itr = TDF.TDF_ChildIterator(box_label, True)
while itr.More():
    sub_label = itr.Value()
    aMap.Add(sub_label)
    itr.Next()

# Solve for the selected edge
ok = selector.Solve(aMap)
print("solve OK", ok)

# Extract the selected edge
nt = TNaming.TNaming_Tool()
shape = nt.CurrentShape(selector.NamedShape())

# display them together
display.DisplayShape(shape)

# Make the box transparent, so it's easier to see the selected edge
ctx = display.Context
ais_shape = AIS.AIS_Shape(box2).GetHandle()
ctx.SetTransparency(ais_shape, 0.8, True)
ctx.Display(ais_shape)

start_display()


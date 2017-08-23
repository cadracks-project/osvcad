# coding: utf-8

r"""Create the assembly from serialized json file"""

from osvcad.nodes import AssemblyGeometryNode

A = AssemblyGeometryNode.read_json("sample.json")
print(type(A))

print(A.number_of_nodes())
print(A.number_of_edges())

A.display_3d_ccad()

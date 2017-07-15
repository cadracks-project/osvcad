# coding: utf-8

r"""Example of direct construction"""

from osvcad.nodes import GeometryNodePyScript, GeometryNodeStep, \
    GeometryNodeLibraryPart, Assembly
from osvcad.edges import ConstraintCoaxial, ConstraintAbsolutePositioning

# n1 = GeometryNodeStep(step_file_path="step/sphere.stp", anchors=None)
n1 = GeometryNodeStep(step_file_path="step/plate_with_holes.step", anchors=None)
n2 = GeometryNodePyScript(py_script_path="py_scripts/plate_with_holes.py")
n3 = GeometryNodeLibraryPart(library_file_path="libraries/ISO4014_library.json",
                             part_id="ISO4014_M2_grade_Bx21")

A = Assembly()

# A.add_node(n1)
# A.add_node(n2)

A.add_edge(n2, n1, object=ConstraintAbsolutePositioning(t=(0, 0, 20),
                                                        r=(0, 0, 0)))

A.add_edge(n2, n3, object=ConstraintAbsolutePositioning(t=(50, 25, 0),
                                                        r=(0, 0, 0)))

print(A.number_of_nodes())
print(A.number_of_edges())

# A.show_plot()
# A.write_yaml("sample.yaml")
A.write_json("sample.json")

A.display_3d()

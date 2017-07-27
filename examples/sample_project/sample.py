# coding: utf-8

r"""Example of direct construction"""

from osvcad.nodes import GeometryNodePyScript, GeometryNodeStep, \
    GeometryNodeLibraryPart, Assembly
from osvcad.edges import ConstraintAnchor

# n1 = GeometryNodeStep(step_file_path="step/sphere.stp", anchors=None)
# n1 = GeometryNodeStep(step_file_path="step/plate_with_holes.step", anchors=None)

plate_gn = GeometryNodePyScript(py_script_path="py_scripts/plate_with_holes.py")

print("Plate gn : %s" % plate_gn)

# n3 = GeometryNodeLibraryPart(library_file_path="libraries/ISO4014_library.json",
#                              part_id="ISO4014_M2_grade_Bx21")
# n4 = GeometryNodeLibraryPart(library_file_path="libraries/ISO4014_library.json",
#                              part_id="ISO4014_M2_grade_Bx21")

screws = [GeometryNodeLibraryPart(
    library_file_path="libraries/ISO4014_library.json",
    part_id="ISO4014_M2_grade_Bx21") for _ in range(4)]

nuts = [GeometryNodeLibraryPart(
    library_file_path="libraries/ISO4032_library.json",
    part_id="ISO4032_Nut_M2.0") for _ in range(4)]


A = Assembly(root=plate_gn)

# A.add_node(n1)
# A.add_node(n2)

# A.add_edge(n2, n1, object=ConstraintAbsolutePositioning(t=(0, 0, 20),
#                                                         r=(0, 0, 0)))
#
# A.add_edge(n2, n3, object=ConstraintAbsolutePositioning(t=(50, 25, 0),
#                                                         r=(0, 0, 0)))

for i, screw in enumerate(screws, 1):
    A.add_edge(plate_gn, screw, object=ConstraintAnchor(anchor_name_master=str(i),
                                                     anchor_name_slave=1,
                                                     distance=0, angle=0))

for i, (screw, nut) in enumerate(zip(screws, nuts), 1):
    A.add_edge(screw, nut, object=ConstraintAnchor(anchor_name_master=1,
                                                     anchor_name_slave=1,
                                                     distance=-5-1.6, angle=0))
#
# A.add_edge(plate_gn, n3, object=ConstraintAnchor(anchor_name_master="1", anchor_name_slave=1, distance=0, angle=0))
# A.add_edge(plate_gn, n4, object=ConstraintAnchor(anchor_name_master="2", anchor_name_slave=1, distance=0, angle=0))


print(A.number_of_nodes())
print(A.number_of_edges())

# A.show_plot()
# A.write_yaml("sample.yaml")

# A.write_json("sample.json")
# A.display_3d()

A.display_3d()

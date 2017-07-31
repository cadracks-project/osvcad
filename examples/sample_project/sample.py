# coding: utf-8

r"""Example of direct construction"""

from osvcad.nodes import GeometryNode, Assembly
from osvcad.edges import ConstraintAnchor

plate_gn = GeometryNode.from_py_script(py_script_path="py_scripts/plate_with_holes.py")

print("Plate gn : %s" % plate_gn)

screws = [GeometryNode.from_library_part(
    library_file_path="libraries/ISO4014_library.json",
    part_id="ISO4014_M2_grade_Bx21") for _ in range(4)]

nuts = [GeometryNode.from_library_part(
    library_file_path="libraries/ISO4032_library.json",
    part_id="ISO4032_Nut_M2.0") for _ in range(4)]


A = Assembly(root=plate_gn)

for i, screw in enumerate(screws, 1):
    A.add_edge(plate_gn,
               screw,
               object=ConstraintAnchor(anchor_name_master=str(i),
                                       anchor_name_slave=1,
                                       distance=0,
                                       angle=0))

for i, (screw, nut) in enumerate(zip(screws, nuts), 1):
    A.add_edge(screw,
               nut, object=ConstraintAnchor(anchor_name_master=1,
                                            anchor_name_slave=1,
                                            distance=-5-1.6,
                                            angle=0))

print(A.number_of_nodes())
print(A.number_of_edges())

#
# A.write_yaml("sample.yaml")

# A.write_json("sample.json")

A.display_3d()

A.show_plot()

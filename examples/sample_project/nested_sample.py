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
project = Assembly(root=A)

for i in range(4):
    bolt = Assembly(root=screws[i])
    bolt.add_edge(screws[i],
                  nuts[i],
                  object=ConstraintAnchor(anchor_name_master=1,
                                          anchor_name_slave=1,
                                          distance=-5-1.6,
                                          angle=0))

    project.add_edge(A, bolt, object=ConstraintAnchor(anchor_name_master=str(hash(plate_gn)) + "/%i" % (i + 1),
                                                      anchor_name_slave=str(hash(screws[i])) + "/1",
                                                      distance=0,
                                                      angle=0))

#
# A.write_yaml("sample.yaml")

# project.write_json("project.json")

project.display_3d_ccad()

project.show_plot()

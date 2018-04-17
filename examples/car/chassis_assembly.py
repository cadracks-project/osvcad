# coding: utf-8

r"""Example of a car model"""

from car_assemblies import make_chassis_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    chassis_assembly_ = make_chassis_assembly()
    for k, v in chassis_assembly_.anchors.items():
        print("%s : %s" % (k, v))

    view_assembly(chassis_assembly_)
    view_assembly_graph(chassis_assembly_)

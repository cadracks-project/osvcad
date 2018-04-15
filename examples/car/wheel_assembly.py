# coding: utf-8

r"""Tabby wheel assembly"""

import logging

from car_assemblies import make_wheel_assembly

from osvcad.view import view_assembly, view_assembly_graph

if __name__ == "__main__":
    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        _ = [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.INFO,
                        format='%(relativeCreated)6d :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    wheel_assembly = make_wheel_assembly()
    # wheel_assembly.display_3d()
    wheel_assembly.display_3d()
    wheel_assembly.show_plot()
    view_assembly(wheel_assembly)
    view_assembly_graph(wheel_assembly)

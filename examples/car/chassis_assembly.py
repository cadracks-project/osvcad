# coding: utf-8

r"""Example of a car model"""

import logging

from car_assemblies import make_chassis_assembly

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

    chassis_assembly_ = make_chassis_assembly()
    for k, v in chassis_assembly_.anchors.items():
        print("%s : %s" % (k, v))

    # chassis_assembly_.display_3d()
    chassis_assembly_.display_3d()
    chassis_assembly_.show_plot()

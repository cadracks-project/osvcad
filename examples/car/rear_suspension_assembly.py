# coding: utf-8

r"""Tabby rear suspension assembly"""

import logging

from car_assemblies import make_rear_suspension_assembly

if __name__ == "__main__":
    # Workaround badly formatted log messages
    # Probably originating from aocutils (likely cause: call to logger.* before
    # call to basicConfig)
    root = logging.getLogger()
    if root.handlers:
        [root.removeHandler(handler) for handler in root.handlers]

    logging.basicConfig(level=logging.INFO,
                        format='%(relativeCreated)6d :: %(levelname)6s :: '
                               '%(module)20s :: %(lineno)3d :: %(message)s')

    rear_suspension_assembly_ = make_rear_suspension_assembly()
    # rear_suspension_assembly_.display_3d()
    rear_suspension_assembly_.display_3d_alternative()
    rear_suspension_assembly_.show_plot()

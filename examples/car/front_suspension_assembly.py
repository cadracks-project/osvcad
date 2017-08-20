# coding: utf-8

r"""Tabby rear suspension assembly"""

import logging

from car_assemblies import make_front_suspension_assembly

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

    front_suspension_assembly_ = make_front_suspension_assembly()
    # front_suspension_assembly_.display_3d()
    front_suspension_assembly_.display_3d_alternative()
    front_suspension_assembly_.show_plot()

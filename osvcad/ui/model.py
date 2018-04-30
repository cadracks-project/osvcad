# coding: utf-8

r"""Model of the waterline app"""

import logging

from atom.api import Atom
from atom.scalars import Str
logger = logging.getLogger(__name__)


class Model(Atom):
    r"""Model for the waterline app"""
    code = Str()

    def set_code(self, code):
        r"""Set the code

        Parameters
        ----------
        code : str

        """
        logger.debug("Setting the code")
        self.code = code
        logger.debug("Notify that code_changed")
        self.notify("code_changed", None)

# coding: utf-8

r"""Model of the waterline app"""

import logging

from atom.api import Atom
from atom.scalars import Str

logger = logging.getLogger(__name__)


class Model(Atom):
    r"""Model for the waterline app"""
    root_folder = Str()
    selected = Str()
    code = Str()

    def set_root_folder(self, root_folder):
        r"""Set the root folder
        
        Parameters
        ----------
        root_folder : str

        """
        logger.debug("Setting the root folder")
        self.root_folder = root_folder
        logger.debug("Notify that root folder changed")
        self.notify("root_folder_changed", None)

    def set_selected(self, selected):
        logger.debug("Setting the selected item")
        self.selected = selected
        logger.debug("Notify that selected item changed")
        self.notify("selected_changed", None)

    # def set_code(self, code):
    #     r"""Set the code
    #
    #     Parameters
    #     ----------
    #     code : str
    #
    #     """
    #     logger.debug("Setting the code")
    #     self.code = code
    #     logger.debug("Notify that code_changed")
    #     self.notify("code_changed", None)

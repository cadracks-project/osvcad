# coding: utf-8

r"""Shelf panel"""

import wx


class ShelfPanel(wx.Panel):
    r"""Panel containing potential parts for the project"""
    def __init__(self,
                 parent,
                 model):
        super(ShelfPanel, self).__init__(parent=parent)
        self.model = model
        self.model.observe("assembly_changed", self.on_model_change)

    def on_model_change(self, change):
        """Callback function for listener"""
        pass

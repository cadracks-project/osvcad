# coding: utf-8

r"""Widgets used in various places of the ui"""

import os.path

import wx
import wx.lib.buttons


class OkBtn(wx.lib.buttons.GenBitmapTextButton):
    r"""A reusable ok button with a bitmap"""
    def __init__(self, parent, label="Ok"):
        img = wx.Bitmap(os.path.join(os.path.dirname(__file__),
                                     "./icons/dialog-ok-apply.png"))
        super(OkBtn, self).__init__(parent, wx.ID_OK, img, label)


class CloseBtn(wx.lib.buttons.GenBitmapTextButton):
    r"""A reusable close button with a bitmap"""
    def __init__(self, parent, label="Close"):
        img = wx.Bitmap(os.path.join(os.path.dirname(__file__),
                                     "./icons/dialog-cancel.png"))
        super(CloseBtn, self).__init__(parent, wx.ID_CANCEL, img, label=label)

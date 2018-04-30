# coding: utf-8

r"""Graph visualization component"""

import wx

import matplotlib
# The following line solves the
# Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
# bug on linux 64 (and maybe elsewhere)
matplotlib.use('wx')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt


class GraphPanel(wx.Panel):
    r"""wx Panel embedding a Matplotlib plot

    Parameters
    ----------
    parent : wx parent
    model : Model

    """
    def __init__(self, parent, model):
        super(GraphPanel, self).__init__(parent, wx.ID_ANY)
        self.model = model

        self.figure = plt.figure()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = FigureCanvas(self, -1, self.figure)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
        self.SetSizer(sizer)

    def plot(self):
        r"""Plot values with an associated color and an associated name"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        self.canvas.draw()

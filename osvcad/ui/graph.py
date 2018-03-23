#!/usr/bin/env python
# coding: utf-8

r"""Assembly graph display"""

import wx

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt


class GraphPanel(wx.Panel):
    r"""wx Panel embedding a Matplotlib plot

    Parameters
    ----------
    parent : wx parent

    """
    def __init__(self, parent, model):
        super(GraphPanel, self).__init__(parent, wx.ID_ANY)

        self.model = model

        self.figure = plt.figure()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.canvas = FigureCanvas(self, -1, self.figure)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.toolbar = NavigationToolbar(self.canvas)

        # Show the toolbar at the bottom of the graphs, so that it is
        # possible to use the standard toolbar
        # functionalities and to export the graph
        # self.toolbar.Hide()
        sizer.Add(self.toolbar)
        self.toolbar.Show()

        self.SetSizer(sizer)

    def plot(self,
             xs,
             y_series,
             color_series,
             name_series,
             x_label="x",
             y_label="y"):
        r"""Plot values with an associated color and an associated name

        Parameters
        ----------
        xs : list x values
            List of heel angles or list of trim angles
        y_series : list of list of y values
            List of list of measured values (e.g. tm, trm, Cp)
        color_series : list of colors
            List of colors in the same order a y_series,
            i.e. the first list of y_series is plotted with the first
            color of color_series
        name_series : list of names
            List of names in the same order a y_series,
            i.e. the first list of y_series is plotted with the first
            name of name_series
        x_label : str
        y_label : str

        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        # ax.hold(False)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        #
        for y_serie, color, name in zip(y_series, color_series, name_series):
            ax.plot(xs, y_serie, marker='+', color=color, label=name)

        legend = ax.legend(loc='upper left', shadow=True)
        if legend is not None:
            for label in legend.get_texts():
                label.set_fontsize('small')
            legend.draggable()

        self.canvas.draw()

    def plot_curve_of_areas(self,
                            x_series,
                            areas_series,
                            color_series,
                            linestyle_series,
                            name_series,
                            x_label="x",
                            y_label="area"):
        r"""Plot the curves of areas"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        for x_serie, area_serie, color, linestyle, name in zip(x_series,
                                                               areas_series,
                                                               color_series,
                                                               linestyle_series,
                                                               name_series):
            ax.plot(x_serie,
                    area_serie,
                    marker="+",
                    color=color,
                    linestyle=linestyle,
                    label=name)
        legend = ax.legend(loc='upper right', shadow=True)

        if legend is not None:
            for label in legend.get_texts():
                label.set_fontsize('small')
            legend.draggable()

        self.canvas.draw()

# coding: utf-8

r"""Graph visualization component"""

from os.path import splitext, isdir
import logging
import imp

import wx
import networkx as nx

import matplotlib
# The following line solves the
# Process finished with exit code 139 (interrupted by signal 11: SIGSEGV)
# bug on linux 64 (and maybe elsewhere)
matplotlib.use('wx')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt

from corelib.core.python_ import is_valid_python

logger = logging.getLogger(__name__)


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

        self.model.observe("selected_changed", self.on_selected_change)

    def plot(self, assembly):
        r"""Plot values with an associated color and an associated name"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        val_map = {'A': 1.0,
                   'D': 0.5714285714285714,
                   'H': 0.0}

        values = [val_map.get(node, 0.25) for node in assembly.nodes()]

        # pos = nx.circular_layout(assembly)
        # pos = nx.circular_layout(assembly)
        # pos = nx.kamada_kawai_layout(assembly)
        # pos = nx.random_layout(assembly)
        # pos = nx.rescale_layout(assembly)
        # pos = nx.shell_layout(assembly)
        # pos = nx.spring_layout(assembly)
        # pos = nx.spectral_layout(assembly)
        pos = nx.fruchterman_reingold_layout(assembly)

        nx.draw_networkx_nodes(assembly,
                               pos,
                               cmap=plt.get_cmap('jet'),
                               node_color=values)
        nx.draw_networkx_edges(assembly,
                               pos,
                               edgelist=assembly.edges(),
                               edge_color='r',
                               arrows=True)
        nx.draw_networkx_labels(assembly, pos)
        nx.draw_networkx_edge_labels(assembly, pos)

        # plt.show()

        self.canvas.draw()

    def on_selected_change(self, change):
        """Callback function for listener"""

        logger.debug("Selection changed")

        sel = self.model.selected

        if not isdir(sel):
            # what extension ?
            ext = splitext(sel)[1].lower()

            logger.info("File extension : %s" % ext)

            if ext == ".py":
                with open(sel) as f:
                    content = f.read()

                if is_valid_python(content) is True:
                    with wx.BusyInfo("Loading Python defined geometry ...") as _:
                        module_ = imp.load_source(sel, sel)
                    # has_part = hasattr(module_, "part")
                    has_assembly = hasattr(module_, "assembly")
                    # has_anchors = hasattr(module_, "anchors")

                    self.figure.clear()

                    if has_assembly is True:
                        logger.info("%s has assembly" % sel)
                        try:
                            self.plot(module_.assembly)
                        except KeyError as ke:
                            self.figure.clear()
                            logger.exception(ke)
                    else:
                        self.figure.clear()
                        logger.warning("Nothing to display")
                else:  # the file is not a valid Python file
                    logger.warning("Not a valid python file")
                    self.figure.clear()

            elif ext in [".step", ".stp", ".iges", ".igs", ".stl", ".json",
                         ".stepzip", ".anchors"]:
                self.figure.clear()

            else:
                logger.error("File has an extension %s that is not "
                             "handled by the 3D panel" % ext)
                self.figure.clear()

        else:  # a directory is selected
            self.figure.clear()

        self.Layout()

        logger.debug("code change detected in 3D panel")

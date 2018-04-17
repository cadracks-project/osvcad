# coding: utf-8

r"""Visualization of Parts and Assemblies"""

from random import uniform, randint

import platform
import wx
import wx.aui
import wx.lib.agw.aui
import matplotlib.pyplot as plt
import networkx as nx

from OCC.Core.gp import gp_Pnt, gp_Vec
import ccad.display as cd
# from osvcad.ui.wx_viewer import Wx3dViewer, colour_wx_to_occ
from aocutils.display.wx_viewer import Wx3dViewer, colour_wx_to_occ

#
# class MyFrame(wx.Frame):
#     r"""Frame for testing"""
#
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1)
#         self.wx_3d_viewer = Wx3dViewer(self)
#         self.Show()


class MyFrame(wx.Frame):
    r"""Frame for testing"""

    def __init__(self):
        wx.Frame.__init__(self, None, -1)
        if platform.system() == "Linux":
            self.Show()

        self._mgr = wx.lib.agw.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        # wx.SafeYield()
        # # TODO : check if running on Linux
        # if wx.version().startswith("3.") or wx.version().startswith("4."):
        #     # issue with GetHandle on Linux for wx versions
        #     # >3 or 4. Window must be displayed before GetHandle is
        #     # called. For that, just wait for a few milliseconds/seconds
        #     # before calling InitDriver
        #     # a solution is given here
        #     # see https://github.com/cztomczak/cefpython/issues/349
        #     # but raises an issue with wxPython 4.x
        #     # finally, it seems that the sleep function does the job
        #     from time import sleep
        #     sleep(2)
        #     wx.SafeYield()
        self.wx_3d_viewer = Wx3dViewer(self, show_topology_menu=False)

        self._mgr.AddPane(self.wx_3d_viewer,
                          wx.lib.agw.aui.AuiPaneInfo().CenterPane())

        self._mgr.Update()

        self.wx_3d_viewer.Layout()

        # self.Show(True)
        # self.CenterOnScreen()


# parts


def view_part(part, color_255, transparency=0.):
    r"""Display the node in a 3D viewer

    Parameters
    ----------
    part : PartGeometryNode
    color_255 : Tuple[float, float, float]
        8-bit (0 - 255) color tuple
    transparency : float
        From 0. (not transparent) to 1 (fully transparent)

    """
    app = wx.App()
    frame = MyFrame()
    for k, _ in part.anchors.items():
        frame.wx_3d_viewer.display_vector(gp_Vec(*part.anchors[k]["direction"]),
                                          gp_Pnt(*part.anchors[k]["position"]))
        frame.wx_3d_viewer.display_shape(part.node_shape.node_shape,
                                         color_=colour_wx_to_occ(color_255),
                                         transparency=transparency)
    app.SetTopWindow(frame)
    app.MainLoop()

# assemblies


def view_assembly_graph(assembly):
    r"""Create a Matplotlib graph of the plot

    Parameters
    ----------
    assembly : AssemblyGeometryNode

    """
    val_map = {'A': 1.0,
               'D': 0.5714285714285714,
               'H': 0.0}

    values = [val_map.get(node, 0.25) for node in assembly.nodes()]

    pos = nx.circular_layout(assembly)
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
    plt.show()


def view_assembly_ccad(assembly):
    r"""Display the Assembly in a the ccad 3D viewer

    Parameters
    ----------
    assembly : AssemblyGeometryNode

    """
    v = cd.view()

    assembly.build()

    for node in assembly.nodes():
        v.display(node._node_shape,
                  color=(uniform(0, 1), uniform(0, 1), uniform(0, 1)),
                  transparency=0.)
    # v.display(assembly._node_shape,
    #           color=(uniform(0, 1), uniform(0, 1), uniform(0, 1)),
    #           transparency=0.)

    cd.start()


def view_assembly(assembly):
    r"""Display using osvcad's integrated wx viewer"""
    assembly.build()

    app = wx.App()
    frame = MyFrame()

    for node in assembly.nodes():
        # for k, v in node.anchors.items():
        #     frame.p.display_vector(gp_Vec(*node.anchors[k]["direction"]),
        #                            gp_Pnt(*node.anchors[k]["position"]))
        frame.wx_3d_viewer.display_shape(node.node_shape.shape,
                                         color_=colour_wx_to_occ((randint(0, 255), randint(0, 255), randint(0, 255))),
                                         transparency=0.)
    app.SetTopWindow(frame)
    app.MainLoop()

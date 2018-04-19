# coding: utf-8

r"""Visualization of Parts and Assemblies"""

from random import uniform, randint

import wx
import wx.aui
import wx.lib.agw.aui
import matplotlib.pyplot as plt
import networkx as nx

from OCC.Core.gp import gp_Pnt, gp_Vec
import ccad.display as cd
from aocutils.display.wx_viewer import Wx3dViewerFrame, colour_wx_to_occ


class OsvCadFrame(Wx3dViewerFrame):
    r"""Specialization of aocutil's Wx3dViewerFrame for OsvCad"""
    def __init__(self):
        Wx3dViewerFrame.__init__(self,
                                 title="OsvCad 3d viewer",
                                 welcome="Starting OsvCad 3d viewer ...")

    def display_part(self, part, color_255=None, transparency=0.):
        r"""Display a single Part (shape + anchors)

        Parameters
        ----------
        part : PartGeometryNode
        color_255 : tuple of integers from 0 to 255
        transparency : float from 0 to 1

        """
        if color_255 is None:
            color_255 = (randint(0, 255), randint(0, 255), randint(0, 255))
        for k, _ in part.anchors.items():
            self.wx_3d_viewer.display_vector(
                gp_Vec(*part.anchors[k]["direction"]),
                gp_Pnt(*part.anchors[k]["position"]))
        self.wx_3d_viewer.display_shape(part.node_shape.shape,
                                        color_=colour_wx_to_occ(color_255),
                                        transparency=transparency)

    def display_assembly(self, assembly, transparency=0.):
        r"""Display an assembly of parts and assemblies
        
        Parameters
        ----------
        assembly : AssemblyGeometryNode
        transparency : float from 0 to 1

        """
        assembly.build()

        for node in assembly.nodes():
            # for k, v in node.anchors.items():
            #     frame.p.display_vector(gp_Vec(*node.anchors[k]["direction"]),
            #                            gp_Pnt(*node.anchors[k]["position"]))
            self.wx_3d_viewer.display_shape(node.node_shape.shape,
                                            color_=colour_wx_to_occ((randint(0, 255),
                                                                      randint(0, 255),
                                                                      randint(0, 255))),
                                            transparency=transparency)

# parts


def view_part(part, color_255=None, transparency=0.):
    r"""Display the node in a 3D viewer

    Parameters
    ----------
    part : PartGeometryNode
    color_255 : Tuple[float, float, float]
        8-bit (0 - 255) color tuple
    transparency : float
        From 0. (not transparent) to 1 (fully transparent)

    """
    if color_255 is None:
        color_255 = (randint(0, 255), randint(0, 255), randint(0, 255))
    app = wx.App()
    frame = OsvCadFrame()

    frame.display_part(part, color_255, transparency)

    app.SetTopWindow(frame)
    app.MainLoop()

# assemblies


def view_assembly(assembly):
    r"""Display using osvcad's integrated wx viewer"""
    assembly.build()

    app = wx.App()
    frame = OsvCadFrame()

    frame.display_assembly(assembly)

    app.SetTopWindow(frame)
    app.MainLoop()


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

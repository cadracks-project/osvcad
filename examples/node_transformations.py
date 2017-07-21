# coding: utf-8

r"""Node transformations visual tests"""

from __future__ import division

from aocutils.display.wx_viewer import Wx3dViewer
import wx
from osvcad.nodes import GeometryNodeDirect
from ccad.model import box, translated

node_1 = GeometryNodeDirect(translated(box(30, 20, 10),
                                       (0, 0, 0)),
                            anchors={"a1": {"position": (5, 5, 10),
                                            "direction": (0, 0, 1)},
                                     "a2": {"position": (30, 10, 5),
                                            "direction": (1, 0, 1)}
                                     })

node_2 = node_1.translate((0, 0, 15))

node_3 = node_1.rotate(45, (0, 1, 0), (0, 0, 0))

node_4 = node_1.rotate(45, (0, 1, 0), (-30, 0, 0))


def main():
    r"""Main function of the example"""

    class MyFrame(wx.Frame):
        r"""Frame for testing"""

        def __init__(self):
            wx.Frame.__init__(self, None, -1)
            self.p = Wx3dViewer(self)
            self.Show()

    app = wx.App()
    frame = MyFrame()

    node_1.display(frame.p, (255, 0, 0), transparency=0.5)
    node_2.display(frame.p, (128, 0, 0), transparency=0.5)
    node_3.display(frame.p, (255, 0, 255), transparency=0.5)
    node_4.display(frame.p, (255, 128, 255), transparency=0.5)

    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == "__main__":
    main()

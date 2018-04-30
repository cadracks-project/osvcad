#!/usr/bin/env python
# coding: utf-8

r"""Main UI for osvcad"""

# import sys
import platform
import logging
import os.path
import configobj

import wx
import wx.aui
import wx.lib.agw.aui
from wx.adv import AboutDialogInfo, AboutBox

from corelib.core.files import path_from_file

import osvcad
from osvcad.ui.model import Model

from osvcad.ui.three_d import ThreeDPanel
from osvcad.ui.code import PythonEditor
from osvcad.ui.graph import GraphPanel

logger = logging.getLogger(__name__)


class OsvCadUiFrame(wx.Frame):
    r"""Main application frame

    Parameters
    ----------
    parent : None
    model : osvcad.ui.model.Model
        The application model.
    config : configobj.ConfigObj or None
        The application options

    """

    PANE_CODE_NAME = "Code"
    PANE_3D_NAME = "3d"
    PANE_GRAPH_NAME = "Graph"
    PANES = [PANE_CODE_NAME,
             PANE_3D_NAME,
             PANE_GRAPH_NAME]

    def __init__(self, parent, model, config):
        # logger.debug("Initializing WaterlineUiFrame")
        wx.Frame.__init__(self,
                          parent,
                          -1,
                          "osvcad",
                          style=wx.DEFAULT_FRAME_STYLE,
                          size=(800, 600))
        # Application icon
        # self.SetIcon(wx.IconFromLocation(wx.IconLocation(filename=r'fs.ico',
        #                                                  num=0)))
        if platform.system() == "Linux":
            self.Show()

        ico = path_from_file(__file__, "./fs.ico")
        self.SetIcon(wx.Icon(wx.IconLocation(filename=ico, num=0)))
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Config
        self.config = config
        try:
            frame_maximize = True if self.config["frame"]["maximize"] == "True" else False
            self.confirm_close = True if self.config["frame"]["confirm_close"] == "True" else False
            self.cad_default_dir = self.config["app"]["default_dir"]
            self.viewer_background_colour = tuple([float(el) for el in self.config["viewer"]["viewer_background_colour"]])
            self.objects_transparency = float(self.config["viewer"]["objects_transparency"])
            self.text_height = int(self.config["viewer"]["text_height"])
            self.text_colour = tuple([float(el) for el in self.config["viewer"]["text_colour"]])
        except (TypeError, KeyError):
            frame_maximize = True
            self.confirm_close = True
            self.cad_default_dir = ""
            self.viewer_background_colour = (50., 50., 50.)
            self.objects_transparency = 0.2
            self.text_height = 20
            self.text_colour = (0, 0, 0)
            # Report the problem
            msg = "No config loaded (wrong ini file name or missing key), " \
                  "using program defaults"
            wx.MessageBox(msg, 'Warning', wx.OK | wx.ICON_WARNING)

        self.model = model

        # Panels
        self.three_d_panel = \
            ThreeDPanel(self,
                        model,
                        viewer_background_color=self.viewer_background_colour,
                        object_transparency=self.objects_transparency,
                        text_height=self.text_height,
                        text_colour=self.text_colour)
        self.code_panel = PythonEditor(self, self.model)
        self.graph_panel = GraphPanel(self, self.model)

        # Menus, status bar ...
        self.init_ui()

        # AUI manager
        self._mgr = wx.lib.agw.aui.AuiManager()
        self._mgr.SetManagedWindow(self)  # notify AUI which frame to use

        self._mgr.AddPane(self.three_d_panel,
                          wx.lib.agw.aui.AuiPaneInfo().Right().
                          Name(OsvCadUiFrame.PANE_3D_NAME).Caption("3D").
                          MinSize(wx.Size(400, 200)).MaximizeButton(True))
        self._mgr.AddPane(self.graph_panel,
                          wx.lib.agw.aui.AuiPaneInfo().Right().
                          Name(OsvCadUiFrame.PANE_GRAPH_NAME).Caption("Graph").
                          MinSize(wx.Size(400, 100)).MaximizeButton(True))
        self._mgr.AddPane(self.code_panel,
                          wx.lib.agw.aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        # Show and maximize the frame
        self.Show(True)
        if frame_maximize is True:
            self.Maximize(True)  # Use the full screen
        else:
            self.CenterOnScreen()

        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        self._mgr.Update()

    def init_ui(self):
        r"""UI elements initialization"""

        menubar = wx.MenuBar()

        # File menu
        file_menu = wx.Menu()
        self.add_menu_item(menu=file_menu,
                           id_=wx.ID_OPEN,
                           text='&Open\tCtrl+O',
                           handler=self.on_open,
                           icon='./icons/open.png',
                           enabled=True)

        file_menu.AppendSeparator()

        self.add_menu_item(menu=file_menu,
                           id_=wx.ID_CLOSE,
                           text='&Quit\tCtrl+Q',
                           handler=self.on_quit,
                           icon='./icons/quit.png')
        menubar.Append(file_menu, '&File')

        # Windows menu
        windows_menu = wx.Menu()
        for name in OsvCadUiFrame.PANES:
            self.Bind(wx.EVT_MENU,
                      self.on_window_show,
                      windows_menu.Append(wx.ID_ANY, name, "Show " + name))
        menubar.Append(windows_menu, "&Windows")

        # Refresh menu
        refresh_menu = wx.Menu()
        self.add_menu_item(menu=refresh_menu,
                           id_=wx.NewId(),
                           text="Refresh",
                           handler=self.on_refresh,
                           icon='./icons/refresh.png')
        menubar.Append(refresh_menu, "&Refresh")

        # Help menu
        help_menu = wx.Menu()
        m_about = help_menu.Append(wx.ID_ABOUT,
                                   "&About",
                                   "Information about this program")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        menubar.Append(help_menu, "&Help")

        self.SetMenuBar(menubar)

        status_bar = wx.StatusBar(self)
        self.SetStatusBar(status_bar)

    def add_menu_item(self, menu, id_, text, handler, icon=None, enabled=True):
        r"""Add an item to a menu

        Parameters
        ----------
        menu
        id_
        text
        handler
        icon
        enabled : bool
            Should the menu item be enable (True) or
            Disabled (False) when created

        """
        menu_item = wx.MenuItem(parentMenu=menu, id=id_, text=text)
        if icon is not None:
            menu_item.SetBitmap(wx.Bitmap(icon))
        menu.Append(menu_item)
        if enabled is True:
            self.Bind(event=wx.EVT_MENU, handler=handler, id=id_)
        else:
            menu_item.Enable(False)

    # on_*
    # |
    # v

    def on_refresh(self, event):
        r"""Refresh handler"""
        with wx.BusyInfo("Refreshing ...") as busy_info:
            pass

    def on_window_show(self, event):
        r"""Handler that toggles AUI pane, allows to male an AUI pane visible
        again after it has been closed

        Parameters
        ----------
        event : wx event

        """
        name = event.GetEventObject().FindItemById(event.GetId()).GetLabel()

        if self._mgr.GetPane(name).IsShown():
            self._mgr.GetPane(name).Hide()
        else:
            self._mgr.GetPane(name).Show()
        self._mgr.Update()

    @staticmethod
    def on_about(event):
        r"""About has been chosen from the menu

        Parameters
        ----------
        event : wx.Event

        """
        info = AboutDialogInfo()
        info.Name = osvcad.__name__
        info.Version = osvcad.__version__
        info.Copyright = "(C) 2017 2018 osv-team"
        info.WebSite = (osvcad.__url__, )
        info.Developers = [osvcad.__author__]
        info.License = osvcad.__license__
        AboutBox(info)  # Show the wx.AboutBox

    def on_close(self, event):
        r"""Handle a click on the closing button (upper right cross)
        of the frame

        Parameters
        ----------
        event : wx.event

        """
        if self.confirm_close is True:
            dlg = wx.MessageDialog(self,
                                   "Do you really want to close this application?",
                                   "Confirm Exit",
                                   wx.OK | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.Destroy()
        else:
            self.Destroy()

    def on_open(self, e):
        r"""Handler for the Open menu item

        Open a Python file

        Parameters
        ----------
        e : wx.CommandEvent

        """
        dlg = wx.FileDialog(self,
                            message="Choose a file",
                            defaultFile="",
                            defaultDir="",
                            wildcard="Python files (*.py)|*.py",
                            style=wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path) as f:
                self.model.set_code(f.read())
        dlg.Destroy()

    def on_quit(self, e):
        r"""Handler for the Quit menu item

        Parameters
        ----------
        e : wx.CommandEvent

        """
        # logger.debug("Event Id : {id}".format(id=e.GetId()))
        self.Close()


def get_config():
    r"""Get the ConfigObj object from a osvcadui.ini file

    Returns
    -------
    configobj.ConfigObj or None

    """
    # app_path = os.path.abspath(os.path.dirname(os.path.join(sys.argv[0])))
    # inifile = os.path.join(app_path, "osvcadui.ini")
    inifile = path_from_file(__file__, "./osvcadui.ini")
    if not os.path.exists(inifile):
        logger.warning("No osvcadui.ini, using default values")
        return None
    else:
        config = configobj.ConfigObj(inifile)
    return config


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                               ':: %(lineno)3d :: %(message)s')

    app = wx.App()
    # wx.InitAllImageHandlers()
    model = Model()
    frame = OsvCadUiFrame(parent=None, model=model, config=get_config())
    frame.Show(True)

    # SafeYield(win, onlyIfNeeded)
    # see https://www.wxpython.org/docs/api/wx-module.html#SafeYield
    wx.SafeYield()

    # frame.runTests()
    app.SetTopWindow(frame)
    app.MainLoop()


if __name__ == '__main__':
    main()
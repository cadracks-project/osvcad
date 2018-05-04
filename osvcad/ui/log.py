# coding: utf-8

r"""Log panel that displays log messages"""

import wx
import logging


class WxTextCtrlHandler(logging.Handler):
    r"""Wx text control log handler
    
    Parameters
    ----------
    ctrl : wx.TextCtrl
        The control that will display the message

    """

    colors = {logging.DEBUG: wx.Colour(224, 224, 224),
              logging.INFO: wx.Colour(0, 204, 0),
              logging.WARNING: wx.Colour(255, 128, 0),
              logging.ERROR: wx.Colour(255, 51, 51),
              logging.CRITICAL: wx.Colour(102, 0, 102)}

    def __init__(self, ctrl):
        logging.Handler.__init__(self)
        self.ctrl = ctrl

    def emit(self, record):
        r"""Overriding the emit() method of Handler

        Parameters
        ----------
        record : ?
            The record to display

        """
        print(record.levelno)
        s = self.format(record) + '\n'
        self.ctrl.SetForegroundColour(WxTextCtrlHandler.colors[record.levelno])
        self.ctrl.WriteText(s)
        # wx.CallAfter(self.ctrl.WriteText, s)


# class RedirectText(object):
#     def __init__(self, aWxTextCtrl):
#         self.out = aWxTextCtrl
#
#     def write(self, string):
#         # self.out.WriteText(string)
#         wx.CallAfter(self.out.WriteText, string)


class LogPanel(wx.Panel):
    def __init__(self, parent):
        super(LogPanel, self).__init__(parent, wx.ID_ANY)

        # Add a panel so it looks the correct on all platforms
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=(300, 100),
                               style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL |wx.TE_RICH2)

        # Use a font where spaces and characters have the same width
        font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.log.SetFont(font)
        btn = wx.Button(self, wx.ID_ANY, 'Clear')
        self.Bind(wx.EVT_BUTTON, self.onButton, btn)

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(sizer)

        # Get the root logger
        logger = logging.getLogger()

        handler = WxTextCtrlHandler(self.log)
        logger.addHandler(handler)
        format_ = '%(asctime)s :: %(levelname)8s :: ' \
                  '%(module)20s :: %(lineno)3d :: %(message)s'
        handler.setFormatter(logging.Formatter(format_))
        logger.setLevel(logging.DEBUG)

        # redirect text here
        # redir = RedirectText(self.log)
        # sys.stdout = redir
        # sys.stderr = redir

    def onButton(self, event):
        self.log.Clear()

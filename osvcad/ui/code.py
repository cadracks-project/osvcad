# coding: utf-8

r"""Python code edition components"""

import keyword
import logging

import wx
import wx.stc

logger = logging.getLogger()

faces = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    # try temporary switch to mono
    'helv': 'Courier New',
    'other': 'Courier New',
    'size': 10,
    'size2': 8,
    }


class PythonEditor(wx.stc.StyledTextCtrl):
    """PythonEditor"""
    def __init__(self, parent, model):
        wx.stc.StyledTextCtrl.__init__(self, parent)
        self.model = model
        self.model.observe("selected_changed", self.on_selected_changed)
        # self.save_button = wx.Button(self, wx.ID_ANY, "Save code")
        self.initial_content = "".encode('utf-8')
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetTabWidth(4)

        keywords_list = []
        keywords_list.extend(keyword.kwlist)
        keywords_list.extend(['None', 'True', 'False'])
        # self.SetKeyWords(0, " ".join(keyword.kwlist))
        self.SetKeyWords(0, " ".join(keywords_list))

        # line numbers in the margin
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)

        # set other options ...
        self.SetProperty("fold", "1")
        self.SetMargins(0, 0)
        self.SetViewWhiteSpace(True)
        self.SetEdgeMode(wx.stc.STC_EDGE_BACKGROUND)
        # self.python_definition_file_editor.SetEdgeColumn(78)
        self.SetEdgeColumn(1000)
        self.SetCaretForeground("blue")

        # setup a margin to hold the fold markers
        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # fold markers use square headers
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,
                          wx.stc.STC_MARK_BOXMINUS,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,
                          wx.stc.STC_MARK_BOXPLUS,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,
                          wx.stc.STC_MARK_VLINE,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,
                          wx.stc.STC_MARK_LCORNER,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,
                          wx.stc.STC_MARK_BOXPLUSCONNECTED,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID,
                          wx.stc.STC_MARK_BOXMINUSCONNECTED,
                          "white",
                          "#808080")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL,
                          wx.stc.STC_MARK_TCORNER,
                          "white",
                          "#808080")

        # bind some events ...
        self.Bind(wx.stc.EVT_STC_UPDATEUI, self.onUpdateUI)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.onMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPressed)
        # self.Bind(wx.EVT_KEY_UP, self.onKeyUp)

        # make some general styles ...
        # global default styles for all languages
        # set default font
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                          "face:%(helv)s,size:%(size)d" % faces)

        # set default background color
        self.StyleSetBackground(style=wx.stc.STC_STYLE_DEFAULT, back='#FFFFFF')

        # reset all to be like the default
        # self.StyleClearAll()

        # more global default styles for all languages
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,
                          "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR,
                          "face:%(other)s" % faces)
        # self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,
        #                   "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,
                          "fore:#000000,back:#00FF33,bold")
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
                          "fore:#000000, back:#FF0000,bold")

        # make the Python styles ...

        # default
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT,
                          "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # comments
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,
                          "fore:#00CDCD,face:%(other)s,size:%(size)d" % faces)
        # comment-blocks
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK,
                          "fore:#7F7F7F,size:%(size)d" % faces)
        # number
        self.StyleSetSpec(wx.stc.STC_P_NUMBER,
                          "fore:#FF6600,bold,size:%(size)d" % faces)
        # string
        self.StyleSetSpec(wx.stc.STC_P_STRING,
                          "fore:#7F007F, face:%(helv)s,size:%(size)d" % faces)
        # single quoted string
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER,
                          "fore:#7F007F, face:%(helv)s,size:%(size)d" % faces)
        # keyword
        self.StyleSetSpec(wx.stc.STC_P_WORD,
                          "fore:#00007F,bold,size:%(size)d" % faces)
        # triple quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE,
                          "fore:#7F0000,size:%(size)d" % faces)
        # triple double quotes
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE,
                          "fore:#7F0000,size:%(size)d" % faces)
        # class name definition
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME,
                          "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # function or method name definition
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME,
                          "fore:#007F7F,bold,size:%(size)d" % faces)
        # operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # identifiers
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER,
                          "fore:#000000, underline, face:%(helv)s,size:%(size)d" % faces)

        # end of line where string is not closed
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL,
                          "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        # register some images for use in the AutoComplete box
        self.RegisterImage(1, wx.ArtProvider.GetBitmap(wx.ART_TIP,
                                                       size=(16, 16)))
        self.RegisterImage(2, wx.ArtProvider.GetBitmap(wx.ART_NEW,
                                                       size=(16, 16)))
        self.RegisterImage(3, wx.ArtProvider.GetBitmap(wx.ART_COPY,
                                                       size=(16, 16)))

    def on_selected_changed(self, evt):
        r"""Callback for a change of selected file in the model"""
        from os.path import isfile
        if isfile(self.model.selected):
            with open(self.model.selected) as f:
                try:
                    content = f.read()  # may raise UnicodeDecodeError
                    self.SetText(content)
                    self.Enable()
                except UnicodeDecodeError as e:
                    self.SetText("File cannot be decoded")
                    self.Disable()
        else:
            self.SetText("Not a file")
            self.Disable()

    def load_file(self, filepath):
        """Load a file in the PythonEditor"""
        parameters_file = open(filepath)
        self.initial_content = parameters_file.read()
        parameters_file.close()
        # self.SetTextUTF8(self.initial_content)
        self.SetText(self.initial_content)
        # self.save_button.Disable()
        self.EmptyUndoBuffer()

    def onKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()
            # tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'show tip stuff')
            # code completion (needs more work)
            else:
                kw = keyword.kwlist[:]
                # optionally add more ...
                kw.append("__init__?3")
                # Python sorts are case sensitive
                kw.sort()
                # so this needs to match
                self.AutoCompSetIgnoreCase(False)
                # registered images are specified with appended "?type"
                # for i in range(len(kw)):
                #     if kw[i] in keyword.kwlist:
                #         kw[i] += "?1"
                for word in kw:
                    if word in keyword.kwlist:
                        word += "?1"
                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def has_been_modified(self):
        """True if the current content is different from the content
        when a file was loaded"""
        if self.initial_content == self.GetText().encode('utf-8'):
            return False
        else:
            return True

    def onUpdateUI(self, evt):
        """Update the user interface"""

        # if self.has_been_modified():
        #     self.save_button.Enable()
        # else:
        #     self.save_button.Disable()

        # check for matching braces
        brace_at_caret = -1
        brace_opposite = -1
        char_before = None
        caret_pos = self.GetCurrentPos()
        if caret_pos > 0:
            char_before = self.GetCharAt(caret_pos - 1)
            style_before = self.GetStyleAt(caret_pos - 1)
        # check before
        if char_before and chr(char_before) in "[]{}()"\
                and style_before == wx.stc.STC_P_OPERATOR:
            brace_at_caret = caret_pos - 1
        # check after
        if brace_at_caret < 0:
            char_after = self.GetCharAt(caret_pos)
            style_after = self.GetStyleAt(caret_pos)

            if char_after and chr(char_after) in "[]{}()"\
                    and style_after == wx.stc.STC_P_OPERATOR:
                brace_at_caret = caret_pos
        if brace_at_caret >= 0:
            brace_opposite = self.BraceMatch(brace_at_caret)
        if brace_at_caret != -1 and brace_opposite == -1:
            self.BraceBadLight(brace_at_caret)
        else:
            self.BraceHighlight(brace_at_caret, brace_opposite)

    def onMarginClick(self, evt):
        """Fold and unfold as needed"""
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.foldAll()
            else:
                line_clicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(line_clicked) &\
                        wx.stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldexpanded(line_clicked, True)
                        self.expand(line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldexpanded(line_clicked):
                            self.SetFoldexpanded(line_clicked, False)
                            self.expand(line_clicked, False, True, 0)
                        else:
                            self.SetFoldexpanded(line_clicked, True)
                            self.expand(line_clicked, True, True, 100)
                    else:
                        self.ToggleFold(line_clicked)

    def foldAll(self):
        """Folding folds, marker - to +"""
        line_count = self.GetLineCount()
        expanding = True
        # find out if folding or unfolding
        for line_num in range(line_count):
            if self.GetFoldLevel(line_num) &\
                    wx.stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldexpanded(line_num)
                break
        line_num = 0
        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG\
                    and (level & wx.stc.STC_FOLDLEVELNUMBERMASK) == wx.stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldexpanded(line_num, True)
                    line_num = self.expand(line_num, True)
                    line_num -= 1
                else:
                    last_child = self.GetLastChild(line_num, -1)
                    self.SetFoldexpanded(line_num, False)
                    if last_child > line_num:
                        self.HideLines(line_num+1, last_child)
            line_num += 1

    def expand(self, line, doexpand, force=False, vis_levels=0, level=-1):
        """Expanding folds, marker + to -"""
        last_child = self.GetLastChild(line, level)
        line += 1
        while line <= last_child:
            if force:
                if vis_levels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doexpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if vis_levels > 1:
                        self.SetFoldexpanded(line, True)
                    else:
                        self.SetFoldexpanded(line, False)
                    line = self.expand(line, doexpand, force, vis_levels-1)
                else:
                    if doexpand and self.GetFoldexpanded(line):
                        line = self.expand(line, True, force, vis_levels-1)
                    else:
                        line = self.expand(line, False, force, vis_levels-1)
            else:
                line += 1
        return line

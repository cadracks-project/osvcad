# coding: utf-8

r"""Python code edition components"""

import keyword
import logging
from os.path import splitext, isfile

import wx
import wx.stc

from corelib.core.files import p_, is_binary
from corelib.core.python_ import is_valid_python

logger = logging.getLogger(__name__)


class CodePanel(wx.Panel):
    """Panel that displays code

    Parameters
    ----------
    parent : wx window

    """

    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.model = model

        self.save_button = wx.Button(self, wx.ID_ANY, "Save")

        # The save_button is initially disabled and will be enabled
        # when a modification has been made for an editable file
        self.save_button.Disable()

        bmp = wx.Image(p_(__file__, 'icons/save.png'),
                       wx.BITMAP_TYPE_PNG).Scale(24, 24).ConvertToBitmap()
        self.save_button.SetBitmap(bmp, wx.LEFT)
        self.Bind(wx.EVT_BUTTON,
                  self.on_save_button,
                  self.save_button)

        # # Sizers
        # controls_panel_sizer = wx.BoxSizer()
        # controls_panel_sizer.Add(self.save_button,
        #                          0,
        #                          wx.ALIGN_CENTER | wx.ALL, 10)

        self.file_editor = Editor(self, model, self.save_button)
        self.file_editor.Disable()
        # self.python_definition_file_editor.EmptyUndoBuffer()

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.file_editor, 90, wx.EXPAND)
        sizer.Add(self.save_button, 0, wx.ALIGN_RIGHT)

        self.SetSizer(sizer)

    def on_save_button(self, evt):
        r"""Callback for a click on the 'save parameters' button"""
        self.save_()

    def save_(self):
        r"""Write the parameters - i.e. save the modifications"""
        # Check that the definition file has a valid python syntax
        try:
            is_valid_python(self.file_editor.GetText())
        except SyntaxError as e:
            dlg = wx.MessageBox(
                'The parameters file contains the following '
                'error:\n    %s\n'
                'Do you want to save it anyway?' % e,
                'Save invalid parameters file ?',
                wx.YES_NO | wx.ICON_QUESTION)
            if dlg == wx.YES:
                pass
            elif dlg == wx.NO:
                return

        with open(self.file_editor.filepath, 'w') as f:
            f.write(self.file_editor.GetText())

        self.save_button.Disable()
        self.file_editor.initial_content = self.file_editor.GetText()
        # refresh all views
        self.model.set_selected(self.file_editor.filepath)

faces = {
    'times': 'Times New Roman',
    'mono': 'Courier New',
    # try temporary switch to mono
    'helv': 'Courier New',
    'other': 'Courier New',
    'size': 10,
    'size2': 8,
    }


class Editor(wx.stc.StyledTextCtrl):
    """Code Editor"""
    def __init__(self, parent, model, save_button):
        wx.stc.StyledTextCtrl.__init__(self, parent)
        self.model = model
        self.save_button = save_button
        self.model.observe("selected_changed", self.on_selected_changed)
        self.model.observe("root_folder_changed", self.on_root_folder_changed)
        # self.save_button = wx.Button(self, wx.ID_ANY, "Save code")
        self.initial_content = "".encode('utf-8')
        self.filepath = None
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

        logger.debug("Selection changed")

        sel = self.model.selected
        ext = splitext(sel)[1].lower()
        logger.info("File extension : %s" % ext)

        if isfile(sel):
            if is_binary(sel):
                if ext in [".stepzip"]:
                    self.SetText("Stepzip (binary) file")
                else:
                    self.SetText("Binary file")
                self.Disable()
            else:
                if ext in [".py", ".anchors"]:
                    self.SetLexer(wx.stc.STC_LEX_PYTHON)
                    self.load_file(sel)
                    self.Enable()
                elif ext in [".stepzip"]:
                    self.SetLexer(wx.stc.STC_LEX_AUTOMATIC)
                    self.SetText("zip file")
                    self.Disable()
                elif ext in [".step", ".stp", ".iges", ".igs", ".stl"]:
                    self.SetLexer(wx.stc.STC_LEX_AUTOMATIC)
                    self.load_file(sel)
                    self.Disable()
                elif ext == ".json":
                    self.SetLexer(wx.stc.STC_LEX_AUTOMATIC)
                    self.load_file(sel)
                    self.Disable()
                else:
                    self.SetLexer(wx.stc.STC_LEX_AUTOMATIC)
                    self.load_file(sel)
                    self.Disable()
                    logger.error("File has an extension %s that is not "
                                 "handled by the code panel" % ext)

        else:  # a directory is selected
            self.SetText("Not a file")
            self.Disable()

        self.Layout()

        logger.debug("code change detected in 3D panel")

    def on_root_folder_changed(self, evt):
        r"""Callback for a change of root folder"""
        self.SetText("")
        self.Disable()

    def load_file(self, filepath):
        """Load a file in the PythonEditor"""
        with open(filepath) as f:
            self.initial_content = f.read()
            self.filepath = filepath

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

        if self.has_been_modified():
            self.save_button.Enable()
        else:
            self.save_button.Disable()

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
                        self.SetFoldExpanded(line_clicked, True)
                        self.expand(line_clicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(line_clicked):
                            self.SetFoldExpanded(line_clicked, False)
                            self.expand(line_clicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(line_clicked, True)
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
                expanding = not self.GetFoldExpanded(line_num)
                break
        line_num = 0
        while line_num < line_count:
            level = self.GetFoldLevel(line_num)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG\
                    and (level & wx.stc.STC_FOLDLEVELNUMBERMASK) == wx.stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(line_num, True)
                    line_num = self.expand(line_num, True)
                    line_num -= 1
                else:
                    last_child = self.GetLastChild(line_num, -1)
                    self.SetFoldExpanded(line_num, False)
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
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.expand(line, doexpand, force, vis_levels-1)
                else:
                    if doexpand and self.GetFoldExpanded(line):
                        line = self.expand(line, True, force, vis_levels-1)
                    else:
                        line = self.expand(line, False, force, vis_levels-1)
            else:
                line += 1
        return line

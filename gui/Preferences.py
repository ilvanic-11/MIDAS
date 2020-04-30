import wx
import music21
import inspect
from midas_scripts import midiart, midiart3D, musicode, music21funcs
from midas_scripts.musicode import *
from midas_scripts.midiart import *
from midas_scripts.midiart3D import *
from midas_scripts.music21funcs import *

class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "", (20, 20))

        self.static_color = self.name_static = wx.StaticText(self, -1, "Default Color Palette")


        self.popupCtrl = ListCtrlComboPopup()

        # It is important to call SetPopupControl() as soon as possible
        self.comboCtrl.SetPopupControl(self.popupCtrl)

        # Populate using wx.ListView methods (populated with colors)
        for clrs in midiart.get_color_palettes():
            self.popupCtrl.AddItem(clrs)
        #One more call for FL Colors:
        self.popupCtrl.AddItem("FLStudioColors")

            #self.popupCtrl.InsertItem(popupCtrl.GetItemCount(), clrs)
        # self.popupCtrl.AddItem("Second Item")
        # self.popupCtrl.AddItem("Third Item")


        #self.chBox = wx.CheckBox(self, -1, "Create Musicode")
        self.span_statictxt = wx.StaticText(self, -1, "Grid-3D Span", style=wx.ALIGN_LEFT)
        self.input_span = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        self.bpm_statictxt = wx.StaticText(self, -1, "BPM", style=wx.ALIGN_LEFT)
        self.input_bpm = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        self.i_div_statictxt = wx.StaticText(self, -1, "i_div", style=wx.ALIGN_LEFT)
        self.input_i_div = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(self.span_statictxt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        topsizer.Add(self.input_span, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        topsizer.Add(self.bpm_statictxt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        topsizer.Add(self.input_bpm, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        topsizer.Add(self.i_div_statictxt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        topsizer.Add(self.input_i_div, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.static_color, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(self.comboCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(topsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        self.SetSizerAndFit(sizerMain)


#Taken straight from the docs.  See -->https://wxpython.org/Phoenix/docs/html/wx.ComboCtrl.html#wx-comboctrl
class ListCtrlComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)

class ToolsDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Midas Tool'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.func_id = 0

        #self.ass = wx.StaticText(self, -1, "ASS ASS ASS ASS")

        #self.funcname = wx.StaticText(self, -1, str(self.GetParent().FindItemById(self.func_id).GetName()))



        #eval("midiart." + "%s" % "array_to_lists_of")
        #[j for j in inspect.getfullargspec(midiart.array_to_lists_of)][0]

        #[j for j in inspect.getfullargspec(eval("midiart." + "%s" % "array_to_lists_of"))][0]

    def _generate_layout(self, event_id):
        self.func_id = event_id
        print("Gen_ID", self.func_id)
        self.func_name = str(self.GetParent().FindItemById(self.func_id).GetName())
        print("Gen_func_name", self.func_name)
        #self.musicode_workaround = super().GetParent().GetTopLevelParent().musicode
        #print("Gen_mc_func_name:", self.musicode_workaround)
        try:
            self.func_module = inspect.getmodule(eval(self.func_name))
        except NameError:
            self.func_module = super().GetParent().GetTopLevelParent().musicode
        #self.func_class = inspect.getmodule(eval(self))
        print("Gen_func_module", self.func_module)
        self.func_txt = wx.StaticText(self, -1, self.func_name)
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerHorizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerHorizontal.Add(self.func_txt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        #self.sizerMain.Add(self.ass, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        #print(eval("self.func_module.translate"))
        print("self.func_module" + '.' + "%s" % self.func_name)
        for argskwargs in [j for j in inspect.getfullargspec(eval(str("self.func_module" + '.' + "%s" % self.func_name)))][0]:
            argSizer = wx.BoxSizer(wx.VERTICAL)
            argkwargname = wx.StaticText(self, 0, argskwargs)
            argkwarginput = wx.TextCtrl(self, 0, argskwargs, size=(70, -1), style=wx.ALIGN_CENTER_HORIZONTAL, name=argskwargs)
            argSizer.Add(argkwargname, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
            argSizer.Add(argkwarginput, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
            self.sizerHorizontal.Add(argSizer)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.sizerMain.Add(self.sizerHorizontal)
        self.sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.SetSizerAndFit(self.sizerMain)
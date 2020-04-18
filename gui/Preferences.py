import wx
import music21


class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)


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
        sizerMain.Add(topsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        self.SetSizerAndFit(sizerMain)
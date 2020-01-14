import wx
import wx.richtext as rt
from midas_scripts import musicode, midiart, music21funcs

class StatsDisplayPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        #self.statsdisplay = StatsDisplay(self, -1, "StatsDisplay", wx.DefaultPosition,
         #                             (-1, -1), wx.DEFAULT_FRAME_STYLE, self.log)

        sizer = wx.BoxSizer(wx.VERTICAL)

        statsdisplaytitle = wx.StaticText(self, -1, "StatsDisplay", (20, 10))
        sizer.Add(statsdisplaytitle, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)

        btn_displaychords = wx.Button(self, -1, "Display Chord Details")
        sizer.Add(btn_displaychords, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnDisplayChords, btn_displaychords)

        btn_music21showtxt = wx.Button(self, -1, "Display Music21.show(\'txt\')")
        sizer.Add(btn_music21showtxt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnDisplayStreamShowTxt, btn_music21showtxt)

        btn_showmididata = wx.Button(self, -1, "Show Midi Data")
        sizer.Add(btn_showmididata, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnDisplayMidiData, btn_showmididata)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def OnDisplayChords(self, evt):
        chord_details_string = ""
        for i,p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
            chord_details_string += f"Layer {i}\n"
            chord_details_string += music21funcs.print_chords_in_piece(p.stream)
            chord_details_string += "\n"

        win = RichTextFrame(self, -1, chord_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Chord_Details")
        win.Show(True)

    def OnDisplayStreamShowTxt(self, evt):
        stream_details_string = ""
        for i,p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
            stream_details_string += f"Layer {i}\n"
            stream_details_string += music21funcs.print_show_streamtxt(p.stream)
            stream_details_string += "\n"

        win = RichTextFrame(self, -1, stream_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Stream_Details")
        win.Show(True)

    def OnDisplayMidiData(self, evt):
        stream_details_string = ""
        for i, p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
            stream_details_string += f"Layer {i}\n"
            stream_details_string += music21funcs.print_midi_data(p.stream)
            stream_details_string += "\n"

        win = RichTextFrame(self, -1, stream_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Midi_Details")
        win.Show(True)

class RichTextFrame(wx.Frame):
    def __init__(self, parent, id, value, pos, size, style, validator, name):
        wx.Frame.__init__(self, parent, id, name, pos, size, style, name)
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER);
        wx.CallAfter(self.rtc.SetFocus)
        self.rtc.WriteText(value)

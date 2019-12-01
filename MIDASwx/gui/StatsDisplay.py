import wx

class StatsDisplay(wx.Panel):
    def __init__(self, parent, id, title,  pos, size, style, log):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.log = log
        wx.StaticText(self, -1, title, (20, 10))

class StatsDisplayPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log
        #self.statsdisplay = StatsDisplay(self, -1, "StatsDisplay", wx.DefaultPosition,
         #                             (-1, -1), wx.DEFAULT_FRAME_STYLE, self.log)
        wx.StaticText(self, -1, "StatsDisplay", (20, 10))

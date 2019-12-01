import wx
from gui import MainButtons, StatsDisplay, PianoRollPanel
from wx.adv import SplashScreen as SplashScreen
import os
# explicitly importing these so pyInstaller works
import wx._adv, wx._html, wx._xml, wx.py, Musical_Matrix_Rain, time

loglevel = 1
class Log():
    """
    Temporary stupid logging to console.  Can add more later.
    """
    def WriteText(self, str):
        if (loglevel > 0):
            print(str)



class MainWindow(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)

        self.log = Log()

        self.SetSize((1400, 900))
        #self.CheckVersion()

        self.main = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.topsplit = wx.SplitterWindow(self.main, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)

        self.leftsplit = wx.SplitterWindow(self.topsplit, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)


        self.pycrustpanel = wx.py.shell.Shell(self.main)
        self.pianorollpanel = PianoRollPanel.PianoRollPanel(self.topsplit, self.log)
        self.mainbuttonspanel = MainButtons.MainButtonsPanel(self.leftsplit, self.log)
        self.statsdisplaypanel = StatsDisplay.StatsDisplayPanel(self.leftsplit, self.log)

        self.CreateStatusBar()
        self._set_properties()
        self._do_layout()
        self.Maximize(True)


    def _set_properties(self):
        self.SetTitle("MIDAS")
        self.pianorollpanel.SetBackgroundColour("white")
        self.statsdisplaypanel.SetBackgroundColour("silver")
        self.mainbuttonspanel.SetBackgroundColour("green")
        self.main.SetBackgroundColour("black")
        self.main.SetMinimumPaneSize(200)
        self.topsplit.SetMinimumPaneSize(200)
        self.leftsplit.SetMinimumPaneSize(150)

    def _do_layout(self):
        self.leftsplit.SplitHorizontally(self.mainbuttonspanel, self.statsdisplaypanel)
        self.topsplit.SplitVertically(self.leftsplit, self.pianorollpanel, )
        self.main.SplitHorizontally(self.topsplit, self.pycrustpanel)
        self.topsplit.SetSashPosition(200)

        self.Layout()


class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Image(r"..\resources\MIDAS_splash.png").ConvertToBitmap()
        SplashScreen.__init__(self, bmp,
                                 wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                                 2000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.CallLater(2000, self.ShowMain)


    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # topsplit frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        frame = MainWindow(None,-1, "MIDAS")
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
       #f wx.CallAfter(frame.ShowTip)



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainWindow(None, -1, "MIDAS")
    Musical_Matrix_Rain.rain_execute()

    splash = MySplashScreen()
    splash.Show()
    #time.sleep(5)
    #frm.Show()
    time.sleep(1.2)
    app.MainLoop()


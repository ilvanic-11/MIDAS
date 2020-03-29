import wx
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from gui import MainButtons, StatsDisplay, PianoRollPanel,Musical_Matrix_Rain
from wx.adv import SplashScreen as SplashScreen
#from Mayavi3D import Mayavi3idiArtAnimation
from Mayavi3D import Mayavi3DWindow
import mayavi
from mayavi import mlab
from mayavi import plugins
from mayavi.plugins import envisage_engine
from mayavi.api import Engine
from traits.trait_types import Function
from traits.trait_types import Method
import copy

import os
# explicitly importing these so pyInstaller works
import wx._adv, wx._html, wx._xml, wx.py, time

from traits.api import HasTraits

loglevel = 1
class Log():
    """
    Temporary stupid logging to console.  Can add more later.
    """
    def WriteText(self, str):
        if (loglevel > 0):
            print(str)

class MySplashScreen(SplashScreen):
    def __init__(self):
        bmp = wx.Image(r"resources\MIDAS_splash.png").ConvertToBitmap()
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
        # frame = MainWindow(None,-1, "MIDAS")
        # frame.Show()
        if self.fc.IsRunning():
            self.Raise()
       #f wx.CallAfter(frame.ShowTip)

class MainWindow(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)

        self.mainpanel = wx.Panel(self,-1)
        self.log = Log()

        self.SetSize((1400, 900))  #TODO Optimize for users screen resolution.

        self.basesplit = wx.SplitterWindow(self.mainpanel, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.main = wx.SplitterWindow(self.basesplit, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.topsplit = wx.SplitterWindow(self.main, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.leftsplit = wx.SplitterWindow(self.topsplit, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)



        # self.pianorollview = PianoRollPanel.PianoRollPanel()
        # self.pianorollpanel = self.pianorollview.edit_traits(
        #     parent=self.basesplit,
        #     kind='subpanel').control

        self.mayavi_view = Mayavi3DWindow.Mayavi3idiView()
        self.mayavi_view_control_panel = self.mayavi_view.edit_traits(parent=self.basesplit, kind='subpanel').control

        self.pyshellpanel = wx.py.shell.Shell(self.main)
        self.pianorollpanel = PianoRollPanel.PianoRollPanel(self.topsplit, self.log)
        self.mainbuttonspanel = MainButtons.MainButtonsPanel(self.leftsplit, self.log)
        self.statsdisplaypanel = StatsDisplay.StatsDisplayPanel(self.leftsplit, self.log)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.basesplit, 1, wx.EXPAND)
        self.mainpanel.SetSizerAndFit(sizer)

        # Use traits to create a panel, and use it as the content of this


        # Uncomment this for blank 3D panel
        #self.mayavi_view_control_panel = wx.Panel(self.basesplit)


        #self.mayavi_view.grid_to_stream = copy.deepcopy(self.pianorollpanel.Piano_Roll.PianoRoll.GridToStream)
        # print("FUNCTION", type(self.mayavi_view.grid_to_stream))
       # self.mayavi_view.stream_to_grid = copy.deepcopy(self.pianorollpanel.Piano_Roll.PianoRoll.StreamToGrid)
       # self.mayavi_view.pianolist = self.pianorollpanel.pianorolls
#
        #print("GRID_TO_STREAM2", type(self.mayavi_view.grid_to_stream))

        self.CreateStatusBar()
        self._set_properties()
        self._do_layout()


        #self.Maximize(True)

        self.pyshellpanel.run('''exec(open(str(os.getcwd()) + "\\\\resources\\\\" + "Midas_Startup_Configs.py").read())''')
        self.pyshellpanel.run('''intermediary_path''')
        #self.mayavi_view_control_panel.configure_traits()

        self.mainpanel.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        self.Show(True)
        self.mainpanel.SetFocus()
        #sizer.Layout()

    def OnKeyDown(self, event):
        #DDprint("OnKeyDown(): {}".format(chr(event.GetUnicodeKey())))
        if event.GetUnicodeKey() == ord('D'):
            if event.ShiftDown():
                #TopSashUp
                self.main.SetSashPosition(self.main.GetSashPosition() - 30)
            elif event.ControlDown():
                #TopSashDown
                self.main.SetSashPosition(self.main.GetSashPosition() + 30)
        elif event.GetUnicodeKey() == ord('G'):
            if event.ShiftDown():
                #BottomSashUp
                self.basesplit.SetSashPosition(self.basesplit.GetSashPosition() - 30)
            elif event.ControlDown():
                #BottomSashDown
                self.basesplit.SetSashPosition(self.basesplit.GetSashPosition() + 30)
        event.Skip()

    def _set_properties(self):
        self.SetTitle("MIDAS")
        self.pianorollpanel.SetBackgroundColour("white")
        self.statsdisplaypanel.SetBackgroundColour("silver")
        self.mainbuttonspanel.SetBackgroundColour("green")
        self.main.SetBackgroundColour("black")
        self.main.SetMinimumPaneSize(50)
        self.topsplit.SetMinimumPaneSize(150)
        self.leftsplit.SetMinimumPaneSize(200)
        self.basesplit.SetMinimumPaneSize(50)

    def _do_layout(self):
        self.leftsplit.SplitHorizontally(self.mainbuttonspanel, self.statsdisplaypanel)
        self.topsplit.SplitVertically(self.leftsplit, self.pianorollpanel)
        self.main.SplitHorizontally(self.topsplit, self.pyshellpanel)
        self.basesplit.SplitHorizontally(self.main, self.mayavi_view_control_panel)
        self.topsplit.SetSashPosition(200)
        self.leftsplit.SetSashPosition(600)
        self.main.SetSashPosition(900)
        self.basesplit.SetSashPosition(300)  ###Affects 3D title insert.
        self.mainpanel.Layout()
        self.Layout()







if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    #Musical_Matrix_Rain.rain_execute()
    # time.sleep(5)
    # splash = MySplashScreen()
    # splash.Show()
    app = wx.App()
    print(type(app))
    frm = MainWindow(None, -1, "MIDAS")

    #frm.Show()
    # time.sleep(1.2)
    app.MainLoop()
    #frm.mayavi_view.configure_traits()
   # mlab.show()
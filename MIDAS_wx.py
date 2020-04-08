import wx
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from gui import MainButtons, StatsDisplayPanel, PianoRollPanel,Musical_Matrix_Rain
from wx.adv import SplashScreen as SplashScreen
#from mayavi3D import Mayavi3idiArtAnimation
from mayavi3D import Mayavi3DWindow
from gui import StatusBar
#from logging import log
import mayavi
from mayavi import mlab
from mayavi import plugins
from mayavi.plugins import envisage_engine
from mayavi.api import Engine
from traits.trait_types import Function
from traits.trait_types import Method
import copy
from demo import images
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




        self.mayaviview = Mayavi3DWindow.Mayavi3idiView()

        self.mayaviviewpanel = self.mayaviview.edit_traits(parent=self.basesplit, kind='subpanel').control
        self.pyshellpanel = wx.py.crust.Crust(self.main, startupScript=str(os.getcwd() + "\\\\resources\\\\" + "Midas_Startup_Configs.py"))
        self.pianorollpanel = PianoRollPanel.PianoRollPanel(self.topsplit, self.log)
        self.mainbuttonspanel = MainButtons.MainButtonsPanel(self.leftsplit, self.log)
        self.statsdisplaypanel = StatsDisplayPanel.StatsDisplayPanel(self.leftsplit, self.log)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.basesplit, 1, wx.EXPAND)
        self.mainpanel.SetSizerAndFit(sizer)

        #Icon
        self.icon = wx.Icon()
        self.icon.LoadFile(r".\resources\TrebleClefIcon.bmp", type=wx.BITMAP_TYPE_ANY)     #, desiredHeight=10, desiredWidth=10)
        #self.icon.SetHeight(25)
        #self.icon.SetWidth(25)
        print("W", self.icon.GetWidth())
        print("H", self.icon.GetHeight())
        self.SetIcon(self.icon)

        #Status Bar
        self.statusbar = StatusBar.CustomStatusBar(self)
        self.SetStatusBar(self.statusbar)

        #This was fucking up size shit.
        #tc = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.SetSize((640, 480))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


        # Prepare the menu bar
        menuBar = wx.MenuBar()

        # 1st menu from left
        menu1 = wx.Menu()
        menu1.Append(101, "&New Session\tCtrl+Shift+N", "This the text in the Statusbar")  #TODO Saved Midas States
        menu1.Append(102, "&Open Session\tCtrl+O", "Open Slutsame")
        menu1.Append(103, "&Save Session\tCtrl+S", "You may select Earth too")
        menu1.Append(104, "&Save Session As\tCtrl+Shift+S")
        menu1.Append(105, "&Import...\tCtrl+I")
        menu1.Append(106, "&Import Directory\tCtrl+Shift+I")
        menu1.Append(105, "&Export...\tCtrl+E")  #Current Actor
        menu1.Append(106, "&Export Directory\tCtrl+Shift+E") #All Actors
        menu1.Append(107, "&Export Musicode\tCtrl+Shift+M") #All Actors
        menu1.Append(108, "&Export Movie\tCtrl+Alt+E") #All Actors
        menu1.Append(109, "&Preferences\tCtrl+P")
        menu1.Append(110, "&Intermediary Path\t")   #The Default Save path for all files. Found in resources.
        menu1.AppendSeparator()
        menu1.Append(104, "&Exit", "Close this frame")
        # Add menu to the menu bar
        menuBar.Append(menu1, "&File")

        # 2nd menu from left
        menu2 = wx.Menu()
        menu2.Append(201, "Undo\tCtrl+Z")
        menu2.Append(202, "Redo\tCtrl+Y")
        menu2.Append(203, "Cut\tCtrl+X")
        menu2.Append(204, "Copy\tCtrl+C")
        menu2.Append(205, "Paste\tCtrl+V")
        menu2.Append(206, "History")
        # a submenu in the 2nd menu
        #submenu = wx.Menu()
        #submenu.Append(2031, "Lanthanium")
        #submenu.Append(2032, "Cerium")
        #submenu.Append(2033, "Praseodymium")
        #menu2.Append(203, "Lanthanides", submenu)
        # Append 2nd menu
        menuBar.Append(menu2, "&Edit")

        menu3 = wx.Menu()
        # Radio items
        menu3.Append(301, "Show in DAW", "a Python shell using wxPython as GUI", wx.ITEM_RADIO)
        menu3.Append(302, "Show in Musescore", "a simple Python shell using wxPython as GUI", wx.ITEM_RADIO)
        menu3.Append(303, "Show in Word Processor", "a Python shell using tcl/tk as GUI", wx.ITEM_RADIO)
        menu3.Append(304, "Show in PicPick\Paint", "a Python shell using tcl/tk as GUI", wx.ITEM_RADIO)
        menu3.Append(305, "Show in Meshlab", "a simple Python shell using wxPython as GUI", wx.ITEM_RADIO)
        menu3.Append(306, "Show in Blender", "a simple Python shell using wxPython as GUI", wx.ITEM_RADIO)
        menu3.AppendSeparator()
        menu3.Append(307, "Scene3d_1?", "", wx.ITEM_NORMAL)
        menu3.Append(308, "project2", "", wx.ITEM_NORMAL)
        menuBar.Append(menu3, "&Show")

        menu4 = wx.Menu()
        # Check menu items
        menu4.Append(401, "Musicode")
        menu4.Append(402, "Midiart")
        menu4.Append(403, "3iDiart")
        menu4.Append(404, "Music21Funcs")
        menu7 = wx.Menu()
        menu8 = wx.Menu()
        menu9 = wx.Menu()
        menu4.Append(405, "Current ActorList to Shell", menu7)    #Dict of coords_arrays or Stream with parts(we're dealing with multiple actors for colors...)
        menu4.Append(406, "Current Actor to Shell", menu8)
        menu4.Append(407, "Current Z-Plane to Shell", menu9)

        menu7.Append(700, "As Music21 Stream with Parts")
        menu7.Append(701, "As Dictionary of Points")
        menu8.Append(800, "As Music21 Stream")
        menu8.Append(801, "As Numpy Points")
        menu9.Append(900, "As Music21 Stream")
        menu9.Append(901, "As Numpy Points")
        menuBar.Append(menu4, "&Tools")

        menu5 = wx.Menu()
        # Show how to put an icon in the menu item
        item = wx.MenuItem(menu5, 500, "&Search-Help\tCtrl++Shift+S")    #, "This one has an icon"
        #TODO Use a search bar with help(), inspect.getdoc, and for j in inspect.getmembers: print(j[0], j[1])

        item.SetBitmap(images.Smiles.GetBitmap())
        menu5.Append(item)

        # menuitemwithbmp = wx.MenuItem(menu5, wx.ID_ANY, "Submenu with Bitmap")
        # # Show how to change the background colour of the menu item
        # menuitemwithbmp.SetBackgroundColour(wx.YELLOW)
        # # Show how to change the menu item's text colour
        # menuitemwithbmp.SetTextColour(wx.BLUE)
        # # Show how to change the menu item's font
        # menuitemwithbmp.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, ''))
        # submenu = wx.Menu(style=wx.MENU_TEAROFF)
        # submenu.Append(wx.MenuItem(menu5, wx.ID_ANY, "Woot!"))
        # menuitemwithbmp.SetBitmap(images.book.GetBitmap())
        # menuitemwithbmp.SetSubMenu(submenu)
        # menu5.Append(menuitemwithbmp)

        # Shortcuts
        menu5.Append(501, "About Midas...")
        menu5.AppendSeparator()
        menu5.Append(502, "Licensing\tShift+H")
        menu5.AppendSeparator()
        menu6 = wx.Menu()
        menu5.Append(503, "Documentation", menu6)
        menu6.Append(601, "Music21")
        menu6.Append(602, "Mayavi")
        menu6.Append(603, "Numpy")
        menu6.Append(604, "Sympy")
        menu6.Append(605, "Open3D")
        menu6.Append(606, "Open-CVPython")
        menu6.Append(607, "VTK")
        menu6.Append(608, "TVTK")
        #menu6.Append(601, "Midas Homepage")
        menu5.Append(504, "Midas Homepage")
        menu5.Append(505, "The Magic Hammer Homepage")
        menu5.Append(506, "Tutorials")
        menu5.Append(507, "Community")
        menu5.Append(508, "Google Search")
        menu5.Append(509, "Check for Updates...")
        menu5.Append(510, "Credits.")
        menuBar.Append(menu5, "&Help")

        self.SetMenuBar(menuBar)
        #self.CreateStatusBar()
        self._set_properties()
        self._do_layout()

        self.Maximize(True)
        #pyshell
        #self.pyshellpanel.run('''exec(open(str(os.getcwd()) + "\\\\resources\\\\" + "Midas_Startup_Configs.py").read())''')
        #self.pyshellpanel.run('''intermediary_path''')


        self.mainpanel.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        self.Show(True)
        self.SetFocus()
        #sizer.Layout()

    def OnCloseWindow(self, event):
        self.statusbar.timer.Stop()
        del self.statusbar.timer
        self.Destroy()

    def OnKeyDown(self, event):
        #DDprint("OnKeyDown(): {}".format(chr(event.GetUnicodeKey())))
        if event.GetUnicodeKey() == ord('D'):
            if event.ShiftDown():
                #TopSashUp
                self.main.SetSashPosition(self.main.GetSashPosition() - 150)
            elif event.ControlDown():
                #TopSashDown
                self.main.SetSashPosition(self.main.GetSashPosition() + 150)
        elif event.GetUnicodeKey() == ord('G'):
            if event.ShiftDown():
                #BottomSashUp
                self.basesplit.SetSashPosition(self.basesplit.GetSashPosition() - 150)
            elif event.ControlDown():
                #BottomSashDown
                self.basesplit.SetSashPosition(self.basesplit.GetSashPosition() + 150)
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
        self.basesplit.SplitHorizontally(self.main, self.mayaviviewpanel)
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
    Midas = wx.App()
    print(type(Midas))
    frm = MainWindow(None, -1, "MIDAS")

    #frm.Show()
    # time.sleep(1.2)
    Midas.MainLoop()
    #frm.mayaviview.configure_traits()
   # mlab.show()

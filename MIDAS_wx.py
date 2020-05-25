import wx
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from gui import MenuButtons, MainButtons, PianoRollPanel,Musical_Matrix_Rain,Preferences
from wx.adv import SplashScreen as SplashScreen
#from mayavi3D import Mayavi3idiArtAnimation
from mayavi3D import Mayavi3DWindow, MusicObjects
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
#from demo import images
import os
# explicitly importing these so pyInstaller works
import wx._adv, wx._html, wx._xml, wx.py, time

from traits.api import HasTraits
from midas_scripts import musicode


import logging
logFormatter = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.DEBUG, filename=r"./log.txt")


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
        # pianoroll_mainbuttons_split frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()


    def ShowMain(self):
        # frame = MainWindow(None,-1, "MIDAS")
        # frame.Show()
        if self.fc.IsRunning():
            self.Raise()
       #f wx.CallAfter(frame.ShowTip)

class MyCrust(wx.py.crust.Crust):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SP_3D | wx.SP_LIVE_UPDATE,
                 name='Crust Window', rootObject=None, rootLabel=None,
                 rootIsNamespace=True, intro='', locals=None,
                 InterpClass=None,
                 startupScript=None, execStartupScript=True,
                 *args, **kwds):
        super().__init__(parent, id, pos, size, style, name, rootObject, rootLabel, rootIsNamespace,intro,
                       locals, InterpClass, startupScript, execStartupScript)

        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnSashDClick)
        
    def OnSashDClick(self, event):
        # do nothing.  overloads pycrust's default implementation which is to unsplit when double clicking the sash
        pass
    
        
class MainWindow(wx.Frame):
    log = logging.getLogger(__name__)
    
    def __init__(self, parent, id, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.mainpanel = wx.Panel(self,-1)
       
        self.SetSize((1400, 900))  #TODO Optimize for users screen resolution.

        self.top_mayaviview_split = wx.SplitterWindow(self.mainpanel, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.top_pyshell_split = wx.SplitterWindow(self.top_mayaviview_split, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.pianoroll_mainbuttons_split = wx.SplitterWindow(self.top_pyshell_split, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.mainbuttons_stats_split = wx.SplitterWindow(self.pianoroll_mainbuttons_split, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)


        #self.musicode = musicode.Musicode()


        self.mayavi_view = Mayavi3DWindow.Mayavi3idiView(self)
        self.mayavi_view_control_panel = self.mayavi_view.edit_traits(parent=self.top_mayaviview_split, kind='subpanel').control
       
        self.pyshellpanel = MyCrust(self.top_pyshell_split, startupScript=str(os.getcwd() + "\\\\resources\\\\" + "Midas_Startup_Configs.py"))
        self.pianorollpanel = PianoRollPanel.PianoRollPanel(self.pianoroll_mainbuttons_split, self.log)
        self.mainbuttonspanel = MainButtons.MainButtonsPanel(self.pianoroll_mainbuttons_split, self.log)
        #self.statsdisplaypanel = StatsDisplayPanel.StatsDisplayPanel(self.mainbuttons_stats_split, self.log)

        #Actor on startup.
        self.pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(0)
        self.mayavi_view.actors[0].change_points(MusicObjects.earth())

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.top_mayaviview_split, 1, wx.EXPAND)
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
        self.menuBar = MenuButtons.CustomMenuBar()


        # TODO Use a search bar with help(), inspect.getdoc, and for j in inspect.getmembers: print(j[0], j[1])
        ##Notes for creating a dynamic user help system.
        # In conjuction with the status bar, Use python's help(), inspect.getdocs(object) and\or
        # -->for i in inspect.getmembers(object):
        # --->   print(i[0], "  ", i[1])


        ###Menu Button Bindings
        ##wx Restriction ---    Note: To respond to a menu selection, provide a handler for wx.EVT_MENU
        # in the frame that contains the menu bar.

        # File
        #Note -- Conflicting\Double ids will cause the function call to fail\not exist.
        self.Bind(wx.EVT_MENU, self.menuBar.OnNewSession, id=101)
        self.Bind(wx.EVT_MENU, self.menuBar.OnOpenSession, id=102)
        self.Bind(wx.EVT_MENU, self.menuBar.OnSaveSession, id=103)
        self.Bind(wx.EVT_MENU, self.menuBar.OnSaveSessionAs, id=104)
        self.Bind(wx.EVT_MENU, self.menuBar.OnImport, id=105)
        self.Bind(wx.EVT_MENU, self.menuBar.OnImportDirectory, id=106)

        #self.Bind(wx.EVT_MENU, self.menuBar.OnExport, id=107)  #TODO Free id available; 107
        #Export Submenu
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_CurrentActor, id=1500)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_AllActors, id=1501)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_CurrentActorsCurrentZplane, id=1502)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_AllCurrentActorsZplanes, id=1503)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Selection, id=1504)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Colors, id=1505)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Text, id=1506)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_PointCloud, id=1507)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Image, id=1508)

        self.Bind(wx.EVT_MENU, self.menuBar.OnExportAsDirectory, id=108)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExportMusicode, id=109)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExportMovie, id=110)
        self.Bind(wx.EVT_MENU, self.menuBar.OnPreferences, id=111)
        # Preferences Dialog bind.
        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.menuBar._OnPrefDialogCloser)

        self.Bind(wx.EVT_MENU, self.menuBar.OnIntermediaryPath, id=112)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExit, id=113)

        # Edit
        self.Bind(wx.EVT_MENU, self.menuBar.OnUndo, id=201)
        self.Bind(wx.EVT_MENU, self.menuBar.OnRedo, id=202)
        self.Bind(wx.EVT_MENU, self.menuBar.OnCut, id=203)
        self.Bind(wx.EVT_MENU, self.menuBar.OnCopy, id=204)
        self.Bind(wx.EVT_MENU, self.menuBar.OnPaste, id=205)
        self.Bind(wx.EVT_MENU, self.menuBar.OnHistory, id=206)

        # Show
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInDAW, id=301)
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInMuseScore, id=302)
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInWordProcessor, id=303)
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInPaint, id=304)
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInMeshlab, id=305)
        self.Bind(wx.EVT_MENU, self.menuBar.OnShowInBlender, id=306)

        self.Bind(wx.EVT_MENU, self.menuBar.OnScene3d_1, id=307)
        self.Bind(wx.EVT_MENU, self.menuBar.OnProject2, id=308)

        # Tools
        #Analyze..
        self.Bind(wx.EVT_MENU, self.menuBar.OnDisplayChords, id=1400)
        self.Bind(wx.EVT_MENU, self.menuBar.OnDisplayStreamShowTxt, id=1401)
        self.Bind(wx.EVT_MENU, self.menuBar.OnDisplayMidiData, id=1402)
        self.Bind(wx.EVT_MENU, self.menuBar.OnDisplayCellSizesData, id=1403)

        #Musicode, Midiart, 3idiart, Music21funcs...
        # self.Bind(wx.EVT_MENU, self.menuBar.OnMusicode, id=401)
        # self.Bind(wx.EVT_MENU, self.menuBar.OnMidiart, id=402)
        # self.Bind(wx.EVT_MENU, self.menuBar.On3iDiart, id=403)
        # self.Bind(wx.EVT_MENU, self.menuBar.OnMusic21Funcs, id=404)

        #Submenus...
        # self.Bind(wx.EVT_MENUself.menuBar.f.OnCurrentActorListToShell, id=405)
        # self.Bind(wx.EVT_MENUself.menuBar.f.OnCurrentActorToShell, id=406)
        # self.Bind(wx.EVT_MENUself.menuBar.f.OnCurrentZplaneToShell, id=407)

        # Submenu #TODO Might have to do additional work for different cases.....(i.e the multi-actor color image import)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsMusic21StreamWithParts, id=700)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsDictionaryOfPoints, id=701)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsMusic21Stream,
                  id=800)  # Caself.menuBar. same function be bound to two different buttons?
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsNumpyPoints, id=801)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsMusic21Stream, id=900)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAsNumpyPoints, id=901)

        # Help
        self.Bind(wx.EVT_MENU, self.menuBar.OnSearchHelp, id=500)
        self.Bind(wx.EVT_MENU, self.menuBar.OnAboutMidas, id=501)
        self.Bind(wx.EVT_MENU, self.menuBar.OnLicensing, id=502)
        #self.Bind(wx.EVT_MENU, self.menuBar.OnDocumentation, id=503)  #This leads to a submenu.
        self.Bind(wx.EVT_MENU, self.menuBar.OnMidasHomepage, id=504)
        self.Bind(wx.EVT_MENU, self.menuBar.OnTheMagicHammerHomepage, id=505)
        self.Bind(wx.EVT_MENU, self.menuBar.OnTutorials, id=506)
        self.Bind(wx.EVT_MENU, self.menuBar.OnCommunity, id=507)
        self.Bind(wx.EVT_MENU, self.menuBar.OnGoogleSearch, id=508)
        self.Bind(wx.EVT_MENU, self.menuBar.OnCheckForUpdates, id=509)
        self.Bind(wx.EVT_MENU, self.menuBar.OnCredits, id=510)

        # Documentation Submenu
        self.Bind(wx.EVT_MENU, self.menuBar.OnPython, id=600)
        self.Bind(wx.EVT_MENU, self.menuBar.OnMusic21, id=601)
        self.Bind(wx.EVT_MENU, self.menuBar.OnMayavi, id=602)
        self.Bind(wx.EVT_MENU, self.menuBar.OnNumpy, id=603)
        self.Bind(wx.EVT_MENU, self.menuBar.OnSympy, id=604)
        self.Bind(wx.EVT_MENU, self.menuBar.OnOpen3D, id=605)
        self.Bind(wx.EVT_MENU, self.menuBar.OnOpenCVPython, id=606)
        self.Bind(wx.EVT_MENU, self.menuBar.OnVTK, id=607)
        self.Bind(wx.EVT_MENU, self.menuBar.OnTVTK, id=608)

        # Tools Menu Comprehensive Bind Functions
        #0self.Bind(wx.EVT_MENU, self.menuBar.OnToolSelection, id=1100)

        self._bind_musicode_tools()
        self._bind_midiart_tools()
        self._bind_midiart3D_tools()
        self._bind_music21funcs_tools()

        self.SetMenuBar(self.menuBar)

        # Maxes top_pyshell_split window.
        #self.Maximize(True)
        self.SetSize(1920, 1080)
        
        # self.CreateStatusBar()
        self._set_properties()
        self._do_layout()

        


        # Pyshell Resplit on Init becasue pyshell defaults to SplitHorizontal()
        self.pyshellpanel.Unsplit(self.pyshellpanel.Window2)  #Actually, it can be read, because this works.
        # self.pyshellpanel.AddChild(self.pyshellpanel.notebook)
        self.pyshellpanel.SplitVertically(self.pyshellpanel.Window1, self.pyshellpanel.notebook)
        self.pyshellpanel.SetSashPosition(800)
        self.pyshellpanel.SetMinimumPaneSize(400)
        


        self.mainpanel.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        self.Show(True)
        self.SetFocus()

    #Comprehensive Menu Bind Functions
    def _bind_musicode_tools(self):
        binding = 1000
        for i in range(0, len(self.menuBar.musicodetools.MenuItems)):
            self.Bind(wx.EVT_MENU, self.menuBar.OnToolSelection, id=binding)
            binding += 1

    def _bind_midiart_tools(self):
        binding = 1100
        for i in self.menuBar.midiarttools.MenuItems:
            self.Bind(wx.EVT_MENU, self.menuBar.OnToolSelection, id=binding)
            binding += 1

    def _bind_midiart3D_tools(self):
        binding = 1200
        for i in self.menuBar.midiart3Dtools.MenuItems:
            self.Bind(wx.EVT_MENU, self.menuBar.OnToolSelection, id=binding)
            binding += 1

    def _bind_music21funcs_tools(self):
        binding = 1300
        for i in self.menuBar.music21funcstools.MenuItems:
            self.Bind(wx.EVT_MENU, self.menuBar.OnToolSelection, id=binding)
            binding += 1


    #StatusBarClose
    def OnCloseWindow(self, event):
        self.statusbar.timer.Stop()
        del self.statusbar.timer
        self.Destroy()

    #Sash Hotkey
    def OnKeyDown(self, event):
        #DDprint("OnKeyDown(): {}".format(chr(event.GetUnicodeKey())))
        if event.GetUnicodeKey() == ord('D'):
            if event.AltDown():
                #TopSashUp
                self.top_pyshell_split.SetSashPosition(self.top_pyshell_split.GetSashPosition() - 48)
            elif event.ControlDown():
                #TopSashDown
                self.top_pyshell_split.SetSashPosition(self.top_pyshell_split.GetSashPosition() + 48)
        elif event.GetUnicodeKey() == ord('G'):
            if event.AltDown():
                #BottomSashUp
                self.top_mayaviview_split.SetSashPosition(self.top_mayaviview_split.GetSashPosition() - 48)
            elif event.ControlDown():
                #BottomSashDown
                self.top_mayaviview_split.SetSashPosition(self.top_mayaviview_split.GetSashPosition() + 48)
        event.Skip()


    def _set_properties(self):
        self.SetTitle("MIDAS")
        self.pianorollpanel.SetBackgroundColour("white")
        #self.statsdisplaypanel.SetBackgroundColour("silver")
        self.mainbuttonspanel.SetBackgroundColour("green")
        self.top_pyshell_split.SetBackgroundColour("black")
        self.top_pyshell_split.SetMinimumPaneSize(50)
        self.pianoroll_mainbuttons_split.SetMinimumPaneSize(120)
        #self.mainbuttons_stats_split.SetMinimumPaneSize(200)
        self.top_mayaviview_split.SetMinimumPaneSize(50)

        #TODO Put somewhere else?
        self.mayavi_view.cur_z = 90

    def _do_layout(self):
        #self.mainbuttons_stats_split.SplitHorizontally(self.mainbuttonspanel, self.statsdisplaypanel)
        #self.pianoroll_mainbuttons_split.SplitVertically(self.mainbuttons_stats_split, self.pianorollpanel)
        self.pianoroll_mainbuttons_split.SplitVertically(self.mainbuttonspanel, self.pianorollpanel)
        self.top_pyshell_split.SplitHorizontally(self.pianoroll_mainbuttons_split, self.pyshellpanel)
        self.top_mayaviview_split.SplitHorizontally(self.top_pyshell_split, self.mayavi_view_control_panel)
        
        self.pianoroll_mainbuttons_split.SetSashPosition(120)
        #self.mainbuttons_stats_split.SetSashPosition(400)
        self.top_pyshell_split.SetSashPosition(300)
        self.top_mayaviview_split.SetSashPosition(600)  ###Affects 3D title insert
        
        self.top_mayaviview_split.SetSashGravity(0.5)
        self.top_pyshell_split.SetSashGravity(0.5)
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
    Midas = app.GetTopWindow()
    #frm.Show()
    # time.sleep(1.2)

    app.MainLoop()




    #frm.mayavi_view.configure_traits()

   # mlab.show()


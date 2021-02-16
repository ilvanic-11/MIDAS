import wx
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from gui import MenuButtons, MainButtons, PianoRollPanel, Musical_Matrix_Rain, Preferences
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
from midas_scripts import musicode   ###, midiart3D


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

    ###F Hotkeys for this panel.
    # -----------------------------------------
    def AccelerateHotkeys(self):

        entries = [wx.AcceleratorEntry() for i in range(0, 10)]


        new_id1 = wx.NewIdRef()
        new_id2 = wx.NewIdRef()
        new_id3 = wx.NewIdRef()
        new_id4 = wx.NewIdRef()
        new_id5 = wx.NewIdRef()
        new_id6 = wx.NewIdRef()
        new_id7 = wx.NewIdRef()
        new_id8 = wx.NewIdRef()
        new_id9 = wx.NewIdRef()
        new_id10 = wx.NewIdRef()

        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMusic21ConverterParseDialog, id=new_id1)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMusicodeDialog, id=new_id2)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMIDIArtDialog, id=new_id3)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMIDIArt3DDialog, id=new_id4)

        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_actors_listbox, id=new_id5)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_zplanes, id=new_id6)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_pianorollpanel, id=new_id7)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_pycrust, id=new_id8)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_mayavi_view, id=new_id9)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_mainbuttonspanel, id=new_id10)

        # Shift into which gear.
        entries[0].Set(wx.ACCEL_NORMAL, wx.WXK_F1, new_id1)
        entries[1].Set(wx.ACCEL_NORMAL, wx.WXK_F2, new_id2)
        entries[2].Set(wx.ACCEL_NORMAL, wx.WXK_F3, new_id3)
        entries[3].Set(wx.ACCEL_NORMAL, wx.WXK_F4, new_id4)

        entries[4].Set(wx.ACCEL_NORMAL, wx.WXK_F5, new_id5)
        entries[5].Set(wx.ACCEL_NORMAL, wx.WXK_F6, new_id6)
        entries[6].Set(wx.ACCEL_NORMAL, wx.WXK_F7, new_id7)
        entries[7].Set(wx.ACCEL_NORMAL, wx.WXK_F8, new_id8)
        entries[8].Set(wx.ACCEL_NORMAL, wx.WXK_F9, new_id9)

        entries[9].Set(wx.ACCEL_NORMAL, wx.WXK_F11, new_id10)

        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)
        
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


        self.musicode = musicode.Musicode()


        self.mayavi_view = Mayavi3DWindow.Mayavi3idiView(self)

        self.mayaviviewcontrolpanel = self.mayavi_view.edit_traits(parent=self.top_mayaviview_split, kind='subpanel').control
        self.pyshellpanel = MyCrust(self.top_pyshell_split, startupScript=str(os.getcwd() + "\\\\resources\\\\" + "Midas_Startup_Configs.py"))
        self.pianorollpanel = PianoRollPanel.PianoRollPanel(self.pianoroll_mainbuttons_split, self.log)
        self.mainbuttonspanel = MainButtons.MainButtonsPanel(self.pianoroll_mainbuttons_split, self.log)
        #self.statsdisplaypanel = StatsDisplayPanel.StatsDisplayPanel(self.mainbuttons_stats_split, self.log)

        ###

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
        self.menuBar = MenuButtons.CustomMenuBar(self)


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

        #self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Colors, id=1505)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Text, id=1506)  #TODO Change ids?
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_Image, id=1507)
        self.Bind(wx.EVT_MENU, self.menuBar.OnExport_PointCloud, id=1508)

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
        

        self.mainpanel.Bind(wx.EVT_CHAR_HOOK, self.OnSashKeyDown)
        #self.mainpanel.Bind(wx.EVT_MOUSEWHEEL, self.OnScrollZplanes)
        self.mainpanel.Bind(wx.EVT_MOUSEWHEEL, self.OnScrollActors_Zplanes)
        self.mainpanel.Bind(wx.EVT_CHAR_HOOK, self.OnMiddleClickGrabNSend)
        from wx import grid
        self.pianorollpanel.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.PrintOurCell)
        self.Show(True)

        #TODO Return to this? (focus is set on mainbuttonspanel as part of the __main__ loop call at the bottom.
        #self.SetFocus()



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
    def OnSashKeyDown(self, event):
        #TODO Doc strings.

        #DDprint("OnKeyDown(): {}".format(chr(event.GetUnicodeKey())))
        if event.GetUnicodeKey() == ord('D'):
            if event.AltDown():
                #TopSashUp
                self.top_pyshell_split.SetSashPosition(self.top_pyshell_split.GetSashPosition() - 48)
            elif event.ControlDown():
                #TopSashDown
                self.top_pyshell_split.SetSashPosition(self.top_pyshell_split.GetSashPosition() + 48)
            self.mayavi_view.new_reticle_box()
        elif event.GetUnicodeKey() == ord('G'):
            if event.AltDown():
                #BottomSashUp
                self.top_mayaviview_split.SetSashPosition(self.top_mayaviview_split.GetSashPosition() - 48)
            elif event.ControlDown():
                #BottomSashDown
                self.top_mayaviview_split.SetSashPosition(self.top_mayaviview_split.GetSashPosition() + 48)
            self.mayavi_view.new_reticle_box()
        event.Skip()


    def OnScrollActors_Zplanes(self, event):
        """
        :param event:
        :return:
        This function allows for rapid selection of actors and zplanes via a CTRL+SHIFT\CTRL+ALL hotkey combination while scrolling the mousewheel.
        Ctrl+Shift+Scroll up and down will scroll through the actors listbox while Ctrl+Alt+Scroll will scroll through the zplanes list box. Upon scrolling
        to the desired item, release the respective SHIFT or ALT will stop the scroll process; then, while CTRL is still held, Ctrl+Scroll UP to 'activate' selected
        actor, and Ctrl+Scroll DOWN to activate selected Zplane.
        Notes:
        1*--This loop prevents multiple-select while trying to scroll through the listboxes using this function.
        """

        # if self.FindFocus() != type('gui.MainButtons.MainButtonsPanel'):
        #     self.mainbuttonspanel.SetFocus()
        alb = self.pianorollpanel.actorsctrlpanel.actorsListBox
        zlb = self.pianorollpanel.zplanesctrlpanel.ZPlanesListBox

        if event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL or event.GetWheelDelta() < 120:
            event.Skip()
            return

        mousestate = wx.GetMouseState()

        #TODO FIgure out way to activate one at a time.

        ##ACTORS List Box
        #if event.GetUnicodeKey() == ord('A'):
        if mousestate.ControlDown():  #HOLD CTRL
            if mousestate.ShiftDown():  #HOLD SHIFT AND SCROLL TO DESIRED ACTOR LIST ITEM
                #self.IsActorScrolling = True
                alb.SetFocus()
                if event.GetWheelRotation() >= 120:
                    if self.actor_scrolled == 0:
                        pass
                    else:
                        self.actor_scrolled -= 1
                    print("Actor Scrolled -->", self.actor_scrolled)
                    alb.Select(self.actor_scrolled)
                    alb.Focus(self.actor_scrolled)
                    #1*
                    for i in range(0, len(self.mayavi_view.actors)):
                        # If it's selected, unselect it.
                        if alb.IsSelected(i) and i != self.actor_scrolled:
                            alb.Select(i, on=0)
                        # If not, pass.
                        elif alb.IsSelected(i) and i == self.actor_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            alb.Select(self.actor_scrolled, on=1)
                    # self.pianorollpanel.actorsctrlpanel.actorsListBox.Select
                elif event.GetWheelRotation() <= -120:
                    if self.actor_scrolled == alb.GetItemCount() - 1:
                        pass
                    else:
                        self.actor_scrolled += 1
                    print("Actor Scrolled -->", self.actor_scrolled)
                    alb.Select(self.actor_scrolled)
                    alb.Focus(self.actor_scrolled)
                    #1*
                    for i in range(0, len(self.mayavi_view.actors)):
                        # If it's selected, unselect it.
                        if alb.IsSelected(i) and i != self.actor_scrolled:
                            alb.Select(i, on=0)
                        # If not, pass.
                        elif alb.IsSelected(i) and i == self.actor_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            alb.Select(self.actor_scrolled, on=1)
            elif mousestate.AltDown():  # HOLD ALT AND SCROLL TO DESIRED Z-PLANE LIST ITEM   # and event.ShiftDown():
                #self.IsZPlaneScrolling = True
                if event.GetWheelRotation() >= 120:
                    if self.zplane_scrolled == 0:
                        pass
                    else:
                        self.zplane_scrolled -= 1
                    print("Zplane Scrolled -->", self.zplane_scrolled)
                    zlb.Select(self.zplane_scrolled)
                    zlb.Focus(self.zplane_scrolled)
                    #1*
                    for i in range(0, 128):
                        # If it's selected, unselect it.
                        if zlb.IsSelected(i) and i != self.zplane_scrolled:
                            zlb.Select(i, on=0)
                        # If not, pass.
                        elif zlb.IsSelected(i) and i == self.zplane_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            zlb.Select(self.zplane_scrolled, on=1)
                    # self.pianorollpanel.actorsctrlpanel.actorsListBox.Select
                elif event.GetWheelRotation() <= -120:
                    if self.zplane_scrolled == 127:
                        pass
                    else:
                        self.zplane_scrolled += 1
                    print("Zplane Scrolled -->", self.zplane_scrolled)
                    zlb.Select(self.zplane_scrolled)
                    zlb.Focus(self.zplane_scrolled)
                    #1*
                    for i in range(0, 128):
                        # If it's selected, unselect it.
                        if zlb.IsSelected(i) and i != self.zplane_scrolled:
                            zlb.Select(i, on=0)
                        # If not, pass.
                        elif zlb.IsSelected(i) and i == self.zplane_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            zlb.Select(self.zplane_scrolled, on=1)

            else:  #RELEASE SHIFT, SCROLL ONE MORE TIME HERE, IN EITHER DIRECTION, TO ACTIVATE.
                #TODO SCROLL UP FOR ACTOR? SCROLL DOWN FOR ZPLANE? Brilliant....
                #Correct Highlight all.
                self.IsActorScrolling = False
                self.IsZPlaneScrolling = False
                #alb = self.pianorollpanel.actorsctrlpanel.actorsListBox

                #While holding, scroll up once to activate new actor.
                if event.GetWheelRotation() >= 120:
                    alb.Activate_Actor(self.actor_scrolled)
                    #if not self.IsActorScrolling:
                    # print(f"actor = {self.actor_scrolled}")
                    # self.mayavi_view.cur_ActorIndex = self.actor_scrolled
                    # self.mayavi_view.cur_z = self.mayavi_view.actors[self.actor_scrolled].cur_z
                    # self.mayavi_view.cur_changed_flag = not self.mayavi_view.cur_changed_flag
                    # self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

                #zlb = self.pianorollpanel.Zplanesctrlpanel.actorsListBox
                #While holding, scroll up once to activate new zplane.
                elif event.GetWheelRotation() <= -120:
                    zlb.Activate_Zplane(self.zplane_scrolled)
                    #if not self.IsZPlaneScrolling:
                    # print(f"zplane = {self.zplane_scrolled}")
                    # self.GetTopLevelParent().pianorollpanel.currentZplane = self.zplane_scrolled
                    # self.GetTopLevelParent().mayavi_view.cur_z = self.zplane_scrolled
                    # self.GetTopLevelParent().mayavi_view.CurrentActor().cur_z = self.zplane_scrolled
                    # self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

                #TODO Is this used?
                 # elif wx.GetMouseState().MiddleIsDown():
                #
                #     print("Middle-click zooming...")
                #     self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None,
                #                                        carry_to_z=True, array=False)

        event.Skip()


    def PrintOurCell(self, event):
        print("Our_X", event.Col)
        print("Our_Y", event.Row)
        event.Skip()

    def OnMiddleClickGrabNSend(self, event):
        #TODO Doc strings.
        #print("Middle-click zooming2...")
        state = wx.GetMouseState()
        #state2 = wx.KeyboardState()
        #print("State", state)
        #print("MiddleDown?", state.MiddleIsDown())
        #TODO Consider other binding gates, instead of CTRL ALT SHIFT.

        #Send selected notes to self.actor_scrolled.  Works
        if event.GetKeyCode() == wx.WXK_SHIFT and state.MiddleIsDown():
            print("Sending to scrolled Actor-->Shift and Middle down here.")
            # if self.actor_scrolled == self.mayavi_view.cur_ActorIndex and self.zplane_scrolled == self.mayavi_view.CurrentActor().cur_z and self.pianorollpanel.last_push == self.mayavi_view.CurrentActor().cur_z:
            self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None, carry_to_z=True, carry_to_actor=True, array=False)
            # else:
                #self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None, carry_to_z=False, carry_to_actor=True, array=False)
                # print("Here, actor true, z false.")
        #Send selected notes to self.zplane_scrolled.  Works
        elif event.GetKeyCode() == wx.WXK_ALT and state.MiddleIsDown():
            print("Sending to scrolled Zplane-->Alt and Middle down here.")
            self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None, carry_to_z=True, array=False)
            #TODO Attribute error expection here. Write.

        #Send selected notes to the pyshell as an np.array and as a music21.stream.Stream.
        elif event.GetKeyCode() == wx.WXK_CONTROL and state.MiddleIsDown():
            #TODO Send selected_notes to pyshell.
            self.pianorollpanel.ArrayFromSelection(self.pianorollpanel.selected_notes, scroll_value=self.zplane_scrolled, carry=True)
            self.selection_print = "Selection sent here to the pyshell as variables Midas_Array and Midas_Stream.\n Midas_Array is an np.array.\n Midas_Stream is a music21.stream.Stream()."
            self.pyshellpanel.shell.Execute("Midas_Array = Midas.pianorollpanel.selection_array")
            self.pyshellpanel.shell.Execute("Midas_Stream = midiart3D.extract_xyz_coordinates_to_stream(Midas.pianorollpanel.ArrayFromSelection(Midas.pianorollpanel.selected_notes, scroll_value=Midas.zplane_scrolled, carry=True))")

            self.pyshellpanel.shell.Execute("print(Midas_Array)")
            #self.pyshellpanel.shell.Execute("print(Midas_Stream)")
            self.pyshellpanel.shell.Execute("Midas_Stream.show('txt')")
            self.pyshellpanel.shell.Execute("""print(Midas.selection_print)""")

        #Send selected notes to the selected mouse coordinate on the grid upon pressing 'F'.
        elif event.GetUnicodeKey() == ord("F") and state.MiddleIsDown():
            print("Sending to Mouse Focus--> 'F' and Middle down here.")

            ####Method
            #Get Transforming value
            cell = self.pianorollpanel.pianoroll.GetCellFromMouseState()

            print("SELECTED_NOTES before loss", self.pianorollpanel.selected_notes)
            assert not not self.pianorollpanel.selected_notes, "You do not have selected_notes yet."

            #Get Selection
            #selected_notes = self.pianorollpanel.selected_notes


            #Transform the grid selection block as well as our self.selected_notes
            top_left = self.pianorollpanel.pianoroll.GetSelectionBlockTopLeft()
            bottom_right = self.pianorollpanel.pianoroll.GetSelectionBlockBottomRight()

            #The difference between our selection top_left and our target new location is our 'transform_value'.
            transform_value = (int(top_left[0][0]) - int(cell[0]), int(top_left[0][1]) - int(cell[1]))  #THIS WAY, we only have to ADD target times -1
            #without boolean condition gates.
            #(2, 2) - (4, 4) = (-2, -2) Moving down and right we multiple by negative 1.
            #(2, 2) - (0, 0) = (2, 2)   Moving up and left, we still multiply by negative 1.

            if not self.pianorollpanel.last_highlight:
                last_highlight = self.pianorollpanel.previously_selected_cells
            else:
                last_highlight = self.pianorollpanel.last_highlight

            #Transform here--
            notes_being_transformed = list()
            for i in self.pianorollpanel.selected_notes:
                new_tuple = (i[0] + (-1 * transform_value[0]), i[1] + (-1 * transform_value[1]))
                notes_being_transformed.append(new_tuple)

            #Core
            selected_notes = notes_being_transformed
            new_top_left = (top_left[0][0] + (-1 * transform_value[0]), top_left[0][1] + (-1 * transform_value[1]))
            new_bottom_right = (bottom_right[0][0] + (-1 * transform_value[0]), bottom_right[0][1] + (-1 * transform_value[1]))

            #self.pianorollpanel.selection_array[0] = self.pianorollpanel.selection_array[0] + cell[1]
            #self.pianorollpanel.selection_array[1] = self.pianorollpanel.selection_array[1] + cell[0]


            #Selection To Array
            selection_array = self.pianorollpanel.ArrayFromSelection(selected_notes, self.mayavi_view.CurrentActor().cur_z, carry=True)



            print("TRANSFORMED_SELECTION_ARRAY", self.pianorollpanel.selection_array)


            #Perform send.  Note: MAKE SURE THAT, if array=TRUE, that you are actually using an array as your input.
            self.pianorollpanel.Selection_Send(selection_array,
                                        self.mayavi_view.CurrentActor().cur_z, event=None, carry_to_z=True, array=True, transform_xy=True)

            print("Last Highlight", last_highlight)

            self.pianorollpanel.clear_out_highlight(event=None, manual_selection=last_highlight, manual=True)
            self.pianorollpanel.pianoroll.GoToCell(new_top_left)
            self.pianorollpanel.pianoroll.SelectBlock(new_top_left, new_bottom_right)

            print("SELECTED_NOTES before loss2", self.pianorollpanel.selected_notes)
            self.pianorollpanel.last_highlight = self.pianorollpanel.selecting_cells
            self.pianorollpanel.selected_notes = selected_notes

            #self.pianorollpanel.previously_selected_cells = self.pianorollpanel.selected_cells
            print("SELECTED_NOTES before loss3", self.pianorollpanel.selected_notes)


        else:
            event.Skip()


    def ShowCurrents(self):
        print("###For Selection functions:")
        try:
            print("Currently Selected Notes -->", self.pianorollpanel.selected_notes)
        except AttributeError as i:
            #print(i)
            print("Currently Selected Notes -->", "   ___no selected notes___")
        try:
            print("Last push -->", self.pianorollpanel.last_push)
        except AttributeError as i:
            print("Last push -->", "   ---no last push yet---")
        try:
            print("Last actor -->", self.pianorollpanel.last_actor)
        except AttributeError as i:
            print("Last actor -->", "   ---no last actor yet---")
        print("\n")
        print("###For all else:")
        if self.mayavi_view.previous_ActorIndex == None:
            print("Previous_ActorIndex -->", "   ---no previous actor_index yet---")
        else:
            print("Previous_ActorIndex -->", self.mayavi_view.previous_ActorIndex)

        if self.mayavi_view.CurrentActor().previous_z == None:
            print("Previous_ZPlane -->", "   ---no previous_z yet")
        else:
            print("Previous_ZPlane -->", self.mayavi_view.CurrentActor().previous_z)
        print("\n")
        print("Current M_V Actor           -->", self.mayavi_view.cur_ActorIndex)
        print("Current M_V zplane      -->", self.mayavi_view.cur_z)
        print("Current Actors zplane    -->", self.mayavi_view.CurrentActor().cur_z, "Note: Synced one way to ---> M_V zplane")
        print("\n")
        print("Current actor_scrolled  -->", self.actor_scrolled)  #TODO Should self.actor_scrolled anad zplane_scrolled go inside the actor class?
        print("Current zplane_scrolled -->", self.zplane_scrolled)



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
        #Necessary Startup stuff.
        self.mayavi_view.cur_z = 90
        self.mayavi_view.grid_reticle.mlab_source.points = self.mayavi_view.initial_reticle

        #Actor and Zplane scrolling attributes.
        self.zplane_scrolled = 90
        self.actor_scrolled = 0
        # self.IsActorScrolling = False
        # self.IsZPlaneScrolling = False

        #Accelerator table additions:
        #self.mainbuttonspanel.AccelerateMainButtons_Keys()


    def _do_layout(self):
        #self.mainbuttons_stats_split.SplitHorizontally(self.mainbuttonspanel, self.statsdisplaypanel)
        #self.pianoroll_mainbuttons_split.SplitVertically(self.mainbuttons_stats_split, self.pianorollpanel)
        self.pianoroll_mainbuttons_split.SplitVertically(self.mainbuttonspanel, self.pianorollpanel)
        self.top_pyshell_split.SplitHorizontally(self.pianoroll_mainbuttons_split, self.pyshellpanel)
        self.top_mayaviview_split.SplitHorizontally(self.top_pyshell_split, self.mayaviviewcontrolpanel)
        
        self.pianoroll_mainbuttons_split.SetSashPosition(120)
        #self.mainbuttons_stats_split.SetSashPosition(400)
        self.top_pyshell_split.SetSashPosition(306)  ## 2 Octaves are in view perfectly with this setting.
        self.top_mayaviview_split.SetSashPosition(600)  ###Affects 3D title insert
        
        self.top_mayaviview_split.SetSashGravity(0.5)
        self.top_pyshell_split.SetSashGravity(0.5)

        # Titles.
        self.mayavi_view.insert_titles()

        # Actor on startup.
        self.pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(0)
        self.pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(1)
        self.mayavi_view.actors[0].change_points(MusicObjects.earth())
        self.mayavi_view.actors[0].color = (1, 0, 0)        #For easy testing.

        #self.mayavi_view.sources[0].actor.property.color = (0, 1., .75)


        #Shows the zplanes on startup.
        self.pianorollpanel.zplanesctrlpanel.OnBtnShowAll(event=None)


        #These give the user 'F" hotkey control from any panel.
        #self.menuBar.AccelerateHotkeys()
        self.mainbuttonspanel.AccelerateHotkeys()
        self.pianorollpanel.actorsctrlpanel.actorsListBox.AccelerateHotkeys()
        self.pianorollpanel.zplanesctrlpanel.ZPlanesListBox.AccelerateHotkeys()
        self.pianorollpanel.pianoroll.AccelerateHotkeys()
        self.pyshellpanel.AccelerateHotkeys()
        self.mayavi_view.AccelerateHotkeys()


        self.mainpanel.Layout()
        self.Layout()



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    #Musical_Matrix_Rain.rain_execute()
    ## time.sleep(5)
    # splash = MySplashScreen()
    # splash.Show()
    app = wx.App()
    print(type(app))
    Midas = MainWindow(None, -1, "MIDAS")
    Midas.mainbuttonspanel.SetFocus()
    #frm.Show()
    # time.sleep(1.2)
    app.MainLoop()



    #frm.mayavi_view.configure_traits()
   # mlab.show()

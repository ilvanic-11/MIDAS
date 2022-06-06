import wx
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from gui import MenuButtons, MainButtons, PianoRollPanel, Musical_Matrix_Rain #Preferences
from wx.adv import SplashScreen as SplashScreen
#from mayavi3D import Mayavi3idiArtAnimation
from mayavi3D import Mayavi3DWindow, MusicObjects
from gui import StatusBar
import numpy as np
import pyo
import os
import gc
import sys
import wx._adv, wx._html, wx._xml, wx.py, time
import threading
import multiprocessing
import logging

#from logging import log
# import mayavi
# from mayavi import mlab
# from mayavi import plugins
# from mayavi.plugins import envisage_engine
# from mayavi.api import Engine
# from traits.trait_types import Function
# from traits.trait_types import Method
# import copy
#pyo.PYO_USE_WX = False
# from gui.Playback import Player
#from demo import images
# explicitly importing these so pyInstaller works

# from traits.api import HasTraits
# from midas_scripts import musicode   ###, midiart3D



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


        self.musicode = None
        #self.musicode = musicode.Musicode()

        #Named with an underscore because it's not actually a "panel" as below; it is a class called often from pycrust.
        self.mayavi_view = Mayavi3DWindow.Mayavi3idiView(self)

        self.server = pyo.Server()
        self.planescroll_animator = None
        self.player = None

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

        self.SetIcon(self.icon)

        #Status Bar
        self.statusbar = StatusBar.CustomStatusBar(self)
        self.SetStatusBar(self.statusbar)

        #This was messing up size stuff.
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
        self.Maximize(True)

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

        # self.pyshellpanel.shell.SetScrollPos(wx.VERTICAL, 29)
        # self.pyshellpanel.shell.SetEdgeColour("green")

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
        self.mayavi_view.scene3d.disable_render=True

        # TEMPORARY STUFF
        if self.mayavi_view.volume_slice:
            self.ipw = self.mayavi_view.image_plane_widget.ipw
            self.ipw2 = None
        else:
            self.ipw = self.mayavi_view.slice.actor.actor
            self.ipw2 = self.mayavi_view.slice_edges.actor.actor


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

                #Scrolling up, decreasing in value.
                if event.GetWheelRotation() >= 120:
                    #if self.actor_scrolled == 0:
                    if self.actor_scrolled == alb.filter[0]:   #First in the filter list, we don't go past it.
                        pass
                    else:
                        self.actor_scrolled = alb.filter[alb.filter.index(self.actor_scrolled) - 1]
                        #self.actor_scrolled -= 1
                    print("Actor Scrolled -->", self.actor_scrolled)
                    alb.Select(self.actor_scrolled)
                    alb.Focus(self.actor_scrolled)
                    #1*
                    #HERE

                    for i in alb.filter:
                        # If it's already selected, unselect it.
                        if alb.IsSelected(i) and i != self.actor_scrolled:
                            alb.Select(i, on=0)
                        # If not, pass.
                        elif alb.IsSelected(i) and i == self.actor_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            alb.Select(self.actor_scrolled, on=1)
                    # self.pianorollpanel.actorsctrlpanel.actorsListBox.Select

                #Scrolling down, increasing in value
                elif event.GetWheelRotation() <= -120:
                    #if self.actor_scrolled == alb.GetItemCount() - 1:
                    if self.actor_scrolled == alb.filter[-1]:   #Last in the filter list, we don't go past it.
                        pass
                    else:
                        self.actor_scrolled = alb.filter[alb.filter.index(self.actor_scrolled) + 1]
                        #self.actor_scrolled += 1
                    print("Actor Scrolled -->", self.actor_scrolled)
                    alb.Select(self.actor_scrolled)
                    alb.Focus(self.actor_scrolled)
                    #1*
                    #HERE

                    for i in alb.filter:
                        # If it's already selected, unselect it.
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

                #Scrolling up, decreasing in value.
                if event.GetWheelRotation() >= 120:
                    #if self.zplane_scrolled == 0:
                    if self.zplane_scrolled == zlb.filter[0]:  #First in the filter list, we don't go past it.
                        pass
                    else:
                        #say, from 90 to 95
                        self.zplane_scrolled = zlb.filter[zlb.filter.index(self.zplane_scrolled) - 1]
                        #self.zplane_scrolled -= 1
                    print("Zplane Scrolled -->", self.zplane_scrolled)
                    zlb.Select(self.zplane_scrolled)
                    zlb.Focus(self.zplane_scrolled)
                    #1*
                    #HERE

                    for i in zlb.filter:
                        # If it's already selected, unselect it.
                        if zlb.IsSelected(i) and i != self.zplane_scrolled:
                            zlb.Select(i, on=0)
                        # If not, pass.
                        elif zlb.IsSelected(i) and i == self.zplane_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            zlb.Select(self.zplane_scrolled, on=1)
                            #GREEN HERE
                            if self.mayavi_view.quick_plane:  #TODO Create option to turn off.
                                self.mayavi_view.highlighter_calls[0].actor.actor.trait_set(position=np.array([0., 0., self.zplane_scrolled]))

                                # if self.mayavi_view.volume_slice:
                                #     self.ipw.trait_set(slice_position=self.zplane_scrolled)  ##ipw.position = i  #/i_div
                                #     # self.scene3d.disable_render=False
                                #
                                # else:
                                #     pos = np.array([self.zplane_scrolled, 0, 0])
                                #     self.ipw.trait_set(position=pos)
                                #     self.ipw2.trait_set(position=pos)


                #Scrolling down, increasing in value.
                elif event.GetWheelRotation() <= -120:
                    #if self.zplane_scrolled == 127:
                    if self.zplane_scrolled == zlb.filter[-1]:  #Last in the filter list, we don't go past it.
                        pass
                    else:
                    #From, say, 90 to 95
                        self.zplane_scrolled = zlb.filter[zlb.filter.index(self.zplane_scrolled) + 1] #The next one.
                        #self.zplane_scrolled += 1
                    #print("Zplane Scrolled -->", self.zplane_scrolled)
                    zlb.Select(self.zplane_scrolled)
                    zlb.Focus(self.zplane_scrolled)
                    #1*
                    #HERE

                    for i in zlb.filter:
                        # If it's already selected, unselect it.
                        if zlb.IsSelected(i) and i != self.zplane_scrolled:
                            zlb.Select(i, on=0)
                        # If not, pass.
                        elif zlb.IsSelected(i) and i == self.zplane_scrolled:
                            pass
                        #Else, select the current.
                        else:
                            zlb.Select(self.zplane_scrolled, on=1)
                            #GREEN HERE
                            if self.mayavi_view.quick_plane:
                                self.mayavi_view.highlighter_calls[0].actor.actor.trait_set(position = np.array([0., 0., self.zplane_scrolled]))

                                # if self.mayavi_view.volume_slice:
                                #     self.ipw.trait_set(slice_position=self.zplane_scrolled)  ##ipw.position = i  #/i_div
                                #     # self.scene3d.disable_render=False
                                #
                                # else:
                                #     pos = np.array([self.zplane_scrolled, 0, 0])
                                #     self.ipw.trait_set(position=pos)
                                #     self.ipw2.trait_set(position=pos)



            else:  #RELEASE SHIFT, SCROLL ONE MORE TIME HERE, IN EITHER DIRECTION, TO ACTIVATE.
                #TODO SCROLL UP FOR ACTOR? SCROLL DOWN FOR ZPLANE? Brilliant....
                #Correct Highlight all.
                self.IsActorScrolling = False
                self.IsZPlaneScrolling = False


                #While holding, scroll up once to activate new actor.
                if event.GetWheelRotation() >= 120:
                    alb.Activate_Actor(self.actor_scrolled)

                #While holding, scroll up once to activate new zplane.
                elif event.GetWheelRotation() <= -120:
                    zlb.Activate_Zplane(self.zplane_scrolled)

        self.mayavi_view.scene3d.disable_render=False
        event.Skip()


    def PrintOurCell(self, event):
        #print("Our_X", event.Row)
        #print("Our_Y", event.Col)
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
            #print("Sending to scrolled Actor-->Shift and Middle down here.")
            #pass
            self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None, carry_to_z=True, carry_to_actor=True, array=False)

        #Send selected notes to self.zplane_scrolled.  Works
        elif event.GetKeyCode() == wx.WXK_ALT and state.MiddleIsDown():
            #print("Sending to scrolled Zplane-->Alt and Middle down here.")
            self.pianorollpanel.Selection_Send(self.pianorollpanel.selected_notes, self.zplane_scrolled, event=None, carry_to_z=True, array=False)
            #TODO Attribute error expection here. Write.

        #Send selected notes to the pyshell as an np.array and as a music21.stream.Stream.
        elif event.GetKeyCode() == wx.WXK_CONTROL and state.MiddleIsDown():
            #TODO Send selected_notes to pyshell.
            self.pianorollpanel.ArrayFromSelection(self.pianorollpanel.selected_notes, scroll_value=self.zplane_scrolled, carry=True)
            self.selection_print = "Selection sent here to the pyshell as variables Midas_Array and Midas_Stream.\n Midas_Array is an np.array.\n Midas_Stream is a music21.stream.Stream()."
            self.pyshellpanel.shell.Execute("Midas_Array = Midas.pianorollpanel.selection_array")
            self.pyshellpanel.shell.Execute("Midas_Stream = midiart3D.extract_xyz_coordinates_to_stream(Midas.pianorollpanel.ArrayFromSelection(Midas.pianorollpanel.selected_notes, scroll_value=Midas.zplane_scrolled, carry=True), durations=True)")

            self.pyshellpanel.shell.Execute("print(Midas_Array)")
            #self.pyshellpanel.shell.Execute("print(Midas_Stream)")
            self.pyshellpanel.shell.Execute("Midas_Stream.show('txt')")
            self.pyshellpanel.shell.Execute("""print(Midas.selection_print)""")

        #Send selected notes to the selected mouse coordinate on the grid upon pressing 'F'.
        elif event.GetUnicodeKey() == ord("F") and state.MiddleIsDown():
            #print("Sending to Mouse Focus--> 'F' and Middle down here.")

            ####Method
            #Get Transforming value
            target_cell = self.pianorollpanel.pianoroll.GetCellFromMouseState()

            #print("SELECTED_NOTES before loss", self.pianorollpanel.selected_notes)
            assert not not self.pianorollpanel.selected_notes, "You do not have selected_notes yet."

            #Get Selection
            #selected_notes = self.pianorollpanel.selected_notes


            #Transform the grid selection block as well as our self.selected_notes
            top_left = self.pianorollpanel.pianoroll.GetSelectionBlockTopLeft()
            bottom_right = self.pianorollpanel.pianoroll.GetSelectionBlockBottomRight()

            #The difference between our selection top_left and our target new location is our 'transform_value'.
            transform_value = (int(top_left[0][0]) - int(target_cell[0]), int(top_left[0][1]) - int(target_cell[1]))  #THIS WAY, we only have to ADD target times -1
                                                                                                        #without boolean condition gates.

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
            # Note: in the context of this example, (0,0) is topleft origin. (wx.grid stuff)
            ###
            # (2, 2) - (4, 4) = (-2, -2,) --> transformation difference.  Moving down and right we multiple target by negative 1.
            # (-2, -2) * -1 = (2, 2) --> transformation difference multiplied by negative 1.
            # (2, 2) + (2, 2) = (4,4) --> Result
            ###
            # (2, 2) - (0, 0) = (2, 2) --> transformation difference.  Moving up and left, we still multiply target by negative 1.
            # (2, 2) * -1 = (-2, -2,)
            # (2, 2) + (-2,-2) = (0,0)
            selected_notes = notes_being_transformed
            new_top_left = (top_left[0][0] + (-1 * transform_value[0]), top_left[0][1] + (-1 * transform_value[1]))
            new_bottom_right = (bottom_right[0][0] + (-1 * transform_value[0]), bottom_right[0][1] + (-1 * transform_value[1]))

            #self.pianorollpanel.selection_array[0] = self.pianorollpanel.selection_array[0] + cell[1]
            #self.pianorollpanel.selection_array[1] = self.pianorollpanel.selection_array[1] + cell[0]


            #Selection To Array
            selection_array = self.pianorollpanel.ArrayFromSelection(selected_notes, self.mayavi_view.CurrentActor().cur_z, carry=True)



            #print("TRANSFORMED_SELECTION_ARRAY", self.pianorollpanel.selection_array)


            #Perform send.  Note: MAKE SURE THAT, if array=TRUE, that you are actually using an array as your input.
            self.pianorollpanel.Selection_Send(selection_array,
                                               self.mayavi_view.CurrentActor().cur_z, event=None, carry_to_z=True, array=True, carry_to_current=True)

            #print("Last Highlight", last_highlight)

            self.pianorollpanel.clear_out_highlight(event=None, manual_selection=last_highlight, manual=True)
            self.pianorollpanel.pianoroll.GoToCell(new_top_left)
            self.pianorollpanel.pianoroll.SelectBlock(new_top_left, new_bottom_right)

            #print("SELECTED_NOTES before loss2", self.pianorollpanel.selected_notes)
            self.pianorollpanel.last_highlight = self.pianorollpanel.selecting_cells
            self.pianorollpanel.selected_notes = selected_notes

            #self.pianorollpanel.previously_selected_cells = self.pianorollpanel.selected_cells
            #print("SELECTED_NOTES before loss3", self.pianorollpanel.selected_notes)


        else:
            event.Skip()


    def ShowCurrents(self):
        print("###For Selection functions:")
        try:
            print("Currently Selected Notes -->", self.pianorollpanel.selected_notes)
        except AttributeError as i:
            #print(i)
            print("Currently Selected Notes    -->", "   ___no selected notes___")
        try:
            print("Last push -->", self.pianorollpanel.last_push)
        except AttributeError as i:
            print("Last push                   -->", "   ---no last push yet---")
        try:
            print("Last actor -->", self.pianorollpanel.last_actor)
        except AttributeError as i:
            print("Last actor                  -->", "   ---no last actor yet---")
        print("\n")
        print("###For all else:")
        if self.mayavi_view.previous_ActorIndex == None:
            print("Previous_ActorIndex         -->", "   ---no previous actor_index yet---")
        else:
            print("Previous_ActorIndex -->", self.mayavi_view.previous_ActorIndex)

        if self.mayavi_view.CurrentActor().previous_z == None:
            print("Previous_ZPlane             -->", "   ---no previous_z yet")
        else:
            print("Previous_ZPlane -->", self.mayavi_view.CurrentActor().previous_z)
        print("\n")
        print("Current M_V Actor           -->", self.mayavi_view.cur_ActorIndex)
        print("Current M_V zplane          -->", self.mayavi_view.cur_z)
        print("Current Actors zplane       -->", self.mayavi_view.CurrentActor().cur_z, "Note: Synced one way to ---> M_V zplane")
        print("\n")
        print("Current actor_scrolled      -->", self.actor_scrolled)  #TODO Should self.actor_scrolled anad zplane_scrolled go inside the actor class?
        print("Current zplane_scrolled     -->", self.zplane_scrolled)
        print("\n")
        print("Current palette name        -->", self.mayavi_view.current_palette_name)
        print("Current color palette       -->")
        print(self.mayavi_view.current_color_palette)
        print("Current mayavi palette      -->  #Note: R and B will appear swapped here, but this is handled in the workflows.") #12/03/2021
        print(self.mayavi_view.current_mayavi_palette)
        #TODO Change default to "current" with these last two names. 12/03/2021



    def clear_all_and_redraw(self):
        # TODO CLEAR ALL ACTOR"S AND ZPLANES AS WELL ---> 04/17/2021
        self.mayavi_view.scene3d.disable_render = True
        self.mayavi_view.scene3d.close()
        # mlab.clf()
        self.mayavi_view.mlab_calls.clear()
        self.mayavi_view.mlab_calls = []
        self.mayavi_view.sources.clear()            #Shut
        self.mayavi_view.sources.clear = []
        self.mayavi_view.highlighter_calls.clear()  #dahfuq
        self.mayavi_view.highlighter_calls.clear = []
        self.mayavi_view.text3d_calls.clear()       #up.
        self.mayavi_view.text3d_calls.clear = []
        self.mayavi_view.text3d_default_positions.clear()
        self.mayavi_view.text3d_default_positions = []
        self.mayavi_view.create_3dmidiart_display()
        self.mayavi_view.scene3d.disable_render = False
        # TODO Add delete_actors stuff here too. New Session function?! :)


    # TODO Redundant now?
    def redraw_mayaviview(self, event):
        self.mayavi_view.scene3d.disable_render = True
        self.mayavi_view.scene3d.mlab.clf()
        # self.scene3d.close()  #Be Careful with mlab.clf() 04/17/2021
        # self.scene3d = Instance(MlabSceneModel, ())
        # self.reset_traits(traits=["scene3d"])
        # self.engine.start()  # TODO What does this do?
        # self.scene = self.engine.scenes[0]
        # self.figure = self.scene3d.mayavi_scene
        self.mayavi_view.create_3dmidiart_display()
        self.mayavi_view.scene3d.disable_render = False
        # Set focus on mbp for fast use of "F" hotkeys.
        self.mainbuttonspanel.SetFocus()
        self.pianorollpanel.actorsctrlpanel.actorsListBox.Activate_Actor(
            self.mayavi_view.cur_ActorIndex)  # TODO Watch for cpqn bugs here. 04/17/2021


    def _delete_mayavi_views(self):
    #NOT meant to be used casually. This was intended to be the start of a chain of logic that solved a memory problem.

        """
        Warning: Executing this function will require a restart of Midas in order to continue using Midas.
        . Use only if you know what you are doing.

        This function DELETES all POINTERS\INSTAANCES of the Mayavi3idiView() class instantiated as  m_v throughout
        MIDAS. It was intended to solve a memory problem. The ONLY instance it doesn't delete is the main one here in
        our MainWindow class, self.mayavi_view; this is for confirmation purposes.

        NOTE: The referrence count will print "3" at the end, but note that there are TWO pointers within the scope of
        this function that don't get garbage collected themselves obviously until the interpreter has exited this
        function's scope. And since this function doesn't delete the main self.mayavi_view pointer, running
        sys.getrefcount(Midas.mayavi_view) in the pycrust, should return 2, which means there's only one left;
        the main one. (because 2 minus sys.getrefcounts()'s pointer == 1)

        #TODO Write sister function that restores all m_v's during mainloop running.
        :return:
        """
        try:
            ref_list = gc.get_referrers(self.mayavi_view) #Temp pointer here 1.
            del (self.pianorollpanel.m_v)
            del (self.pianorollpanel.pianoroll.m_v)
            del (self.menuBar.m_v)
            del (self.mainbuttonspanel.m_v)
            del (self.pianorollpanel.actorsctrlpanel.m_v)
            del (self.pianorollpanel.actorsctrlpanel.actorsListBox.m_v)
            del (self.pianorollpanel.zplanesctrlpanel.m_v)
            del (self.pianorollpanel.zplanesctrlpanel.ZPlanesListBox.m_v)
            # ref_list[1]['__sync_trait__']['cur_z']  #deletes a weakreference
            if len(Midas.mayavi_view.actors) != 0:
                for i in Midas.mayavi_view.actors:
                    del (i.m_v)

            deletion_list = ['object', 'default_value', '_traits_cache_context_object', '_object']  # 'mayavi_view' is last
            for i in range(0, len(ref_list)):
                for j in deletion_list:
                    try:
                        k = [x for x in ref_list[i].keys()]
                        if j in k:
                            del (ref_list[i][j])
                        else:
                            pass
                    except Exception as e:
                        print(e)
                        pass
            # print(ref_list[1])
            print("Ctrait?", [ref_list[5]])
            ctrait_ref_list = gc.get_referrers(ref_list[5])
            print("Ctrait_ref_list??", ctrait_ref_list)
            print("  --  ")
            print("Ctrait?", ctrait_ref_list[-1]['object'])
            print("Ctrait type?", type(ctrait_ref_list[-1]))
            assert ctrait_ref_list[-1]['object'] == ref_list[5], "Ctrait no match here."
            del (ctrait_ref_list[-1]['object'])
            print("Crait deleted.")
            count = sys.getrefcount(Midas.mayavi_view)  #Temp pointer here 2.
            print("Count", count)
            # del(Midas.mayavi_view)
            # count -=1
            print("Count", count)
        except TypeError as e:
            print("TypeError", e)
            return
        return count


    def zoom_to_coordinates(self, picker):
        print("PICKER", picker)
        print("PICKER_TYPE", type(picker))
        print("Point", picker.point_id)
        picker.tolerance = 0.01
        picked = picker.actors
        print("Picked", picked)
        #print(picker.trait_names())
        print("Selection Point:", picker.pick_position)

        mproll = self.pianorollpanel.pianoroll

        self.ret_x = picker.pick_position[0] * self.mayavi_view.cpqn  ######Account for cpqn here.
        self.ret_y = picker.pick_position[1]
        self.ret_z = picker.pick_position[2]

        #In scrollunits, which should == to pixels.

        #TODO..Conversions for cells, coords, and scrollunits?
        #10 pixels per cell
        #ScrollRate = Pixels/Scrollunit

        #Pixels to Cell --- User Grid.XYToCell()
        #Cell to Pixels -- Cell Row\Col * 10

        #Cell to ScrollUnits -- Cell * 10 / ScrollRate
        #Measure to ScrollUnits -- Measure * (Cell * PixelsperCell-->10 * CellsperMeasure-->(timesig_numerator*cellsperqrtrnote))

        #Cell to Mayavi_Coords --  Synced as ints.
        #MayaviCoords to Cell -- Synced as ints.

        #( 160 * 10) / (160 / 4 * (4 * 10)
        self.cur_scroll_x = (int(self.ret_x) *10) / mproll.GetScrollPixelsPerUnit()[0]  #Scrollrate / cells per measure #TODO CPQN FACTORED IN HERE -- Acounted for above.
        self.cur_scroll_y = ((127-int(self.ret_y)) * 10) / mproll.GetScrollPixelsPerUnit()[1]   #Scrollrate Y / cells per two octaves == 24

        #TODO Fix this limit cap.
        if self.cur_scroll_y > 1040:   #Caps off scrolling at the bottom, so the rectangle doesn't go funky.
            self.cur_scroll_y = 1040    #Sash position affects this because num of pixels in client view relates to ViewStart().

        print("Coord", self.ret_x, self.ret_y, self.ret_z)
        if mproll is not None:

            #Zooms on middle click.  #TODO Math is not exact yet...
            mproll.Scroll(self.cur_scroll_x, self.cur_scroll_y)
            self.mayavi_view.new_reticle_box()
        else:
            pass


    def _set_properties(self):
        self.SetTitle("MIDAS")

        #COLORS
        self.SetBackgroundColour("green")
        self.SetForegroundColour("green")
        self.pianorollpanel.SetBackgroundColour("white")
        #self.statsdisplaypanel.SetBackgroundColour("silver")
        self.mainbuttonspanel.SetBackgroundColour("white")
        self.top_pyshell_split.SetBackgroundColour("black")

        #TODO Put button color setting here?

        self.top_pyshell_split.SetMinimumPaneSize(50)
        self.pianoroll_mainbuttons_split.SetMinimumPaneSize(120)
        #self.mainbuttons_stats_split.SetMinimumPaneSize(200)
        self.top_mayaviview_split.SetMinimumPaneSize(50)

        #TODO Put somewhere else?
        #Necessary Startup stuff.
        self.mayavi_view.cur_z = 90

        #This call "catches up" the updating of reticle points (it's complicated, a stupid bug).
        #self.mayavi_view.grid_reticle.mlab_source.points = self.mayavi_view.initial_reticle

        #Startup position for red reticle.
        self.mayavi_view.set_grid_reticle_position(z=[0., 0., 90.])

        # Actor and Zplane scrolling attributes.
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

        #self.pyshellpanel.shell.SetBackgroundColour("green")

        # Titles.
        self.mayavi_view.insert_titles()

        self.pianorollpanel.actorsctrlpanel.actorsListBox.filter = [0]

        # Actors on startup.
        self.pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(0)
        #self.pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(1)
        self.mayavi_view.actors[0].change_points(MusicObjects.earth())
        #self.mayavi_view.actors[0].color = (1, 0, 0)        #For easy testing.
        self.mayavi_view.sources[0].actor.property.color = (0, 1., .75)


        #Unless written differently, this call needs to happen after we have actors instantiated; would other wise be
        #in _set_properties.
        #Show the actors on startup, and update actorsListBox.filter.
        self.pianorollpanel.actorsctrlpanel.OnBtnToggleAll(event=None)
        #Shows the zplanes on startup and update ZPlanesListBox.filter
        self.pianorollpanel.zplanesctrlpanel.OnBtnShowAll(event=None)


        #These give the user 'F" hotkey control from any 'panel'.
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
    #from resources.Midas_Startup_Configs import Startup

    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.

    app = wx.App()

    splash = MySplashScreen()
    splash.Show()
    time.sleep(4) #3, #5
    splash.DestroyLater()
    time.sleep(.2)

    #threading.Thread(target=Musical_Matrix_Rain.rain_execute).start()
    #Musical_Matrix_Rain.rain_execute()
    rain = multiprocessing.Process(target=Musical_Matrix_Rain.rain_execute)
    rain.start()
    time.sleep(4) #.3

    Midas = MainWindow(None, -1, "MIDAS")
    #Midas.mainbuttonspanel.SetFocus()

    #Startup = Startup()
    #Midas.pyshellpanel.shell.GotoPos(29)

    #frm.Show()
    time.sleep(1.75)

    #threading.Thread(target=app.MainLoop).start()
    #multiprocessing.Process(target=app.MainLoop).start()

    app.MainLoop()

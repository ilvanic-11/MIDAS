import wx
from midas_scripts import midiart, midiart3D, musicode, music21funcs
from gui import Generate
import music21
import cv2, numpy
import os
import shutil
from collections import OrderedDict
from mayavi3D.Mayavi3DWindow import Mayavi3idiView, MayaviMiniView
from time import sleep
import copy

import gc

import traceback

# from gui import Preferences
# from mayavi import mlab
# import numpy as np
# import subprocess
# import random
# from gui.Preferences import ListCtrlComboPopup

class MainButtonsPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        self.musicode = None  #Not necessary, but I'll leave for now. 04/18/2021

        self.toplevel = parent.GetTopLevelParent()

        # mayavi_view reference
        self.m_v = self.toplevel.mayavi_view

        self.main_buttons_sizer = wx.BoxSizer(wx.VERTICAL)

        #btn_midi_import.
        #self.btn_Music21_Converter_Parse = wx.Button(self, -1, "Midi\Score \n Import", size=(75, 36))
        # self.btn_Music21_Converter_Parse = wx.Button(self, -1, "Midi\Score \n Import", size=(75, 36))
        # self.btn_Music21_Converter_Parse.SetBackgroundColour((200, 150, 200, 255))
        # # btn_Music21_Converter_Parse.SetForegroundColour((255, 255, 255, 255))
        # self.main_buttons_sizer.Add(self.btn_Music21_Converter_Parse, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        # self.Bind(wx.EVT_BUTTON, self.OnMusic21ConverterParseDialog, self.btn_Music21_Converter_Parse)
        # self.midi_TT = wx.ToolTip("Import Midi\Score files.")
        #self.btn_The_Midas_Button.SetToolTip(self.midi_TT)

        #btn_midas_operations
        self.btn_The_Midas_Button = wx.Button(self, -1, "Midas", size=(75, 30)) #36
        self.btn_The_Midas_Button.SetBackgroundColour((200, 150, 200, 255))
        #btn_Music21_Converter_Parse.SetForegroundColour((255, 255, 255, 255))
        self.main_buttons_sizer.Add(self.btn_The_Midas_Button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnTheMidasButtonDialog, self.btn_The_Midas_Button)
        self.midi_TT = wx.ToolTip("Musicologically operate on a directory of midi files "
                                  "as well as imported lists of music21 streams. "
                                  "This button will also do basic imports of midi and score files into Midas_wx.")
        #self.midi_TT = wx.ToolTip("Import Midi\Score files.")
        self.btn_The_Midas_Button.SetToolTip(self.midi_TT)


        #btn_musicode.
        self.btn_musicode = wx.Button(self, -1, "Musicode") #, size=(75, 30))
        self.btn_musicode.SetBackgroundColour((0, 150, 255, 255))
        self.main_buttons_sizer.Add(self.btn_musicode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMusicodeDialog, self.btn_musicode)
        self.musicode_TT = wx.ToolTip("Turn text into music.")
        self.btn_musicode.SetToolTip(self.musicode_TT)

        #btn_midiart.
        self.btn_MIDIart = wx.Button(self, -1, "MidiArt") #, size=(75, 30))  #MIDI Art
        self.btn_MIDIart.SetBackgroundColour((0, 222, 70, 255))
        self.main_buttons_sizer.Add(self.btn_MIDIart, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArtDialog, self.btn_MIDIart)
        self.midiart_TT = wx.ToolTip("Turn pictures into music.")
        self.btn_MIDIart.SetToolTip(self.midiart_TT)

        #btn_midiart3D.
        self.btn_MIDIart3D = wx.Button(self, -1, "3iDiArt") #, size=(75, 30))  #3IDI Art
        self.btn_MIDIart3D.SetBackgroundColour((222, 222, 0, 255))
        self.main_buttons_sizer.Add(self.btn_MIDIart3D, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArt3DDialog, self.btn_MIDIart3D)
        self.midiart3D_TT = wx.ToolTip("Turn point clouds\\3D scans into music.")
        self.btn_MIDIart3D.SetToolTip(self.midiart3D_TT)

        # btn_show_in_FLStudio = wx.Button(self, -1, "Show in FLStudio")
        # sizer.Add(btn_show_in_FLStudio, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinFLStudio, btn_show_in_FLStudio)

        # btn_show_in_MuseScore = wx.Button(self, -1, "Show in MuseScore")
        # sizer.Add(btn_show_in_MuseScore, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinMuseScore, btn_show_in_MuseScore)

        # btn_show_stream_txt = wx.Button(self, -1, "Show Stream Text")
        # sizer.Add(btn_show_stream_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowStreamTxt, btn_show_stream_txt)

        # self.btn_update_stream = wx.Button(self, -1, "Update Stream")
        # self.main_buttons_sizer.Add(self.btn_update_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        # self.Bind(wx.EVT_BUTTON, self.OnUpdateStream, self.btn_update_stream)

        self.btn_clear_pianoroll = wx.Button(self, -1, "Clear PianoRoll")
        #btn_clear_pianoroll.SetBackgroundColour((255, 230, 200, 255))
        self.main_buttons_sizer.Add(self.btn_clear_pianoroll, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.OnClearPianoRoll, self.btn_clear_pianoroll)
        self.clear_proll_TT = wx.ToolTip("Clear all notes within the red reticle, the viewable area of the pianoroll. #TODO!!!!!")
        self.btn_clear_pianoroll.SetToolTip(self.clear_proll_TT)


        self.btn_clear_zplane = wx.Button(self, -1, "Clear Z_Plane")
        #btn_clear_pianoroll.SetBackgroundColour((255, 230, 200, 255))
        self.main_buttons_sizer.Add(self.btn_clear_zplane, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.OnClearZPlane, self.btn_clear_zplane)
        self.clear_zplane_TT = wx.ToolTip("Clear the entirety of notes within the current zplane.")
        self.btn_clear_zplane.SetToolTip(self.clear_zplane_TT)

        self.btn_redraw_mayaviview = wx.Button(self, -1, "Redraw Mayavi \n View")
        self.main_buttons_sizer.Add(self.btn_redraw_mayaviview, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.GetTopLevelParent().redraw_mayaviview, self.btn_redraw_mayaviview)
        self.redraw_mv_TT = wx.ToolTip("Clears and redraws the 3-dimensional MayaviView below.")
        self.btn_redraw_mayaviview.SetToolTip(self.redraw_mv_TT)
        # btn_print_cell_sizes = wx.Button(self, -1, "Print Cell Sizes")
        # sizer.Add(btn_print_cell_sizes, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnPrintCellSizes , btn_print_cell_sizes)
        #
        # btn_grid_to_stream = wx.Button(self, -1, "Grid To Stream")
        # sizer.Add(btn_grid_to_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnGridToStream , btn_grid_to_stream)


        self.SetSizer(self.main_buttons_sizer)
        self.main_buttons_sizer.Fit(self)

        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnDialogClosed)

        #self.AccelerateHotkeys()
        self.SetFocus() #THIS HERE IS ACTUALLY THE STARTUP FOCUS.

        #Update user-generated name.
        # self.mc_dialog = MusicodeDialog()
        # self.mc_dialog.user_named = self.GetTopLevelParent().musicode.musicode_name


        # For a bug fix---------------
        #id = 7182389573431346  , id=id
        self.musicode_btn_colour = self.btn_musicode.GetBackgroundColour()
        self.btn_musicode.Bind(wx.EVT_ENTER_WINDOW, self.onMouseOver)
        self.btn_musicode.Bind(wx.EVT_LEAVE_WINDOW, self.onMouseLeave)


    # For a bug fix, had to be hardcoded *
    def onMouseOver(self, event):
        # mouseover changes colour of button
        self.btn_musicode.SetBackgroundColour((229, 241, 251, 255))
        event.Skip()


    def onMouseLeave(self, event=None):
        # mouse not over button, back to original colour
        self.btn_musicode.SetBackgroundColour(self.musicode_btn_colour)
        if event is not None:
            event.Skip()
    # #----------------------------


    def AccelerateHotkeys(self):

        entries = [wx.AcceleratorEntry() for i in range(0, 10)]

        #new_id0 = wx.NewIdRef()
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


        self.Bind(wx.EVT_MENU, self.OnTheMidasButtonDialog, id=new_id1)
        #self.Bind(wx.EVT_MENU, self.OnMusic21ConverterParseDialog, id=new_id1)
        self.Bind(wx.EVT_MENU, self.OnMusicodeDialog, id=new_id2)
        self.Bind(wx.EVT_MENU, self.OnMIDIArtDialog, id=new_id3)
        self.Bind(wx.EVT_MENU, self.OnMIDIArt3DDialog, id=new_id4)
        self.Bind(wx.EVT_MENU, self.focus_on_actors_listbox, id=new_id5)
        self.Bind(wx.EVT_MENU, self.focus_on_zplanes, id=new_id6)
        self.Bind(wx.EVT_MENU, self.focus_on_pianorollpanel, id=new_id7)
        self.Bind(wx.EVT_MENU, self.focus_on_pycrust, id=new_id8)
        self.Bind(wx.EVT_MENU, self.focus_on_mayavi_view, id=new_id9)
        self.GetTopLevelParent().mayaviviewcontrolpanel.Bind(wx.EVT_MENU,
                                                             self.GetTopLevelParent().mainbuttonspanel.focus_on_mainbuttonspanel, id=new_id10)

        #Shift into which gear.
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

    ##Focus Functions
    ###-----------------------


    def focus_on_actors_listbox(self, event):
        """
        This function binds to F5 and sets the user focus to the panel containing the pycrust python console.

        :return:
        """
        #print("Focusing on actorsListBox")

        self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.SetFocus()


    def focus_on_zplanes(self, event):
        """
        This function binds to F6 and sets the user focus to the panel containing the pycrust python console.

        :return:
        """
        #print("Focusing on ZPlanesListBox")

        self.GetTopLevelParent().pianorollpanel.zplanesctrlpanel.ZPlanesListBox.SetFocus()


    def focus_on_pianorollpanel(self, event):
        """
        This function binds to F7 and sets the user focus to the panel containing the pianoroll grid class.

        :return:
        """
        #print("Focusing on pianorollpanel")

        self.GetTopLevelParent().pianorollpanel.pianoroll.SetFocus()


    def focus_on_pycrust(self, event):
        """
        This function binds to F8 and sets the user focus to the panel containing the pycrust python console.

        :return:
        """
        #print("Focusing on pyshellpanel")

        self.GetTopLevelParent().pyshellpanel.SetFocus()


    def focus_on_mayavi_view(self, event):
        """
        This function binds to F9 and sets the user focus to the panel containing the mayavi visualization.
        :return:
        """
        #print("Focusing on mayavai_view_control_panel")

        self.GetTopLevelParent().mayaviviewcontrolpanel.SetFocus()


    def focus_on_mainbuttonspanel(self, event):
        """
        This function binds to F12 and sets the user focus to back to the mainbuttonspanel.
        NOTE: THIS IS KIND OF LIKE A HOME FEATURE; The rest of the hotkeys in this accelerator cannot be called unless the focus is already on the mainbuttons panel.
        #TODO Fix.
        :return:
        """

        #print("Focusing home on mainbuttonspanel.")

        self.SetFocus()
        #self.parent.mainbuttonspanel.SetFocus()

    ##--------------------------------------------------

    #TODO Redundant?
    def OnGridToStream(self, evt):
        self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream()


    def OnPrintCellSizes(self, evt):
        self.GetTopLevelParent().pianorollpanel.print_cell_sizes()


    def OnClearZPlane(self, evt):
        self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.GetTopLevelParent().pianorollpanel.currentZplane)


    def OnClearPianoRoll(self, evt):
        pass

    # def OnDeleteAllPianoRolls(self, evt):
    #     self.GetTopLevelParent().


    def OnShowStreamTxt(self, evt):
        self.GetTopLevelParent().pianorollpanel.pianoroll.stream.show('txt')


    def OnMusic21ConverterParseDialog(self, evt):
        dlg = Music21ConverterParseDialog(self, -1, "       music21.converter.parse") #9 Spaces deliberate here.
        #dlg = Music21ConverterParseDialog(self, -1, "                                 The Midas Button") # Spaces deliberate here.
        dlg.ShowWindowModal()


    def OnTheMidasButtonDialog(self, evt):
        #dlg = Music21ConverterParseDialog(self, -1, "         music21.converter.parse") #9 Spaces deliberate here.
        dlg = TheMidasButtonDialog(self, -1, "                                     The Midas Button -- Load a midi or "
                                             "score file. Optionally, operate musicologically on global loads in memory"
                                             " or on a directory of midi files; this allows you to mass-apply "
                                             "Visual Music musicianship.")  # Spaces deliberate here.


        dlg.ShowWindowModal()


    def OnMusicodeDialog(self, evt):


        #TODO 06/28/2023 TEST THIS
        # print("CB_GETVALUE()", self.toplevel.pianorollpanel.cbCellsPerQrtrNote.GetValue())
        # if self.toplevel.pianorollpanel.cbCellsPerQrtrNote.GetValue() != "(4, '16th', .25)": #can't use 'is not' here...
        #     #THIS IS TEMPORARY; Once Durations are perfect, we can remove these two calls.
        #     self.toplevel.pianorollpanel.zplanesctrlpanel.OnGoToNearestEmptyZplane(event=None)
        #     sleep(.35)
        #     self.toplevel.pianorollpanel.cbCellsPerQrtrNote.SetValue("(4, '16th', .25)")
        #     sleep(.35)
        #     self.toplevel.pianorollpanel.OnCellsPerQrtrNoteChanged(event=None)
        #     sleep(.35)
        # else:
        #     pass

        dlg = MusicodeDialog(self, -1, "Musicode")
        dlg.ShowWindowModal()


    def OnMIDIArtDialog(self, evt):
        dlg = MIDIArtDialog(self, -1, "MidiArt")
        dlg.ShowWindowModal()


    def OnMIDIArt3DDialog(self, evt):
        dlg = MIDIArt3DDialog(self, -1, "3D MidiArt")
        dlg.ShowWindowModal()


    def OnDialogClosed(self, evt):
        dialog = evt.GetDialog()
        #print("Dialog closed")
        #print(type(dialog))
        if type(dialog) is TheMidasButtonDialog:
            self._OnTheMidasButtonDialogClosed(dialog, evt)
        if type(dialog) is MusicodeDialog:
            self._OnMusicodeDialogClosed(dialog, evt)
        elif type(dialog) is MIDIArtDialog:
            self._OnMIDIArtDialogClosed(dialog, evt)
        elif type(dialog) is Music21ConverterParseDialog:
            self._OnM21ConverterParseDialogClosed(dialog, evt)
        elif type(dialog) is MIDIArt3DDialog:
            self._OnMIDIArt3DDialogClosed(dialog, evt)
        dialog.Destroy()



    def _OnTheMidasButtonDialogClosed(self, dialog, evt):
        pass


    def _OnM21ConverterParseDialogClosed(self, dialog, evt):
        ###NOTE: BE MINDFUL OF YOUR CPQN

        print("OnM21ConverterParseDialogClosed():")
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        actor = len(self.m_v.actors) + 1
        if btn == "OK":



            m_v = self.GetTopLevelParent().mayavi_view
            color_palette = m_v.current_color_palette

            stream = music21.converter.parse(dialog.midi)
            stream.show('txt')
            #TODO CORE DATA UPDATE Here
            points = midiart3D.extract_xyz_coordinates_to_array(stream)
            index = len(m_v.actors) if dialog.chbxNewActor.IsChecked() is True else m_v.cur_ActorIndex
            name = str(index) + "_" + "Midi" + "_" + dialog.midi_name
            # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
            m_v.disable_render = True
            # New Actor Checkbox
            # self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(actor)
            actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)\
                if dialog.chbxNewActor.IsChecked() is True else None
            # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            for j in m_v.actors:
                if dialog.chbxNewActor.IsChecked() is True:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)
                else:
                    m_v.actors[index].change_points(points)
            m_v.disable_render = False
            #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            m_v.new_reticle_box()



    def _OnMusicodeDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        # New Actor Checkbox
        self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(len(self.m_v.actors)) \
            if dialog.chbxNewActor.IsChecked() is True else None

        musicode_name = dialog.input_mcname.GetLineText(0)

        if dialog.input_mcname.GetLineText(0) == "" or None:
            musicode_name = "User_Generated"

        shorthand_name = dialog.input_sh.GetLineText(0)
        if dialog.input_sh.GetLineText(0) == "" or None:
            shorthand_name = "ug"


        if dialog.create_musicode.GetValue() is True and btn == "OK":
            print("DialogCheck:", dialog.create_musicode.GetValue())
            stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream(update_actor=False)
            self.musicode.make_musicode(stream, musicode_name, shorthand_name, filepath=None,
                                        selection=str(dialog.inputTxt.GetLineText(0)), write=False, timeSig=None)
            self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.m_v.cur_z)

        elif dialog.create_musicode.GetValue() is False and btn == "OK":
            if dialog.translate_multiline_musicode.GetValue() is False:
                print("DialogCheck:", dialog.create_musicode.GetValue())
                stream = self.musicode.translate(
                    dialog.rdbtnMusicodeChoice.GetString(dialog.rdbtnMusicodeChoice.GetSelection()),
                    dialog.inputTxt.GetLineText(0))
                print("LINETEXT:", dialog.inputTxt.GetLineText(0))
                self.m_v.z_flag = True
                #Stream to Grid method
                self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                self.m_v.z_flag = False
                self.m_v.CurrentActor().array4Dchangedflag = not self.m_v.CurrentActor().array4Dchangedflag

            else:
                print("Modified?:", dialog.inputTxt.IsModified())
                if dialog.inputTxt.IsModified():
                    write_name = "Musicode_Modified"
                else:
                    try:
                        write_name = dialog.pathname
                    except Exception as e:
                        print("Traceback___Message:")
                        print(traceback.format_exc())
                        print(e)
                        print("Compensating...translate_multiline will use function default write name.")
                        write_name = "Multiline_Musicode_Write"

                string = dialog.inputTxt.GetValue()
                print("LINETEXT:", string)
                #Immediately write to file for all lines.
                self.musicode.translate_multiline(
                    dialog.rdbtnMusicodeChoice.GetString(dialog.rdbtnMusicodeChoice.GetSelection()),
                    string,
                    write=True,
                    write_name=write_name,
                    from_text_file=False)
        else:
            pass
        #pass
        dlg = super().GetParent().GetTopLevelParent().statusbar.gauge
        dlg.SetValue(0)



    def _OnMIDIArtDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)



        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        try:

            if btn == "OK":

                print(btn, "Button")

                print("mult", dialog.MultipleCheck)
                print("select", dialog.SelectCheck)
                print("all", dialog.AllCheck)

                #New Actor Checkbox
                #TODO Finish! 07/10/2023
                # self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(len(self.m_v.actors)) \
                #     if dialog.chbxNewActor.IsChecked() is True else None
                # NOTE: With monochrome and edges, new_actor is doable. With colors, the new_actor chbx needs to Disable()
                print("multcheck", dialog.MultipleCheck)

                if dialog.MultipleCheck:
                    # if dialog.SelectCheck and dialog.AllCheck:
                    #     print("DUCK1")
                    #     print("Pick one or the other.")
                    #     pass

                    #En Mass Export Directly to File.
                    if not dialog.SelectCheck and dialog.AllCheck:
                        ###Multiple of EVERY Color PER Image.
                        ##NOTE: Processing intensive; use wisely.

                        print("DUCK2")
                        #pathname = dialog.pathname
                        for i in dialog.pathnames:
                            num = 0
                            for j in range(0, dialog.listCtrl.ItemCount):
                                palette_name = dialog.listCtrl.GetItemText(j)
                                print("PALETTE_NAME!!!!:", palette_name)
                                # self.pathname = pathname
                                img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                                img2 = cv2.imread(i,
                                                  cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                                # height = MIDAS_Settings.noteHeight
                                height = int(dialog.sldrHeight.GetValue())
                                width = int(height / len(img) * len(img[0]))
                                # print(type(self.img))
                                ###Name without filetype suffix '.png'
                                img_name = os.path.basename(i).partition('.png')[0]
                                # print("IMG_NAME", img_name)
                                resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                                resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                                pixels = resizedImg  # 2D array (2D of only on\off values.)
                                pixels2 = resizedImg2  # 3D array (2D of color tuples)
                                # if dialog.chbxToGlobals:
                                #     self.transform_images(i, (pixels, pixels2), height, img_name, dialog, num,
                                #                           palette_name=palette_name, to_file=False)
                                # if not dialog.chbxToGlobals:
                                dialog.transform_images(i, (pixels, pixels2), height, img_name, dialog, num,
                                                      palette_name=palette_name, to_file=True)
                                num += 1


                    elif dialog.SelectCheck and not dialog.AllCheck:
                        ### Multiple Of EACH Selected Color PER Image.
                        print("DUCK3")
                        for k in self.m_v.current_palette_names:
                            for i in dialog.pathnames:
                                num = 0
                                #for j in range(0, dialog.listCtrl.ItemCount):
                                #palette_name = dialog.listCtrl.GetItemText(j)
                                #print("PALETTE_NAME!!!!:", palette_name)
                                # self.pathname = pathname
                                img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                                img2 = cv2.imread(i,
                                                  cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                                # height = MIDAS_Settings.noteHeight
                                height = int(dialog.sldrHeight.GetValue())
                                width = int(height / len(img) * len(img[0]))
                                # print(type(self.img))
                                ###Name without filetype suffix '.png'
                                img_name = os.path.basename(i).partition('.png')[0]
                                # print("IMG_NAME", img_name)
                                resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                                resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                                pixels = resizedImg  # 2D array (2D of only on\off values.)
                                pixels2 = resizedImg2  # 3D array (2D of color tuples)
                                dialog.transform_images(i, (pixels, pixels2), height, img_name, dialog, num,
                                                      palette_name=k)
                                num += 1


                    elif not dialog.SelectCheck and not dialog.AllCheck:
                        ###Multiple WITHOUT Multiple Colors.

                        print("DUCK4")
                        num = 0
                        for i in dialog.pathnames:
                            # self.pathname = pathname
                            img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                            img2 = cv2.imread(i,
                                              cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                            # height = MIDAS_Settings.noteHeight
                            height = int(dialog.sldrHeight.GetValue())

                            width = int(height / len(img) * len(img[0]))
                            # print(type(self.img))
                            ###Name without filetype suffix '.png'
                            img_name = os.path.basename(i).partition('.png')[0]
                            # print("IMG_NAME", img_name)
                            resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                            resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                            pixels = resizedImg  # 2D array (2D of only on\off values.)
                            pixels2 = resizedImg2  # 3D array (2D of color tuples)
                            dialog.transform_images(i, (pixels, pixels2), height, img_name, dialog, num)
                            num += 1


                #Load to Gui Grid.
                else:  # False False False
                    print("DUCK5")
                    pixels = dialog.resizedImg     #2D array (2D of only on\off values.)
                    pixels2 = dialog.resizedImg2   #3D array (2D of color tuples)

                    super().GetParent().GetTopLevelParent().connect = dialog.chbxConnect.GetValue()
                    print("Connect at Top Level?", super().GetParent().GetTopLevelParent().connect)
                    #Test -This was the magical one that found our bug. 11/30/2021
                    #pixels2 = cv2.cvtColor(pixels2, cv2.COLOR_BGR2RGB)

                    #pixels_resized = dialog.resizedImg
                    gran = dialog.pixScaler
                    print("PIXELS", pixels)
                    print("PIXELS2", pixels2)
                    print("PIXELS_RESIZED:", pixels, type(pixels))
                    print("pixels shape", numpy.shape(pixels))

                    m_v = self.GetTopLevelParent().mayavi_view
                    default_color_palette = m_v.current_color_palette
                    mayavi_color_palette = m_v.current_mayavi_palette

                    if dialog.EdgesCheck:
                        edges = cv2.Canny(pixels, 100, 200)
                        stream = midiart.make_midi_from_grayscale_pixels(edges, gran, True,  note_pxl_value=255)   ##dialog.inputKey.GetValue(), , colors=False


                        print("EdgeStream:", stream)
                        stream.show('txt')
                        points = midiart3D.extract_xyz_coordinates_to_array(stream, velocities=m_v.cur_z)
                        index = len(m_v.actors)
                        name = str(len(m_v.actors)) + "_" + "Edges" + "_" + dialog.img_name
                        #clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now?
                        m_v.disable_render = True
                        actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                        #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                        for j in m_v.actors:
                            if j.name == name:
                                print("Points here?")
                                j.change_points(points)
                        m_v.disable_render = False
                        print("Edges load completed.")


                    elif dialog.ColorsCheck:
                        #TODO Display in grid upon completion of Actors\Z-Planes classes.
                        print("PREPixels2:", pixels2)
                        print("Gran", gran)
                        print("Here.")

                        print("DEFAULT_COLOR_PALETTE_2, import.", default_color_palette)
                        #The default_color_palette is the dictionary of colors by which our coords must be sorted.
                        self.num_dict = midiart.separate_pixels_to_coords_by_color(pixels2, m_v.cur_z, nn=True, clrs=default_color_palette, num_dict=True)
                        #TODO DOUBLE CHECK THIS #TODO use default_color_palette---Yes, the sorting MUST be based on the INT colors.
                        print('Num_dict:', self.num_dict)
                        m_v.colors_call += 1
                        #TODO Add colors menu append here.
                        m_v.colors_name = dialog.img_name + "_" + "Clrs"

                        #Menu Appends for new menu export method.
                        new_id = wx.NewIdRef()
                        self.GetTopLevelParent().menuBar.colors.Append(new_id, str(m_v.colors_call) + "\tCtrl+Shift+%s" % m_v.colors_call)
                        self.GetTopLevelParent().Bind(wx.EVT_MENU, self.GetTopLevelParent().menuBar.OnExport_Colors, id=new_id)


                        print("And Here2.")
                        print("Palette", mayavi_color_palette)

                        #Main call.
                        m_v.colors_increment = 1
                        priority_num = -16
                        m_v.scene3d.disable_render = True
                        m_v.colors_calling = True
                        #m_v.scene3d.off_screen_rendering = True
                        for h in self.num_dict.keys():
                            # m_v.scene3d.off_screen_render = True
                            index = len(m_v.actors)
                            # for i in mayavi_color_palette.keys():
                            #     if mayavi_color_palette[i] == h:
                            #Get the color we are on.

                            #R and B color values are swapped. This is fixed here, for now.
                            #TODO Fix inverted color tuples in color dicts? (this is still relevant. It's complicated -- 11/25/20)
                            #SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT --- we know this is part of it because our R and B values are force-swapped here.
                            clr = tuple([mayavi_color_palette[h][0], mayavi_color_palette[h][1], mayavi_color_palette[h][2]])

                            name = "Clrs" + str(m_v.colors_call) + "_" + str(h) + "_" + dialog.img_name
                            actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                            m_v.number_of_noncolorscall_actors -= 1 #Cancels += within new_actor() #TODO Make this a kwarg. 11/25/2020
                            #Colors_call and colors_instance are functionally the same thing, just one in m_v, other in Actor().
                            #TODO Rename? 12/02/2021
                            colors_instance = "Clrs" + str(m_v.colors_call)
                            m_v.actors[index].colors_instance = colors_instance

                            for j in m_v.actors:
                                if j.name == name:
                                    #print("Points here?")
                                    if self.num_dict[h] is not None:
                                        j.change_points(self.num_dict[h])
                                    #print("Color Change:", clr)
                                    j.color = clr
                                    j.part_num = m_v.colors_increment
                                    j.priority = priority_num
                                    m_v.colors_increment += 1
                                    priority_num += 1
                            if m_v.colors_increment >= 16:
                                m_v.scene3d.disable_render = False
                                print(m_v.colors_calling)
                                m_v.colors_calling = False
                                print(m_v.colors_calling)


                        #m_v.scene3d.off_screen_rendering = False
                        print("Colors load completed.")

                    elif dialog.MonochromeCheck:

                        stream = midiart.make_midi_from_grayscale_pixels(pixels, gran, False, note_pxl_value=0)
                        stream.show('txt')
                        points = midiart3D.extract_xyz_coordinates_to_array(stream, velocities=m_v.cur_z)
                        index = len(m_v.actors)
                        name = str(len(m_v.actors)) + "_" + "QR-BW" + "_" + dialog.img_name
                        # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
                        m_v.disable_render = True

                        actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                        # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                        for j in m_v.actors:
                            if j.name == name:
                                print("Points here?")
                                j.change_points(points)
                        m_v.disable_render = False
                        print("Monochrome load completed.")
        except Exception as e:
            print("Exception", "No image yet.")
            print("mult", dialog.MultipleCheck)
            print("select", dialog.SelectCheck)
            print("all", dialog.AllCheck)

                    #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)

    # def update_images(pathname, dialog):
    #     # self.pathname = pathname
    #     img = cv2.imread(pathname, 0)  # 2D array (2D of only on\off values.)
    #     img2 = cv2.imread(pathname, cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
    #
    #     # height = MIDAS_Settings.noteHeight
    #     height = int(dialog.sldrHeight.GetValue())
    #     width = int(height / len(img) * len(img[0]))
    #
    #     # print(type(self.img))
    #     ###Name without filetype suffix '.png'
    #     #img_name = os.path.basename(pathname).partition('.png')[0]
    #     #print("IMG_NAME", img_name)
    #
    #     resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
    #     resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
    #     pixels = resizedImg  # 2D array (2D of only on\off values.)
    #     pixels2 = resizedImg2  # 3D array (2D of color tuples)



    def _OnMIDIArt3DDialogClosed(self, dialog, evt):
        m_v = self.GetTopLevelParent().mayavi_view
        mini_view = dialog.mini_mv

        val = evt.GetReturnCode()
        print("Val %d: " % val)

        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        if btn == "OK":
            try:
                ##ply = dialog.ply
                points = dialog.points

            except AttributeError:
                ##ply = None
                points = None
                return



            if dialog.chbxCurrentActor.IsChecked() is True:
                m_v.scene3d.disable_render = True
                for j in dialog.m_v.actors:
                    for i in dialog.pointclouds:
                        j.change_points(dialog.pointclouds[i])
                #dialog.m_v.CurrentActor().change_points(dialog.pointclouds[dialog.point_cloud_counter])
                m_v.scene3d.disable_render = False

            else:
                if dialog.chbxMultiple.IsChecked():
                    if dialog.chbxPlanes.IsChecked():
                        print("Exporting all Current Actor's Zplanes....")
                        for i in dialog.pointclouds:
                            intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
                            planes_dict = midiart3D.get_planes_on_axis(i)     ###self.m_v.CurrentActor()._points)
                            for zplane in planes_dict.keys():
                                filename = os.path.basename(dialog.ply_names[dialog.pointclouds.index(i)]).partition('.ply')[0] + "_Z_" + str(int(zplane))  #self.m_v.CurrentActor().name
                                output = intermediary_path + filename + ".mid"
                                stream = midiart3D.extract_xyz_coordinates_to_stream(planes_dict[zplane],
                                                                                     durations=False) ##TODO Work on that durations = True stuff. :) 06/22/2022
                                stream.write('mid', output)
                        print("All Current Actor's Zplanes Exported Successfully!")


                    else:
                        actor_counter = 0
                        print("Exporting Loaded Point Clouds....")
                        for i in dialog.pointclouds:
                            intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
                            filename = os.path.basename(dialog.ply_names[dialog.pointclouds.index(i)]).partition('.ply')[0]   #self.m_v.actors[i].name
                            output = intermediary_path + filename + "_Actor_" + str(actor_counter) + ".mid"
                            stream = midiart3D.extract_xyz_coordinates_to_stream(   #self.m_v.actors[i]._
                                i,                                                  ##self.m_v.actors[i]._points,
                                durations=False)  #TODO Work on that durations = True stuff. :) 06/22/2022
                            stream.write('mid', output)                             #self.m_v.actors[i]._
                            actor_counter += 1

                        print("All Point Clouds Exported Successfully!")


                else:
                    if points is not None:
                        #TODO CORE DATA UPDATE Here
                        ##points = midiart3D.get_points_from_ply(dialog.ply)

                        print("DIALOGUE.points", points)
                        #planes_dict = midiart3D.get_planes_on_axis(points, 'z', ordered=True, clean=True)
                        #TODO Delete the startup piano roll/actor when loading ply. ---Still do this?
                        # try:
                        #     self.GetTopLevelParent().pianorollpanel.DeletePianoRoll(1)
                        # except IndexError:
                        #     pass

                        #Establish "Midas Actor" name and index.
                        #TODO Acquire from dialog
                        i = len(m_v.actors)
                        name = str(i) + "_" + "PointCloud" + "_" + dialog.ply_names[dialog.point_cloud_counter]
                        m_v.scene3d.disable_render = True
                        actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(i, name)
                        # New Actor Checkbox
                        # self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(
                        #     len(self.m_v.actors)) \
                        #     if dialog.chbxNewActor.IsChecked() is True else None


                        for j in m_v.actors:
                            if j.name == name:
                                print("Points here?")
                                #j.change_points(points)
                                j._points = points
                                #self.pointschangedflag = not self.pointschangedflag
                                j.actor_points_changed()
                                print("And here?")
                        m_v.scene3d.disable_render = False
                    else:
                        m_v.scene3d.disable_render = False

                        pass
                m_v.scene3d.disable_render = False

        #mini_view.scene.close()
        #self.__delattr__('mini_view')
        #dialog.__delattr__("dialog.mini_mv")
        #gc.collect()

        #index_list = [k for k in planes_dict.keys()]
        # for k in index_list:
        #     self.GetTopLevelParent().pianorollpanel.InsertNewPianoRoll(int(index_list.index(k)))
        #     self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(midiart3D.extract_xyz_coordinates_to_stream((np.array(planes_dict[k]))))


        #r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"


class TheMidasButtonDialog(wx.Dialog):   #TheMidasButtonDialog(wx.Dialog)
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=(194, 0), style=wx.DEFAULT_DIALOG_STYLE, name='Visual Music Operations and Loading Basic Midi'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)
        #self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)
        #self.Centre(direction=wx.BOTH)
        #self.Center(dir=wx.BOTH)


        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, (313, 1081), style=wx.BORDER_RAISED)  # 770
        self.imgPreviewPanel1 = wx.Panel(self, -1, wx.DefaultPosition, (1111, 313), style=wx.BORDER_RAISED)
        self.imgPreviewPanel2 = wx.Panel(self, -1, wx.DefaultPosition, (1111, 546), style=wx.BORDER_RAISED)

        # MuseNet Panel
        self.muse_panel = wx.Panel(self.ctrlsPanel, -1, wx.DefaultPosition, (250, -1), style=wx.BORDER_RAISED)  #

        self.displayImage1 = None
        self.displayImage2 = None


        self.directory_or_globals = []   #Used with the Globals.


        self.DirectoryFlag = None
        self.MusicodeGlobalsFlag = None
        self.MidiartGlobalsFlag = None
        self.Midiart3DGlobalsFlag = None


        self.progressify_counter = 1

        #Basic Midi\Score Load
        self.help_static = wx.StaticText(self.ctrlsPanel, -1, "Import a midi file or a score file.", style=wx.ALIGN_CENTER)

        self.btnLoadMidi = wx.Button(self.ctrlsPanel, -1, "Load Midi\\Score")


        # Input text box

        self.inputTxt = wx.TextCtrl(self.muse_panel, -1, "              Input MuseNet Prompt Here", size=(250, -1),
                                    style=wx.TE_MULTILINE, name="Generative Prompter Input")
        #self.inputTxt.Disable()
        self.musepanel_flag = False


        self.btnGenerate_MuseNet = wx.Button(self.ctrlsPanel, -1, "MuseNet Midi\nGenerate")
        self.musenet_tooltip = wx.ToolTip("MuseNet is not publicly available.......yet.")
        self.btnGenerate_MuseNet.SetToolTip(self.musenet_tooltip)
        #self.btnGenerate_MuseNet.Disable()

        self.staticLoadSingles = wx.StaticText(self.ctrlsPanel, 0, "Load...")
        #Operation Buttons
        self.btnLoadMelody = wx.Button(self.ctrlsPanel, -1, "Load Melody")
        self.btnRandomMelody = wx.Button(self.ctrlsPanel, -1, "Random Melody")

        self.btnLoadMusicode = wx.Button(self.ctrlsPanel, -1, "Load Musicode")


        self.staticMelody_Length = wx.StaticText(self.ctrlsPanel, 0, "Melody Length")
        self.txtctrlMelodyLength = wx.TextCtrl(self.ctrlsPanel, -1, "0", size=(70, -1), style=wx.TE_CENTER)   #, name=argskwargs)
        self.melody_tooltip = wx.ToolTip("The length of the Melody; it's number of notes.\n"
                                         "It must match the length of the number of"
                                         "measures|letters in your Musicode  in order for "
                                         "Align_Musicode_With_Melody to work properly.")
        self.txtctrlMelodyLength.SetToolTip(self.melody_tooltip)


        self.staticMusicode_Length = wx.StaticText(self.ctrlsPanel, 0, "Musicode Length")
        self.txtctrlMusicodeLength = wx.TextCtrl(self.ctrlsPanel, -1, "0", size=(70, -1), style=wx.TE_CENTER)   #, name=argskwargs)
        self.musicode_tooltip = wx.ToolTip("The length of the number of measures in a musicode."
                                           "It is also the length of its number of letters.\n"
                                           "It must match the number of notes in your Melody for "
                                           "Align_Musicode_With_Melody to work properly. This length value ignores "
                                           "measures that are empty; musicode measures created with the ' ' string.")
        self.txtctrlMusicodeLength.SetToolTip(self.musicode_tooltip)

        #self.chbxDirectory = wx.CheckBox(self.ctrlsPanel, -1, "Operate on Entire Directory?")    #ctrlsPanel

        self.staticOperandDirectory = wx.StaticText(self.ctrlsPanel, 0, "Operand Directory:")

        self.txtctrlOperandDirectory = wx.TextCtrl(self.ctrlsPanel, -1, "Your Directory Choice",
                                                   size=(280, -1),
                                                   style=wx.TE_CENTER)   #, name=argskwargs)
        self.staticOutputDirectory = wx.StaticText(self.ctrlsPanel, 0, "Output Directory:")
        self.tooltipOutput = wx.ToolTip("You can type your own output folder name here. Operations that require an "
                                        "output folder will create one with your selected name.")
        self.staticOutputDirectory.SetToolTip(self.tooltipOutput)
        self.txtctrlOutputDirectory = wx.TextCtrl(self.ctrlsPanel, -1, "Your Output Directory Choice",
                                                  size=(280, -1),
                                                  style=wx.TE_CENTER)  # , name=argskwargs)

        self.staticLoadGlobals = wx.StaticText(self.ctrlsPanel, 0, "Load en Mass...")
        self.btnLoadMusicodeGlobals = wx.Button(self.ctrlsPanel, -1, "Musicode Globals")
        self.musicodeGL_tooltip = wx.ToolTip("Load music21 streams from memory of the 'Full Series' created with the Musicode button.")
        self.btnLoadMusicodeGlobals.SetToolTip(self.musicodeGL_tooltip)
        self.btnLoadMidiartGlobals = wx.Button(self.ctrlsPanel, -1, "Midiart Globals")
        self.midiartGL_tooltip = wx.ToolTip("Load music21 streams from memory of the 'directory' transformed with the MidiArt button.")
        self.btnLoadMidiartGlobals.SetToolTip(self.midiartGL_tooltip)
        self.btnLoad3idiartGlobals = wx.Button(self.ctrlsPanel, -1, "3idiart Globals")
        self.midiart3DGL_tooltip = wx.ToolTip("Load music21 streams from memory of a list of x-y planes along the z-axis of the last point cloud created with the 3idiArt button.")
        self.btnLoad3idiartGlobals.SetToolTip(self.midiart3DGL_tooltip)

        self.btnLoadDirectory = wx.Button(self.ctrlsPanel, -1, "Load Directory||File")

        self.btnLoadProgression = wx.Button(self.ctrlsPanel, -1, "Load Progression")
        self.btnRandomProgression = wx.Button(self.ctrlsPanel, -1, "Random Progression")
        self.btnCorpusProgression = wx.Button(self.ctrlsPanel, -1, "Corpus Progression")
        self.corpusprogression_tooltip = wx.ToolTip(
            "Get a progression using a piece of freely-distributable music found in music21.")  #.corpus.getPaths()
        self.btnCorpusProgression.SetToolTip(self.corpusprogression_tooltip)

        self.btnDownloadLinks = wx.Button(self.ctrlsPanel, -1, "Download...")
        self.downloadlinks_tooltip = wx.ToolTip("Use this button to open up several hyperlinks to freely downloadable, "
                                                "Creative Commons works, as well as a few that require a subscription.")
        self.btnDownloadLinks.SetToolTip(self.downloadlinks_tooltip)


        #######
        #Corpus Dicts
        self.m21s_big_34 = {'airdsAirs': '''Aird’s Airs''',
                       'bach': 'Johann Sebastian Bach',
                       'beach': 'Amy Beach',
                       'beethoven': 'Ludwig van Beethoven',
                       'chopin': 'Frederic Chopin',
                       'ciconia': 'Johannes Ciconia',
                       'corelli': 'Arcangelo Corelli',
                       'cpebach': 'C.P.E. Bach',
                       'demos': 'Demonstration Files',
                       'essenFolksong': 'Essen Folksong Collection',
                       'handel': 'George Frideric Handel',
                       'haydn': 'Joseph Haydn',
                       'joplin': 'Scott Joplin',
                       'johnson_j_r': 'J. Rosamund Johnson',
                       'josquin': 'Josquin des Prez',
                       'leadSheet': 'Leadsheet demos',
                       'liliuokalani': 'Queen Liliʻuokalani',
                       'luca': 'D. Luca',
                       'lusitano': 'Vicente Lusitano',
                       'miscFolk': 'Miscellaneous Folk',
                       'monteverdi': 'Claudio Monteverdi',
                       'mozart': 'Wolfgang Amadeus Mozart',
                       'nottingham-dataset': 'Nottingham Music Database (partial)',
                       'oneills1850': 'Oneill’s 1850 Collection',
                       'palestrina': 'Giovanni Palestrina',
                       'ryansMammoth': 'Ryan’s Mammoth Collection',
                       'schoenberg': 'Arnold Schoenberg',
                       'schubert': 'Franz Schubert',
                       'schumann_robert': 'Robert Schumann',
                       'schumann_clara': 'Clara Schumann',
                       'theoryExercises': 'Theory Exercises',
                       'trecento': 'Fourteenth-Century Italian Music',
                       'verdi': 'Giuseppe Verdi',
                       'weber': 'Carl Maria von Weber'}

        self.corpus_selection = ""
        self.corpus_progression = ""
        self.the_big34_odict = OrderedDict(self.m21s_big_34)
        self.big34_selection_list = [i for i in self.the_big34_odict.keys()]
        # for i in range(0, 35, 1):
        #     print(i)
        #     eval('Menu%s' % i)
        #         #= 'self.Menu%s' % i
        #     eval('menu')
        #     _ = wx.Menu()
        self.menu_34 = wx.Menu()


        #######
        #Downloads Resources
        self.download_links_dict = {"Musescore": "https://musescore.org/en",
                                    "Chordify": "https://chordify.net/",
                                    "Mutopia": "https://www.mutopiaproject.org/",
                                    "Kern Humdrum": "https://kern.humdrum.org/",
                                    "Classical Archives": "https://www.classicalarchives.com/newca/#!/",
                                    "Choral Public Domain Library": "https://www.cpdl.org/wiki/index.php/Main_Page",
                                    "Petrucci Music Library": "https://imslp.org/"}
                                    #"Discover More!!": ""}

        self.download_link = ""
        self.the_free7_odict = OrderedDict(self.download_links_dict)
        self.the_free7_list = [i for i in self.the_free7_odict.keys()]

        self.menu_7 = wx.Menu()

                         # wx.Menu(),


        self.generate_corpus_menus()

        self.generate_download_menus()

        self.btnAlignMusicodeWithMelody = wx.Button(self.ctrlsPanel, -1, "Align Musicode With Melody")
        self.btnProgressifyVisualMusic = wx.Button(self.ctrlsPanel, -1, "Progressify Visual Music")
        self.progressify_visualmusic_tooltip = wx.ToolTip(
            "Quite possibly the most powerful musicological function. This function takes a midi file on input"
            "(except for color midi files) and, with an input progression of chords and those chords' spans, all the "
            "midi of an input midi file -- as a music21 stream ALIGNED with that input progression-- will have notes "
            "removed that DO NOT belong to those chord WITHIN those spans.")
        self.progressify_visualmusic_tooltip.SetAutoPop(17000)
        self.btnProgressifyVisualMusic.SetToolTip(self.progressify_visualmusic_tooltip)

        self.btnSplitMidiChannels = wx.Button(self.ctrlsPanel, -1, "Split Midi Channels")
        self.btnProgressifyDirectory = wx.Button(self.ctrlsPanel, -1, "Progressify Directory")
        self.progressify_directory_tooltip = wx.ToolTip("An expanded version of the most powerful Midas function; this operates on"
                                              " entire directories and was also specifically designed for Colored midi "
                                              "transformations in mind. NOTE: The contents of the operand directory "
                                              "must be .mid files only: no folders will work here.")
        self.btnProgressifyDirectory.SetToolTip(self.progressify_directory_tooltip)


        self.chbxZero_Velocity = wx.CheckBox(self.ctrlsPanel, -1, "Zero Velocities?")
        self.chbxZero_Velocity.Disable()


        self.chbxColorsOnly = wx.CheckBox(self.ctrlsPanel, -1, "Colors-Only Directory?")#ctrlsPanel
        self.colors_onlydir_tooltip = wx.ToolTip(
            "Check this box if your directory is comprised of midi files created with the split_midi_channels() function"
            " that operated on a color-midi transformation.")

        self.chbxColorsOnly.SetToolTip(self.colors_onlydir_tooltip)

        self.chbxStretch_Progression = wx.CheckBox(self.ctrlsPanel, -1, "Stretch Progression?")
        self.stretch_Tooltip = wx.ToolTip(
            "If unchecked, this will stretch the operand stream(s) TO the progression. This is the default setting. "
            "If checked, this will stretch the progression stream TO the operand stream(s). ")
        self.chbxStretch_Progression.SetToolTip(self.stretch_Tooltip)
        #self.chbxStretch_Progression.SetValue(True)

        self.staticStretch = wx.StaticText(self.ctrlsPanel, 0, "Stretch by...")

        self.chbxDirectory_Stretch = wx.CheckBox(self.ctrlsPanel, -1, "Directory")
        self.directory_Tooltip = wx.ToolTip("Stretching will be factored by ONE highestTime for every item in the "
                                            "directory|list. Highly useful for color transformations and pointclouds work "
                                            "with 'Stretch Progression?' checked. Useful with musicodes if 'Stretch "
                                            "Progression?' unchecked.")
        self.chbxDirectory_Stretch.SetToolTip(self.directory_Tooltip)
        self.chbxDirectory_Stretch.SetValue(True)

        self.chbxStream_Stretch = wx.CheckBox(self.ctrlsPanel, -1, "Stream")
        self.stream_Tooltip = wx.ToolTip("The stretch will be factored by each item's OWN highestTime in the "
                                         "directory|list. Highly useful for folder of edge-detections, "
                                         "monochrome transformations, or lots of individualized work.")
        self.chbxStream_Stretch.SetToolTip(self.stream_Tooltip)

        self.chbxStretch_None = wx.CheckBox(self.ctrlsPanel, -1, "None")
        self.none_Tooltip = wx.ToolTip(
            "This will make it so your neither your operand stream nor your progression stream are stretched at all."
            " Useful with select musical working such as working with musicodes where you want them to stay in their "
            "own measures, and, say, you already have chords set up for a non-stretch scenario---already aligned.")
        self.chbxStretch_None.SetToolTip(self.none_Tooltip)


        self.btnSnapDirectory = wx.Button(self.ctrlsPanel, -1, "Snap Directory")
        self.btnFilterDirectory = wx.Button(self.ctrlsPanel, -1, "Filter Directory")

        self.staticKey = wx.StaticText(self.ctrlsPanel, 0, "Key")
        self.statickey_tooltip = wx.ToolTip('''Keys can be: "A", "A#m", "Ab", "Abm", "Am", "B", "Bb", "Bbm", "Bm", "C", 
        "C#", "C#m", "Cb", "Cm", "D", "D#m", "Db", "Dm", "E", "Eb", "Ebm", "Em", "F", "F#", "F#m", "Fm", "G", "G#m",
        "Gb", "Gm". \n Quotation marks are not needed around them.''')
        self.staticKey.SetToolTip(self.statickey_tooltip)

        self.txtctrlKey = wx.TextCtrl(self.ctrlsPanel, -1, "C", size=(70, -1), style=wx.TE_CENTER)

        self.staticCurrentFile = wx.StaticText(self.ctrlsPanel, 0, "Current File|Selection:")
        self.txtctrlCurrentFile = wx.TextCtrl(self.ctrlsPanel, -1, "Your Current File|Selection Choice",
                                                   size=(280, -1),
                                                   style=wx.TE_CENTER)  # , name=argskwargs)

        self.chbxToGUI = wx.CheckBox(self.ctrlsPanel, -1, "To GUI?")    #ctrlsPanel



        # New Actor Checkbox
        # self.chbxNewActor = wx.CheckBox(self.ctrlsPanel, -1, "New Actor?")    #ctrlsPanel
        # self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())

        self.sldrStatic = wx.StaticText(self.ctrlsPanel, -1, "Height")
        self.sldrHeight = wx.Slider(self.ctrlsPanel, -1, 546, 1, 546, wx.DefaultPosition, (190, 40), #127
                                    wx.SL_HORIZONTAL | wx.SL_LABELS)

        self.btnPrevious = wx.Button(self.ctrlsPanel, -1, "◄---Prev", size=(83, 17))
        self.btnNext = wx.Button(self.ctrlsPanel, -1, "Next---►", size=(83, 17))


        #############
        #OpenAI Class
        #self.muse_net = Generate.Muse_Net()


        #Binds
        self.Bind(wx.EVT_BUTTON, self.OnLoadMidi, self.btnLoadMidi)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate_MuseNet_Midi, self.btnGenerate_MuseNet)
        #self.Bind(wx.EVT_BUTTON, )

        self.Bind(wx.EVT_BUTTON, self.OnLoadMelody, self.btnLoadMelody)
        self.Bind(wx.EVT_BUTTON, self.OnLoadMusicode, self.btnLoadMusicode)
        self.Bind(wx.EVT_BUTTON, self.OnLoadProgression, self.btnLoadProgression)

        self.Bind(wx.EVT_BUTTON, self.OnMusic21sBig34, self.btnCorpusProgression)
        self.Bind(wx.EVT_BUTTON, self.OnFreeLinks7, self.btnDownloadLinks)   ##Subject to additions!!! 02/26/24

        self.Bind(wx.EVT_BUTTON, self.onLoadMusicodeGlobals, self.btnLoadMusicodeGlobals)
        self.Bind(wx.EVT_BUTTON, self.onLoadMidiartGlobals, self.btnLoadMidiartGlobals)
        self.Bind(wx.EVT_BUTTON, self.onLoadMidiart3DGlobals, self.btnLoad3idiartGlobals)

        self.Bind(wx.EVT_BUTTON, self.OnLoadDirectory, self.btnLoadDirectory)

        self.Bind(wx.EVT_BUTTON, self.onRandomMelody, self.btnRandomMelody)
        self.Bind(wx.EVT_BUTTON, self.onRandomProgression, self.btnRandomProgression)
        self.Bind(wx.EVT_BUTTON, self.onSplitMidiChannels, self.btnSplitMidiChannels)

        self.Bind(wx.EVT_BUTTON, self.onProgressify, self.btnProgressifyVisualMusic)
        self.Bind(wx.EVT_BUTTON, self.onAlignMusicodeWithMelody, self.btnAlignMusicodeWithMelody)

        self.Bind(wx.EVT_BUTTON, self.onProgressifyDirectory, self.btnProgressifyDirectory)
        self.Bind(wx.EVT_BUTTON, self.onFilterDirectory, self.btnFilterDirectory)
        self.Bind(wx.EVT_BUTTON, self.onSnapDirectory, self.btnSnapDirectory)

        self.Bind(wx.EVT_BUTTON, self.onCyclePrevious2, self.btnPrevious)
        self.Bind(wx.EVT_BUTTON, self.onCycleNext2, self.btnNext)

        self.Bind(wx.EVT_SLIDER, self.OnSliderChanged, self.sldrHeight)

        self.Bind(wx.EVT_CHECKBOX, self.OnPolarizeCheckboxes)        #  , self.onPolarizeCheckboxes)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnLoadCorpusProgression)

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)

        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.sizerMuseNet = wx.BoxSizer(wx.VERTICAL)
        self.sizerMuseNet.Add(self.muse_panel, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerMuseNet.Add(self.btnGenerate_MuseNet, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerMelody = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerMelody.Add(self.btnLoadMelody, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerMelody.Add(self.btnRandomMelody, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerProgression = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerProgression.Add(self.btnLoadProgression, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerProgression.Add(self.btnRandomProgression, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerCorpusandDownloads = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerCorpusandDownloads.Add(self.btnCorpusProgression, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerCorpusandDownloads.Add(self.btnDownloadLinks, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerLengths1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerLengths1.Add(self.staticMelody_Length, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerLengths1.Add(self.txtctrlMelodyLength, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerLengths2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerLengths2.Add(self.staticMusicode_Length, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerLengths2.Add(self.txtctrlMusicodeLength, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerParams = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerParams.Add(self.staticKey, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerParams.Add(self.txtctrlKey, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerOperand = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerOperand.Add(self.staticOperandDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerOperand.Add(self.txtctrlOperandDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerOutput = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerOutput.Add(self.staticOutputDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerOutput.Add(self.txtctrlOutputDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerCurrent = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerCurrent.Add(self.staticCurrentFile, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerCurrent.Add(self.txtctrlCurrentFile, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerSlider = wx.BoxSizer(wx.VERTICAL)
        self.sizerSlider.Add(self.sldrStatic, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerSlider.Add(self.sldrHeight, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerStretch = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerStretch.Add(self.chbxDirectory_Stretch, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerStretch.Add(self.chbxStream_Stretch, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerStretch.Add(self.chbxStretch_None, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerSnapnFilter = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerSnapnFilter.Add(self.btnFilterDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerSnapnFilter.Add(self.btnSnapDirectory, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerCycle = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerCycle.Add(self.btnPrevious, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerCycle.AddSpacer(30)
        self.sizerCycle.Add(self.btnNext, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        self.sizerGlobals = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerGlobals.Add(self.btnLoadMusicodeGlobals, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerGlobals.Add(self.btnLoadMidiartGlobals, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizerGlobals.Add(self.btnLoad3idiartGlobals, 0, wx.ALL | wx.ALIGN_CENTER, 0)




        sizerMain = wx.BoxSizer(wx.VERTICAL)
        #sizerMain.Add(sizerHor, 30)
        sizerMain.Add(self.help_static, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.Add(self.btnLoadMidi, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.Add(self.sizerMuseNet, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(15)
        sizerMain.Add(self.staticLoadSingles, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.sizerMelody, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.btnLoadMusicode, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.sizerProgression, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.sizerCorpusandDownloads, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(15)
        sizerMain.Add(self.staticLoadGlobals, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.btnLoadDirectory, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(5)
        sizerMain.Add(self.sizerGlobals, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(15)
        sizerMain.Add(self.sizerLengths1, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(5)
        sizerMain.Add(self.sizerLengths2, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(5)
        sizerMain.Add(self.sizerOperand, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(5)
        sizerMain.Add(self.sizerOutput, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(15)
        sizerMain.Add(self.btnAlignMusicodeWithMelody, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizerMain.Add(self.btnProgressifyVisualMusic, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizerMain.Add(self.btnSplitMidiChannels, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizerMain.AddSpacer(2)
        sizerMain.Add(self.btnProgressifyDirectory, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizerMain.Add(self.chbxZero_Velocity, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.Add(self.chbxStretch_Progression, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.Add(self.staticStretch, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.sizerStretch, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        #sizerMain.AddSpacer(10)
        #sizerMain.Add(self.btnFilterDirectory, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizerMain.AddSpacer(12)
        sizerMain.Add(self.chbxColorsOnly, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.Add(self.sizerSnapnFilter, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        sizerMain.Add(self.sizerParams, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.AddSpacer(12)
        sizerMain.Add(self.sizerCycle, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerMain.Add(self.sizerCurrent, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        sizerMain.AddSpacer(10)
        sizerMain.Add(self.sizerSlider, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        sizerMain.AddSpacer(7)
        sizerMain.Add(self.chbxToGUI, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        #sizerMain.Add(self.chbxNewActor, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        #sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizerCtrls.Add(sizerMain)

        #self.SetSizer(sizerCtrls)
        #self.SetSizerAndFit(sizerMain)

        self.ctrlsPanel.SetSizer(sizerCtrls)

        #sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        sizerVerti = wx.BoxSizer(wx.VERTICAL)

        sizerVerti.Add(self.imgPreviewPanel1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizerVerti.AddSpacer(15)
        sizerVerti.Add(self.imgPreviewPanel2, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        #sizerVerti.AddSpacer(45)

        sizerHori = wx.BoxSizer(wx.HORIZONTAL)
        sizerHori.Add(self.ctrlsPanel, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        #sizerVerti.AddSpacer(25)
        sizerHori.Add(sizerVerti, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        sizerMaster = wx.BoxSizer(wx.VERTICAL)
        sizerMaster.Add(sizerHori, 30)
        sizerMaster.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizerAndFit(sizerMaster)


    ####
    #####################
    def generate_corpus_menus(self):
        num = 0
        for i in range(1, len(self.big34_selection_list) + 1):   #34 elements in this iteration
            #menus_34)):   #self.big34_selection_list:   #self.axis_menu_list:
            zero_holder = "0" if not int(i) >= 10 else ""
            zero_holder = "" if i == 10 else zero_holder
            #print("Zero_Holder", zero_holder)
            print("INVALID_ID?", int(eval("%s" % 1 + "7" + zero_holder + str(i))))     #self.menu_34.index(i)
            # print("INVALID_ID?", int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "102"))) ....

            self.menu_34.Append(int(eval("%s" % 1 +     #(self.menu_34.index(i)
                               "7" + zero_holder + str(i))),
                               self.the_big34_odict[self.big34_selection_list[i-1]])  #String name of the Corpus selection||Artist
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "102")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "103")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "104")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "105")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "106")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "107")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "108")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "109")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "110")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "111")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "112")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "113")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "114")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "115")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "116")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "117")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "118")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "119")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "120")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "121")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "122")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "123")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "124")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "125")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "126")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "127")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "128")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "129")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "130")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "131")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "132")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "133")), self.the_big34_odict[i])  #
        #     self.big34_selection_list[i].Append(int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "134")), self.the_big34_odict[i])  #
        # # menu.Append(10102, "y")  #
        # menu.Append(10103, "z")  #

        # for i in self.axis_menu_list:
        #     for j in i.GetMenuItems():
        #         i.Bind(wx.EVT_MENU, self.menu_return,
        #                id=int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "101")))
        #         i.Bind(wx.EVT_MENU, self.menu_return,
        #                id=int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "102")))
        #         i.Bind(wx.EVT_MENU, self.menu_return,
        #                id=int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "103")))

        # for i in self.axis_menu_list:
        # for j in self.menu_34.GetMenuItems():
        for i in range(1, len(self.big34_selection_list) + 1):
            zero_holder = "0" if not int(i) >= 10 else ""
            # print("Zero_Holder", zero_holder)
            id = int(eval("%s" % 17 + zero_holder + str(i))) if i != 10 else 1710
            print("ID", id)
            self.menu_34.Bind(wx.EVT_MENU, self.menu_return, id=id)
        # self.menu_34.Bind(wx.EVT_MENU, self.menu_return, id=int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "102")))
        # self.menu_34.Bind(wx.EVT_MENU, self.menu_return, id=int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "103")))


    def OnMusic21sBig34(self, evt):   #OnAxisButton1
        #self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu1)
        print("Corpus_1")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.menu_34)

    #
    # def OnAxisButton1(self, evt):
    #     print("Axis_1")
    #     self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu1)
    #
    # def OnAxisButton2(self, evt):
    #     print("Axis_2")
    #     self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu2)
    #
    # def OnAxisButton3(self, evt):
    #     print("Axis_3")
    #     self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu3)
    #
    # def OnAxisButton4(self, evt):
    #     print("Axis_4")
    #     self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu4)
        self.OnOverwriteMusePanel() if not self.musepanel_flag else None
        self.musepanel_flag = True  #True is listBox, False is inputTxt

        try:
            if self.listctrl_CorpusBox.GetItemCount() != 0:
                self.listctrl_CorpusBox.DeleteAllItems()
            # for i in range(len(self.corpus_selection)):
            #     self.listctrl_CorpusBox.DeleteItem(self.corpus_selection(i))
        except AttributeError as AE:
            print("Attribute Error", AE)
            pass

        self.index = 1
        self.corpus_selection_works_list = music21.corpus.getComposer(self.corpus_selection)
        for music in self.corpus_selection_works_list:
            print("Composer|Selection_Choice", music)
            self.listctrl_CorpusBox.InsertItem(self.index, str(music))
            self.index += 1


    def menu_return(self, evt):
        #pass
        if evt.GetId() == 1701:
            print('airdsAirs')
            self.corpus_selection = 'airdsAirs'
            'airdsAirs'
        if evt.GetId() == 1702:
            print('bach')
            self.corpus_selection = 'bach'
            'bach'
        if evt.GetId() == 1703:
            print('beach')
            self.corpus_selection = 'beach'
            'beach'
        if evt.GetId() == 1704:
            print('beethoven')
            self.corpus_selection = 'beethoven'
            'beethoven'
        if evt.GetId() == 1705:
            print('chopin')
            self.corpus_selection = 'chopin'
            'chopin'
        if evt.GetId() == 1706:
            print('ciconia')
            self.corpus_selection = 'ciconia'
            'ciconia'
        if evt.GetId() == 1707:
            print('corelli')
            self.corpus_selection = 'corelli'
            'corelli'
        if evt.GetId() == 1708:
            print('cpebach')
            self.corpus_selection = 'cpebach'
            'cpebach'
        if evt.GetId() == 1709:
            print('demos')
            self.corpus_selection = 'demos'
            'demos'
        if evt.GetId() == 1710:
            print('essenFolksong')
            self.corpus_selection = 'essenFolksong'
            'essenFolksong'
        if evt.GetId() == 1711:
            print('handel')
            self.corpus_selection = 'handel'
            'handel'
        if evt.GetId() == 1712:
            print('haydn')
            self.corpus_selection = 'haydn'
            'haydn'
        if evt.GetId() == 1713:
            print('joplin')
            self.corpus_selection = 'joplin'
            'joplin'
        if evt.GetId() == 1714:
            print('johnson_j_r')
            self.corpus_selection = 'johnson_j_r'
            'johnson_j_r'
        if evt.GetId() == 1715:
            print('josquin')
            self.corpus_selection = 'josquin'
            'josquin'
        if evt.GetId() == 1716:
            print('leadSheet')
            self.corpus_selection = 'leadSheet'
            'leadSheet'
        if evt.GetId() == 1717:
            print('liliuokalani')
            self.corpus_selection = 'liliuokalani'
            'liliuokalani'
        if evt.GetId() == 1718:
            print('luca')
            self.corpus_selection = 'luca'
            'luca'
        if evt.GetId() == 1719:
            print('lusitano')
            self.corpus_selection = 'lusitano'
            'lusitano'
        if evt.GetId() == 1720:
            print('miscFolk')
            self.corpus_selection = 'miscFolk'
            'miscFolk'
        if evt.GetId() == 1721:
            print('monteverdi')
            self.corpus_selection = 'monteverdi'
            'monteverdi'
        if evt.GetId() == 1722:
            print('mozart')
            self.corpus_selection = 'mozart'
            'mozart'
        if evt.GetId() == 1723:
            print('nottingham-dataset')
            self.corpus_selection = 'nottingham-dataset'
            'nottingham-dataset'
        if evt.GetId() == 1724:
            print('oneills1850')
            self.corpus_selection = 'oneills1850'
            'oneills1850'
        if evt.GetId() == 1725:
            print('palestrina')
            self.corpus_selection = 'palestrina'
            'palestrina'
        if evt.GetId() == 1726:
            print('ryansMammoth')
            self.corpus_selection = 'ryansMammoth'
            'ryansMammoth'
        if evt.GetId() == 1727:
            print('schoenberg')
            self.corpus_selection = 'schoenberg'
            'schoenberg'
        if evt.GetId() == 1728:
            print('schubert')
            self.corpus_selection = 'schubert'
            'schubert'
        if evt.GetId() == 1729:
            print('schumann_robert')
            self.corpus_selection = 'schumann_robert'
            'schumann_robert'
        if evt.GetId() == 1730:
            print('schumann_clara')
            self.corpus_selection = 'schumann_clara'
            'schumann_clara'
        if evt.GetId() == 1731:
            print('theoryExercises')
            self.corpus_selection = 'theoryExercises'
            'theoryExercises'
        if evt.GetId() == 1732:
            print('trecento')
            self.corpus_selection = 'trecento'
            'trecento'
        if evt.GetId() == 1733:
            print('verdi')
            self.corpus_selection = 'verdi'
            'verdi'
        if evt.GetId() == 1734:
            print('weber')
            self.corpus_selection = 'weber'
            'weber'
        #     self.axisVar_Trim.SetLabelText('x')
        #####################


    def OnOverwriteMusePanel(self):
        try:
            self.inputTxt.Destroy()
            print(self.inputTxt)
            self.listctrl_CorpusBox = CustomListBox2(self.muse_panel, log=None)
        except Exception as e:
            try:
                print("Exception_OOwMP", e)
                self.listctrl_CorpusBox.Destroy()
                self.inputTxt = wx.TextCtrl(self.muse_panel, -1, "              Input MuseNet Prompt Here", size=(250, -1),
                                            style=wx.TE_MULTILINE, name="Generative Prompter Input")
            except Exception as f:
                print("Exception_OOwMP--f", f)
                self.inputTxt.Destroy()
                self.listctrl_CorpusBox = CustomListBox2(self.muse_panel, log=None)
        self.muse_panel.Refresh()


    ####
    ######################
    def generate_download_menus(self):
        #*IDs are in the 2000s range instead of 1000s range here.
        #Append the menu with an ID and the string assigned to it.
        for i in range(1, len(self.download_links_dict) + 1):
            zero_holder = "0" if not int(i) >= 10 else ""
            zero_holder = "" if i == 10 else zero_holder
            # print("Zero_Holder", zero_holder)
            print("INVALID_ID?", int(eval("%s" % 2 + "7" + zero_holder + str(i))))  # self.menu_34.index(i)
            # print("INVALID_ID?", int(eval("%s" % (self.axis_menu_list.index(i) + 1) + "102"))) ....

            self.menu_7.Append(int(eval("%s" % 2 +  #ID
                                         "7" + zero_holder + str(i))),
                                    self.the_free7_list[i - 1])  # String name of the Resource Hyperlink


        for i in range(1, len(self.download_links_dict) + 1):
            zero_holder = "0" if not int(i) >= 10 else ""
            # print("Zero_Holder", zero_holder)
            #*
            id = int(eval("%s" % 27 + zero_holder + str(i))) if i != 10 else 2710
            print("ID", id)
            self.menu_7.Bind(wx.EVT_MENU, self.menu_return2, id=id)


    def menu_return2(self, evt):
        if evt.GetId() == 2701:
            print("Musescore")
            self.download_link = "Musescore"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2702:
            print("Chordify")
            self.download_link = "Chordify"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2703:
            print("Mutopia")
            self.download_link = "Mutopia"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2704:
            print("Kern Humdrum")
            self.download_link = "Kern Humdrum"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2705:
            print("Classical Archives")
            self.download_link = "Classical Archives"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2706:
            print("Choral Public Domain Library")
            self.download_link = "Choral Public Domain Library"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)
        if evt.GetId() == 2707:
            print("Petrucci Music Library")
            self.download_link = "Petrucci Music Library"
            wx.LaunchDefaultBrowser(self.the_free7_odict[self.download_link], 0)

    def OnFreeLinks7(self, evt):   #OnAxisButton1
        #self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu1)
        print("Corpus_1")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.menu_7)

        # self.OnOverwriteMusePanel() if not self.musepanel_flag else None
        # self.musepanel_flag = True  #True is listBox, False is inputTxt

        try:
            if self.listctrl_CorpusBox.GetItemCount() != 0:
                self.listctrl_CorpusBox.DeleteAllItems()
            # for i in range(len(self.corpus_selection)):
            #     self.listctrl_CorpusBox.DeleteItem(self.corpus_selection(i))
        except AttributeError as AE:
            print("Attribute Error", AE)
            pass

        # self.index = 1
        # self.corpus_selection_works_list = music21.corpus.getComposer(self.corpus_selection)
        # for music in self.corpus_selection_works_list:
        #     print("Composer|Selection_Choice", music)
        #     self.listctrl_CorpusBox.InsertItem(self.index, str(music))
        #     self.index += 1


    def OnPolarizeCheckboxes(self, evt):
        print("Setting your stretch choice, passing...")
        if self.chbxStretch_None.IsChecked():
            self.chbxDirectory_Stretch.SetValue(False)
            self.chbxStream_Stretch.SetValue(False)

        elif self.chbxStream_Stretch.IsChecked():
            self.chbxDirectory_Stretch.SetValue(False)
            self.chbxStretch_None.SetValue(False)

        elif self.chbxDirectory_Stretch.IsChecked():
            self.chbxStream_Stretch.SetValue(False)
            self.chbxStretch_None.SetValue(False)

        if self.chbxColorsOnly.IsChecked():
            self.chbxStretch_Progression.SetValue(True)
            self.chbxDirectory_Stretch.SetValue(True)
            self.chbxStream_Stretch.SetValue(False)
            self.chbxStretch_None.SetValue(False)

        #TODO
        #if None CHecked():

    def UpdateImageData1(self):
        # self.EdgesCheck = self.chbxEdges.IsChecked()
        # self.ColorsCheck = self.chbxColorImage.IsChecked()
        # self.MonochromeCheck = self.chbxMonochrome.IsChecked()
        #
        # self.MultipleCheck = self.chbxMultiple.IsChecked()
        # print(self.chbxMultiple.IsChecked())
        # self.AllCheck = self.chbxAllColors.IsChecked()
        # print(self.chbxAllColors.IsChecked())
        # self.SelectCheck = self.chbxSelectColors.IsChecked()
        # print(self.chbxSelectColors.IsChecked())

        self.pathnames_1 = self.pathnames_1
        self.pathname_1 = self.pathname_1

        #I love conditional statements. :)

        print("pathname_1", self.pathname_1)
        print("corpus_progression", self.corpus_progression)

        #If it's a midifile, we converter.parse() it.
        self.stream_1 = music21.converter.parse(self.pathname_1) if not \
            self.pathname_1 == self.corpus_progression else music21.corpus.parse(self.pathname_1)
            #If it's a corpurs\other file, we corpus.parse() it.

        #TODO Create workaround that details with the odd corpus loads. 02/13/2024
        #https://web.mit.edu/music21/doc/moduleReference/moduleCorpus.html#music21.corpus.parse

        print("Parsing midi or corpus file....")

        #If it's a corpus\other file, we chordify() it so the progressions are chord-wise correct.
        #inPlace=True
        self.stream_1 = self.stream_1.chordify() if not \
            self.pathname_1 == self.corpus_progression else self.stream_1

        music21funcs.compress_durations(self.stream_1)


        self.img_1 = midiart.make_pixels_from_midi(self.stream_1, color=(109, 255, 0), background_color=(0, 0, 0))
        print("img_1:DTYPE", self.img_1.dtype)

        #self.img2_1 = midiart.make_pixels_from_midi()

        # self.img_1 = cv2.imread(self.pathname_1, 0)  # 2D array (2D of only on\off values.)
        # self.img2_1 = cv2.imread(self.pathname_1,
        #                        cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
        # # print(type(self.img))

        self.img_name_1 = os.path.basename(self.pathname_1)
        print("Image Data1 Updated.")


    def UpdateImageData2(self):
        # self.EdgesCheck = self.chbxEdges.IsChecked()
        # self.ColorsCheck = self.chbxColorImage.IsChecked()
        # self.MonochromeCheck = self.chbxMonochrome.IsChecked()
        #
        # self.MultipleCheck = self.chbxMultiple.IsChecked()
        # print(self.chbxMultiple.IsChecked())
        # self.AllCheck = self.chbxAllColors.IsChecked()
        # print(self.chbxAllColors.IsChecked())
        # self.SelectCheck = self.chbxSelectColors.IsChecked()
        # print(self.chbxSelectColors.IsChecked())

        #This function has stream and image data now. #TODO Fix?

        self.pathnames_2 = self.pathnames_2
        self.pathname_2 = self.pathname_2

        print("pathname2", self.pathname_2)

        self.stream_2 = self.pathname_2
        self.stream_2 = music21.converter.parse(self.pathname_2) if self.DirectoryFlag else self.stream_2


        if self.stream_2 is not None:
            print("self.stream_2")
            self.stream_2.show('txt')
            print("LENGTH_self.stream_2", len([i for i in self.stream_2.flat.notes]))

            self.stream_2.makeMeasures(inPlace=True)

            print("LENGTH0_self.stream_2", len([i for i in self.stream_2.flat.notes]))
            music21funcs.compress_durations(self.stream_2)
        else:
            pass

        self.img_2 = midiart.make_pixels_from_midi(self.stream_2, color=(0,183,255), background_color=(0, 0, 0)) \
            if not self.MidiartGlobalsFlag else\
            super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails[self.image_list_counter_2]


        #self.img2_2 = midiart.make_pixels_from_midi()

        # self.img_2 = cv2.imread(self.pathname_2, 0)  # 2D array (2D of only on\off values.)
        # self.img2_2 = cv2.imread(self.pathname_2,
        #                        cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
        # # print(type(self.img))

        self.img_name_2 = os.path.basename(self.pathname_2) if self.DirectoryFlag else None

        #TODO Add GLOBALS into account here. 01/20/2024
        #TODO Skip non .mid files. 01/20/2024
        self.txtctrlCurrentFile.SetValue(self.img_name_2) if self.DirectoryFlag else None
        print("Image Data2 Updated.")

    def onCycleNext1(self, event):
        self.image_list_counter_1 += 1
        if self.image_list_counter_1 > len(self.pathnames_1) - 1:
            self.image_list_counter_1 = 0
        print("counter:", self.image_list_counter_1)
        self.pathname_1 = self.pathnames_1[self.image_list_counter_1]
        self.UpdateImageData1()
        self.UpdatePreview1()

    def onCyclePrevious1(self, event):
        self.image_list_counter_1 -= 1
        if self.image_list_counter_1 < 0:
            self.image_list_counter_1 = len(self.pathnames_1) - 1
        print("counter:", self.image_list_counter_1)
        self.pathname_1 = self.pathnames_1[self.image_list_counter_1]
        self.UpdateImageData1()
        self.UpdatePreview1()

    def onCycleNext2(self, event):
        self.image_list_counter_2 += 1

        if not self.MusicodeGlobalsFlag and not self.Midiart3DGlobalsFlag:
            self.pathnames_2 = super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails \
                if self.MidiartGlobalsFlag else self.pathnames_2
            print("1-Self.pathnames_2", self.pathnames_2)
        else:
            self.pathnames_2 = super().GetParent().GetTopLevelParent().mayavi_view.MusicodeGlobals \
                if self.MusicodeGlobalsFlag else super().GetParent().GetTopLevelParent().mayavi_view.Midiart3DGlobals
            print("2-Self.pathnames_2", self.pathnames_2)
        print("3-Self.pathnames_2", self.pathnames_2)

        try:
            if self.image_list_counter_2 > len(self.pathnames_2) - 1:
                self.image_list_counter_2 = 0
            print("counter:", self.image_list_counter_2)
            self.pathname_2 = self.pathnames_2[self.image_list_counter_2]
            self.UpdateImageData2()
            self.UpdatePreview2()
        except Exception as e:
            print("Traceback___Message:")
            print(traceback.format_exc())
            print("Exception", e)


    def onCyclePrevious2(self, event):
        self.image_list_counter_2 -= 1

        if not self.MusicodeGlobalsFlag and not self.Midiart3DGlobalsFlag:
            self.pathnames_2 = super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails \
                if self.MidiartGlobalsFlag else self.pathnames_2
            print("1-Self.pathnames_2", self.pathnames_2)
        else:
            self.pathnames_2 = super().GetParent().GetTopLevelParent().mayavi_view.MusicodeGlobals \
                if self.MusicodeGlobalsFlag else super().GetParent().GetTopLevelParent().mayavi_view.Midiart3DGlobals
            print("2-Self.pathnames_2", self.pathnames_2)
        print("3-Self.pathnames_2", self.pathnames_2)


        try:
            if self.image_list_counter_2 < 0:
                self.image_list_counter_2 = len(self.pathnames_2) - 1
            print("counter:", self.image_list_counter_2)
            self.pathname_2 = self.pathnames_2[self.image_list_counter_2]
            self.UpdateImageData2()
            self.UpdatePreview2()
        except Exception as e:
            print("Traceback___Message:")
            print(traceback.format_exc())
            print("Exception", e)


    def UpdateAttritutes1(self):
        # self.pixScaler = int(
        #     8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        #self.height = int(self.sldrHeight.GetValue())
        self.height_1 = 313
        self.width_1 = 1111    #  int(self.height_1 / len(self.img_1) * len(self.img_1[0])) #1111

        cv2.imwrite(r".\resources\intermediary_path" + "\img_1.png", self.img_1)

        # Core Images for passing.
        self.img_1 = self.img_1.astype(numpy.uint8)
        # self.img_1 = numpy.asarray(self.img_1, dtype='int8')  # <-- convert image to float32

        #self.resizedImg_1 = cv2.resize(self.img_1, (self.width_1, self.height_1), cv2.INTER_AREA)

        #self.resizedImg2_1 = cv2.resize(self.img2_1, (self.width_1, self.height_1), cv2.INTER_AREA)

        # Join with Piano
        self.img_with_piano1 = self.join_with_piano(self.img_1, 128)

    def UpdateAttritutes2(self):
        # self.pixScaler = int(
        #     8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        self.height_2 = int(self.sldrHeight.GetValue())
        self.width_2 = 1111    #  int(self.height_2 / len(self.img_2) * len(self.img_2[0])) #1111

        cv2.imwrite(r".\resources\intermediary_path" + "\img_2.png", self.img_2)


        # Core Images for passing.
        self.img_2 = self.img_2.astype(numpy.uint8)
        # self.img_2 = numpy.asarray(self.img_2, dtype='int8')  # <-- convert image to float32

        #self.resizedImg_2 = cv2.resize(self.img_2, (self.width_2, self.height_2), cv2.INTER_AREA)
        #self.resizedImg2_2 = cv2.resize(self.img2_2, (self.width_2, self.height_2), cv2.INTER_AREA)

        # Join with Piano
        self.img_with_piano2 = self.join_with_piano(self.img_2, 128) if not self.MidiartGlobalsFlag else self.img_2

    def UpdatePreview1(self):

        # TODO Fix the slider resize for all img instances.
        if self.displayImage1:
            self.displayImage1.Destroy()

        self.update_called1 = True

        self.UpdateAttritutes1()

        # This error happens if your image dtype is float; cv2.resize() operates with ints:
        # TypeError: only size-1 arrays can be converted to Python scalars"

        # ass_picture = r"C:\Users\Isaac's\Midas\resources\intermediary_path\ass_picture.png"
        # ass_img = cv2.imread(ass_picture, cv2.IMREAD_COLOR)
        # print("ass_img", ass_img)
        # print("ass_img_type", type(ass_img))
        # print("ass_img_dtype", ass_img.dtype)
        # print("ass_img_shape", ass_img.shape)
        print("img_1", self.img_1)
        print("img_1_type", type(self.img_1))
        print("img_1_dtype", self.img_1.dtype)
        print("img_1_shape", self.img_1.shape)
        # cv2.imshow('assssss', ass_img)
        # cv2.waitKey(0)


        # Preview stuff.
        preview = cv2.resize(self.img_with_piano1, (self.width_1, self.height_1), cv2.INTER_AREA) #self.img2_1
        # self.self.previewImg = cv2.resize(self.resizedImg, (self.pixScaler*width, height), cv2.INTER_AREA)
        # rgb = cv2.cvtColor(self.previewImg, cv2.COLOR_GRAY2RGB)   ###cv2.COLOR_RGB2BGR)   ### ####cv2.COLOR_BGR2HSV)   ### #cv2.COLOR_BGR2RGB

        #if self.chbxShowTransformed.IsChecked():

            # if self.ColorsCheck:
            #     # TODO Swap both above---configuration must be the same for colors import as this.
            #     preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
            #     ##preview = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)
            #
            #     m_v = super().GetParent().m_v
            #
            #     # preview = midiart.set_to_nn_colors(preview, m_v.clr_dict_list[m_v.current_palette_name])
            #
            #     # SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
            #     # NOTE: Since this is the preview, this is the same "force-swap" as above in OnMidiartDialogCLosed() function.
            #     # This lends evidence to the logic that our problem  may NOT be in mainbuttons.py.
            #     # Original
            #     ##print("Default_Color_Palette", m_v.default_color_palette)
            #     # NOTE: This uses default_color_palette, which DOES NOT have floats for color values. Mayavi float colors
            #     # do not work for this preview.
            #     swaprnb = midiart.convert_dict_colors(m_v.current_color_palette, invert=True)  # invert=True)
            #     ##print("Default_Color_Palette_SWAPPED", swaprnb)
            #     print("DEFAULT_COLOR_PALETTE_1--preview.", m_v.current_color_palette)
            #     preview = midiart.set_to_nn_colors(preview, swaprnb)  # m_v.default_color_palette) #
            #
            #     self.previewImg = cv2.resize(preview, (self.pixScaler * self.width * 4, self.height * 4),
            #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
            #
            #     h, w = self.previewImg.shape[:2]
            #
            #     self.preview = wx.Image(w, h, self.previewImg)  # ImageFromData -- deprecated
            #
            #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
            #                                         wx.DefaultPosition,
            #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
            #
            #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
            #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)
            #
            #
            #
            # elif self.EdgesCheck:
            #     # preview = cv2.Canny(preview, 100, 200)
            #     # self.im2 = preview
            #     preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Edges")
            #     self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
            #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
            #
            #     h, w = self.previewImg.shape[:2]
            #
            #     self.preview = wx.ImageFromData(w, h, self.previewImg)
            #
            #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
            #                                         wx.DefaultPosition,
            #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
            #
            #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
            #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)
            #
            #
            # elif self.MonochromeCheck:
            #     preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Monochrome")
            #
            #     # print("PREVIEW MC", preview[1])
            #     # print("PREVIEW MC THRESH", thresh)
            #
            #     self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
            #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
            #
            #     h, w = self.previewImg.shape[:2]
            #     print("Monochrome", self.previewImg)
            #     print("Ndim", self.previewImg.ndim)
            #     self.preview = wx.ImageFromData(w, h, self.previewImg)
            #
            #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
            #                                         wx.DefaultPosition,
            #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
            #
            #     # Overwrite, so any image imported will be converted to black and white.
            #     # Images that users sets to monochrome manually will still be more accurate.
            #     self.resizedImg = preview[0]
            #
            #     # TODO Place this process of transformation in the OnMidiartDialogClosed(). 12/01/20
            #     # (This is preview stuff, so, even though things happen twice, it's neater to have the 'preview'
            #     # and transformation stuff separate.
            #
            #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
            #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)


        # else:
        rgb = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)
        self.preview1 = rgb
        #o_height, o_width = preview[1].shape[:2]
        self.previewImg1 = cv2.resize(self.preview1, (int(self.width_1), int(self.height_1)),
                                      #(int((o_width*313)/o_height), 313),,  #self.pixScaler
                                     cv2.INTER_AREA)  # * 3 increases the size of the preview.

        h, w = self.previewImg1.shape[:2]
        print("H", h)
        print("W", w)
        self.preview1 = wx.ImageFromData(w, h, self.previewImg1)
        #self.preview1 = wx.ImageFromData(w, h, ass_img) #self.previewImg1)


        cv2.imwrite(r".\resources\intermediary_path" + "\previewImg1.png", self.previewImg1)

        self.displayImage1 = wx.StaticBitmap(self.imgPreviewPanel1, -1, wx.Bitmap(self.preview1), wx.DefaultPosition,
                                            (int(self.width_1), int(self.height_1)), wx.ALIGN_CENTER_HORIZONTAL)  # w, h

        print("Preview1 Updated.")

    def UpdatePreview2(self):

        # TODO Fix the slider resize for all img instances.
        if self.displayImage2:
            self.displayImage2.Destroy()

        self.update_called2 = True

        self.UpdateAttritutes2()

        if not self.DirectoryFlag:
            self.img_with_piano2 = cv2.cvtColor(self.img_with_piano2, cv2.COLOR_RGB2BGR)
        # This error happens if your image dtype is float; cv2.resize() operates with ints:
        # TypeError: only size-1 arrays can be converted to Python scalars"

        # Preview stuff.
        #preview = cv2.resize(self.img_2, (self.width_2, self.height_2), cv2.INTER_AREA) #self.img2_2
        ####
        # self.self.previewImg = cv2.resize(self.resizedImg, (self.pixScaler*width, height), cv2.INTER_AREA)
        # rgb = cv2.cvtColor(self.previewImg, cv2.COLOR_GRAY2RGB)   ###cv2.COLOR_RGB2BGR)   ### ####cv2.COLOR_BGR2HSV)   ### #cv2.COLOR_BGR2RGB

        # if self.chbxShowTransformed.IsChecked():

        # if self.ColorsCheck:
        #     # TODO Swap both above---configuration must be the same for colors import as this.
        #     preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        #     ##preview = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)
        #
        #     m_v = super().GetParent().m_v
        #
        #     # preview = midiart.set_to_nn_colors(preview, m_v.clr_dict_list[m_v.current_palette_name])
        #
        #     # SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
        #     # NOTE: Since this is the preview, this is the same "force-swap" as above in OnMidiartDialogCLosed() function.
        #     # This lends evidence to the logic that our problem  may NOT be in mainbuttons.py.
        #     # Original
        #     ##print("Default_Color_Palette", m_v.default_color_palette)
        #     # NOTE: This uses default_color_palette, which DOES NOT have floats for color values. Mayavi float colors
        #     # do not work for this preview.
        #     swaprnb = midiart.convert_dict_colors(m_v.current_color_palette, invert=True)  # invert=True)
        #     ##print("Default_Color_Palette_SWAPPED", swaprnb)
        #     print("DEFAULT_COLOR_PALETTE_1--preview.", m_v.current_color_palette)
        #     preview = midiart.set_to_nn_colors(preview, swaprnb)  # m_v.default_color_palette) #
        #
        #     self.previewImg = cv2.resize(preview, (self.pixScaler * self.width * 4, self.height * 4),
        #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
        #
        #     h, w = self.previewImg.shape[:2]
        #
        #     self.preview = wx.Image(w, h, self.previewImg)  # ImageFromData -- deprecated
        #
        #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
        #                                         wx.DefaultPosition,
        #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
        #
        #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
        #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)
        #
        #
        #
        # elif self.EdgesCheck:
        #     # preview = cv2.Canny(preview, 100, 200)
        #     # self.im2 = preview
        #     preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Edges")
        #     self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
        #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
        #
        #     h, w = self.previewImg.shape[:2]
        #
        #     self.preview = wx.ImageFromData(w, h, self.previewImg)
        #
        #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
        #                                         wx.DefaultPosition,
        #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
        #
        #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
        #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)
        #
        #
        # elif self.MonochromeCheck:
        #     preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Monochrome")
        #
        #     # print("PREVIEW MC", preview[1])
        #     # print("PREVIEW MC THRESH", thresh)
        #
        #     self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
        #                                  cv2.INTER_AREA)  # * 3 increases the size of the preview.
        #
        #     h, w = self.previewImg.shape[:2]
        #     print("Monochrome", self.previewImg)
        #     print("Ndim", self.previewImg.ndim)
        #     self.preview = wx.ImageFromData(w, h, self.previewImg)
        #
        #     self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview),
        #                                         wx.DefaultPosition,
        #                                         (w, h), wx.ALIGN_CENTER_HORIZONTAL)
        #
        #     # Overwrite, so any image imported will be converted to black and white.
        #     # Images that users sets to monochrome manually will still be more accurate.
        #     self.resizedImg = preview[0]
        #
        #     # TODO Place this process of transformation in the OnMidiartDialogClosed(). 12/01/20
        #     # (This is preview stuff, so, even though things happen twice, it's neater to have the 'preview'
        #     # and transformation stuff separate.
        #
        #     # Changes the raised-panel size to fit the exact dimensions of the self.previewImg
        #     # self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)

        # else:
        #rgb = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)
        ####
        #self.preview2 = preview #rgb
        self.previewImg2 = cv2.resize(self.img_with_piano2, (self.width_2, self.height_2),  # self.pixScaler   #*4,*4
                                     cv2.INTER_AREA)  # * 3 increases the size of the preview.

        cv2.imwrite(r".\resources\intermediary_path" + "\previewImg2.png", self.previewImg2)

        h, w = self.previewImg2.shape[:2]
        print("H", h)
        print("W", w)
        self.preview2 = wx.ImageFromData(w, h, self.previewImg2)
        self.displayImage2 = wx.StaticBitmap(self.imgPreviewPanel2, -1, wx.Bitmap(self.preview2), wx.DefaultPosition,
                                            (w, h), wx.ALIGN_CENTER_HORIZONTAL)  # w, h   #*4,*4
        print("Preview2 Updated.")


    def OnSliderChanged(self,event):
        if self.img_2 is not None:
            self.UpdatePreview2()


    def OnLoadMidi(self, evt):
        with wx.FileDialog(self, "Open Midi file", wildcard="Midi files (*.mid)|*.mid",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print(pathname)
            try:
                self.midi = pathname
                self.midi_name = os.path.basename(pathname)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


    def OnLoadMelody(self, evt):
        with wx.FileDialog(self, "Load Melody", wildcard="Midi files (*.mid)|*.mid",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            self.pathname_1 = fileDialog.GetPath()
            self.pathnames_1 = fileDialog.GetPaths()   #[]
            print(self.pathname_1)
            try:
                self.melody = self.pathname_1
                self.melody_name = os.path.basename(self.pathname_1)

                self.txtctrlMelodyLength.SetValue(value=str(len([i for i in
                                                                 music21.converter.parse(self.melody).flat.notes])))

                self.UpdateImageData1()
                self.UpdatePreview1()
            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathname_1)


    def OnLoadMusicode(self, evt):
        with wx.FileDialog(self, "Load Musicode", wildcard="Midi files (*.mid)|*.mid",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            self.pathname_2 = fileDialog.GetPath()
            ###Proceed loading the file(s) chosen by the user
            self.pathnames_2 = fileDialog.GetPaths()   #[]
            if len(self.pathnames_2) > 1:
                # self.chbxMultiple.SetValue(True)
                ##self.chbxMultiple.Enable()        #This disables clickable checking of the box.
                self.pathname_2 = self.pathnames_2[0]
                # First image in the list, then we cycle through use (previous, next) btns.
                self.image_list_counter_2 = 0  # come back here 07/10/2023
            else:
                # self.chbxMultiple.SetValue(False)
                ##self.chbxMultiple.Disable()       #This disables clickable checking of the box.
                self.pathname_2 = self.pathnames_2[0]  ##don't need fileDialog.GetPath() anymore
                self.image_list_counter_2 = 0
            print(self.pathname_2)
            try:
                self.musicode = self.pathname_2
                self.musicode_name = os.path.basename(self.pathname_2)
                self.txtctrlMusicodeLength.SetValue(value=str(len([i for i in music21.converter.parse(
                                                                    self.musicode).makeMeasures(inPlace=False)
                                                                    if len(i) is not 0])))
                                                                    #measures, accounting for the scenario of empty
                                                                    #'spaces' measures

                self.UpdateImageData2()
                self.UpdatePreview2()
            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathname_2)

    def OnLoadProgression(self, evt):
        with wx.FileDialog(self, "Load Progression", wildcard="Midi files (*.mid)|*.mid",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            self.pathname_1 = fileDialog.GetPath()
            self.pathnames_1 = fileDialog.GetPaths()

            #print(pathname)
            try:
                self.progression = self.pathname_1
                #self.progression_stream = music21.converter.parse(self.progression)
                self.progression_name = os.path.basename(self.pathname_1)
                print("Progression_Name", self.progression_name)


                self.UpdateImageData1()
                self.UpdatePreview1()

            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathname_1)


    def OnLoadCorpusProgression(self, evt):
        # Proceed loading the file chosen by the user
        self.pathname_1 = self.listctrl_CorpusBox.GetItemText(evt.Index, 0)   #GetItem,  #fileDialog.GetPath()
        print("pathname_1", self.pathname_1)
        self.pathnames_1 = self.corpus_selection_works_list  #fileDialog.GetPaths()
        print("pathnames_1", self.pathnames_1)

        # print(pathname)
        try:
            self.corpus_progression = self.pathname_1
            # self.progression_stream = music21.converter.parse(self.progression)
            self.corpus_progression_name = os.path.basename(self.pathname_1)
            print("Progression_Name", self.corpus_progression_name)

            self.UpdateImageData1()
            self.UpdatePreview1()

        except IOError:
            wx.LogError("Cannot open file '%s'." % self.pathname_1)


    def OnLoadDirectory(self, evt):
        with wx.FileDialog(self, "Load Directory -- Select a File in this Directory to Load the Entire Directory",
                           wildcard="Midi files (*.mid)|*.mid",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:   # wx.FD_MULTIPLE |

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            #pathnames = fileDialog.GetPaths()
            #print("Pathnames", pathnames)
            #filepathname = fileDialog.GetPath()
            #print(filepathname)
            ###Proceed loading the file(s) chosen by the user
            #self.pathnames_2 = fileDialog.GetPaths()
            #print("Pathnames", self.pathnames_2)
            #if len(self.pathnames_2) > 1:
                # self.chbxMultiple.SetValue(True)
                ##self.chbxMultiple.Enable()        #This disables clickable checking of the box.
            #self.pathname_2 = self.pathnames_2[0]  # First image in the list, then we cycle through use (previous, next) btns.
            self.image_list_counter_2 = 0  # come back here 07/10/2023
            # else:
            #     # self.chbxMultiple.SetValue(False)
            #     ##self.chbxMultiple.Disable()       #This disables clickable checking of the box.
            #     self.pathname_2 = self.pathnames_2[0]  ##don't need fileDialog.GetPath() anymore
            #     self.image_list_counter_2 = 0

            try:
                #self.file = self.pathnames_2   #Won't be necessary, but it's cleaner writing.
                ##
                self.directory_or_globals = fileDialog.GetDirectory()
                print("directory", self.directory_or_globals)
                ##
                self.txtctrlOperandDirectory.SetValue(value=self.directory_or_globals)

                subdir = ""
                parsed = []
                #filepaths = []
                self.pathnames_2 = []
                # Walk directory for files.
                for subd, dirs, files in os.walk(self.directory_or_globals):
                    # This loop loops once.
                    subdir += subd
                    #parsed += [music21.converter.parse(subd + os.sep + file) for file in files]
                    self.pathnames_2 += [subd + os.sep + file for file in files]
                            ###Create constraint for just .mid files.


                print("Pathnames_2", self.pathnames_2)

                #self.image_list_counter_2 = 0  # come back here 07/10/2023

                #self.file = self.pathnames_2[self.image_list_counter_2]
                self.file = fileDialog.GetFilename()
                print("Filename", self.file)

                self.fptf = self.directory_or_globals + os.sep + self.file
                # if len(fileDialog.GetPaths()) == 1:
                #     self.file = fileDialog.GetPaths()[0]
                # else:
                #     print("The mentality with this Load Directory|File feature is to only select one file. Please choose"
                #           "one file in your target folder.")
                self.image_list_counter_2 = self.pathnames_2.index(self.fptf)
                        ###Create constraint for just .mid files.


                print("midi_list_counter", self.image_list_counter_2)

                self.pathname_2 = self.file
                self.txtctrlCurrentFile.SetValue(self.fptf)
                #print("BASE_NAME", os.path.basename(self.pathname_2))

            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathnames_2)
                # print("This load feature requires that you select a midi file. All directory operations will operate on"
                #       " midi files located within this folder; it must be selected by selecting a midi file within it.")

        self.DirectoryFlag = True
        self.MusicodeGlobalsFlag = False
        self.MidiartGlobalsFlag = False
        self.Midiart3DGlobalsFlag = False

    def onLoadMusicodeGlobals(self, evt):
        self.directory_or_globals = super().GetParent().GetTopLevelParent().mayavi_view.MusicodeGlobals

        # for h in self.directory_or_globals:
        #     h.makeMeasures(inPlace=True)
        #
        # for g in self.directory_or_globals:
        #     for i in list(g.recurse()):
        #         print("MusicodeGlobalsOffsets:", i.offset, i)

        self.image_list_counter_2 = 0

        self.DirectoryFlag = False
        self.MusicodeGlobalsFlag = True
        self.MidiartGlobalsFlag = False
        self.Midiart3DGlobalsFlag = False
        print("Musicode Globals Loaded. Variable list set.")

    def onLoadMidiartGlobals(self, evt):
        self.directory_or_globals = super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobals

        self.image_list_counter_2 = 0

        self.DirectoryFlag = False
        self.MusicodeGlobalsFlag = False
        self.MidiartGlobalsFlag = True
        self.Midiart3DGlobalsFlag = False
        print("Midiart Globals Loaded. Variable list set.")

    def onLoadMidiart3DGlobals(self, evt):
        self.directory_or_globals = super().GetParent().GetTopLevelParent().mayavi_view.Midiart3DGlobals

        self.image_list_counter_2 = 0

        self.DirectoryFlag = False
        self.MusicodeGlobalsFlag = False
        self.MidiartGlobalsFlag = False
        self.Midiart3DGlobalsFlag = True
        print("Midiart3D Globals Loaded. Variable list set.")


    def OnGenerate_MuseNet_Midi(self, event):
        #self.midi = self.muse_net.Generate(prompt="user midi selection\plane\midi_file\etc....")
        print("Generating MuseNet Midi....not implemented yet though!")
        self.btnGenerate_MuseNet.Disable()
        self.inputTxt.Disable()
        #pass


    def join_with_piano(self, image, height, piano=r".\resources\ThePhatPiano16.png"):
        image = image
        piano = cv2.imread(piano)  # Remember, cv2.imread swaps rgb to bgr.

        height = height #MIDAS_Settings.noteHeight
        width = int(height / len(piano) * len(piano[0]))

        piano = cv2.resize(piano, (width, height), cv2.INTER_AREA)

        print("IMAGE_ndim", image.ndim)
        print("IMAGE_shape", image.shape)
        # piano = cv2.cvtColor(piano, cv2.COLOR_BGR2RGB)   #Keep an EYE on this thang.
        # if len(image) > 127:
        # print("The .png file size is too large. Scaling to height of 127.")
        # height = 127
        # width = int(127 / len(image) * len(image[0]))
        # resizedImg = cv2.resize(image, (width, height), cv2.INTER_AREA)
        musicode_image = numpy.hstack([piano, image])
        return musicode_image


    def onRandomMelody(self, evt):
        try:
            random_stream = midiart.generate_random_melody()

            music21funcs.compress_durations(random_stream)    #TODO Fix.

            self.img_1 = midiart.make_pixels_from_midi(random_stream, color=(109, 255, 0),
                                                                      background_color=(0, 0, 0))
            self.UpdatePreview1()

        except Exception as e:
            print("Traceback___Message:")
            print(traceback.format_exc())
            print("Exception_oRMelody", "You messed up.")
            print(e)


    def onRandomProgression(self, evt):
        try:
            progression_stream = midiart.generate_random_progression()

            print("Prog_stream_length1", len([i for i in progression_stream.flat.notes]))

            progression_stream2 = music21funcs.chop_up_notes(progression_stream, offset_interval=.125)

            #music21funcs.compress_durations(progression_stream)   #TODO Fix.

            print("Prog_stream", type(progression_stream))
            print("Prog_stream_length2", len([i for i in progression_stream.flat.notes]))

            self.img_1 = midiart.make_pixels_from_midi(progression_stream2, color=(109, 255, 0),
                                                                           background_color=(0, 0, 0))
            print("self.img_1", type(self.img_1))

            self.UpdatePreview1()

        except Exception as e:
            print("Traceback___Message:")
            print(traceback.format_exc())
            print("Exception_oRMusicode", "You messed up.")
            print(e)


    def onSplitMidiChannels(self, evt):
        # #music21funcs.split_midi_channels(self.stream_2, )
        print("Splitting Midi Channels, writing to new directory TODO!")
        print(self.txtctrlOutputDirectory.GetValue())
        print(type(self.txtctrlOutputDirectory.GetValue()))
        print("Current_File", self.txtctrlCurrentFile.GetValue())
        split_number = 1
        if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
            directory = r".\resources\intermediary_path\Split_Outputs_%s" % split_number + os.sep
            if os.path.exists(directory) is False:
                os.mkdir(directory)
            #os.mkdir(directory)
            music21funcs.split_midi_channels(self.txtctrlCurrentFile.GetValue(),
                                             directory, self.file)   ####, to_file=True)
        else:
            if os.path.exists(self.txtctrlOperandDirectory.GetValue() + os.sep +
                                             self.txtctrlOutputDirectory.GetValue()) is False:
                os.mkdir(self.txtctrlOperandDirectory.GetValue() + os.sep +
                                             self.txtctrlOutputDirectory.GetValue())
            music21funcs.split_midi_channels(self.txtctrlCurrentFile.GetValue(),
                                             self.txtctrlOperandDirectory.GetValue() + os.sep +
                                             self.txtctrlOutputDirectory.GetValue(),
                                             self.file)   ##,to_file=True
        split_number += 1



    def onProgressifyDirectory(self, evt):

        #TODO Stretch needs multiple checkboxes for different stretches: 01/31/24
        #   1. Operand_Stream stretched to Progression_Stream
        #   2. Progression_Stream stretched to Operand_Stream
        #   3. No Stretch. Operand stream stays put in length, and only the spans that overlap directly from prog_stream
        #                  Will Dictate the filtering.

        our_stretch = None

        if self.chbxStretch_Progression.IsChecked():
            stretch_progression = True
        else:
            stretch_progression = False

        if self.chbxDirectory_Stretch.IsChecked():
            our_stretch = True

        elif self.chbxStream_Stretch.IsChecked():
            our_stretch = False

        elif self.chbxStretch_None.IsChecked():
            our_stretch = None

        print("Our_Stretch", our_stretch)

        zero_velocity = False if not self.chbxZero_Velocity.IsChecked() else True



        if self.directory_or_globals:
            print("DIRECTORY", self.directory_or_globals)

            try:
                if self.stream_1:
                    print("self.stream_1", self.stream_1)
                    self.stream_1.show('txt')
                    print("between_stream")
                    self.stream_1.flat.show('txt')
                    print("after_stream")

                if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
                    midiart.progressify_directory(self.directory_or_globals,
                                                  progression_stream=self.stream_1,
                                                  stretch=our_stretch,
                                                  stretch_progression=stretch_progression,
                                                  zero_velocity=zero_velocity)   #file_path=self.directory
                    print("HERE_1")
                else:
                    output_directory = \
                        self.txtctrlOperandDirectory.GetValue() + os.sep + self.txtctrlOutputDirectory.GetValue()
                    if os.path.exists(output_directory) is False:
                        os.mkdir(output_directory)
                    midiart.progressify_directory(self.directory_or_globals,
                                                  progression_stream=self.stream_1,
                                                  file_path=output_directory,
                                                  stretch=our_stretch,
                                                  stretch_progression=stretch_progression,
                                                  zero_velocity=zero_velocity)
                    print("HERE_2")
            except AttributeError as e:
                print("Attribute Error", e)
                print("You must 'Load Progression' first.")
                pass
            # except AttributeError as e:
            #     print("Attribute Error", e)
            #     if self.stream_2:
            #         print("self.stream_2", self.stream_2)
            #         self.stream_2.show('txt')
            #         print("between_stream")
            #         self.stream_2.flat.show('txt')
            #         print("after_stream")
            #
            #         if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
            #             midiart.progressify_directory(self.directory_or_globals,
            #                                           progression_stream=self.stream_2)  # file_path=self.directory
            #             print("HERE_1")
            #         else:
            #             output_directory = \
            #                 self.txtctrlOperandDirectory.GetValue() + os.sep + self.txtctrlOutputDirectory.GetValue()
            #             if os.path.exists(output_directory) is False:
            #                 os.mkdir(output_directory)
            #             midiart.progressify_directory(self.directory_or_globals,
            #                                           progression_stream=self.stream_2,
            #                                           file_path=output_directory)
        else:
            print("You must 'Load Directory|File' first.")
    # else:
    #     if self.directory_or_globals:
    #         print("DIRECTORY", self.directory_or_globals)
    #
    #         try:
    #             if self.stream_1:
    #                 print("self.stream_1", self.stream_1)
    #                 self.stream_1.show('txt')
    #                 print("between_stream")
    #                 self.stream_1.flat.show('txt')
    #                 print("after_stream")
    #
    #             if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
    #                 midiart.progressify_directory(self.directory_or_globals,
    #                     progression_stream=self.stream_1, stretch=False)    # file_path=self.directory
    #                 print("HERE_1")
    #             else:
    #                 output_directory = \
    #                     self.txtctrlOperandDirectory.GetValue() + os.sep + self.txtctrlOutputDirectory.GetValue()
    #                 if os.path.exists(output_directory) is False:
    #                     os.mkdir(output_directory)
    #                 midiart.progressify_directory(self.directory_or_globals,
    #                                               progression_stream=self.stream_1,
    #                                               file_path=output_directory, stretch=False)
    #                 print("HERE_2")
    #         except AttributeError as e:
    #             print("Attribute Error", e)
    #             print("You must 'Load Progression' first.")
    #             pass
    #     else:
    #         print("You must 'Load Directory|File' first.")

    def onFilterDirectory(self, evt):

        colors_only_directory = False if not self.chbxColorsOnly.IsChecked() else True

        zero_velocity = False if not self.chbxZero_Velocity.IsChecked() else True

        if self.directory_or_globals:
            print("DIRECTORY", self.directory_or_globals)
            # if self.stream_1:
            #     print("self.stream_1", self.stream_1)
            #     self.stream_1.show('txt')
            #     print("between_stream")
            #     self.stream_1.flat.show('txt')
            #     print("after_stream")

            if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
                midiart.filter_directory_to_key(self.directory_or_globals,
                                                key=self.txtctrlKey.GetValue(),
                                                file_path=self.directory_or_globals,
                                                colors_only_directory=colors_only_directory,
                                                zero_velocity=zero_velocity)
                                                #progression_stream=self.stream_1)
                print("HERE_1")
            else:
                output_directory = \
                    self.txtctrlOperandDirectory.GetValue() + os.sep + self.txtctrlOutputDirectory.GetValue()
                if os.path.exists(output_directory) is False:
                    os.mkdir(output_directory)
                midiart.filter_directory_to_key(self.directory_or_globals,
                                                key=self.txtctrlKey.GetValue(),
                                                file_path=output_directory,
                                                colors_only_directory=colors_only_directory,
                                                zero_velocity=zero_velocity)
                                                #progression_stream=self.stream_1,
                print("HERE_2")
            # else:
            #     print("You must 'Load Progression' first.")
        else:
            print("You must 'Load Directory|File' first.")
        pass


    def onSnapDirectory(self, evt):

        colors_only_directory = False if not self.chbxColorsOnly.IsChecked() else True

        if self.directory_or_globals:
            print("DIRECTORY", self.directory_or_globals)
            # if self.stream_1:
            #     print("self.stream_1", self.stream_1)
            #     self.stream_1.show('txt')
            #     print("between_stream")
            #     self.stream_1.flat.show('txt')
            #     print("after_stream")

            if self.txtctrlOutputDirectory.GetValue() == "Your Output Directory Choice" or "":
                midiart.snap_directory_to_key(self.directory_or_globals,
                                              key =self.txtctrlKey.GetValue(),
                                              #progression_stream=self.stream_1)  # file_path=self.directory
                                              file_path=self.directory_or_globals,
                                              colors_only_directory=colors_only_directory)
                print("HERE_1")

            else:
                output_directory = \
                    self.txtctrlOperandDirectory.GetValue() + os.sep + self.txtctrlOutputDirectory.GetValue()
                if os.path.exists(output_directory) is False:
                    os.mkdir(output_directory)
                midiart.snap_directory_to_key(self.directory_or_globals,
                                              key =self.txtctrlKey.GetValue(),
                                              #progression_stream=self.stream_1,
                                              file_path=output_directory,
                                              colors_only_directory=colors_only_directory)
                print("HERE_2")

            # else:
            #     print("You must 'Load Progression' first.")
        else:
            print("You must 'Load Directory|File' first.")
        pass


    def onProgressify(self, evt):

        zero_velocity = False if not self.chbxZero_Velocity.IsChecked() else True

        print("Progressifying....")
        print("DIRECTORY2", self.directory_or_globals)

        midi_file = self.txtctrlCurrentFile.GetValue()
        # midi_file = music21funcs.change_midi_channels_to_one_channel(midi_file, 1)


        stream = music21.converter.parse(midi_file, quantizePost=True,
                                                    quarterLengthDivisors=(8,6),
                                                    makeNotation=True,
                                                    forceSource=True)


        midiart.progressify(vm_stream=stream, progression_stream=self.stream_1,
                            file_path=self.directory_or_globals,
                            file_name="PROGRESSIFIED_00%s_" % self.progressify_counter + self.file,
                            zero_velocity=zero_velocity)

        print("Progressified....")
        self.progressify_counter += 1


    def onAlignMusicodeWithMelody(self, evt):
        try:
            #Left off here.... Remember to clean up between 1s and 2s.
            #self.stream_2.makeMeasures(inPlace=True)
            # print("LENGTH2_self.stream_2", len([i for i in self.stream_2.flat.notes]))
            # print("Buttons Here0")

            woven_stream = super().GetParent().GetTopLevelParent().musicode. \
                align_musicode_with_melody(self.stream_1, self.stream_2)
            # print("LENGTH3_self.stream_2", len([i for i in woven_stream.flat.notes]))
            woven_stream.show('txt')
            # print("Buttons Here1")
            self.img_2 = midiart.make_pixels_from_midi(woven_stream, color=(0,183,255), background_color=(0, 0, 0))
            #self.UpdateAttritutes2()
            self.UpdatePreview2()

        except Exception as e:
            print("Traceback___Message:")
            print(traceback.format_exc())
            print("Exception_oAMWM", "Musicodes not loaded yet, loading and re-executing now...")
            print(e)
            super().GetParent().GetTopLevelParent().musicode = musicode.Musicode()
            print("Musicodes loaded.")
            woven_stream = super().GetParent().GetTopLevelParent().musicode. \
                align_musicode_with_melody(self.stream_1, self.stream_2)
            woven_stream.show('txt')
            self.img_2 = midiart.make_pixels_from_midi(woven_stream, color=(0,183,255), background_color=(0, 0, 0))
            self.UpdatePreview2()



class Music21ConverterParseDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Traditional Music'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)
        # self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)

        self.help_static = wx.StaticText(self, -1, "Import a midi file or a score file.", style=wx.ALIGN_CENTER)

        self.btnLoadMidi = wx.Button(self, -1, "Load Midi\\Score")

        ## Input text box
        #self.inputTxt = wx.TextCtrl(self, -1, "              Input MuseNet Prompt Here", size=(250, -1),
        #                            style=wx.TE_MULTILINE, name="Generative Prompter Input")
        #self.inputTxt.Disable()
        #self.btnGenerate_MuseNet = wx.Button(self, -1, "MuseNet Midi\nGenerate")
        #self.btnGenerate_MuseNet.Disable()

        # New Actor Checkbox
        self.chbxNewActor = wx.CheckBox(self, -1, "New Actor?")  # ctrlsPanel
        self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())

        #############
        # OpenAI Class
        # self.muse_net = Generate.Muse_Net()

        # Binds
        #self.Bind(wx.EVT_BUTTON, self.OnLoadMidi, self.btnLoadMidi)
        #self.Bind(wx.EVT_BUTTON, self.OnGenerate_MuseNet_Midi, self.btnGenerate_MuseNet)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        #self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        #self.sizer5.Add(self.inputTxt, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        #self.sizer5.Add(self.btnGenerate_MuseNet, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        # sizerMain.Add(sizerHor, 30)
        sizerMain.Add(self.help_static, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizerMain.Add(self.btnLoadMidi, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        #sizerMain.Add(self.sizer5, 0, wx.ALIGN_CENTER | wx.ALL, 30)

        #sizerMain.Add(self.chbxNewActor, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizerCtrls = wx.BoxSizer(wx.VERTICAL)

        self.SetSizerAndFit(sizerMain)




class MusicodeDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Musicode'):
        
        wx.Dialog.__init__(self)

        self.Create(parent, id, title, pos, size, style, name)
        self.parent = parent


        self.MusicodeGlobals = []


        self.textinputPanel = wx.Panel(self, -1, wx.DefaultPosition, (254, 162), style=wx.BORDER_RAISED)

        #MODE
        self.translate_musicode = wx.CheckBox(self, -1, "Translate Musicode")
        self.create_musicode = wx.CheckBox(self, -1, "Create Musicode")
        self.translate_multiline_musicode = wx.CheckBox(self, -1, "Translate Multiline")
        self.translate_multiline_musicode.Enable(enable=False)
        self.tm_tooltip = wx.ToolTip("Translate multiline checked will translate"
                                     " all lines in your text directly to individual midi files.")
        self.translate_multiline_musicode.SetToolTip(self.tm_tooltip)

        self.create_musicode.SetValue(True)  ##Set to 'create' a musicode at the ready by default.

        #Musicode name.
        self.name_static = wx.StaticText(self, -1, "Musicode Name",     style=wx.ALIGN_LEFT)
        self.input_mcname = wx.TextCtrl(self, -1, "Musicode", size=(90, -1), style=wx.TE_CENTER)

        #Shorthand variable name.
        self.sh_static = wx.StaticText(self, -1, "Shorthand", style=wx.ALIGN_LEFT)
        self.input_sh = wx.TextCtrl(self, -1, "mc", size=(30, -1), style=wx.TE_CENTER)

        #Load text button
        loadtxtID = wx.NewIdRef()
        self.loadTxt_Btn = wx.Button(self, loadtxtID, "Load Text File")

        #Supported Characters
        self.supported_static = wx.StaticText(self, -1, ('''Supported Musicode Characters: \n <<<< AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz       ?,;\':-.!\"()[]/       0123456789 >>>>'''), style=wx.ALIGN_CENTER)
        self.generate_musicode_text = wx.CheckBox(self, -1, "Generate Musicode Text")
        #self.generate_musicode_text.SetValue(not self.generate_musicode_text.IsChecked())
        #Input text box
        self.inputTextString = "♫♪♪♪♪♪♪♪♪♪Musicode Text Here♪♪♪♪♪♪♪♪♫"
        self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, self.inputTextString, size=(250, -1), style=wx.TE_MULTILINE, name="Translate\\Create")
        self.musicodeInputTT = wx.ToolTip("Enter Musicode Text Here")

        # self.inpTxt_Tooltip = wx.ToolTip('''Supported Musicode Characters: \n <<<< AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz  ?,;\':-.!\"()[]/  0123456789 >>>>''')
        # self.inputTxt.SetToolTip(self.inpTxt_Tooltip)
        #
        #####
        #Todo Use as possible example question for Robin Dunn when asking about wx Events
        super().GetParent().btn_musicode.Disable()  #These disable\enable calls fix a button highlight bug.
        #*# dlg = wx.ProgressDialog("Loading", "Loading Musicode Libraries...", maximum=12, parent=self,
        #*#                         style = wx.PD_ELAPSED_TIME
        #*#                               | wx.PD_REMAINING_TIME
        #*#                               | wx.PD_AUTO_HIDE
        #*#                         )

        dlg = super().GetParent().GetTopLevelParent().statusbar.gauge
        print("DLG", dlg)

        #super().GetParent().btn_musicode.SetFocusfromKbd()
        if self.parent.musicode == None:
            self.parent.GetTopLevelParent().musicode = self.parent.musicode = musicode.Musicode()
            self.parent.musicode.SetupDefaultMidiDictionaries(wx_progress_updater=dlg)

        else:
            pass
        #*#dlg.Destroy()
        dlg.SetValue(11)
        sleep(.53)
        dlg.SetValue(11.25)
        sleep(.53)
        dlg.SetValue(11.5)
        sleep(.53)
        dlg.SetValue(11.75)
        dlg.SetValue(12)
        sleep(.53)
        # sleep(.55)
        # dlg.SetValue(12.5)
        # sleep(.55)
        #dlg.SetValue(0)
        super().GetParent().btn_musicode.Enable()
        #####

        #super().GetParent().btn_musicode.SetFocus()
        #super().GetParent().HighlightSizerItem(super().GetParent().btn_musicode, super().GetParent().main_buttons_sizer, penWidth=2)


        # The string name of the user's making referring to the name of their musicode.
        # self.user_named = super().GetParent().GetTopLevelParent().musicode.musicode_name  #Thith is the coolest thing I have ever theen.
        self.user_named = self.parent.musicode.musicode_name  # Thith is the coolest thing I have ever theen.
        print("user_named", self.user_named)

        #Necessary calls to update self.rdbtnMusicodeChoice
        self.musicodesList = sorted(list(self.parent.musicode.shorthand.keys()))
        self.musicodesList.append(self.user_named)

        self.btnGenerate_ChatGPT = wx.Button(self, -1, "ChatGPT Response\nGenerate")
        self.btnGenerate_ChatGPT.Disable()


        self.rdbtnMusicodeChoice = wx.RadioBox(self, -1, "Musicode Choice",
                                               wx.DefaultPosition, wx.DefaultSize,
                                               self.musicodesList,
                                               2, wx.RA_SPECIFY_COLS)


        self.rdbtnMusicodeChoice.Enable(enable=False)

        self.chbxToFile = wx.CheckBox(self, -1, "To File?")
        self.chbxToFile.Disable()

        self.btnFullSeries = wx.Button(self, -1, "Full Series to Globals")
        self.btnFullSeries.Disable()
        self.fullseries_tooltip = wx.ToolTip("Translate a full series; your line(s) of text will be translated into all"
                                             "10 primary musicodes and written to 10 individual midi files.")
        self.btnFullSeries.SetToolTip(self.fullseries_tooltip)

        #self.newactor_static =  wx.StaticText(self, -1, ('''New Actor?'''), style=wx.ALIGN_CENTER)
        self.chbxNewActor = wx.CheckBox(self, -1, "New Actor?")  #ctrlsPanel
        self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())


        # Input text box
        # self.inputTxt = wx.TextCtrl(self, -1, "              Input MuseNet Prompt Here", size=(250, -1),
        #                             style=wx.TE_MULTILINE, name="Generative Prompter Input")
        # self.inputTxt.Disable()

        ##############
        # OpenAI Class
        self.chat_gpt = Generate.Chat_GPT()


        #"♫♪♪♪♪♪♪♪Generative Prompt Here♪♪♪♪♪♪♫"

        #Bindings.
        self.Bind(wx.EVT_CHECKBOX, self.OnPolarizeCheckboxes)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxes2, self.generate_musicode_text)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate_ChatGPT_Response, self.btnGenerate_ChatGPT) #, self.generate_musicode_text)
        self.Bind(wx.EVT_BUTTON, self.OnFullSeries, self.btnFullSeries)
        self.Bind(wx.EVT_BUTTON, self.OnLoadTextFile, id=loadtxtID)



        #Sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        #self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        # self.sizer5.Add(self.inputTxt, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        #self.sizer5.Add(self.btnGenerate_ChatGPT, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        #Sizer adds.
        self.sizer2.Add(self.translate_musicode, 0, wx.ALL | wx.ALIGN_TOP, 20)
        self.sizer2.Add(self.create_musicode, 0, wx.ALL | wx.ALIGN_TOP, 20)

        self.sizer3.Add(self.name_static, 15, wx.ALL | wx.ALIGN_LEFT, 5)
        self.sizer3.Add(self.input_mcname, 10, 10, 10)

        self.sizer4.Add(self.sh_static, 15, wx.ALL | wx.ALIGN_LEFT, 5)
        self.sizer4.Add(self.input_sh, 10, 50, 10)

        self.btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != "__WXMSW__":
            self.btn = wx.ContextHelpButton(self)
            self.btnsizer.AddButton(self.btn)
        self.btn = wx.Button(self, wx.ID_OK)
        self.btn.SetDefault()
        self.btnsizer.AddButton(self.btn)
        self.btn = wx.Button(self, wx.ID_CANCEL)
        self.btnsizer.AddButton(self.btn)
        self.btnsizer.Realize()

        self.sizer.Add(self.sizer2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.sizer.Add(self.translate_multiline_musicode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.sizer.Add(self.sizer3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.sizer.Add(self.sizer4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.sizer.Add(self.loadTxt_Btn, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.sizer.Add(self.supported_static, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.Add(self.textinputPanel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10) #20
        self.sizer.Add(self.generate_musicode_text, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.Add(self.btnGenerate_ChatGPT, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.Add(self.rdbtnMusicodeChoice, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.AddSpacer(5)
        self.sizer.Add(self.chbxToFile, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.Add(self.btnFullSeries, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.sizer.AddSpacer(30)
        self.sizer.Add(self.chbxNewActor, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, -5)
        self.sizer.Add(self.btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        #print("Sizer Children", self.sizer.Children)

        self.SetSizerAndFit(self.sizer)



    def OnLoadTextFile(self, event):
        with wx.FileDialog(self, "Open Text File", wildcard="TXT (*.txt)|*.txt|",
                                                             #"JPG (*.jpg)|*.jpg|",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            self.pathname = fileDialog.GetPath()
            print("Textfile pathname:", self.pathname)
            text_read = open(self.pathname, "r", encoding='utf-8')
            text = text_read.read()
            try:
               self.inputTxt.SetValue(text)
            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathname)
                text_read.close()
            text_read.close()


    def OnGenerate_ChatGPT_Response(self, event):
        assert self.inputTxt.GetValue() is not None or '', "You do not have a string yet. Please type something. :)"
        self.inputTxt.SetValue(self.chat_gpt.Generate(prompt = self.inputTxt.GetLineText(0)))
        print("Chat GPT Response generated.")
        #pass


    def OnFullSeries(self, event):
        self.MusicodeGlobals = []

        assert self.inputTxt.GetValue() is not None or '', "You do not have a string yet. Please type something. :)"
        print("Self.musicodeList", self.musicodesList)
        self.pure_musicodes_list = copy.deepcopy(self.musicodesList)
        self.pure_musicodes_list.pop(-1)
        print("pml", self.pure_musicodes_list)
        print("ml", self.musicodesList)
        for musicode in self.pure_musicodes_list:
            print("Musicode", musicode)
            stream = self.parent.musicode.translate(musicode, self.inputTxt.GetValue())
            self.MusicodeGlobals.append(stream)
            if self.chbxToFile.IsChecked():
                stream.write('mid', r".\resources\intermediary_path" + os.sep + "Full-Series___%s.mid" % musicode)
            else:
                pass

        super().GetParent().GetTopLevelParent().mayavi_view.MusicodeGlobals = self.MusicodeGlobals
        print("Musicode Globals", self.MusicodeGlobals)
        print("Musicode Globals Updated.")


    #TODO Needs work.
    def OnPolarizeCheckboxes(self, event):
        self.inputTextString = self.inputTxt.GetValue()

        if self.create_musicode.IsChecked(): #Click on other one...
            self.translate_musicode.SetValue(not self.create_musicode.IsChecked())
            self.translate_multiline_musicode.SetValue(False)

            self.rdbtnMusicodeChoice.Enable(enable=False)
            self.name_static.Enable(enable=True)
            self.input_mcname.Enable(enable=True)
            self.input_sh.Enable(enable=True)
            self.sh_static.Enable(enable=True)
            self.translate_multiline_musicode.Enable(enable=False)

            self.btnFullSeries.Disable()
            self.chbxToFile.Disable()

            # self.inputTxt.SetWindowStyle(style=wx.TE_LEFT)
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1,  self.inputTextString, size=(250, -1),
                                        style=wx.TE_LEFT,
                                        name="Translate\\Create")
            #self.inputTxt.SetToolTip()
            try:
                self.inputTxt.SetToolTip(self.musicodeInputTT) if self.inputTxt.ToolTip else None
            except Exception as e:
                print("e", e, )
                print("OPCb")
            self.inputTxt.SetValue(self.inputTextString)
            self.textinputPanel.SetSize(253, 27)
            self.textinputPanel.Refresh()
            self.Refresh()
            # self.sizer.Children[3] = self.inputTxt

        elif self.translate_musicode.IsChecked():  #True by default.
            #self.translate_musicode.SetValue(not self.translate_musicode.IsChecked()) #
            self.create_musicode.SetValue(False)
            #self.translate_multiline.SetValue(not self.translate_multiline.IsChecked())

            self.rdbtnMusicodeChoice.Enable(enable=True)
            self.name_static.Enable(enable=False)
            self.input_mcname.Enable(enable=False)
            self.input_sh.Enable(enable=False)
            self.sh_static.Enable(enable=False)
            self.translate_multiline_musicode.Enable(enable=True)

            #self.inputTxt.SetWindowStyle(style=wx.TE_LEFT)
            if self.translate_multiline_musicode.IsChecked():
                self.inputTxt.Destroy()
                self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, self.inputTextString, size=(250, -1),
                                            style=wx.TE_MULTILINE,
                                            name="Translate\\Create")
                try:
                    self.inputTxt.SetToolTip(self.musicodeInputTT) if self.inputTxt.ToolTip else None
                except Exception as e:
                    print("e", e,)
                    print("OPCb")
                self.inputTxt.SetValue(self.inputTextString)

                self.btnFullSeries.Enable()
                self.chbxToFile.Enable()

                self.textinputPanel.SetSize(254, 162)
                self.textinputPanel.Refresh()
                self.Refresh()
            else:
                self.inputTxt.Destroy()
                self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, self.inputTextString, size=(250, -1),
                                            style=wx.TE_LEFT,
                                            name="Translate\\Create")

                try:
                    self.inputTxt.SetToolTip(self.musicodeInputTT) if self.inputTxt.ToolTip else None
                except Exception as e:
                    print("e", e, )
                    print("OPCb")
                self.inputTxt.SetValue(self.inputTextString)

                self.btnFullSeries.Disable()
                self.chbxToFile.Disable()


                self.textinputPanel.SetSize(253, 27)
                self.textinputPanel.Refresh()
                self.Refresh()
                # self.sizer.Children[3] = self.inputTxt

                #def OnCheckboxMultiline(self, event):
        elif self.translate_multiline_musicode.IsChecked():
            self.create_musicode.SetValue(False) #not self.translate_musicode.IsChecked())
            self.translate_musicode.SetValue(True)

            self.rdbtnMusicodeChoice.Enable(enable=True)
            self.name_static.Enable(enable=False)
            self.input_mcname.Enable(enable=False)
            self.input_sh.Enable(enable=False)
            self.sh_static.Enable(enable=False)


        
            # self.inputTxt.SetWindowStyle(style=wx.TE_MULTILINE)
            # self.inputTxt.Destroy()
            # self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter Musicode Text Here", size=(250, -1),
            #                             style=wx.TE_MULTILINE,
            #                             name="Translate\\Create")
            # self.textinputPanel.SetSize(254, 162)
            # self.textinputPanel.Refresh()
            # self.Refresh()
            # self.sizer.Children[3] = self.inputTxt

        # elif self.translate_musicode.GetValue() is False:
        #     self.create_musicode.SetValue(True)
        # elif self.create_musicode.GetValue() is False:
        #     self.translate_musicode.SetValue(True)

    def OnCheckBoxes2(self, evt):
       # self.inputTextString = self.inputTxt.GetValue()
        #print("TEXT_STRING", self.inputTextString)

        if self.generate_musicode_text.IsChecked():
            self.inputTextString = self.inputTxt.GetValue()
            print("TEXT_STRING", self.inputTextString)
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter ChatGPT Text Prompt Here", size=(250, -1),
                                        style=wx.TE_MULTILINE,
                                        name="CHATGPT Prompt Trigger")
            try:
                self.inputTxt.SetToolTip(self.musicodeInputTT) if self.inputTxt.ToolTip else None
            except Exception as e:
                print("e", e, )
                print("OCB2")
            self.textinputPanel.SetSize(254, 162)
            self.textinputPanel.Refresh()
            self.Refresh()
            self.inputTxt.Refresh()

            self.btnGenerate_ChatGPT.Enable(enable=True)


        else:
            #self.inputTextString = self.inputTxt.GetValue()
            print("TEXT_STRING2", self.inputTextString)
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, self.inputTextString, size=(250, -1),
                                        style=wx.TE_LEFT,
                                        name="CHATGPT Prompt Trigger")
            try:
                self.inputTxt.SetToolTip(self.musicodeInputTT) if self.inputTxt.ToolTip else None
            except Exception as e:
                print("e", e, )
                print("OCB2")
            self.inputTxt.SetValue(self.inputTextString)
            self.textinputPanel.SetSize(253, 27)
            self.textinputPanel.Refresh()
            self.Refresh()
            self.inputTxt.Refresh()
            self.btnGenerate_ChatGPT.Disable()
        print("OnCheckBoxes2....")


class CustomColorsListBox(wx.ListCtrl):
    def __init__(self, parent, log):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT
                                   #wx.LC_VIRTUAL |
                                   # wx.LC_NO_HEADER |
                                   #|wx.LC_SINGLE_SEL  #True for this color selection stuff.
                             )

        self.log = log

        self.SetBackgroundColour((100, 100, 100))
        self.SetTextColour((255, 255, 255))

        self.InsertColumn(0, "Color", wx.LIST_FORMAT_CENTER, width=150)

class CustomListBox2(wx.ListCtrl):
    def __init__(self, parent, log):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT,
                                   #wx.LC_VIRTUAL |
                                   # wx.LC_NO_HEADER |
                                   #|wx.LC_SINGLE_SEL  #True for this color selection stuff.
                             name="Corpus Selection Works"
                             )

        #self.log = log

        self.SetBackgroundColour((100, 100, 100))
        self.SetTextColour((255, 255, 255))

        # self.InsertColumn(0, "Location", wx.LIST_FORMAT_CENTER, width=125)
        self.InsertColumn(0, "Musical Peace", wx.LIST_FORMAT_CENTER, width=250)


class MIDIArtDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MidiArt' ):

        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #self.comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "", (20, 20))
        #self.popupCtrl = ListCtrlComboPopup()

        #self.comboCtrl.UseAltPopupWindow(enable=True)

        # It is important to call SetPopupControl() as soon as possible
        #self.comboCtrl.SetPopupControl(self.popupCtrl)
        # Populate using wx.ListView methods (populated with colors)
        #for clrs in midiart.get_color_palettes():
            #self.listCtrl.Append(clrs)
            #self.popupCtrl.AddItem(clrs)
        # One more call for FL Colors:
        #self.popupCtrl.AddItem("FLStudioColors")

        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, (236, 870), style=wx.BORDER_RAISED) #770
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (515, 515), style=wx.BORDER_RAISED)
        self.displayImage = None

        self.MidiartGlobals = []
        self.MidiartGlobalsThumbnails = []
                                                                        #Spaces deliberate here.
        self.static_color = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "Select Color Palette") #self, bug?? size=(100,100),
        #self.static_color = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "              Select Color Palette") #self, bug?? size=(100,100),

        self.listCtrl = CustomColorsListBox(self.ctrlsPanel, log=None)
        #self.listCtrl.InsertItem(0, "FLStudioColors")

        self.index = 1
        for clrs in midiart.get_color_palettes():
            self.listCtrl.InsertItem(self.index, clrs)
            self.index += 1

        print("LISTCTRL_LENGTH:", self.listCtrl.GetItemCount())
        print("ITEM_0", self.listCtrl.GetItemText(0))

        font = wx.Font(9, wx.FONTFAMILY_MODERN, 0, 90, underline=False,
                       faceName="")
        self.btnLoadImage = wx.Button(self.ctrlsPanel, -1, "Load Image(s)")
        self.btnPreviousImage = wx.Button(self.ctrlsPanel, -1, "◄---Prev", size=(83, 17))
        self.btnNextImage = wx.Button(self.ctrlsPanel, -1, "Next---►", size=(83, 17))
        self.chbxShowTransformed = wx.CheckBox(self.ctrlsPanel, -1, "Show Transformed?")
        self.chbxShowTransformed.SetValue(not self.chbxShowTransformed.IsChecked())
        self.btnPreviousImage.SetFont(font)
        self.btnNextImage.SetFont(font)

        #Spaces deliberate here.
        self.exportStatic = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "Multi-Export Options") #self, bug? size=(100,100),
        #self.exportStatic = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "              Multi-Export Options") #self, bug? size=(100,100),

        self.chbxMultiple = wx.CheckBox(self.ctrlsPanel, -1, "Multiple")

        self.chbxEdges = wx.CheckBox(self.ctrlsPanel, -1, "Edges")
        self.chbxColorImage = wx.CheckBox(self.ctrlsPanel, -1, "Color Image")
        self.chbxColorImage.SetValue(not self.chbxColorImage.IsChecked())
        self.chbxMonochrome = wx.CheckBox(self.ctrlsPanel, -1, "Monochrome")

        self.chbxAllColors = wx.CheckBox(self.ctrlsPanel, -1, "All Colors?")

        self.chbxSelectColors = wx.CheckBox(self.ctrlsPanel, -1, "Select Colors?")

        self.btnMultipleToGlobals = wx.Button(self.ctrlsPanel, -1, "Multiple To Globals")
        #self.chbxSelectColors.SetValue(not self.chbxSelectColors.IsChecked())
        self.btnMultipleToGlobals.Disable()

        self.sldrStatic  = wx.StaticText(self.ctrlsPanel, -1, "Height")
        self.sldrHeight = wx.Slider(self.ctrlsPanel, -1, 127, 1, 127, wx.DefaultPosition, (190,40),
                                    wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.txtKey = wx.StaticText(self.ctrlsPanel, -1, "Key", style= wx.ALIGN_RIGHT )
        self.inputKey = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(30, 24), style=wx.TE_CENTER)

        print("inputKey_LABEL", self.inputKey.GetValue()) ##Temporary
        #self.txtKey.GetLabelText()

        self.granularitiesDict = OrderedDict()
        self.granularitiesDict["32nd Note"]      = 0.125
        self.granularitiesDict["16th Note"]      = 0.25
        self.granularitiesDict["8th Note"]       = 0.5
        self.granularitiesDict["Quarter Note"]   = 1
        self.granularitiesDict["Half Note"]      = 2
        self.granularitiesDict["Whole Note"]     = 4

        self.rdbtnGranularity = wx.RadioBox(self.ctrlsPanel, -1, "Granularity",
                                            wx.DefaultPosition, wx.DefaultSize,
                                            list(self.granularitiesDict.keys()),
                                            2, wx.RA_SPECIFY_COLS)

        #self.rdbtnGranularity.


        #Should be disabled unless Multiple? is checked.
        self.chbxConnect = wx.CheckBox(self.ctrlsPanel, -1, "Connect?")

        #This hella speeds things up. You can up the notes in FL Studio
        self.chbxConnect.SetValue(not self.chbxConnect.IsChecked())

        # New Actor Checkbox
        self.chbxNewActor = wx.CheckBox(self.ctrlsPanel, -1, "New Actor?")
        self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())
        #Todo Finish
        self.chbxNewActor.Disable()

        #TODO Change default granularity checked box.

        #self.txtConnectNotes = wx.StaticText(self, -1, "Connect Notes?", style=wx.ALIGN_RIGHT)

        # Input text box
        self.inputTxt = wx.TextCtrl(self, -1, "                                                         Input DALL-E Prompt Here",
                                    size=(500, 70), #250, -1
                                    style=wx.TE_MULTILINE, name="Generative Prompter Input")
        #self.inputTxt.Disable()
        self.btnGenerate_DALL_E = wx.Button(self, -1, "DALL-E Image\nGenerate")
        #self.btnGenerate_DALL_E.Disable()

        ##############
        # OpenAI Class
        self.dall_e = Generate.DALL_E()


        self.Bind(wx.EVT_BUTTON, self.OnLoadImage, self.btnLoadImage)
        self.Bind(wx.EVT_BUTTON, self.OnCyclePrevious, self.btnPreviousImage)
        self.Bind(wx.EVT_BUTTON, self.OnCycleNext, self.btnNextImage)
        self.Bind(wx.EVT_SLIDER, self.OnSliderChanged, self.sldrHeight)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxChanged, self.rdbtnGranularity)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxSelection)  #This methodology is questionable......but it works.

        self.Bind(wx.EVT_BUTTON, self.OnGenerate_Dall_E_Image, self.btnGenerate_DALL_E)
        self.Bind(wx.EVT_BUTTON, self.OnUpdateGlobals, self.btnMultipleToGlobals)

        #self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.OnChangeColor)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnUpdateColor) #Change

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        #colorSizer = wx.BoxSizer(wx.VERTICAL)
        cycleimagesSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerVer = wx.BoxSizer(wx.VERTICAL)

        sizer5 = wx.BoxSizer(wx.VERTICAL)
        sizer5.Add(self.inputTxt, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizer5.Add(self.btnGenerate_DALL_E, 0, wx.ALL | wx.ALIGN_CENTER, 0)



        topSizer.Add(self.static_color, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)  #35 #25
        #sizerCtrls.Add(self.static_color, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        #sizerCtrls.Add(self.comboCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        topSizer.Add(self.listCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0) #-35
        
        topSizer.AddSpacer(25) #50

        #colorSizer.Add(self.chbxColorImage, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        #colorSizer.Add(self.chbxAllColors, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        cycleimagesSizer.Add(self.btnPreviousImage, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        cycleimagesSizer.Add(self.btnNextImage, 0, wx.ALL | wx.ALIGN_CENTER, 20)



        exportSizer.Add(self.chbxMultiple, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        exportSizer2.Add(self.chbxAllColors, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        exportSizer2.Add(self.chbxSelectColors, 0, wx.ALL | wx.ALIGN_CENTER, 3)



        sizerCtrls.Add(topSizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)  #35
        sizerCtrls.Add(self.chbxEdges, 0, wx.ALL | wx.ALIGN_LEFT, 11)
        sizerCtrls.Add(self.chbxColorImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0) #colorSizer
        sizerCtrls.Add(self.chbxMonochrome, 0, wx.ALL | wx.ALIGN_RIGHT, 14)
        sizerCtrls.AddSpacer(25)
        sizerCtrls.Add(self.btnLoadImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.Add(cycleimagesSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -10)
        sizerCtrls.Add(self.chbxShowTransformed, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -10)



        ###NOTE: These space settings are affect by the resolution settings of Windows.
        ###Of particular note is where it says "Change the size of text, apps, and other items"  '%---'
        sizerCtrls.AddSpacer(40)  ####* commented out if res settings changed
        #sizerCtrls.AddSpacer(30)  ####* commented out if res settings changed
        #sizerCtrls.AddSpacer(65)
        sizerCtrls.Add(self.exportStatic, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0) #-25  -15 swap these if res changed
        #sizerCtrls.AddSpacer(5)  ####* commented out if res settings changed
        #sizerCtrls.AddSpacer(1)  ####* commented out if res settings changed

        #sizerCtrls.AddSpacer(40)  ####insterted if resolutions settings are changed

        sizerCtrls.Add(exportSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.AddSpacer(1)
        #sizerCtrls.AddSpacer(20)
        sizerCtrls.Add(exportSizer2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.Add(self.btnMultipleToGlobals, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        sizerCtrls.AddSpacer(35)


        sizerCtrls.Add(self.sldrStatic, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.Add(self.sldrHeight, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.AddSpacer(15)


        keysizer = wx.BoxSizer(wx.HORIZONTAL)
        keysizer.Add(self.txtKey, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        keysizer.Add(self.inputKey, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        sizerCtrls.Add(keysizer, 0, wx.ALIGN_CENTER | wx.ALL, -10)
        sizerCtrls.Add(self.rdbtnGranularity, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        sizerCtrls.Add(self.chbxConnect, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerCtrls.Add(self.chbxNewActor, 0, wx.ALL | wx.ALIGN_CENTER, 25)


        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.ctrlsPanel.SetSizer(sizerCtrls)

        #sizerVer.Add(sizer5, 0, wx.ALIGN_CENTER | wx.ALL, 30)
        sizerVer.Add(self.imgPreviewPanel, 0, wx.ALIGN_CENTER | wx.ALL, 40)
        sizerVer.AddSpacer(45)
        sizerVer.Add(sizer5, 0, wx.ALIGN_CENTER | wx.ALL, 30)

        sizerHor = wx.BoxSizer(wx.HORIZONTAL)
        sizerHor.Add(self.ctrlsPanel, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        sizerHor.Add(sizerVer, 0, wx.ALIGN_CENTER | wx.ALL, 20)


        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(sizerHor, 30)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.SetSizerAndFit(sizerMain)


    def OnLoadImage(self, evt):
        with wx.FileDialog(self, "Open Image File(s)", wildcard="PNG (*.png)|*.png|"
                                                             "JPG (*.jpg)|*.jpg",
                           style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST) as fileDialog: #FD_FILE_MUST_EXIST

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            ###Proceed loading the file(s) chosen by the user
            self.pathnames = fileDialog.GetPaths()
            if len(self.pathnames) > 1:
                #self.chbxMultiple.SetValue(True)
                ##self.chbxMultiple.Enable()        #This disables clickable checking of the box.
                self.pathname = self.pathnames[0] #First image in the list, then we cycle through use (previous, next) btns.
                self.image_list_counter = 0 #come back here 07/10/2023
            else:
                #self.chbxMultiple.SetValue(False)
                ##self.chbxMultiple.Disable()       #This disables clickable checking of the box.
                self.pathname = self.pathnames[0] ##don't need fileDialog.GetPath() anymore
                self.image_list_counter = 0


            print(self.pathname)
            try:
                self.UpdateImageData()
                self.UpdatePreview()
            except IOError:
                wx.LogError("Cannot open file '%s'." % self.pathname)


    def OnGenerate_Dall_E_Image(self, event):
        self.chbxMultiple.SetValue(False)
        self.pathname = self.dall_e.Generate(prompt=self.inputTxt.GetLineText(0)) #self.pathnames[0]  ##don't need fileDialog.GetPath() anymore

        print("DALL_E Image", self.pathname)
        #if self.pathnames:
        try:
            self.pathnames.append(self.pathname)
            #print("Pathnames:", self.pathnames)
            self.image_list_counter = len(self.pathnames) - 1
            self.UpdateImageData()
            self.UpdatePreview()
        except AttributeError as e:
            #print("Attibute Error", e, "Skipping...")
            self.pathnames = []
            self.pathnames.append(self.pathname)
            self.image_list_counter = 0
            self.UpdateImageData()
            self.UpdatePreview()
        print("DALL_E image generated.")
        #pass


    def OnSliderChanged(self,event):
        if self.img is not None:
            self.UpdatePreview()


    def OnRadioBoxChanged(self,event):
        if self.img is not None:
            print("No image selected. Select an image first. :)")
            self.UpdatePreview()


    def UpdateImageData(self):
        self.EdgesCheck = self.chbxEdges.IsChecked()
        self.ColorsCheck = self.chbxColorImage.IsChecked()
        self.MonochromeCheck = self.chbxMonochrome.IsChecked()

        self.MultipleCheck = self.chbxMultiple.IsChecked()
        print(self.chbxMultiple.IsChecked())
        self.AllCheck = self.chbxAllColors.IsChecked()
        print(self.chbxAllColors.IsChecked())
        self.SelectCheck = self.chbxSelectColors.IsChecked()
        print(self.chbxSelectColors.IsChecked())

        self.pathnames = self.pathnames
        self.pathname = self.pathname

        self.img = cv2.imread(self.pathname, 0)  # 2D array (2D of only on\off values.)
        self.img2 = cv2.imread(self.pathname,
                               cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
        # print(type(self.img))
        self.img_name = os.path.basename(self.pathname)
        print("Image Data Updated.")

    def OnCycleNext(self, event):
        self.image_list_counter += 1
        if self.image_list_counter > len(self.pathnames) - 1:
            self.image_list_counter = 0
        print("counter:", self.image_list_counter)
        self.pathname = self.pathnames[self.image_list_counter]
        self.UpdateImageData()
        self.UpdatePreview()


    def OnCyclePrevious(self, event):
        self.image_list_counter -= 1
        if self.image_list_counter < 0:
            self.image_list_counter = len(self.pathnames) - 1
        print("counter:", self.image_list_counter)
        self.pathname = self.pathnames[self.image_list_counter]
        self.UpdateImageData()
        self.UpdatePreview()


    def UpdateAttritutes(self):
        self.pixScaler = int(
            8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        self.height = int(self.sldrHeight.GetValue())
        self.width = int(self.height / len(self.img) * len(self.img[0]))

        # Core Images for passing.
        self.resizedImg = cv2.resize(self.img, (self.width, self.height), cv2.INTER_AREA)
        self.resizedImg2 = cv2.resize(self.img2, (self.width, self.height), cv2.INTER_AREA)


    def UpdatePreview(self):


        #TODO Fix the slider resize for all img instances.
        if self.displayImage:
            self.displayImage.Destroy()

        self.update_called = True


        self.UpdateAttritutes()
        #This error happens if your image dtype is float; cv2.resize() operates with ints:
        # TypeError: only size-1 arrays can be converted to Python scalars"


        #Preview stuff.
        preview = cv2.resize(self.img2, (self.width, self.height), cv2.INTER_AREA)
        #self.self.previewImg = cv2.resize(self.resizedImg, (self.pixScaler*width, height), cv2.INTER_AREA)
        #rgb = cv2.cvtColor(self.previewImg, cv2.COLOR_GRAY2RGB)   ###cv2.COLOR_RGB2BGR)   ### ####cv2.COLOR_BGR2HSV)   ### #cv2.COLOR_BGR2RGB

        if self.chbxShowTransformed.IsChecked():


            if self.ColorsCheck:
                #TODO Swap both above---configuration must be the same for colors import as this.
                preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
                ##preview = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)

                m_v = super().GetParent().m_v

                #preview = midiart.set_to_nn_colors(preview, m_v.clr_dict_list[m_v.current_palette_name])

                #SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
                #NOTE: Since this is the preview, this is the same "force-swap" as above in OnMidiartDialogCLosed() function.
                #This lends evidence to the logic that our problem  may NOT be in mainbuttons.py.
                #Original
                ##print("Default_Color_Palette", m_v.default_color_palette)
                #NOTE: This uses default_color_palette, which DOES NOT have floats for color values. Mayavi float colors
                #do not work for this preview.
                swaprnb = midiart.convert_dict_colors(m_v.current_color_palette, invert=True) #invert=True)
                ##print("Default_Color_Palette_SWAPPED", swaprnb)
                print("DEFAULT_COLOR_PALETTE_1--preview.", m_v.current_color_palette)
                preview = midiart.set_to_nn_colors(preview, swaprnb)  #m_v.default_color_palette) #

                self.previewImg = cv2.resize(preview, (self.pixScaler * self.width * 4, self.height * 4),
                                             cv2.INTER_AREA)  # * 3 increases the size of the preview.

                h, w = self.previewImg.shape[:2]

                self.preview = wx.Image(w, h, self.previewImg) #ImageFromData -- deprecated

                self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                    (w, h), wx.ALIGN_CENTER_HORIZONTAL)

                #Changes the raised-panel size to fit the exact dimensions of the self.previewImg
                #self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)



            elif self.EdgesCheck:
                #preview = cv2.Canny(preview, 100, 200)
                #self.im2 = preview
                preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Edges")
                self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
                                             cv2.INTER_AREA)  # * 3 increases the size of the preview.

                h, w = self.previewImg.shape[:2]

                self.preview = wx.ImageFromData(w, h, self.previewImg)

                self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                    (w, h), wx.ALIGN_CENTER_HORIZONTAL)

                #Changes the raised-panel size to fit the exact dimensions of the self.previewImg
                #self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)


            elif self.MonochromeCheck:
                preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Monochrome")

                #print("PREVIEW MC", preview[1])
                #print("PREVIEW MC THRESH", thresh)

                self.previewImg = cv2.resize(preview[1], (self.pixScaler * self.width * 4, self.height * 4),
                                             cv2.INTER_AREA)  # * 3 increases the size of the preview.

                h, w = self.previewImg.shape[:2]
                print("Monochrome", self.previewImg)
                print("Ndim", self.previewImg.ndim)
                self.preview = wx.ImageFromData(w, h, self.previewImg)

                self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                    (w, h), wx.ALIGN_CENTER_HORIZONTAL)

                #Overwrite, so any image imported will be converted to black and white.
                #Images that users sets to monochrome manually will still be more accurate.
                self.resizedImg = preview[0]

                #TODO Place this process of transformation in the OnMidiartDialogClosed(). 12/01/20
                 # (This is preview stuff, so, even though things happen twice, it's neater to have the 'preview'
                # and transformation stuff separate.

                #Changes the raised-panel size to fit the exact dimensions of the self.previewImg
                #self.imgPreviewPanel.SetSize(self.pixScaler * width * 4, height * 4)
        else:
            rgb = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)
            self.preview = rgb
            self.previewImg = cv2.resize(self.preview, (self.pixScaler * self.width * 4, self.height * 4),
                                         cv2.INTER_AREA)  # * 3 increases the size of the preview.

            h, w = self.previewImg.shape[:2]
            print("H", h)
            print("W", w)
            self.preview = wx.ImageFromData(w, h, self.previewImg)
            self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                (self.width * 4, self.height * 4), wx.ALIGN_CENTER_HORIZONTAL)  #w, h
        print("Preview Updated.")


    def OnCheckBoxSelection(self, event):
        # import inspect
        # for i in inspect.getmembers(event):
        #     print("EVENT", i[0], i[1])
        if self.chbxMonochrome.IsChecked():
            self.MonochromeCheck = True
            self.chbxEdges.SetValue(False)
            self.EdgesCheck = False
            self.chbxColorImage.SetValue(False)
            self.ColorsCheck = False
            self.chbxAllColors.SetValue(False)
            self.chbxSelectColors.SetValue(False)
            self.chbxAllColors.Enable(enable=False)
            self.chbxSelectColors.Enable(enable=False)
        if self.chbxColorImage.IsChecked():
            self.ColorsCheck = True
            self.chbxEdges.SetValue(False)
            self.EdgesCheck = False
            self.chbxMonochrome.SetValue(False)
            self.MonochromeCheck = False
            #self.chbxAllColors.SetValue(True)
            self.chbxAllColors.Enable(enable=True)
            self.chbxSelectColors.Enable(enable=True)
        if self.chbxEdges.IsChecked():
            self.EdgesCheck = True
            self.chbxColorImage.SetValue(False)
            self.ColorsCheck = False
            self.chbxMonochrome.SetValue(False)
            self.MonochromeCheck = False
            self.chbxAllColors.SetValue(False)
            self.chbxSelectColors.SetValue(False)
            self.chbxAllColors.Enable(enable=False)
            self.chbxSelectColors.Enable(enable=False)

        if self.chbxMultiple.IsChecked():
            self.MultipleCheck = True
            self.chbxMultiple.SetValue(True)
            self.btnMultipleToGlobals.Enable()

        if not self.chbxMultiple.IsChecked():
            self.MultipleCheck = False
            self.chbxMultiple.SetValue(False)
            self.btnMultipleToGlobals.Disable()

        if self.chbxSelectColors.IsChecked():
            self.SelectCheck = True
            self.AllCheck = False
            self.chbxSelectColors.SetValue(True)
            self.chbxAllColors.SetValue(False)

        if self.chbxAllColors.IsChecked():
            self.SelectCheck = False
            self.AllCheck = True
            self.chbxSelectColors.SetValue(False)
            self.chbxAllColors.SetValue(True)




        self.UpdatePreview()


        #print("self.edges.shape=", self.edges.shape)

        #self.im = wx.ImageFromBuffer(w, h, rgb)


    def OnUpdateColor(self, event):
        #This is the greatest thing.
        m_v = super().GetParent().m_v
        m_v.current_palette_names = []
        #FLStudio Colors
        #TODO Test color constistency across all views (preview, mayaviview, exported to FL)
        if self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem()) == "FLStudioColors":

            m_v.current_color_palette = midiart.FLStudioColors

            #Convert
            m_v.current_mayavi_palette = \
            midiart.convert_dict_colors(m_v.current_color_palette, invert=False)

            m_v.current_palette_name = "FLStudioColors"
            print("FL Colors Here.")

        #Colors Dicts
        else:
            self.ChangeColor(m_v=m_v)

            m_v.current_palette_name = self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())
            print("3")

        print("Item_Count", self.listCtrl.ItemCount)
        m_v.current_palette_names = [self.listCtrl.GetItemText(i)
                                     for i in range(0, self.listCtrl.ItemCount) if self.listCtrl.IsSelected(i)]
        # This '0' int here in GetItemCount(0) is strange......


        print("Current Palette Name Changed", m_v.current_palette_name)
        print("Current Palette NameS Changed", m_v.current_palette_names)

        self.UpdatePreview()

    def ChangeColor(self, m_v = None):
        m_v = super().GetParent().m_v if m_v is None else m_v

        # Assign Dict.
        m_v.current_color_palette = m_v.clr_dict_list[self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())]

        # Invert tuples.
        # m_v.default_color_palette = midiart.convert_dict_colors(m_v.default_color_palette, invert=True)

        # SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
        # Convert to mayavi floats and necessary compensatory SWAP because of cvt BGR inversion and to make all rest code cleaner.

        m_v.current_mayavi_palette = midiart.convert_dict_colors(m_v.current_color_palette, both=True)  # invert=True)

        # print("MAYAVI PALETTE", m_v.default_mayavi_palette)
        # m_v.default_mayavi_palette = midiart.convert_dict_colors(m_v.default_mayavi_palette, invert=True)
        print("MAYAVI PALETTE", m_v.current_mayavi_palette)
        # palette = \
        # midiart.convert_dict_colors(m_v.default_color_palette, invert=False)
        # Invert tuples.

        # Invert Color Tuples (swap R with B)
        # m_v.default_mayavi_palette = \
        # midiart.convert_dict_colors(m_v.default_color_palette, invert=True)
        # A tuple R\B switch happens here; tuple is inverted.

    def OnUpdateGlobals(self, event):
        self.MidiartGlobals = []
        self.MidiartGlobalsThumbnails = []


        if self.MultipleCheck:
            # if dialog.SelectCheck and dialog.AllCheck:
            print("DUCK1")
            #     print("Pick one or the other.")
            #     pass

            # En Mass Export Directly to File.
            if not self.SelectCheck and self.AllCheck:
                ###Multiple of EVERY Color PER Image.
                ##NOTE: Processing intensive; use wisely.

                print("DUCK2")
                # pathname = dialog.pathname
                for i in self.pathnames:
                    num = 0
                    for j in range(0, self.listCtrl.ItemCount):
                        palette_name = self.listCtrl.GetItemText(j)
                        print("PALETTE_NAME!!!!:", palette_name)
                        # self.pathname = pathname
                        img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                        img2 = cv2.imread(i,
                                          cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                        # height = MIDAS_Settings.noteHeight
                        height = int(self.sldrHeight.GetValue())
                        width = int(height / len(img) * len(img[0]))
                        # print(type(self.img))
                        ###Name without filetype suffix '.png'
                        img_name = os.path.basename(i).partition('.png')[0]
                        # print("IMG_NAME", img_name)
                        resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                        resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                        pixels = resizedImg  # 2D array (2D of only on\off values.)
                        pixels2 = resizedImg2  # 3D array (2D of color tuples)
                        # if dialog.chbxToGlobals:
                        #     self.transform_images(i, (pixels, pixels2), height, img_name, dialog, num,
                        #                           palette_name=palette_name, to_file=False)
                        # if not dialog.chbxToGlobals:
                        stream_1, image_1 = self.transform_images(i, (pixels, pixels2), height, img_name, self, num,
                                                                  to_file=False)
                        num += 1

                        print("Transformed Stream", stream_1)
                        # num += 1
                        self.MidiartGlobals.append(stream_1)
                        self.MidiartGlobalsThumbnails.append(image_1)
                        super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobals = self.MidiartGlobals
                        super().GetParent().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails = self.MidiartGlobalsThumbnails

                        print("Midiart Globals", self.MidiartGlobals)
                        print("Midiart Globals Updated.")
                        print("Midiart Globals Thumbnails", self.MidiartGlobalsThumbnails)
                        print("Midiart Globals Thumbnails Updated.")


            elif self.SelectCheck and not self.AllCheck:
                ### Multiple Of EACH Selected Color PER Image.
                print("DUCK3")
                for k in super().GetParent().m_v.current_palette_names:
                    for i in self.pathnames:
                        num = 0
                        # for j in range(0, dialog.listCtrl.ItemCount):
                        # palette_name = dialog.listCtrl.GetItemText(j)
                        # print("PALETTE_NAME!!!!:", palette_name)
                        # self.pathname = pathname
                        img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                        img2 = cv2.imread(i,
                                          cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                        # height = MIDAS_Settings.noteHeight
                        height = int(self.sldrHeight.GetValue())
                        width = int(height / len(img) * len(img[0]))
                        # print(type(self.img))
                        ###Name without filetype suffix '.png'
                        img_name = os.path.basename(i).partition('.png')[0]
                        # print("IMG_NAME", img_name)
                        resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                        resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                        pixels = resizedImg  # 2D array (2D of only on\off values.)
                        pixels2 = resizedImg2  # 3D array (2D of color tuples)
                        stream_1, image_1 = self.transform_images(i, (pixels, pixels2), height, img_name, self, num,
                                                                  to_file=False)
                        num += 1

                        print("Transformed Stream", stream_1)
                        # num += 1
                        self.MidiartGlobals.append(stream_1)
                        self.MidiartGlobalsThumbnails.append(image_1)
                        super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobals = self.MidiartGlobals
                        super().GetParent().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails = self.MidiartGlobalsThumbnails

                        print("Midiart Globals", self.MidiartGlobals)
                        print("Midiart Globals Updated.")
                        print("Midiart Globals Thumbnails", self.MidiartGlobalsThumbnails)
                        print("Midiart Globals Thumbnails Updated.")

            elif not self.SelectCheck and not self.AllCheck:
                ###Multiple WITHOUT Multiple Colors.

                print("DUCK4")
                num = 0
                for i in self.pathnames:
                    # self.pathname = pathname
                    img = cv2.imread(i, 0)  # 2D array (2D of only on\off values.)
                    img2 = cv2.imread(i,
                                      cv2.IMREAD_COLOR)  # 3D array (2D of color tuples, which makes a 3D array.)
                    # height = MIDAS_Settings.noteHeight
                    height = int(self.sldrHeight.GetValue())

                    width = int(height / len(img) * len(img[0]))
                    # print(type(self.img))
                    ###Name without filetype suffix '.png'
                    img_name = os.path.basename(i).partition('.png')[0]
                    # print("IMG_NAME", img_name)
                    resizedImg = cv2.resize(img, (width, height), cv2.INTER_AREA)
                    resizedImg2 = cv2.resize(img2, (width, height), cv2.INTER_AREA)
                    pixels = resizedImg  # 2D array (2D of only on\off values.)
                    pixels2 = resizedImg2  # 3D array (2D of color tuples)
                    stream_1, image_1 = self.transform_images(i, (pixels, pixels2), height, img_name, self, num, to_file=False)
                    num += 1

                    print("Transformed Stream", stream_1)
                    #num += 1
                    self.MidiartGlobals.append(stream_1)
                    self.MidiartGlobalsThumbnails.append(image_1)
                    super().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobals = self.MidiartGlobals
                    super().GetParent().GetParent().GetTopLevelParent().mayavi_view.MidiartGlobalsThumbnails = self.MidiartGlobalsThumbnails

                    print("Midiart Globals", self.MidiartGlobals)
                    print("Midiart Globals Updated.")
                    print("Midiart Globals Thumbnails", self.MidiartGlobalsThumbnails)
                    print("Midiart Globals Thumbnails Updated.")

    def join_with_piano(self, image, height, piano=r".\resources\ThePhatPiano16.png"):
        image = image
        piano = cv2.imread(piano)  # Remember, cv2.imread swaps rgb to bgr.

        height = height  # MIDAS_Settings.noteHeight
        width = int(height / len(piano) * len(piano[0]))

        piano = cv2.resize(piano, (width, height), cv2.INTER_AREA)

        print("IMAGE_ndim", image.ndim)
        print("IMAGE_shape", image.shape)
        # piano = cv2.cvtColor(piano, cv2.COLOR_BGR2RGB)   #Keep an EYE on this thang.
        # if len(image) > 127:
        # print("The .png file size is too large. Scaling to height of 127.")
        # height = 127
        # width = int(127 / len(image) * len(image[0]))
        # resizedImg = cv2.resize(image, (width, height), cv2.INTER_AREA)
        musicode_image = numpy.hstack([piano, image])
        return musicode_image

        #################

    def transform_images(self, image_path, pxls_tuple, height, img_name, dialog, num, palette_name=None, to_file=True):

        # ***Here.
        filepath = r".\resources\intermediary_path"
        pathname = image_path
        print("PATHNAME", pathname)

        height = height
        img_name = img_name

        pixels = pxls_tuple[0]
        pixels2 = pxls_tuple[1]

        # Test -This was the magical one that found our bug. 11/30/2021
        # pixels2 = cv2.cvtColor(pixels2, cv2.COLOR_BGR2RGB)

        # pixels_resized = dialog.resizedImg

        gran = dialog.granularitiesDict[dialog.rdbtnGranularity.GetString(dialog.rdbtnGranularity.GetSelection())]
        ###MIDAS_Settings.granularity]

        # print("PIXELS", pixels)
        # print("PIXELS2", pixels2)
        # print("PIXELS_RESIZED:", pixels, type(pixels))
        # print("pixel s_shape", np.shape(pixels))

        current_color_palette = super().GetParent().m_v.current_color_palette = super().GetParent().m_v.clr_dict_list[
            palette_name] if palette_name is not None else super().GetParent().m_v.current_color_palette  # TODO Is this used?
        # mayavi_color_palette = self.current_mayavi_palette
        current_palette_name = super().GetParent().m_v.current_palette_name

        if dialog.EdgesCheck:
            # if self.ids.midiart_Choice.text == "Edges":
            print("Transforming Edges!")
            # IMAGE
            self.selection = "Edges"
            self.edges = cv2.Canny(pixels, 100, 200)

            # self.edges2 = cv2.Canny(pixels2, 100, 200)
            # CONCATENATE with PIANO
            self.preview = midiart.cv2_tuple_reconversion(pixels2,
                                                          inPlace=False,
                                                          conversion='Edges')[1]
            self.img_without_piano = self.preview

            self.img_with_piano = self.join_with_piano(self.preview, height)

            # NAME
            self.name = self.selection + "_" + str(num) + "_" + img_name

            # STREAM
            self.stream = midiart.make_midi_from_grayscale_pixels(self.edges,
                                                                  gran,
                                                                  connect=dialog.chbxConnect.GetValue(),
                                                                  ##.connectNotes,
                                                                  note_pxl_value=255)
            ##dialog.inputKey.GetValue(), , colors=False
            print("EdgeStream:", self.stream)
            self.stream.show('txt')

            # name = str(len(m_v.actors)) + "_" + "Edges" + "_" + dialog.img_name
            print("Edges load completed.")

        elif dialog.ColorsCheck:
            # if self.ids.midiart_Choice.text == "Color":
            print("Transforming Color!")
            print("PREPixels2:", pixels2)
            print("Gran", gran)
            print("Here.")
            print("DEFAULT_COLOR_PALETTE_2, import.", current_color_palette)
            # The default_color_palette is the dictionary of colors by which our coords must be sorted.

            # IMAGE
            self.selection = "Colors"
            self.colors = pixels2
            self.nn_colors = midiart.set_to_nn_colors(pixels2, super().GetParent().m_v.current_color_palette)

            self.img_without_piano = self.nn_colors

            # CONCATENATE with PIANO
            self.img_with_piano = self.join_with_piano(self.nn_colors, height)

            # NAME
            if palette_name is None:
                palette_name = current_palette_name
            self.name = self.selection + "_" + str(num) + "_" + palette_name + "_" + img_name
            #     self.name = self.selection +  "_" + str(num) + "_" + dialog.listCtrl.GetItemText(num) + "_" + img_name
            # else:
            #     self.name = self.selection +  "_" + str(num) + "_" + palette_name + "_" + img_name

            # STREAM
            # swaprnb = midiart.convert_dict_colors(MIDAS_Settings.current_color_palette, invert=True)

            swaprnb = super().GetParent().m_v.current_color_palette

            self.stream = midiart.transcribe_colored_image_to_midiart(self.colors,
                                                                      granularity=gran,
                                                                      connect=dialog.chbxConnect.GetValue(),
                                                                      ##MIDAS_Settings.connectNotes,
                                                                      keychoice=dialog.inputKey.GetValue(),
                                                                      colors=swaprnb,
                                                                      output_path=None)
            print("ColorsStream:", self.stream)
            self.stream.show('txt')
            print("Colors load completed.")


        elif dialog.MonochromeCheck:
            # if self.ids.midiart_Choice.text == "Monochrome":
            print("Transforming Monochrome!")
            # IMAGE
            self.selection = "Monochrome"
            self.monochrome = pixels
            # CONCATENATE with PIANO
            conversion = midiart.cv2_tuple_reconversion(pixels2,
                                                        inPlace=False,
                                                        conversion='Monochrome')
            self.preview = conversion[1]
            self.preview2 = conversion[0]
            # list_1 = [tuple(i) for i in self.preview2]
            # list_2 = [tuple(i) for i in self.monochrome]
            # assert list_1 == list_2, print("These are not the same.") assert failed

            self.img_without_piano = self.preview

            self.img_with_piano = self.join_with_piano(self.preview, height)

            # NAME
            self.name = self.selection + "_" + str(num) + "_" + img_name  # "QR-BW"

            # STREAM
            self.stream = midiart.make_midi_from_grayscale_pixels(self.preview2,
                                                                  gran,
                                                                  dialog.chbxConnect.GetValue(),
                                                                  ###MIDAS_Settings.connectNotes,
                                                                  note_pxl_value=0)
            # TODO Temporary
            # self.m_v.CurrentActor()._stream = self.stream

            print("MonochromeStream:", self.stream)
            self.stream.show('txt')
            print("Monochrome load completed.")

        # Strings
        file_path_img = filepath + os.sep + self.name + ".png"  # str
        file_path_img_with_piano = filepath + os.sep + self.name + "_with_piano.png"
        # musicode_default_img = MIDAS_Settings.musicode_default

        # Remove existing, if true
        # if os.path.exists(file_path_img) is True:
        #     shutil.rmtree(file_path_img, ignore_errors=True)
        # if os.path.exists(file_path_img_with_piano) is True:
        #     shutil.rmtree(file_path_img_with_piano, ignore_errors=True)

        ###Midi to file strings
        filepath_midi = filepath + os.sep + "midiart_%s" % self.name + "_" + ".mid" \
            if not dialog.ColorsCheck else \
            filepath + os.sep + "midiart_%s" % self.selection + str(num) + "__%s.mid" \
            % palette_name
        # filepath_midi = filepath + os.sep + "midiart_%s.mid" % self.ids.midiart_Choice.text \
        #     if self.ids.midiart_Choice.text != "Color" else \
        #     filepath + os.sep + "midiart_%s" % self.ids.midiart_Choice.text + "_%s.mid" \
        #     % self.m_v.current_palette_name

        ###Existing file cleanup.
        # if os.path.exists(filepath_midi) is True:
        #     shutil.rmtree(filepath_midi, ignore_errors=True)

        ###Key filtering
        midiart.filter_notes(self.stream, key=dialog.inputKey.GetValue(), in_place=True)

        ###Midi written to file.
        # print("CHOICE", self.ids.midiart_Choice.text)
        # if self.ids.midiart_Choice.text != "Midiart":

        if to_file:
            if dialog.ColorsCheck:
                midiart.set_parts_to_midi_channels(self.stream, filepath_midi)
            else:
                self.stream.write("mid", filepath_midi)
            ##midiart.set_parts_to_midi_channels(self.stream, filepath_midi) \
            ##        if self.ids.midiart_Choice.text == "Color" else self.stream.write("mid", filepath_midi)
            ##else:
            ##    pass

            # Image with midi to file
            # cv2.imwrite(file_path_img, self.img_without_piano)
            cv2.imwrite(file_path_img_with_piano, self.img_with_piano)
            print("SELF.IMAGE_WITH_PIANO", self.img_with_piano)

        return self.stream, self.img_with_piano
        # Update Gui View
        ##self.parent.ids.imagedraw_Area.ids.image_View.source = file_path_img_with_piano
        # self.parent.ids.imagedraw_Area.ids.image_View.reload()
    #################


class MIDIArt3DDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='3idiArt'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #Points
        self.points = numpy.array([[0, 0, 0]])
        self.point_cloud_counter = 0

        self.pointclouds = []

        self.Midiart3DGlobals = []

        #Panels
        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, size=(485,605), style=wx.BORDER_RAISED) #515
        #self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (500, 500), style=wx.BORDER_RAISED)
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (450, 450), style=wx.BORDER_RAISED)

        #Disable main mv window before proceeding

        # super().GetParent().GetTopLevelParent().mayaviviewcontrolpanel.Disable()
        # super().GetParent().GetTopLevelParent().pianorollpanel.pianoroll.Disable()

        # mayavi_view reference override
        self.m_v = super().GetParent().GetTopLevelParent().mayavi_view
        self.m_v.scene3d.disable_render = True

        self.mini_mv = MayaviMiniView(parent=self)
        self.mini = self.mini_mv.edit_traits(parent=self.imgPreviewPanel, kind='subpanel').control

        self.mlab_call = self.m_v.insert_array_data(self.points, color=(1, 1, 0),
                                   figure=self.mini_mv.scene_mini.mayavi_scene,
                                   scale_factor=1)

        #toplevel = super().GetParent().GetTopLevelParent()


        #Help Text
        self.helpStatic = wx.StaticText(self.ctrlsPanel, -1, "Load a point cloud and manipulate it in 3 dimensions "
                                                              "as music \n                      with a "
                                                             "specially designed processing "
                                                              "chain.")

        # self.actorStatic = wx.StaticText(self.ctrlsPanel, -1, "Actor Index")
        # choices = [str(i) for i in range(0, len(super().GetParent().mv.actors))]
        # #cur_ActorIndex Combo Box dropdown.
        # self.cbActorIndices = wx.ComboBox(self.ctrlsPanel, -1, "1", wx.DefaultPosition, wx.DefaultSize,
        #                                   choices=choices,
        #                                   style=wx.CB_DROPDOWN | wx.CB_READONLY)
        # self.Bind(wx.EVT_COMBOBOX, self.OnComboBoxSelection)

        #LoadPly
        self.btnLoadPly = wx.Button(self.ctrlsPanel, -1, "Load Point Cloud(s)")

        # Load Current
        self.chbxCurrentActor = wx.CheckBox(self.ctrlsPanel, -1, "Import Current Actor(s)?")

        #TODO Change this? 06/30/2023
        self.btnLoadPly.SetToolTip(tipString="Load 3D Object(s) from file.")
        #"Load Ply will only be enabled if an actor is empty."

        # Cycle
        font = wx.Font(9, wx.FONTFAMILY_MODERN, 0, 90, underline=False,
                       faceName="")
        # self.btnLoadImage = wx.Button(self.ctrlsPanel, -1, "Load Image(s)")
        self.btnPreviousImage = wx.Button(self.ctrlsPanel, -1, "◄---Prev", size=(83, 17))
        self.btnNextImage = wx.Button(self.ctrlsPanel, -1, "Next---►", size=(83, 17))
        self.btnPreviousImage.SetFont(font)
        self.btnNextImage.SetFont(font)

        # self.OnComboBoxSelection(evt=None)   #self.points is written in this function.
        # Spaces deliberate here.
        self.exportStatic = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "Multi-Export Options") #self
        #self.exportStatic = self.name_static = wx.StaticText(self, -1, "Multi-Export Options") #self
        self.chbxMultiple = wx.CheckBox(self.ctrlsPanel, -1, "Multiple")
        self.chbxPlanes = wx.CheckBox(self.ctrlsPanel, -1, "Planes")
        self.chbxPlanes.Disable()

        self.chbxToFile = wx.CheckBox(self.ctrlsPanel, -1, "To File?")
        self.chbxToFile.Disable()

        self.btnCurrentPlanesToGlobals = wx.Button(self.ctrlsPanel, -1, "Planes to Globals")
        self.btnCurrentPlanesToGlobals.Disable()


        self.axis_Menu1 = wx.Menu()
        self.axis_Menu2 = wx.Menu()
        self.axis_Menu3 = wx.Menu()
        self.axis_Menu4 = wx.Menu()
        self.axis_menu_list = [self.axis_Menu1, self.axis_Menu2, self.axis_Menu3, self.axis_Menu4]
        self.generate_axis_menus()


        #Standard Reorientation
        self.btnStandardReo = wx.Button(self.ctrlsPanel, -1, "Standard Reorientation")
        # pointsVar_Reo = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        ##self.scaleVar_Reo = wx.TextCtrl(self.ctrlsPanel, -1, "1", size=(70, -1), style=wx.TE_CENTER)
        ##self.scaleVar_Reo.Disable()

        # Scale
        self.btnScale = wx.Button(self.ctrlsPanel, -1, "Scale Points")
        self.scaleVar_Scale = wx.TextCtrl(self.ctrlsPanel, -1, "2", size=(70, -1), style=wx.TE_CENTER)

        #Trim
        self.btnTrim = wx.Button(self.ctrlsPanel, -1, "Trim Points")
        # pointsVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        self.axisVar_Trim = wx.Button(self.ctrlsPanel, -1, "y")
        ###wx.Panel(self, -1, wx.DefaultPosition, size=(70, 21), style=wx.BORDER_RAISED)
        ###self.axisMenuTrim = wx.Menu()
        #### self.axisVar_Trim.AddChild(self.axisMenuTrim)
        #### self.generate_axis_menus(self.axisMenuTrim)
        #self.axisVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "y", size=(70, -1), style=wx.TE_CENTER)
        self.trimVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "1", size=(70, -1), style=wx.TE_CENTER)

        #Rotate
        self.btnRotate = wx.Button(self.ctrlsPanel, -1, "Rotate Points")
        # pointsVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        self.axisVar_Rot = wx.Button(self.ctrlsPanel, -1, "x")
        ###wx.Panel(self, -1, wx.DefaultPosition, size=(70, 21), style=wx.BORDER_RAISED)
        ###self.axisMenuRotate = wx.Menu()
       #### self.axisVar_Rot.AddChild(self.axisMenuRotate)
       #### self.generate_axis_menus(self.axisMenuRotate)
        #self.axisVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "y", size=(70, -1), style=wx.TE_CENTER)
        self.degreesVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "90", size=(70, -1), style=wx.TE_CENTER)

        #Transform
        self.btnTransform = wx.Button(self.ctrlsPanel, -1, "Transform Points")
        self.axisVar_Trans = wx.Button(self.ctrlsPanel, -1, "z")
        print("AXISVAR_TRANS --- LABEL", self.axisVar_Trans.GetLabelText())
        ###wx.Panel(self, -1, wx.DefaultPosition, size=(70, 21), style=wx.BORDER_RAISED)
        ###elf.axisMenuTrans = wx.Menu()
        #### self.axisVar_Trans.AddChild(self.axisMenuTrans)
        #### self.generate_axis_menus(self.axisMenuTrans)
        #self.axisVar_Trans = wx.TextCtrl(self.ctrlsPanel, -1, "z", size=(70, -1), style=wx.TE_CENTER)
        self.offsetVar_Trans = wx.TextCtrl(self.ctrlsPanel, -1, "5", size=(70, -1), style=wx.TE_CENTER)

        #Mirror
        self.btnMirror = wx.Button(self.ctrlsPanel, -1, "Mirror Points")
        self.axisVar_Mir = wx.Button(self.ctrlsPanel, -1, "x")
        ###wx.Panel(self, -1, wx.DefaultPosition, size=(70, 21), style=wx.BORDER_RAISED)
        ###self.axisMenuMir = wx.Menu()
        #### self.axisVar_Mir.AddChild(self.axisMenuMir)
        #### self.generate_axis_menus(self.axisMenuMir)
        #self.axisVar_Mir = wx.TextCtrl(self.ctrlsPanel, -1, "x", size=(70, -1), style=wx.TE_CENTER)

        #New Actor Checkbox
        self.chbxNewActor = wx.CheckBox(self.ctrlsPanel, -1, "New Actor?")
        self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())
        #Todo Finish
        self.chbxNewActor.Disable()

        # Input text box
        self.inputTxt = wx.TextCtrl(self, -1, "                                                Input Brief Point-E Prompt Here", size=(450, 35), #250, 1
                                    style=wx.TE_MULTILINE, name="Generative Prompter Input")
        #self.inputTxt.Disable()
        self.btnGenerate_Point_E = wx.Button(self, -1, "Point_E PointCloud\nGenerate")



        ##############
        # OpenAI Class
        try:
            self.point_e = super().GetParent().GetTopLevelParent().point_e  #Generate.Point_E()
        except AttributeError as e:
            print("You computer does not have cuda loaded\installed\configured. Point_E generation components will be disabled.")
            self.inputTxt.Disable()
            self.btnGenerate_Point_E.Disable()

        sizer5 = wx.BoxSizer(wx.VERTICAL)
        sizer5.Add(self.inputTxt, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizer5.Add(self.btnGenerate_Point_E, 0, wx.ALL | wx.ALIGN_CENTER, 0)


        #Bindings
        self.axisVar_Trim.Bind(wx.EVT_BUTTON, self.OnAxisButton1)
        self.axisVar_Rot.Bind(wx.EVT_BUTTON, self.OnAxisButton2)
        self.axisVar_Trans.Bind(wx.EVT_BUTTON, self.OnAxisButton3)
        self.axisVar_Mir.Bind(wx.EVT_BUTTON, self.OnAxisButton4)

        self.Bind(wx.EVT_BUTTON, self.OnLoadPly, self.btnLoadPly)
        self.Bind(wx.EVT_BUTTON, self.OnStandardReorientation, self.btnStandardReo)
        self.Bind(wx.EVT_BUTTON, self.OnTrim, self.btnTrim)
        self.Bind(wx.EVT_BUTTON, self.OnScale, self.btnScale)
        self.Bind(wx.EVT_BUTTON, self.OnRotate, self.btnRotate)
        self.Bind(wx.EVT_BUTTON, self.OnTransform, self.btnTransform)
        self.Bind(wx.EVT_BUTTON, self.OnMirror, self.btnMirror)
        self.Bind(wx.EVT_BUTTON, self.OnCyclePrevious, self.btnPreviousImage)
        self.Bind(wx.EVT_BUTTON, self.OnCycleNext, self.btnNextImage)

        self.Bind(wx.EVT_BUTTON, self.OnGenerate_Point_E_PointCloud, self.btnGenerate_Point_E)
        self.Bind(wx.EVT_BUTTON, self.UpdateGlobals, self.btnCurrentPlanesToGlobals)



        self.Bind(wx.EVT_CHECKBOX, self.OnLoadChange)

        self.Bind(wx.EVT_CHECKBOX, self.OnMultipleChange)


        #self.Bind(wx.EVT_CHECKBOX, self.OnPolarizeCheckboxes)


        #Sizers
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        # indexSizer = wx.BoxSizer(wx.VERTICAL)
        # indexSizer.Add(self.actorStatic, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        # indexSizer.Add(self.cbActorIndices, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        sizerStandardReo = wx.BoxSizer(wx.HORIZONTAL)
        horSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer1.AddSpacer(129)
        #sizerStandardReo.Add(self.btnStandardReo, 0, wx.ALIGN_CENTER, 30)
        #sizerStandardReo.Add(self.btnStandardReo, 0, wx.ALIGN_CENTER, 30)
        # sizerStandardReo.Add(pointsVar_Reo, 0, 50, 20)
        # sizerStandardReo.Add(scaleVar_Reo, 0, 50, 20)
        # horSizer1.Add(pointsVar_Reo, 0, 50, 20)

        ##horSizer1.Add(self.scaleVar_Reo, 0, 50, 20)
        sizerStandardReo.Add(horSizer1, 0, wx.ALIGN_CENTER, 10)

        sizerScale = wx.BoxSizer(wx.HORIZONTAL)
        horSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer3.AddSpacer(187)
        sizerScale.Add(self.btnScale, 0, wx.ALIGN_CENTER, 30)
        # sizerScale.Add(scaleVar_Scale, 0, 50, 20)
        horSizer3.Add(self.scaleVar_Scale, 0, 50, 20)
        sizerScale.Add(horSizer3, 0, wx.ALIGN_CENTER, 10)


        sizerTrim = wx.BoxSizer(wx.HORIZONTAL)
        horSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer2.AddSpacer(135)
        sizerTrim.Add(self.btnTrim, 0, wx.ALIGN_CENTER, 30)
        # sizerTrim.Add(pointsVar_Trim, 0, 50, 20)
        # sizerTrim.Add(axisVar_Trim, 0, 50, 20)
        # sizerTrim.Add(trimVar_Trim, 0, 50, 20)
        # horSizer2.Add(pointsVar_Trim, 0, 50, 20)
        horSizer2.Add(self.axisVar_Trim, 0, 50, 20)
        horSizer2.Add(self.trimVar_Trim, 0, 50, 20)
        sizerTrim.Add(horSizer2, 0, wx.ALIGN_CENTER, 10)


        sizerRotate = wx.BoxSizer(wx.HORIZONTAL)
        horSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer4.AddSpacer(125)
        sizerRotate.Add(self.btnRotate, 0, wx.ALIGN_CENTER, 30)
        # sizerRotate.Add(pointsVar_Rot, 0, 50, 20)
        # sizerRotate.Add(axisVar_Rot, 0, 50, 20)
        # sizerRotate.Add(degreesVar_Rot, 0, 50, 20)
        # horSizer4.Add(pointsVar_Rot, 0, 50, 20)
        horSizer4.Add(self.axisVar_Rot, 0, 50, 20)
        horSizer4.Add(self.degreesVar_Rot, 0, 50, 20)
        sizerRotate.Add(horSizer4, 0, wx.ALIGN_CENTER, 10)


        sizerTransform = wx.BoxSizer(wx.HORIZONTAL)
        horSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer5.AddSpacer(105)
        sizerTransform.Add(self.btnTransform, 0, wx.ALIGN_CENTER, 30)
        horSizer5.Add(self.axisVar_Trans, 0, 50, 20)
        horSizer5.Add(self.offsetVar_Trans, 0, 50, 20)
        sizerTransform.Add(horSizer5, 0, wx.ALIGN_CENTER, 10)


        sizerMirror = wx.BoxSizer(wx.HORIZONTAL)
        horSizer6 = wx.BoxSizer(wx.HORIZONTAL)
        horSizer6.AddSpacer(126)
        sizerMirror.Add(self.btnMirror, 0, wx.ALIGN_CENTER, 30)
        horSizer6.Add(self.axisVar_Mir, 0, 50, 20)
        sizerMirror.Add(horSizer6, 0, wx.ALIGN_CENTER, 10)


        cycleimagesSizer = wx.BoxSizer(wx.HORIZONTAL)
        cycleimagesSizer.Add(self.btnPreviousImage, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        cycleimagesSizer.Add(self.btnNextImage, 0, wx.ALL | wx.ALIGN_CENTER, 20)


        exportSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportSizer.Add(self.chbxMultiple, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        exportSizer.Add(self.chbxPlanes, 0, wx.ALL | wx.ALIGN_CENTER, 3)


        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        sizerCtrls.Add(self.helpStatic, 0, wx.ALL | wx.ALIGN_CENTER, 16)
        #sizerCtrls.Add(indexSizer, 0, wx.ALL | wx.ALIGN_CENTER, 18)

        sizerCtrls.Add(self.btnLoadPly, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerCtrls.Add(self.chbxCurrentActor, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizerCtrls.Add(cycleimagesSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -15)


        sizerCtrls.AddSpacer(35)

        sizerCtrls.Add(self.exportStatic, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        sizerCtrls.Add(exportSizer, 0, wx.ALL | wx.ALIGN_CENTER, 0) #-25
        sizerCtrls.AddSpacer(5)
        sizerCtrls.Add(self.chbxToFile, 0, wx.ALL | wx.ALIGN_CENTER, 0) #-25
        sizerCtrls.Add(self.btnCurrentPlanesToGlobals, 0, wx.ALL | wx.ALIGN_CENTER, 0) #-25


        sizerCtrls.AddSpacer(15)
        ##scale variable box for btnStandardReo taken out, so layout had to be adjusted as well, here.  *##
        sizerCtrls.Add(self.btnStandardReo, 0, wx.ALL | wx.ALIGN_CENTER, 20)  #30

        ##sizerCtrls.Add(sizerStandardReo, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizerCtrls.Add(sizerScale, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        sizerCtrls.Add(sizerTrim, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        sizerCtrls.Add(sizerRotate, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        sizerCtrls.Add(sizerTransform, 0, wx.ALL | wx.ALIGN_LEFT, 10)
        sizerCtrls.Add(sizerMirror, 0, wx.ALL | wx.ALIGN_LEFT, 10)

        sizerCtrls.AddSpacer(30)

        sizerCtrls.Add(self.chbxNewActor, 0, wx.ALL | wx.ALIGN_CENTER, -10)



        # self.ctrlsPanel.SetSizer(indexSizer)
        # self.ctrlsPanel.SetSizer(sizerStandardReo)
        # self.ctrlsPanel.SetSizer(sizerTrim)
        # self.ctrlsPanel.SetSizer(sizerScale)
        # self.ctrlsPanel.SetSizer(sizerRotate)
        #sizeCtrlsn.Add(self.btnRedrawMayaviView, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        #sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 1)

        sizerVer = wx.BoxSizer(wx.VERTICAL)
        sizerVer.Add(self.imgPreviewPanel, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizerVer.AddSpacer(20)
        sizerVer.Add(sizer5, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizerHor = wx.BoxSizer(wx.HORIZONTAL)
        sizerHor.Add(self.ctrlsPanel, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizerHor.Add(sizerVer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        #self.mini.FitInside()
        #print("SIZE", self.mini.Size)
        #self.mini_mv.remove_highlighter_plane()
        #self.mini_mv.remove_grid_reticle()




        self.m_v.insert_piano_grid_text_timeplane(length=self.m_v.grid3d_span, volume_slice=None, figure=self.mini_mv.scene_mini.mayavi_scene)
        self.m_v.insert_note_text(text="♫Point Cloud Processing♫", color=(1, 1, 0), figure=self.mini_mv.scene_mini.mayavi_scene, scale=11)
        self.mini_mv.scene_mini.background = (0/255, 0/255, 0/255)  #(222/255, 222/255, 0/255)
        self.mini.SetSize((446, 446))




        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(sizerHor, 30)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.ctrlsPanel.SetSizer(sizerCtrls)
        self.SetSizerAndFit(sizerMain)


    def generate_axis_menus(self):
        num = 0
        for i in self.axis_menu_list:  #4 items in this list
            print("INVALID_ID?", int(eval("%s" % (self.axis_menu_list.index(i)+1) + "101")))
            print("INVALID_ID?", int(eval("%s" % (self.axis_menu_list.index(i)+1) + "102")))
            print("INVALID_ID?", int(eval("%s" % (self.axis_menu_list.index(i)+1) + "103 ")))
            i.Append(int(eval("%s" % (self.axis_menu_list.index(i)+1) + "101")), "x")  #
            i.Append(int(eval("%s" % (self.axis_menu_list.index(i)+1) + "102")), "y")  #
            i.Append(int(eval("%s" % (self.axis_menu_list.index(i)+1) + "103")), "z")  #
        #menu.Append(10102, "y")  #
        #menu.Append(10103, "z")  #

        for i in self.axis_menu_list:
            for j in i.GetMenuItems():
                i.Bind(wx.EVT_MENU, self.menu_return, id=int(eval("%s" % (self.axis_menu_list.index(i)+1) + "101")))
                i.Bind(wx.EVT_MENU, self.menu_return, id=int(eval("%s" % (self.axis_menu_list.index(i)+1) + "102")))
                i.Bind(wx.EVT_MENU, self.menu_return, id=int(eval("%s" % (self.axis_menu_list.index(i)+1) + "103")))

        ##FOR ALL THE WORLD TO KNOW:
        ######1448, in _EvtHandler_Bind
             #assert source is None or hasattr(source, 'GetId')
             #AssertionError
        ### ^^^THIS error is because of not using """id=""" when assigning your bind to a menu item.


    def OnAxisButton1(self, evt):
        print("Axis_1")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu1)

    def OnAxisButton2(self, evt):
        print("Axis_2")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu2)

    def OnAxisButton3(self, evt):
        print("Axis_3")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu3)

    def OnAxisButton4(self, evt):
        print("Axis_4")
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu4)


    def menu_return(self, evt):

        if evt.GetId() == 1101:
            self.axisVar_Trim.SetLabelText('x')
        if evt.GetId() == 1102:
            self.axisVar_Trim.SetLabelText('y')
        if evt.GetId() == 1103:
            self.axisVar_Trim.SetLabelText('z')
        if evt.GetId() == 2101:
            self.axisVar_Rot.SetLabelText('x')
        if evt.GetId() == 2102:
            self.axisVar_Rot.SetLabelText('y')
        if evt.GetId() == 2103:
            self.axisVar_Rot.SetLabelText('z')
        if evt.GetId() == 3101:
            self.axisVar_Trans.SetLabelText('x')
        if evt.GetId() == 3102:
            self.axisVar_Trans.SetLabelText('y')
        if evt.GetId() == 3103:
            self.axisVar_Trans.SetLabelText('z')
        if evt.GetId() == 4101:
            self.axisVar_Mir.SetLabelText('x')
        if evt.GetId() == 4102:
            self.axisVar_Mir.SetLabelText('y')
        if evt.GetId() == 4103:
            self.axisVar_Mir.SetLabelText('z')




    def OnLoadPly(self, evt):
        ###If Working on CurrentActor Points
        if self.chbxCurrentActor.IsChecked():
            self.points = super().GetParent().GetTopLevelParent().mayavi_view.CurrentActor()._points
            self.actor__points = [i._points for i in super().GetParent().GetTopLevelParent().mayavi_view.actors]
            self.pointclouds = [numpy.column_stack([i[:, 0], i[:, 1], i[:, 2]]) for i in self.actor__points]
            #super().GetParent().GetTopLevelParent().mayavi_view.actors
            if len(self.pointclouds) > 1:
                self.chbxMultiple.SetValue(True)
                self.points = self.pointclouds[0]
                # self.pathname = self.pathnames[
                #     0]  # First pointcloud in the list, then we cycle through use (previous, next) btns.
                self.point_cloud_counter = 0
            else:
                self.chbxMultiple.SetValue(False)
                self.points = self.pointclouds[0]
                #self.pathname = self.pathnames[0]  ##don't need fileDialog.GetPath() anymore
                self.point_cloud_counter = 0
            try:
                self.UpdateDisplay()
            except IOError:
                # TODO Rewrite this log error message.
                wx.LogError("Cannot open file '%s'." % self.pathnames[0])
        ###If loading points from file
        else:
            with wx.FileDialog(self, "Open Ply file(s)", wildcard="Ply files (*.ply)|*.ply",
                               style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST) as fileDialog:

                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return  # the user changed their mind

                # Proceed loading the file chosen by the user
                #pathname = fileDialog.GetPath()
                self.pathnames = fileDialog.GetPaths()

                #self.ply = self.pathname
                #self.ply_name = os.path.basename(self.pathname)
                self.ply_names = [os.path.basename(i) for i in self.pathnames]  #TODO Not used, delete? 07/10/2023
                self.pointclouds = [midiart3D.get_points_from_ply(i) for i in self.pathnames]

                #print(self.pathnames)
                if len(self.pointclouds) > 1:
                    self.chbxMultiple.SetValue(True)
                    self.points = self.pointclouds[0]
                    # self.pathname = self.pathnames[
                    #     0]  # First image in the list, then we cycle through use (previous, next) btns.
                    self.point_cloud_counter = 0
                else:
                    self.chbxMultiple.SetValue(False)
                    self.points = self.pointclouds[0]
                    #self.pathname = self.pathnames[0]  ##don't need fileDialog.GetPath() anymore
                    self.point_cloud_counter = 0
                try:
                    self.UpdateDisplay()
                except IOError:
                    #TODO Rewrite this log error message.
                    wx.LogError("Cannot open file '%s'." % self.pathnames[0])


    def OnGenerate_Point_E_PointCloud(self, event):
        self.chbxMultiple.SetValue(False)
        self.points = self.point_e.Generate(prompt=self.inputTxt.GetLineText(0)) #self.pathnames[0]  ##don't need fileDialog.GetPath() anymore
        self.points = midiart3D.process_3d_points_for_Midas(self.points)

        print("Point_E Image", self.points)
        try:
            self.pointclouds.append(self.points)
            self.image_list_counter = len(self.pointclouds) - 1  #TODO TEST 07/14/2023
            self.UpdateDisplay()
        except AttributeError as e:
            print("AttributeError", e, "Skipping...")
            self.pointclouds = []
            self.pointclouds.append(self.points)
            self.image_list_counter = 0
            self.UpdateDisplay()
        #pass
        print("Point_E Point Cloud generated.")


    def OnLoadChange(self, evt):
        if self.chbxCurrentActor.IsChecked():
            self.btnLoadPly.SetLabel("Load Current Actor(s)")
        else:
            #self.chbxCurrentActor.IsChecked()
            self.btnLoadPly.SetLabel("Load Point Cloud(s)")


    def OnMultipleChange(self, evt):
        if self.chbxMultiple.IsChecked():
            self.chbxPlanes.Enable(enable=True)
            self.chbxToFile.Enable()
            self.btnCurrentPlanesToGlobals.Enable()
        else:
            self.chbxPlanes.Disable()
            self.chbxToFile.Disable()
            self.btnCurrentPlanesToGlobals.Disable()


    def UpdateGlobals(self, evt):
        self.Midiart3DGlobals = []
        planes_dict = midiart3D.get_planes_on_axis(self.points)
        for i in planes_dict.keys():
            streams = midiart3D.extract_xyz_coordinates_to_stream(planes_dict[i])
            self.Midiart3DGlobals.append(streams)
            if self.chbxToFile.IsChecked():
                streams.write('mid', r".\resources\intermediary_path" + os.sep + "CurrentPointCloud_plane--%s.mid" % i)
        super().GetParent().GetTopLevelParent().mayavi_view.Midiart3DGlobals = self.Midiart3DGlobals
        print("Midiart3D Globals", self.Midiart3DGlobals)
        print("Midiart3D Globals Length", len(self.Midiart3DGlobals))
        print("Midiart3D Globals Updated.")

    # def OnComboBoxSelection(self, evt):
    #     points = super().GetParent().mv.actors[int(self.cbActorIndices.GetSelection())]._points
    #     if points.size is 0:
    #         self.btnLoadPly.Enable()  #If no points, allow for the loading of a .ply.
    #     else:
    #         self.btnLoadPly.Disable() #If there are points, select a different actor to avoid overlapping notes.
    #     self.points = points


    def UpdateDisplay(self):
        self.mlab_call.mlab_source.points = self.points
            # = self.m_v.insert_array_data(self.points, color=(1, 1, 0),
            #                                         figure=self.mini_mv.scene_mini.mayavi_scene,
            #                                         scale_factor=1)
        #trait_set(points=points

    def OnCycleNext(self, event):
        self.point_cloud_counter += 1
        if self.point_cloud_counter > len(self.pointclouds) - 1:
            self.point_cloud_counter = 0
        self.points = self.pointclouds[self.point_cloud_counter]
        #self.pathname = self.pathnames[self.point_cloud_counter]
        #self.UpdateImageData()
        #self.UpdatePreview()
        self.UpdateDisplay()


    def OnCyclePrevious(self, event):
        self.point_cloud_counter -= 1
        if self.point_cloud_counter < 0:
            self.point_cloud_counter = len(self.pointclouds) - 1
        self.points = self.pointclouds[self.point_cloud_counter]
        #self.pathname = self.pathnames[self.point_cloud_counter]
        #self.UpdateImageData()
        #self.UpdatePreview()
        self.UpdateDisplay()


    #Points processing functions
    def OnStandardReorientation(self, evt, points=None, scale=1.):
        print("Standard Reorientation of points...")

        self.marker = 0
        #Cleans strays on first call only.
        if self.marker < 1:
            self.points = midiart3D.standard_reorientation(points=self.points,
                                                           scale=1, clean=True)   ###int(self.scaleVar_Reo.GetValue())
            self.marker = 1
        else:
            self.points = midiart3D.standard_reorientation(points=self.points,
                                                           scale=1, clean=False)   ###int(self.scaleVar_Reo.GetValue())
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Standard Reorientation complete.")
        self.pointclouds[self.point_cloud_counter] = self.points
        return self.points


    def OnTrim(self, evt, points=None, axis = 'y', trim = 0):
        print("Trimming points...")

        self.points = midiart3D.trim(points=self.points,
                                     axis=str(self.axisVar_Trim.GetLabelText()),
                                     trim=int(self.trimVar_Trim.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Points trimmed.")
        self.pointclouds[self.point_cloud_counter] = self.points
        return self.points


    def OnScale(self, evt, points=None, scale_factor=2):
        #Todo Write
        print("Scaling points...")

        midiart3D.scale_points(self.points, scale=float(self.scaleVar_Scale.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Points scaled.")
        self.pointclouds[self.point_cloud_counter] = self.points
        return self.points


    def OnRotate(self, evt, points=None, axis = 'y', degrees=90):
        print("Rotating points...")

        self.points = midiart3D.rotate_array_points_about_axis(points=self.points,
                                                               axis=str(self.axisVar_Rot.GetLabelText()),
                                                               degrees=int(self.degreesVar_Rot.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Points rotated.")
        self.pointclouds[self.point_cloud_counter] = self.points

        return self.points


    def OnMirror(self, evt, points=None, axis = 'x'):
        print("Mirroring on %s axis" % str(self.axisVar_Mir.GetLabelText()))

        self.points = midiart3D.mirror_points_on_axis(coords_array=self.points,
                                                      axis = str(self.axisVar_Mir.GetLabelText()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Points mirrored on %s axis." % str(self.axisVar_Mir.GetLabelText()))
        self.pointclouds[self.point_cloud_counter] = self.points


    def OnTransform(self, coords_array=None, offset=0, axis='y', center_axis=False, positive_octant=False):
        print("Transforming points...")

        self.points = midiart3D.transform_points_by_axis(coords_array=self.points,
                                                         offset=int(self.offsetVar_Trans.GetValue()),
                                                         axis=str(self.axisVar_Trans.GetLabelText()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Points transformed.")
        self.pointclouds[self.point_cloud_counter] = self.points

        return self.points




    # def On3DDisplayRedraw(self, evt):
    #     super().GetParent().mv.redraw_mayaviview()




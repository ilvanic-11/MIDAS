import wx
from midas_scripts import midiart, midiart3D, musicode # music21funcs,
from gui import Generate
import music21
import cv2, numpy
import os
import shutil
from collections import OrderedDict
from mayavi3D.Mayavi3DWindow import Mayavi3idiView, MayaviMiniView
from time import sleep
import gc
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
        self.btn_Music21_Converter_Parse = wx.Button(self, -1, "Midi\Score \n Import", size=(75, 36))
        self.btn_Music21_Converter_Parse.SetBackgroundColour((200, 150, 200, 255))
        #btn_Music21_Converter_Parse.SetForegroundColour((255, 255, 255, 255))
        self.main_buttons_sizer.Add(self.btn_Music21_Converter_Parse, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMusic21ConverterParseDialog, self.btn_Music21_Converter_Parse)
        self.midi_TT = wx.ToolTip("Import Midi\Score files.")
        self.btn_Music21_Converter_Parse.SetToolTip(self.midi_TT)


        #btn_musicode.
        self.btn_musicode = wx.Button(self, -1, "Musicode")
        self.btn_musicode.SetBackgroundColour((0, 150, 255, 255))
        self.main_buttons_sizer.Add(self.btn_musicode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMusicodeDialog, self.btn_musicode)
        self.musicode_TT = wx.ToolTip("Turn text into music.")
        self.btn_musicode.SetToolTip(self.musicode_TT)

        #btn_midiart.
        self.btn_MIDIart = wx.Button(self, -1, "MidiArt")  #MIDI Art
        self.btn_MIDIart.SetBackgroundColour((0, 222, 70, 255))
        self.main_buttons_sizer.Add(self.btn_MIDIart, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArtDialog, self.btn_MIDIart)
        self.midiart_TT = wx.ToolTip("Turn pictures into music.")
        self.btn_MIDIart.SetToolTip(self.midiart_TT)

        #btn_midiart3D.
        self.btn_MIDIart3D = wx.Button(self, -1, "3iDiArt")  #3IDI Art
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

        self.Bind(wx.EVT_MENU, self.OnMusic21ConverterParseDialog, id=new_id1)
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
        dlg = Music21ConverterParseDialog(self, -1, "         music21.converter.parse") #9 Spaces deliberate here.
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
        if type(dialog) is MusicodeDialog:
            self._OnMusicodeDialogClosed(dialog, evt)
        elif type(dialog) is MIDIArtDialog:
            self._OnMIDIArtDialogClosed(dialog, evt)
        elif type(dialog) is Music21ConverterParseDialog:
            self._OnM21ConverterParseDialogClosed(dialog, evt)
        elif type(dialog) is MIDIArt3DDialog:
            self._OnMIDIArt3DDialogClosed(dialog, evt)
        dialog.Destroy()



    def _OnM21ConverterParseDialogClosed(self, dialog, evt):
        print("OnM21ConverterParseDialogClosed():")
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        if btn == "OK":

            #New Actor Checkbox
            self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor() \
                if dialog.chbxNewActor.IsChecked() is True else None

            m_v = self.GetTopLevelParent().mayavi_view
            color_palette = m_v.current_color_palette

            stream = music21.converter.parse(dialog.midi)
            stream.show('txt')
            #TODO CORE DATA UPDATE Here
            points = midiart3D.extract_xyz_coordinates_to_array(stream)
            index = len(m_v.actors)
            name = str(len(m_v.actors)) + "_" + "Midi" + "_" + dialog.midi_name
            # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
            m_v.disable_render = True
            actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
            # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            for j in m_v.actors:
                if j.name == name:
                    print("Points here?")
                    j.change_points(points)
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
                    write_name = dialog.pathname
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

        if btn == "OK":

            #New Actor Checkbox
            #TODO Finish! 07/10/2023
            # self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(len(self.m_v.actors)) \
            #     if dialog.chbxNewActor.IsChecked() is True else None
            # NOTE: With monochrome and edges, new_actor is doable. With colors, the new_actor chbx needs to Disabl()

            #En Mass Export Directly to File.
            if dialog.MultipleCheck == True and dialog.AllCheck == True:
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
                        self.transform_images(i, (pixels, pixels2), height, img_name, dialog, num,
                                              palette_name=palette_name)
                        num += 1
            elif dialog.MultipleCheck == True and dialog.AllCheck == False:
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
                    self.transform_images(i, (pixels, pixels2), height, img_name, dialog, num)
                    num += 1

            #Load to Gui Grid.
            else:
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


    def join_with_piano(self, image, height, piano=r".\resources\ThePhatPiano16.png"):
        image = image
        piano = cv2.imread(piano)  # Remember, cv2.imread swaps rgb to bgr.

        height = height#MIDAS_Settings.noteHeight
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
    def transform_images(self, image_path, pxls_tuple, height, img_name, dialog, num, palette_name=None):

        #***Here.
        filepath = r".\resources\intermediary_path"
        pathname = image_path
        print("PATHNAME", pathname)

        height = height
        img_name = img_name

        pixels = pxls_tuple[0]
        pixels2 = pxls_tuple[1]

        #Test -This was the magical one that found our bug. 11/30/2021
        #pixels2 = cv2.cvtColor(pixels2, cv2.COLOR_BGR2RGB)

        #pixels_resized = dialog.resizedImg

        gran = dialog.granularitiesDict[dialog.rdbtnGranularity.GetString(dialog.rdbtnGranularity.GetSelection())]
            ###MIDAS_Settings.granularity]

        # print("PIXELS", pixels)
        # print("PIXELS2", pixels2)
        # print("PIXELS_RESIZED:", pixels, type(pixels))
        # print("pixel s_shape", np.shape(pixels))

        current_color_palette = self.m_v.current_color_palette = self.m_v.clr_dict_list[palette_name] if palette_name is not None else self.m_v.current_color_palette #TODO Is this used?
        #mayavi_color_palette = self.current_mayavi_palette
        current_palette_name = self.m_v.current_palette_name


        if dialog.EdgesCheck:
        #if self.ids.midiart_Choice.text == "Edges":
            print("Transforming Edges!")
            #IMAGE
            self.selection = "Edges"
            self.edges = cv2.Canny(pixels, 100, 200)

            #self.edges2 = cv2.Canny(pixels2, 100, 200)
            #CONCATENATE with PIANO
            self.preview = midiart.cv2_tuple_reconversion(pixels2,
                                                          inPlace=False,
                                                          conversion='Edges')[1]
            self.img_without_piano = self.preview

            self.img_with_piano = self.join_with_piano(self.preview, height)

            #NAME
            self.name = self.selection + "_" + str(num) + "_" + img_name

            #STREAM
            self.stream = midiart.make_midi_from_grayscale_pixels(self.edges,
                                                                  gran,
                                                                  connect=dialog.chbxConnect.GetValue(), ##.connectNotes,
                                                                  note_pxl_value=255)
                                                                  ##dialog.inputKey.GetValue(), , colors=False
            print("EdgeStream:", self.stream)
            self.stream.show('txt')

            #name = str(len(m_v.actors)) + "_" + "Edges" + "_" + dialog.img_name
            print("Edges load completed.")

        elif dialog.ColorsCheck:
        #if self.ids.midiart_Choice.text == "Color":
            print("Transforming Color!")
            print("PREPixels2:", pixels2)
            print("Gran", gran)
            print("Here.")
            print("DEFAULT_COLOR_PALETTE_2, import.", current_color_palette)
            #The default_color_palette is the dictionary of colors by which our coords must be sorted.

            #IMAGE
            self.selection = "Colors"
            self.colors = pixels2
            self.nn_colors = midiart.set_to_nn_colors(pixels2, self.m_v.current_color_palette)

            self.img_without_piano = self.nn_colors

            #CONCATENATE with PIANO
            self.img_with_piano = self.join_with_piano(self.nn_colors, height)

            #NAME
            if palette_name is None:
                palette_name = current_palette_name
            self.name = self.selection + "_" + str(num) + "_" + palette_name + "_" + img_name
            #     self.name = self.selection +  "_" + str(num) + "_" + dialog.listCtrl.GetItemText(num) + "_" + img_name
            # else:
            #     self.name = self.selection +  "_" + str(num) + "_" + palette_name + "_" + img_name

            #STREAM
            #swaprnb = midiart.convert_dict_colors(MIDAS_Settings.current_color_palette, invert=True)

            swaprnb = self.m_v.current_color_palette

            self.stream = midiart.transcribe_colored_image_to_midiart(self.colors,
                                                                 granularity=gran,
                                                                 connect=dialog.chbxConnect.GetValue(),##MIDAS_Settings.connectNotes,
                                                                 keychoice=dialog.inputKey.GetValue(),
                                                                 colors=swaprnb,
                                                                 output_path=None)
            print("ColorsStream:", self.stream)
            self.stream.show('txt')
            print("Colors load completed.")


        elif dialog.MonochromeCheck:
        #if self.ids.midiart_Choice.text == "Monochrome":
            print("Transforming Monochrome!")
            #IMAGE
            self.selection = "Monochrome"
            self.monochrome = pixels
            #CONCATENATE with PIANO
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

            #NAME
            self.name = self.selection + "_" + str(num) + "_" + img_name  # "QR-BW"

            #STREAM
            self.stream = midiart.make_midi_from_grayscale_pixels(self.preview2,
                                                                  gran,
                                                                  dialog.chbxConnect.GetValue(), ###MIDAS_Settings.connectNotes,
                                                                  note_pxl_value=0)
            #TODO Temporary
            #self.m_v.CurrentActor()._stream = self.stream

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
        #print("CHOICE", self.ids.midiart_Choice.text)
        #if self.ids.midiart_Choice.text != "Midiart":
        if dialog.ColorsCheck:
            midiart.set_parts_to_midi_channels(self.stream, filepath_midi)
        else:
            self.stream.write("mid", filepath_midi)
            ##midiart.set_parts_to_midi_channels(self.stream, filepath_midi) \
            ##        if self.ids.midiart_Choice.text == "Color" else self.stream.write("mid", filepath_midi)
            ##else:
            ##    pass

        # Image with midi to file
        #cv2.imwrite(file_path_img, self.img_without_piano)
        cv2.imwrite(file_path_img_with_piano, self.img_with_piano)

        #Update Gui View
        ##self.parent.ids.imagedraw_Area.ids.image_View.source = file_path_img_with_piano
        #self.parent.ids.imagedraw_Area.ids.image_View.reload()
    #################



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


class Music21ConverterParseDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Traditional Music'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)
        #self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)

        self.help_static = wx.StaticText(self, -1, "Import a midi file or a score file.", style=wx.ALIGN_CENTER)

        self.btnLoadMidi = wx.Button(self, -1, "Load Midi\\Score")

        # Input text box
        self.inputTxt = wx.TextCtrl(self, -1, "              Input MuseNet Prompt Here", size=(250, -1),
                                    style=wx.TE_MULTILINE, name="Generative Prompter Input")
        self.inputTxt.Disable()
        self.btnGenerate_MuseNet = wx.Button(self, -1, "MuseNet Midi\nGenerate")
        self.btnGenerate_MuseNet.Disable()

        # New Actor Checkbox
        self.chbxNewActor = wx.CheckBox(self, -1, "New Actor?")    #ctrlsPanel
        self.chbxNewActor.SetValue(not self.chbxNewActor.IsChecked())

        #############
        #OpenAI Class
        #self.muse_net = Generate.Muse_Net()


        #Binds
        self.Bind(wx.EVT_BUTTON, self.OnLoadMidi, self.btnLoadMidi)
        self.Bind(wx.EVT_BUTTON, self.OnGenerate_MuseNet_Midi, self.btnGenerate_MuseNet)


        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.sizer5 = wx.BoxSizer(wx.VERTICAL)
        self.sizer5.Add(self.inputTxt, 0, wx.ALL | wx.ALIGN_CENTER, 0)
        self.sizer5.Add(self.btnGenerate_MuseNet, 0, wx.ALL | wx.ALIGN_CENTER, 0)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        #sizerMain.Add(sizerHor, 30)
        sizerMain.Add(self.help_static, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizerMain.Add(self.btnLoadMidi, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        sizerMain.Add(self.sizer5, 0, wx.ALIGN_CENTER | wx.ALL, 30)

        sizerMain.Add(self.chbxNewActor, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        sizerCtrls = wx.BoxSizer(wx.VERTICAL)


        self.SetSizerAndFit(sizerMain)


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

    def OnGenerate_MuseNet_Midi(self, event):
        #self.midi = self.muse_net.Generate(prompt="user midi selection\plane\midi_file\etc....")
        print("Generating MuseNet Midi....not implemented yet though!")
        pass


class MusicodeDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Musicode'):
        
        wx.Dialog.__init__(self)

        self.Create(parent, id, title, pos, size, style, name)
        self.parent = parent

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
        self.Bind(wx.EVT_BUTTON, self.OnLoadTextFile, id=loadtxtID)

        #Supported Characters
        self.supported_static = wx.StaticText(self, -1, ('''Supported Musicode Characters: \n <<<< AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz       ?,;\':-.!\"()[]/       0123456789 >>>>'''), style=wx.ALIGN_CENTER)
        self.generate_musicode_text = wx.CheckBox(self, -1, "Generate Musicode Text")
        #self.generate_musicode_text.SetValue(not self.generate_musicode_text.IsChecked())
        #Input text box
        self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "♫♪♪♪♪♪♪♪♪♪Musicode Text Here♪♪♪♪♪♪♪♪♫", size=(250, -1), style=wx.TE_MULTILINE, name="Translate\\Create")
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


        self.rdbtnMusicodeChoice = wx.RadioBox(self, -1, "Musicode Choice",
                                               wx.DefaultPosition, wx.DefaultSize,
                                               self.musicodesList,
                                               2, wx.RA_SPECIFY_COLS)

        self.btnGenerate_ChatGPT = wx.Button(self, -1, "ChatGPT Response\nGenerate")
        self.btnGenerate_ChatGPT.Disable()

        self.rdbtnMusicodeChoice.Enable(enable=False)

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
        self.sizer.Add(self.rdbtnMusicodeChoice, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 30)
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
        self.inputTxt.SetValue(self.chat_gpt.Generate(prompt = self.inputTxt.GetLineText(0)))
        print("Chat GPT Response generated.")
        #pass


    #TODO Needs work.
    def OnPolarizeCheckboxes(self, event):
        if self.create_musicode.IsChecked(): #Click on other one...
            self.translate_musicode.SetValue(not self.create_musicode.IsChecked())
            self.translate_multiline_musicode.SetValue(False)

            self.rdbtnMusicodeChoice.Enable(enable=False)
            self.name_static.Enable(enable=True)
            self.input_mcname.Enable(enable=True)
            self.input_sh.Enable(enable=True)
            self.sh_static.Enable(enable=True)
            self.translate_multiline_musicode.Enable(enable=False)

            # self.inputTxt.SetWindowStyle(style=wx.TE_LEFT)
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter Musicode Text Here", size=(250, -1),
                                        style=wx.TE_LEFT,
                                        name="Translate\\Create")
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
                self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter Musicode Text Here", size=(250, -1),
                                            style=wx.TE_MULTILINE,
                                            name="Translate\\Create")
                self.textinputPanel.SetSize(254, 162)
                self.textinputPanel.Refresh()
                self.Refresh()
            else:
                self.inputTxt.Destroy()
                self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter Musicode Text Here", size=(250, -1),
                                            style=wx.TE_LEFT,
                                            name="Translate\\Create")
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
        if self.generate_musicode_text.IsChecked():
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter ChatGPT Text Prompt Here", size=(250, -1),
                                        style=wx.TE_MULTILINE,
                                        name="CHATGPT Prompt Trigger")
            self.textinputPanel.SetSize(254, 162)
            self.textinputPanel.Refresh()
            self.Refresh()

            self.btnGenerate_ChatGPT.Enable(enable=True)

        else:
            self.inputTxt.Destroy()
            self.inputTxt = wx.TextCtrl(self.textinputPanel, -1, "Enter ChatGPT Text Prompt Here", size=(250, -1),
                                        style=wx.TE_LEFT,
                                        name="CHATGPT Prompt Trigger")
            self.textinputPanel.SetSize(253, 27)
            self.textinputPanel.Refresh()
            self.Refresh()
            self.btnGenerate_ChatGPT.Disable()
        print("OnCheckBoxes2....")


class CustomColorsListBox(wx.ListCtrl):
    def __init__(self, parent, log):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT
                                   #wx.LC_VIRTUAL |
                                   # wx.LC_NO_HEADER |
                                   |wx.LC_SINGLE_SEL  #True for this color selection stuff.
                             )

        self.log = log

        self.SetBackgroundColour((100, 100, 100))
        self.SetTextColour((255, 255, 255))

        self.InsertColumn(0, "Color", wx.LIST_FORMAT_CENTER, width=150)


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

        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, (236, 810), style=wx.BORDER_RAISED) #770
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (515, 515), style=wx.BORDER_RAISED)
        self.displayImage = None

        self.listCtrl = CustomColorsListBox(self.ctrlsPanel, log=None)
        #self.listCtrl.InsertItem(0, "FLStudioColors")
        self.index = 1
        for clrs in midiart.get_color_palettes():
            self.listCtrl.InsertItem(self.index, clrs)
            self.index += 1

        print("LISTCTRL_LENGTH:", self.listCtrl.GetItemCount())
        print("ITEM_0", self.listCtrl.GetItemText(0))
                                                                        #Spaces deliberate here.
        self.static_color = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "Select Color Palette") #self, bug?? size=(100,100),
        #self.static_color = self.name_static = wx.StaticText(self.ctrlsPanel, -1, "              Select Color Palette") #self, bug?? size=(100,100),

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
        self.chbxMonochorome = wx.CheckBox(self.ctrlsPanel, -1, "Monochrome")

        self.chbxAllColors = wx.CheckBox(self.ctrlsPanel, -1, "All Colors?")

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
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxSelection)

        self.Bind(wx.EVT_BUTTON, self.OnGenerate_Dall_E_Image, self.btnGenerate_DALL_E)


        #self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.OnChangeColor)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnChangeColor)

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        #colorSizer = wx.BoxSizer(wx.VERTICAL)
        cycleimagesSizer = wx.BoxSizer(wx.HORIZONTAL)
        exportSizer = wx.BoxSizer(wx.HORIZONTAL)
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
        exportSizer.Add(self.chbxAllColors, 0, wx.ALL | wx.ALIGN_CENTER, 3)

        sizerCtrls.Add(topSizer, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)  #35
        sizerCtrls.Add(self.chbxEdges, 0, wx.ALL | wx.ALIGN_LEFT, 11)
        sizerCtrls.Add(self.chbxColorImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0) #colorSizer
        sizerCtrls.Add(self.chbxMonochorome, 0, wx.ALL | wx.ALIGN_RIGHT, 14)
        sizerCtrls.AddSpacer(25)
        sizerCtrls.Add(self.btnLoadImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizerCtrls.Add(cycleimagesSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -10)
        sizerCtrls.Add(self.chbxShowTransformed, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -10)



        ###NOTE: These space settings are affect by the resolution settings of Windows.
        ###Of particular note is where it says "Change the size of text, apps, and other items"  '%---'
        sizerCtrls.AddSpacer(30)  ####* commented out if res settings changed
        sizerCtrls.AddSpacer(40)  ####* commented out if res settings changed
        #sizerCtrls.AddSpacer(65)
        sizerCtrls.Add(self.exportStatic, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -25) #-25  -15 swap these if res changed

        #sizerCtrls.AddSpacer(40)  ####insterted if resolutions settings are changed

        sizerCtrls.Add(exportSizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, -35)
        sizerCtrls.AddSpacer(45)


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

            ###Proceed loading the file chosen by the user
            self.pathnames = fileDialog.GetPaths()
            if len(self.pathnames) > 1:
                self.chbxMultiple.SetValue(True)
                self.pathname = self.pathnames[0] #First image in the list, then we cycle through use (previous, next) btns.
                self.image_list_counter = 0 #come back here 07/10/2023
            else:
                self.chbxMultiple.SetValue(False)
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
        self.MonochromeCheck = self.chbxMonochorome.IsChecked()
        self.MultipleCheck = self.chbxMultiple.IsChecked()
        self.AllCheck = self.chbxAllColors.IsChecked()

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
        if self.chbxMonochorome.IsChecked():
            self.MonochromeCheck = True
            self.chbxEdges.SetValue(False)
            self.EdgesCheck = False
            self.chbxColorImage.SetValue(False)
            self.ColorsCheck = False
            self.chbxAllColors.SetValue(False)
            self.chbxAllColors.Enable(enable=False)
        if self.chbxColorImage.IsChecked():
            self.ColorsCheck = True
            self.chbxEdges.SetValue(False)
            self.EdgesCheck = False
            self.chbxMonochorome.SetValue(False)
            self.MonochromeCheck = False
            #self.chbxAllColors.SetValue(True)
            self.chbxAllColors.Enable(enable=True)
        if self.chbxEdges.IsChecked():
            self.EdgesCheck = True
            self.chbxColorImage.SetValue(False)
            self.ColorsCheck = False
            self.chbxMonochorome.SetValue(False)
            self.MonochromeCheck = False
            self.chbxAllColors.SetValue(False)
            self.chbxAllColors.Enable(enable=False)
        self.UpdatePreview()

        #print("self.edges.shape=", self.edges.shape)

        #self.im = wx.ImageFromBuffer(w, h, rgb)


    def OnChangeColor(self, event):
        #This is the greatest thing.
        m_v = super().GetParent().m_v
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
            #Assign Dict.
            m_v.current_color_palette = m_v.clr_dict_list[self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())]

            #Invert tuples.
            #m_v.default_color_palette = midiart.convert_dict_colors(m_v.default_color_palette, invert=True)


            #SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
            #Convert to mayavi floats and necessary compensatory SWAP because of cvt BGR inversion and to make all rest code cleaner.

            m_v.current_mayavi_palette = midiart.convert_dict_colors(m_v.current_color_palette, both=True) #invert=True)

            #print("MAYAVI PALETTE", m_v.default_mayavi_palette)
            #m_v.default_mayavi_palette = midiart.convert_dict_colors(m_v.default_mayavi_palette, invert=True)
            print("MAYAVI PALETTE", m_v.current_mayavi_palette)
            #palette = \
            #midiart.convert_dict_colors(m_v.default_color_palette, invert=False)
            #Invert tuples.

            #Invert Color Tuples (swap R with B)
            #m_v.default_mayavi_palette = \
            #midiart.convert_dict_colors(m_v.default_color_palette, invert=True)
            #A tuple R\B switch happens here; tuple is inverted.

            m_v.current_palette_name = self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())
            print("3")

        print("Current Palette Name Changed", m_v.current_palette_name)
        self.UpdatePreview()


class MIDIArt3DDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='3idiArt'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #Points
        self.points = numpy.array([[0, 0, 0]])
        self.point_cloud_counter = 0

        self.pointclouds = []

        #Panels
        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, size=(485,565), style=wx.BORDER_RAISED) #515
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
            print("You computer does not have cuda installed\configured. Point_E generation components will be disabled.")
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
        for i in self.axis_menu_list:
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
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu1)

    def OnAxisButton2(self, evt):
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu2)

    def OnAxisButton3(self, evt):
        self.popupMenu = wx.Window.PopupMenu(self.ctrlsPanel, self.axis_Menu3)

    def OnAxisButton4(self, evt):
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
        else:
            self.chbxPlanes.Disable()



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




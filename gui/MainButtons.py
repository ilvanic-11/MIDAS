import wx
from midas_scripts import midiart, midiart3D, musicode # music21funcs,
import music21
import cv2, numpy
import os
from collections import OrderedDict
from mayavi3D.Mayavi3DWindow import Mayavi3idiView, MayaviMiniView
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
        self.mv = self.toplevel.mayavi_view

        self.main_buttons_sizer = wx.BoxSizer(wx.VERTICAL)

        self.btn_Music21_Converter_Parse = wx.Button(self, -1, "Midi\Score \n Import", size=(75, 36))
        self.btn_Music21_Converter_Parse.SetBackgroundColour((200, 150, 200, 255))
        #btn_Music21_Converter_Parse.SetForegroundColour((255, 255, 255, 255))
        self.main_buttons_sizer.Add(self.btn_Music21_Converter_Parse, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMusic21ConverterParseDialog, self.btn_Music21_Converter_Parse)

        self.btn_musicode = wx.Button(self, -1, "Musicode")
        self.btn_musicode.SetBackgroundColour((0, 150, 255, 255))

        #btn_musicode.
        self.main_buttons_sizer.Add(self.btn_musicode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMusicodeDialog, self.btn_musicode)

        self.btn_MIDIart = wx.Button(self, -1, "MIDI Art")
        self.btn_MIDIart.SetBackgroundColour((0, 222, 70, 255))
        self.main_buttons_sizer.Add(self.btn_MIDIart, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArtDialog, self.btn_MIDIart)

        self.btn_MIDIart3D = wx.Button(self, -1, "3IDI Art")
        self.btn_MIDIart3D.SetBackgroundColour((222, 222, 0, 255))
        self.main_buttons_sizer.Add(self.btn_MIDIart3D, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 9)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArt3DDialog, self.btn_MIDIart3D)

        # btn_show_in_FLStudio = wx.Button(self, -1, "Show in FLStudio")
        # sizer.Add(btn_show_in_FLStudio, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinFLStudio, btn_show_in_FLStudio)

        # btn_show_in_MuseScore = wx.Button(self, -1, "Show in MuseScore")
        # sizer.Add(btn_show_in_MuseScore, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinMuseScore, btn_show_in_MuseScore)

        # btn_show_stream_txt = wx.Button(self, -1, "Show Stream Text")
        # sizer.Add(btn_show_stream_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowStreamTxt, btn_show_stream_txt)

        self.btn_update_stream = wx.Button(self, -1, "Update Stream")
        self.main_buttons_sizer.Add(self.btn_update_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.OnUpdateStream, self.btn_update_stream)

        self.btn_clear_pianoroll = wx.Button(self, -1, "Clear Piano Roll")
        #btn_clear_pianoroll.SetBackgroundColour((255, 230, 200, 255))
        self.main_buttons_sizer.Add(self.btn_clear_pianoroll, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.OnClearPianoRoll, self.btn_clear_pianoroll)

        self.btn_redraw_mayaviview = wx.Button(self, -1, "Redraw Mayavi \n View")
        self.main_buttons_sizer.Add(self.btn_redraw_mayaviview, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 8)
        self.Bind(wx.EVT_BUTTON, self.toplevel.mayavi_view.redraw_mayaviview, self.btn_redraw_mayaviview)

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


    def OnClearPianoRoll(self,evt):
        self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.GetTopLevelParent().pianorollpanel.currentZplane)

    # def OnDeleteAllPianoRolls(self, evt):
    #     self.GetTopLevelParent().


    def OnUpdateStream(self,evt):
        self.GetTopLevelParent().pianorollpanel.pianoroll.UpdateStream()


    def OnShowStreamTxt(self, evt):
        self.GetTopLevelParent().pianorollpanel.pianoroll.stream.show('txt')


    def OnMusic21ConverterParseDialog(self, evt):
        dlg = Music21ConverterParseDialog(self, -1, "         music21.converter.parse") #9 Spaces deliberate here.
        dlg.ShowWindowModal()


    def OnMusicodeDialog(self, evt):
        dlg = MusicodeDialog(self, -1, "Musicode")
        dlg.ShowWindowModal()


    def OnMIDIArtDialog(self, evt):
        dlg = MIDIArtDialog(self, -1, "Create MIDIArt")
        dlg.ShowWindowModal()


    def OnMIDIArt3DDialog(self, evt):
        dlg = MIDIArt3DDialog(self, -1, "Create 3D MIDIArt")
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


    def _OnMusicodeDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'


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
            self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.GetTopLevelParent().mayavi_view.cur_z)


        elif dialog.create_musicode.GetValue() is False and btn == "OK":
            print("DialogCheck:", dialog.create_musicode.GetValue())
            stream = self.musicode.translate(
                dialog.rdbtnMusicodeChoice.GetString(dialog.rdbtnMusicodeChoice.GetSelection()),
                dialog.inputTxt.GetLineText(0))
            print("LINETEXT:", dialog.inputTxt.GetLineText(0))
            self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
        else:
            pass


    def _OnMIDIArtDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        if btn == "OK":
            #pathname = dialog.pathname

            pixels = dialog.resizedImg     #2D array (2D of only on\off values.)
            pixels2 = dialog.resizedImg2   #3D array (2D of color tuples)
            #pixels_resized = dialog.resizedImg
            gran = dialog.pixScaler
            print("PIXELS", pixels)
            print("PIXELS2", pixels2)
            print("PIXELS_RESIZED:", pixels, type(pixels))
            print("pixels shape", numpy.shape(pixels))

            mayavi_view = self.GetTopLevelParent().mayavi_view
            #default_color_palette = mayavi_view.default_color_palette
            mayavi_color_palette = mayavi_view.default_mayavi_palette

            if dialog.EdgesCheck:
                edges = cv2.Canny(pixels, 100, 200)
                stream = midiart.make_midi_from_grayscale_pixels(edges, gran, True,  note_pxl_value=255)   ##dialog.inputKey.GetValue(), , colors=False


                print("EdgeStream:", stream)
                stream.show('txt')
                points = midiart3D.extract_xyz_coordinates_to_array(stream, velocities=mayavi_view.cur_z)
                index = len(mayavi_view.actors)
                name = str(len(mayavi_view.actors)) + "_" + "Edges" + "_" + dialog.img_name
                #clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now?
                mayavi_view.disable_render = True
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)
                mayavi_view.disable_render = False


            elif dialog.ColorsCheck:
                #TODO Display in grid upon completion of Actors\Z-Planes classes.
                print("PREPixels2:", pixels2)
                print("Gran", gran)
                print("Here.")

                #The default_color_palette is the dictionary of colors by which our coords must be sorted.
                self.num_dict = midiart.separate_pixels_to_coords_by_color(pixels2, mayavi_view.cur_z, nn=True, clrs=mayavi_view.default_color_palette, num_dict=True) #TODO use default_color_palette
                print('Num_dict:', self.num_dict)
                mayavi_view.colors_call += 1
                #TODO Add colors menu append here.
                mayavi_view.colors_name = dialog.img_name + "_" + "Clrs"

                #Menu Appends for new menu export method.
                new_id = wx.NewIdRef()
                self.GetTopLevelParent().menuBar.colors.Append(new_id, str(mayavi_view.colors_call) + "\tCtrl+Shift+%s" % mayavi_view.colors_call)
                self.GetTopLevelParent().Bind(wx.EVT_MENU, self.GetTopLevelParent().menuBar.OnExport_Colors, id=new_id)


                print("And Here2.")
                print("Palette", mayavi_color_palette)

                #Main call.
                num = 1
                priority_num = -16
                mayavi_view.scene3d.disable_render = True
                for h in self.num_dict.keys():

                    index = len(mayavi_view.actors)
                    # for i in mayavi_color_palette.keys():
                    #     if mayavi_color_palette[i] == h:
                    #Get the color we are on.

                    #R and B color values are swapped. This is fixed here, for now.
                    #TODO Fix inverted color tuples in color dicts? (this is still relevant. It's complicated -- 11/25/20)
                    clr = tuple([mayavi_color_palette[h][2], mayavi_color_palette[h][1], mayavi_color_palette[h][0]])

                    name = "Clrs" + str(mayavi_view.colors_call) + "_" + str(h) + "_" + dialog.img_name
                    actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                    mayavi_view.number_of_noncolorscall_actors -= 1 #Cancels += within new_actor() #TODO Make this a kwarg. 11/25/2020
                    colors_instance = "Clrs" + str(mayavi_view.colors_call)
                    mayavi_view.actors[index].colors_instance = colors_instance

                    for j in mayavi_view.actors:
                        if j.name == name:
                            print("Points here?")
                            if self.num_dict[h] is not None:
                                j.change_points(self.num_dict[h])
                            print("Color Change:", clr)
                            j.color = clr
                            j.part_num = num
                            j.priority = priority_num
                            num += 1
                            priority_num += 1
                mayavi_view.scene3d.disable_render = False

            elif dialog.MonochromeCheck:
                stream = midiart.make_midi_from_grayscale_pixels(pixels, gran, False, note_pxl_value=0)
                stream.show('txt')
                points = midiart3D.extract_xyz_coordinates_to_array(stream, velocities=mayavi_view.cur_z)
                index = len(mayavi_view.actors)
                name = str(len(mayavi_view.actors)) + "_" + "QR-BW" + "_" + dialog.img_name
                # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
                mayavi_view.disable_render = True
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)
                mayavi_view.disable_render = False
                #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)


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
            mayavi_view = self.GetTopLevelParent().mayavi_view
            color_palette = mayavi_view.default_color_palette

            stream = music21.converter.parse(dialog.midi)
            stream.show('txt')
            #TODO CORE DATA UPDATE Here
            points = midiart3D.extract_xyz_coordinates_to_array(stream)
            index = len(mayavi_view.actors)
            name = str(len(mayavi_view.actors)) + "_" + "Midi" + "_" + dialog.midi_name
            # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
            mayavi_view.disable_render = True
            actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
            # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            for j in mayavi_view.actors:
                if j.name == name:
                    print("Points here?")
                    j.change_points(points)
            mayavi_view.disable_render = False
            #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            mayavi_view.new_reticle_box()

    def _OnMIDIArt3DDialogClosed(self, dialog, evt):
        mayavi_view = self.GetTopLevelParent().mayavi_view

        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        #self.GetTopLevelParent().mayavi_view
        if btn == "OK":
            try:
                ##ply = dialog.ply
                points = dialog.points

            except AttributeError:
                ##ply = None
                points = None
                return

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
                i = len(mayavi_view.actors)
                name = str(i) + "_" + "PointCloud" + "_" + dialog.ply_name
                mayavi_view.scene3d.disable_render = True
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(i, name)

                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        #j.change_points(points)
                        j._points = points
                        #self.pointschangedflag = not self.pointschangedflag
                        j.actor_points_changed()
                        print("And here?")
                mayavi_view.scene3d.disable_render = False
            else:
                mayavi_view.scene3d.disable_render = False

                pass
        mayavi_view.scene3d.disable_render = False


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
        self.Bind(wx.EVT_BUTTON, self.OnLoadMidi, self.btnLoadMidi)



        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        #sizerMain.Add(sizerHor, 30)
        sizerMain.Add(self.help_static, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        sizerMain.Add(self.btnLoadMidi, 0, wx.ALL | wx.ALIGN_CENTER, 10)
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


class MusicodeDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Musicode' ):
        
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)
        self.parent = parent
        
        #MODE
        self.translate_musicode = wx.CheckBox(self, -1, "Translate Musicode")
        self.create_musicode = wx.CheckBox(self, -1, "Create Musicode")

        self.create_musicode.SetValue(True)  ##Set to translate at the ready by default.

        #Musicode name.
        self.name_static = wx.StaticText(self, -1, "Musicode Name",     style=wx.ALIGN_LEFT)
        self.input_mcname = wx.TextCtrl(self, -1, "", size=(90, -1), style=wx.TE_CENTER)

        #Shorthand variable name.
        self.sh_static = wx.StaticText(self, -1, "Shorthand", style=wx.ALIGN_LEFT)
        self.input_sh = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)
        self.inputTxt = wx.TextCtrl(self, -1, "", size=(250, -1), name="Translate\\Create")

        #####
        #Todo Use as possible example question for Robin Dunn when asking about wx Events
        super().GetParent().btn_musicode.Disable()  #These disable\enables calls fix a button highlight bug.
        dlg = wx.ProgressDialog("Loading", "Loading Musicode Libraries...", maximum=12, parent=self,
                                style = wx.PD_ELAPSED_TIME
                                      | wx.PD_REMAINING_TIME
                                      | wx.PD_AUTO_HIDE
                                )
        #super().GetParent().btn_musicode.SetFocusfromKbd()
        if self.parent.musicode == None:
            self.parent.GetTopLevelParent().musicode = self.parent.musicode = musicode.Musicode()
            self.parent.musicode.SetupDefaultMidiDictionaries(wx_progress_updater=dlg)
        else:
            pass
        dlg.Destroy()
        super().GetParent().btn_musicode.Enable()
        #####

        #super().GetParent().btn_musicode.SetFocus()
        #super().GetParent().HighlightSizerItem(super().GetParent().btn_musicode, super().GetParent().main_buttons_sizer, penWidth=2)


        self.musicodesList = sorted(list(self.parent.musicode.shorthand.keys()))

        self.rdbtnMusicodeChoice = wx.RadioBox(self, -1, "Musicode Choice",
                                               wx.DefaultPosition, wx.DefaultSize,
                                               self.musicodesList,
                                               2, wx.RA_SPECIFY_COLS)

        self.rdbtnMusicodeChoice.Enable(enable=False)

        
        #Bindings.
        self.Bind(wx.EVT_CHECKBOX, self.OnPolarizeCheckboxes)

        #Sizers
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)

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

        self.sizer.Add(self.sizer2, 0, wx.ALL | wx.ALIGN_TOP, 15)
        self.sizer.Add(self.sizer3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 30)
        self.sizer.Add(self.sizer4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 40)
        self.sizer.Add(self.inputTxt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.sizer.Add(self.rdbtnMusicodeChoice, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.sizer.Add(self.btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizerAndFit(self.sizer)
   

    #TODO Needs work.
    def OnPolarizeCheckboxes(self, event):
        if self.create_musicode.IsChecked(): #Click on other one...
            self.translate_musicode.SetValue(not self.create_musicode.IsChecked())
            self.rdbtnMusicodeChoice.Enable(enable=False)
            self.name_static.Enable(enable=True)
            self.input_mcname.Enable(enable=True)
            self.input_sh.Enable(enable=True)
            self.sh_static.Enable(enable=True)
        elif self.translate_musicode.IsChecked():  #True by default.
            #self.translate_musicode.SetValue(not self.translate_musicode.IsChecked()) #
            self.create_musicode.SetValue(not self.translate_musicode.IsChecked())
            self.rdbtnMusicodeChoice.Enable(enable=True)
            self.name_static.Enable(enable=False)
            self.input_mcname.Enable(enable=False)
            self.input_sh.Enable(enable=False)
            self.sh_static.Enable(enable=False)


        # elif self.translate_musicode.GetValue() is False:
        #     self.create_musicode.SetValue(True)
        # elif self.create_musicode.GetValue() is False:
        #     self.translate_musicode.SetValue(True)


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
    def __init__(self,parent,id,title, size=wx.DefaultSize,
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

        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (400, 400), style=wx.BORDER_RAISED)
        self.displayImage = None

        self.listCtrl = CustomColorsListBox(self.ctrlsPanel, log=None)
        self.listCtrl.InsertItem(0, "FLStudioColors")
        self.index = 1
        for clrs in midiart.get_color_palettes():
            self.listCtrl.InsertItem(self.index, clrs)
            self.index += 1
        self.static_color = self.name_static = wx.StaticText(self, -1, "Select Color Palette")


        self.btnLoadImage = wx.Button(self.ctrlsPanel, -1, "Load Image")

        self.chbxEdges = wx.CheckBox(self.ctrlsPanel, -1, "Edges")
        self.chbxColorImage = wx.CheckBox(self.ctrlsPanel, -1, "Color Image")
        self.chbxColorImage.SetValue(not self.chbxColorImage.IsChecked())
        self.chbxMonochorome = wx.CheckBox(self.ctrlsPanel, -1, "Monochrome")


        self.sldrHeight = wx.Slider(self.ctrlsPanel, -1, 127, 1, 127, wx.DefaultPosition, (190,40),
                                    wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.txtKey = wx.StaticText(self.ctrlsPanel, -1, "Key", style= wx.ALIGN_RIGHT )
        self.inputKey = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(30, 24), style=wx.TE_CENTER)

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

        #TODO Change default granularity checked box.

        #self.txtConnectNotes = wx.StaticText(self, -1, "Connect Notes?", style=wx.ALIGN_RIGHT)


        self.Bind(wx.EVT_BUTTON, self.OnLoadImage, self.btnLoadImage)
        self.Bind(wx.EVT_SLIDER, self.OnSliderChanged, self.sldrHeight)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxChanged, self.rdbtnGranularity)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxSelection)
        #self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.OnChangeColor)
        self.listCtrl.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnChangeColor)

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        sizerCtrls.Add(self.static_color, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        #sizerCtrls.Add(self.comboCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerCtrls.Add(self.listCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerCtrls.Add(self.chbxEdges, 0, wx.ALL  | wx.ALIGN_LEFT, 15)
        sizerCtrls.Add(self.chbxColorImage, 0, wx.ALL  | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizerCtrls.Add(self.chbxMonochorome, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        sizerCtrls.Add(self.btnLoadImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerCtrls.Add(self.sldrHeight, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)


        keysizer = wx.BoxSizer(wx.HORIZONTAL)
        keysizer.Add(self.txtKey, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        keysizer.Add(self.inputKey, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        sizerCtrls.Add(keysizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizerCtrls.Add(self.rdbtnGranularity, 0, wx.ALL | wx.ALIGN_CENTER, 20)


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

        sizerHor = wx.BoxSizer(wx.HORIZONTAL)
        sizerHor.Add(self.ctrlsPanel, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        sizerHor.Add(self.imgPreviewPanel, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(sizerHor, 30)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.SetSizerAndFit(sizerMain)


    def OnLoadImage(self, evt):
        with wx.FileDialog(self, "Open image file", wildcard="IMG files (*.png)|*.png|(*.jpeg)|*.jpeg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print(pathname)
            try:
                self.EdgesCheck = self.chbxEdges.IsChecked()
                self.ColorsCheck = self.chbxColorImage.IsChecked()
                self.MonochromeCheck = self.chbxMonochorome.IsChecked()

                self.pathname = pathname
                self.img = cv2.imread(pathname, 0)  #2D array (2D of only on\off values.)
                self.img2 = cv2.imread(pathname, cv2.IMREAD_COLOR)   #3D array (2D of color tuples, which makes a 3D array.)
                #print(type(self.img))
                self.img_name = os.path.basename(pathname)

                self.UpdatePreview()
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


    def OnSliderChanged(self,event):
        if self.img is not None:
            self.UpdatePreview()


    def OnRadioBoxChanged(self,event):
        if self.img is not None:
            print("No image selected. Select an image first. :)")
            self.UpdatePreview()


    def UpdatePreview(self):
        #TODO Fix the slider resize for all img instances.
        if self.displayImage:
            self.displayImage.Destroy()

        self.update_called = True

        self.pixScaler = int(8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        height = int(self.sldrHeight.GetValue())
        width = int(height / len(self.img) * len(self.img[0]))

        #Core Images for passing.
        self.resizedImg = cv2.resize(self.img, (width, height), cv2.INTER_AREA)
        self.resizedImg2 = cv2.resize(self.img2, (width, height), cv2.INTER_AREA)


        #Preview stuff.
        preview = cv2.resize(self.img2, (width, height), cv2.INTER_AREA)
        #self.self.previewImg = cv2.resize(self.resizedImg, (self.pixScaler*width, height), cv2.INTER_AREA)
        #rgb = cv2.cvtColor(self.previewImg, cv2.COLOR_GRAY2RGB)   ###cv2.COLOR_RGB2BGR)   ### ####cv2.COLOR_BGR2HSV)   ### #cv2.RG


        if self.ColorsCheck:
            preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
            #preview = cv2.cvtColor(preview, cv2.COLOR_RGB2BGR)

            mayavi_view = super().GetParent().mv

            #preview = midiart.set_to_nn_colors(preview, mayavi_view.clr_dict_list[mayavi_view.current_palette_name])

            #SWAP HERE
            swaprnb = midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=True)
            preview = midiart.set_to_nn_colors(preview, swaprnb)

            self.previewImg = cv2.resize(preview, (self.pixScaler * width * 3, height * 3),
                                         cv2.INTER_AREA)  # * 3 increases the size of the preview.

            h, w = self.previewImg.shape[:2]

            self.preview = wx.ImageFromData(w, h, self.previewImg)

            self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                (w, h), wx.ALIGN_CENTER_HORIZONTAL)


        elif self.EdgesCheck:
            #preview = cv2.Canny(preview, 100, 200)
            #self.im2 = preview
            preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Edges")
            self.previewImg = cv2.resize(preview[1], (self.pixScaler * width * 3, height * 3),
                                         cv2.INTER_AREA)  # * 3 increases the size of the preview.

            h, w = self.previewImg.shape[:2]

            self.preview = wx.ImageFromData(w, h, self.previewImg)

            self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.preview), wx.DefaultPosition,
                                                (w, h), wx.ALIGN_CENTER_HORIZONTAL)

        
        elif self.MonochromeCheck:
            preview = midiart.cv2_tuple_reconversion(preview, inPlace=False, conversion="Monochrome")

            print("PREVIEW MC", preview[1])
            #print("PREVIEW MC THRESH", thresh)
            self.previewImg = cv2.resize(preview[1], (self.pixScaler * width * 3, height * 3),
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
        if self.chbxColorImage.IsChecked():
            self.ColorsCheck = True
            self.chbxEdges.SetValue(False)
            self.EdgesCheck = False
            self.chbxMonochorome.SetValue(False)
            self.MonochromeCheck = False
        if self.chbxEdges.IsChecked():
            self.EdgesCheck = True
            self.chbxColorImage.SetValue(False)
            self.ColorsCheck = False
            self.chbxMonochorome.SetValue(False)
            self.MonochromeCheck = False


        self.UpdatePreview()

        #print("self.edges.shape=", self.edges.shape)

        #self.im = wx.ImageFromBuffer(w, h, rgb)


    def OnChangeColor(self, event):
        #This is the greatest thing.
        mayavi_view = super().GetParent().mv
        #FLStudio Colors
        #TODO Test color constistency across all views (preview, mayaviview, exported to FL)
        if self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem()) == "FLStudioColors":

            mayavi_view.default_color_palette = midiart.FLStudioColors

            #Convert
            mayavi_view.default_mayavi_palette = \
            midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=False)

            mayavi_view.current_palette_name = "FLStudioColors"
            print("FL Fuck")

        #Colors Dicts
        else:
            #Assign Dict.
            mayavi_view.default_color_palette= mayavi_view.clr_dict_list[self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())]
            #Invert tuples.
            #mayavi_view.default_color_palette = midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=True)

            #Convert to mayavi floats.
            mayavi_view.default_mayavi_palette = midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=False)

            #print("MAYAVI PALETTE", mayavi_view.default_mayavi_palette)
            #mayavi_view.default_mayavi_palette = midiart.convert_dict_colors(mayavi_view.default_mayavi_palette, invert=True)
            print("MAYAVI PALETTE", mayavi_view.default_mayavi_palette)
            #palette = \
            #midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=False)
            #Invert tuples.

            #Invert Color Tuples (swap R with B)
            #mayavi_view.default_mayavi_palette = \
            #midiart.convert_dict_colors(mayavi_view.default_color_palette, invert=True)
            #A tuple R\B switch happens here; tuple is inverted.

            mayavi_view.current_palette_name = self.listCtrl.GetItemText(self.listCtrl.GetFocusedItem())
            print("3")

        print("Current Palette Name Changed", mayavi_view.current_palette_name)
        self.UpdatePreview()


class MIDIArt3DDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='3idiArt'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #Points
        self.points = None

        #Panels
        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, size=(485,485), style=wx.BORDER_RAISED)
        #self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (500, 500), style=wx.BORDER_RAISED)
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (450, 450), style=wx.BORDER_RAISED)

        #Disable main mv window before proceeding

        # super().GetParent().GetTopLevelParent().mayaviviewcontrolpanel.Disable()
        # super().GetParent().GetTopLevelParent().pianorollpanel.pianoroll.Disable()


        self.mv = super().GetParent().GetTopLevelParent().mayavi_view
        self.mv.scene3d.disable_render = True

        self.mini_mv = MayaviMiniView(parent=self)
        self.mini = self.mini_mv.edit_traits(parent=self.imgPreviewPanel, kind='subpanel').control

        #toplevel = super().GetParent().GetTopLevelParent()


        #Help Text
        self.helpStatic = wx.StaticText(self.ctrlsPanel, -1, "Load a point cloud and manipulate its 3-dimensional "
                                                              "aspects as music \n                      with a "
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
        self.btnLoadPly = wx.Button(self.ctrlsPanel, -1, "Load Point Cloud")
        self.btnLoadPly.SetToolTip(tipString="Load Ply will only be enabled if an actor is empty.")
        self.Bind(wx.EVT_BUTTON, self.OnLoadPly, self.btnLoadPly)

        # self.OnComboBoxSelection(evt=None)   #self.points is written in this function.


        #Standard Reorientation
        self.btnStandardReo = wx.Button(self.ctrlsPanel, -1, "Standard Reorientation")
        self.Bind(wx.EVT_BUTTON, self.OnStandardReorientation, self.btnStandardReo)
        # pointsVar_Reo = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        self.scaleVar_Reo = wx.TextCtrl(self.ctrlsPanel, -1, "1", size=(70, -1), style=wx.TE_CENTER)

        #Trim
        self.btnTrim = wx.Button(self.ctrlsPanel, -1, "Trim Points")
        self.Bind(wx.EVT_BUTTON, self.OnTrim, self.btnTrim)
        # pointsVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        self.axisVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "y", size=(70, -1), style=wx.TE_CENTER)
        self.trimVar_Trim = wx.TextCtrl(self.ctrlsPanel, -1, "1", size=(70, -1), style=wx.TE_CENTER)

        # Scale
        self.btnScale = wx.Button(self.ctrlsPanel, -1, "Scale Points")
        self.Bind(wx.EVT_BUTTON, self.OnScale, self.btnScale)
        self.scaleVar_Scale = wx.TextCtrl(self.ctrlsPanel, -1, "2", size=(70, -1), style=wx.TE_CENTER)

        #Rotate
        self.btnRotate = wx.Button(self.ctrlsPanel, -1, "Rotate Points")
        self.Bind(wx.EVT_BUTTON, self.OnRotate, self.btnRotate)
        # pointsVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "", size=(60, -1), style=wx.TE_CENTER)
        self.axisVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "y", size=(70, -1), style=wx.TE_CENTER)
        self.degreesVar_Rot = wx.TextCtrl(self.ctrlsPanel, -1, "90", size=(70, -1), style=wx.TE_CENTER)

        #Transform
        self.btnTransform = wx.Button(self.ctrlsPanel, -1, "Transform Points")
        self.Bind(wx.EVT_BUTTON, self.OnTransform, self.btnTransform)
        self.axisVar_Trans = wx.TextCtrl(self.ctrlsPanel, -1, "z", size=(70, -1), style=wx.TE_CENTER)
        self.offsetVar_Trans = wx.TextCtrl(self.ctrlsPanel, -1, "5", size=(70, -1), style=wx.TE_CENTER)



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
        sizerStandardReo.Add(self.btnStandardReo, 0, wx.ALIGN_CENTER, 30)
        # sizerStandardReo.Add(pointsVar_Reo, 0, 50, 20)
        # sizerStandardReo.Add(scaleVar_Reo, 0, 50, 20)
        # horSizer1.Add(pointsVar_Reo, 0, 50, 20)
        horSizer1.Add(self.scaleVar_Reo, 0, 50, 20)
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
        horSizer5.AddSpacer(104)
        sizerTransform.Add(self.btnTransform, 0, wx.ALIGN_CENTER, 30)
        horSizer5.Add(self.axisVar_Trans, 0, 50, 20)
        horSizer5.Add(self.offsetVar_Trans, 0, 50, 20)
        sizerTransform.Add(horSizer5, 0, wx.ALIGN_CENTER, 10)

        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        sizerCtrls.Add(self.helpStatic, 0, wx.ALL | wx.ALIGN_CENTER,16)
        #sizerCtrls.Add(indexSizer, 0, wx.ALL | wx.ALIGN_CENTER, 18)


        sizerCtrls.Add(self.btnLoadPly, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        sizerCtrls.Add(sizerStandardReo, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizerCtrls.Add(sizerScale, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizerCtrls.Add(sizerTrim, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizerCtrls.Add(sizerRotate, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizerCtrls.Add(sizerTransform, 0, wx.ALL | wx.ALIGN_LEFT, 20)

        # self.ctrlsPanel.SetSizer(indexSizer)
        # self.ctrlsPanel.SetSizer(sizerStandardReo)
        # self.ctrlsPanel.SetSizer(sizerTrim)
        # self.ctrlsPanel.SetSizer(sizerScale)
        # self.ctrlsPanel.SetSizer(sizerRotate)
        #sizeCtrlsn.Add(self.btnRedrawMayaviView, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        #sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 1)

        sizerHor = wx.BoxSizer(wx.HORIZONTAL)
        sizerHor.Add(self.ctrlsPanel, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizerHor.Add(self.imgPreviewPanel, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        #self.mini.FitInside()
        #print("SIZE", self.mini.Size)
        #self.mini_mv.remove_highlighter_plane()
        #self.mini_mv.remove_grid_reticle()
        self.mv.insert_piano_grid_text_timeplane(length=self.mv.grid3d_span, volume_slice=None, figure=self.mini_mv.scene_mini.mayavi_scene)
        self.mv.insert_note_text(text="♫Point Cloud Processing♫", color=(1, 1, 0), figure=self.mini_mv.scene_mini.mayavi_scene, scale=11)
        self.mini_mv.scene_mini.background = (0/255, 0/255, 0/255)  #(222/255, 222/255, 0/255)
        self.mini.SetSize((446, 446))

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(sizerHor, 30)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 20)

        self.ctrlsPanel.SetSizer(sizerCtrls)
        self.SetSizerAndFit(sizerMain)


    def OnLoadPly(self, evt):
        with wx.FileDialog(self, "Open Ply file", wildcard="Ply files (*.ply)|*.ply",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            print(pathname)
            try:
                self.ply = pathname
                self.ply_name = os.path.basename(pathname)
                self.points = midiart3D.get_points_from_ply(self.ply)
                self.mlab_call = self.mv.insert_array_data(self.points, color=(1, 1, 0),
                                                                figure=self.mini_mv.scene_mini.mayavi_scene,
                                                                scale_factor=1)
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


    # def OnComboBoxSelection(self, evt):
    #     points = super().GetParent().mv.actors[int(self.cbActorIndices.GetSelection())]._points
    #     if points.size is 0:
    #         self.btnLoadPly.Enable()  #If no points, allow for the loading of a .ply.
    #     else:
    #         self.btnLoadPly.Disable() #If there are points, select a different actor to avoid overlapping notes.
    #     self.points = points


    #Points processing functions
    def OnStandardReorientation(self, evt, points=None, scale=1.):
        print("Standard Reorientation of points...")

        self.marker = 0
        #Cleans strays on first call only.
        if self.marker < 1:
            self.points = midiart3D.standard_reorientation(points=self.points,
                                                           scale=int(self.scaleVar_Reo.GetValue()), clean=True)
            self.marker = 1
        else:
            self.points = midiart3D.standard_reorientation(points=self.points,
                                                           scale=int(self.scaleVar_Reo.GetValue()), clean=False)
        self.mlab_call.mlab_source.trait_set(points=self.points)
        return self.points


    def OnTrim(self, evt, points=None, axis = 'y', trim = 0):
        print("Trimming points...")

        self.points = midiart3D.trim(points=self.points,
                                     axis=str(self.axisVar_Trim.GetValue()),
                                     trim=int(self.trimVar_Trim.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        print("Trimmed points.")
        return self.points


    def OnScale(self, evt, points=None, scale_factor=2):
        #Todo Write
        print("Scaling points...")

        midiart3D.scale_points(self.points, scale=float(self.scaleVar_Scale.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        return self.points


    def OnRotate(self, evt, points=None, axis = 'y', degrees=90):
        print("Rotating points...")

        self.points = midiart3D.rotate_array_points_about_axis(points=self.points,
                                                               axis=str(self.axisVar_Rot.GetValue()),
                                                               degrees=int(self.degreesVar_Rot.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        return self.points


    def OnTransform(self, coords_array=None, offset=0, axis='y', center_axis=False, positive_octant=False):
        print("Transforming points...")

        self.points = midiart3D.transform_points_by_axis(coords_array=self.points,
                                                         offset=int(self.offsetVar_Trans.GetValue()),
                                                         axis=str(self.axisVar_Trans.GetValue()))
        self.mlab_call.mlab_source.trait_set(points=self.points)
        return self.points




    # def On3DDisplayRedraw(self, evt):
    #     super().GetParent().mv.redraw_mayaviview()






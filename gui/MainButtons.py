import wx
from midas_scripts import musicode, midiart, music21funcs, midiart3D
from gui import Preferences
import music21
from mayavi import mlab
import cv2, numpy
import numpy as np
import os
import subprocess
import random
from collections import OrderedDict

class MainButtonsPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        sizer = wx.BoxSizer(wx.VERTICAL)

        btn_Music21_Converter_Parse = wx.Button(self, -1, "Midi\Score \n Import")
        sizer.Add(btn_Music21_Converter_Parse, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnMusic21ConverterParseDialog, btn_Music21_Converter_Parse)

        btn_musicode = wx.Button(self, -1, "Musicode" )
        sizer.Add(btn_musicode, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnMusicodeDialog, btn_musicode)

        btn_MIDIart = wx.Button(self, -1, "MIDI Art")
        sizer.Add(btn_MIDIart, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArtDialog, btn_MIDIart)

        btn_MIDIart3D = wx.Button(self, -1, "3IDI Art")
        sizer.Add(btn_MIDIart3D, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnMIDIArt3DDialog, btn_MIDIart3D)

        # btn_show_in_FLStudio = wx.Button(self, -1, "Show in FLStudio")
        # sizer.Add(btn_show_in_FLStudio, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinFLStudio, btn_show_in_FLStudio)

        # btn_show_in_MuseScore = wx.Button(self, -1, "Show in MuseScore")
        # sizer.Add(btn_show_in_MuseScore, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowinMuseScore, btn_show_in_MuseScore)

        # btn_show_stream_txt = wx.Button(self, -1, "Show Stream Text")
        # sizer.Add(btn_show_stream_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowStreamTxt, btn_show_stream_txt)

        btn_update_stream = wx.Button(self, -1, "Update Stream")
        sizer.Add(btn_update_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnUpdateStream, btn_update_stream)

        btn_clear_pianoroll = wx.Button(self, -1, "Clear Piano Roll")
        sizer.Add(btn_clear_pianoroll, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnClearPianoRoll , btn_clear_pianoroll)

        # btn_print_cell_sizes = wx.Button(self, -1, "Print Cell Sizes")
        # sizer.Add(btn_print_cell_sizes, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnPrintCellSizes , btn_print_cell_sizes)
        #
        # btn_grid_to_stream = wx.Button(self, -1, "Grid To Stream")
        # sizer.Add(btn_grid_to_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnGridToStream , btn_grid_to_stream)


        self.SetSizer(sizer)
        sizer.Fit(self)

        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnDialogClosed)

        #Update user-generated name.
        # self.mc_dialog = MusicodeDialog()
        # self.mc_dialog.user_named = self.GetTopLevelParent().musicode.musicode_name

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
        dlg = Music21ConverterParseDialog(self, -1, "       music21.converter.parse")
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
        print("Dialog closed")
        print(type(dialog))
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
        #Variables..
        # musicode_name = self.GetTopLevelParent().musicode.musicode_name
        # shorthand_name = self.GetTopLevelParent().musicode.sh
        musicode_name = dialog.input_mcname.GetLineText(0)
        if dialog.input_mcname.GetLineText(0) == "" or None:
            musicode_name = "User_Generated"
        shorthand_name = dialog.input_sh.GetLineText(0)
        if dialog.input_sh.GetLineText(0) == "" or None:
            shorthand_name = "ug"
        if dialog.create_musicode.GetValue() is True and btn == "OK":
            print("DialogCheck:", dialog.create_musicode.GetValue())
            stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream()  # TODO Change to currentActor's currentZplane upon completion.
            self.GetTopLevelParent().musicode.make_musicode(stream, musicode_name, shorthand_name, filepath=None,
                                     selection=str(dialog.inputTxt.GetLineText(0)), write=False, timeSig=None)
            self.GetTopLevelParent().pianorollpanel.pianoroll.ClearGrid()
            #print("DialogCheck:", dialog.createMusicode.GetValue())
        elif dialog.create_musicode.GetValue() is False and btn == "OK":
            print("DialogCheck:", dialog.create_musicode.GetValue())
            stream = self.GetTopLevelParent().musicode.translate(
                dialog.rdbtnMusicodeChoice.GetString(dialog.rdbtnMusicodeChoice.GetSelection()),
                dialog.inputTxt.GetLineText(0))
            print("LINETEXT:", dialog.inputTxt.GetLineText(0))
            self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)



    def _OnMIDIArtDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        if btn == "OK":
            pathname = dialog.pathname
            pixels = dialog.img     #2D array (2D of only on\off values.)
            pixels2 = dialog.img2   #3D array (2D of color tuples)
            pixels_resized = dialog.resizedImg
            gran = dialog.pixScaler
            print("PIXELS", pixels)
            print("PIXELS2", pixels2)
            print("PIXELS_RESIZED:", pixels, type(pixels))
            print("pixels shape", numpy.shape(pixels))

            mayavi_view = self.GetTopLevelParent().mayavi_view
            #default_color_palette = mayavi_view.default_color_palette
            mayavi_color_palette = mayavi_view.default_mayavi_palette

            if dialog.EdgesCheck:
                edges = cv2.Canny(pixels_resized, 100, 200)
                stream = midiart.make_midi_from_grayscale_pixels(edges, gran, True,  note_pxl_value=255)   ##dialog.inputKey.GetValue(), , colors=False
                print("EdgeStream:", stream)
                stream.show('txt')
                points = midiart3D.extract_xyz_coordinates_to_array(stream)
                index = len(mayavi_view.actors)
                name = str(len(mayavi_view.actors)) + "_" + "Edges" + "_" + dialog.img_name
                #clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)


            elif dialog.ColorsCheck:
                #TODO Display in grid upon completion of Actors\Z-Planes classes.
                print("PREPixels2:", pixels2)
                print("Gran", gran)
                #stream = midiart.transcribe_colored_image_to_midiart(pixels2, gran, connect=False, keychoice=None, colors=None)

                coords_dict = midiart.separate_pixels_to_coords_by_color(pixels2, mayavi_view.cur_z, nn=True)

                #TODO This logic needs to go INSIDE the separte_pixels_to_coords_by_color function.
                num_dict = OrderedDict()
                num_dict.fromkeys([num for num in mayavi_color_palette.keys()])
                for c in mayavi_color_palette.keys():
                    for e in coords_dict.keys():
                        if mayavi_color_palette[c] == e:
                            num_dict[c] = coords_dict[e]
                for d in num_dict.keys():
                    if num_dict[d] is None:
                        del(num_dict[d])

                #Main call.
                for h in num_dict.keys():
                    index = len(mayavi_view.actors)
                    # for i in mayavi_color_palette.keys():
                    #     if mayavi_color_palette[i] == h:
                            #Get the color we are on.
                    clr = mayavi_color_palette[h]
                    name = "Clrs" + "_" + str(h) + "_" + dialog.img_name
                    actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                    for j in mayavi_view.actors:
                        if j.name == name:
                            print("Points here?")
                            j.change_points(num_dict[h])
                            print("Color Change:", clr)
                            j.color = clr


            elif dialog.QRCheck:
                stream = midiart.make_midi_from_grayscale_pixels(pixels_resized, gran, False, note_pxl_value=0)
                stream.show('txt')
                points = midiart3D.extract_xyz_coordinates_to_array(stream)
                index = len(mayavi_view.actors)
                name = str(len(mayavi_view.actors)) + "_" + "Edges" + "_" + dialog.img_name
                # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
                # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)
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
            points = midiart3D.extract_xyz_coordinates_to_array(stream)
            index = len(mayavi_view.actors)
            name = str(len(mayavi_view.actors)) + "_" + "Midi" + "_" + dialog.midi_name
            # clr = color_palette[random.randint(1, 16)]  #TODO Random color of 16 possible for now.
            actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(index, name)
            # self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)
            for j in mayavi_view.actors:
                if j.name == name:
                    print("Points here?")
                    j.change_points(points)
            #self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(stream)



    def _OnMIDIArt3DDialogClosed(self, dialog, evt):
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
                ply = dialog.ply
            except AttributeError:
                ply = None
            if ply is not None:
                points = midiart3D.get_points_from_ply(dialog.ply)
                print(points)
                #planes_dict = midiart3D.get_planes_on_axis(points, 'z', ordered=True, clean=True)
                #TODO Delete the startup piano roll/actor when loading ply. ---Still do this?
                # try:
                #     self.GetTopLevelParent().pianorollpanel.DeletePianoRoll(1)
                # except IndexError:
                #     pass
                mayavi_view = self.GetTopLevelParent().mayavi_view

                #Establish "Midas Actor" name and index.
                #TODO Acquire from dialog
                i = len(mayavi_view.actors)
                name = str(len(mayavi_view.actors)) + "_" + "PointCloud" + "_" + dialog.ply_name
                actor = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox.new_actor(i, name)

                for j in mayavi_view.actors:
                    if j.name == name:
                        print("Points here?")
                        j.change_points(points)
            else:
                pass
                #index_list = [k for k in planes_dict.keys()]
                # for k in index_list:
                #     self.GetTopLevelParent().pianorollpanel.InsertNewPianoRoll(int(index_list.index(k)))
                #     self.GetTopLevelParent().pianorollpanel.pianoroll.StreamToGrid(midiart3D.extract_xyz_coordinates_to_stream((np.array(planes_dict[k]))))


        #r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"


class MusicodeDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Musicode' ):

        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #MODE
        self.translate_musicode = wx.CheckBox(self, -1, "Translate Musicode")
        self.create_musicode = wx.CheckBox(self, -1, "Create Musicode")

        self.create_musicode.SetValue(True)  ##Set to translate at the ready by default.

        #Musicode name.
        self.name_static = wx.StaticText(self, -1, "Musicode Name",     style=wx.ALIGN_RIGHT)
        self.input_mcname = wx.TextCtrl(self, -1, "", size=(90, -1), style=wx.TE_CENTER)

        #Shorthand variable name.
        self.sh_static = wx.StaticText(self, -1, "Shorthand", style=wx.ALIGN_RIGHT)
        self.input_sh = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        #self.inputTxt2 = wx.TextCtrl(self, -1, "", size=(250,-1))

        self.user_named = super().GetParent().GetTopLevelParent().musicode.musicode_name  #Thith is the coolest thing I have ever theen.
        print("User_Named:", self.user_named)

        self.musicodesList = sorted(list(musicode.mc.shorthand.keys()))
        self.musicodesList.append(self.user_named)


        self.inputTxt = wx.TextCtrl(self, -1, "", size=(250,-1), name="Translate\\Create")
        self.rdbtnMusicodeChoice = wx.RadioBox(self, -1, "Musicode Choice",
                                            wx.DefaultPosition, wx.DefaultSize,
                                            self.musicodesList,
                                            2, wx.RA_SPECIFY_COLS)
        #self.userMusicodeChoice = wx.RadioBox(self, -1, "")

        #Bindings.
        self.Bind(wx.EVT_CHECKBOX, self.OnPolarizeCheckboxes)

        #Sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        #Sizer adds.
        sizer2.Add(self.translate_musicode, 0, wx.ALL | wx.ALIGN_TOP, 20)
        sizer2.Add(self.create_musicode, 0, wx.ALL | wx.ALIGN_TOP, 20)

        sizer3.Add(self.name_static, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer3.Add(self.input_mcname, 0, wx.ALL | wx.ALIGN_RIGHT, 20)

        sizer4.Add(self.sh_static, 0, wx.ALL | wx.ALIGN_LEFT, 20)
        sizer4.Add(self.input_sh, 0, wx.ALL | wx.ALIGN_CENTER, 20)

        sizer.Add(sizer2, 0, wx.ALL | wx.ALIGN_TOP, 20)
        sizer.Add(sizer3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer.Add(sizer4, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)

        sizer.Add(self.inputTxt,0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer.Add(self.rdbtnMusicodeChoice,0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 20)


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

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    #TODO Needs work.
    def OnPolarizeCheckboxes(self, event):
        if self.create_musicode.IsChecked(): #Click on other one...
            self.translate_musicode.SetValue(not self.create_musicode.IsChecked())

        elif self.translate_musicode.IsChecked():  #True by default.
            #self.translate_musicode.SetValue(not self.translate_musicode.IsChecked()) #
            self.create_musicode.SetValue(not self.translate_musicode.IsChecked())
            #pass


        # elif self.translate_musicode.GetValue() is False:
        #     self.create_musicode.SetValue(True)
        # elif self.create_musicode.GetValue() is False:
        #     self.translate_musicode.SetValue(True)


class MIDIArtDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art' ):

        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (400, 400), style=wx.BORDER_RAISED)
        self.displayImage = None

        self.btnLoadImage = wx.Button(self.ctrlsPanel, -1, "Load Image")

        self.chbxEdges = wx.CheckBox(self.ctrlsPanel, -1, "Edges")
        self.chbxColorImage = wx.CheckBox(self.ctrlsPanel, -1, "Color Image")
        self.chbxQRCode = wx.CheckBox(self.ctrlsPanel, -1, "QR Code")


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

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
        sizerCtrls.Add(self.chbxEdges, 0, wx.ALL  | wx.ALIGN_LEFT, 10)
        sizerCtrls.Add(self.chbxColorImage, 0, wx.ALL  | wx.ALIGN_CENTER_HORIZONTAL, 10)
        sizerCtrls.Add(self.chbxQRCode, 0, wx.ALL  | wx.ALIGN_RIGHT, 10)
        sizerCtrls.Add(self.btnLoadImage, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerCtrls.Add(self.sldrHeight, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)


        keysizer = wx.BoxSizer(wx.HORIZONTAL)
        keysizer.Add(self.txtKey, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        keysizer.Add(self.inputKey, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerCtrls.Add(keysizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        sizerCtrls.Add(self.rdbtnGranularity, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)


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
        sizerHor.Add(self.ctrlsPanel)
        sizerHor.Add(self.imgPreviewPanel, 0, wx.ALL, 20)

        sizerMain = wx.BoxSizer(wx.VERTICAL )
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
                self.pathname = pathname
                self.img = cv2.imread(pathname, 0)
                #print(type(self.img))
                self.img_name = os.path.basename(pathname)
                self.img2 = cv2.imread(pathname, cv2.IMREAD_COLOR)
                self.EdgesCheck = self.chbxEdges.IsChecked()
                self.ColorsCheck = self.chbxColorImage.IsChecked()
                self.QRCheck = self.chbxQRCode.IsChecked()
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

        if self.displayImage:
            self.displayImage.Destroy()

        self.pixScaler = int(8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        height = int(self.sldrHeight.GetValue())
        width = int(height / len(self.img) * len(self.img[0]))

        self.resizedImg = cv2.resize(self.img, (width, height), cv2.INTER_AREA)

        self.previewImg = cv2.resize(self.resizedImg, (self.pixScaler*width, height), cv2.INTER_AREA)
        rgb = cv2.cvtColor(self.previewImg, cv2.COLOR_GRAY2RGB)

        #print("self.edges.shape=", self.edges.shape)
        h, w = self.previewImg.shape[:2]
        self.im = wx.ImageFromBuffer(w, h, rgb)

        self.displayImage = wx.StaticBitmap(self.imgPreviewPanel, -1, wx.Bitmap(self.im), wx.DefaultPosition, (w,h), wx.ALIGN_CENTER)


class MIDIArt3DDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #LoadPly
        self.btnLoadPly = wx.Button(self, -1, "Load Point Cloud")
        self.Bind(wx.EVT_BUTTON, self.OnLoadPly, self.btnLoadPly)
        #Redraw MayaviView
        self.btnRedrawMayaviView = wx.Button(self, -1, "Redraw Mayavi Figure")
        self.Bind(wx.EVT_BUTTON, self.On3DDisplayRedraw, self.btnRedrawMayaviView)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        # sizerMain.Add(sizerHor, 30)

        sizerMain.Add(self.btnLoadPly, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(self.btnRedrawMayaviView, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 1)

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
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


    def On3DDisplayRedraw(self, evt):
        super().GetParent().GetTopLevelParent().mayavi_view.redraw_mayaviview()


class Music21ConverterParseDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)
        #self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)

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
        sizerMain.Add(self.btnLoadMidi, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 1)

        #sizerCtrls = wx.BoxSizer(wx.VERTICAL)

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

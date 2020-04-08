import wx
from midas_scripts import musicode, midiart, music21funcs, midiart3D
import music21
import cv2, numpy
import numpy as np
import os
import subprocess
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

        btn_show_in_FLStudio = wx.Button(self, -1, "Show in FLStudio")
        sizer.Add(btn_show_in_FLStudio, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnShowinFLStudio, btn_show_in_FLStudio)

        btn_show_in_MuseScore = wx.Button(self, -1, "Show in MuseScore")
        sizer.Add(btn_show_in_MuseScore, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnShowinMuseScore, btn_show_in_MuseScore)

        # btn_show_stream_txt = wx.Button(self, -1, "Show Stream Text")
        # sizer.Add(btn_show_stream_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.Bind(wx.EVT_BUTTON, self.OnShowStreamTxt, btn_show_stream_txt)

        btn_update_stream = wx.Button(self, -1, "Update Stream")
        sizer.Add(btn_update_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnUpdateStream, btn_update_stream)

        btn_clear_pianoroll = wx.Button(self, -1, "Clear Piano Roll")
        sizer.Add(btn_clear_pianoroll, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnClearPianoRoll , btn_clear_pianoroll)

        btn_print_cell_sizes = wx.Button(self, -1, "Print Cell Sizes")
        sizer.Add(btn_print_cell_sizes, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnPrintCellSizes , btn_print_cell_sizes)

        btn_grid_to_stream = wx.Button(self, -1, "Grid To Stream")
        sizer.Add(btn_grid_to_stream, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.Bind(wx.EVT_BUTTON, self.OnGridToStream , btn_grid_to_stream)


        self.SetSizer(sizer)
        sizer.Fit(self)

        self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnDialogClosed)

    def OnGridToStream(self, evt):
        self.GetTopLevelParent().pianorollpanel.currentPage.GridToStream()

    def OnPrintCellSizes(self, evt):
        self.GetTopLevelParent().pianorollpanel.print_cell_sizes()

    def OnClearPianoRoll(self,evt):
        self.GetTopLevelParent().pianorollpanel.currentPage.ClearGrid()
        self.GetTopLevelParent().pianorollpanel.currentPage.stream = music21.stream.Stream()

    # def OnDeleteAllPianoRolls(self, evt):
    #     self.GetTopLevelParent().

    def OnUpdateStream(self,evt):
        self.GetTopLevelParent().pianorollpanel.currentPage.UpdateStream()

    def OnShowStreamTxt(self, evt):
        self.GetTopLevelParent().pianorollpanel.currentPage.stream.show('txt')

    def OnMusic21ConverterParseDialog(self, evt):
        dlg = Music21ConverterParseDialog(self, -1, "       music21.converter.parse")
        dlg.ShowWindowModal()

    def OnMusicodeDialog(self, evt):
        dlg = MusicodeDialog(self, -1, "Create Musicode")
        dlg.ShowWindowModal()
    
    def OnMIDIArtDialog(self, evt):
        dlg = MIDIArtDialog(self, -1, "Create MIDIArt")
        dlg.ShowWindowModal()

    def OnMIDIArt3DDialog(self, evt):
        dlg = MIDIArt3DDialog(self, -1, "Display MIDIArt3D")
        dlg.ShowWindowModal()

    def OnDialogClosed(self, evt):
        dialog = evt.GetDialog()
        print("Dialog closed")
        print(type(dialog))
        if type(dialog) is MusicodeDialog:
            self._OnMusicodeDialogClosed(dialog, evt)
        elif type (dialog) is MIDIArtDialog:
            self._OnMIDIArtDialogClosed(dialog, evt)
        elif type (dialog) is Music21ConverterParseDialog:
            self._OnM21ConverterParseDialogClosed(dialog, evt)
        elif type (dialog) is MIDIArt3DDialog:
            self._OnMIDIArt3DDialogClosed(dialog, evt)
        dialog.Destroy()

    def _OnMusicodeDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        if btn == "OK":
            stream = musicode.mc.translate(
                dialog.rdbtnMusicodeChoice.GetString(dialog.rdbtnMusicodeChoice.GetSelection()),
                dialog.inputTxt.GetLineText(0))
            self.GetTopLevelParent().pianorollpanel.currentPage.StreamToGrid(stream)



    def _OnMIDIArtDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        if btn == "OK":
            pixels = dialog.edges
            print (pixels)
            print("pixels shape", numpy.shape(pixels))

            stream = midiart.make_midi_from_grayscale_pixels(pixels, 0.125, True,  note_pxl_value=255)   ##dialog.inputKey.GetValue(), , colors=False
            stream.show('txt')

            self.GetTopLevelParent().pianorollpanel.currentPage.StreamToGrid(stream)

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
            stream = music21.converter.parse(dialog.midi)
            stream.show('txt')
            self.GetTopLevelParent().pianorollpanel.currentPage.StreamToGrid(stream)

    def _OnMIDIArt3DDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'

        if btn == "OK":
            points = midiart3D.get_points_from_ply(dialog.ply)
            planes_dict = midiart3D.get_planes_on_axis(points, 'z', ordered=True, clean=True)
            #Delete the startup piano roll when loading ply.
            try:
                self.GetTopLevelParent().pianorollpanel.DeletePianoRoll(1)
            except IndexError:
                pass
            index_list = [k for k in planes_dict.keys()]
            for k in index_list:
                self.GetTopLevelParent().pianorollpanel.InsertNewPianoRoll(int(index_list.index(k)))
                self.GetTopLevelParent().pianorollpanel.currentPage.StreamToGrid(midiart3D.extract_xyz_coordinates_to_stream((np.array(planes_dict[k]))))

    def OnShowinFLStudio(self, evt):
        grid = self.GetTopLevelParent().pianorollpanel.currentPage


        # s = music21funcs.matrix_to_stream(matrix, True, self.GetTopLevelParent().pianorollpanel.currentPage.pix_note_size)
        s = self.GetTopLevelParent().pianorollpanel.currentPage.stream
        s.show('txt')

        s.write("mid", os.getcwd() + os.sep + "MIDAS_temp.mid")
        print("\"C:\Program Files (x86)\Image-Line\FL Studio 12\FL64.exe\" \"" + os.getcwd() + os.sep + "MIDAS_temp.mid\"")
        subprocess.Popen([r"C:\Program Files (x86)\Image-Line\FL Studio 20\FL64.exe", os.getcwd() + os.sep + "MIDAS_temp.mid"])

    def OnShowinMuseScore(self, evt):
        s = self.GetTopLevelParent().pianorollpanel.currentPage.stream
        s.show('txt')

        s.write("mid", os.getcwd() + os.sep + "MIDAS_temp.mid")
        print("\"C:\Program Files\MuseScore 3\bin\MuseScore3.exe\" \"" + os.getcwd() + os.sep + "MIDAS_temp.mid\"")
        subprocess.Popen([r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe", os.getcwd() + os.sep + "MIDAS_temp.mid"])
        #r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"


class MusicodeDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Musicode' ):

        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.inputTxt = wx.TextCtrl(self, -1, "", size=(250,-1))

        self.rdbtnMusicodeChoice = wx.RadioBox(self, -1, "Musicode Choice",
                                            wx.DefaultPosition, wx.DefaultSize,
                                            sorted(list(musicode.mc.shorthand.keys())),
                                            2, wx.RA_SPECIFY_COLS)

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

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


class MIDIArtDialog(wx.Dialog):
    def __init__(self,parent,id,title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art' ):

        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.ctrlsPanel = wx.Panel(self, -1, wx.DefaultPosition, style=wx.BORDER_RAISED)
        self.imgPreviewPanel = wx.Panel(self, -1, wx.DefaultPosition, (400, 400), style=wx.BORDER_RAISED)
        self.displayImage = None
        self.btnLoadImage = wx.Button(self.ctrlsPanel, -1, "Load Image")

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

        #self.txtConnectNotes = wx.StaticText(self, -1, "Connect Notes?", style=wx.ALIGN_RIGHT)


        self.Bind(wx.EVT_BUTTON, self.OnLoadImage, self.btnLoadImage)
        self.Bind(wx.EVT_SLIDER, self.OnSliderChanged, self.sldrHeight)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxChanged, self.rdbtnGranularity)

        #Sizers
        sizerCtrls = wx.BoxSizer(wx.VERTICAL)
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
        sizerMain.Add(btnsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.SetSizerAndFit(sizerMain)


    def OnLoadImage(self, evt):
        with wx.FileDialog(self, "Open image file", wildcard="IMG files (*.png)|*.png|(*.jpeg)|*.jpeg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                self.img = cv2.imread(pathname, 0)
                self.UpdatePreview()
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


    def OnSliderChanged(self,event):
        if self.img is not None:
            self.UpdatePreview()

    def OnRadioBoxChanged(self,event):
        if self.img is not None:
            self.UpdatePreview()

    def UpdatePreview(self):

        if self.displayImage:
            self.displayImage.Destroy()

        self.pixScaler = int(8 * self.granularitiesDict[self.rdbtnGranularity.GetString(self.rdbtnGranularity.GetSelection())])

        height = int(self.sldrHeight.GetValue())
        width = int(height / len(self.img) * len(self.img[0]))

        resizedImg = cv2.resize(self.img, (width, height), cv2.INTER_AREA)
        self.edges = cv2.Canny(resizedImg, 100, 200)
        self.previewImg = cv2.resize(self.edges, (self.pixScaler*width, height), cv2.INTER_AREA)
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
        self.btnLoadPly = wx.Button(self, -1, "Load Point Cloud")
        self.Bind(wx.EVT_BUTTON, self.OnLoadPly, self.btnLoadPly)

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
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)


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
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

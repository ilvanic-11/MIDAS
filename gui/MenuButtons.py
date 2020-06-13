import wx
import subprocess
import os
import shutil
import time
import wx.richtext as rt
import pprint
import pydoc
import inspect
import copy
from gui import Preferences
import wx.lib.filebrowsebutton as filebrowse


#Imports for the help feature:
#TODO Better way to do this for the HelpDialog()
import mayavi
import music21
import open3d
import cv2
import numpy
#import sympy
import vtk
import tvtk
from midas_scripts import music21funcs, midiart, midiart3D, musicode


class CustomMenuBar(wx.MenuBar):

    def __init__(self, parent):
        super().__init__(style=0)
        self.parent = parent
        #A help dialog instance
        self.helper = HelpDialog(self, -1, "Help Window")

        #mayavi_view reference
        self.m_v = self.parent.mayavi_view

        #TODO Do this?
        #self.preferences = Preferences.PreferencesDialog()

        #wx.Frame.__init__(self, parent, id, 'Playing with menus', size=(500, 250))

        # File
        self.filemenu = wx.Menu()
        self.filemenu.Append(101, "&New Session\tCtrl+Shift+N", "This the text in the Statusbar")  # TODO Saved Midas States
        self.filemenu.Append(102, "&Open Session\tCtrl+O", "Open Slutsame")
        self.filemenu.Append(103, "&Save Session\tCtrl+S", "You may select Earth too")
        self.filemenu.Append(104, "&Save Session As\tCtrl+Shift+S")
        self.filemenu.Append(105, "&Import...\tCtrl+I")
        self.filemenu.Append(106, "&Import Directory\tCtrl+Shift+I")
        self.export = wx.Menu()
        self.export.Append(1500, "&Current Actor\tCtrl+E+1")
        self.export.Append(1501, "&All Actors\tCtrl+E+2")
        self.export.Append(1502, "&Current Actor's Current Zplane\tCtrl+E+3")
        self.export.Append(1503, "&All Actor's Zplanes\tCtrl+E+4")
        self.export.Append(1504, "&Selection\tCtrl+E+5")
        self.colors = wx.Menu()
        self.export.Append(1505, "&Colors", self.colors)
        self.export.Append(1506, "&Text\tCtrl+E+6")
        self.export.Append(1507, "&Image\tCtrl+E+7")
        self.export.Append(1508, "&Point Cloud\tCtrl+E+8")
        # Current Actor        self.filemenu.Append(108, "&Export As Directory\tCtrl+Shift+E")  # All Actors
        self.filemenu.Append(107, "Export...", self.export)
        self.filemenu.Append(109, "&Export Musicode\tCtrl+Shift+M")
        self.filemenu.Append(110, "&Export Movie\tCtrl+Alt+E")
        self.filemenu.Append(111, "&Preferences\tCtrl+P")
        self.filemenu.Append(112, "&Intermediary Path\t")  # The Default Save path for all files. Found in resources.
        self.filemenu.AppendSeparator()
        self.filemenu.Append(113, "&Exit", "Close this frame")
        # Add menu to the menu bar
        self.Append(self.filemenu, "&File")

        # Edit
        self.editmenu = wx.Menu()
        self.editmenu.Append(201, "Undo\tCtrl+Z")
        self.editmenu.Append(202, "Redo\tCtrl+Y")
        self.editmenu.Append(203, "Cut\tCtrl+X")
        self.editmenu.Append(204, "Copy\tCtrl+C")
        self.editmenu.Append(205, "Paste\tCtrl+V")
        self.editmenu.Append(206, "History")
        # a submenu in the 2nd menu
        # submenu = wx.Menu()
        # submenu.Append(2031, "Lanthanium")
        # submenu.Append(2032, "Cerium")
        # submenu.Append(2033, "Praseodymium")
        # menu2.Append(203, "Lanthanides", submenu)
        # Append 2nd menu
        self.Append(self.editmenu, "&Edit")

        # Show
        self.showmenu = wx.Menu()
        # Radio items
        self.showmenu.Append(301, "Show in DAW")  ###, wx.ITEM_RADIO, "a Python shell using wxPython as GUI"
        self.showmenu.Append(302, "Show in Musescore", "a simple Python shell using wxPython as GUI")    ###, wx.ITEM_RADIO)
        self.showmenu.Append(303, "Show in Word Processor", "a Python shell using tcl/tk as GUI")    ###, wx.ITEM_RADIO)
        self.showmenu.Append(304, "Show in PicPick\Paint", "a Python shell using tcl/tk as GUI")    ###, wx.ITEM_RADIO)
        self.showmenu.Append(305, "Show in Meshlab", "a simple Python shell using wxPython as GUI")    ###, wx.ITEM_RADIO)
        self.showmenu.Append(306, "Show in Blender", "a simple Python shell using wxPython as GUI")     ###, wx.ITEM_RADIO)
        self.showmenu.AppendSeparator()
        self.showmenu.Append(307, "Scene3d_1?", "", wx.ITEM_NORMAL)
        self.showmenu.Append(308, "project2", "", wx.ITEM_NORMAL)
        self.Append(self.showmenu, "&Show")

        # Tools
        self.toolsmenu = wx.Menu()
        # Check menu items
        self.analyzetools = wx.Menu()
        self.toolsmenu.Append(400, "Analyze", self.analyzetools)
        self.analyzetools.Append(1400, "Display Chord Details")
        self.analyzetools.Append(1401, "Display Music21.show('txt')")
        self.analyzetools.Append(1402, "Show Midi Data")
        self.analyzetools.Append(1403, "Show Cell Sizes Data")

        self.musicodetools = wx.Menu()
        self.toolsmenu.Append(401, "Musicode", self.musicodetools)
        self._append_musicode_tools()

        self.midiarttools = wx.Menu()
        self.toolsmenu.Append(402, "Midiart", self.midiarttools)
        self._append_midiart_tools()

        self.midiart3Dtools = wx.Menu()
        self.toolsmenu.Append(403, "3iDiart", self.midiart3Dtools)
        self._append_midiart3D_tools()

        self.music21funcstools = wx.Menu()
        self.toolsmenu.Append(404, "Music21Funcs", self.music21funcstools)
        self._append_music21funcs_tools()

        menu7 = wx.Menu()
        menu8 = wx.Menu()
        menu9 = wx.Menu()

        self.toolsmenu.Append(405, "Current ActorList to Shell", menu7)

        # Dict of coords_arrays or Stream with parts(we're dealing with multiple actors for colors...)
        self.toolsmenu.Append(406, "Current Actor to Shell", menu8)
        self.toolsmenu.Append(407, "Current Z-Plane to Shell", menu9)

        menu7.Append(700, "As Music21 Stream with Parts")
        menu7.Append(701, "As Dictionary of Points")

        menu8.Append(800, "As Music21 Stream")
        menu8.Append(801, "As Numpy Points")

        menu9.Append(900, "As Music21 Stream")
        menu9.Append(901, "As Numpy Points")
        self.Append(self.toolsmenu, "&Tools")



        # Help
        self.helpmenu = wx.Menu()
        item = wx.MenuItem(self.helpmenu, 500, "&Search-Help\tCtrl+Alt+S")  # , "This one has an icon"
        self.helpmenu.Append(item)
        self.helpmenu.Append(501, "About Midas...")
        self.helpmenu.AppendSeparator()
        self.helpmenu.Append(502, "Licensing\tShift+H")
        self.helpmenu.AppendSeparator()
        self.docsubmenu = wx.Menu()
        self.helpmenu.Append(503, "Documentation", self.docsubmenu)

        #Documentation Submenu
        self.docsubmenu.Append(600, "Python")
        self.docsubmenu.Append(601, "Music21")
        self.docsubmenu.Append(602, "Mayavi")
        self.docsubmenu.Append(603, "Numpy")
        self.docsubmenu.Append(604, "Sympy")
        self.docsubmenu.Append(605, "Open3D")
        self.docsubmenu.Append(606, "Open-CVPython")
        self.docsubmenu.Append(607, "VTK")
        self.docsubmenu.Append(608, "TVTK")

        # menu6.Append(601, "Midas Homepage")
        self.helpmenu.Append(504, "Midas Homepage")
        self.helpmenu.Append(505, "The Magic Hammer Homepage")
        self.helpmenu.Append(506, "Tutorials")
        self.helpmenu.Append(507, "Community")
        self.helpmenu.Append(508, "Google Search")
        self.helpmenu.Append(509, "Check for Updates...")
        self.helpmenu.Append(510, "Credits.")
        self.Append(self.helpmenu, "&Help")



    # #File Buttons Defined
    def OnNewSession(self, event):
        pass


    def OnOpenSession(self, event):
        pass


    def OnSaveSession(self, event):
        pass


    def OnSaveSessionAs(self, event):
        pass


    def OnImport(self, event):
        pass


    def OnImportDirectory(self, event):
        pass


    #Now Submenu
    #Define Export Submenu Functions
    #--------------------------------------------

    def OnExport_CurrentActor(self, event):
        print("Exporting Current Actor....")
        if len(self.m_v.actors) is not 0:
            for i in range(0, len(self.m_v.actors)):
                # alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
                # #If it's selected, unselect it.
                # if alb.IsSelected(i):
                if i == self.m_v.cur_ActorIndex:
                    intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
                    filename = self.m_v.actors[i].name
                    output = intermediary_path + filename + ".mid"
                    selected_stream = midiart3D.extract_xyz_coordinates_to_stream(self.m_v.actors[i]._points)
                    selected_stream.write('mid', output)
        pass

    def OnExport_AllActors(self, event):
        print("Exporting All Actors....")
        if len(self.m_v.actors) is not 0:
            for i in range(0, len(self.m_v.actors)):
                # alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
                # #If it's selected, unselect it.
                # if alb.IsSelected(i):
                intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
                filename = self.m_v.actors[i].name
                output = intermediary_path + filename + ".mid"
                self.m_v.actors[i]._stream = midiart3D.extract_xyz_coordinates_to_stream(self.m_v.actors[i]._points)
                self.m_v.actors[i].write('mid', output)
        pass

    #TODO *Be mindful of 'track mode' vs 'velocity mode' for later; when we have those modes for each zplane.
    def OnExport_CurrentActorsCurrentZplane(self, event):
        print("Exporting Current Actor's Current Zplane....")
        intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
        filename = self.m_v.CurrentActor().name
        output = intermediary_path + filename + ".mid"
        zplane = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points)[  #Todo user GridToStream()
            eval('self.m_v.cur_z')] #TODO Watch for debug errors here.
        self.m_v.CurrentActor()._stream = midiart3D.extract_xyz_coordinates_to_stream(zplane)
        self.m_v.CurrentActor()._stream.write('mid', output)


    #TODO *Same.
    def OnExport_AllCurrentActorsZplanes(self, event):
        print("Exporting all Current Actor's Zplanes....")
        intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
        planes_dict = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points)
        for zplane in planes_dict.keys():
            filename = self.m_v.CurrentActor().name + "_" + str(zplane)
            output = intermediary_path + filename + ".mid"
            stream = midiart3D.extract_xyz_coordinates_to_stream(planes_dict[zplane])
            stream.write('mid', output)


    def OnExport_Selection(self, event):
        print("Exporting Selection....")

        if len(self.m_v.actors) is not 0:
            for i in range(0, len(self.m_v.actors)):
                alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
                #If it's selected, unselect it.
                if alb.IsSelected(i):
                    intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
                    filename = self.m_v.actors[i].name
                    output = intermediary_path + filename + ".mid"
                    self.m_v.actors[i]._stream = midiart3D.extract_xyz_coordinates_to_stream(self.m_v.actors[i]._points)
                    self.m_v.actors[i]._stream.write('mid', output)
        pass


    def OnExport_Colors(self, event):
        print("Exporting Colors....")
        self.mv = self.GetTopLevelParent().mayavi_view
        self.mv.colors_call = int(self.GetTopLevelParent().menuBar.colors.FindItemById(event.GetId()).Name)
        num = -16
        for i in range(0, len(self.mv.actors)):
            if "Clrs%s" % str(self.mv.colors_call) == self.mv.actors[i].colors_instance:
                self.mv.actors[i]._stream = midiart3D.extract_xyz_coordinates_to_stream(self.mv.actors[i]._points, part=True)
                self.mv.actors[i]._stream.partsName = self.mv.actors[i].part_num
                self.mv.actors[i].priority = num
                self.mv.stream.append(self.mv.actors[i]._stream)
                num += 1
            else:
                pass
        print("MainStream Length:", len(self.mv.stream))
        if len(self.mv.stream) != 16:
            append_priority = set([i for i in range(-1, -17, -1)]).difference(set([i.priority for i in self.mv.stream])).pop()

            append_part = music21.stream.Part()
            for i in range(0, 16 - len(self.mv.stream)):
                append_part.priority = append_priority
                append_part.partsName = append_priority + 17
                #append_part.partsName = (16-(16-len(self.mv.stream))) + 1
                self.mv.stream.append(copy.deepcopy(append_part))
        else:
            pass
        intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
        filename = self.mv.colors_name + str(self.mv.colors_call)
        output = intermediary_path + filename + ".mid"
        midiart.set_parts_to_midi_channels(self.mv.stream, output)
        # Clear mainstream if it has already been used.
        if self.mv.stream.hasPartLikeStreams():
            for i in self.mv.stream:
                self.mv.stream.remove(i)
        else:
            pass


    def OnExport_Text(self, event):
        #TODO
        print("Exporting extracted musicode text as .txt....")
        pass

    def OnExport_PointCloud(self, event):
        #TODO
        print("Exporting _points as .ply....")
        pass

    def OnExport_Image(self, event):
        #TODO
        print("Exporting as img as .png/.jpg....")
        pass

    #self.export.Append(1500, "&Current Actor\tCtrl+E+1")
    # self.export.Append(1500, "&All Actors\tCtrl+E+2")
    # self.export.Append(1500, "&Current Actor's Current Zplane\tCtrl+E+3")
    # self.export.Append(1500, "&All Current Actor's Zplanes\tCtrl+E+4")
    # self.export.Append(1500, "&Selection\tCtrl+E+5")
    # self.export.Append(1500, "&Colors\tCtrl+E+6")
    # self.export.Append(1500, "&Text\tCtrl+E+7")
    # self.export.Append(1500, "&Point Cloud\tCtrl+E+8")
    # self.export.Append(1500, "&Image\tCtrl+E+9")





    def OnExportAsDirectory(self, event):
        pass






    def OnExportMusicode(self, event):
        print("Exporting Musicode...")
        user_Created = self.GetTopLevelParent().musicode.user_Created
        print("User Created")
        user_Created.show('txt')
        Punct_Names = self.GetTopLevelParent().musicode.Punct_Names
        Punct_Symbols = self.GetTopLevelParent().musicode.Punct_Symbols
        Punct_Workaround = self.GetTopLevelParent().musicode.Punct_Workaround
        musicode_name = self.GetTopLevelParent().musicode.musicode_name
        short_hand = self.GetTopLevelParent().musicode.sh

        full_new_musicode_path = self.GetTopLevelParent().musicode.full_new_musicode_path
        resource_path = os.path.dirname(os.path.abspath(r"musicode_libraries\\")) + "\\resources\\" + r"musicode_libraries\\"
        print("RPath:", resource_path)
        if os.path.exists(full_new_musicode_path):
            shutil.rmtree(resource_path + musicode_name + "\\\\", ignore_errors=True)
        os.mkdir(resource_path + musicode_name + "\\\\")
        full_new_musicode_path = self.GetTopLevelParent().musicode.full_new_musicode_path
        self.GetTopLevelParent().musicode.create_directories()
        
        for j in range(0, len(user_Created)):
            # user_generated_musicode[j].append(wrapper_list[j])
            element_wrapper = user_Created[j][-1]  # The last element in each measure.
            if type(element_wrapper) == music21.note.Rest:
                element_wrapper = user_Created[j][-2]
            if type(element_wrapper) == music21.bar.Barline:
                element_wrapper = user_Created[j][-3]
            # print(user_generated_musicode[j].measureNumber, stringz.obj)
            print("X", [user_Created[j]])
            # A check against writing empty measures and whether to write at all.
            if element_wrapper.obj is not ' ':
                if user_Created[j].hasElementOfClass(music21.note.Note) or user_Created[j].hasElementOfClass(
                        music21.chord.Chord):
                    if element_wrapper.obj.islower() and element_wrapper.obj not in Punct_Names:
                        user_Created[j].write("mid",
                                            full_new_musicode_path + "\\" + short_hand + "_" + "Lowercase\\" + "musicode" + "_" + short_hand + "_" + str(
                                                element_wrapper.obj) + ".mid")
                    elif element_wrapper.obj in Punct_Names or element_wrapper.obj in Punct_Symbols:
                        user_Created[j].write("mid",
                                            full_new_musicode_path + "\\" + short_hand + "_" + "Punctuation\\" + "musicode" + "_" + short_hand + "_" + str(
                                                Punct_Workaround[element_wrapper.obj]) + ".mid")
                    elif element_wrapper.obj.isupper():
                        user_Created[j].write("mid",
                                            full_new_musicode_path + "\\" + short_hand + "_" + "Uppercase\\" + "musicode" + "_" + short_hand + "_" + str(
                                                element_wrapper.obj) + ".mid")
                    elif element_wrapper.obj.isdigit():
                        user_Created[j].write("mid",
                                            full_new_musicode_path + "\\" + short_hand + "_" + "Numbers\\" + "musicode" + "_" + short_hand + "_" + str(
                                                element_wrapper.obj) + ".mid")
                else:
                    pass
            # print(j, stringz.obj)

        # Account for the " " space string manually, so user is encouraged not to set a musicode for a space.
        # Append "space_measure to user-generated musicode.
        #space_measure = music21funcs.empty_measure(timeSig)
        #user_generated_musicode.append(space_measure)
        print("FINAL_NEW_STREAM:")
        user_Created.show('txt')
        if not user_Created.hasElementOfClass(music21.note.Note):
            print("No musicode created. (stream still empty)  Create a musicode!")
        else:
            print("Musicode Written Successfully!")
        #self.userCreated = user_generated_musicode


    def OnExportMovie(self, event):
        print("Exporting Movie Frames as .jpgs...")
        movie_maker = self.m_v.engine.scenes[0].scene.movie_maker
        length = (self.m_v.grid3d_span)
        bpm_speed = self.GetTopLevelParent().mayavi_view.bpm    ###+ 60
        i_div = self.m_v.i_div

        print("# BPM:", bpm_speed)
        print("# Grid Length:", self.m_v.grid3d_span)
        print("# Animation Step Value:", 1/i_div)
        print("# of Measures:", length/4)   #Measures assumed to be in '4/4' time. #TODO Fix by syncing with a time signature object.
        print("# of Frames:", (length * i_div))
        print("# of Frames per Measure:", i_div*4)
        print("# of Frames per Beat:", i_div)

        #mayavi_view.volume_slice.remove()
        #mayavi_view.insert_volume_slice(length)
        #TODO Add to preferences as checkbox. (for animation without creating frames.)

        #Enable frame saving.
        if movie_maker.record is False:
            movie_maker.record = True
        self.m_v.animate(length, bpm_speed, i_div, sleep = 0)
        animator_instance = self.m_v.animate1
        animator_instance._start_fired()
        time.sleep(1)
        #TODO set movie_maker back False in animate function after loop completes.
        print("In Blender, set FPS to:", midiart3D.BPM_to_FPS(bpm_speed, i_div)) ##((bpm_speed * (i_div/4) /60)))
        pass


    def OnPreferences(self, event):
        dlg = Preferences.PreferencesDialog(self, -1, "Midas Preferences")
        dlg.ShowWindowModal()
        #pass


    def OnIntermediaryPath(self, event):
        wildcard = "Text files (*.txt)|*.txt|" \
                   "JPG files (*.jpg)|*.jpg|" \
                   "PNG files (*.png)|*.png|" \
                   "PLY files (*.ply)|*.ply|" \
                   "Midi files (*.mid)|*.mid|" \
                   "All files (*.*)|*.*"

        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=r".\resources\intermediary_path",
            defaultFile="",
            wildcard=wildcard,
            style=wx.FC_OPEN | wx.FD_MULTIPLE |
                  wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST |
                  wx.FD_PREVIEW
        )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            #self.log.WriteText('You selected %d files:' % len(paths))

            # for path in paths:
            #     self.log.WriteText('           %s\n' % path)

        # Compare this with the debug above; did we change working dirs?
        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()


    def OnExit(self, event):
        pass

        # #Edit Buttons Defined


    def OnUndo(self, event):
        pass


    def OnRedo(self, event):
        pass


    def OnCut(self, event):
        pass


    def OnCopy(self, event):
        pass


    def OnPaste(self, event):
        pass


    def OnHistory(self, event):
        pass


        # Show Buttons Defined


    def OnShowInDAW(self, event):
            # s = music21funcs.matrix_to_stream(matrix, True, self.GetTopLevelParent().pianorollpanel.currentPage.pix_note_size)
        s = self.GetTopLevelParent().pianorollpanel.currentPage.stream #TODO Change upon implementing Actors and Zplanes.
        s.show('txt')

        intermediary_path = os.sep + "resources" + os.sep + "intermediary_path" + os.sep

        s.write("mid", os.getcwd() + intermediary_path + "MIDAS_showtemp.mid")
            #TODO Option to choose DAW in Preferences.
        print("\"C:\Program Files (x86)\Image-Line\FL Studio 20\FL64.exe\" \"" + os.getcwd() + intermediary_path
              + "MIDAS_showtemp.mid\"")
        print("FL STUDIO")
        subprocess.Popen(
            [r"C:\Program Files (x86)\Image-Line\FL Studio 20\FL64.exe", os.getcwd() + intermediary_path + "MIDAS_showtemp.mid"])


    def OnShowInMuseScore(self, event):
        # TODO Change upon implementing Actors and Zplanes.
        s = self.GetTopLevelParent().pianorollpanel.currentPage.stream
        s.show('txt')

        intermediary_path = os.sep + "resources" + os.sep + "intermediary_path" + os.sep
        print("PATH:", os.getcwd() + intermediary_path)

        s.write("mid", os.getcwd() + intermediary_path + "MIDAS_showtemp.mid")
        #TODO Option to choose default "Score" program in Preferences.
        print("\"C:\Program Files\MuseScore 3\bin\MuseScore3.exe\" \"" + os.getcwd() + intermediary_path
              + "MIDAS_showtemp.mid\"")
        subprocess.Popen([r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe", os.getcwd() + intermediary_path
                          + "MIDAS_showtemp.mid"])


    def OnShowInWordProcessor(self, event):
        pass


    def OnShowInPaint(self, event):
        # PicPick by default, to be included in distribution.
        pass


    def OnShowInMeshlab(self, event):
        pass


    def OnShowInBlender(self, event):
        pass


    def OnScene3d_1(self, event):
        pass


    def OnProject2(self, event):
        pass


    ## Tools Buttons Defined
    #---------------------------------------------

    def OnDisplayChords(self, evt):
        chord_details_string = ""
        # for i, p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
        #     chord_details_string += f"Layer {i}\n"
        #     chord_details_string += music21funcs.print_chords_in_piece(p.stream)
        #     chord_details_string += "\n"

        z_stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream(update_actor=False)
        chord_details_string += music21funcs.print_chords_in_piece(z_stream)
        win = RichTextFrame(self, -1, chord_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Chord_Details")
        win.Show(True)

    def OnDisplayStreamShowTxt(self, evt):
        stream_details_string = ""
        # for i, p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
        #     stream_details_string += f"Layer {i}\n"
        #     stream_details_string += music21funcs.print_show_streamtxt(p.stream)
        #     stream_details_string += "\n"
        z_stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream(update_actor=False)

        stream_details_string += music21funcs.print_show_streamtxt(z_stream)
        win = RichTextFrame(self, -1, stream_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Stream_Details")
        win.Show(True)

    def OnDisplayMidiData(self, evt):
        midi_details_string = ""
        # for i, p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
        #     midi_details_string += f"Layer {i}\n"
        #     midi_details_string += music21funcs.print_midi_data(p.stream)
        #     midi_details_string += "\n"
        z_stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream(update_actor=False)

        midi_details_string += music21funcs.print_midi_data(z_stream)
        win = RichTextFrame(self, -1, midi_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Midi_Details")
        win.Show(True)

    def OnDisplayCellSizesData(self, evt):
        cell_details_string = ""
        # for i, p in enumerate(self.GetTopLevelParent().pianorollpanel.pianorolls):
        #     cell_details_string += f"Layer {i}\n"
        #     cell_details_string += self.GetTopLevelParent().pianorollpanel.print_cell_sizes()
        #     cell_details_string += "\n"
        #z_stream = self.GetTopLevelParent().pianorollpanel.pianoroll.GridToStream(update_actor=False)
        #TODO This is slow. Possible fixes?
        cell_details_string += self.GetTopLevelParent().pianorollpanel.print_cell_sizes()
        win = RichTextFrame(self, -1, cell_details_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Cell_Sizes_Details")
        win.Show(True)


    # Test #TODO Figure out what to do to finish these midas_scripts quick tools.
    def OnToolSelection(self, event):
        print(event.Id)
        print("ass ass ass ass")
        dlg = Preferences.ToolsDialog(self, -1, "Midas Dynamic Tool")
        dlg.func_id = event.Id
        # Generate custom tool-based layout here.
        dlg._generate_layout(event.Id)
        dlg.ShowWindowModal()

    # TODO def OnToolClose() ??

    # Everytime a new function is added to one of the midas_scripts, it automatically is appended to it's appropriate
    # tools submenu.
    # #Menu Comprehensive Append Functions --In MIDAS_wx.py, see #Menu Comprehensive Bind Functions
    def _append_musicode_tools(self):
        mcode_ids = 1000
        self.musicode_list = [o for o in inspect.getmembers(musicode.Musicode) if inspect.isfunction(o[1])]
        for func in self.musicode_list:
            self.musicodetools.Append(mcode_ids, func[0])
            mcode_ids += 1

    def _append_midiart_tools(self):
        mcode_ids = 1100
        self.midiart_list = [o for o in inspect.getmembers(midiart) if inspect.isfunction(o[1])]
        for func in self.midiart_list:
            self.midiarttools.Append(mcode_ids, func[0])
            mcode_ids += 1

    def _append_midiart3D_tools(self):
        mcode_ids = 1200
        self.midiart3D_list = [o for o in inspect.getmembers(midiart3D) if inspect.isfunction(o[1])]
        for func in self.midiart3D_list:
            self.midiart3Dtools.Append(mcode_ids, func[0])
            mcode_ids += 1

    def _append_music21funcs_tools(self):
        mcode_ids = 1300
        self.music21funcs_list = [o for o in inspect.getmembers(music21funcs) if inspect.isfunction(o[1])]
        for func in self.music21funcs_list:
            self.music21funcstools.Append(mcode_ids, func[0])
            mcode_ids += 1

    #Menus that lead to submenus---so these will not be functions.
    # def OnMusicode(self, event):
    #     pass
    #
    #
    # def OnMidiart(self, event):
    #     pass
    #
    #
    # def On3iDiart(self, event):
    #     pass
    #
    #
    # def OnMusic21Funcs(self, event):
    #     pass

        # Submenu 7, 8, 9
        # def OnCurrentActorListToShell(self, event):
        #     pass
        #
        # def OnCurrentActorToShell(self, event):
        #     pass
        #
        # def OnCurrentZplaneToShell(self, event):
        #     pass

        # Submenu 7,8,9 Defined


    def OnAsMusic21StreamWithParts(self, event):
        pass


    def OnAsDictionaryOfPoints(self, event):
        pass


    def OnAsMusic21Stream(self, event):
        pass


    def OnAsNumpyPoints(self, event):
        pass


    ## Help Buttons Defined
    #---------------------------------------------

    def OnSearchHelp(self, event):
        dlg = self.helper
        dlg.ShowWindowModal()


    def OnAboutMidas(self, event):
        #TODO Better method? Better about?
        about_midas = music21funcs.about_midas()
        win = RichTextFrame(self, -1, about_midas, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="About Midas")
        win.Show(True)


    def OnLicensing(self, event):
        pass

    #This is a submenu button.
    # def OnDocumentation(self, event):
    #     pass


    def OnMidasHomepage(self, event):
        pass


    def OnTheMagicHammerHomepage(self, event):
        wx.LaunchDefaultBrowser(r"www.themagichammer.com", 0)


    def OnTutorials(self, event):
        pass


    def OnCommunity(self, event):
        pass


    def OnGoogleSearch(self, event):
        wx.LaunchDefaultBrowser(r"www.google.com", 0)
        pass


    def OnCheckForUpdates(self, event):
        pass


    def OnCredits(self, event):
        pass


    # Documentation Submenu
    def OnPython(self, event):
        wx.LaunchDefaultBrowser(r"https://docs.python.org/3/", 0)

    def OnMusic21(self, event):
        wx.LaunchDefaultBrowser(r"https://web.mit.edu/music21/", 0)


    def OnMayavi(self, event):
        wx.LaunchDefaultBrowser(r"https://docs.enthought.com/mayavi/mayavi/index.html#", 0)


    def OnNumpy(self, event):
        wx.LaunchDefaultBrowser(r"https://numpy.org/", 0)


    def OnSympy(self, event):
        wx.LaunchDefaultBrowser(r"https://www.sympy.org/en/index.html", 0)


    def OnOpen3D(self, event):
        wx.LaunchDefaultBrowser(r"http://www.open3d.org/", 0)


    def OnOpenCVPython(self, event):
        wx.LaunchDefaultBrowser(r"https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html", 0)
        wx.LaunchDefaultBrowser(r"https://docs.opencv.org/master/", 0)


    def OnVTK(self, event):
        #VTK by itself is a C++ library later ported to python.
        wx.LaunchDefaultBrowser(r"https://vtk.org/doc/nightly/html/index.html", 0)
        wx.LaunchDefaultBrowser(r"https://vtk.org/overview/", 0)

        pass


    def OnTVTK(self, event):
        wx.LaunchDefaultBrowser(r"https://docs.enthought.com/mayavi/tvtk/index.html", 0)
        pass



    def _OnPreferencesDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        #self.GetTopLevelParent().mayavi_view
        if btn == "OK":
            if dialog.input_span.GetLineText(0) == None:
                pass
            else:
                self.GetTopLevelParent().mayavi_view.grid3d_span = float(dialog.input_span.GetLineText(0))
            if dialog.input_bpm.GetLineText(0) == None:
                pass
            else:
                self.GetTopLevelParent().mayavi_view.bpm = float(dialog.input_bpm.GetLineText(0))
            if dialog.input_i_div.GetLineText(0) == None:
                pass
            else:
                self.GetTopLevelParent().mayavi_view.i_div = float(dialog.input_i_div.GetLineText(0))
            if dialog.popupCtrl.GetStringValue() == "FLStudioColors":
                self.GetTopLevelParent().mayavi_view.default_color_palette = midiart.FLStudioColors
                self.GetTopLevelParent().mayavi_view.default_mayavi_palette = \
                    midiart.convert_dict_colors(self.GetTopLevelParent().mayavi_view.default_color_palette)
            else:
                self.GetTopLevelParent().mayavi_view.default_color_palette = midiart.get_color_palettes()[dialog.popupCtrl.GetStringValue()]
                self.GetTopLevelParent().mayavi_view.default_mayavi_palette = \
                    midiart.convert_dict_colors(self.GetTopLevelParent().mayavi_view.default_color_palette)

    def _OnHelpDialogClosed(self, dialog, evt):
        val = evt.GetReturnCode()
        print("Val %d: " % val)
        try:
            btn = {wx.ID_OK: "OK",
                   wx.ID_CANCEL: "Cancel"}[val]
        except KeyError:
            btn = '<unknown>'
        if btn == "OK":
            pass

    def _OnPrefDialogCloser(self, evt):
        # One for Preferences, bound in MainWindow.
        dialog = evt.GetDialog()
        if type(dialog) is Preferences.PreferencesDialog:
            self._OnPreferencesDialogClosed(dialog, evt)

    def _OnHelpDialogCloser(self, dialog, evt):
        dialog = evt.GetDialog()
        if type(dialog) is HelpDialog:
            self._OnHelpDialogClosed(dialog, evt)






class RichTextFrame(wx.Frame):
    def __init__(self, parent, id, value, pos, size, style, validator, name):
        wx.Frame.__init__(self, parent, id, name, pos, size, style, name)
        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER)
        wx.CallAfter(self.rtc.SetFocus)
        self.rtc.WriteText(value)


class HelpDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        #Helps with help.
        #self.Midas = self.GetParent().GetTopLevelParent()

        #Static Text
        self.description = self.name_static = wx.StaticText(self, -1, "Type in a python module\class\object name. "
                                                        "Then choose a help method.",     style=wx.ALIGN_CENTER_HORIZONTAL)

        #Text Query
        self.inputtxt = wx.TextCtrl(self, -1, "", size=(250, -1), name="Help Query")
        self.helpbutton = wx.Button(self, -1, "Help()")
        self.membersbutton = wx.Button(self, -1, "Get Members")
        self.methodsbutton = wx.Button(self, -1, "All Methods")
        self.argsbutton = wx.Button(self, -1, "ArgSpec")

        #Special Help Buttons!
        self.Bind(wx.EVT_BUTTON, self.OnShowHelp, self.helpbutton)
        self.Bind(wx.EVT_BUTTON, self.OnShowAllMethods, self.methodsbutton)
        self.Bind(wx.EVT_BUTTON, self.OnShowMembers, self.membersbutton)
        self.Bind(wx.EVT_BUTTON, self.OnShowArgs, self.argsbutton)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.helpbutton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer1.Add(self.methodsbutton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer1.Add(self.membersbutton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizer1.Add(self.argsbutton, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.description, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(self.inputtxt, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(sizer1,  0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        self.SetSizerAndFit(sizerMain)


    def OnShowHelp(self, event):
        object = self.inputtxt.GetLineText(0)

        # Helps with introspecting the entire hierarchy.
        Midas = self.GetParent().GetTopLevelParent()

        help_string = pydoc.render_doc(eval(object), renderer=pydoc.plaintext)
        win = RichTextFrame(self, -1, help_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Pydoc's Help")
        win.Show(True)
    def OnShowAllMethods(self, event):
        object = self.inputtxt.GetLineText(0)

        # Helps with introspecting the entire hierarchy.
        Midas = self.GetParent().GetTopLevelParent()

        methods_string = ""
        for j in pydoc.allmethods(eval(object)).keys():
            string = str(j) + '   ' + str(pydoc.allmethods(eval(object))[j]) + "\n"
            methods_string += string

        win = RichTextFrame(self, -1, methods_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name="Pydoc's All Methods")
        win.Show(True)
    def OnShowMembers(self, event):
        object = self.inputtxt.GetLineText(0)

        # Helps with introspecting the entire hierarchy.
        Midas = self.GetParent().GetTopLevelParent()

        members_string = " "
        for j in inspect.getmembers(eval(object)):
            string = str(j[0]) + "   ----->    "  + pprint.pformat(str(j[1]), width = 100) + "\n"
            members_string += string
        sexierstring = pprint.pformat(members_string, width = 150)

        win = RichTextFrame(self, -1, sexierstring, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name='''Inspect's "Get Members"''')
        win.Show(True)
    def OnShowArgs(self, event):
        object = self.inputtxt.GetLineText(0)

        # Helps with introspecting the entire hierarchy.
        Midas = self.GetParent().GetTopLevelParent()

        args_string = str(inspect.getfullargspec(eval(object)))

        win = RichTextFrame(self, -1, args_string, wx.DefaultPosition,
                            size=(700, 500),
                            style=wx.DEFAULT_FRAME_STYLE, validator=wx.DefaultValidator, name='''Inspect's "GetFullArgSpec"''')
        win.Show(True)


# class FileBrowseButton(wx.Panel):
#     def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL,
#              labelText="File Entry:", buttonText="Browse", toolTip="Type filename or click browse to choose file",
#              dialogTitle="Choose a file", startDirectory=".", initialValue="", fileMask="*.*", fileMode=wx.FD_OPEN,
#              changeCallback=lambda x: x, labelWidth=0, name='fileBrowseButton'):



    ## 101New Session
    ## 102Open Session
    ## 103Save Session
    ## 104Save Session As
    ## 105Import...
    # 106Import Directory
    # 107Export...
    # 108Export As Directory
    # 109Export Musicode
    # 110Export Movie
    # 111Preferences
    # 112Intermediary Path
    # 113Exit

    # #Edit
    # 201Undo
    # 202Redo
    # 203Cut
    # 204Copy
    # 205Paste
    # 206History

    # #Show
    # 301    Show in DAW
    # 302    Show in Musescore
    # 303    Show in Word Processor
    # 304    Show in PicPick\Paint
    # 305    Show in Meshlab
    # 306    Show in Blender
    # 307    Scene3d_1
    # 308    project2

    # #Tools
    #401Musicode
    # 402Midiart
    # 4033iDiart
    # 404Music21Funcs
    # 405Current ActorList to Shell
    # 406Current Actor to Shell
    # 407Current Z-Plane to Shell

    #Submenus
    # 700AsMusic21StreamWithParts
    # 701AsDictionaryOfPoints

    #Submenu
    # 800AsMusic21Stream
    # 801AsNumpyPoints
    # 900AsMusic21Stream
    # 901AsNumpyPoints

    # #Help
    # 501About Midas
    # 502Licensing
    # 503Documentation

    # 601Music21
    # 602Mayavi
    # 603Numpy
    # 604Sympy
    # 605Open3D
    # 606Open-CVPython
    # 607VTK
    # 608TVTK

    # 504Midas Homepage
    # 505The Magic Hammer Homepage
    # 506Tutorials
    # 507Community
    # 508Google Search
    # 509Check for Updates...
    # 510Credits.

# item.SetBitmap(images.Smiles.GetBitmap())
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


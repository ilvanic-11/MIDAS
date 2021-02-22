import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import numpy as np
import math
#from midas_scripts import musicode, music21funcs
from midas_scripts import midiart3D
from gui import PianoRoll
from gui import ZPlanesControlPanel, ActorsControlPanel
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray
from collections import OrderedDict
#import numpy_indexed as npi
import time
import logging

"""
PianoRollPanel
Toolbar
wxNoteBook
|-Page: PianoRoll0
|-Page: PianoRoll1
|-Page: PianoRoll2
|- ...


"""


class PianoRollPanel(wx.Panel):
    log = logging.getLogger("PianoRollPanel")

    def __init__(self, parent, log):
        # HasTraits.__init__(self)
        wx.Panel.__init__(self, parent, -1)

        self.log = log
        self.log.info("PianoRollPanel.__init__()")
        self.tb = self.SetupToolbar()

        #mayavi_view reference
        self.m_v = self.GetTopLevelParent().mayavi_view

        self.currentZplane = 90



        self.draw_mode = 1
        self.select_mode = 0

        self.z_pushnpull = 1  #For the zplane\velocity push n pull scrolling

        self.last_highlight = []

        self.mode = self.draw_mode  ### "1" for Draw, 0 for Select

        #self.mayavi_view = self.GetTopLevelParent().mayavi_view

        self.pianorollSplit = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)
        self.ctrlpanelSplit = wx.SplitterWindow(self.pianorollSplit, wx.ID_ANY, style=wx.SP_3DSASH | wx.SP_BORDER)

        self.zplanesctrlpanel = ZPlanesControlPanel.ZPlanesControlPanel(self.ctrlpanelSplit, self.log)
        self.actorsctrlpanel = ActorsControlPanel.ActorsControlPanel(self.ctrlpanelSplit, self.log)

        self.pianoroll = PianoRoll.PianoRoll(self.pianorollSplit,
                                             self.currentZplane,
                                             -1,
                                             wx.DefaultPosition,
                                             wx.DefaultSize,
                                             0,
                                             "Piano Roll",
                                             self.log
                                             )

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.tb, 1, wx.EXPAND)
        mainSizer.Add(self.pianorollSplit, 1, wx.EXPAND)

        self.pianorollSplit.SplitVertically(self.ctrlpanelSplit, self.pianoroll)
        self.ctrlpanelSplit.SplitVertically(self.actorsctrlpanel, self.zplanesctrlpanel)
        self.ctrlpanelSplit.SetSashGravity(0.5)

        self.pianorollSplit.SetSashPosition(240)
        self.ctrlpanelSplit.SetSashPosition(120)

        self.pianorollSplit.SetMinimumPaneSize(240)
        # self.ctrlpanelSplit.SetMinimumPaneSize(10)

        # For Draw feature(s).
        self.pianoroll.GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        self.pianoroll.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        #self.pianoroll.Bind(wx.EVT_MOUSEWHEEL, self.Scroll_ZPlanesVelocities)

        # For Highlight Selection feature.

        self.pianoroll.GetGridWindow().Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)
        #TODO For Middle-Down drag-n-move.
        #self.pianoroll.GetGridWindow().Bind(wx.EVT_MIDDLE_DOWN, self.onMouseLeftDown)

        self.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onLeftSelectDown1)
        self.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onLeftSelectDown2)
        #PLUS THE ONE IN PIANOROLL.py


        self.pianoroll.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDoubleClick_Out)
        self.pianoroll.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.onDragSelection)

        self.Layout()
        #self.AccelerateHomeHotkey()
        self.SetSizerAndFit(mainSizer)

    #TODO Deprecated?
    def DeletePianoRoll(self, index):
        self.log.info("DeletePianoRoll")
        self.pianorolls.pop(index - 1)
        # self.pianorollNB.DeletePage(index-1)

    def SetupToolbar(self):

        btn_size = (20, 20)
        self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
        self.toolbar.SetToolBitmapSize(btn_size)

        bmp_drawmode = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, btn_size)
        bmp_selectmode = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, btn_size)

        id_drawmode = 10
        self.toolbar.AddRadioTool(id_drawmode, "Select", bmp_drawmode, wx.NullBitmap, "Draw Mode",
                                  "Change to Select Mode", None)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_drawmode)

        id_selectmode = 20
        self.toolbar.AddRadioTool(id_selectmode, "select", bmp_selectmode, wx.NullBitmap, "Select Mode",
                                  "Change to Draw Mode", None)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_selectmode)

        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()

        cbID = 101
        lblID = 1011
        lbl = wx.StaticText(self.toolbar, lblID, label="Cell Draw Size: ")

        self.toolbar.AddControl(lbl, "")
        self.cbDrawCellSize = wx.ComboBox(self.toolbar, cbID, "1", wx.DefaultPosition, wx.DefaultSize,
                                          choices=["1", "2", "4", "8"],
                                          style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.toolbar.AddControl(self.cbDrawCellSize)
        self.Bind(wx.EVT_COMBOBOX, self.OnDrawCellSizeChanged, id=cbID)

        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()

        cbID1 = 102
        lblID1 = 1021
        lbl1 = wx.StaticText(self.toolbar, lblID1, label="Cells Per Qrtr Note: ")

        self.toolbar.AddControl(lbl1, "")
        self.cbCellsPerQrtrNote = wx.ComboBox(self.toolbar, cbID1, "(1, 'Qrtr', 1)", wx.DefaultPosition, wx.DefaultSize,
                                              choices=["(1, 'Qrtr', 1)", "(2, '8th', .5)", "(4, '16th', .25)", "(8, '32nd', .125)", "(16, '64th', .0625)", "(32, '128th', .03125)"],
                                              style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.toolbar.AddControl(self.cbCellsPerQrtrNote)
        self.Bind(wx.EVT_COMBOBOX, self.OnCellsPerQrtrNoteChanged, id=cbID1)

        self.toolbar.AddSeparator()
        self.toolbar.AddSeparator()

        brushlbl = wx.StaticText(self.toolbar, lblID, label="Brush: ")

        self.toolbar.AddControl(brushlbl, "")

        id_Brush = 30
        #Unused

        bmp_Brush = wx.ArtProvider.GetBitmap(wx.ART_MINUS, wx.ART_TOOLBAR, btn_size)
        btn_Brush = wx.Button(self, -1, "Brush")
        # # sizer.Add(btnAddLayer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.toolbar.AddTool(id_Brush, "", bmp_Brush, shortHelp="Brush", kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_Brush)

        id_DeleteLayer = 40
        #Unused


        # bmp_RedrawMayaviView = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, btn_size)
        # # btn_RedrawMayaviView = wx.Button(self, -1, "MIDI Art")
        # # sizer.Delete(btnRedrawMayaviView, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.toolbar.AddTool(id_RedrawMayaviView, "", bmp_RedrawMayaviView, shortHelp="Delete Layer", kind=wx.ITEM_NORMAL)
        # self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_RedrawMayaviView)

        id_DeleteAllLayers = 50
        #Unused


        # bmp_DeleteAllLayers = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, btn_size)
        # self.toolbar.AddTool(id_DeleteAllLayers, "", bmp_DeleteAllLayers, shortHelp="Delete All Layers",
        #                      kind=wx.ITEM_NORMAL)
        # self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_DeleteAllLayers)

        self.toolbar.Realize()
        return self.toolbar


    def OnCellsPerQrtrNoteChanged(self, event):
        print("OnCellsPerQrtrNoteChanged(): new size = %s" % self.cbCellsPerQrtrNote.GetValue())

        eval_value = eval(self.cbCellsPerQrtrNote.GetValue())
        newvalue = eval_value[0]

        self.m_v.cpqn = newvalue
        print("Changing CPQN, updating grid reticle.")

        #self.mayavi_view.cpqn = newvalue
        #print("Changing CPQN, updating grid reticle.")


        # need to redraw current piano roll and update stream
        self.pianoroll.ChangeCellsPerQrtrNote(newvalue)

        # self.pianoroll.ForceRefresh()

        # I don't fully understand, but this call needs to happen at the end of the function. (On-que, reticle update bugfix.)
        self.m_v.cpqn_changed_flag = not self.m_v.cpqn_changed_flag


    def OnDrawCellSizeChanged(self, event):
        print("OnDrawCellSizeChanged(): new size = %s" % self.cbDrawCellSize.GetValue())
        self.pianoroll.draw_cell_size = int(self.cbDrawCellSize.GetValue())


    def OnToolBarClick(self, event):
        """
        Event handler for when user clicks a button on the toolbar.
        Determines which button was called and calls sub-handler functions
        :return:
        """
        print("OnToolBarClick():")
        if event.GetId() == 10:
            self.OnDrawMode(event)
        elif event.GetId() == 20:
            self.OnSelectMode(event)
        elif event.GetId() == 30:
            # self.InsertNewPianoRoll(len(self.pianorolls))
            pass
        elif event.GetId() == 40:
            #self.DeletePianoRoll(len(self.pianorolls))
            pass
        elif event.GetId() == 50:
            # self.DeleteAllPianoRolls()
            pass


    def OnDrawMode(self, event):
        self.log.info("OnSelectMode():")
        self.mode = self.draw_mode
        self.m_v.CurrentActor().array3Dchangedflag = self.m_v.CurrentActor().array3Dchangedflag


    def OnSelectMode(self, event):
        self.log.info("OnDrawMode():")
        self.mode = self.select_mode


    def print_cell_sizes(self):  # TODO Redundant? Consider deleting this button.
        s = ""
        with open("test.txt", 'w') as f:
            for row in range(0, self.pianoroll.GetNumberRows()):
                for col in range(0, self.pianoroll.GetNumberCols()):
                    s += self.pianoroll.print_cell_info(row, col)
                s += "\n"
                print(type(s))
            f.write(s)

            return s


    def ClearZPlane(self, z):
        # for x in range(0, self.pianoroll._table.GetNumberCols()):
        #     for y in range(0, self.pianoroll._table.GetNumberRows()):
        # self.pianoroll._table.SetValue(y, x, "0")
        # self.GetTopLevelParent().mayavi_view.CurrentActor()._array3D[x, 127 - y, z] = 0



        if self.m_v.CurrentActor() == None:

            pass
            # current_actor = self.pianoroll.cur_array3d
        else:
            current_actor = self.m_v.CurrentActor()
            on_points = np.argwhere(current_actor._array3D[:, :, z] >= 1.0)
            #print("On_Points", on_points)
            for i in on_points:
                #Grid set.
                self.pianoroll._table.SetValue(127 - i[1], i[0],
                                               "0")  # TODO Track mode stuff! What can the 'value' parameter be?
            #array3D set.
            current_actor._array3D[:, :, z] = current_actor._array3D[:, :,
                                              z] * 0  # TODO Different way to write this? Multiply whole array3d by 0?
            self.pianoroll.ForceRefresh()

            #self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag += 1

        self.pianoroll.ResetGridCellSizes()
        #self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag = not self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag

        #Manual override, trait update not working....
        self.m_v.actors[self.m_v.cur_ActorIndex].actor_array3D_changed()

        self.pianoroll.ForceRefresh()


    def Scroll_ZPlanesVelocities(self, event):
        #TODO Doc strings.

        #print("Push Scrolling HERE.")
        try:
            self.last_push = self.last_push
        except AttributeError as i:
            print(i, "You don't have a last push yet.")
            self.last_push = self.m_v.CurrentActor().cur_z  #Because in order to highlight-select some notes, the cur_z will always be current.

        if not self.pianoroll.HasFocus():
            event.Skip()
            pass
        else:
            #print("Push Scrolling HERE2.")
            if not self.selected_notes:
                return
            else:
                #notes = np.argwhere(self.m_v.CurrentActor()._array3D == 3.0)
                if event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL or event.GetWheelDelta() < 120:
                    event.Skip()
                    return
                scroll = self.z_pushnpull  #equals 1 on init.

                state = wx.GetMouseState()

                if state.ControlDown() and state.AltDown() and state.ShiftDown():   #CHANGED FROM ControlDown to avoid conflicting with other scrolling function(s).
                    if event.GetWheelRotation() >= 120:   #Scroll foward makes smaller.

                        self.Selection_Send(self.selected_notes, scroll * -1, event)
                        #self.z_pushnpull += 1
                        #self.cur_push -= 1
                    elif event.GetWheelRotation() <= -120:   #Scroll forward

                        self.Selection_Send(self.selected_notes, scroll, event)
                        #self.z_pushnpull += 1
                        #self.cur_push += 1
                else:
                    event.Skip()
            #print("Push Scrolling HERE3.")


    def Selection_Send(self, selected_notes, scroll_value, event=None, carry_to_z=False, carry_to_actor=False, array=True, transform_xy=False):
        """
        This function is intended to take highlighted grid 'selections' of notes and push and/or pull them between our actor/zplanes based on a user-defined value.\
        If both scroll_to_z and scroll_to_actor are False, this function functions incrementally. (+1 or -1 on the current actor). If one or both is true, the 'self.selected_notes' will
        be 'sent' directly TO the scroll_value, instead of scrolling BY that value.

        :param scroll_value:    The z_plane scroll pushnpull value.
        :param event:           Passed in event, for more writing options.
        :param carry_to_z:      Bool determining scroll method; scroll by increment or scroll to z value itself.
        :param carry_to_actor:  Bool determing scrool method; scroll to self.GTLP.actor_scrolled actor, else remain on current actor.
        :param array:           Set this to true if the array input is already a numpy array of np.array(selected_notes)
        :return: None
        """

        #If we don't have selected_notes, break here.
        assert not not self.selected_notes, "You do not have selected_notes yet."

        if carry_to_z or carry_to_actor:
            try:
                #The last scroll value.
                self.last_push = self.last_push
                self.last_actor = self.last_actor
            except AttributeError as i:
                print(i, "You don't have a 'last push' and\or a 'last actor' yet.")
                #self.last_push = self.GetTopLevelParent().zplane_scrolled #Because in order to highlight-select some notes, the cur_z will always be current.
                self.last_push = self.m_v.CurrentActor().cur_z #cur_z, intially?
                self.last_actor = self.m_v.cur_ActorIndex
        else:
            pass

        #Carry method.
        #(Carry_to_z or carry_to_actor allows carrying for shift GrabNSend to scrolled_actor alt GrabnSend to scrolled_zplane
        # AND carry==False will allow for Scroll_Zplanes_Velocities() and GrabnSend() to pyshell)
        if carry_to_z is True or carry_to_actor is True:
            carry = True
        else:
            carry = False

        #Make selected_notes ((Y,X) cells) into a np.array.
        if array is True:
            assert isinstance(self.selection_array, np.ndarray), "Your input is not a numpy array. Fix."
            self.selection_array = selected_notes
        else:
            self.ArrayFromSelection(selection=selected_notes, scroll_value=scroll_value, carry=carry)

        #CORE-------------------------------------------------------------------------
        #array3D method
        #####Transfrom on current plane method.
        if transform_xy:
            for i in self.selection_array:
                print("INDEX_FIND", [i[0], i[1], i[2]])
                self.m_v.CurrentActor()._array3D[
                    i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                # TODO HERE>

                # This condition block accounts for the first miss.
            for j in self.ArrayFromSelection(self.selected_notes, self.m_v.CurrentActor().cur_z):
                self.m_v.CurrentActor()._array3D[j[0], j[1], self.m_v.CurrentActor().cur_z] = 0.

            self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
            #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag

            # self.m_v.actors[self.last_actor].array3Dchangedflag = not self.m_v.actors[
            #     self.last_actor].array3Dchangedflag
            #
            # self.m_v.actors[self.GetTopLevelParent().actor_scrolled].array3Dchangedflag = not self.m_v.actors[
            #     self.GetTopLevelParent().actor_scrolled].array3Dchangedflag

            #3self.last_actor = self.m_v.cur_ActorIndex

            self.last_push = self.GetTopLevelParent().zplane_scrolled
            self.pianoroll.ForceRefresh()


        else:
            #print("SELECTION_ARRAY", self.selection_array)
            for i in self.selection_array:

                if carry_to_actor is False:
                    if carry_to_z is True:
                        print("INDEX_FIND", [i[0], i[1], i[2]])
                        ##Note: zplane_scrolled here, NOT last_actor.....

                        # We are pushing our 'selection' FROM the cur_z TO somewhere else.
                        if self.GetTopLevelParent().zplane_scrolled != self.m_v.CurrentActor().cur_z and self.last_push == self.m_v.CurrentActor().cur_z:  ##Note: zplane_scrolled here, NOT last_actor.....
                            self.m_v.CurrentActor()._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[
                                2]] = 1.0  # Scrolled-to plane notes become activated.

                # if send_to_actor is False:
                #     if send_to_z is True:
                #         if self.last_push == self.m_v.CurrentActor().cur_z:
                #             #print("INDEX_FIND", [i[0], i[1], i[2]])
                #             self.m_v.CurrentActor()._array3D[
                #                 i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.

                            # TODO HERE>

                            # This condition block accounts for a 'first miss'. In our logic, the first case is exceptional.
                            if i[2] == self.last_push:
                                self.m_v.CurrentActor()._array3D[i[0], i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.CurrentActor()._array3D[i[0], i[1], self.last_push] = 0.

                            print("A1")

                        # We are pushing our 'selection' FROM somewhere else TO our CurrentActor's cur_z.
                        elif self.GetTopLevelParent().zplane_scrolled == self.m_v.CurrentActor().cur_z and self.last_push != self.m_v.CurrentActor().cur_z:
                            self.m_v.CurrentActor()._array3D[
                                i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                        # else:
                        #     #print("INDEX_FIND", [i[0], i[1], i[2]])
                        #     self.m_v.CurrentActor()._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                        #     #TODO HERE>


                            # This condition block accounts for the first miss.
                            if i[2] == self.last_push:
                                self.m_v.CurrentActor()._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[
                                    1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.CurrentActor()._array3D[
                                    int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.last_push] = 0.
                            print("A2")

                        # We are pushing our 'selection' FROM somewhere else TO another somewhere else that isn't cur_z.
                        elif self.GetTopLevelParent().zplane_scrolled != self.m_v.CurrentActor().cur_z and self.last_push != self.m_v.CurrentActor().cur_z:
                            self.m_v.CurrentActor()._array3D[
                                int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            # This condition block accounts for a 'first miss'. In our logic, the first case is exceptional.
                            if i[2] == self.last_push:
                                self.m_v.CurrentActor()._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.CurrentActor()._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.last_push] = 0.
                            print("A3")

                        # Accounting for a possible user mis-click, we are pushing our 'selection' FROM our cur_z right back TO our cur_z. #TODO Use Pass?
                        elif self.GetTopLevelParent().zplane_scrolled == self.m_v.CurrentActor().cur_z and self.last_push == self.m_v.CurrentActor().cur_z:
                            #Turn on..
                            self.m_v.CurrentActor()._array3D[
                                i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            #But don't turn off.
                            # This condition block accounts for the first miss.
                            # if i[2] == self.last_push:
                            #     self.m_v.CurrentActor()._array3D[i[0], i[1], self.m_v.CurrentActor().cur_z] = 0.
                            # elif i[2] != self.last_push:
                            #     self.m_v.CurrentActor()._array3D[i[0], i[1], self.last_push] = 0.
                            print("A4")

                    elif carry_to_z is False:
                        #If carry-to-actor AND carry-to-z are both false, are we really carrying anything?! Pass here?
                        self.m_v.CurrentActor()._array3D[i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.

                        self.m_v.CurrentActor()._array3D[i[0], i[1], i[2] - scroll_value] = 0.   #Abandoned plane notes are zero'd.


                elif carry_to_actor is True: #If carry_to_actor is True....    #Scroll-to_actor method.

                    if carry_to_z is True:

                        print("INDEX_FIND_2", [i[0], i[1], i[2]])
                        ##Note: zplane_scrolled here, NOT last_actor.....

                        # We are pushing our 'selection' FROM the cur_z TO somewhere else.
                        if self.GetTopLevelParent().zplane_scrolled != self.m_v.CurrentActor().cur_z and self.last_push == self.m_v.CurrentActor().cur_z:  ##Note: zplane_scrolled here, NOT last_actor.....
                            self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[
                                2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            # This condition block accounts for a 'first miss'. In our logic, the first case is exceptional.
                            if i[2] == self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[i[0], i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[i[0], i[1], self.last_push] = 0.
                            print("S1.")

                        # We are pushing our 'selection' FROM somewhere else TO our CurrentActor's cur_z.
                        elif self.GetTopLevelParent().zplane_scrolled == self.m_v.CurrentActor().cur_z and self.last_push != self.m_v.CurrentActor().cur_z:
                            self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            # This condition block accounts for the first miss.
                            if i[2] == self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.last_push] = 0.
                            print("S2")

                        # We are pushing our 'selection' FROM somewhere else TO another somewhere else that isn't cur_z.
                        elif self.GetTopLevelParent().zplane_scrolled != self.m_v.CurrentActor().cur_z and self.last_push != self.m_v.CurrentActor().cur_z:
                            self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[
                                    2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            # This condition block accounts for a 'first miss'. In our logic, the first case is exceptional.
                            if i[2] == self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], self.last_push] = 0.
                            print("S3")

                        # Accounting for a possible user mis-click, we are pushing our 'selection' FROM our cur_z right back TO our cur_z. #TODO Use Pass?
                        elif self.GetTopLevelParent().zplane_scrolled == self.m_v.CurrentActor().cur_z and self.last_push == self.m_v.CurrentActor().cur_z:
                            self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[int(i[0] / self.pianoroll._cells_per_qrtrnote), i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                            # TODO HERE>

                            # This condition block accounts for the first miss.
                            if i[2] == self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[i[0], i[1], self.m_v.CurrentActor().cur_z] = 0.
                            elif i[2] != self.last_push:
                                self.m_v.actors[self.last_actor]._array3D[i[0], i[1], self.last_push] = 0.
                            print("S4")

                        ## index = npi.indices(self.m_v.CurrentActor()._points, ),
                        #self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[i[0], i[1], i[2]] = 1.0  # Scrolled-to plane notes become activated.
                        #self.m_v.actors[self.last_actor]._array3D[i[0], i[1], self.last_push] = 0.   # Abandoned plane notes are zero'd.

                    elif carry_to_z is False:
                        self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._array3D[i[0], i[1], self.m_v.CurrentActor().cur_z] = 1.0  # Scrolled-to plane notes become activated.
                        self.m_v.actors[self.last_actor]._array3D[
                            i[0], i[1], self.last_push] = 0.  # Abandoned plane notes are zero'd.
                        #
                        # self.m_v.CurrentActor()._points[]


            ####Flags and refreshes -----------------------------------------------------------
            #TODO Clean this up better.   --- 11/25/20
            #Direct-to-points method.
            if carry_to_actor and carry_to_z: #Send-to-z method or Send-to-actor method.
                # self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag = not self.m_v.actors[
                #             self.m_v.cur_ActorIndex].array3Dchangedflag

                #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
                #self.m_v.CurrentActor().actor_array3D_changed()
                self.m_v.actors[self.last_actor].array3Dchangedflag = not self.m_v.actors[
                    self.last_actor].array3Dchangedflag

                print("Right here.")

                self.m_v.actors[self.GetTopLevelParent().actor_scrolled].array3Dchangedflag = not self.m_v.actors[
                     self.GetTopLevelParent().actor_scrolled].array3Dchangedflag

                #Method here to get ON points as odict
                self.m_v.actors[self.GetTopLevelParent().actor_scrolled].get_ON_points_as_odict()
                #Method here to change cur_plane for compensation
                self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._cur_plane[:, 0] = self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._cur_plane[:, 0] * self.pianoroll._cells_per_qrtrnote
                self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._points = midiart3D.restore_coords_array_from_ordered_dict(self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._all_points)

                self.m_v.sources[self.GetTopLevelParent().actor_scrolled].mlab_source.points = self.m_v.actors[self.GetTopLevelParent().actor_scrolled]._points
                #TODO Double check order here?
                self.last_actor = self.m_v.cur_ActorIndex
                self.actorsctrlpanel.actorsListBox.Activate_Actor(self.GetTopLevelParent().actor_scrolled)  #Then, got to new actor.




                self.last_push = self.GetTopLevelParent().zplane_scrolled
                self.pianoroll.ForceRefresh()


            elif not carry_to_actor and carry_to_z:
                # self.m_v.actors[self.last_actor].array3Dchangedflag = not self.m_v.actors[
                #     self.last_actor].array3Dchangedflag

                # self.m_v.actors[self.GetTopLevelParent().actor_scrolled].array3Dchangedflag = not self.m_v.actors[
                #     self.GetTopLevelParent().actor_scrolled].array3Dchangedflag

                #TODO MAKE SURE ALL CARRY METHODS ARE CONSISTENT WITH THEIR RESPECTIVE array3D updating!!

                self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag

                self.last_actor = self.m_v.cur_ActorIndex

                self.last_push = self.GetTopLevelParent().zplane_scrolled
                self.pianoroll.ForceRefresh()


            # Carry-to-z method or Carry-to-actor method.
            elif carry_to_actor and not carry_to_z:
                self.m_v.actors[self.last_actor].array3Dchangedflag = not self.m_v.actors[self.last_actor].array3Dchangedflag

                self.m_v.actors[self.GetTopLevelParent().actor_scrolled].array3Dchangedflag = not self.m_v.actors[
                            self.GetTopLevelParent().actor_scrolled].array3Dchangedflag

                #TODO Double check order here?
                self.last_actor = self.m_v.cur_ActorIndex  # Establish as self.last_actor.
                self.actorsctrlpanel.actorsListBox.Activate_Actor(self.GetTopLevelParent().actor_scrolled)  #Then, got to new actor.



                self.last_push = self.GetTopLevelParent().zplane_scrolled
                self.pianoroll.ForceRefresh()
            #TODO Correct actor update after selected_points move.

            #Incremental scroll method of pushing.
            else:
                if event.GetWheelRotation() >= 120:
                    self.last_push -= 1
                elif event.GetWheelRotation() <= -120:
                    self.last_push += 1
                self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag = not self.m_v.actors[
                            self.m_v.cur_ActorIndex].array3Dchangedflag
                self.pianoroll.ForceRefresh()



    # def Selection_Transform(self, selection):
    #     # CORE-------------------------------------------------------------------------
    #     # array3D method
    #     print("SELECTION_ARRAY", self.selection_array)


    def ArrayFromSelection(self, selection, scroll_value, carry=False):
        #TODO Doc strings.

        # Establish selected_notes as a numpy array.
        selected_array = np.array(selection)

        # Because our selected_notes are (Y, X), we flip them with numpy.flip(sn, axis=1)
        selected_array = np.flip(selection,
                                 1)  # TODO Got an error with this line. Reproduce?   #numpy.AxisError: axis 1 is out of bounds for array of dimension 1 (Because we didn't have a selection?)

        # 127-y compensation, for iteration reasons.
        selected_array[:, 1] = 127 - selected_array[:, 1]

        # Next, we create an array full of our cur_z value, and transform that by our pushnpull value or transform
        # to our carr 'scroll_value'
        # ones = np.ones((len(selected_notes), 1), dtype=np.float32)
        # TODO Condition here?

        if carry is True: #Carry to
            full_array = np.full((len(selected_array), 1), scroll_value, dtype=np.float32)
            push_pull = full_array
        else:   #Push by
            full_array = np.full((len(selected_array), 1), self.last_push, dtype=np.float32)
            push_pull = full_array + scroll_value

        # Now, we hstack our selected_array and 'our_push' and create a standard ([[x,y,z]]) np.coords_array.
        self.selection_array = np.hstack(
            (selected_array, push_pull))  # When stacking an int array with a float array, all values become floats.
        self.selection_array = np.asarray(self.selection_array,
                                          dtype=np.int8)  # So, we change back to dtype=np.int8 here.
        #print("NEW_PUSH_ARRAY", self.selection_array)


        #TODO Figure out why this doesnt work with our points. 11/24/20
         # For the direct_to_points method, we acquire our indices for our points based on their value using npi.
        # new_array2 = np.hstack((selected_array, push_pull))
        # new_array2 = np.asarray(new_array2, dtype=np.float32)
        # print("NEW_PUSH_ARRAY2", new_array2)
        ### selection_indices = npi.indices(self.m_v.CurrentActor()._points, [i for i in new_array2], axis=0, missing='mask')
        # print("SELECTION POINT_INDICES", selection_indices)
        # index = npi.indices(self.m_v.CurrentActor()._points, ),

        return self.selection_array




    ####FOR DRAW-SELECTION FEATURE
    ###----------------------------------------------------------------------
    #################------------------------------------------------------------------------------------------
    def OnMotion(self, evt):
        # self.log.debug("OnMotion: Drawing=%d " % self.pianoroll.drawing)
        cpqn = self.pianoroll._cells_per_qrtrnote
        z = self.currentZplane
        if self.mode == self.draw_mode:  ##If mode is "Draw Mode".....
            if evt.Dragging() and evt.LeftIsDown():
                x, y = self.pianoroll.CalcUnscrolledPosition(evt.GetPosition())
                row = self.pianoroll.YToRow(y)
                col = self.pianoroll.XToCol(x)
                (span, sx, sy) = self.pianoroll.GetCellSize(row, col)
                # print(f"row={row},col={col}" + self.pianorolls[self.currentpianoroll].print_cell_info(row,col))

                if self.pianoroll.drawing == 0:
                    if (self.pianoroll.GetCellValue(row, col) == "1" or span == wx.grid.Grid.CellSpan_Inside):
                        self.pianoroll.EraseCell(row, col)

                        #self.mayavi_view.CurrentActor()._array3D[int(col), int(127-row), int(z)] = 0    #*cpqn  /cpqn...


                elif self.pianoroll.drawing == 1:
                    if (self.pianoroll.GetCellValue(row, col) == "0" and span != wx.grid.Grid.CellSpan_Inside):

                        cell = self.pianoroll.DrawCell("1", row, col, 1, self.pianoroll.draw_cell_size)

                        #self.mayavi_view.CurrentActor()._array3D[int(col/cpqn), int(127-row), int(z)] = 1


        elif self.mode == self.select_mode:  ##if Select Mode...
            pass

        else:
            pass
            # self.mayavi_view.CurrentActor()._array3D[int(col / cpqn), int(127 - row), int(z)] = 1
            # print("x=%d, y=%d, row=%d, col=%d" % (x,y,row,col))
        evt.Skip()


    ###FOR HIGHLIGHT SELECTION FEATURE
    ###----------------------------------------------------------------------
    def onMouseLeftDown(self, event):

        curmousecoords = event.GetPosition()  ##In logical pixel coordinates.
        curgridcoords = self.pianoroll.XYToCell(curmousecoords)

        if not event.ShiftDown() and self.mode == self.select_mode:
            # Differentiates between 'first' selection, and 'additional' selections using shift.

            try:
                if len(self.selected_cells) != 0:
                    self.first_selection = False  #It it is NOT the first selection....
                    self.selected_cells = []      # Make our main list..
                    self.pianoroll.GoToCell(curgridcoords)  # THIS call fires an event, the handler for which we go to pronto.
                    #print("onMouseLeftDown mouse position", curgridcoords)
                    # event.Skip()
                    # print("Skipping..")
                else:
                    self.first_selection = True
                    # event.Skip()
            except AttributeError as i:
                # print(i)
                pass

        if event.ShiftDown() and self.mode == self.select_mode:

            # SELECTED_CELLS is the start of what we want for functions involving CUT\COPY\PASTEing of selections of cells in the grid.
            try:
                if not self.selected_cells:
                    self.selected_cells = []
            except AttributeError:
                pass
            #self.pianoroll.GoToCell(curgridcoords)
            # event.Skip()
            # pass
            # No new 'selected_cells' here.
            # self.selecting_cells = []
        else:
            pass
        event.Skip()




    def onLeftSelectDown1(self, event):
        """
        Get the selection of a single cell by clicking or
        moving the selection with the arrow keys
        This is an OnCellSelection event handler. It processes the selection of cell from the mouse left click, as well as from arrow keys.
        """
        if self.mode == self.select_mode:
            #print("You selected Row %s, Col %s" % (event.GetRow(), event.GetCol()))
            self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())

            self.first_selection = False
            self.selected_cells = []




            self.anti_select2()
            event.Skip()
        elif self.mode == self.draw_mode:
            pass
            #print("Drawmode HERE.")
            #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
        #time.sleep(20)


    def clear_out_highlight(self, event, manual_selection=None,  manual=False):
        if not manual:
           # print("Attempting Clear Out....")

            try:
                if not self.first_selection:  # If it's not the first selection batch....
                    if self.previously_selected_cells:
                        #print("You have PSCs.", self.previously_selected_cells)
                        for i in self.previously_selected_cells:
                            # Then, clear last drag event box.
                            if self.pianoroll.GetCellValue(i[0], i[1]) == '2':  # Blue highlight to...
                                self.pianoroll.SetCellValue(i[0], i[1], '0')  # Back to white.
                            elif self.pianoroll.GetCellValue(i[0], i[1]) == '3':  # Green highlighted notes...
                                self.pianoroll.SetCellValue(i[0], i[1], '1')  # Back to black.
                            else:
                                pass
                        print("Cleared out here.")
                        self.selected_cells.clear()  # We clear our selection, in order to start a new one.
                        self.selected_notes.clear()  # We clear our NOTE selection as well, starting over on a new click-highlight.
                        self.previously_selected_cells.clear()

            except AttributeError:
                print("You do not yet have previously_selected_cells.")
                pass
        else:
            for i in manual_selection:
                # Then, clear last drag event box.
                if self.pianoroll.GetCellValue(i[0], i[1]) == '2':  # Blue highlight to...
                    self.pianoroll.SetCellValue(i[0], i[1], '0')  # Back to white.
                elif self.pianoroll.GetCellValue(i[0], i[1]) == '3':  # Green highlighted notes...
                    self.pianoroll.SetCellValue(i[0], i[1], '1')  # Back to black.
                else:
                    pass
            #print("Cleared out here.")
            self.selected_cells.clear()  # We clear our selection, in order to start a new one.
            self.selected_notes.clear()  # We clear our NOTE selection as well, starting over on a new click-highlight.
            self.previously_selected_cells.clear()

    ###----------------------------------------------------------------------
    def onLeftSelectDown2(self, event):

        self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())
        #pass
        if self.mode == self.select_mode:
            if self.pianoroll.XYToCell(event.GetPosition()) != self.currentlySelectedCell:
                if not event.ShiftDown():
                    wx.CallAfter(self.clear_out_highlight, event)
                    #wx.CallAfter(self.m_v.CurrentActor().actor_array3D_changed, event)
                    #self.m_v.CurrentActor().actor_array3D_changed()
        elif self.mode == self.draw_mode:
            #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
            #print("Drawing 2 HERE")

            event.Skip()
        # else:
        #     pass
        #event.Veto()



    def onDragSelection(self, event):
        """
        Gets the cells that are selected by holding the left
        mouse button down and dragging
        This is a repeatedly firing function because of a drag event, meaning there are multiple calls before the final "LEFT_UP" event.
        """
        # import inspect
        # for i in inspect.getmembers(event):
        #     print("EVENT", i[0], i[1])


        #Here, we establish our starting block,
        if event.ShiftDown() and self.mode == self.select_mode:
            if self.pianoroll.GetSelectionBlockTopLeft():
                #--acquiring our top_left and bottom_right, respectively, from it.
                top_left = self.pianoroll.GetSelectionBlockTopLeft()[0] #This is repeatedly overwritten, but stays the same coordinate.
                bottom_right = self.pianoroll.GetSelectionBlockBottomRight()[0]

                #If already a shift-highlight...we don't clear it out.
                #top_left = self.currentlySelectedCell  ###.pianoroll.GetGridCursorCoords()
                #Our block is expanding as we drag, and we call this highlight function to highlight that.
                self.highlightSelectingCells(top_left, bottom_right, event)


        #Todo Unused, atm....
        #If a single-instance highlight, we clear out the previously_selected_cells.
        elif not event.ShiftDown() and self.mode == self.select_mode:
            if self.pianoroll.GetSelectionBlockTopLeft():
                # --acquiring our top_left and bottom_right, respectively, from it.
                top_left2 = self.pianoroll.GetSelectionBlockTopLeft()[0]
                bottom_right2 = self.pianoroll.GetSelectionBlockBottomRight()[0]

                #Highlighting current drag event box.
                self.highlightSelectingCells(top_left2, bottom_right2, event)


            else:
                print("No Get Selection Block Top Left?")
                pass


    ###----------------------------------------------------------------------
    def highlightSelectingCells(self, top_left, bottom_right, event):
        """
        Based on code from http://ginstrom.com/scribbles/2008/09/07/getting-the-selected-cells-from-a-wxpython-grid/
        #NOTE: This function is fired multiple times within onDragSelection, a fire for every mouse movement over a cell.
        This function is intended to only handle the BLOCK of selecting_cells by highlighting them.
        """

        #TODO Git rid of other clear out calls, the ones unnecessary.
        # if event.ShiftDown():
        #     if not self.pianoroll.GetGridCursorCoords() == self.currentlySelectedCell:
        try:
            if not event.ShiftDown() and self.mode == self.select_mode:
                #self.clear_out_highlight(event=None, manual_selection=self.selected_notes, manual=True)
                self.clear_out_highlight(event=None, manual_selection=self.all_edges, manual=True)
                #self.clear_out_highlight(event=None, manual_selection=self.selecting_cells, manual=True)
            else:
                pass
        except Exception as e:
            print(e, "No selection yet, nothing to clear out therefore.")
        self.selecting_cells = []
        self.all_edges = np.array([])

        #Assuming a 4X4 starting at cell(0,0)... (Y,X)

        rows_start = top_left[0]   #Y  (0, 3)
        rows_end = bottom_right[0] #Y  (3, 3)
        cols_start = top_left[1]   #X  (3, 0)
        cols_end = bottom_right[1] #X  (3, 3)
        rows = range(rows_start, rows_end + 1)
        cols = range(cols_start, cols_end + 1)

        #top_left = Midas.pianorollpanel.pianoroll.GetSelectionBlockTopLeft()[0]
        #bottom_right = Midas.pianorollpanel.pianoroll.GetSelectionBlockBottomRight()[0]
        #np.arange(Midas.pianorollpanel.cols_start, Midas.pianorollpanel.cols_end+1, 1).reshape(len(Midas.pianorollpanel.rows), 1)
        #np.full((Midas.pianorollpanel.cols_end+1, 1), Midas.pianorollpanel.rows_start)

        #(0, 0) (0, 1) (0, 2) (0, 3)
        top_edge_cells = np.hstack([np.full((len(cols), 1), rows_start), np.arange(cols_start, cols_end+1, 1).reshape(len(cols), 1)])

        #(0, 0) (1, 0) (2, 0) (3, 0)
        left_edge_cells = np.hstack([np.arange(rows_start, rows_end+1, 1).reshape(len(rows), 1), np.full((len(rows), 1), cols_start)])

        #(3, 0) (3, 1) (3, 2) (3, 3)
        bottom_edge_cells = np.hstack([np.full((len(cols),  1), rows_end), np.arange(cols_start, cols_end+1, 1).reshape(len(cols), 1)])

        #(0, 3) (1, 3) (2, 3) (3, 3)
        right_edge_cells = np.hstack([np.arange(rows_start, rows_end+1, 1).reshape(len(rows), 1), np.full((len(rows), 1), cols_end)])

        self.all_edges = np.vstack([top_edge_cells, left_edge_cells, bottom_edge_cells, right_edge_cells])


        # print("EDGES")
        # print("Top_Edge", top_edge_cells)
        # print("Left_Edge", left_edge_cells)
        # print("Bottom_Edge", bottom_edge_cells)
        # print("Right_Edge", right_edge_cells)
        # print("All Edges", all_edges)

        # if event.ShiftDown():
        #     for i in self.previously_selected_cells:
        #         self.selecting_cells.append(i)

        self.selecting_cells.extend([(row, col)
                      for row in rows
                      for col in cols])

        # self.selecting_cells_array = np.array([self.selecting_cells])
        # print("SCA", self.selecting_cells_array)


        self.tuple_edges_list = [tuple(i) for i in self.all_edges]

        self.difference = set(self.selecting_cells).difference(set(self.tuple_edges_list))  #Cells that aren't edges.


        #for i in self.selecting_cells:
        for i in self.all_edges:
            # self.selecting_cells.append((i[0], i[1]))

            ###This v-block-v 'colors' the 'highlight' area a "LIGHT BLUE" color by setting the cells "Value" to "2". (191, 216, 216)
            #If not black or green
            if self.pianoroll.GetCellValue(i[0], i[1]) != '1' and self.pianoroll.GetCellValue(i[0], i[1]) != '3':
                #Then make highlight-blue.
                self.pianoroll.SetCellValue(i[0], i[1], '2')
        print("DIFFERENCE", self.difference)
        for i in self.selecting_cells:
            # If the "NOTES" are within the selection area, repaint them "GREEN."
            if self.pianoroll.GetCellValue(i[0], i[1]) == '1':
                self.pianoroll.SetCellValue(i[0], i[1], '3')


        #print("Selecting_cells", self.selecting_cells)




            # self.selecting_cells.append((row, col))
            #
            # ###This v-block-v 'colors' the 'highlight' area a "LIGHT BLUE" color by setting the cells "Value" to "2". (191, 216, 216)
            #
            # if self.pianoroll.GetCellValue(row, col) != '1' and self.pianoroll.GetCellValue(row, col) != '3':
            #     self.pianoroll.SetCellValue(row, col, '2')
            #
            # # If the "NOTES" are within the selection area, repaint them "GREEN."
            # if self.pianoroll.GetCellValue(row, col) == '1':
            #     self.pianoroll.SetCellValue(row, col, '3')


                #This blocks would get rid of blue highlight, just be enabling.
                # if self.pianoroll.GetCellValue(row,col) == '2':
                #     self.pianoroll.SetCellValue(row, col, '0')



        #print("You are selecting and highlighting the following cells: ", self.selecting_cells)


    def establish_rowscols_variables(self, top_left, bottom_right):
        #For debugging.....
        self.rows_start = top_left[0]  # Y  (0, 3)
        self.rows_end = bottom_right[0]  # Y  (3, 3)
        self.cols_start = top_left[1]  # X  (3, 0)
        self.cols_end = bottom_right[1]  # X  (3, 3)
        self.rows = range(self.rows_start, self.rows_end + 1)
        self.cols = range(self.cols_start, self.cols_end + 1)

    ###------------------------------------------------------------------
    def OnMouseLeftUp(self, evt):
        """
        On mouse left up, in draw mode, flags the change of array3d.  #Todo Do as trait events.
        In selectmode, ...
        :param evt:
        :return:
        """

        if self.mode == self.draw_mode:  ##If "Draw Mode"....
            # TODO Account for cpqn here?
            #self.log.info("OnMouseLeftUp():")
         
            # self.currentpianoroll.UpdateStream()
            mv = self.GetTopLevelParent().mayavi_view

            #THIS IS THE UPDATE FLAG FOR DRAWING NOW. It is no longer in the draw function.
            mv.CurrentActor().array3Dchangedflag = not mv.CurrentActor().array3Dchangedflag


            print("Flag changed now.", mv.CurrentActor().array3Dchangedflag)


        elif self.mode == self.select_mode:

            if evt.ShiftDown() and not evt.AltDown() and not evt.ControlDown():
                #print("Shift-Selecting 3")

                # ON SHIFT, selecting_cells gets ADDED to PREVIOUSLY_SELECTED_CELLS, then self.selected_cells becomes self.psc.
                try:
                    for i in self.selecting_cells:
                        self.previously_selected_cells.append(i) ##Append current selecting onto previous selection.

                    #Make our selected_cells set to this now appended selection.
                    self.selected_cells = self.previously_selected_cells
                    self.selected_cells = OrderedDict.fromkeys([i for i in self.selected_cells])
                    self.selected_cells = list([i for i in self.selected_cells.keys()])

                    # FINALLY, after the correct self.SELECTED_CELLS exists, we derive our 'selected_notes' from it to use in awesome functions.
                    self.selected_notes = [i for i in self.selected_cells if
                                           self.pianoroll.GetCellValue(i[0], i[1]) == '3']
                    #print("Number of DRAWN cells in selection1:", len(self.selected_notes))
                    # if not self.previously_selected_cells:
                    #     self.previously_selected_cells = self.selected_cells
                    # else:
                    #     self.previously_selected_cells = self.selected_cells
                    #         #self.previously_selected_cells.append(i)

                except AttributeError as i:
                    print("Shifted here..", i)
                    # Attempt to remember and store 'previous' ACCUMULATING blocks of selections. (so, they STACK if shift-highlighting)
                    self.selected_cells = self.selecting_cells
                    self.previously_selected_cells = self.selected_cells

                    # FINALLY, after the correct self.SELECTED_CELLS exists, we derive our 'selected_notes' from it to use in awesome functions.
                    self.selected_notes = [i for i in self.selected_cells if
                                           self.pianoroll.GetCellValue(i[0], i[1]) == '3']
                    print("Number of DRAWN cells in selection2:", len(self.selected_notes))
                    pass

            elif not evt.ShiftDown():
                #print("Not Shift-Selecting 3")
                # On not Shift, selected_cells becomes selecting_cells.
                # self.selected_cells = []  # Overwrite.
                #try:
                self.selected_cells = self.selecting_cells
                #except AttributeError:
                    #print("Still no previously_selected_cells.")
                    #pass
                self.selected_cells = OrderedDict.fromkeys([i for i in self.selected_cells])  #Gets rid of duplicates.
                self.selected_cells = list([i for i in self.selected_cells.keys()])

                # FINALLY, after the correct self.SELECTED_CELLS exists, we derive our 'selected_notes' from it to use in awesome functions.
                self.selected_notes = [i for i in self.selected_cells if self.pianoroll.GetCellValue(i[0], i[1]) == '3']
                #print("Number of DRAWN cells in selection3:", len(self.selected_notes))
                self.previously_selected_cells = self.selected_cells  #(self. previously_selected_cells already condensed here  with ordered dict)


        #if self.first_selection:

            # try:
            #     print("self.selected_cells", self.selected_cells)
            #     self.selected_notes = [i for i in self.selected_cells if
            #                            self.pianoroll.GetCellValue(i[0], i[1]) == '3']  # If cell is GREEN.
            #
            #
            #     # Then, we get rid of blue highlight.
            #     # for i in self.selected_cells:
            #     #     if self.pianoroll.GetCellValue(i[0], i[1]) == '2':  # Blue highlight to...
            #     #         self.pianoroll.SetCellValue(i[0], i[1], '0')
            #
            # except AttributeError as i:
            #     print("Attribute error here.", i)



        print("HERE!")


        # This skip is necessary. :)
        evt.Skip()


    ###------------------------------------------------------------------
    def OnDoubleClick_Out(self, evt):
        #print("Double Clicking out of selection....")
        # This block 'clicks out' of your selection.
        if not evt.ShiftDown() and self.mode == self.select_mode:
            try:
                if self.selected_cells:
                    self.clearing_cells = self.selected_cells + self.previously_selected_cells
                    for i in self.clearing_cells:
                        if self.pianoroll.GetCellValue(i[0], i[1]) == '2':  # Blue highlight to...
                            self.pianoroll.SetCellValue(i[0], i[1], '0')  # Back to white.
                        elif self.pianoroll.GetCellValue(i[0], i[1]) == '3':  # Green highlighted notes...
                            self.pianoroll.SetCellValue(i[0], i[1], '1')  # Back to black.
                        else:
                            pass
                    self.selected_cells.clear()  # We clear our selection, in order to start a new one.
                    self.selected_notes.clear()
                    self.previously_selected_cells.clear()

            except AttributeError as i:
                print("Attribute Error", i)
                pass
            self.anti_select()


    def anti_select(self):
        if self.pianoroll.GetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1]) == '1':
            if not wx.GetKeyState(wx.WXK_UP) or not wx.GetKeyState(wx.WXK_LEFT) or not wx.GetKeyState(
                    wx.WXK_DOWN) or not wx.GetKeyState(wx.WXK_RIGHT):
                self.pianoroll.SetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1], '1')
        elif self.pianoroll.GetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1]) == '0':
            if not wx.GetKeyState(wx.WXK_UP) or not wx.GetKeyState(wx.WXK_LEFT) or not wx.GetKeyState(
                    wx.WXK_DOWN) or not wx.GetKeyState(wx.WXK_RIGHT):
                self.pianoroll.SetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1], '0')


    def anti_select2(self):
        if self.pianoroll.GetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1]) == '1':
            if not wx.GetKeyState(wx.WXK_UP) or not wx.GetKeyState(wx.WXK_LEFT) or not wx.GetKeyState(
                    wx.WXK_DOWN) or not wx.GetKeyState(wx.WXK_RIGHT):
                self.pianoroll.SetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1], '0')
        elif self.pianoroll.GetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1]) == '0':
            if not wx.GetKeyState(wx.WXK_UP) or not wx.GetKeyState(wx.WXK_LEFT) or not wx.GetKeyState(
                    wx.WXK_DOWN) or not wx.GetKeyState(wx.WXK_RIGHT):
                self.pianoroll.SetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1], '1')


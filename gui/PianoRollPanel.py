import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import numpy as np
import math
#from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from gui import ZPlanesControlPanel, ActorsControlPanel
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray
from collections import OrderedDict
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

        self.currentZplane = 90

        self.draw_mode = 1
        self.select_mode = 0

        self.mode = self.draw_mode  ### "1" for Draw, 0 for Select

        self.mayavi_view = self.GetTopLevelParent().mayavi_view

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

        # For Highlight Selection feature.

        self.pianoroll.GetGridWindow().Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)

        self.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onLeftSelectDown1)
        self.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onLeftSelectDown2)


        self.pianoroll.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnDoubleClick_Out)
        self.pianoroll.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.onDragSelection)

        self.Layout()
        #self.AccelerateHomeHotkey()
        self.SetSizerAndFit(mainSizer)


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
        self.cbCellsPerQrtrNote = wx.ComboBox(self.toolbar, cbID1, "4", wx.DefaultPosition, wx.DefaultSize,
                                              choices=["1", "2", "4", "8", "16", "32"],
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


        # bmp_DeleteLayer = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, btn_size)
        # # btn_DeleteLayer = wx.Button(self, -1, "MIDI Art")
        # # sizer.Delete(btnDeleteLayer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        # self.toolbar.AddTool(id_DeleteLayer, "", bmp_DeleteLayer, shortHelp="Delete Layer", kind=wx.ITEM_NORMAL)
        # self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_DeleteLayer)

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

        newvalue = int(self.cbCellsPerQrtrNote.GetValue())
        self.mayavi_view.cpqn = newvalue
        print("Changing CPQN, updating grid reticle.")

        # need to redraw current piano roll and update stream
        self.pianoroll.ChangeCellsPerQrtrNote(newvalue)

        # self.pianoroll.ForceRefresh()

        # I don't fully understand, but this call needs to happen at the end of the function. (On-que, reticle update bugfix.)
        self.mayavi_view.cpqn_changed_flag = not self.mayavi_view.cpqn_changed_flag

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

        mv = self.GetTopLevelParent().mayavi_view

        if mv.CurrentActor() == None:
            pass
            # current_actor = self.pianoroll.cur_array3d
        else:
            current_actor = mv.CurrentActor()
            on_points = np.argwhere(current_actor._array3D[:, :, z] >= 1.0)
            print("On_Points", on_points)
            for i in on_points:
                self.pianoroll._table.SetValue(127 - i[1], i[0],
                                               "0")  # TODO Track mode stuff! What can the 'value' parameter be?
            current_actor._array3D[:, :, z] = current_actor._array3D[:, :,
                                              z] * 0  # TODO Different way to write this? Multiply whole array3d by 0?
            self.pianoroll.ForceRefresh()
            mv.actors[mv.cur_ActorIndex].array3Dchangedflag += 1

        self.pianoroll.ResetGridCellSizes()
        self.pianoroll.ForceRefresh()

    ####FOR DRAW-SELECTION FEATURE
    ###----------------------------------------------------------------------

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
                        # self.mayavi_view.CurrentActor()._array3D[int(col / cpqn), int(127 - row), int(z)] = 0
                elif self.pianoroll.drawing == 1:
                    if (self.pianoroll.GetCellValue(row, col) == "0" and span != wx.grid.Grid.CellSpan_Inside):
                        self.pianoroll.DrawCell("1", row, col, 1, self.pianoroll.draw_cell_size)
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
                    print("onMouseLeftDown mouse position", curgridcoords)
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
        This is an OnCellSelection event handler. It process the selection of cell from the mouse left click, as well as from arrow keys.
        """
        if self.mode == self.select_mode:
            print("You selected Row %s, Col %s" % (event.GetRow(), event.GetCol()))
            self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())

            self.first_selection = False
            self.selected_cells = []



        # WORKING ANTI_SELECT for select_mode!!!!!
            self.anti_select2()
        #event.Skip()
        elif self.mode == self.draw_mode:
            print("Drawmode HERE.")
        #time.sleep(20)

        # if self.pianoroll.GetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1]) == '1':
        #     if not wx.GetKeyState(wx.WXK_UP) or wx.GetKeyState(wx.WXK_LEFT) or wx.GetKeyState(
        #             wx.WXK_DOWN) or wx.GetKeyState(wx.WXK_RIGHT):
        #         self.pianoroll.SetCellValue(self.currentlySelectedCell[0], self.currentlySelectedCell[1], '0    ')

        #curgridcoords[0], curgridcoords[1]

    def clear_out(self, event):
        print("Attempting Clear Out....")

        try:
            if not self.first_selection:  # If it's not the first selection batch....
                if self.previously_selected_cells:
                    print("You have PCRs.", self.previously_selected_cells)
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


    ###----------------------------------------------------------------------
    def onLeftSelectDown2(self, event):

        self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())
        #pass
        if self.mode == self.select_mode:
            if self.pianoroll.XYToCell(event.GetPosition()) != self.currentlySelectedCell:
                if not event.ShiftDown():
                    wx.CallAfter(self.clear_out, event)
        elif self.mode == self.draw_mode:
            print("Drawing 2 HERE")

        #event.Skip()
        else:
            pass
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
        This function is intended to only handle the BLOCK of selecting cells by highlighting them.
        """

        # if event.ShiftDown():
        #     if not self.pianoroll.GetGridCursorCoords() == self.currentlySelectedCell:


        rows_start = top_left[0]
        rows_end = bottom_right[0]
        cols_start = top_left[1]
        cols_end = bottom_right[1]
        rows = range(rows_start, rows_end + 1)
        cols = range(cols_start, cols_end + 1)

        self.selecting_cells = []

        # if event.ShiftDown():
        #     for i in self.previously_selected_cells:
        #         self.selecting_cells.append(i)

        for row in rows:
            for col in cols:
                self.selecting_cells.append((row, col))

                ###This v-block-v 'colors' the 'highlight' area a "LIGHT BLUE" color by setting the cells "Value" to "2". (191, 216, 216)

                if self.pianoroll.GetCellValue(row, col) != '1' and self.pianoroll.GetCellValue(row, col) != '3':
                    self.pianoroll.SetCellValue(row, col, '2')

                # If the "NOTES" are within the selection area, repaint them "GREEN."
                if self.pianoroll.GetCellValue(row, col) == '1':
                    self.pianoroll.SetCellValue(row, col, '3')

        print("You are selecting and highlighting the following cells: ", self.selecting_cells)


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
            self.log.info("OnMouseLeftUp():")
            print("On Mouse Left Up:")
            # self.currentpianoroll.UpdateStream()
            mv = self.GetTopLevelParent().mayavi_view
            print("Flag not changed yet.", mv.CurrentActor().array3Dchangedflag)
            mv.CurrentActor().array3Dchangedflag = not mv.CurrentActor().array3Dchangedflag
            print("Flag changed now.", mv.CurrentActor().array3Dchangedflag)

        elif self.mode == self.select_mode:

            if evt.ShiftDown():
                print("Shift-Selecting 3")

                # ON SHIFT, selecting_cells gets ADDED to PREVIOUSLY_SELECTED_CELLS, then self.selected_cells becomes self.psc.
                try:
                    for i in self.selecting_cells:
                        self.previously_selected_cells.append(i) ##Append current selecting onto previous selection.

                    #Make our selected_cells set to this now appended selection.
                    self.selected_cells = self.previously_selected_cells
                    self.selected_cells = OrderedDict.fromkeys([i for i in self.selected_cells])
                    self.selected_cells = list([i for i in self.selected_cells.keys()])

                    # Attempt to remember and store 'previous' ACCUMULATING blocks of selections. (so, they STACK if shift-highlighting)
                    if not self.previously_selected_cells:
                        self.previously_selected_cells = self.selected_cells
                    else:
                        self.previously_selected_cells = self.selected_cells
                            #self.previously_selected_cells.append(i)
                except AttributeError as i:
                    #print(i)
                    pass
            elif not evt.ShiftDown():



                print("Not Shift-Selecting 3")
                # On not Shift, selected_cells becomes selecting_cells.
                # self.selected_cells = []  # Overwrite.
                try:
                    self.selected_cells = self.selecting_cells
                except AttributeError:
                    print("Still no previously_selected_cells.")
                    pass
                self.selected_cells = OrderedDict.fromkeys([i for i in self.selected_cells])
                self.selected_cells = list([i for i in self.selected_cells.keys()])

                self.previously_selected_cells = self.selected_cells  #(self. previously_selected_cells already condensed here  with ordered dict)



            # FINALLY, after the correct self.SELECTED_CELLS exists, we derive our 'selected_notes' from it to use in awesome functions.
            try:
                print("self.selected_cells", self.selected_cells)
                self.selected_notes = [i for i in self.selected_cells if
                                       self.pianoroll.GetCellValue(i[0], i[1]) == '3']  # If cell is GREEN.
                print("Number of DRAWN cells in selection:", len(self.selected_notes))

                # Then, we get rid of blue highlight.
                # for i in self.selected_cells:
                #     if self.pianoroll.GetCellValue(i[0], i[1]) == '2':  # Blue highlight to...
                #         self.pianoroll.SetCellValue(i[0], i[1], '0')

            except AttributeError as i:
                print("Attribute error here.", i)

        print("HERE!")

        # This skip is necessary. :)
        evt.Skip()


    ###------------------------------------------------------------------
    def OnDoubleClick_Out(self, evt):
        print("Double Clicking out of selection....")
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


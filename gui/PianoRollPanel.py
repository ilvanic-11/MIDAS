import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import numpy as np
import math
from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from gui import ZPlanesControlPanel, ActorsControlPanel
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray

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
        #HasTraits.__init__(self)
        wx.Panel.__init__(self, parent, -1)
        
        self.log = log
        self.log.info("PianoRollPanel.__init__()")
        self.tb = self.SetupToolbar()

        self.currentZplane = 90

        self.mode = 1  ### "1" for Draw, 0 for Select

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
        #self.ctrlpanelSplit.SetMinimumPaneSize(10)

        #For Draw feature(s).
        self.pianoroll.GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        self.pianoroll.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)

        #For Highlight Selection feature.
        self.pianoroll.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onSingleSelect)
        self.pianoroll.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.onDragSelection)


        self.Layout()
        self.SetSizerAndFit(mainSizer)

  
    def DeletePianoRoll(self, index):
        self.log.info("DeletePianoRoll")
        self.pianorolls.pop(index-1)
        #self.pianorollNB.DeletePage(index-1)
        
    
    def OnMotion(self, evt):
        #self.log.debug("OnMotion: Drawing=%d " % self.pianoroll.drawing)
        cpqn = self.pianoroll._cells_per_qrtrnote
        z = self.currentZplane
        if self.mode == 1:  ##If mode is "Draw Mode".....
            if evt.Dragging() and evt.LeftIsDown():
                x, y = self.pianoroll.CalcUnscrolledPosition(evt.GetPosition())
                row = self.pianoroll.YToRow(y)
                col = self.pianoroll.XToCol(x)
                (span, sx, sy) = self.pianoroll.GetCellSize(row, col)
                # print(f"row={row},col={col}" + self.pianorolls[self.currentpianoroll].print_cell_info(row,col))

                if self.pianoroll.drawing == 0:
                    if (self.pianoroll.GetCellValue(row, col) == "1" or span == wx.grid.Grid.CellSpan_Inside):
                        self.pianoroll.EraseCell(row, col)
                        #self.mayavi_view.CurrentActor()._array3D[int(col / cpqn), int(127 - row), int(z)] = 0
                elif self.pianoroll.drawing == 1:
                    if (self.pianoroll.GetCellValue(row, col) == "0" and span != wx.grid.Grid.CellSpan_Inside):
                        self.pianoroll.DrawCell("1", row, col, 1, self.pianoroll.draw_cell_size)
        elif self.mode == 0:  ##if Select Mode...
            pass
        else:
            pass
                    #self.mayavi_view.CurrentActor()._array3D[int(col / cpqn), int(127 - row), int(z)] = 1
            # print("x=%d, y=%d, row=%d, col=%d" % (x,y,row,col))
        evt.Skip()


    def OnMouseLeftUp(self, evt):
        """
        On mouse left up, flags the change of array3d.  #Todo Do as trait events.
        :param evt:
        :return:
        """
        if self.mode == 1: ##If "Draw Mode"....
            #TODO Account for cpqn here?
            self.log.info("OnMouseLeftUp():")
            print("On Mouse Left Up:")
            #self.currentpianoroll.UpdateStream()
            mv = self.GetTopLevelParent().mayavi_view
            print("Flag not changed yet.", mv.CurrentActor().array3Dchangedflag)
            mv.CurrentActor().array3Dchangedflag = not mv.CurrentActor().array3Dchangedflag
            print("Flag changed now.", mv.CurrentActor().array3Dchangedflag)
        else:
            pass
        evt.Skip()


    def SetupToolbar(self):

        btn_size = (20, 20)
        self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
        self.toolbar.SetToolBitmapSize(btn_size)

        bmp_drawmode = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, btn_size)
        bmp_selectmode = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, btn_size)

        id_drawmode = 10
        self.toolbar.AddRadioTool(id_drawmode, "Select", bmp_drawmode, wx.NullBitmap, "Draw Mode", "Change to Select Mode",None)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_drawmode)

        id_selectmode = 20
        self.toolbar.AddRadioTool(id_selectmode, "select", bmp_selectmode, wx.NullBitmap, "Select Mode", "Change to Draw Mode",None)
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

        id_AddLayer = 30
        bmp_AddLayer = wx.ArtProvider.GetBitmap(wx.ART_PLUS, wx.ART_TOOLBAR, btn_size)
        #btn_AddLayer = wx.Button(self, -1, "MIDI Art")
       # sizer.Add(btnAddLayer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.toolbar.AddTool(id_AddLayer, "", bmp_AddLayer, shortHelp="Add Layer", kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id= id_AddLayer)

        id_DeleteLayer = 40
        bmp_DeleteLayer = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, btn_size)
        # btn_DeleteLayer = wx.Button(self, -1, "MIDI Art")
        # sizer.Delete(btnDeleteLayer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.toolbar.AddTool(id_DeleteLayer, "", bmp_DeleteLayer, shortHelp="Delete Layer", kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_DeleteLayer)

        id_DeleteAllLayers = 50
        bmp_DeleteAllLayers = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_TOOLBAR, btn_size)
        self.toolbar.AddTool(id_DeleteAllLayers, "", bmp_DeleteAllLayers, shortHelp="Delete All Layers", kind=wx.ITEM_NORMAL)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_DeleteAllLayers)


        self.toolbar.Realize()
        return self.toolbar


    def OnCellsPerQrtrNoteChanged(self, event):
        print("OnCellsPerQrtrNoteChanged(): new size = %s" % self.cbCellsPerQrtrNote.GetValue())

        newvalue = int(self.cbCellsPerQrtrNote.GetValue())
        self.mayavi_view.cpqn = newvalue
        print("Changing CPQN, updating grid reticle.")

        # need to redraw current piano roll and update stream
        self.pianoroll.ChangeCellsPerQrtrNote(newvalue)

        #self.pianoroll.ForceRefresh()

        #I don't fully understand, but this call needs to happen at the end of the function. (On-que, reticle update bugfix.)
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
            #self.InsertNewPianoRoll(len(self.pianorolls))
            pass
        elif event.GetId() == 40:
            self.DeletePianoRoll(len(self.pianorolls))
        elif event.GetId() == 50:
            #self.DeleteAllPianoRolls()
            pass


    def OnDrawMode(self, event):
        self.log.info("OnSelectMode():")
        self.mode = 1

    def OnSelectMode(self, event):
        self.log.info("OnDrawMode():")
        self.mode = 0


    def print_cell_sizes(self):  #TODO Redundant? Consider deleting this button.
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
                #self.pianoroll._table.SetValue(y, x, "0")
                #self.GetTopLevelParent().mayavi_view.CurrentActor()._array3D[x, 127 - y, z] = 0

        mv = self.GetTopLevelParent().mayavi_view
        if mv.CurrentActor() == None:
            pass
            #current_actor = self.pianoroll.cur_array3d
        else:
            current_actor = mv.CurrentActor()
            on_points = np.argwhere(current_actor._array3D[:, :, z] >= 1.0)
            print("On_Points", on_points)
            for i in on_points:
                self.pianoroll._table.SetValue(127- i[1], i[0], "0")   #TODO Track mode stuff! What can the 'value' parameter be?
            current_actor._array3D[:, :, z] = current_actor._array3D[:, :, z] * 0   #TODO Different way to write this? Multiply whole array3d by 0?
            self.pianoroll.ForceRefresh()
            mv.actors[mv.cur_ActorIndex].array3Dchangedflag += 1
        self.pianoroll.ResetGridCellSizes()
        self.pianoroll.ForceRefresh()


    ####FOR HIGHLIGHT-SELECTION FEATURE
    # ----------------------------------------------------------------------
    def onDragSelection(self, event):
        """
        Gets the cells that are selected by holding the left
        mouse button down and dragging
        """
        # import inspect
        # for i in inspect.getmembers(event):
        #     print("EVENT", i[0], i[1])
        if event.ShiftDown() and self.mode == 0:
            if self.pianoroll.GetSelectionBlockTopLeft():
                top_left = self.pianoroll.GetSelectionBlockTopLeft()[0]
                bottom_right = self.pianoroll.GetSelectionBlockBottomRight()[0]
                self.highlightSelectedCells(top_left, bottom_right, event)
            # for i in self.selected_cells:
            #     if self.pianoroll.GetCellValue(i[0], i[1]) != '1':
            #         self.pianoroll.SetCellValue(i[0], i[1], '2')

        elif not event.ShiftDown() and self.mode == 0:
            if self.pianoroll.GetSelectionBlockTopLeft():
                top_left = self.pianoroll.GetSelectionBlockTopLeft()[0]
                bottom_right = self.pianoroll.GetSelectionBlockBottomRight()[0]
                self.highlightSelectedCells(top_left, bottom_right, event)
            # if self.selected_cells:
            #     for i in self.selected_cells:
            #         if self.pianoroll.GetCellValue(i[0], i[1]) == '2':
            #             self.pianoroll.SetCellValue(i[0], i[1], '0')
            else:
                pass
    # ----------------------------------------------------------------------
    def onGetSelection(self, event):
        """
        Get whatever cells are currently selected
        """
        cells = self.pianoroll.GetSelectedCells()
        if not cells:
            if self.pianoroll.GetSelectionBlockTopLeft():
                top_left = self.pianoroll.GetSelectionBlockTopLeft()[0]
                bottom_right = self.pianoroll.GetSelectionBlockBottomRight()[0]
                self.highlightSelectedCells(top_left, bottom_right, event)
            else:
                print(self.currentlySelectedCell)
        else:
            print(cells)

    # ----------------------------------------------------------------------
    def onSingleSelect(self, event):
        """
        Get the selection of a single cell by clicking or
        moving the selection with the arrow keys
        """
        print("You selected Row %s, Col %s" % (event.GetRow(), event.GetCol()))

        self.currentlySelectedCell = (event.GetRow(),
                                      event.GetCol())
        event.Skip()

    # ----------------------------------------------------------------------
    def highlightSelectedCells(self, top_left, bottom_right, event):
        """
        Based on code from http://ginstrom.com/scribbles/2008/09/07/getting-the-selected-cells-from-a-wxpython-grid/
        """





        rows_start = top_left[0]
        rows_end = bottom_right[0]
        cols_start = top_left[1]
        cols_end = bottom_right[1]
        rows = range(rows_start, rows_end + 1)
        cols = range(cols_start, cols_end + 1)

        if event.ShiftDown() and self.mode == 0:
            self.selected_cells = []
            for row in rows:
                for col in cols:
                ###This v-block-v 'colors' the 'highlight' area a "LIGHT BLUE" color by setting the cells "Value" to "2". (191, 216, 216)
                    self.selected_cells.extend([(row, col)])
                    if self.pianoroll.GetCellValue(row, col) != '1':
                        self.pianoroll.SetCellValue(row, col, '2')
        elif not event.ShiftDown() and self.mode == 0:
            self.unselecting_cells = []
            for row in rows:
                for col in cols:
                    self.unselecting_cells.extend([(row, col)])
                    if self.pianoroll.GetCellValue(row, col) == '2':
                        self.pianoroll.SetCellValue(row, col, '0')
                    #This "if" removes cells being "unselected" from the stored self.selected_cells.
                    #If there is a selection....
                    try:

                        if (row, col) in self.selected_cells:
                            self.selected_cells.remove((row, col))
                            #Remove unselectings...
                        else:
                            pass
                    except AttributeError as i:
                        #print(i)
                        pass
            # for deselect in self.selected_cells:
            #     if deselect in self.unselecting_cells:
            #         self.selected_cells.remove(deselect)

         # self.selected_cells.extend([(row, col)
         #               for row in rows
         #               for col in cols])

        #print("You selected the following cells: ", self.selected_cells)

        # for cell in self.selected_cells:
        #     row, col = cell
        #     print("Cell's Value", self.pianoroll.GetCellValue(row, col))

        self.selected_cells_activated = [i for i in self.selected_cells if int(self.pianoroll.GetCellValue(i[0], i[1])) == 1]
        print("Number of DRAWN cells in selection:", len(self.selected_cells_activated))
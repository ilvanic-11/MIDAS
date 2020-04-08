import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import numpy as np
import math
from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from gui import ZPlanesControlPanel
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
        
        self.zplanesctrlpanel = ZPlanesControlPanel.ZPlanesControlPanel(self, self.log)
        
        self.currentZplane = 0
        
        self.pianoroll = PianoRoll.PianoRoll(self,
                                             self.currentZplane,
                                             -1,
                                             wx.DefaultPosition,
                                             wx.DefaultSize,
                                             0,
                                             "Piano Roll",
                                             self.log
                                             )
        
        self.pianoroll.GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        self.pianoroll.GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)

        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        horizSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(self.tb, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4)
        mainSizer.Add(horizSizer, 0, wx.EXPAND)
        
        horizSizer.Add(self.zplanesctrlpanel, 1, wx.EXPAND,)
        horizSizer.Add(self.pianoroll, 1, wx.EXPAND)
        self.SetSizer(mainSizer)

   # def OnPageChanged(self, evt):
        #self.currentpianoroll = self.pianorolls[self.pianorollNB.GetSelection()]
        #self.cbCellsPerQrtrNote.SetSelection(self.cbCellsPerQrtrNote.FindString(repr(self.currentpianoroll.GetCellsPerQrtrNote())))


    #def InsertNewPianoRoll(self, index):
        #self.log.info("InsertNewPianoRoll")
        #pianoroll = PianoRoll.PianoRoll(self.pianorollNB, index, -1, wx.DefaultPosition, wx.DefaultSize, 0, f"Piano Roll {index}" , self.log)

        #self.pianorolls.insert(index, pianoroll)
        #self.pianorollNB.InsertPage(index, pianoroll, str(index), select=True)
		

        #self.pianorolls[index].GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        #self.pianorolls[index].GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)

        #self.currentpianoroll = self.pianorolls[self.currentZplane]

    def DeletePianoRoll(self, index):
        self.log.info("DeletePianoRoll")
        self.pianorolls.pop(index-1)
        #self.pianorollNB.DeletePage(index-1)
        

    # def DeleteAllPianoRolls(self):
    #     self.log.info("DeleteAllPianoRolls: ")
    #     self.pianorolls.clear()
    #     #self.pianorollNB.DeleteAllPages()
    
    def OnMotion(self, evt):
        #self.log.debug("OnMotion: Drawing=%d " % self.pianoroll.drawing)

        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.pianoroll.CalcUnscrolledPosition(evt.GetPosition())
            row = self.pianoroll.YToRow(y)
            col = self.pianoroll.XToCol(x)
            (span, sx, sy) = self.pianoroll.GetCellSize(row, col)
            # print(f"row={row},col={col}" + self.pianorolls[self.currentpianoroll].print_cell_info(row,col))

            if self.pianoroll.drawing == 0:
                if (self.pianoroll.GetCellValue(row, col) == "1" or span == wx.grid.Grid.CellSpan_Inside):
                    self.pianoroll.EraseCell(row, col)
            elif self.pianoroll.drawing == 1:
                if (self.pianoroll.GetCellValue(row, col) == "0" and span != wx.grid.Grid.CellSpan_Inside):
                    self.pianoroll.DrawCell("1", row, col, 1, self.pianoroll.draw_cell_size)

            # print("x=%d, y=%d, row=%d, col=%d" % (x,y,row,col))
        evt.Skip()

    def SetupToolbar(self):

        btn_size = (20, 20)
        self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
        self.toolbar.SetToolBitmapSize(btn_size)

        bmp_selectmode = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, btn_size)
        bmp_drawmode = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, btn_size)

        id_selectmode = 10
        self.toolbar.AddRadioTool(id_selectmode, "Select", bmp_selectmode, wx.NullBitmap, "Select Mode", "Change to Select Mode",None)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_selectmode)

        id_drawmode = 20
        self.toolbar.AddRadioTool(id_drawmode, "Draw", bmp_drawmode, wx.NullBitmap, "Draw Mode", "Change to Draw Mode",None)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_drawmode)

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
        self.cbCellsPerQrtrNote = wx.ComboBox(self.toolbar, cbID1, "1", wx.DefaultPosition, wx.DefaultSize,
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

        # need to redraw current piano roll and update stream
        self.pianoroll.ChangeCellsPerQrtrNote(newvalue)

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
            self.OnSelectMode(event)
        elif event.GetId() == 20:
            self.OnDrawMode(event)
        elif event.GetId() == 30:
            #self.InsertNewPianoRoll(len(self.pianorolls))
            pass
        elif event.GetId() == 40:
            self.DeletePianoRoll(len(self.pianorolls))
        elif event.GetId() == 50:
            #self.DeleteAllPianoRolls()
            pass


    def OnSelectMode(self, event):
        self.log.info("OnSelectMode():")

    def OnDrawMode(self, event):
        self.log.info("OnDrawMode():")

    def OnMouseLeftUp(self, evt):
        self.log.info("OnMouseLeftUp():")
        #self.currentpianoroll.UpdateStream()
        self.GetTopLevelParent().mayavi_view.arraychangedflag += 1
        evt.Skip()

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
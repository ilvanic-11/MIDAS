import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import numpy as np
import math
from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray

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
    def __init__(self, parent, log):
        #HasTraits.__init__(self)
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        tb = self.SetupToolbar()
        self.Piano_Roll = PianoRoll


        self.pianorollNB = wx.Notebook(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.NB_LEFT|wx.NB_FIXEDWIDTH)
        self.pianorolls = list()


        self.InsertNewPianoRoll(0)
        self.currentPage = self.pianorolls[self.pianorollNB.GetSelection()]


        self.pianorolls[0].GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        self.pianorolls[0].GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)


        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)



        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(tb, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4)
        mainSizer.Add(self.pianorollNB, 1, wx.EXPAND)
        self.SetSizer(mainSizer)



    def OnPageChanged(self, evt):
        self.currentPage = self.pianorolls[self.pianorollNB.GetSelection()]
        self.cbCellsPerQrtrNote.SetSelection(self.cbCellsPerQrtrNote.FindString(repr(self.currentPage.GetCellsPerQrtrNote())))
        #TODO: Fix DrawCellSize

    def InsertNewPianoRoll(self, index):
        self.log.WriteText("InsertNewPianoRoll(): ")
        pianoroll = self.Piano_Roll.PianoRoll(self.pianorollNB, index, -1, wx.DefaultPosition, wx.DefaultSize, 0, f"Piano Roll {index}" , self.log)

        self.pianorolls.insert(index, pianoroll)
        self.pianorollNB.InsertPage(index, pianoroll, str(index), select=True)

        self.pianorolls[index].GetGridWindow().Bind(wx.EVT_MOTION, self.OnMotion)
        self.pianorolls[index].GetGridWindow().Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)

        self.currentPage = self.pianorolls[self.pianorollNB.GetSelection()]

    def DeletePianoRoll(self, index):
        self.log.WriteText("DeletePianoRoll(): ")
        self.pianorolls.pop(index-1)
        self.pianorollNB.DeletePage(index-1)

    def DeleteAllPianoRolls(self): #TODO Notebook is gone, so needs rewriting.
        self.log.WriteText("DeletePianoRoll(): ")
        self.pianorolls.clear()
        self.pianorollNB.DeleteAllPages()

    def OnMotion(self, evt):
        # print("OnMotion: Drawing=%d, " % self.pianorolls[self.currentPage].drawing)

        if evt.Dragging() and evt.LeftIsDown():
            page = self.currentPage
            x, y = page.CalcUnscrolledPosition(evt.GetPosition())
            row = page.YToRow(y)
            col = page.XToCol(x)
            (span, sx, sy) = page.GetCellSize(row, col)
            # print(f"row={row},col={col}" + self.pianorolls[self.currentPage].print_cell_info(row,col))

            if page.drawing == 0:
                if (page.GetCellValue(row, col) == "1" or span == wx.grid.Grid.CellSpan_Inside):
                    page.EraseCell(row, col)
            elif page.drawing == 1:
                if (page.GetCellValue(row, col) == "0" and span != wx.grid.Grid.CellSpan_Inside):
                    page.DrawCell("1", row, col, 1, self.currentPage.draw_cell_size)

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
        self.currentPage.ChangeCellsPerQrtrNote(newvalue)

    def OnDrawCellSizeChanged(self, event):
        print("OnDrawCellSizeChanged(): new size = %s" % self.cbDrawCellSize.GetValue())
        self.currentPage.draw_cell_size = int(self.cbDrawCellSize.GetValue())

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
            self.InsertNewPianoRoll(len(self.pianorolls))
        elif event.GetId() == 40:
            self.DeletePianoRoll(len(self.pianorolls))
        elif event.GetId() == 50:
            self.DeleteAllPianoRolls()


    def OnSelectMode(self, event):
        print("OnSelectMode():")

    def OnDrawMode(self, event):
        print("OnDrawMode():")

    def OnMouseLeftUp(self, evt):
        self.log.WriteText("OnMouseLeftUp():")
        #self.currentPage.UpdateStream()
        self.GetTopLevelParent().mayaviview.arraychangedflag += 1
        evt.Skip()

    def print_cell_sizes(self):  #TODO Redundant? Consider deleting this button.
        s = ""
        with open("test.txt", 'w') as f:
            for row in range(0, self.currentPage.GetNumberRows()):
                for col in range(0, self.currentPage.GetNumberCols()):
                    s += self.currentPage.print_cell_info(row, col)
                s += "\n"
                print(type(s))
            f.write(s)
            return s
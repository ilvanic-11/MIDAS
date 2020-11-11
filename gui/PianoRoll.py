import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import copy
import logging
import numpy as np
from wx._core import PaintDC
import math
#from midas_scripts import musicode, music21funcs

import time

""" 
PianoRollPanel
Toolbar
wxNoteBook
|-Page: PianoRoll0
|-Page: PianoRoll1
|-Page: PianoRoll2
|- ...


"""


# 10 Octaves for midi = 120 semitones.  Some DAWs (FL) allow 128 semitones
NUM_TONES = 128

# 1=white key; 2=black key
                #   C  #  D  #  E  F  #  G  #  A  #  B
SEMITONE_PIANO = (  1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1,
                    )
SEMITONE_NOTES = ("C","#","D","#","E","F","#","G","#","A","#","B")


# Used to make the row Labels of the grid look like a piano
class PianoRollRowLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color):
        self.color = color

    def Draw(self, grid, dc, rect, row):
        dc.SetBrush(wx.Brush(wx.Colour(self.color)))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangle(rect)
        hAlign, vAlign = grid.GetRowLabelAlignment()
        text = grid.GetRowLabelValue(row)
        self.DrawBorder(grid, dc, rect)
        self.DrawText(grid, dc, rect, text, hAlign, vAlign)


class PianoRollColLabelRenderer(glr.GridLabelRenderer):
    def __init__(self, color, txtcolor):
        self.color = color
        self.txtcolor = txtcolor

    def Draw(self, grid, dc, rect, col):
        dc.SetBrush(wx.Brush(wx.Colour(self.color)))
        dc.SetPen(wx.Pen(wx.Colour(self.color)))
        dc.DrawRectangle(rect)
        self.DrawBorder(grid, dc, rect)

        #STUPID WX WON'T LET ME CHANGE THE TEXT COLOR AND I DON'T KNOW WHY
        dc.SetPen(wx.Pen(wx.Colour(self.txtcolor)))
        dc.SetFont(wx.Font(6, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        dc.SetBrush(wx.Brush(wx.Colour(self.txtcolor)))
        dc.SetTextForeground(wx.Colour(self.txtcolor))

        hAlign, vAlign = grid.GetColLabelAlignment()
      # text = grid.GetColLabelValue(col)

        #self.DrawText(grid, dc, rect, text, hAlign, vAlign)

class PianoRollDataTable(wx.grid.GridTableBase):
    """ A grid data table that connects to the traited 3D array in the mayavi_view
    """
    
    log = logging.getLogger("PianoRollDataTable")
    def __init__(self, pianorollpanel):
        wx.grid.GridTableBase.__init__(self)
        self.pianorollpanel = pianorollpanel
    # need to store a reference to the piano roll panel.  GridTableBase does not store gui parents.
    
    #def SetRefToPianoRollPanel(self, pianorollpanel):



    def GetNumberCols(self):
        #print("GetNumberCols(): {}".format(self.parent.GetTopLevelParent().mayavi_view.CurrentActor()._array3D.shape[0]))
        if self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor():
            #print(self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor())
            #print("Has current_actor.")
            return self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor()._array3D.shape[0]
        else:
            return 5000
        
    def GetNumberRows(self):
        #print("GetNumberCols(): {}".format(self.parent.GetTopLevelParent().mayavi_view.CurrentActor()._array3D.shape[1]))
        if self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor():
            #print(self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor())
            #print("Has current_actor.")
            return self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor()._array3D.shape[1]
        else:
            return 128
        
    def GetValue(self, row, col):


        if self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor():
            if (self.pianorollpanel):
                z = self.pianorollpanel.currentZplane
            else:
                z = 0
            if z < 0:
                return ""
            self.log.debug(f"ZZZ = {z} type:")
            self.log.debug(type(z))
            return str(int(self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor()._array3D[col][127-row][z]))

        else:
            return ""

    def SetValue(self, row, col, value):
        self.log.info(f"PianoRollDataTable.SetValue(): ({col},{row}),val={value}")

        if self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor():
            z = self.pianorollpanel.currentZplane
            self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor()._array3D[col][127-row][z] = int(value)

    def AppendCols(self, numCols=1, updateLables=True):
        #print("Super", super())
        #wx.grid.GridTableBase.AppendCols(self, numCols)
        pass #TODO WHY does this have to be pass when overriding? I don't fully understand this.
    #
    def DeleteCols(self, pos=0, numCols=1, updateLables=True):  #Overload duplicates original here.
        #print("Super", super())
        #wx.grid.GridTableBase.DeleteCols(self, pos, numCols)
        pass

# Main Class for the PianoRoll, based orn wx.Grid
class PianoRoll(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
    log = logging.getLogger("PianoRoll")
    
    def __init__(self, parent, z, id, pos, size, style, name, log):
        wx.grid.Grid.__init__(self, parent, id, pos, size, wx.RETAINED, name)

        self.log = log

        self.stream = music21.stream.Stream()

        #mayavi_view reference
        self.m_v = self.GetTopLevelParent().mayavi_view

        #wx background style
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        #self.CreateGrid(NUM_TONES,512)
        self._table = PianoRollDataTable(self.GetParent().GetParent())

        #current array_3d
        self.cur_array3d = None

        self.SetTable(self._table, True)

        glr.GridWithLabelRenderersMixin.__init__(self)
        # self.SetDefaultEditor(wx.grid.GridCellBoolEditor())
        self.PCR = PianoRollCellRenderer(self)
        self.SetDefaultRenderer(self.PCR)
        print("BDC", self.PCR.bdc)

        # upd = wx.RegionIterator(self.GetUpdateRegion())
        # print("UPD", upd)
        # #wx.RegionIterator

        #One measure and one octave at a time.
        self.SetScrollRate(160, 120)  #For precision scrolling, use scrollbar arrows, or scroll-bar right-click-->"Scroll Here"

        self.cur_scrollrate = self.GetScrollPixelsPerUnit()
        self.last_known_pos = None
        self.last_known_scrollX = None
        self.last_known_scrollY = None

        self.max_x = 600  # max zoom-in
        self.max_y = 400  # max zoom-in

        self.zoom_interval = 4

        self.drawing = 1  # Used for click and drag to draw notes

        self.draw_cell_size = 1
        self._cells_per_qrtrnote = 4

        self.SetColMinimalAcceptableWidth(3)
        self.SetRowMinimalAcceptableHeight(3)
        self.RowLabelSize = 60  #was 40
        self.ColLabelSize = 20


        # Initial label size for piano keys
        self.SetLabelFont(wx.Font(6, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        self.DrawColumnLabels()

        #TODO Why isn't this a function? 9/23/20
        # Set up the "piano" with note labels
        for i in reversed(range(self.NumberRows)):
            self.SetRowSize(i, 10)
            #crazy fuck math I'll never remember to label the piano roll notes and octaves
            self.SetRowLabelValue(i, SEMITONE_NOTES[(NUM_TONES - 1 - i) % 12] + str(10 - int((i+4)/12)))

            if SEMITONE_PIANO[NUM_TONES - 1 - i]:
                self.SetRowLabelRenderer(i, PianoRollRowLabelRenderer("WHITE"))
            else:
                self.SetRowLabelRenderer(i, PianoRollRowLabelRenderer("BLACK"))
            #self.DisableRowResize(i)

        self.DisableDragColMove()
        self.DisableDragColSize()
        self.DisableDragGridSize()
        self.DisableDragRowSize()


        self.EnableEditing(False)  #TODO What does this do? 11/2/20 (read-only something, someshit....)

        #self.SetSelectionBackground(wx.Colour(0, 255, 0, 50)) #Since we have our own CellRenderer, I believe this doesn't work...

        self.SetSelectionForeground(wx.Colour(0, 255, 0, 50)) ##Green Edges

        #EVT Bindings
        #------------------
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridLClick)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnCellSelected)
        #self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

        #--Right Click menu binding.
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)


        # self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.ChangeScrollRate)

        #--Left Click on Labels scrolls the client area. #TODO Fix and do better.
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnMeasureLabelsLeftClick)

        self.Bind(wx.EVT_SCROLLWIN_THUMBTRACK, self.OnThumbDragging)
        self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.OnThumbRelease)


        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
        # self.Bind(wx.EVT_SCROLLWIN_LINEUP, self.OnScroll)
        # self.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.OnScroll)

        self.Bind(wx.EVT_PAINT, self.OnPaint)




    #Functions--------------------
    def OnThumbDragging(self, event):
        print("Dragging")
        #self.m_v.new_reticle_box()


    def OnThumbRelease(self, event):
        print("Thumb Release")
        #self.m_v.scroll_changed_flag = not self.m_v.scroll_changed_flag
        #self.m_v.new_reticle_box()
        event.Skip()


    def OnMeasureLabelsLeftClick(self, event):
        self.last_known_pos = event.GetPosition()
        print("Label Event Position:", self.last_known_pos)
        row = event.GetRow()
        print("Label Event Row:", row)
        col = event.GetCol()
        print("Label Event Col:", col)

        s_h = self.GetScrollPos(wx.HORIZONTAL)  #cur scrollunitsperpixel here is 100
        print("Scroll_H:", s_h)
        s_v = self.GetScrollPos(wx.VERTICAL)    #cur scrollunitsperpixel here is 100
        print("Scroll_V:", s_v)
        s_linex = self.GetScrollLineX()
        print("Scroll_LineX:", s_linex)
        s_liney = self.GetScrollLineY()
        print("Scroll_LineY:", s_liney)
        c_s = self.GetClientSize()
        print("ClientSize:", c_s)

        #Acquire scrollunitsperpixel as tuple.
        scrollrate_x, scrollrate_y = self.GetScrollPixelsPerUnit()

        #SetScrollRate so pixels==scrollticks.
        self.SetScrollLineX(1)
        self.SetScrollRate(1, 1)

        #Store scroll positions after scrollrate change.
        self.last_known_scrollX = self.GetScrollPos(wx.HORIZONTAL)    #cur scrollunitsperpixel here is 1
        self.last_known_scrollY = self.GetScrollPos(wx.VERTICAL)      #cur scrollunitsperpixel here is 1

        viewstart = self.GetViewStart()
        print("ViewStart:", viewstart)
        print("SCROLLRATE:", self.GetScrollPixelsPerUnit())

        #Pixels == Scroll-ticks here.
        self.Scroll((viewstart[0] + self.last_known_pos[0] - 60), self.last_known_scrollY * scrollrate_y)  #38 is the label compensation value.    new_s_v-19
        #wx.CallLater(1000, self.SetScrollRate, x=100, y=100)
        wx.CallAfter(self.m_v.new_reticle_box)

        #Reestablish after event.
        self.last_known_scrollY = self.GetScrollPos(wx.HORIZONTAL)  #cur h_scrollunitsperpixel here is 1
        self.last_known_scrollX = self.GetScrollPos(wx.VERTICAL)    #cur v_scrollunitsperpixel here is 1
        #self.ChangeScrollRate(scrollrate_x, scrollrate_y)
        #event.Skip()



    def OnScroll(self, event):
        print("EVT_ID", event.GetId())

        print("Scrolling, bitch.")
        #TODO Learn Event Stack

        s_h = self.GetScrollPos(wx.HORIZONTAL)
        s_v = self.GetScrollPos(wx.VERTICAL)

        if len(self.m_v.highlighter_calls) == 0:
            pass
        else:
            wx.CallAfter(self.m_v.new_reticle_box)
            event.Skip()


    def OnPaint(self, event):
        print("Painting, bitch.")
        pdc = wx.PaintDC(self)
        PRClientSize = self.GetClientSize()
        self.bitmap = wx.Bitmap(PRClientSize[0], PRClientSize[1])
        dc = wx.BufferedPaintDC(self, self.bitmap)
        #dc = wx.AutoBufferedPaintDC(self)
        #TODO What Dafuq calls Draw() in the CellRenderer?
        #TODO Then
        #TODO DO DRAW SHIT HERE, LICKABITCH


    def DrawColumnLabels(self):
        # Set up column labels to have measure numbers and stuff
        for i in range(self.NumberCols):
            self.SetColSize(i, 10)
            self.DisableColResize(i)
            cells_per_measure = self._cells_per_qrtrnote * 4
            if (i % cells_per_measure == 0):
                self.SetColLabelValue(i, repr(int(i / cells_per_measure + 1)))
                self.SetColLabelRenderer(i, PianoRollColLabelRenderer("LIME GREEN", "BLACK"))
            elif (i % (cells_per_measure / 4) == 0):
                self.SetColLabelValue(i, "")
                self.SetColLabelRenderer(i, PianoRollColLabelRenderer("FOREST GREEN", "BLACK"))
            else:
                self.SetColLabelValue(i, "")
                self.SetColLabelRenderer(i, PianoRollColLabelRenderer("LIGHT STEEL BLUE", "BLACK"))


    def ClearGrid(self):
        #TODO Is this working? ResetGridCellSizes has 'spans' that haven't been touched in a while....
        print("ClearGrid():")
        #TODO Clear using self.cur_array3d
        super().ClearGrid()
        print("Here.")
        self.ResetGridCellSizes()  #TODO This breaks ChangeCellsPerQrtrNote?
        #print("Here5.")


    def ChangeCellsPerQrtrNote(self, newvalue):
        if newvalue == self._cells_per_qrtrnote:
            pass
        oldvalue = self._cells_per_qrtrnote
        self._cells_per_qrtrnote = newvalue

        # Clear grid
        self.ClearGrid()
        #print("Here5.1")
        #Change number of columns
        oldNumCols = self._table.GetNumberCols()
        #print("Here5.2")
        newNumCols = int((newvalue / oldvalue) * oldNumCols)
        #print("Here5.3")
        if newNumCols > oldNumCols:
            #print("Here5.4, --newNumCols is >")
            self._table.AppendCols(newNumCols - oldNumCols, True)
            #print("Here5.5.")
        elif oldNumCols > newNumCols:
            #print("Here5.4, --newNumCols is <")
            self._table.DeleteCols(0, oldNumCols - newNumCols, True)
            #print("Here5.6.")

        self.DrawColumnLabels()
        #print("Here6.")

        # Draw notes based on the saved stream
        #self.StreamToGrid(self.stream) #TODO WE don't use a stream here anymore?


    def GetCellsPerQrtrNote(self):
        return self._cells_per_qrtrnote


    def ResetGridCellSizes(self):
        noUpdates = wx.grid.GridUpdateLocker(self)

        #TODO Haven't touched spans in a while. Return to this when we deal with cellspans\stream durations.
        print("Here2")
        for y in range(self._table.GetNumberRows()):
            for x in range(self._table.GetNumberCols()):
                span,r,c = self.GetCellSize(x,y)

                #print("Here3")
                if span == wx.grid.Grid.CellSpan_Main:
                    print("({},{})".format(x, y))
                    self.SetCellSize(x,y,1,1)
                   # msg = wx.grid.GridTableMessage(self,wx.grid.GRIDNO
        print("Here4")


    def UpdateStream(self):
        print("Update Stream()")
        # matrix = np.zeros((self.GetNumberCols(), self.GetNumberRows()), dtype=np.int8)
        # # matrix = [ [None] * self.GetNumberRows() for _ in range(self.GetNumberCols())]
        # for x in range(self.GetNumberCols()):
        #     for y in range(self.GetNumberRows()):
        #         # print("x=%d,y=%d" % (x, y))
        #         # print("grid.NumRows=%d" % grid.GetNumberRows())
        #         if self.GetCellValue(self.GetNumberRows() - 1 - y, x) >= "1":
        #             matrix[x, y] = 1
        # self.stream = music21funcs.matrix_to_stream(matrix, False, self._cells_per_qrtrnote)
        self.GridToStream()

    # def OnCellChanged(self):
    #     self.log.info"OnCellChanged:")
    #     x, y = self.CalcUnscrolledPosition(evt.GetPosition())
    #     row = self.YToRow(y)
    #     col = self.XToCol(x)
    #
    #     n = music21.note.Note()
    #     n.pitch.midi = row
    #     n.duration.quarterLength = self.pix_note_size * self.current_note_draw_size
    #     self.stream.insert(col, n)


    def OnMouseWheel(self, event):
        if event.GetWheelAxis() == wx.MOUSE_WHEEL_HORIZONTAL or event.GetWheelDelta() < 120:
            event.Skip()
            return

        state = wx.GetMouseState()
        if state.ShiftDown():
            if event.GetWheelRotation() >= 120:
                self.ZoomInVertical(1)
                return
            elif event.GetWheelRotation() <= -120:
                self.ZoomOutVertical(1)
        elif state.AltDown():   #CHANGED FROM ControlDown to avoid conflicting with other scrolling function(s).
            if event.GetWheelRotation() >= 120:
                self.ZoomInHorizontal(1)
            elif event.GetWheelRotation() <= -120:
                self.ZoomOutHorizontal(1)



        event.Skip()


    def ZoomInVertical(self, intervals):
        cur = self.GetRowSize(1)
        if (cur - intervals * self.zoom_interval) > 1:
            for r in range(0, self.GetNumberRows()):
                self.SetRowSize(r, cur - intervals * self.zoom_interval)
        else:
            for r in range(0, self.GetNumberRows()):
                self.SetRowSize(r, 1)
        newfontsize = max(min(self.GetRowSize(1) - 4, 14), 2)

        #It would be nice to set the LabelFont size for the columns and rows separately,
        #but it would take writing a new function.
        self.SetLabelFont(wx.Font(newfontsize, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


    def ZoomOutVertical(self, intervals):
        cur = self.GetRowSize(1)
        if (cur + intervals * self.zoom_interval) < self.max_y:
            for r in range(0, self.GetNumberRows()):
                self.SetRowSize(r, cur + intervals * self.zoom_interval)
        newfontsize = max(min(self.GetRowSize(1) - 4, 14), 2)

        # It would be nice to set the LabelFont size for the columns and rows separately,
        # but it would take writing a new function.
        self.SetLabelFont(wx.Font(newfontsize, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


    def ZoomInHorizontal(self, intervals):
        cur = self.GetColSize(1)
        if (cur - intervals * self.zoom_interval) > 1:
            for c in range(0, self.GetNumberCols()):
                self.SetColSize(c, cur - intervals * self.zoom_interval)
        else:
            for c in range(0, self.GetNumberCols()):
                self.SetColSize(c, 1)


    def ZoomOutHorizontal(self, intervals):
        cur = self.GetColSize(1)
        if (cur + intervals * self.zoom_interval) < self.max_x:
            for c in range(0, self.GetNumberCols()):
                self.SetColSize(c, cur + intervals * self.zoom_interval)


    def DrawPianoRoll(self, matrix):
        self.log.warning("DrawPianoRoll(): (Deprecated)")
        """
        Expects that "matrix" origin is at the top left,

        [ (0,0) (1,0) (2,0) (3,0) ... |
	    | (0,1) (1,1) (2,1) (3,1) ... |
	    | (0,2) (1,2) (2,2) (3,2) ... |
	    | (0,3) (1,3) (2,3) (3,3) ... ]

        :param matrix:  npArray of shape (x, 128)
        :return:
        """
        assert(type(matrix) == np.ndarray)

        self.ClearGrid()

        if matrix.shape[1] > NUM_TONES :
            print("DrawPianoRoll: Error with height of matrix")
            return

        if self.GetNumberCols() < matrix.shape[0]:
            print("Appending additional columns.")
            self.AppendCols(matrix.shape[0] - self.GetNumberCols())

        noUpdates = wx.grid.GridUpdateLocker(self)

        for x in range(0, matrix.shape[0]):
            for y in range(0, matrix.shape[1]):
                self._table.SetValue(y, x, str(matrix[x][y]))

        self.UpdateStream()


    def OnCellSelected(self, evt):
        self.log.info("onCellSelected():")
        #self.SetCellValue(evt.Row, evt.Col, "1")
        #self.DeselectCell(evt.GetRow(), evt.GetCol())
        evt.Skip()


    def OnGridLClick(self, evt):

        z = self.GetTopLevelParent().pianorollpanel.currentZplane
        current_actor = self.m_v.CurrentActor()
        cpqn = self._cells_per_qrtrnote

        row = evt.GetRow()
        col = evt.GetCol()
        self.log.info(f"OnGridLClick({col},{row}")
        self.log.debug("  _table.GetValue(0,0) = {}".format(self._table.GetValue(0, 0)))
        self.log.debug("  self.GetCellValue(0,0) = {}".format(self.GetCellValue(0,0)))

       # x = evt.GetRow()
        #y = evt.GetCol()
        if self._table.GetValue(row, col) == "1":
            self.EraseCell( row, col)
            current_actor._array3D[int(row / cpqn), int(127-col), int(z)] =  0
            self.drawing = 0
        elif self._table.GetValue(row, col) == "0":
            #print("ROW", row)
            #print("COL", col)
            self.DrawCell("1", row, col, 1, int(self.draw_cell_size))
            #current_actor._array3D[int(row / cpqn), int(127-col), int(z)] = 1
            self.drawing = 1

        evt.Skip()
        self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag += 1

        #After the drawing event, update the array_3d accordingly.

        # on_points = np.argwhere(current_actor._array3D[row, col, z] >= 1.0)
        # print("On_Points", on_points)
        # for i in on_points:
        #     self._table.SetValue(127 - i[1], i[0], eval("self.drawing"))
        #
        # current_actor._array3D[:, :, z] = current_actor._array3D[:, :, z] * 0
        # self.ForceRefresh()
        # self.m_v.actors[self.m_v.cur_ActorIndex].array3Dchangedflag += 1
        # self.ResetGridCellSizes()
        # self.ForceRefresh()


    def EraseCell(self, row, col):
        cur_span, cur_sy, cur_sx = self.GetCellSize(row, col)
        c = col
        while cur_span == wx.grid.Grid.CellSpan_Inside and c >= 0:
           # self.log.debug(f"  going left ({row}, {c}): " + self.print_cell_info(row, c))
            c = c - 1
            cur_span, cur_sy, cur_sx = self.GetCellSize(row, c)


       # self.log.debug(f"  (actual erase) ({row}, {c}): " + self.print_cell_info(row, c))
        self.SetCellSize(row, c, 1, 1)
        self.SetCellValue(row, c, "0")

        #page = self.GetTopLevelParent().pianorollpanel.pianoroll
        layer = self.GetTopLevelParent().pianorollpanel.currentZplane

        self.m_v.CurrentActor()._array3D[c, 127 - row, layer] = 0


    def DrawCell(self, val, row, col, new_sy, new_sx):
        self.log.info(f"DrawCell():")
        cur_span, cur_sy, cur_sx = self.GetCellSize(row, col)

        if cur_span == wx.grid.Grid.CellSpan_Inside:
            return

        #layer = self.GetTopLevelParent().pianorollpanel.currentZplane

        x = col
        while x < (col + new_sx):
            #self.log.debug(f"x={x}: " + self.print_cell_info(row, x))

            span, _, _ = self.GetCellSize(row, x)
            if span != wx.grid.Grid.CellSpan_None:
                #self.log.debug("Break")
                return
            x += 1

        y = row
        while y < (row + new_sy):
            span, _, _ = self.GetCellSize(y, col)
            if span != wx.grid.Grid.CellSpan_None:
                return
            y += 1

        print(f"  {row},{col} = {val}")
        self._table.SetValue(row, col, val)
        #self.SetCellValue(row, col, val)
        #print("X", x)
        #self.m_v.CurrentActor()._array3D[x * self._cells_per_qrtrnote, 127 - y, val] = 1
        #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
        self.SetCellSize(row, col, new_sy, new_sx)


    def StreamToGrid(self, in_stream, z=None):
        """
        Converts a music21 stream into wxGrid of shape (x,128) where x is the highestTime of the stream.

        The piano roll grid indexes beginning at the top left, e.g.:
        [ (0,0) (1,0) (2,0) (3,0) ... ]
        | (0,1) (1,1) (2,1) (3,1) ... |
        | (0,2) (1,2) (2,2) (3,2) ... |
        | (0,3) (1,3) (2,3) (3,3) ... |

        but midi pitches begin at 0 for the low C0 note and go up the piano roll.
        So the y index of the matrix will be subtracted from 128.  #TODO 127?

        :param in_stream: 			music21.Stream object
        :param cell_note_size:  note duration that each cell/pixel represents
        :return: 				np.array
        """
        if z is None:
            z = self.GetTopLevelParent().pianorollpanel.currentZplane

        self.ClearGrid()



        for n in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            if type(n) is music21.chord.Chord:
                for p in n.pitches:
                    y = int(self._cells_per_qrtrnote * n.offset)
                    x = 127 - p.midi
                    size = int(self._cells_per_qrtrnote * n.duration.quarterLength)
                    if size < 1:
                        print("Note size is too small for current grid CellsPerNote.")
                    else:
                        self._table.SetValue(x, y, "1")
                        self.m_v.CurrentActor()._array3D[y, 127 - x, z] = 1
                        self.SetCellSize(x, y, 1, size)
                # print(matrix)
            elif type(n) is music21.note.Note:
                y = int(self._cells_per_qrtrnote * n.offset)
                x = 127 - n.pitch.midi
                size =  int(self._cells_per_qrtrnote * n.duration.quarterLength)
                if size < 1:
                    print("Note size is too small for current grid CellsPerNote.")
                else:
                    self._table.SetValue(x, y, "1")
                    self.m_v.CurrentActor()._array3D[y, 127 - x, z] = 1
                    self.SetCellSize(x, y, 1, size)

        # print(matrix)

        self.m_v.CurrentActor().array3Dchangedflag += 1
        self.stream = in_stream


    def GridToStream(self, update_actor=True):
        """
        Converts a wxGrid of shape (x,128) into a music21 stream.
        x-axis is note offsets and durations
        y index is midi pitches

        The piano roll grid indexes beginning at the top left, e.g.:
        [ (0,0) (1,0) (2,0) (3,0) ... ]
        | (0,1) (1,1) (2,1) (3,1) ... |
        | (0,2) (1,2) (2,2) (3,2) ... |
        | (0,3) (1,3) (2,3) (3,3) ... |

        but midi pitches begin at 0 for the low C0 note and go up the piano roll.
        So the y index of the matrix will be subtracted from 128.

        :param matrix: 	npArray of shape (x, 128) with only possible values of 1 and 0.
        :param connect:  Connect adjacent cells of the matrix into a single longer note in the stream
        :param cells_per_qrtrnote:  number of pixels/cells per quarter note
        :return: music21 stream
        """
        print("GridToStream()")
        self.log.debug("GridToStream():")
        s = music21.stream.Stream()
        print("1")
        print("Rows:", self._table.GetNumberRows())
        print("Cols:", self._table.GetNumberCols())
        # for x in range(0, self._table.GetNumberRows()):
        #     for y in range(0, self._table.GetNumberCols()):
        #         #print(self.GetCellValue(x,y))
        #         #time.sleep(1)
        #         if (self._table.GetValue(x, y) == "1"):
        on_points = np.argwhere(self.m_v.CurrentActor()._array3D[:, :, self.m_v.cur_z] >= 1.0)
        print("On_Points", on_points)
        for i in on_points:
            (span, sx, sy) = self.GetCellSize(i[1], i[0])
            #print("2")
            n = music21.note.Note()
            #print("A note:", n)
            #print("3")
            n.pitch.midi = i[1]
            n.offset = i[0] / self._cells_per_qrtrnote
            n.duration.quarterLength = sy / self._cells_per_qrtrnote
            n.volume.velocity = self.m_v.cur_z
            s.insert(n.offset, n)

        print("4")
        s.makeMeasures(inPlace=True)
        print("5")
        self.stream = s
        if update_actor:
            self.m_v.CurrentActor()._stream = s
        else:
            pass
        s.show('txt')
        #self.m_v.CurrentActor().array3Dchangedflag += 1  #TODO Change to 'not' method?
        return s


    def print_cell_info(self, row, col):
        s = ""
        span_print = ("N","M","I")
        v = self.GetCellValue(row, col)
        (span, sx, sy) = self.GetCellSize(row, col)
        # s += repr(size) + ", "
        s += "(" + v + "," + span_print[span] + "," + repr(sx) + "," + repr(sy) + ") "
        return s

    def OnCellRightClick(self, evt):
        # def OnContextMenu(self, event):
        # self.log.WriteText("OnContextMenu\n")

        # only do this part the first time so the events are only bound once
        #
        # Yet another anternate way to do IDs. Some prefer them up top to
        # avoid clutter, some prefer them close to the object of interest
        # for clarity.
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewIdRef()
            self.popupID2 = wx.NewIdRef()
            self.popupID3 = wx.NewIdRef()
            self.popupID4 = wx.NewIdRef()
            self.popupID5 = wx.NewIdRef()
            self.popupID6 = wx.NewIdRef()
            self.popupID7 = wx.NewIdRef()
            self.popupID8 = wx.NewIdRef()
            self.popupID9 = wx.NewIdRef()

            self.Bind(wx.EVT_MENU, self.OnPopup_Properties, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnDeleteSelection, id=self.popupID6)
            self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
            self.Bind(wx.EVT_MENU, self.OnPopupEight, id=self.popupID8)
            self.Bind(wx.EVT_MENU, self.OnPopupNine, id=self.popupID9)

        # make a menu
        menu = wx.Menu()
        # Show how to put an icon in the menu
        item = wx.MenuItem(menu, self.popupID1, "Properties")
        # bmp = images.Smiles.GetBitmap()
        # item.SetBitmap(bmp)
        menu.Append(item)
        # add some other items
        menu.Append(self.popupID2, "Two")
        menu.Append(self.popupID3, "Three")
        menu.Append(self.popupID4, "Four")
        menu.Append(self.popupID5, "Five")
        menu.Append(self.popupID6, "Delete Selection")
        # make a submenu
        sm = wx.Menu()
        sm.Append(self.popupID8, "sub item 1")
        sm.Append(self.popupID9, "sub item 1")
        menu.Append(self.popupID7, "Test Submenu", sm)

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopup_Properties(self, event):
        pass

    def OnPopupTwo(self, event):
        pass

    def OnPopupThree(self, event):
        pass

    def OnPopupFour(self, event):
        pass

    def OnPopupFive(self, event):
        pass

    def OnDeleteSelection(self, event):
        # Deletes 'selected' not 'activated' actors.
        alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
        print("J_list", [j for j in range(len(self.mayavi_view.actors), -1, -1)])
        for j in range(len(self.mayavi_view.actors), 0, -1):  # Fucking OBOE errors...
            print("J", j)
            if alb.IsSelected(j - 1):
                self.OnBtnDelActor(evt=None, cur=j - 1)
                print("Seletion %s Deleted." % (j - 1))
        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

    def OnPopupSeven(self, event):
        pass

    def OnPopupEight(self, event):
        pass

    def OnPopupNine(self, event):
        pass

# class MyGridCellAttributerProvider(wx.grid.GridCellAttrProvider)
#     def __init__(self):

    ###
    ######
    #########--------------------------------------------
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

        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMusic21ConverterParseDialog, id=new_id1)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMusicodeDialog, id=new_id2)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMIDIArtDialog, id=new_id3)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMIDIArt3DDialog, id=new_id4)
        # TODO These aren't working as desired.....
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_actors_listbox, id=new_id5)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_zplanes, id=new_id6)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_pianorollpanel, id=new_id7)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_pycrust, id=new_id8)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_mayavi_view, id=new_id9)
        self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.focus_on_mainbuttonspanel, id=new_id10)

        # Shift into which gear.
        entries[0].Set(wx.ACCEL_NORMAL, wx.WXK_F1, new_id1)
        entries[1].Set(wx.ACCEL_NORMAL, wx.WXK_F2, new_id2)
        entries[2].Set(wx.ACCEL_NORMAL, wx.WXK_F3, new_id3)
        entries[3].Set(wx.ACCEL_NORMAL, wx.WXK_F4, new_id4)
        # TODO THESE aren't working as desired...
        entries[4].Set(wx.ACCEL_NORMAL, wx.WXK_F5, new_id5)
        entries[5].Set(wx.ACCEL_NORMAL, wx.WXK_F6, new_id6)
        entries[6].Set(wx.ACCEL_NORMAL, wx.WXK_F7, new_id7)
        entries[7].Set(wx.ACCEL_NORMAL, wx.WXK_F8, new_id8)
        entries[8].Set(wx.ACCEL_NORMAL, wx.WXK_F9, new_id9)

        entries[9].Set(wx.ACCEL_NORMAL, wx.WXK_F11, new_id10)

        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)


class PianoRollCellRenderer(wx.grid.GridCellRenderer):
    def __init__(self, parent):
        wx.grid.GridCellRenderer.__init__(self)
        #self.window = wx.Window()
        #self.new_dc = wx._core.PaintDC(self.window)
        self.parent = parent

        self.pdc = None
        self.bdc = None
        self.PRClientSize = self.parent.GetClientSize()
        #self.bitmap.Create()
        self.bitmap = wx.Bitmap(self.PRClientSize[0], self.PRClientSize[1])

        # print("BitSize", self.bitmap.GetSize())
        # self.ndc = None
        #self.mdc = wx.MemoryDC(self.bitmap)
        # self.mdc.SetBrush(wx.Brush("BLACK", wx.SOLID))
        #
        #     #self.mdc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
        # self.mdc.SetPen(wx.TRANSPARENT_PEN)
        # self.mdc.SelectObject(self.bitmap)
        #self.mdc.Blit()
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        # self.bitmap.SetSize(wx.Size(rect.width, rect.height))
        # print("ori", dc.DeviceOrigin)
        #print("Grid", grid)
        #print("RECT", rect)
        #def Intercept(dc, Draw=self.Draw):
            #self.bdc = wx.BufferedDC(dc, self.bitmap, style=wx.BUFFER_VIRTUAL_AREA)
        if self.pdc is None:
            self.pdc = dc

        if self.bdc is None:
            self.bdc = wx.BufferedDC(dc, self.bitmap, style=wx.BUFFER_CLIENT_AREA)
        else:
            pass
        #print("DC", type(dc), dc)

        #dc = self.new_dc
        #if self.ndc is not None:
        #self.ndc = dc
        #dc = self.mdc
        #print("BITMAP Draw?")
        #dc.CanDrawBitmap()
        #print(self.GetRefCount())

        self.grid_highlight_color = "LIGHT BLUE"

        value = grid.GetCellValue(row, col)
        #values = grid._table.Get

        ##NOTE: "value" is a string.
        if value == "1":
            dc.SetBrush(wx.Brush("BLACK", wx.BRUSHSTYLE_SOLID))
        elif int(value) == 2:
            dc.SetBrush(wx.Brush(self.grid_highlight_color, wx.BRUSHSTYLE_SOLID))
        elif int(value) >= 3:
            dc.SetBrush(wx.Brush("GREEN", wx.BRUSHSTYLE_SOLID))
        else:
            dc.SetBrush(wx.Brush("WHITE", wx.BRUSHSTYLE_SOLID))
        try:
            dc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
            dc.SetPen(wx.TRANSPARENT_PEN)
            #print("rx, ry, rw, rh", rect.x, rect.y, rect.width, rect.height)
            #dc.DrawIcon(wx.Icon('black', type=wx.BITMAP_TYPE_ANY, desiredWidth=rect.width, desiredHeight=rect.height), rect.x, rect.y)
            dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
        finally:
            dc.SetPen(wx.NullPen)
            dc.SetBrush(wx.NullBrush)
            dc.DestroyClippingRegion()
        #dc.UnMask()


import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import copy
import numpy as np
import math
from midas_scripts import musicode, music21funcs
import wx.lib.dragscroller

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
    """
    A custom wx.Grid Table using user supplied data
    """
    def __init__(self,parent, z):
        # The base class must be initialized *first*
        wx.grid.GridTableBase.__init__(self)
        self.parent = parent
        self.z = z

    def GetNumberCols(self):
        #print("GetNumberCols(): {}".format(self.parent.GetTopLevelParent().mayavi_view.array3D.shape[0]))
        return self.parent.GetTopLevelParent().mayavi_view.array3D.shape[0]

    def GetNumberRows(self):
        #print("GetNumberCols(): {}".format(self.parent.GetTopLevelParent().mayavi_view.array3D.shape[1]))
        return self.parent.GetTopLevelParent().mayavi_view.array3D.shape[1]

    def GetValue(self,row,col):
        #z = self.GetTopLevelParent().pianorollpanel.currentPage
        #z = 0
        value = str(int(self.parent.GetTopLevelParent().mayavi_view.array3D[col][127-row][self.z]))
       # print(f"GetValue({col},{row}) = {value}")
        return value

    def SetValue(self,row,col,value):

        #z = self.parent.GetTopLevelParent().pianorollpanel.currentPage
        #print(f"SetValue(({col},{row},{self.z}) val={value} ")
        #z = 0
        self.parent.GetTopLevelParent().mayavi_view.array3D[col][127-row][self.z] = int(value)

# Main Class for the PianoRoll, based on wx.Grid
class PianoRoll(wx.grid.Grid, glr.GridWithLabelRenderersMixin):
    def __init__(self, parent,z, id, pos, size, style, name, log):
        wx.grid.Grid.__init__(self, parent, id, pos, size, style, name)

        self.log = log

        self.stream = music21.stream.Stream()

        #self.CreateGrid(NUM_TONES,512)
        self._table = PianoRollDataTable(self, z)

        for x in range(0, self.GetNumberCols()):
            for y in range(0, self.GetNumberRows()):
                self.SetCellValue(y,x,"0")

        self.SetTable(self._table,True)

        #ATTEMPT at drag scroll.
        self.scroller = wx.lib.dragscroller.DragScroller(self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)



        glr.GridWithLabelRenderersMixin.__init__(self)
        # self.SetDefaultEditor(wx.grid.GridCellBoolEditor())
        self.SetDefaultRenderer(PianoRollCellRenderer())


        self.max_x = 600  # max zoom-in
        self.max_y = 400  # max zoom-in

        self.zoom_interval = 4

        print("ScrollLineX", self.GetScrollLineX())
        print("ScrollLineY", self.GetScrollLineY())
        self.SetScrollLineX(30)
        self.SetScrollLineY(30)


        self.drawing = 1 # Used for click and drag to draw notes

        self.draw_cell_size = 1
        self._cells_per_qrtrnote = 4

        self.SetColMinimalAcceptableWidth(3)
        self.SetRowMinimalAcceptableHeight(3)
        self.RowLabelSize = 40
        self.ColLabelSize = 20


        # Initial label size for piano keys
        self.SetLabelFont(wx.Font(6, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))


        self.DrawColumnLabels()

        # Set up the "piano" with note labels
        for i in reversed(range(self.NumberRows)):
            self.SetRowSize(i,10)
            #crazy fuck math I'll never remember to label the piano roll notes and octaves
            self.SetRowLabelValue(i, SEMITONE_NOTES[(NUM_TONES - 1 - i) % 12] + str(10 - int((i+4)/12)))

            if SEMITONE_PIANO[NUM_TONES - 1 - i]:
                self.SetRowLabelRenderer(i, PianoRollRowLabelRenderer("WHITE"))
            else:
                self.SetRowLabelRenderer(i, PianoRollRowLabelRenderer("BLACK"))
            self.DisableRowResize(i)

        self.DisableDragColMove()
        self.DisableDragColSize()
        self.DisableDragGridSize()
        self.DisableDragRowSize()

        self.EnableEditing(False)


        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridLClick)
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnCellSelected)
       # self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)


    #Used with attempt on right click dragscrolling.
    def OnRightDown(self, event):
        print(event)
        self.scroller.Start(event.GetPosition())

    def OnRightUp(self, event):
        self.scroller.Stop()



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
        super().ClearGrid()
        page = self.GetTopLevelParent().pianorollpanel.currentPage
        layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)

        for x in range(0, self.GetNumberCols()):
            for y in range(0, self.GetNumberRows()):
                self.SetCellValue(y,x,"0")
                self.GetTopLevelParent().mayaviview.array3D[x, 127 - y, layer] = 0
        self.ResetGridCellSizes()
        self.GetTopLevelParent().mayaviview.arraychangedflag += 1

    def ChangeCellsPerQrtrNote(self, newvalue):
        if newvalue == self._cells_per_qrtrnote:
            pass
        oldvalue = self._cells_per_qrtrnote
        self._cells_per_qrtrnote = newvalue

        # Clear grid
        self.ClearGrid()

        #Change number of columns
        oldNumCols = self.GetNumberCols()
        newNumCols = int((newvalue / oldvalue) * oldNumCols)
        if newNumCols > oldNumCols:
            self.AppendCols(newNumCols - oldNumCols, False)
        elif oldNumCols > newNumCols:
            self.DeleteCols(0, oldNumCols - newNumCols, False)

        self.DrawColumnLabels()

        # Draw notes based on the saved stream
        self.StreamToGrid(self.stream)

    def GetCellsPerQrtrNote(self):
        return self._cells_per_qrtrnote


    def ResetGridCellSizes(self):
        noUpdates = wx.grid.GridUpdateLocker(self)
        for y in range(self.GetNumberRows()):
            for x in range(self.GetNumberCols()):
                span,r,c = self.GetCellSize(x,y)

                if span == wx.grid.Grid.CellSpan_Main:
                    print("({},{})".format(x, y))
                    self.SetCellSize(x,y,1,1)
                   # msg = wx.grid.GridTableMessage(self,wx.grid.GRIDNO


    def UpdateStream(self):
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
    #     self.log.WriteText("OnCellChanged:")
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
        elif state.ControlDown():
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
        self.log.WriteText("DrawPianoRoll(): (Deprecated)")
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
                self.SetCellValue(y, x, str(matrix[x][y]))

        self.UpdateStream()

    def OnCellSelected(self, evt):
        print("onCellSelected():")
        #self.SetCellValue(evt.Row, evt.Col, "1")
        self.DeselectCell(evt.GetRow(), evt.GetCol())
        evt.Skip()

    def OnGridLClick(self, evt):


        row = evt.GetRow()
        col = evt.GetCol()
        print(f"OnGridLClick({col},{row}")
        print("  _table.GetValue(0,0) = {}".format(self._table.GetValue(0, 0)))
        print("  self.GetCellValue(0,0) = {}".format(self.GetCellValue(0,0)))

       # x = evt.GetRow()
        #y = evt.GetCol()
        if self._table.GetValue(row, col) == "1":
            self.EraseCell( row, col)
            self.drawing = 0
        elif self._table.GetValue(row, col) == "0":
            self.DrawCell("1", row, col, 1, int(self.draw_cell_size))
            self.drawing = 1

        evt.Skip()

    def EraseCell(self, row, col):
        cur_span, cur_sy, cur_sx = self.GetCellSize(row, col)
        c = col
        while cur_span == wx.grid.Grid.CellSpan_Inside and c >= 0:
           # self.log.WriteText(f"  going left ({row}, {c}): " + self.print_cell_info(row, c))
            c = c - 1
            cur_span, cur_sy, cur_sx = self.GetCellSize(row, c)


       # self.log.WriteText(f"  (actual erase) ({row}, {c}): " + self.print_cell_info(row, c))
        self.SetCellSize(row, c, 1, 1)
        self.SetCellValue(row, c, "0")

        page = self.GetTopLevelParent().pianorollpanel.currentPage
        layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)

        self.GetTopLevelParent().mayavi_view.array3D[c, 127 - row, layer] = 0


    def DrawCell(self, val, row, col, new_sy, new_sx):
        print(f"DrawCell():")
        cur_span, cur_sy, cur_sx = self.GetCellSize(row, col)

        if cur_span == wx.grid.Grid.CellSpan_Inside:
            return

        page = self.GetTopLevelParent().pianorollpanel.currentPage
        layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)

        x = col
        while x < (col + new_sx):
            #self.log.WriteText(f"x={x}: " + self.print_cell_info(row, x))

            span, _, _ = self.GetCellSize(row, x)
            if span != wx.grid.Grid.CellSpan_None:
                #self.log.WriteText("Break")
                return
            x += 1

        y = row
        while y < (row + new_sy):
            span, _, _ = self.GetCellSize(y, col)
            if span != wx.grid.Grid.CellSpan_None:
                return
            y += 1

        print(f"  {row},{col} = {val}")
        #self._table.SetValue(row, 127-col, val)
        self.SetCellValue(row, col, val)
        #self.GetTopLevelParent().mayavi_view.array3D[x, 127 - y, layer] = 1
        self.SetCellSize(row, col, new_sy, new_sx)



    def SetCellValue(self, row, col, val):
        #print("SetCellValue")
        super().SetCellValue(row, col, val)
        try:

            page = self.GetTopLevelParent().pianorollpanel.currentPage
            #print("try")
            layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)
            print(f" {col}, {row}, {layer}, {val}")





    def StreamToGrid(self, in_stream):
        """
        Converts a music21 stream into wxGrid of shape (x,128) where x is the highestTime of the stream.

        The piano roll grid indexes beginning at the top left, e.g.:
        [ (0,0) (1,0) (2,0) (3,0) ... ]
        | (0,1) (1,1) (2,1) (3,1) ... |
        | (0,2) (1,2) (2,2) (3,2) ... |
        | (0,3) (1,3) (2,3) (3,3) ... |

        but midi pitches begin at 0 for the low C0 note and go up the piano roll.
        So the y index of the matrix will be subtracted from 128.

        :param in_stream: 			music21.Stream object
        :param cell_note_size:  note duration that each cell/pixel represents
        :return: 				np.array
        """

        self.ClearGrid()

        page = self.GetTopLevelParent().pianorollpanel.currentPage
        layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)

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
                        self.GetTopLevelParent().mayavi_view.array3D[y, 127 - x, layer] = 1
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
                    self.GetTopLevelParent().mayavi_view.array3D[y, 127 - x, layer] = 1
                    self.SetCellSize(x, y, 1, size)

        # print(matrix)

        self.GetTopLevelParent().mayavi_view.arraychangedflag += 1
        self.stream = in_stream


    def GridToStream(self):
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
        self.log.WriteText("GridToStream():")
        s = music21.stream.Stream()
        for x in range(0, self.GetNumberRows()):
            for y in range(0, self.GetNumberCols()):
                if (self.GetCellValue(x, y) == "1"):
                    (span, sx, sy) = self.GetCellSize(x ,y)
                    n = music21.note.Note()
                    n.pitch.midi = 127 - x
                    n.offset = y / self._cells_per_qrtrnote
                    n.duration.quarterLength = sy / self._cells_per_qrtrnote
                    s.insert(n.offset, n)
        s.makeMeasures(inPlace=True)
        self.stream = s
        s.show('txt')
        self.GetTopLevelParent().mayavi_view.arraychangedflag += 1
        return s


    def print_cell_info(self, row, col):
        s = ""
        span_print = ("N","M","I")
        v = self.GetCellValue(row, col)
        (span, sx, sy) = self.GetCellSize(row, col)
        # s += repr(size) + ", "
        s += "(" + v + "," + span_print[span] + "," + repr(sx) + "," + repr(sy) + ") "
        return s

class PianoRollCellRenderer(wx.grid.GridCellRenderer):
    def __init__(self):
        wx.grid.GridCellRenderer.__init__(self)

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):


        value = grid.GetCellValue( row, col )
        if value >= "1":
            dc.SetBrush(wx.Brush("BLACK", wx.SOLID))
        elif value >= "2":
            dc.SetBrush(wx.Brush("GREEN", wx.SOLID))
        else:
            dc.SetBrush(wx.Brush("WHITE", wx.SOLID))
        try:
            dc.SetClippingRegion(rect.x, rect.y, rect.width, rect.height)
            dc.SetPen(wx.TRANSPARENT_PEN)
            dc.DrawRectangle(rect.x, rect.y, rect.width, rect.height)
        finally:
            dc.SetPen(wx.NullPen)
            dc.SetBrush(wx.NullBrush)
            dc.DestroyClippingRegion()

  

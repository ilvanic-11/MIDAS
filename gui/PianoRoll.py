import wx
import wx.lib.plot
import wx.grid
import wx.lib.mixins.gridlabelrenderer as glr
import music21
import copy
import logging
import numpy as np

import os
import signal
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
    """ A grid data table that connects to the traited 4D array in the mayavi_view
    """

    #log = logging.getLogger("PianoRollDataTable")
    def __init__(self, pianorollpanel):
        wx.grid.GridTableBase.__init__(self)
        self.pianorollpanel = pianorollpanel
        self._cur_actor = None #store ref to this locally to optimize (maybe?)

    # need to store a reference to the piano roll panel.  GridTableBase does not store gui parents.

    #def SetRefToPianoRollPanel(self, pianorollpanel):

    def GetNumberCols(self):
        if self._cur_actor:
            #print("CUR_SHAPE_X", self._cur_actor._array4D.shape[0])
            return self._cur_actor._array4D.shape[0]   #Todo Will this mess up on CORE UPDATE? 04/13/2021
        else:
            #return self._cur_actor.grid_length
            return self.pianorollpanel.GetTopLevelParent().mayavi_view.grid_cells_length


    def GetNumberRows(self):
        #print("GetNumberCols(): {}".format(self.parent.GetTopLevelParent().mayavi_view.CurrentActor()._array3D.shape[1]))
        if self._cur_actor:
            #print(self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor())
            #print("Has current_actor.")
            return self._cur_actor._array4D.shape[1]  #Todo Will this mess up on CORE UPDATE? 04/13/2021
        else:
            return 128


    def GetValue(self, row, col):
        # try:
        if self._cur_actor:
            if (self.pianorollpanel):
                z = self.pianorollpanel.currentZplane
            else:
                z = 0
            if z < 0:
                return ""

            return str(int(self._cur_actor._array4D[int(col)][127 - row][z][0]))

        else:
            return ""
        # except IndexError as e:
        #     print("Index error here. Your array4D code is messed up")
        #     #This helped solve a bug.
        #     #os.kill(0, signal.CTRL_C_EVENT)
        #     return ""


    def SetValue(self, row, col, value):
        if self._cur_actor:
            pr = self.pianorollpanel.pianoroll
            dur = pr.GetMusic21DurationRatio()
            print("DUR", dur)
            z = self.pianorollpanel.currentZplane

            #TODO Be minddful of these ints() when debugging.   col/self.pianorollpanel.pianoroll._cells_per_qrtrnote

            #self._cur_actor._draw_array3D[int(col)][127-row][z] = int(value)
            print("Index", ([int(col)],[127 - row],[z]))
            #ON
            self._cur_actor._array4D[int(col)][int(127 - row)][int(z)][int(0)] = int(value)
            # VELOCITY
            self._cur_actor._array4D[int(col)][int(127 - row)][int(z)][int(1)] = int(pr.draw_velocity) \
                if pr.drawing == 1 else value #value is 0 when pr.drawing == 0
            # DURATION1
            self._cur_actor._array4D[int(col)][int(127 - row)][int(z)][int(2)] = int(dur[0]) \
                if pr.drawing == 1 else value
            # DURATION2
            self._cur_actor._array4D[int(col)][int(127 - row)][int(z)][int(3)] = int(dur[1]) \
                if pr.drawing == 1 else value


    def AppendCols(self, numCols=1, updateLables=True, change_value=0):

        #print("Super", super())
        #wx.grid.GridTableBase.AppendCols(self, numCols)

        #THIS LINE CRASHES MIDAS
        #self.pianorollpanel.pianoroll.AppendCols(numCols=numCols)

        ###BIG FIX
        #https://stackoverflow.com/questions/43102681/cant-add-columns-in-wxpython-virtual-grid
        gridlib = wx.grid
        msg = gridlib.GridTableMessage(self,  # The table
                                       gridlib.GRIDTABLE_NOTIFY_COLS_APPENDED,  # what we did to it
                                       numCols)  # how many
        self.GetView().ProcessTableMessage(msg)
        pass #TODO WHY does this have to be pass when overriding...overloading? I don't fully understand this.
        ###


    # class HugeTable(wx.grid.PyGridTableBase):
    #
    #     """
    #     Table class for virtual grid
    #     """
    #
    #     def __init__(self, log, num_rows, num_cols):
    #         wx.grid.PyGridTableBase.__init__(self)
    #
    #     def AppendCols(self, *args):
    #         pass


    def DeleteCols(self, pos=0, numCols=1, updateLables=True):  #Overload duplicates original here.
        #print("Super", super())
        #wx.grid.GridTableBase.DeleteCols(self, pos, numCols)

        #THIS LINE CRASHES MIDAS
        #self.pianorollpanel.pianoroll.DeleteCols(pos=pos, numCols=numCols)

        ###BIG FIX
        #https://stackoverflow.com/questions/43102681/cant-add-columns-in-wxpython-virtual-grid

        gridlib = wx.grid
        print("Delete_method_num_cols", numCols)
        rqst = gridlib.GRIDTABLE_NOTIFY_COLS_DELETED
        print("cols_DEL", rqst)

        ##BIGGER FIX
        #https://bytes.com/topic/python/answers/38376-wxpython-grid-gridtable_notify_rows_deleted
        msg = gridlib.GridTableMessage(self,  # The table
            gridlib.GRIDTABLE_NOTIFY_COLS_DELETED, self.GetNumberCols()-numCols,  # what we did to it, #starting index,
            numCols)  # how many
        ###

        print("SEXY SEXY SEXY HERE")
        self.GetView().ProcessTableMessage(msg)
        print("MORE MORE MORE HERE")
        return

        #pass


    def GetColSize(self, col):  # real signature unknown; restored from __doc__
        """
        GetColSize(col) -> int

        Returns the width of the specified column.
        """
        #pass
        return 0


    def GetRowSize(self, row):  # real signature unknown; restored from __doc__
        """
        GetRowSize(row) -> int

        Returns the height of the specified row.
        """
        return 0



    def GetOnCells(self):
        """
        Written to solve a bug, this function is intended to work on wx grid cells only, and ignores a
        currentActor()._array4D. This function returns a list of all "on" (black) cells in the wx.Grid--
        (our pianoroll._table)--
        :return: List of cell coords(in the order wx uses them in SetValue---GetValue functions)
        """
        cells_list = []
        for i in range(0, self.GetNumberCols()):
            for j in range(0, self.GetNumberRows()):
                if self.GetValue(j, i) != "0":
                    cell = (j, i)
                    cells_list.append(cell)
                    #print("Cell", j, i)
                    #print(self.GetValue(j, i))
        return cells_list


    def ClearCells(self):
        """
        This functions sets on "1" cell's values to "0", turning them from black to white. Does not update an _array4D.
        (although, the current _array4D will still update when the flag is triggered (such as OnMouseLeftUp))

        ---As it is a quick fix for leftover cells in the grid piano roll after all actors are deleted and
        len(Midas.mayavi.actors) == 0, this function does not have to handle the dynamics of our Core Data Update.
        See Trello Cards "Checkpoint" and "Core Data Update."
        https://trello.com/c/MXKIQFAL
        https://trello.com/c/YWiioaqo

        :return: None
        """
        for i in self.GetOnCells():
            self.pianorollpanel.pianoroll.SetCellValue(i[0], i[1], "0")

    #self.pianorollpanel.pianoroll.GetRowSize()





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
        self.cur_array4d = None

        self.SetTable(self._table, True)

        glr.GridWithLabelRenderersMixin.__init__(self)

        self.PCR = PianoRollCellRenderer(self)
        self.SetDefaultRenderer(self.PCR)
        


        #Scroll one measure and one octave at a time.
        self.SetScrollRate(160, 120)  #For precision scrolling, use scrollbar arrows, or scroll-bar right-click-->"Scroll Here" or MIDDLE-CLICK ZOOM SCROLL.

        self.cur_scrollrate = self.GetScrollPixelsPerUnit()
        self.last_known_pos = None
        self.last_known_scrollX = None
        self.last_known_scrollY = None

        self.max_x = 600  # max zoom-in
        self.max_y = 400  # max zoom-in


        self.zoom_interval = 4


        self.drawing = 1  # Used for click and drag to draw notes

        self.draw_cell_size = 1  #TODO Make into drawn_note_duration. 12/31/2021

        self.draw_velocity = 90 #TODO Make scrollable button on the dash to change this.

        self.drawing_duration_value = 1.0 #TODO Make scrollable button on the dash to change this.


        self._cells_per_qrtrnote = 1



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
            #crazy whack math I'll never remember to label the piano roll notes and octaves
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
        #TODO --THIS hashed out disables the Erase Cell functionality-- 12/22/20 ( I turned it off for a reason....)
        self.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnGridLClick)

        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.OnCellSelected)
        #self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
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


    #Tod Fix\Revisit this.
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


    def GetCellFromMouseState(self):
        state = wx.GetMouseState()
        #print("F Pressed Here")
        #print("MOUSESTATE_POS", state.GetPosition())
        #print("Mouse_X", state.X)
        # print("Mouse_x", state.x)
       # print("Mouse_Y", state.Y)
        #client_dif_X = self.GetTopLevelParent().GetClientRect()[2] - self.GetClientRect()[2]
        #client_dif_Y = self.GetTopLevelParent().GetClientRect()[3] - self.GetClientRect()[3]

        #NOW WE HAVE IT, YES!!!
        pos = state.GetPosition()
        new_pos = self.ScreenToClient(pos)
        grid_cell = self.XYToCell(

            self.CalcGridWindowUnscrolledPosition((new_pos[0] - 59, new_pos[1] - 19), gridWindow=self), gridWindow=self)

  

        return grid_cell


    def OnScroll(self, event):
        #print("EVT_ID", event.GetId())

        #print("Scrolling, bitch.")
        #TODO Learn Event Stack

        s_h = self.GetScrollPos(wx.HORIZONTAL)
        s_v = self.GetScrollPos(wx.VERTICAL)

        if len(self.m_v.highlighter_calls) == 0:
            pass
        else:
            #self.m_v.new_reticle_box()
            wx.CallAfter(self.m_v.new_reticle_box)
            event.Skip()


    def ZoomToHere(self, state=None):

        #Todo You're doing it wrong. THE MOUSE CHANGES COORDS WHEN YOU "CLICK" THE BUTTON!!!!
        if state is None:
            state = wx.GetMouseState()
        else:
            state=state
        pos = state.GetPosition()
        new_pos = self.ScreenToClient(pos)
        #print("POSITION", pos)
        #print("NEW_POS", new_pos)
        client_dif_X = self.GetTopLevelParent().GetClientRect()[2] - self.GetClientRect()[2]
        #print("Client_dif_X", client_dif_X)
        client_dif_Y = self.GetTopLevelParent().GetClientRect()[3] - self.GetClientRect()[3]
        #print("Client_dif_Y", client_dif_Y)

        scroll_target = self.CalcUnscrolledPosition(new_pos)
        #print("SCROLL_TARGET", scroll_target)
        # scroll_target = self.CalcGridWindowUnscrolledPosition((new_pos[0],
        #                                                                    new_pos[1]),
        #                                                                     gridWindow=self)
        self.Scroll(scroll_target[0] - 59, scroll_target[1] - 19)
        #self.Scroll(new_pos[0]-59, new_pos[1]-19)

        self.m_v.new_reticle_box()


    def ScrollHome(self):
        self.Scroll(0, 0)
        self.m_v.new_reticle_box()


    def SendToHere(self, selected_notes):
        #TODO Is this function somewhere else now?
        pass


    def OnPaint(self, event):
        #pass
        print("Painting......")
        pdc = wx.PaintDC(self)
        PRClientSize = self.GetClientSize()
        self.bitmap = wx.Bitmap(PRClientSize[0], PRClientSize[1])
        dc = wx.BufferedPaintDC(self, self.bitmap)
        #dc = wx.AutoBufferedPaintDC(self)
        #TODO What Dafuq calls Draw() in the CellRenderer?
        #TODO Then
        #TODO DO DRAW STUFF HERE


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
        #print("ClearGrid():")
        #TODO Clear using self.cur_array3d
        super().ClearGrid()
        #print("Here.")
        self.ResetGridCellSizes()  #TODO This breaks ChangeCellsPerQrtrNote?
        #print("Here5.")


    def SetDrawingDurationValue(self):
        self.drawing_duration_value = self.draw_cell_size / self._cells_per_qrtrnote
        #dv = (dcs/cpqn)
        #dv*cpqn = dcs
        #self.drawing_duration_value / self._cells_per_qrtrnote = self.draw_cell_size

        temp_duration = music21.duration.Duration(self.drawing_duration_value)
        quarterLength_ratio = temp_duration.quarterLength.as_integer_ratio()
        print("Drawing_duration:", self.drawing_duration_value)
        return quarterLength_ratio


    def SetCellDrawingSizeValue(self):
        self.draw_cell_size = self.drawing_duration_value*self._cells_per_qrtrnote
        #dv = (dcs/cpqn)
        #dv*cpqn = dcs
        #self.drawing_duration_value / self._cells_per_qrtrnote = self.draw_cell_size

        temp_duration = music21.duration.Duration(self.drawing_duration_value)
        quarterLength_ratio = temp_duration.quarterLength.as_integer_ratio()
        print("Drawing_duration:", self.drawing_duration_value)
        return quarterLength_ratio


    def GetMusic21DurationRatio(self):
        temp_duration = music21.duration.Duration(self.drawing_duration_value)
        quarterLength_ratio = temp_duration.quarterLength.as_integer_ratio()
        print("Drawing_duration:", self.drawing_duration_value)
        return quarterLength_ratio


    def ChangeCellsPerQrtrNote(self, newcpqnvalue):
        if newcpqnvalue == self._cells_per_qrtrnote:
            pass
        self.m_v.CurrentActor().old_cpqn = self._cells_per_qrtrnote
        self.m_v.CurrentActor().cpqn = newcpqnvalue
        self._cells_per_qrtrnote = newcpqnvalue

        # Clear grid
        self.ClearGrid()
        #print("Here5.1")
        #Change number of columns
        oldNumCols = self._table.GetNumberCols()
        print("OLD_NUM_COLS_TWO", oldNumCols)

        #print("Here5.2")
        newNumCols = int(((newcpqnvalue / self.m_v.CurrentActor().old_cpqn) * oldNumCols))

        #print("Here5.3")
        if newNumCols > oldNumCols:
            #print("Here5.4, --newNumCols is >")

            # Patch in new grid length.
            if newcpqnvalue == self.m_v.CurrentActor().old_cpqn:
                pass
            else:
                self.AdjustGridLengthBasedOnCPQN(newcpqnvalue, self.m_v.CurrentActor().old_cpqn, oldNumCols)
            self._table.AppendCols(newNumCols - oldNumCols, True)
            self.AdjustCellsBasedOnCPQN(self.m_v.CurrentActor().cur_z, newcpqnvalue, self.m_v.CurrentActor().old_cpqn)

            # Reset Grid
            self.DrawColumnLabels()
            print("CPQN Changed Successfully.")
            return True
            #print("Here5.5.")

        elif oldNumCols > newNumCols:
            #print("Here5.4, --newNumCols is <")
            self.AdjustCellsBasedOnCPQN(self.m_v.CurrentActor().cur_z, newcpqnvalue, self.m_v.CurrentActor().old_cpqn)
            self._table.DeleteCols(0, oldNumCols - newNumCols, True)

            # Patch in new grid length.
            if newcpqnvalue == self.m_v.CurrentActor().old_cpqn:
                pass
            else:
                self.AdjustGridLengthBasedOnCPQN(newcpqnvalue, self.m_v.CurrentActor().old_cpqn, oldNumCols)

            # Reset Grid
            self.DrawColumnLabels()

            print("CPQN Changed Successfully.")
            return True

            #print("Here5.6.")


        #Reset Mayavi representative values by factoring cpqn.
        #--> Here.


        # TODO GRID CELLS ADJUSTMENT HERE, MAH BITCH!
        # Todo Condition check for successive factoring


        # print("Here6.")

        # Draw notes based on the saved stream
        # self.StreamToGrid(self.stream) #TODO WE don't use a stream here anymore?

        #self.m_v.CurrentActor().array4Dchangedflag = not self.m_v.CurrentActor().array4Dchangedflag

        #print("Here6.")

        # Draw notes based on the saved stream
        #self.StreamToGrid(self.stream) #TODO WE don't use a stream here anymore?


    def AdjustCellsBasedOnCPQN(self, zplane, newcpqnvalue, oldcpqnvalue):
        """
        This function operates on the selected zplane and changes all the cells in that selected grid by factoring in
        newvcpqnalue. Newcpqnvalue will always be a new cellsperqrtrnote value. (i.e. If cpqn was 1, and we're changing it to 4,
        all cells in the wx.Grid will be multiplied by a factor of 4).

        In addition, if the CPQN is increased or decreased, the x value of the CurrentActor()'s _array4D will be
        increased or decreased as well using np.vstack or np.vsplit.
        (i.e. CurrentActor().
        #>>>cur_array4D = m_v.CurrentActor()._array4D
        #>>>cur_array4D.shape --> (256, 128, 128, 5)
        #CPQN Change:
        :param zplane:          Operand zplane, established as an Int.
        :param oldcpqnvalue:    Old cells per qrtr note value FROM which we are changing.
        :param newcpqnvalue:    New cells per qrtr note value TO which we are changing.
        :return:                N\A
        """

        print("Changing cellsperqrtrnote.")

        cpqn_change_ratio = newcpqnvalue/oldcpqnvalue

        cells_change = np.argwhere(self.m_v.CurrentActor()._array4D[:, :, zplane, 0] == 1.0)  # CRITICAL--> current zplane only.

        #I think this is that one exception to our get_points_with_all_data uses.
        #cells_change = self.m_v.CurrentActor().get_points_with_all_data(z=zplane)

        #Grid cells accessibility
        cells_change[:, 1] = cells_change[:, 1] - 127
        cells_change[:, 1] = cells_change[:, 1] * -1

        #Grid cells set.

        for q in cells_change:
            # self._table.SetValue(q[1], q[0], '0')
            self.SetCellValue(q[1], q[0], '0')

        print("Cells_change", cells_change)
        print("Cells_change_type", type(cells_change))


        if newcpqnvalue > oldcpqnvalue:
            cells_change[:, 0] = cells_change[:, 0] * cpqn_change_ratio
        elif newcpqnvalue < oldcpqnvalue:
            cells_change[:, 0] = cells_change[:, 0] * cpqn_change_ratio
            # TODO Changing from one cpqn to another is producing an inaccurate display, FIXED.
            # NOTE: This method won't work if dealing with odd-metered time signatures.
        elif newcpqnvalue == oldcpqnvalue:
            cells_change[:, 0] = cells_change[:, 0]

        # Establish new.
        for q in cells_change:
            # self._table.SetValue(q[1], q[0], '1')
            self.SetCellValue(q[1], q[0], '1')

        #print("Cells_CHANGED", cells_change)
        print("Cells Adjusted Successfully.")
        return True


    def AdjustGridLengthBasedOnCPQN(self, newcpqn, oldcpqn, oldNumCols):
        """

        :param newcpqn:
        :param oldcpqn:
        :param oldnumcols:
        :return:
        """
        #Increase x length of cells in the grid by a factor of the cpqn using np.vsplit and np.vstack for _array4D.
        #Method involves appending or shaving off appropriate-shaped empty '_array4Ds' from main _array4D.
        cur_array4D = self.m_v.CurrentActor()._array4D
        print("new", newcpqn)
        print("old", oldcpqn)
        cpqn_change_ratio = newcpqn/oldcpqn
        cur_x_length = cur_array4D.shape[0]
        new_x_length = int(((cur_x_length * cpqn_change_ratio) - cur_x_length))
        print("NEW_X_LENGTH", new_x_length)

        if cpqn_change_ratio > 1: #If we are increasing our cpqn, then this value will always be greater than 1.
            print("NEW_X_LENGTH2", new_x_length)

            new_array = np.zeros(dtype=np.int8, shape=(new_x_length, 128, 128, 5))
            print("NEW_X_LENGTH3", new_x_length)

            self.m_v.CurrentActor()._array4D = np.vstack([cur_array4D,
                                                          new_array])
                                                        #As cool as this 'unpacking' was, it was the wrong logic here.
                                                        #*[new_array for i in range(0, int(cpqn_change_ratio)-1, 1)]]])

        elif cpqn_change_ratio < 1: #If we are decreasing our cpqn, then this value will always be less than 1.
            self.m_v.CurrentActor()._array4D = np.vsplit(self.m_v.CurrentActor()._array4D, oldcpqn/newcpqn).pop(0)
            #print("FORCED RETURN HERE")
            print("m_v_array4D.shape", self.m_v.CurrentActor()._array4D.shape)
            #return self.m_v.CurrentActor()._array4D.shape[0]

            #del(new_arrays)
        # except ValueError as e:
        #     print("?", e)
        #     print("Value Error?")
        #     pass
        #
        #
        # elif cpqn_change_ratio == 1:
        #     pass
        # except IndexError as e:
        #     print("NEW_X_LENGTH", new_x_length)
        #     return


        newNumCols = cur_array4D.shape[0]

        if newNumCols > oldNumCols:
            # print("Here5.4, --newNumCols is >")
            self._table.AppendCols(newNumCols - oldNumCols, True)
            # print("Here5.5.")





        elif oldNumCols > newNumCols:
            # print("Here5.4, --newNumCols is <")
            self._table.DeleteCols(pos=0, numCols=(oldNumCols - newNumCols), updateLables=True)
            # print("Here5.6.")


        #Write new cells_length to m_v variable. -->This must be direct access, not a pointer.
        self.m_v.grid_cells_length = self.m_v.CurrentActor()._array4D.shape[0]

        self.Refresh()
        self.ForceRefresh()
        print("Grid Length Adjusted Successfully.")


        #NOTE: self.DrawColumnLabels() is called shortly after this point.
        return True
        #TODO Return to this for implementing duration data.


    def GetCellsPerQrtrNote(self):
        return self._cells_per_qrtrnote


    def ResetGridCellSizes(self):
        #noUpdates = wx.grid.GridUpdateLocker(self)

        #TODO Haven't touched spans in a while. Return to this when we deal with cellspans\stream durations.
        
        for y in range(self._table.GetNumberRows()):
            for x in range(self._table.GetNumberCols()):
                span,r,c = self.GetCellSize(x,y)

                #print("Here3")
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
        if state.ShiftDown() and not state.AltDown() and not state.ControlDown():
            if event.GetWheelRotation() >= 120:
                self.ZoomInVertical(1)
                return
            elif event.GetWheelRotation() <= -120:
                self.ZoomOutVertical(1)
        elif state.AltDown() and not state.ShiftDown() and not state.ControlDown():   #CHANGED FROM ControlDown to avoid conflicting with other scrolling function(s).
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
            #print("Appending additional columns.")
            self.AppendCols(matrix.shape[0] - self.GetNumberCols())

        noUpdates = wx.grid.GridUpdateLocker(self)

        for x in range(0, matrix.shape[0]):
            for y in range(0, matrix.shape[1]):
                self._table.SetValue(y, x, str(matrix[x][y]))

        self.UpdateStream()
        print("IS THIS USED?!?!?!??!?")

    def OnCellSelected(self, evt):

        #self.log.info("onCellSelected():")
        #self.SetCellValue(evt.Row, evt.Col, "1")

        #self.DeselectCell(evt.GetRow(), evt.GetCol())
        evt.Skip()


    def OnGridLClick(self, evt):
        #TODO DOC, relearn, and clean this sh*t up. 12/03/2021

        z = self.GetTopLevelParent().pianorollpanel.currentZplane
        current_actor = self.m_v.CurrentActor()
        cpqn = self._cells_per_qrtrnote

        row = evt.GetRow()
        col = evt.GetCol()
        #self.log.info(f"OnGridLClick({col},{row}")
        #self.log.debug("  _table.GetValue(0,0) = {}".format(self._table.GetValue(0, 0)))
        #self.log.debug("  self.GetCellValue(0,0) = {}".format(self.GetCellValue(0,0)))

       # x = evt.GetRow()
        #y = evt.GetCol()
        if self._table.GetValue(row, col) == "1":

            #self.EraseCell(row, col)

            #print("ROW", row)
            #print("COL", col)
            #current_actor._array3D[int(row / cpqn), int(127-col), int(z)] = 0      #/ cpqn
            self.drawing = 0
        elif self._table.GetValue(row, col) == "0":
            #print("ROW", row)
            #print("COL", col)

            #self.DrawCell("1", row, col, 1, int(self.draw_cell_size))

            #current_actor._array3D[int(row * cpqn), int(127-col), int(z)] = 1
            self.drawing = 1

        evt.Skip()
        #After the drawing event, update the array_3d accordingly.
        #TODO FIGURE OUT--- DO I FRICKIN NEED THIS LINE OF CODE?
        #self.m_v.actors[self.m_v.cur_ActorIndex].array4Dchangedflag = not self.m_v.actors[self.m_v.cur_ActorIndex].array4Dchangedflag


        # on_points = np.argwhere(current_actor._array3D[row, col, z] >= 1.0)
        # print("On_Points", on_points)
        # for i in on_points:
        #     self._table.SetValue(127 - i[1], i[0], eval("self.drawing"))
        #
        # current_actor._array3D[:, :, z] = current_actor._array3D[:, :, z] * 0
        # self.ForceRefresh()
        # self.m_v.actors[self.m_v.cur_ActorIndex].array4Dchangedflag += 1
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
        self.SetCellValue(row, c, "0")

        self.SetCellSize(row, c, 1, 1)
        #self._table.SetValue(row, c, "0")

        #page = self.GetTopLevelParent().pianorollpanel.pianoroll



        ###TODO Be mindful of these ints when debugging.
        #zplane = self.GetTopLevelParent().pianorollpanel.currentZplane
        #self.m_v.CurrentActor()._array3D[int(c*self._cells_per_qrtrnote), 127 - row, zplane] = 0


    def DrawCell(self, val, row, col, new_sy, new_sx):
        #self.log.info(f"DrawCell():")
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

        #print(f"  {row},{col} = {val}")
        #Grid update
        #-----------
        self._table.SetValue(row, col, val)

        #self.SetCellValue(row, col/self._cells_per_qrtrnote, val)

        #print("X", x)
        #zplane = self.GetTopLevelParent().pianorollpanel.currentZplane

        #Mayavi update
        #------------
        #self.m_v.CurrentActor()._array3D[int(col / self._cells_per_qrtrnote)][127 - row][zplane] = int(val)


        #self.m_v.CurrentActor().array3Dchangedflag = not self.m_v.CurrentActor().array3Dchangedflag
        self.SetCellSize(row, col, new_sy, new_sx)

    ######

    #Error received when trying to draw outside the grid, sometimes.------
    #"""Traceback (most recent call last):
    #File "C:\Users\Isaac's\Midas\gui\PianoRoll.py", line 129, in GetValue
    #return str(int(self.pianorollpanel.GetTopLevelParent().mayavi_view.CurrentActor()._array3D[int(col)][127-row][z]))
    #IndexError: index 128 is out of bounds for axis 0 with size 128"""

    ######


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

        for c in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            if type(c) is music21.chord.Chord:
                for n in c.notes:  #was .pitches, changed 12/31/2021
                    x = int(self._cells_per_qrtrnote * c.offset)
                    y = 127 - n.pitch.ps  #was p.midi, changed 12/31/2021
                    size = int(self._cells_per_qrtrnote * c.duration.quarterLength)
                    if size < 1:
                        print("Chord: Note size is too small for current grid CellsPerQrtrNote(%s)." % self._cells_per_qrtrnote)
                    else:
                        self._table.SetValue(y, x, "1")
                        #ON
                        self.m_v.CurrentActor()._array4D[x, 127 - y, z][0] = 1
                        #VELOCITY
                        self.m_v.CurrentActor()._array4D[x, 127 - y, z][1] = n.volume.velocity \
                            if n.volume.velocity is not None else z   #self.m_v.CurrentActor().cur_z
                        #DURATION
                        self.m_v.CurrentActor()._array4D[x, 127-y, z][2] = \
                            n.duration.quarterLength.as_integer_ratio()[0]
                        self.m_v.CurrentActor()._array4D[x, 127-y, z][3] = \
                            n.duration.quarterLength.as_integer_ratio()[1]

                        #int(n.duration * 10000) #Must be int.
                        #SAD?
                        #self.m_v.CurrentActor()._array4D[x, 127 - y, z][4]
                        #self.SetCellSize(y, x, 1, size)     #TODO Code in workaround for cells already part of another cell.

                # print(matrix)
            elif type(c) is music21.note.Note:
                n = c
                x = int(self._cells_per_qrtrnote * c.offset)
                y = 127 - c.pitch.midi

                size =  int(self._cells_per_qrtrnote * c.duration.quarterLength)

                if size < 1:  #TODO IS THIS THE CORRECT CALL?
                    print("Note: Note size is too small for current grid CellsPerNote.")

                else:
                    self._table.SetValue(y, x, "1")
                    #ON
                    self.m_v.CurrentActor()._array4D[x, 127 - y, z][0] = 1
                    #VELOCITY
                    self.m_v.CurrentActor()._array4D[x, 127 - y, z][1] = n.volume.velocity \
                        if n.volume.velocity is not None else z   #self.m_v.CurrentActor().cur_z
                    #DURATION
                    self.m_v.CurrentActor()._array4D[x, 127 - y, z][2] = n.duration.quarterLength.as_integer_ratio()[0]
                    self.m_v.CurrentActor()._array4D[x, 127 - y, z][3] = n.duration.quarterLength.as_integer_ratio()[1]
                    #int(n.duration.quarterLength * 10000) #Must be int.
                    #SAD?

                    self.SetCellSize(y, x, 1, size)

        # print(matrix)

        #self.m_v.CurrentActor().array4Dchangedflag += 1
        self.m_v.CurrentActor().array4Dchangedflag = not self.m_v.CurrentActor().array4Dchangedflag
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

        #TODO Keep an eye on this here line and lines like it. Has to do with correct data access for our new array4D.
        #TODO 08/18/2021
        #This works -- > ...array4D[:, :, self.m_v.cur_z, 0]
        #But this doesn't --> ...array4D[:, :, self.m_v.cur_z][0] Why? 08/18/2021

        on_points = self.m_v.CurrentActor().get_points_with_all_data(z=self.m_v.cur_z)
        #on_points = np.argwhere(self.m_v.CurrentActor()._array4D[:, :, self.m_v.cur_z, 0] >= 1.0)

        print("On_Points", on_points)
        for i in on_points:
            (span, sx, sy) = self.GetCellSize(i[1], i[0])
            #print("2")
            n = music21.note.Note()
            #print("A note:", n)
            #print("3")
            n.offset = i[0] / self._cells_per_qrtrnote
            n.pitch.midi = i[1]
            n.volume.velocity = i[2]
            ##n.volume.velocity = self.m_v.cur_z  ##Pretty sure this was temporary.
            n.duration.quarterLength = i[3]/i[4]    #i[3]/10000
            # n.duration.quarterLength = \
            #     sy/self._cells_per_qrtrnote  #This should be == self.draw_cell_size / self._cells_per_qrtrnote
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
        #self.m_v.CurrentActor().array4Dchangedflag += 1  #TODO Change to 'not' method?
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
        self.right_click_state = wx.GetMouseState()
        #pos = state.GetPosition()


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
            self.Bind(wx.EVT_MENU, self.OnPopup_ScrollHere, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopup_ScrollHome, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
            #self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
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
        menu.Append(self.popupID2, "Scroll Here")
        menu.Append(self.popupID3, "Scroll Home")
        menu.Append(self.popupID4, "Four")
        menu.Append(self.popupID5, "Five")
        menu.Append(self.popupID6, "Six")
        # make a submenu
        sm = wx.Menu()
        menu.Append(self.popupID7, "Set Scroll Rate...", sm)
        sm.Append(self.popupID8, "...To (1,1)")
        sm.Append(self.popupID9, "...To Default (160, 120)")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def OnPopup_Properties(self, event):
        pass

    def OnPopup_ScrollHere(self, event):
        self.ZoomToHere(state=self.right_click_state)


        pass

    def OnPopup_ScrollHome(self, event):
        self.ScrollHome()

    def OnPopupFour(self, event):
        pass

    def OnPopupFive(self, event):
        pass

    def OnPopupSix(self, event):
        pass
        # # Deletes 'selected' not 'activated' actors.
        # alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
        # print("J_list", [j for j in range(len(self.mayavi_view.actors), -1, -1)])
        # for j in range(len(self.mayavi_view.actors), 0, -1):  # Stupid OBOE errors...
        #     print("J", j)
        #     if alb.IsSelected(j - 1):
        #         self.OnBtnDelActor(evt=None, cur=j - 1)
        #         print("Seletion %s Deleted." % (j - 1))
        # self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

    # def OnPopupSeven(self, event):
    #     pass

    def OnPopupEight(self, event):
        self.SetScrollRate(1, 1)


    def OnPopupNine(self, event):
        self.SetScrollRate(160, 120)

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
        self.parent = parent
       
    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        

        self.grid_highlight_color = "LIGHT BLUE"

        if len(self.parent.GetTopLevelParent().mayavi_view.actors) == 0:
            self.current_cells_color = "BLACK"
        else:
            m_v_actor = self.parent.GetTopLevelParent().mayavi_view.CurrentActor()
            self.current_cells_color = (m_v_actor.color[0]*255, m_v_actor.color[1]*255, m_v_actor.color[2]*255)

        value = grid.GetCellValue(row, col)
        #values = grid._table.Get

        ##NOTE: "value" is a string.
        # if value == "":
        #     dc.SetBrush(wx.Brush("WHITE", wx.BRUSHSTYLE_SOLID))
        try:

            if value == "1":
                dc.SetBrush(wx.Brush(self.current_cells_color, wx.BRUSHSTYLE_SOLID))
            elif int(value) == 2:
                #ValueError: invalid literal for int() with base 10: '' THIS is the error acquired when you try do draw without an actor.
                dc.SetBrush(wx.Brush(self.grid_highlight_color, wx.BRUSHSTYLE_SOLID))
            elif int(value) >= 3:
                dc.SetBrush(wx.Brush("GREEN", wx.BRUSHSTYLE_SOLID))
            else:
                dc.SetBrush(wx.Brush("WHITE", wx.BRUSHSTYLE_SOLID))
        except ValueError:
            print("Drawing in emptiness. TODO---scratch pad for drawing without actors on startup.")
            pass
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




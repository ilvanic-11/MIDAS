import  time
import  wx

RELATIVEWIDTHS = True

#---------------------------------------------------------------------------

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        self.SetForegroundColour(self.GetTopLevelParent().text_colour)
        self.SetFont(self.GetTopLevelParent().statusbar_font)
        self.SetOwnForegroundColour(self.GetTopLevelParent().text_colour)

        # This status bar has three fields
        self.SetFieldsCount(3)
        if RELATIVEWIDTHS:
            # Sets the three fields to be relative widths to each other.
            self.SetStatusWidths([-8, -5, -8])
        else:
            self.SetStatusWidths([-2, 90, 140])
        #self.log = log
        self.sizeChanged = False
        ##self.Bind(wx.EVT_SIZE, self.OnSize)
        ##self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.status_text = wx.StaticText(self, -1, "The Midas Status Bar.", pos=(11,4))

        #self.SetStatusText(self.status_text, 0)

        #self.SetStatusStyles(styles=[wx.SB_RAISED, wx.SB_SUNKEN, wx.SB_FLAT])


        # This will fall into field 1 (the second field)
        self.last_musicode_text= wx.TextCtrl(self, -1, "Last Musicode Text Here", pos=(750, 2), size=(370, 20),  #,♫♪♪♪♪♪♪♪♪♪Musicode Text Here♪♪♪♪♪♪♪♪♫
                                    style=wx.TE_MULTILINE | wx.TE_CENTER, name="Current Text") #Musicode?
        #self.last_musicode_text.SetValue()

        self.last_musicode_text.SetFont(wx.Font())
        #self.last_musicode_text = wx.StaticText(self, 1001, "Last Musicode Text Here", pos=(770, 5))
        #self.last_musicode_text.SetSize()
        self.musicode_colour = wx.Colour(0, 150, 255)
        self.last_musicode_text.SetOwnForegroundColour(self.musicode_colour)
        # self.Bind(wx.EVT_CHECKBOX, self.OnToggleClock, self.cb)
        # self.cb.SetValue(True)

        # set the initial position of the checkbox
        ##self.Reposition()

        # We're going to use a timer to drive a 'clock' in the last field.

        try:
            from agw import pygauge as PG
        except ImportError:  # if it's not there locally, try the wxPython lib.
            try:
                import wx.lib.agw.pygauge as PG
            except:
                raise Exception("This demo requires wxPython version greater than 2.9.0.0")

        # self.gauge = PG.PyGauge(self, -1, range=12, pos=(1165,3), size=(550, 18), style=wx.GA_HORIZONTAL)   #size=(100,25),
        # self.gauge.SetBarColour(self.musicode_colour)
        # self.gauge.SetBorderColour(wx.BLACK)
        # self.gauge.SetBorderPadding(2)

        #self.gauge.Update
        #self.gauge.SetValue
        self.gauge = wx.Gauge(self, -1, range=12, pos=(1200,3), size=(550, 18), name="MidasProgressGauge")
        #self.gauge.SetOwnForegroundColour(self.musicode_colour)
        #self.gauge.SetOwnBackgroundColour(self.musicode_colour)
        #self.gauge.
        self.gauge.UseForegroundColour()

        #self.gauge.
        # self.timer = wx.PyTimer(self.Notify)
        # self.timer.Start(1000)
        # self.Notify()




    # Handles events from the timer we started in __init__().
    # We're using it to drive a 'clock' in field 2 (the third field).
    # def Notify(self):
    #     t = time.localtime(time.time())
    #     st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
    #     self.SetStatusText(st, 2)
        #self.log.WriteText("tick...\n")


    ## the checkbox was clicked
    # def OnToggleClock(self, event):
    #     if self.cb.GetValue():
    #         self.timer.Start(1000)
    #         self.Notify()
    #     else:
    #         self.timer.Stop()


    # def OnSize(self, evt):
    #     evt.Skip()
    #     self.Reposition()  # for normal size events
    #
    #     # Set a flag so the idle time handler will also do the repositioning.
    #     # It is done this way to get around a buglet where GetFieldRect is not
    #     # accurate during the EVT_SIZE resulting from a frame maximize.
    #     self.sizeChanged = True


    # def OnIdle(self, evt):
    #     if self.sizeChanged:
    #         self.Reposition()


    # reposition the checkbox
    # def Reposition(self):
    #     rect = self.GetFieldRect(1)
    #     rect.x += 1
    #     rect.y += 1
    #     self.cb.SetRect(rect)
    #     self.sizeChanged = False
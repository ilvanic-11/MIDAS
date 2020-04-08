import wx
import wx.lib.plot
import music21
import numpy as np
import math
from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray



class ActorsControlPanel(wx.Panel):
	def __init__(self, parent, log):
		# HasTraits.__init__(self)
		wx.Panel.__init__(self, parent, -1)
		self.log = log

		#self.ZPlanesListBox = wx.ListBox(self, -1, name="ZPlanesListBox")

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.basesplit, 1, wx.EXPAND)
		self.mainpanel.SetSizerAndFit(sizer)


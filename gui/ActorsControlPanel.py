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
		wx.Panel.__init__(self, parent, -1)
		self.log = log


		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.basesplit, 1, wx.EXPAND)
		self.SetSizerAndFit(sizer)
	
	def SetupToolBar(self):
		btn_size = (8, 8)
		self.toolbar.SetToolBitmapSize(btn_size)
		
		bmp_showall = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, btn_size)
		
		id_showall = 10
		self.toolbar.AddCheckTool(id_showall, "Select", bmp_showall, wx.NullBitmap, "Show All?",
		                          "Toggle between showing ", None)
		self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_showall)
		
		
		self.toolbar.Realize()
	
	def OnToolBarClick(self, event):
		"""
        Event handler for when user clicks a button on the toolbar.
        Determines which button was called and calls sub-handler functions
        :return:
        """
		print("OnToolBarClick():")
		if event.GetId() == 10:
			self.OnBtn(event)
		else:
			pass
	
	def OnBtn(self, event):
		pass


class CustomActorsListBox(wx.ListCtrl):
	def __init__(self, parent, log):
		wx.ListCtrl.__init__(self, parent, -1,
		                     style=wx.LC_REPORT
		                           #wx.LC_VIRTUAL |
		                           # wx.LC_NO_HEADER |
		                           # wx.LC_SINGLE_SEL
		                     )

		self.log = log
		
		self.InsertColumn(0,"Visible", wx.LIST_FORMAT_CENTER, width=40)
		self.InsertColumn(1, "Actor", wx.LIST_FORMAT_CENTER, width=64)

		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActorsListItemActivated)
	
	def OnActorsListItemActivated(self, evt):
		self.log.info("OnListItemActivated():")
		print(f"evt.Index = {evt.Index}")
		self.GetTopLevelParent().mayavi_view.cur = evt.Index
		self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()
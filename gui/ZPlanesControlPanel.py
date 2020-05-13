import wx
import wx.lib.plot
import music21
import numpy as np
import math
from midas_scripts import midiart3D
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from midas_scripts import musicode, music21funcs
from gui import PianoRoll
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray



class ZPlanesControlPanel(wx.Panel):
	def __init__(self, parent, log):
		wx.Panel.__init__(self, parent, -1)
		self.log = log

		self.ZPlanesListBox = CustomZPlanesListBox(self,log)
		self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
		self.SetupToolBar()
		
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar)
		sizer.Add(self.ZPlanesListBox, 1, wx.EXPAND)
		self.SetSizerAndFit(sizer)
		
		
	def SetupToolBar(self):
		btn_size = (8, 8)
		self.toolbar.SetToolBitmapSize(btn_size)
		
		bmp_showall = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, btn_size)
		
		id_showall = 10
		self.toolbar.AddCheckTool(id_showall, "ShowAll", bmp_showall, wx.NullBitmap, "Show All?",
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
			self.OnBtnShowAll(event)
		else:
			pass
	
	def OnBtnShowAll(self, event):
		"""
		TO show all planes in the listbox
		:param event:
		:return:
		"""
		self.ZPlanesListBox.showall = not(self.ZPlanesListBox.showall)
		self.ZPlanesListBox.UpdateFilter()
		
	
	
class CustomZPlanesListBox(wx.ListCtrl, CheckListCtrlMixin):
	def __init__(self, parent, log):
		wx.ListCtrl.__init__(self, parent, -1,
		                     style=wx.LC_REPORT |
		                            wx.LC_VIRTUAL |
		                            #wx.LC_NO_HEADER |
		                            wx.LC_SINGLE_SEL
		                     )
		CheckListCtrlMixin.__init__(self)
		self.log = log

		self.SetBackgroundColour((141, 141, 141))


		self.InsertColumn(0,"Visible", wx.LIST_FORMAT_CENTER, width=50)
		self.InsertColumn(1,"ZPlane", wx.LIST_FORMAT_CENTER, width=64)
		
		
		self.showall = False
		
		self.filter = list()
		self.SetItemCount(0)
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
		
	def OnListItemActivated(self, evt):
		self.log.info("OnListItemActivated():")
		# Change current zplane
		
		print(f"evt.Index = {evt.Index}, zplane = {self.filter[evt.Index]}")
		self.GetTopLevelParent().pianorollpanel.currentZplane = self.filter[evt.Index]
		self.GetTopLevelParent().mayavi_view.cur_z = self.filter[evt.Index]
		self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()
	
	def OnGetItemText(self, item, column):
		if column == 0:
			return f"{self.filter[item]}"
		else:
			return ""
		
	def OnGetItemImage(self, item):
		return item
		
	def GetItemCount(self, count):
		self.log.debug(f" GetItemCount(): itemcount = {len(self.filter)}")
		return len(self.filter)
		
		
	def UpdateFilter(self):
		self.log.info("UpdateFilter():")
		a3D = self.GetTopLevelParent().mayavi_view.CurrentActor()._array3D
		#print(np.shape(a3D))
		
		self.filter = list()
		if self.showall:
			self.filter = [ _ for _ in range(128) ]
		else:
			for i in range(np.shape(a3D)[2]):
				if np.count_nonzero(a3D[:,:,i]) > 0:
					self.filter.append(i)
		
		#print(f"filter = {self.filter}")
		
		self.SetItemCount(len(self.filter))
		self.Refresh()
		return len(self.filter)
		
		
	
	
	
	
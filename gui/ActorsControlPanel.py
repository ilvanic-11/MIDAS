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

		self.actorsListBox = CustomActorsListBox(self, log)
		self.mayavi_view = self.GetTopLevelParent().mayavi_view
		self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
		self.SetupToolBar()
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toolbar)
		sizer.Add(self.actorsListBox, 1, wx.EXPAND)
		self.SetSizerAndFit(sizer)
	
	def SetupToolBar(self):
		btn_size = (8, 8)
		self.toolbar.SetToolBitmapSize(btn_size)
		
		bmp_showall = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, btn_size)
		bmp_newactor = wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, btn_size)
		bmp_delactor = wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR, btn_size)
		
		id_showall = 10
		id_newactor = 20
		id_delactor = 30
		
		self.toolbar.AddTool(id_showall, "ShowAll", bmp_showall,
		                          shortHelp="Toggle all Actors' visibility", kind=wx.ITEM_CHECK)
		self.toolbar.AddTool(id_newactor, "New Actor", bmp_newactor,
		                        shortHelp="Add New Actor", kind=wx.ITEM_NORMAL)
		self.toolbar.AddTool(id_delactor, "Delete Actor", bmp_delactor,
		                        shortHelp="Delete Selected Actor", kind=wx.ITEM_NORMAL)
		
		
		self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_showall)
		self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_newactor)
		self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delactor)
		
		self.toolbar.Realize()
	
	
	def OnToolBarClick(self, event):
		"""
        Event handler for when user clicks a button on the toolbar.
        Determines which button was called and calls sub-handler functions
        :return:
        """
		print("OnToolBarClick():")
		if event.GetId() == 10:
			self.OnBtnToggleAll(event)
		elif event.GetId() == 20:
			self.OnBtnNewActor(event)
		elif event.GetId() == 30:
			self.OnBtnDelActor(event)
		else:
			pass
	
	def OnBtnToggleAll(self, event):
		"""
        TO show all planes in the listbox
        :param event:
        :return:
        """
		self.actorsListBox.showall = not (self.actorsListBox.showall)
		
	
	def OnBtnNewActor(self,evt):
		i = len(self.mayavi_view.actors)
		name = str(i)
		
		self.actorsListBox.new_actor(name, i)
		

	def OnBtnDelActor(self,evt):
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
		
		self.InsertColumn(0, "Visible", wx.LIST_FORMAT_CENTER, width=50)
		self.InsertColumn(1, "Actor", wx.LIST_FORMAT_CENTER, width=64)

		self.showall = True
		
		self.mayavi_view = self.GetTopLevelParent().mayavi_view
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActorsListItemActivated)
	
	def OnActorsListItemActivated(self, evt):
		self.log.info("OnListItemActivated():")
		print(f"evt.Index = {evt.Index}")
		self.mayavi_view.cur = evt.Index
		self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()
	
	def new_actor(self, name, i):
		self.log.info(f"new_actor() {name} {i}")
		self.mayavi_view.append_actor(name, (1,0,0))
		self.InsertItem( i, name)
		self.mayavi_view.cur = i

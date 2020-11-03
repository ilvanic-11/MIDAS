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

		self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnZplaneRightClick)
		
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

	###POPUP MENU Function (keep this at bottom of class)
	# --------------------------------------
	def OnZplaneRightClick(self, evt):
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
			self.Bind(wx.EVT_MENU, self.OnClearSelection, id=self.popupID6)
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
		menu.Append(self.popupID6, "Clear Selection")
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

	def OnClearSelection(self, event):
		pass
		# Deletes 'selected' not 'activated' actors.
		# alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
		# print("J_list", [j for j in range(len(self.mayavi_view.actors), -1, -1)])
		# for j in range(len(self.mayavi_view.actors), 0, -1):  # Fucking OBOE errors...
		# 	print("J", j)
		# 	if alb.IsSelected(j - 1):
		# 		self.OnBtnDelActor(evt=None, cur=j - 1)
		# 		print("Seletion %s Deleted." % (j - 1))
		# self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

	def OnPopupSeven(self, event):
		pass

	def OnPopupEight(self, event):
		pass

	def OnPopupNine(self, event):
		pass
	
class CustomZPlanesListBox(wx.ListCtrl, CheckListCtrlMixin):
	def __init__(self, parent, log):
		wx.ListCtrl.__init__(self, parent, -1,
		                     style=wx.LC_REPORT |
		                            wx.LC_VIRTUAL
		                            #wx.LC_NO_HEADER |
		                            #wx.LC_SINGLE_SEL  #TODO Turned this off to allow for interesting multi-select functions for zplanes.
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
		self.GetTopLevelParent().mayavi_view.CurrentActor().cur_z = self.filter[evt.Index]
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
		
		
	
	
	
	
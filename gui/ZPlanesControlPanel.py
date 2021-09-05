import wx
import wx.lib.plot
import numpy as np
from midas_scripts import midiart3D
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from midas_scripts import music21funcs    #musicode,
from gui.Playback import Player, Animator
import multiprocessing
import os

# import math
# import music21
# from gui import PianoRoll
# from traits.api import HasTraits, on_trait_change
# from traits.trait_numeric import AbstractArray
# from mayavi.tools import animator
# from gui.Preferences import InfiniteTimer   ###, Animator

class ZPlanesControlPanel(wx.Panel):
	def __init__(self, parent, log):
		wx.Panel.__init__(self, parent, -1)
		self.log = log

		self.ZPlanesListBox = CustomZPlanesListBox(self,log)
		self.toolbar = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, style=wx.TB_HORIZONTAL)
		self.SetupToolBar()

		self.m_v = self.GetTopLevelParent().mayavi_view

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
		self.toolbar.AddCheckTool(id_showall, "ShowAll", bmp_showall, wx.NullBitmap,
								  '''Toggle between \"All\" and \"Notes-Only\" Zplanes''',
		                          "???", None)  #???What's supposed to be here?
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
			self.Bind(wx.EVT_MENU, self.OnPlayback_Zplane, id=self.popupID2)
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
		menu.Append(self.popupID2, "Playback Zplane")
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



	def OnPlayback_Zplane(self, event):
		intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
		filename = "Temp_Midi" + "_" + "Z-" + str(self.m_v.CurrentActor().cur_z)
		output = intermediary_path + filename + ".mid"
		zplane = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points)[  # Todo use GridToStream()
			eval('self.m_v.cur_z')]  # TODO Watch for debug errors here.
		self.m_v.CurrentActor()._stream = midiart3D.extract_xyz_coordinates_to_stream(zplane)
		music21funcs.add_timesig_and_metronome(self.m_v.CurrentActor()._stream, bpm=self.m_v.bpm, timesig="4/4")
		self.m_v.CurrentActor()._stream.write('mid', output)
		def execute_animator():
			self.GetTopLevelParent().planescroll_animator = \
				Animator(0, self.m_v.generate_plane_scroll(x_length=self.m_v.grid3d_span,  # animator.
														   bpm=self.m_v.bpm,
														   frames_per_beat=self.m_v.frames_per_beat  ##/2
														   # delay=10,
														   ).__next__)
		def execute_player():
			self.GetTopLevelParent().player = Player(midifile=output, parent=self.GetTopLevelParent(), play_now=True, from_gui=True)

		try:
			#TODO This is multiprocessing, threading, parallelism stuff...help.
			##multiprocessing.Process(target=execute_animator).start()
			self.GetTopLevelParent().planescroll_animator = \
				Animator(0, self.m_v.generate_plane_scroll(x_length=self.m_v.grid3d_span,  # animator.
															bpm=self.m_v.bpm,
															frames_per_beat=self.m_v.frames_per_beat  ##/2
															# delay=10,
															).__next__)

			self.GetTopLevelParent().planescroll_animator._stop_fired()

			#self.GetTopLevelParent().planescroll_animator.timer._start_timer()
			#self.m_v.scene3d.render_window.make_current()

			# Midas.mayavi_view.generate_plane_scroll(x_length=(Midas.mayavi_view.grid3d_span-94)/4,
			# 														   bpm=Midas.mayavi_view.bpm,
			# 			 												frames_per_beat=Midas.mayavi_view.frames_per_beat)

			##multiprocessing.Process(target=execute_player).start()
			self.GetTopLevelParent().player = Player(midifile=output, parent=self.GetTopLevelParent(), play_now=True,
														from_gui=True)


			# for i in np.arange(0, 50, 1):
			#      Midas.mayavi_view.volume_slice.actor.actor.position = np.array([i, 0, 0])

			#self.GetTopLevelParent().planescroll_animator = self.m_v.animate(self.m_v.grid3d_span, self.m_v.bpm, self.m_v.frames_per_beat)
		except StopIteration:
			del(self.GetTopLevelParent().player)
		finally:   #Todo Process this, read the docs and Zach's book.

		#player.load_midifile(midifile=output, bpm=160)
		#player.open_gui()
		#player.load_midifile_and_open_gui()

			print("Gui created, midifile loaded...") #TODO Figure why I can never get here......
			#NOTE: The deleting of the midifile makes things mess up: it is also responsible for the (0xC0000409) error
			# try:
			# 	if os.path.isfile(output):
			# 		os.remove(output)
			# except:
			# 	pass

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


		self.m_v = self.GetTopLevelParent().mayavi_view


		self.InsertColumn(0,"Visible", wx.LIST_FORMAT_CENTER, width=50)
		self.InsertColumn(1,"ZPlane", wx.LIST_FORMAT_CENTER, width=64)  #1
		
		
		self.showall = False
		
		self.filter = list()

		self.SetItemCount(0)
		
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
		
	def OnListItemActivated(self, evt):
		print("EVENT INDEX", evt.Index)
		self.Activate_Zplane(evt.Index)


	def Activate_Zplane(self, index):
		self.prp = self.GetTopLevelParent().pianorollpanel
		temp_prev_z = self.m_v.CurrentActor().previous_z
		self.log.info("OnListItemActivated():")

		#Account for previous zplane in all zplane changes. Since we're changing zplanes within this function, previous = cur here.
		self.m_v.CurrentActor().previous_z = self.m_v.CurrentActor().cur_z



		#CPQN compensatory call.
		self.prp.pianoroll.AdjustCellsBasedOnCPQN(self.m_v.CurrentActor().previous_z, 1, self.m_v.CurrentActor().cpqn)

		# Change current zplane
		print(f"Index = {index}, zplane = {self.filter[index]}")
		self.prp.currentZplane = self.filter[index]
		self.m_v.cur_z = self.filter[index]
		self.m_v.CurrentActor().cur_z = self.filter[index]
		self.prp.pianoroll.ForceRefresh()

		# Condition check for returning to the immediately previous zplane.
		print("INDEX", index)
		print("PREV_Z", self.m_v.CurrentActor().previous_z)
		print("CPQN", self.m_v.CurrentActor().cpqn)

		#For whatever reason, this check had to be called at the end of this function.
		#A 'temp_prev_z' (ln 194) is stored as a local reference, since 'previous_z" is 'written to' in this function above (ln 198).
		if temp_prev_z == index:  # If our new == our previous:
			print("TRUE1")
			# 'index', because we haven't changed cur_z to index yet....
			# assert self.m_v.CurrentActor().previous_z == index, "Previous does not equal index."
			self.prp.pianoroll.AdjustCellsBasedOnCPQN(index, self.m_v.CurrentActor().cpqn, 1)
			print("TRUE2")
		else:
			pass


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
		a4D = self.GetTopLevelParent().mayavi_view.CurrentActor()._array4D
		#print(np.shape(a3D))
		
		self.filter = list()
		if self.showall:
			self.filter = [ _ for _ in range(128) ]
		else:
			for i in range(np.shape(a4D)[2]):
				if np.count_nonzero(a4D[:, :, i]) > 0:
					self.filter.append(i)
		
		#print(f"filter = {self.filter}")
		
		self.SetItemCount(len(self.filter))
		self.Refresh()
		return len(self.filter)
		
		
	#
	###---------------------
	#####----------------------------------
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
	
	
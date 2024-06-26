import wx
import wx.lib.plot
import numpy as np
from midas_scripts import midiart3D
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from midas_scripts import music21funcs    #musicode,
from gui.Playback import Player, Animator
import multiprocessing
import asyncio
import itertools
import more_itertools
import os
import time

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

		# mayavi_view reference
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
			self.Bind(wx.EVT_MENU, self.OnUpdateStream, id=self.popupID3)
			self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
			self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
			self.Bind(wx.EVT_MENU, self.OnClearSelection, id=self.popupID6)
			self.Bind(wx.EVT_MENU, self.OnPopupSeven, id=self.popupID7)
			self.Bind(wx.EVT_MENU, self.OnGoToFirstEmptyZplane, id=self.popupID8)
			self.Bind(wx.EVT_MENU, self.OnGoToNearestEmptyZplane, id=self.popupID9)

		# make a menu
		menu = wx.Menu()
		# Show how to put an icon in the menu
		item = wx.MenuItem(menu, self.popupID1, "Properties")
		# bmp = images.Smiles.GetBitmap()
		# item.SetBitmap(bmp)
		menu.Append(item)
		# add some other items
		menu.Append(self.popupID2, "Playback Zplane")
		menu.Append(self.popupID3, "Update Stream")
		menu.Append(self.popupID4, "Four")
		menu.Append(self.popupID5, "Five")
		menu.Append(self.popupID6, "Clear Selection")
		# make a submenu
		sm = wx.Menu()
		menu.Append(self.popupID7, "Go To...", sm)
		sm.Append(self.popupID8, "..First Empty Zplane")
		sm.Append(self.popupID9, "..Nearest Empty Zplane")

		# Popup the menu.  If an item is selected then its handler
		# will be called before PopupMenu returns.
		self.PopupMenu(menu)
		menu.Destroy()


	def OnPopup_Properties(self, event):
		pass


	def execute_animator(self):
		self.GetTopLevelParent().planescroll_animator = \
			Animator(0, self.m_v.generate_plane_scroll(x_length=self.m_v.grid3d_span,  # animator.
													   bpm=self.m_v.bpm,
													   frames_per_beat=self.m_v.frames_per_beat  ##/2
													   # delay=10,
													   ).__next__, window=self.m_v)


	def execute_player(self):
		self.GetTopLevelParent().player = Player(midifilepath=self.output,
												 parent=self.GetTopLevelParent(),
												 play_now=True,
												 from_gui=True)


	def OnPlayback_Zplane(self, event):

		intermediary_path = os.getcwd() + os.sep + "resources" + os.sep + "intermediary_path" + os.sep
		filename = "Temp_Midi" + "_" + "Z-" + str(self.m_v.CurrentActor().cur_z)
		self.output = intermediary_path + filename + ".mid"
		zplane = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points)[  # Todo use GridToStream()
			eval('self.m_v.cur_z')]  # TODO Watch for debug errors here.
		self.m_v.CurrentActor()._stream = midiart3D.extract_xyz_coordinates_to_stream(zplane, durations=True)
		music21funcs.add_timesig_and_metronome(self.m_v.CurrentActor()._stream, bpm=self.m_v.bpm, timesig="4/4")
		self.m_v.CurrentActor()._stream.write('mid', self.output)
		print("Playing back zplane....")


		try:

			#TODO This is multiprocessing, threading, parallelism stuff...help.

			# ass1 = multiprocessing.Process(target=self.execute_animator)
			# ass1.start()
			# ass3 = torch.multiprocessing.Process(target=self.execute_animator)
			# ass3.start()
			# print("ass1")

			# fps = (self.m_v.bpm * self.m_v.frames_per_beat) / 60
			# dbf = 1 / fps

			# SUPER IMPORTANT :USE SURFACE (self.volume_slice=False) FOR ALL RENDERING OF OUR PLANE SCROLL 01/17/2022
			self.m_v.reset_volume_slice(self.m_v.grid3d_span, volume_slice=False)  # if volume_slice is not None else None
			print("VOLUME_SLICE", self.m_v.volume_slice)

			self.GetTopLevelParent().planescroll_animator = \
				Animator(0,  self.m_v.generate_plane_scroll().__next__, window=self.GetTopLevelParent().mayavi_view, player=False) #2 #, timer_delay=dbf) #().__next__)# ,
				#Animator(0, self.m_v.generate_plane_scroll()) #().__next__)# ,
															#(x_length=self.m_v.grid3d_span,     #itertools.tee(   animator.
															#bpm=self.m_v.bpm,
															#frames_per_beat=self.m_v.frames_per_beat    ##/ 2
															#),  #, 1)[0]
															## delay=10, .__next__
			time.sleep(.5)
			print("Animator here...")
			self.GetTopLevelParent().planescroll_animator._stop_fired()


			#self.m_v.scene3d.disable_render = True
			#print("Render disabled?")
			#self.GetTopLevelParent().planescroll_animator.timer._start_timer()
			#self.m_v.scene3d.render_window.make_current()

			# Midas.mayavi_view.generate_plane_scroll(x_length=(Midas.mayavi_view.grid3d_span-94)/4,
			# 														   bpm=Midas.mayavi_view.bpm,
			# 			 												frames_per_beat=Midas.mayavi_view.frames_per_beat)

			# argh2 = multiprocessing.Process(target=self.execute_player)
			# argh2.start()
			# argh4 = torch.multiprocessing.Process(target=self.execute_player)
			# argh4.start()

			print("Output", self.output)
			self.GetTopLevelParent().player = Player(midifilepath=self.output, parent=self.GetTopLevelParent(), play_now=True,
														from_gui=True, player=True)
			print("Player here...?")

			# for i in np.arange(0, 50, 1):
			#      Midas.mayavi_view.volume_slice.actor.actor.position = np.array([i, 0, 0])
			#self.GetTopLevelParent().planescroll_animator = self.m_v.animate(self.m_v.grid3d_span, self.m_v.bpm, self.m_v.frames_per_beat)

		except StopIteration:
			del(self.GetTopLevelParent().player)
			print("Player deleted?")

		finally:   #Todo Process this, read the docs and Dan Bader's book.
			#Midas.mayavi_view.slice_edges.actor.actor.trait_set(position=np.array([i, 0, 0]))Midas.mayavi_view.slice_edges.actor.actor.trait_set(position=np.array([i, 0, 0]))self.m_v.scene3d.disable_render=False

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

	def OnUpdateStream(self, event):
		zlb = self.GetTopLevelParent().pianorollpanel.zplanesctrlpanel.ZPlanesListBox
		for i in range(0, zlb.GetItemCount(0)):    #This '0' int here in GetItemCount(0) is strange......
			if zlb.IsSelected(i):
				self.GetTopLevelParent().pianorollpanel.pianoroll.UpdateStream(update_actor=True, z_plane=i)


	def OnPopupFour(self, event):
		pass


	def OnPopupFive(self, event):
		pass

	def OnClearSelection(self, event):

		pass
		# Deletes 'selected' not 'activated' actors.
		# alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
		# print("J_list", [j for j in range(len(self.mayavi_view.actors), -1, -1)])
		# for j in range(len(self.mayavi_view.actors), 0, -1):  # Stupid OBOE errors...
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


	def OnGoToFirstEmptyZplane(self, event):
		assert self.m_v.CurrentActor()._points.size != 0, \
			print("Your actor has no points, so your zplane won't either.")
		z_dict = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points, ordered=True, array=True)
		list_1 = [i for i in z_dict.keys() if i.size != 0]
		list_1.sort()
		set_1 = set(list_1)
		list_2 = [i for i in range(0, 128, 1)]
		set_2 = set(list_2)
		zero_list = set_2.difference(set_1)
		zero_list = list(zero_list)
		zero_list.sort()
		print("Zero_list", zero_list)
		#TODO WTF is this? Relearn. 3/30/23
		if zero_list[0] == self.m_v.cur_z:
			pass
		else:
			self.ZPlanesListBox.Activate_Zplane(zero_list[0])
			self.GetTopLevelParent().zplane_scrolled = zero_list[0]


	def OnGoToNearestEmptyZplane(self, event):
		if self.m_v.CurrentActor()._points.size == 0:
			print("Your actor has no points, so your zplane won't either. As such, "
				  "all zplanes are empty and therefore all zplanes are 'nearest'...."
				  "initiating workaround----> Going to Zplane_90")

			self.ZPlanesListBox.Activate_Zplane(90)
			self.GetTopLevelParent().zplane_scrolled = 90
		else:
			z_dict = midiart3D.get_planes_on_axis(self.m_v.CurrentActor()._points, ordered=True, array=True)
			list_1 = [i for i in z_dict.keys() if i.size != 0]
			list_1.sort()
			set_1 = set(list_1)
			list_2 = [i for i in range(0, 128, 1)]
			set_2 = set(list_2)
			zero_list = set_2.difference(set_1)
			zero_list = list(zero_list)
			zero_list.sort()
			print("Zero_list", zero_list)
			a = min(zero_list, key=lambda x: abs(x - self.m_v.cur_z))
			print("Nearest_0", a)

			if a == self.m_v.cur_z:
				pass
			else:
				self.ZPlanesListBox.Activate_Zplane(a)
				self.GetTopLevelParent().zplane_scrolled = a


class CustomZPlanesListBox(wx.ListCtrl, CheckListCtrlMixin):
	def __init__(self, parent, log):
		wx.ListCtrl.__init__(self, parent, -1,
							 style=wx.LC_REPORT |
									wx.LC_VIRTUAL
									#wx.LC_NO_HEADER |
									#wx.LC_SINGLE_SEL  #TODO Turned this off to allow for interesting multi-select functions for zplanes.
							 )

		#TODO I turned this off as well; it gets rid of those weird unused check boxes in the list box. So far,
		# I haven't run into errors from disabling it. 11/29/2021
		#CheckListCtrlMixin.__init__(self)
		self.log = log

		self.SetBackgroundColour((141, 141, 141))

		# mayavi_view reference
		self.m_v = self.GetTopLevelParent().mayavi_view


		#self.InsertColumn(0,"Visible", wx.LIST_FORMAT_CENTER, width=50)
		self.InsertColumn(0,"ZPlane", wx.LIST_FORMAT_CENTER, width=64)  #1


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
		#A 'temp_prev_z'--temporary previous z-- (ln 194) is stored as a local reference, since 'previous_z" is 'written to' in this function above (ln 271).
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
		try:
			a4D = self.m_v.CurrentActor()._array4D
		except AttributeError:
			print("There are no actors yet.")
			pass
		#print(np.shape(a3D))

		self.filter = list()
		if self.showall:
			self.filter = [_ for _ in range(128)]
		else:
			for i in range(np.shape(a4D)[2]):
				if np.count_nonzero(a4D[:, :, i]) > 0:
					self.filter.append(i)

		#print(f"filter = {self.filter}")

		self.SetItemCount(len(self.filter))
		if self.GetTopLevelParent().zplane_scrolled > self.filter[-1]:
			self.GetTopLevelParent().zplane_scrolled = self.filter[-1]
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


		self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnTheMidasButtonDialog, id=new_id1)
		#self.Bind(wx.EVT_MENU, self.GetTopLevelParent().mainbuttonspanel.OnMusic21ConverterParseDialog, id=new_id1)
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


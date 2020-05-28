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
        bmp_delallactors = wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR, btn_size)


        id_showall = 10
        id_newactor = 20
        id_delactor = 30
        id_delallactors = 40


        self.toolbar.AddTool(id_showall, "ShowAll", bmp_showall,
                                  shortHelp="Toggle all Actors' visibility", kind=wx.ITEM_CHECK)
        self.toolbar.AddTool(id_newactor, "New Actor", bmp_newactor,
                                shortHelp="Add New Actor", kind=wx.ITEM_NORMAL)
        self.toolbar.AddTool(id_delactor, "Delete Actor", bmp_delactor,
                                shortHelp="Delete Current Actor", kind=wx.ITEM_NORMAL)
        self.toolbar.AddTool(id_delallactors, "Delete All Actors", bmp_delallactors,
                                shortHelp="Delete All Actors", kind=wx.ITEM_NORMAL)


        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_showall)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_newactor)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delactor)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delallactors)
        #RightClickSubmenu
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnActorRightClick)

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
        elif event.GetId() == 40:
            self.OnBtnDelAllActors(event)
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
        self.actorsListBox.new_actor(i)


    def OnBtnDelActor(self,evt):
        #TODO Make dynamic for all cases.
        #Note: These deletions delete by index, not by actor name.


        current = self.mayavi_view.cur_ActorIndex
        self.mayavi_view.cur_ActorIndex = current - 1

        #Remove from actorsListBox
        self.actorsListBox.DeleteItem(current)
        #Remove from scene(the mayavi pipeline)
        self.mayavi_view.sources[current].remove()
        #Remove from mlab_calls list
        self.mayavi_view.mlab_calls.remove(self.mayavi_view.sources[current])
        #Remove from source list
        self.mayavi_view.sources.remove(self.mayavi_view.sources[current])
        #Remove from actors list
        self.mayavi_view.actors.remove(self.mayavi_view.actors[current])

        # if len(self.mayavi_view.actors) != 0:
        # 	self.mayavi_view.cur = len(self.mayavi_view.actors) - 1
        #else:
            #self.mayavi_view.cur = -1#Condition for single actor case.
            #self.actorsListBox.new_actor("0", 0)


            #Clear Piano

    #TODO Bind to button.
    def OnBtnDelAllActors(self, evt):
        for j in range(0, len(self.mayavi_view.actors)):
            #This function deletes by index 0 the number of times of the loop's range, not by self.mayavi_view.cur.

            index_0 = 0

            self.actorsListBox.DeleteItem(index_0)
            # Remove from scene(the mayavi pipeline)
            self.mayavi_view.sources[index_0].remove()
            # Remove from mlab_calls list
            self.mayavi_view.mlab_calls.remove(self.mayavi_view.sources[index_0])
            # Remove from source list
            self.mayavi_view.sources.remove(self.mayavi_view.sources[index_0])
            # Remove from actors list
            self.mayavi_view.actors.remove(self.mayavi_view.actors[index_0])

    ###POPUP MENU Function (keep this at bottom of class)
    # --------------------------------------
    def OnActorRightClick(self, evt):
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
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)
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
        menu.Append(self.popupID6, "Six")
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

    def OnPopupSix(self, event):
        pass

    def OnPopupSeven(self, event):
        pass

    def OnPopupEight(self, event):
        pass

    def OnPopupNine(self, event):
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

        self.SetBackgroundColour((0, 0, 0))
        self.SetTextColour((191, 191, 191))

        self.InsertColumn(0, "Visible", wx.LIST_FORMAT_CENTER, width=50)
        self.InsertColumn(1, "Actor", wx.LIST_FORMAT_CENTER, width=64)

        self.showall = True

        self.mayavi_view = self.GetTopLevelParent().mayavi_view

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActorsListItemActivated)

    def OnActorsListItemActivated(self, evt):
        self.log.info("OnListItemActivated():")
        print(f"evt.Index = {evt.Index}")
        self.mayavi_view.cur = evt.Index
        self.mayavi_view.cur_z = self.mayavi_view.actors[evt.Index].cur_z
        self.mayavi_view.cur_changed_flag = not self.mayavi_view.cur_changed_flag
        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

    def new_actor(self, i, name = None):
        if name is None:
            name = str(i) + "_" + "Actor"
        self.log.info(f"new_actor() {name} {i}")
        self.mayavi_view.append_actor(name, (0, 1, 0))  #Subsequent actors red.
        self.InsertItem(i, name)


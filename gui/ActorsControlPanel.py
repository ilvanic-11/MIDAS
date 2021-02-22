import wx
import wx.lib.plot
import music21
import numpy as np
import math
from midas_scripts import music21funcs
from gui import PianoRoll
from traits.api import HasTraits, on_trait_change
from traits.trait_numeric import AbstractArray



class ActorsControlPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        self.actorsListBox = CustomActorsListBox(self, log)
        self.m_v = self.GetTopLevelParent().mayavi_view
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
        bmp_delemptyactors = wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, wx.ART_TOOLBAR, btn_size)


        id_showall = 10
        id_newactor = 20
        id_delactor = 30
        id_delallactors = 40
        id_delemptyactors = 50


        self.toolbar.AddTool(id_showall, "ShowAll", bmp_showall,
                                  shortHelp="Toggle all Actors' visibility", kind=wx.ITEM_CHECK)
        self.toolbar.AddTool(id_newactor, "New Actor", bmp_newactor,
                                shortHelp="Add New Actor", kind=wx.ITEM_NORMAL)
        self.toolbar.AddTool(id_delactor, "Delete Actor", bmp_delactor,
                                shortHelp="Delete Current Actor", kind=wx.ITEM_NORMAL)
        self.toolbar.AddTool(id_delallactors, "Delete All Actors", bmp_delallactors,
                                shortHelp="Delete All Actors", kind=wx.ITEM_NORMAL)
        self.toolbar.AddTool(id_delemptyactors, "Delete Empty Actors", bmp_delemptyactors,
                                        shortHelp="Delete Empty Actors", kind=wx.ITEM_NORMAL)


        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_showall)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_newactor)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delactor)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delallactors)
        self.Bind(wx.EVT_TOOL, self.OnToolBarClick, id=id_delemptyactors)
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
        elif event.GetId() == 50:
            self.OnBtnDelEmtpyActors(event)
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
        i = len(self.m_v.actors)
        self.actorsListBox.new_actor(i)


    def OnBtnDelActor(self, evt, cur=None):
        #TODO Make dynamic for all cases.
        #Note: These deletions delete by index, not by actor name.
        self.m_v.scene3d.disable_render=True

        current = self.m_v.cur_ActorIndex
        if cur is None:
            pass
        else:
            current = cur

        self.m_v.cur_ActorIndex = current - 1

        self.m_v.deleting_actor = self.m_v.actors[current].colors_instance

        #Remove from actorsListBox
        self.actorsListBox.DeleteItem(current)
        #Remove from scene(the mayavi pipeline)
        self.m_v.sources[current].parent.stop()
        self.m_v.sources[current].parent.remove()
        self.m_v.sources[current].parent.update()
        self.m_v.sources[current].parent.parent.stop()
        self.m_v.sources[current].parent.parent.remove()
        self.m_v.sources[current].parent.parent.update()
        self.m_v.sources[current].stop()
        self.m_v.sources[current].remove()
        self.m_v.sources[current].update_data()
        self.m_v.sources[current].update_pipeline()


        #Remove from mlab_calls list
        self.m_v.mlab_calls.remove(self.m_v.sources[current])
        #Remove from source list
        self.m_v.sources.remove(self.m_v.sources[current])


        #Remove from actors list
        self.m_v.actors.remove(self.m_v.actors[current])

        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()
        #self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.GetTopLevelParent().pianorollpanel.currentZplane)


        self.m_v.actor_deleted_flag = not self.m_v.actor_deleted_flag

        # if len(self.mayavi_view.actors) != 0:
        # 	self.mayavi_view.cur = len(self.mayavi_view.actors) - 1
        #else:
            #self.mayavi_view.cur = -1#Condition for single actor case.
            #self.actorsListBox.new_actor("0", 0)
            #Clear Piano
        self.m_v.scene3d.disable_render=False
        #self.mayavi_view.scene3d.mlab.draw(self.mayavi_view.scene3d.mlab.gcf())

    def OnBtnDelAllActors(self, evt):
        #self.mayavi_view.scene3d.disable_render=True
        for j in range(0, len(self.m_v.actors)):
            #This function deletes by index 0 the number of times of the loop's range, not by self.mayavi_view.cur.

            index_0 = 0

            self.actorsListBox.DeleteItem(index_0)
            # Remove from scene(the mayavi pipeline)
            self.m_v.sources[index_0].remove()
            # Remove from mlab_calls list
            self.m_v.mlab_calls.remove(self.m_v.sources[index_0])
            # Remove from source list
            self.m_v.sources.remove(self.m_v.sources[index_0])
            # Remove from actors list
            self.m_v.actors.remove(self.m_v.actors[index_0])

        self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.GetTopLevelParent().pianorollpanel.currentZplane)

        for j in self.GetTopLevelParent().menuBar.colors.GetMenuItems():
            self.GetTopLevelParent().menuBar.colors.Delete(j)
        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()
        #self.mayavi_view.scene3d.disable_render=False


    def OnBtnDelEmtpyActors(self, evt):
        #TODO Make a button?
        self.m_v.scene3d.disable_render=True

        empty_actors = [i.index for i in self.m_v.actors if i._points.size is 0]
        alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
        #for i in self.mayavi_view.actors:
        #print(empty_actors)
            #print(i._points)
        for j in empty_actors:
            alb.Select(j)
        self.OnDeleteSelection(event=None)
        self.m_v.scene3d.disable_render=False


            # if i.index == j:  #Compare check here works around the readjusting of actor indices.
            #     self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.OnBtnDelActor(evt=None, cur=j)


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
            self.Bind(wx.EVT_MENU, self.OnDeleteSelection, id=self.popupID6)
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
        menu.Append(self.popupID6, "Delete Selection")
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

    def OnDeleteSelection(self, event):
        #Deletes 'selected' not 'activated' actors.
        alb = self.GetTopLevelParent().pianorollpanel.actorsctrlpanel.actorsListBox
        #print("J_list", [j for j in range(len(self.mayavi_view.actors), -1, -1)])
        for j in range(len(self.m_v.actors), 0, -1):  #Fucking OBOE errors...
            print("J", j)
            if alb.IsSelected(j-1):
                #if j == self.mayavi_view.cur_ActorIndex:
                    #self.GetTopLevelParent().pianorollpanel.ClearZPlane(self.mayavi_view.cur_z)
                #else:
                    #pass
                self.OnBtnDelActor(evt=None, cur=j-1)
                print("Seletion %s Deleted." % (j-1))

        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()

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
        self.InsertColumn(1, "Actor", wx.LIST_FORMAT_CENTER, width=64)    #1

        self.showall = True

        self.m_v = self.GetTopLevelParent().mayavi_view

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnActorsListItemActivated)


    def OnActorsListItemActivated(self, evt):
        self.Activate_Actor(evt.Index)


    def Activate_Actor(self, index):
        self.log.info("OnListItemActivated():")
        print(f"Index = {index}")

        #Account for previous_ActorIndex in all cur_ActorIndex changes. Since we're changing within this function, previous = cur here.
        self.m_v.previous_ActorIndex = self.m_v.cur_ActorIndex


        self.m_v.cur_ActorIndex = index
        self.m_v.cur_z = self.m_v.actors[index].cur_z
        self.m_v.cur_changed_flag = not self.m_v.cur_changed_flag
        self.GetTopLevelParent().pianorollpanel.pianoroll.ForceRefresh()


    def new_actor(self, i, name = None):

        if name is None:
            name = str(i) + "_" + "Actor"
        self.log.info(f"new_actor() {name} {i}")
        self.InsertItem(i, name)                        #TODO Does the order of these matter? -10/8/20
        #TODO Double-triple check all this stuff.

        #TODO Account for noncolorscall deletion.
        #TODO Make palette calls consistent.
        if self.m_v.number_of_noncolorscall_actors > 16:
            color = self.m_v.default_color_palette[1]
            #SWAP HERE.
            color = tuple([color[2] / 255, color[1] / 255, color[0] / 255])     #TODO THIS explains the colors_dicts inversion bug.... 11/25/2020
            self.m_v.number_of_noncolorscall_actors = 1  # The count starts over.
        else:
            if i == 16:
                color = self.m_v.default_mayavi_palette[i]
                # SWAP HERE.
                color = tuple([color[2], color[1], color[0]])
            elif i > 16:
                color_index = 0
                color = self.m_v.default_mayavi_palette[color_index + 1]
                # SWAP HERE.
                color = tuple([color[2], color[1], color[0]])
            else:
                color = self.m_v.default_mayavi_palette[i + 1]
               #print("'i' HERE", i + 1)
                #SWAP HERE.
                color = tuple([color[2], color[1], color[0]])
        self.m_v.append_actor(name, color) #Subsequent actors selected from color_palette..
        self.m_v.number_of_noncolorscall_actors += 1

        #TODO Go by .number_of_noncolor_actors instead of i? ( for the colors)
        #TODO Differentiate between colors_calls new actors and 'normal' new actors?

        #self.mayavi_view.highlighter_transformation()


    ###F Hotkeys for this panel.
    ####-----------------------------------------
    ###########-----------------------------------------
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
import wx
import music21
import inspect
from midas_scripts import midiart, midiart3D, musicode, music21funcs
from midas_scripts.musicode import *
from midas_scripts.midiart import *
from midas_scripts.midiart3D import *
from midas_scripts.music21funcs import *

##Patch Imports
#Wx bug


from pyface.util import fix_introspect_bug
#VTK 9.0.1 and Mayavi 4.7.2 updates
from tvtk.pyface.ui.wx import decorated_scene
from traitsui.wx import tree_editor
from traitsui.wx import helper
from traitsui.wx import file_editor
from pyface.ui.wx.action import menu_manager



class PreferencesDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='MIDI Art 3D'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.comboCtrl = wx.ComboCtrl(self, wx.ID_ANY, "", (20, 20))

        self.static_color = self.name_static = wx.StaticText(self, -1, "Current Color Palette")


        self.popupCtrl = ListCtrlComboPopup()

        # It is important to call SetPopupControl() as soon as possible
        self.comboCtrl.SetPopupControl(self.popupCtrl)

        # Populate using wx.ListView methods (populated with colors)
        for clrs in midiart.get_color_palettes():
            self.popupCtrl.AddItem(clrs)
        #One more call for FL Colors:
        self.popupCtrl.AddItem("FLStudioColors")

            #self.popupCtrl.InsertItem(popupCtrl.GetItemCount(), clrs)
        # self.popupCtrl.AddItem("Second Item")
        # self.popupCtrl.AddItem("Third Item")


        #self.chBox = wx.CheckBox(self, -1, "Create Musicode")
        self.span_statictxt = wx.StaticText(self, -1, "Grid-3D Span", style=wx.ALIGN_LEFT)
        self.input_span = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        self.bpm_statictxt = wx.StaticText(self, -1, "BPM", style=wx.ALIGN_LEFT)
        self.input_bpm = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        self.i_div_statictxt = wx.StaticText(self, -1, "i_div", style=wx.ALIGN_LEFT)
        self.input_i_div = wx.TextCtrl(self, -1, "", size=(30, -1), style=wx.TE_CENTER)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        topsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer.Add(self.span_statictxt, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        topsizer.Add(self.input_span, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        topsizer.Add(self.bpm_statictxt, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        topsizer.Add(self.input_bpm, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        topsizer.Add(self.i_div_statictxt, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        topsizer.Add(self.input_i_div, 0, wx.ALL | wx.ALIGN_CENTER, 20)

        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.static_color, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(self.comboCtrl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(topsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 1)
        print("PENIS")
        self.SetSizerAndFit(sizerMain)


#Taken straight from the docs.  See -->https://wxpython.org/Phoenix/docs/html/wx.ComboCtrl.html#wx-comboctrl
class ListCtrlComboPopup(wx.ComboPopup):
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None

    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.value = self.curitem
        self.Dismiss()


    # The following methods are those that are overridable from the
    # ComboPopup base class.  Most of them are not required, but all
    # are shown here for demonstration purposes.

    # This is called immediately after construction finishes.  You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.value = -1
        self.curitem = -1

    # Create the popup child control.  Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent, style=wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        idx = self.lc.FindItem(-1, val)
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.value >= 0:
            return self.lc.GetItemText(self.value)
        return ""

    # Called immediately after the popup is shown
    def OnPopup(self):
        wx.ComboPopup.OnPopup(self)

    # Called when popup is dismissed
    def OnDismiss(self):
        wx.ComboPopup.OnDismiss(self)

    # This is called to custom paint in the combo control itself
    # (ie. not the popup).  Default implementation draws value as
    # string.
    def PaintComboControl(self, dc, rect):
        wx.ComboPopup.PaintComboControl(self, dc, rect)

    # Receives key events from the parent ComboCtrl.  Events not
    # handled should be skipped, as usual.
    def OnComboKeyEvent(self, event):
        wx.ComboPopup.OnComboKeyEvent(self, event)

    # Implement if you need to support special action when user
    # double-clicks on the parent wxComboCtrl.
    def OnComboDoubleClick(self):
        wx.ComboPopup.OnComboDoubleClick(self)

    # Return final size of popup. Called on every popup, just prior to OnPopup.
    # minWidth = preferred minimum width for window
    # prefHeight = preferred height. Only applies if > 0,
    # maxHeight = max height for window, as limited by screen size
    #   and should only be rounded down, if necessary.
    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth, prefHeight, maxHeight)

    # Return true if you want delay the call to Create until the popup
    # is shown for the first time. It is more efficient, but note that
    # it is often more convenient to have the control created
    # immediately.
    # Default returns false.
    def LazyCreate(self):
        return wx.ComboPopup.LazyCreate(self)

class ToolsDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE, name='Midas Tool'):
        wx.Dialog.__init__(self)
        self.Create(parent, id, title, pos, size, style, name)

        self.func_id = 0

        #self.ass = wx.StaticText(self, -1, "ASS ASS ASS ASS")

        #self.funcname = wx.StaticText(self, -1, str(self.GetParent().FindItemById(self.func_id).GetName()))



        #eval("midiart." + "%s" % "array_to_lists_of")
        #[j for j in inspect.getfullargspec(midiart.array_to_lists_of)][0]

        #[j for j in inspect.getfullargspec(eval("midiart." + "%s" % "array_to_lists_of"))][0]

    def _generate_layout(self, event_id):
        self.func_id = event_id
        print("Gen_ID", self.func_id)
        self.func_name = str(super().GetParent().GetTopLevelParent().menuBar.FindItemById(self.func_id).GetItemLabelText())
        print("Gen_func_name", self.func_name)
        #self.musicode_workaround = super().GetParent().GetTopLevelParent().musicode
        #print("Gen_mc_func_name:", self.musicode_workaround)
        try:
            self.func_module = inspect.getmodule(eval(self.func_name))
        except NameError:
            self.func_module = super().GetParent().GetTopLevelParent().musicode
        #self.func_class = inspect.getmodule(eval(self))
        print("Gen_func_module", self.func_module)
        self.func_txt = wx.StaticText(self, -1, self.func_name)
        self.sizerMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerHorizontal = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerHorizontal.Add(self.func_txt, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        #self.sizerMain.Add(self.ass, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 20)
        #print(eval("self.func_module.translate"))
        print("self.func_module" + '.' + "%s" % self.func_name)
        for argskwargs in [j for j in inspect.getfullargspec(eval(str("self.func_module" + '.' + "%s" % self.func_name)))][0]:
            argSizer = wx.BoxSizer(wx.VERTICAL)
            argkwargname = wx.StaticText(self, 0, argskwargs)
            argkwarginput = wx.TextCtrl(self, 0, argskwargs, size=(70, -1), style=wx.ALIGN_CENTER, name=argskwargs)
            argSizer.Add(argkwargname, 0, wx.ALL | wx.ALIGN_CENTER, 20)
            argSizer.Add(argkwarginput, 0, wx.ALL | wx.ALIGN_CENTER, 20)
            self.sizerHorizontal.Add(argSizer)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.sizerMain.Add(self.sizerHorizontal)
        self.sizerMain.Add(btnsizer, 0, wx.ALL | wx.ALIGN_CENTER, 20)
        self.SetSizerAndFit(self.sizerMain)


#####PATCHES
###########################################
#################################################################
#Attribute autocomplete function rewrite.
def getAllAttributeNames(object):
    """Return dict of all attributes, including inherited, for an object.

    Recursively walk through a class and all base classes.
    """
    attrdict = {}  # (object, technique, count): [list of attributes]
    # !!!
    # Do Not use hasattr() as a test anywhere in this function,
    # because it is unreliable with remote objects: xmlrpc, soap, etc.
    # They always return true for hasattr().
    # !!!
    try:
        # This could(?) fail if the type is poorly defined without
        # even a name.
        key = type(object).__name__
    except:
        key = 'anonymous'
    # Wake up sleepy objects - a hack for ZODB objects in "ghost" state.
    wakeupcall = dir(object)
    del wakeupcall
    # Get attributes available through the normal convention.
    attributes = dir(object)
    attrdict[(key, 'dir', len(attributes))] = attributes
    # Get attributes from the object's dictionary, if it has one.
    try:
        attributes = list(object.__dict__.keys())
        attributes.sort()
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        attrdict[(key, '__dict__', len(attributes))] = attributes
    # For a class instance, get the attributes for the class.
    try:
        klass = object.__class__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if klass is object:
            # Break a circular reference. This happens with extension
            # classes.
            pass
        else:
            attrdict.update(getAllAttributeNames(klass))
    # Also get attributes from any and all parent classes.
    try:
        bases = object.__bases__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if isinstance(bases, tuple):
            for base in bases:
                if type(base) is type:
                    # Break a circular reference. Happens in Python 2.2.
                    pass
                else:
                    attrdict.update(getAllAttributeNames(base))
    return attrdict

def _background_changed(self, value):
    # Depending on the background, this sets the axes text and
    # outline color to something that should be visible.
    axes = self.axes
    if (self._vtk_control is not None) and (axes is not None):
        p = self.axes.x_axis_caption_actor2d.caption_text_property
        m = self.marker
        s = value[0] + value[1] + value[2]
        if s <= 1.0:
            p.color = (1,1,1)
            #BUGm.set_outline_color(1,1,1)
            m.outline_color = (1,1,1)
        else:
            p.color = (0,0,0)
            #BUG m.set_outline_color(0,0,0)
            m.outline_color = (0,0,0)
        self.render()

def restore_window(ui, is_popup=False):
    """ Restores the user preference items for a specified UI.
    """
    prefs = ui.restore_prefs()
    #MIDAS PATCH
    x, y = (1176, 852)
    if prefs is not None and prefs == 2:
        print("Prefs:", prefs)
        x, y, dx, dy = (tuple(prefs) + tuple([0]) + tuple([0]))
    elif prefs is not None and len(prefs) == 4:
        x, y, dx, dy = (tuple(prefs))
    elif prefs is None:
        is_popup = True
        x, y, dx, dy = x, y, 0, 0

        # Check to see if the window's position is within a display.
        # If it is not entirely within 1 display, move it and/or
        # resize it to the closest window

        closest = helper.find_closest_display(x, y)
        x, y, dx, dy = helper.get_position_for_display(x, y, dx, dy, closest)

        if is_popup:
            helper.position_window(ui.control, dx, dy)
        else:
            if (dx, dy) == (0, 0):
                # The window was saved minimized
                ui.control.SetSize(x, y, -1, -1)
            else:
                ui.control.SetSize(x, y, dx, dy)

def add_to_menu(self, parent, menu, controller):
    """ Adds the item to a menu. """

    #Patch Method
    # import inspect
    # print("SUB TYPE:", type(sub))
    # for j in inspect.getmembers(sub):
    #     # if inspect.isfunction(j):
    #     print("SUB-->", j[0], "  ", j[1])

    sub = self.create_menu(parent, controller)

    #BUG id = sub.GetId()

    #FIX
    id = wx.NewIdRef()

    # fixme: Nasty hack to allow enabling/disabling of menus.
    sub._id = id
    sub._menu = menu

    menu.Append(id, self.name, sub)

def _is_pasteable(self, object):
    from pyface.clipboard import clipboard

    return self._menu_node.can_add(object, clipboard.object_type)

def init_1(self, parent):
    """ Finishes initializing the editor by creating the underlying toolkit
        widget.
    """
    self.control = panel = helper.TraitsUIPanel(parent, -1)
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    factory = self.factory

    if factory.entries > 0:
        from traitsui.wx.history_control import HistoryControl

        self.history = HistoryControl(
            entries=factory.entries, auto_set=factory.auto_set
        )
        control = self.history.create_control(panel)
        pad = 3
        button = wx.Button(panel, -1, "...", size=wx.Size(28, -1))
    else:
        if factory.enter_set:
            control = wx.TextCtrl(panel, -1, "", style=wx.TE_PROCESS_ENTER)
            panel.Bind(wx.EVT_TEXT_ENTER, self.update_object, id=control.GetId())
        else:
            control = wx.TextCtrl(panel, -1, "")

        control.Bind(wx.EVT_KILL_FOCUS, self.update_object)

        if factory.auto_set:
            panel.Bind(wx.EVT_TEXT, self.update_object, id=control.GetId())

        bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, size=(15, 15))
        button = wx.BitmapButton(panel, -1, bitmap=bmp)

        pad = 8

    self._file_name = control
    sizer.Add(control, 1, wx.EXPAND)   #MIDAS bug fix
    sizer.Add(button, 0, wx.LEFT, pad)
    panel.Bind(wx.EVT_BUTTON, self.show_file_dialog, id=button.GetId())
    panel.SetDropTarget(file_editor.FileDropTarget(self))
    panel.SetSizerAndFit(sizer)
    self._button = button

    self.set_tooltip(control)


#Method overwrite.
#Permanent fix to the broken attribute auto-complete bug for our pycrust.

#####PATCHES######## (for wx(4.0.7)
fix_introspect_bug.getAllAttributeNames = getAllAttributeNames

#Method bug.
decorated_scene.DecoratedScene._background_changed = _background_changed
#Window coords restorating bug.
helper.restore_window = restore_window
#Right click menu bug.
menu_manager.MenuManager.add_to_menu = add_to_menu
tree_editor.SimpleEditor._is_pasteable = _is_pasteable

#for wx(4.1.0)
#wx error over alignment flags that are now irrelevant and throw an error. (i.e. wx.ALL | ALIGN_CENTER_RIGHT)
file_editor.SimpleEditor.init = init_1

import inspect
import types
from midas_scripts.midiart import *
from midas_scripts.midiart3D import *

##Patch Imports
#Wx bug
###---Note---> Most of these patches are GUI-related bugs.

from pyface.util import fix_introspect_bug
from tvtk.pyface.ui.wx import decorated_scene
from traitsui.wx import tree_editor
from traitsui.wx import helper
from traitsui.wx import file_editor
from pyface.ui.wx.action import menu_manager
import threading
from traits.api import Any, HasTraits, Button, Instance, Range
from traitsui.api import View, Group, Item

from wx import Timer as wxTimer
from pyo.lib._widgets import *
#from pyo.lib._widgets import createServerGUI
from pyface.timer.api import Timer  #GARBAGE TIMER
from mayavi.tools import animator
from multiprocessing import Process, Event


# import wx
# import pyo
# import music21
#VTK 9.0.1 and Mayavi 4.7.2 updates
#from midas_scripts import midiart, midiart3D, musicode, music21funcs
# from midas_scripts.musicode import *
# from midas_scripts.music21funcs import *
# from pyo import Server
# from pyo.lib import _widgets
#pyo.PYO_USE_WX = False
#from threading import Timer, Lock, Semaphore


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

        #self.static = wx.StaticText(self, -1, "ASS ASS ASS ASS")

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

    #TODO OnToolsDialogueClosed():

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
            m.set_outline_color(1,1,1)
            #m.outline_color = (1,1,1)
        else:
            p.color = (0,0,0)
            #m.set_outline_color(0,0,0)
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


def createServerGUI(nchnls, start, stop, recstart, recstop, setAmp, started,
                    locals, shutdown, meter, timer, amp, exit, title, getIsBooted,
                    getIsStarted):
    "Creates the server's GUI."
    global X, Y, MAX_X, NEXT_Y
    if title is None:
        title = "Pyo Server"
    if not PYO_USE_WX:
        createRootWindow()
        win = tkCreateToplevelWindow()
        f = ServerGUI(win, nchnls, start, stop, recstart, recstop, setAmp,
                      started, locals, shutdown, meter, timer, amp, getIsBooted,
                      getIsStarted)
        f.master.title(title)
        f.focus_set()
    else:
        #win = createRootWindow()
        #if win is None:
        win = wx.App()
        f = ServerGUI(None, nchnls, start, stop, recstart, recstop, setAmp,
                      started, locals, shutdown, meter, timer, amp, exit, getIsBooted,
                      getIsStarted)
        f.SetTitle(title)
        f.SetPosition((30, 30))
        f.Show()
        X, Y = (wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X) - 50,
                wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y) - 50)
        if sys.platform.startswith("linux"):
            MAX_X, NEXT_Y = f.GetSize()[0]+30, f.GetSize()[1]+55
        else:
            MAX_X, NEXT_Y = f.GetSize()[0]+30, f.GetSize()[1]+30
        wx.CallAfter(wxCreateDelayedTableWindows)
        wx.CallAfter(wxCreateDelayedGraphWindows)
        wx.CallAfter(wxCreateDelayedDataGraphWindows)
        wx.CallAfter(wxCreateDelayedSndTableWindows)
        wx.CallAfter(wxCreateDelayedMatrixWindows)
        wx.CallAfter(wxCreateDelayedCtrlWindows)
        wx.CallAfter(wxCreateDelayedSpectrumWindows)
        wx.CallAfter(wxCreateDelayedScopeWindows)
        wx.CallAfter(wxCreateDelayedExprEditorWindows)
        wx.CallAfter(wxCreateDelayedMMLEditorWindows)
        wx.CallAfter(wxCreateDelayedNoteinKeyboardWindows)
        wx.CallAfter(f.Raise)
    return f, win, PYO_USE_WX



def gui(self, locals=None, meter=True, timer=True, exit=True, title=None):
    """
    Show the server's user interface.

    :Args:

        locals: locals namespace {locals(), None}, optional
            If locals() is given, the interface will show an interpreter extension,
            giving a way to interact with the running script. Defaults to None.
        meter: boolean, optinal
            If True, the interface will show a vumeter of the global output signal.
            Defaults to True.
        timer: boolean, optional
            If True, the interface will show a clock of the current time.
            Defaults to True.
        exit: boolean, optional
            If True, the python interpreter will exit when the 'Quit' button is pressed,
            Otherwise, the GUI will be closed leaving the interpreter alive.
            Defaults to True.
        title: str, optional
            Alternate title for the server window. If None (default), generic
            title, "Pyo Server" is used.

    """
    import wx ### Isaac change
    self._gui_frame, win, withWX = createServerGUI(self._nchnls, self.start, self.cancel,
                                                   self.recstart, self.recstop, self.setAmp,
                                                   self.getIsStarted(), locals, self.shutdown,
                                                   meter, timer, self._amp, exit, title,
                                                   self.getIsBooted, self.getIsStarted)
    #withWX = False
    if meter:
        self._server.setAmpCallable(self._gui_frame)
    if timer:
        self._server.setTimeCallable(self._gui_frame)
    if withWX:
        try:
            win.MainLoop()
        except AttributeError:
            print("Continuing...")
    else:
        win.mainLoop()

#Modified
def on_quit1(self, evt=None):
    if self.getIsBooted():
        self.shutdown()
        #time.sleep(0.25)
    self.Destroy()
    if self.exit:
        sys.exit()

#Original
def on_quit(self, evt):
    if self.exit and self.getIsBooted(): #In original, self.exit == False; should be true--->this is a bad if statement.
        self.shutdown()
        time.sleep(0.25)
    self.Destroy()
    if self.exit:
        sys.exit()


class Animator(HasTraits):
    """ Convenience class to manage a timer and present a convenient
        UI.  This is based on the code in `tvtk.tools.visual`.
        Here is a simple example of using this class::

            >>> from mayavi import mlab
            >>> def anim():
            ...     f = mlab.gcf()
            ...     while 1:
            ...         f.scene.camera.azimuth(10)
            ...         f.scene.render()
            ...         yield
            ...
            >>> anim = anim()
            >>> t = Animator(500, anim.__next__)
            >>> t.edit_traits()

        This makes it very easy to animate your visualizations and control
        it from a simple UI.

        **Notes**

        If you want to modify the data plotted by an `mlab` function call,
        please refer to the section on: :ref:`mlab-animating-data`
    """

    ########################################
    # Traits.

    start = Button('Start Animation')
    stop = Button('Stop Animation')
    delay = Range(0, 100000, 0,   #Isaac edit
                  desc='frequency with which timer is called')

    # The internal timer we manage.
    timer = Any

    ######################################################################
    # User interface view

    traits_view = View(Group(Item('start'),
                             Item('stop'),
                             show_labels=False),
                       Item('_'),
                       Item(name='delay'),
                       title='Animation Controller',
                       buttons=['OK'])

    ######################################################################
    # Initialize object
    def __init__(self, millisec, callable, *args, **kwargs):
        r"""Constructor.

        **Parameters**

          :millisec: int specifying the delay in milliseconds
                     between calls to the callable.

          :callable: callable function to call after the specified
                     delay.

          :\*args: optional arguments to be passed to the callable.

          :\*\*kwargs: optional keyword arguments to be passed to the callable.

        """
        HasTraits.__init__(self)
        self.delay = millisec
        self.ui = None
        self.timer = Timer(millisec, callable, *args, **kwargs)
        self._stop_fired()
    ######################################################################
    # `Animator` protocol.
    ######################################################################
    def show(self):
        """Show the animator UI.
        """
        self.ui = self.edit_traits()

    def close(self):
        """Close the animator UI.
        """
        if self.ui is not None:
            self.ui.dispose()

    ######################################################################
    # Non-public methods, Event handlers
    def _start_fired(self):
        self.timer.Start(self.delay)

    def _stop_fired(self):
        self.timer.Stop()

    def _delay_changed(self, value):
        t = self.timer
        if t is None:
            return
        if t.IsRunning():
            t.Stop()
            t.Start(value)


class wxInfiniteTimer:
    """A Timer class that does not stop, unless you want it to.
    --Modified for use with wxTimer instead of Threading.Timer.  ...bummer. It's inaccurate.
    --Code attributed to Bill Schumacher, stackoverflow
    https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
    https: // stackoverflow.com / users / 7370877 / bill - schumacher"""
    def __init__(self, seconds, target, window):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target()  #In this case, target must be a generator, and it is activated here.
        #self.thread = None
        self.window = window
        self.thread = wxTimer(self.window) #Todo refactor thread

        #self.lock = threading.Lock()
        #self.semaphore = threading.Semaphore()

    def _handle_target(self, evt):
        self.is_running = True

                      #Need to SET target here too?
        #if type(self.target) is types.GeneratorType:

        self.target.__next__()          #Call target
        self.is_running = False
        #self._start_timer()


    def _start_timer(self):
        #self.lock.acquire()
        # self.semaphore.acquire()
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = wxTimer(owner=self.window)  #owner=self._handle_target)     #(self.seconds, self._handle_target) ##threading. #_Timer.
            #self.target()
            self.window.Bind(wx.EVT_TIMER, self._handle_target, id=self.thread.GetId())
            print("THREAD_ID", self.thread.GetId())
            self.thread.Start(milliseconds=self.seconds, oneShot=wx.TIMER_CONTINUOUS)  #start() for threading.Timer--_Timer
            #print("blah")
            #self.lock.release()
            # self.semaphore.release()


    def start(self):
        #self.lock.acquire()
        #self.semaphore.acquire()
        print("Here 1")
        if not self._should_continue and not self.is_running:
            self._should_continue = True

            self._start_timer()
            #self.lock.release()
            #self.semaphore.release()
        else:
            print("Timer already started or running, please wait if you're restarting.")


    def stop(self):
        #self.lock.acquire()
        # self.semaphore.acquire()
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.

            self.thread.Stop() ##cancel()            #Todo This gives attribute error, wtf? 04/11/2021 It shouldn't.
            #self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer never started or failed to initialize.")



class InfiniteTimer:
    """A Timer class that does not stop, unless you want it to.
    --Code attributed to Bill Schumacher, stackoverflow
    https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
    https: // stackoverflow.com / users / 7370877 / bill - schumacher"""

    def __init__(self, seconds, target, window, player=True):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None
        self.lock = threading.Lock()
        self.m_v = window if player is False else window.mayavi_view
        # self.semaphore = threading.Semaphore()

    def _handle_target(self):
        self.is_running = True

        #self.window.scene3d.render_window.make_current()

        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self._should_continue:  # Code could have been running when cancel was called.

            ####wglMakeCurrent(NULL, NULL)


            #self.m_v.scene3d.render_window._vtk_obj.PushContext()
            #context = self.m_v.scene3d.render_window._vtk_obj.PopContext()

            self.thread = threading.Timer(self.seconds, self._handle_target)  ##_Timer
            if self.m_v is None:
                pass
            else:
                pass
                #self.m_v.scene3d.render_window.make_current()
                #self.m_v.scene3d.render_window._vtk_obj.ReleaseGraphicsResources(None)

                ####wglMakeCurrent(NULL, NULL)
                ####ReleaseDC()


            self.thread.start()
            # self.lock.release()
            # self.semaphore.release()

    def start(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def stop(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer never started or failed to initialize.")


class asyncInfiniteTimer:
    """A Timer class that does not stop, unless you want it to.
    --Code attributed to Bill Schumacher, stackoverflow
    https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
    https: // stackoverflow.com / users / 7370877 / bill - schumacher"""

    def __init__(self, seconds, target, window):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None
        self.lock = threading.Lock()
        self.window = window   #Todo Use.
        # self.semaphore = threading.Semaphore()

    def _handle_target(self):
        self.is_running = True

        #self.window.scene3d.render_window.make_current()

        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = asyncTimer(self.seconds, self._handle_target, context=None, first_immediately=None, timer_name="A_Sync")  ##_Timer
            #TODO Finish
            #self.thread. .start()

            # self.lock.release()
            # self.semaphore.release()

    def start(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def stop(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()  # Todo This gives attribute error, wtf? 04/11/2021 It shouldn't.
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer never started or failed to initialize.")



class mpInfiniteTimer:
    """A Timer class that does not stop, unless you want it to.
    ---Modified for using with multiprocessing and a multiprocessing-derived _Timer.   ---Does not work as intended.
    --- Method handler functionality had to be explicitly executed WITHIN this class.
    --Code attributed to Bill Schumacher, stackoverflow
    https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
    https: // stackoverflow.com / users / 7370877 / bill - schumacher"""

    def __init__(self, seconds, target, parent):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = iter(target)
        self.thread = None
        #self.lock = threading.Lock()
        self.parent = parent   #Todo Use.
        # self.semaphore = threading.Semaphore()

        #WHACK JOB PART 1
        if self.parent.volume_slice:
            self.ipw = self.parent.image_plane_widget.ipw
            self.ipw2 = None
        else:
            self.ipw = self.parent.slice.actor.actor
            self.ipw2 = self.parent.slice_edges.actor.actor

    def _handle_target(self):
        self.is_running = True

        i = self.target.__next__()

        #WHACK JOB PART 2
        if i == self.parent.x_length:  # Because we animate ACROSS our desired range max, we are making darn sure that this
            # condition is met.
            # Destroy the volume_slice and rebuild it at the end of the animating generator function.
            self.parent.reset_volume_slice(self.parent.grid3d_span, volume_slice=self.parent.volume_slice)
            # Fire a "loop_end" flag so we can turn off "movie_maker.record" if we intend to animate without generating frames.
            self.loop_end = True
            # Might change this later, for playback stuff.
            if self.loop_end is True:
                self.parent.scene.scene.movie_maker.record = False

            self.parent.scene3d.anti_aliasing_frames = 8  # TODO Check this again.
            # pass
            return i
        else:
            if self.parent.volume_slice:
                self.ipw.trait_set(slice_position=i)  ##ipw.position = i  #/i_div
                # self.scene3d.disable_render=False

            else:
                pos = np.array([i, 0, 0])
                self.ipw.trait_set(position=pos)
                self.ipw2.trait_set(position=pos)

            time.sleep(self.seconds)

            self.is_running = False
            self._start_timer()

    def _start_timer(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = _Timer(0, self._handle_target)  ##_Timer uses multiprocessing
            self.thread.start()
            # self.lock.release()
            # self.semaphore.release()

    def start(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def stop(self):
        # self.lock.acquire()
        # self.semaphore.acquire()
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()  # Todo This gives attribute error, wtf? 04/11/2021 It shouldn't.
            # self.lock.release()
            # self.semaphore.release()
        else:
            print("Timer never started or failed to initialize.")


class _Timer(Process):
    """ Multiprocessing timer instead of threading timer.
    Attritution:
    Dano -- https://stackoverflow.com/questions/25297627/why-no-timer-class-in-pythons-multiprocessing-module
    https://stackoverflow.com/users/2073595/dano
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        super(_Timer, self).__init__()
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()

import asyncio


class asyncTimer:
    def __init__(self, interval, callback, first_immediately, timer_name, context):
        self._interval = interval
        self._first_immediately = first_immediately
        self._name = timer_name
        self._context = context
        self._callback = callback
        self._is_first_call = True
        self._ok = True
        self._task = asyncio.ensure_future(self._job())
        print(timer_name + " init done")

    async def _job(self):
        try:
            while self._ok:
                if not self._is_first_call or not self._first_immediately:
                    await asyncio.sleep(self._interval)
                await self._callback(self._name, self._context, self)
                self._is_first_call = False
        except Exception as ex:
            print(ex)

    def cancel(self):
        self._ok = False
        self._task.cancel()


async def some_callback(timer_name, context, timer):
    context['count'] += 1
    print('callback: ' + timer_name + ", count: " + str(context['count']))

    if timer_name == 'Timer 2' and context['count'] == 3:
        timer.cancel()
        print(timer_name + ": goodbye and thanks for all the fish")


# timer1 = Timer(interval=1, first_immediately=True, timer_name="Timer 1", context={'count': 0}, callback=some_callback)
# timer2 = Timer(interval=5, first_immediately=False, timer_name="Timer 2", context={'count': 0}, callback=some_callback)
#
# try:
#     loop = asyncio.get_event_loop()
#     loop.run_forever()
# except KeyboardInterrupt:
#     timer1.cancel()
#     timer2.cancel()
#     print("clean up done")



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

#Mayavi Animator Overwrite (fixes the unwanted 10 mil second delay; makes it 0.)
mayavi.tools.animator.Animator = Animator


#Pyo Gui bug patch.
#Server.gui = gui  #-Attempt 1
#pyo.lib._widgets.createServerGUI = createServerGUI  #Attempt 2, works.

#Pyo shutdown bug workaround patch; restores original code after overwrite when gui is terminated from Playback class.
ServerGUI.on_quit = on_quit1  #--First overwrite.
#ServerGUI.on_quit = on_quit  --implemented in Playback.
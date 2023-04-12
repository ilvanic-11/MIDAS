# Author: Prabhu Ramachandran, Gael Varoquaux
# Copyright (c) 2004-2020, Enthought, Inc.
# License: BSD Style.
""" A tool for easy and interactive visualization of data.
    Part of the Mayavi project of the Enthought Tool Suite.
"""

__version__ = '4.7.2'

__requires__ = [
    'apptools',
    'envisage',
    'numpy',
    'pyface>=6.1.1',
    'pygments',  # This is only needed for the Qt backend but we add it anyway.
    'traits>=6.0.0',
    'traitsui>=7.0.0',
    'vtk'
]

__extras_require__ = {
    'app': [
        'envisage',
    ],
}


def _jupyter_nbextension_paths():
    return [dict(
        section="notebook",
        # the path is relative to the `mayavi` directory
        src="tools/static",
        # directory in the `nbextension/` namespace
        dest="mayavi",
        require="mayavi/x3d/x3dom"
    )]


import wx
import music21
import inspect
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

from pyface.util import fix_introspect_bug
#VTK 9.0.1 and Mayavi 4.7.2 updates
from tvtk.pyface.ui.wx import decorated_scene
from traitsui.wx import tree_editor
from traitsui.wx import helper
from pyface.ui.wx.action import menu_manager
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

#Method overwrite.
#Permanent fix to the broken attribute auto-complete bug for our pycrust.

#####PATCHES########


#Method bug.
decorated_scene.DecoratedScene._background_changed = _background_changed
#Window coords restorating bug.
helper.restore_window = restore_window
#Right click menu bug.
menu_manager.MenuManager.add_to_menu = add_to_menu
tree_editor.SimpleEditor._is_pasteable = _is_pasteable

import sys, os

from midas_scripts import midiart, midiart3D     ###,  music21funcs


from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

import mayavi
from numpy import array
import numpy as np
import random
import music21
import wx    #TODO how to do simpler imports (i.e. just what we need instead of all of wx)




from mayavi import mlab, modules, sources, core, components
from mayavi.components import actor
from mayavi.sources import array_source
from mayavi.core import module_manager
#from mayavi.modules import image_plane_widget

from mayavi3D import MusicObjects

from gui import PianoRoll

import copy

from traits.api import HasTraits, Range, Instance, on_trait_change, Float, String, Int, Bool

from traitsui.api import View, Item, HGroup
from traits.trait_numeric import Array
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

#from traits.trait_types import Button

from traits.trait_numeric import AbstractArray

# from traits.trait_types import Function
# from traits.trait_types import Any
from traits.trait_types import Int
# from traits.trait_types import Str
from mayavi.tools import animator
import cv2
# from traits.trait_types import Method
from traits.trait_types import List
from traits.trait_types import Any
from traits.trait_types import Tuple



class Actor(HasTraits):
    #For general purposes as traits.
    name = String()

    _points = Array(dtype=np.float32)

    _array3D = Array(dtype=np.int8, shape=(5000, 128, 128))
    _stream = Any()  #TODO For exporting, finish.

    #For trait flagging.
    array3Dchangedflag = Int()
    pointschangedflag = Int()
    streamchangedflag = Int()

    ##For trait-syncing.
    cur_z = Int(90)  #         #Synced one-way to mayavi_view.cur_z trait.
    color = Tuple(1., 0., 0.)  #Synced two_way with the pipeline's current_actor.property.color trait.
    position = Array()         #Synced two-way with the pipeline's current_actor.actor.actor.position trait.


    # cur = Int()


    def __init__(self, mayavi_view, index):
        HasTraits.__init__(self)
        self.index = index
        self.mayavi_view = mayavi_view
        self.toplevel = self.mayavi_view.parent

        self.colors_instance = ""  #Denotes to what instance of a loaded color image this actor belongs. (call1, call2, etc.)
        self.part_num = 0  #For stream.Part purposes, used in colors function.
        self.priority = 0

        #CHANGE the float dtype from 64 to 16 manually on init.
        #self._points.dtype = np.float16
        #print("_Points", self._points, self._points.dtype)

    #3d numpy array---> True\False map of existing coords for rapid access.
    def change_array3D(self, array3D):
        self._array3D = array3D
        self.array3Dchangedflag = not self.array3Dchangedflag

    #2d numpy array---> List of actual coordinates
    def change_points(self, points):
        self._points = points
        self.pointschangedflag = not self.pointschangedflag

    #music21 stream---> Stream for stream purposes.
    def change_stream(self, stream):
        self._stream = stream
        self.streamchangedflag = not self.streamchangedflag

    def isColorsInstance(self):
        if self.colors_instance == '':
            return False
        else:
            return True
    #def change_color(self, color):

    ##WORKING INSTANCE
    #TODO Is this fired when an actor is deleted? If so, can we shut that off?
    @on_trait_change("array3Dchangedflag")
    def actor_array3D_changed(self):
        print("actor_array3D_changed")
        print("actor_index  ", self.index)

        cpqn = self.toplevel.pianorollpanel.pianoroll._cells_per_qrtrnote


        self._points = np.argwhere(self._array3D == 1.0)
        self._points[:, 0] =  self._points[:, 0] / cpqn #Account for cpqn.  X axis "Slice" rebound here.

        try:
            self.mayavi_view.sources[self.index].mlab_source.trait_set(points=self._points) #Traitset happens on x axis slice rebinding.
        except IndexError:
            pass


    @on_trait_change("pointschangedflag")
    def actor_points_changed(self):
        print("actor_points_changed")
        print("actor_index ", self.index)

        cpqn = self.toplevel.pianorollpanel.pianoroll._cells_per_qrtrnote
        print("CPQN", cpqn)

        new_array3D = np.zeros(self._array3D.shape, dtype=np.int8)
        for p in self._points:
            new_array3D[int(p[0]) * cpqn, int(p[1]), int(p[2])] = 1.0   #TODO Account for cpqn. * cpqn
        self.mayavi_view.parent.pianorollpanel.pianoroll.cur_array3d = self._array3D = new_array3D
        self.mayavi_view.sources[self.index].mlab_source.trait_set(points=self._points)
        print("sources trait_set after actor_points_changed")

    @on_trait_change('color')
    def show_color(self):
        print("COLOR TRAIT CHANGED:", self.color)
        pass

    @on_trait_change('position')
    def show_position(self):
        print("POSITION TRAIT CHANGED:", self.position)
        self.mayavi_view.cur_ActorIndex = self.index




# mlab.options.offscreen = True

class Mayavi3idiView(HasTraits):
    scene3d = Instance(MlabSceneModel, ())
    view = View(Item('scene3d', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
                resizable=True)
    actor = Any()
    actors = List(Actor)


    cur_ActorIndex = Int()
    cur_z = Int()

    cpqn = Int(4)   #Startup cpqn

    cpqn_changed_flag = Bool()

    cur_changed_flag = Int()

    actor_deleted_flag = Bool()

    position = Array()  #Synced one_way 'from' the pipeline current actor's position.(highlighter plane purposes)

    # Stream
    stream = music21.stream.Stream()

    def __init__(self, parent):
        HasTraits.__init__(self)

        #self.on_trait_event(self._array3D_changed, 'array3Dchangedflag')
        self.parent = parent
        self.engine = self.scene3d.engine
        self.engine.start()  # TODO What does this do?
        self.scene = self.engine.scenes[0]

        # Common Scene Properties #TODO Should these be traits? (I think grid3d_span should be...at least)
        self.grid3d_span = 254  # For right now.
        self.bpm = 540  # TODO Set based on music21.tempo.Metronome object.
        self.i_div = 2  #Upon further review, i_div IS frames per beat. I'll change this variable name later.
        #self.time_sig = '4/4' #TODO Set based on music21.meter.TimeSignature object.

        #Calls for colors ---for exporting.
        self.colors_call = 0   #No color calls yet. #TODO Make this part of the actor class in new method that doesn't include the actor listbox name.
        self.colors_name = ""

        #For a trait function, this lets user know what if it's a 'colors' actor before it's actually destroyed.
        self.deleting_actor = ''

        #For another traits function.
        self.ret_x = 0
        self.ret_y = 0
        self.ret_z = 0

        #For color configuring upon creation of new_actor.
        self.number_of_noncolorscall_actors = 0

        # Movie Recording
        self.scene.scene.movie_maker.record = False
        self.scene.scene.movie_maker.directory = r".\resources\intermediary_path\recorded_frames"

        # Colors Imports
        ###Set Scene Background Color
        self.scene.scene.background = (0.0, 0.0, 0.0)



        #Imports Colors

        self.clr_dict_list = midiart.get_color_palettes(r".\resources\color_palettes")



        self.default_color_palette = midiart.FLStudioColors

        self.default_mayavi_palette = midiart.convert_dict_colors(self.default_color_palette)

        #TODO Should this be in main MIDAS_wx?
        self.current_palette_name = "FLStudioColors"   #Palette on startup.




        #Grid Construct
        self.mlab_calls = []  #TODO Note: mlab.clf() in the pyshell does not clear this list.
        self.text3d_calls = []
        self.text3d_default_positions = []

        self.highlighter_calls = []

        self.volume_slice = None
        
        self.sources = list()
        #TODO I don't like "sources" as the name of this list. Sources is actually a trait in the mayavi pipeline somewhere....
        #TODO Also, sources and mlab_calls are virtually the same thing. Delete one?

        #self.append_actor("0")

    #TODO For exporting
    def Append_Streams(self):
        pass

    #Grid Establisher.
    @on_trait_change('scene3d.activated')
    def create_3dmidiart_display(self):

        self.scene3d.disable_render = True



        #self.scene.render_window.line_smoothing = True


        self.midi = music21.converter.parse(r".\resources\Spark4.mid")
        #self.midi = midiart3D.extract_xyz_coordinates_to_array(self.midi)




        #TODO These become buttons.
        #self.Points = midiart3D.get_points_from_ply(r".\resources\sphere.ply")
        self.Points = MusicObjects.earth()
        self.Points = self.standard_reorientation(self.Points, 1.3)
        self.Points = np.asarray(self.Points, dtype=np.int16)
        self.Points = np.asarray(self.Points, dtype=np.float16)
        self.Points = self.trim(self.Points, axis='y', trim=0)
        self.Points = midiart3D.transform_points_by_axis(self.Points, positive_octant=True)
        #print("Points", self.Points[:, 2])



        #self.SM_Span = self.midi.highestTime
        #self.grid3d_span = self.SM_Span
        #self.Points_Span = self.Points.max()

        #Draw Grid
        self.insert_piano_grid_text_timeplane(self.grid3d_span)
        #TODO REFACTOR THIS?

        ###SELECT OBJECT

        #ACTOR EXAMPLES

        #self.music = self.insert_music_data(self.midi, color=(1, .5, 0), mode="sphere", scale_factor=1)
        #self.model = self.insert_array_data(self.Points, color=(0, 0, 1), mode="sphere", scale_factor=2.5)
        #self.text = self.insert_text_data("Script-Ease", "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz         ?,;':-.!\"()[]/   0123456789", color=(0, .5, 1), mode='arrow', scale_factor=2)
        #random.randint(0, 88)
        #self.double = (x, y) = midiart.separate_pixels_to_coords_by_color(cv2.imread(r".\resources\BobMandala.png"), 0,
        #                            nn=True, display=False, clrs=self.clr_dict_list['75_crimso-11-1x'])



        #Highlighter Plane
        self.establish_highlighter_plane(0, color=(0, 1, 0), length=self.grid3d_span)


        #self.points = self.Points


        # @mlab.show
        # self.scene3d.disable_render = False

        #self.insert_titles()     ##I had a 2nd call for a work session where I lost the camera. I may not need this now...
        self.establish_opening()     #TODO Write in a pass statement for when calls to this function are made from within the program; camera issue. Now Redundant?
        self.animate(160, self.grid3d_span, i_div=2)
        #print("Animate")

        #Animator Instance. Instantiated upon the invocation of self.animate after which the animation is immediately stopped here.
        #self.animate1._stop_fired() #TODO Redundant. _stop_fired() now called within Animate after invocation of animate_plane_scroll.
        #print("Animation Stopped")

        ###RECORD python Scripts
        #mlab.start_recording(ui=True)


        self.insert_titles()
        #self.insert_note_text("3-Dimensional Music", 0, 164, 0, color=(1,0,1), opacity=.12, orient_to_camera=False, scale=3

        #Mayavi zoom to coordinates.
        #self.rebind_picker()

        self.scene.on_mouse_pick(self.zoom_to_coordinates, type='point', button='Middle')
        #TODO ERROR---this doesn't trigger after deleting and redrawing the mayavi view. July 30th, 2020.
        #TODO Does mlab.clf() eliminate the picker object?

        self.scene3d.disable_render = False

    @on_trait_change('scene3d.activated')
    def rebind_picker(self):
        self.scene.on_mouse_pick(self.zoom_to_coordinates, type='point', button='Middle')

    # @mlab.clf
    # def clear_lists(self):
    #     self.sources.clear()
    #     self.mlab_calls.clear()
    #     self.highlighter_calls.clear()
    #     self.text3d_calls.clear()
    #     self.text3d_default_positions.clear()

    def clear_all_and_redraw(self):
        self.scene3d.disable_render = True
        mlab.clf()
        self.sources.clear()
        self.mlab_calls.clear()
        self.highlighter_calls.clear()
        self.text3d_calls.clear()
        self.text3d_default_positions.clear()
        self.create_3dmidiart_display()
        self.scene3d.disable_render = False
        #TODO Add delete_actors stuff here too. New Session function?! :)


    #TODO Redundant now?
    def redraw_mayaviview(self):
        self.scene3d.disable_render = True
        mlab.clf()
        self.create_3dmidiart_display()
        self.scene3d.disable_render = False
        #Set focus on mbp for fast use of "F" hotkeys.
        self.parent.mainbuttonspanel.SetFocus()

    def remove_mlab_actor(self, actor_child): #TODO Write from scenes[0].children stuff. CHECK--Use child.remove()
        actor_child.remove()  #Must be an actor_child found in scene3d.engine.scenes[0].children. Use subscript for it.
        #TODO Create version of this to call for the actor by its "name" trait.


    ##ZACH's dynamic trait array3D\points\actors trait updating functions.
    #-------------------
    ##----------------------------------------
    ###-------------------------------------------------------------------


    def CurrentActor(self):
        if len(self.actors) <= 0:
            return None
        else:
            return self.actors[self.cur_ActorIndex]

    def append_actor(self, name, color):
        # self.add_trait(actor_name,Actor())
        #self.scene3d.disable_render = False

        print("append_actor")
        print('1')

        self.cur_ActorIndex = len(self.actors)
        a = Actor(self, self.cur_ActorIndex)

        #self.actor = a

        #TODO Can ALL this v-here-v go into the actor's init?
        print('2')
        # self.sources.append(None)
        self.actors.append(a)
        print('3')
        self.appending_data = self.insert_array_data(a._array3D, color=color, mode="cube", name=name, scale_factor=1.0)
        print('4')
        self.sources.append(self.appending_data)
        print('5')
        self.mlab_calls.append(self.appending_data)
        print('6')


        #TODO Move this to actor class?
        #TODO Dahfuq was this?! 11/08/20
        self.on_trait_change(self.actor_stream_changed, 'actors.streamchangedflag')
        #self.on_trait_change(self.actor_list_changed, 'actors[]')



        #Traits syncing goes here, if desired. (can't go in actor init, because the actor hasn't been appended to any lists yet...)
        #Simplifies access to the pipeline's properties\traits by configuring our "Actor()" class to have these directly.
        self.sources[self.cur_ActorIndex].actor.property.sync_trait('color', a, mutual=True)
        print("Colors synced.")
        self.sources[self.cur_ActorIndex].actor.actor.sync_trait('position', a, mutual=True)
        print("Position synced.")


        a.name = name
        a.color = color


        self.cur_changed_flag = not self.cur_changed_flag

        #self.scene3d.disable_render = False

    @on_trait_change('cur')
    def current_actor_changed(self):
        print("current_actor_changed")



    # TODO Deprecated?
    # def update_3Dpoints(self, row, col, val):
    #     try:
    #         page = self.GetTopLevelParent().pianorollpanel.currentPage
    #         layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)
    #         self._array3D[col, 127 - row, layer] = val
    #     except Exception as e:
    #         print(e)
    #         pass

    # TODO Decide if still doing this.
    def actor_stream_changed(self):
        print("actor_stream_changed")
        pass


    def actor_list_changed(self):
        print("actor_list_changed")
        pass

    ###MAYAVI_VIEW INSERT AND MANIPULATION FUNCTIONS
    #-------------------
    ##----------------------------------------------
    ###---------------------------------------------------------------------------------------

    def insert_array_data(self, array_2d, color=(0, 0, 0), mode="cube", name='', scale_factor=.25):
        # print(array_2d)
            #color = lambda x: super().actors[super().cur].color
        print("insert_array_data")
        mlab_data = mlab.points3d(array_2d[:, 0], array_2d[:, 1], array_2d[:, 2], color=self.actors[self.cur_ActorIndex].color, mode=mode, name=name,
                                  scale_factor=scale_factor)
        return mlab_data


    def insert_music_data(self, in_stream, color=(0., 0., 0.), mode="cube", name='', scale_factor=1):
        array_data = midiart3D.extract_xyz_coordinates_to_array(in_stream)
        array_data = array_data.astype(float)
        # print(array_data)
        mlab_data = mlab.points3d(array_data[:, 0], array_data[:, 1], array_data[:, 2], color=color, mode=mode, name=name,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data


    def insert_text_data(self, mc, text, color=(0., 0., 0.), mode="cube", name='', scale_factor=1):
        text_stream = self.parent.musicode.mc.translate(mc, text)
        text_array = midiart3D.extract_xyz_coordinates_to_array(text_stream)
        mlab_data = mlab.points3d(text_array[:, 0], text_array[:, 1], text_array[:, 2], color=color, mode=mode, name=name,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data


    ###TITLES and NOTE inserts.
    def insert_note_text(self, text, x=0, y=154, z=0, color=(0, 0, 1), opacity=1, orient_to_camera=True, scale=3):
        mlab_t3d = mlab.text3d(text=text, x=x, y=y, z=z, color=color, opacity=opacity,
                               orient_to_camera=orient_to_camera, scale=scale)
        self.text3d_calls.append(mlab_t3d)
        self.text3d_default_positions.append(mlab_t3d.actor.actor.position)
        # TODO
        ## def insert_image_data(self, imarray_2d, color=(0,0,0), mode="cube", scale_factor = 1):


    ###SCENE TITLEd
    def insert_title(self, text, color=(1, .5, 0), height=.7, opacity=1.0, size=1):
        return mlab.title(text=text, color=color, height=height, opacity=opacity, size=size)

    # Leave this here for now.
    def insert_titles(self):
        self.insert_note_text("The Midas Display", 0, 137, 0, color=(1, 1, 0), orient_to_camera=True,
                              scale=7)
        ###Note: affected by top_mayaviview_split sash position.
        self.title = self.insert_title("3-Dimensional Music", color=(1, 0, 1), height=.82, opacity=.12, size=.65)



    #Volume Slice Functions
    def insert_volume_slice(self, length=127):
        # Time_ScrollPlane
        # x,y,z = np.mgrid[0:127, 0:127, 0:127]
        self.scene3d.disable_render = True

        if self.grid3d_span is not None:
            length = self.grid3d_span
        else:
            length = length
        xh, yh, zh = np.mgrid[0:int(length), 0:254, 0:254]
        # Scalars_1 = (x+y+z)
        Scalars_2 = np.zeros((int(length), 254, 254))
        # xtent = np.array([0, 127, 0, 127, 0, 127])
        self.image_plane_widget = mlab.volume_slice(xh, yh, zh, Scalars_2, opacity=.7, plane_opacity=.7, plane_orientation='x_axes',
                          transparent=True)
        #if self.volume_slice is not None:
        self.volume_slice = self.image_plane_widget.parent.parent
        print(self.image_plane_widget)
        self.image_plane_widget.ipw.origin = array([0., 0., 0.])
        self.image_plane_widget.ipw.point1 = array([0.0, 127., 0.0])
        self.image_plane_widget.ipw.point2 = array([0.0, 0.0, 127.])
        self.image_plane_widget.ipw.slice_position = 1
        self.image_plane_widget.ipw.slice_position = 0


        self.scene3d.disable_render = False

        return self.volume_slice


    def reset_volume_slice(self, length=127):
        if self.grid3d_span is not None:
            length = self.grid3d_span
        else:
            length = length
        self.volume_slice.remove()
        self.insert_volume_slice(length)

    #Highlighter Plane functions.
    def establish_highlighter_plane(self, z_points=0, z_marker=0, position = np.array([0, 0, 90]), color=(0, 1, 0), grandstaff=True, length=None):
        self.scene3d.disable_render = True
        if length is not None:
            length = length
        else:
            length = self.grid3d_span
        x1, y1, z1 = (0, 0, z_points)  # | => pt1
        x2, y2, z2 = (0, 127, z_points)  # | => pt2
        x3, y3, z3 = (length, 0, z_points)  # | => pt3
        x4, y4, z4 = (length, 127, z_points)  # | => pt4
        linebox = MusicObjects.line_square(length=length, z_axis=z_points)
        #Green Surface
        plane = mlab.mesh([[x1, x2],
                                 [x3, x4]],  # | => x coordinate

                                  [[y1, y2],
                                  [y3, y4]],  # | => y coordinate

                                  [[z1, z2],
                                  [z3, z4]],  # | => z coordinate

                                  color=color, line_width=5.0, mode='sphere', name="Green Surface", opacity=.125, scale_factor=1, tube_radius=None)  # black#extent=(-50, 128, -50, 128, 114, 114)
        #self.mlab_calls.append(plane)
        self.highlighter_calls.append(plane)
        #White Edges
        plane_edges = mlab.plot3d(linebox[:, 0], linebox[:, 1], linebox[:, 2]+.25,
                                         color=(1,1,1), line_width=.5, name="White Edges", opacity=1., tube_radius=None)
        self.highlighter_calls.append(plane_edges)
        #self.mlab_calls.append(plane_edges)
        if grandstaff:
            stafflines = MusicObjects.grand_staff(z_value=z_points, length=length)
            gclef = MusicObjects.create_glyph(r".\resources\TrebleClef.png", y_shift=59, z_value = z_points)
            fclef = MusicObjects.create_glyph(r".\resources\BassClef.png", y_shift=44.3, z_value = z_points)
            #for j in grandstaff:
            #Grand Staff Lines
            self.gscalls = mlab.plot3d(stafflines[:, 0], stafflines[:, 1], stafflines[:, 2], color=(0,1,0), line_width=.5, name="Staff Lines", opacity=1., tube_radius=None)
            #Treble Clef
            self.gclef_call = mlab.points3d(gclef[:, 0], gclef[:, 1], gclef[:, 2], color=(0,1,0), mode='cube', name="Treble Clef", opacity=.015, scale_factor=.25)
            #Bass Clef
            self.fclef_call = mlab.points3d(fclef[:, 0], fclef[:, 1], fclef[:, 2], color=(0,1,0), mode='cube', name="Bass Clef", opacity=.015, scale_factor=.25)
            #self.mlab_calls.append(self.gscalls)
            self.highlighter_calls.append(self.gscalls)
            #self.mlab_calls.append(self.gclef_call)
            self.highlighter_calls.append(self.gclef_call)
            #self.mlab_calls.append(self.fclef_call)
            self.highlighter_calls.append(self.fclef_call)
            #self.gclef_call.actor.actor.position = np.array([0, 59, 0])
            #self.fclef_call.actor.actor.position = np.array([0, 44.3, 0])
        #Z-Plane marker.
        #a_marker = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.GetItemText(self.cur_ActorIndex)

        a_label = mlab.text3d(-40, -10, 0, "Actor_0", color=(0, 1., .75), name="Actor_Label", orient_to_camera=False, scale=4)
        z_label = mlab.text3d(-40, 0, 0, "Z-Plane_%s" % z_marker, color=(.55, .55, .55), name="Z_Label", orient_to_camera=False, scale=4)
        self.highlighter_calls.append(a_label)
        self.highlighter_calls.append(z_label)

        self.initial_reticle = np.asarray(np.vstack(((0, 127-0,  0),
                             (149, 127-0,  0),
                             (149, 127-22, 0),
                             (0, 127-22, 0),
                             (0, 127-0,  0))), dtype=np.float32)

        ##Red Grid Reticle Box
        self.grid_reticle = mlab.plot3d( self.initial_reticle[:, 0],  self.initial_reticle[:, 1],  self.initial_reticle[:, 2],
                                        color=(1,.42, 0), line_width=2., name="Red Edges", opacity=1., tube_radius=None, tube_sides=12)
        self.highlighter_calls.append(self.grid_reticle)
        self.scene3d.disable_render = False



        #INITIAL Highlighter positions AND redraw_mayaviview positions.
        #Note: self.cur_z = 90 set in MIDAS_wx.py      #Matches position variable.
        for h in self.highlighter_calls:
            if h.name == "Z_Label":
                h.actor.actor.position = np.array([position[0]-40, position[1], position[2]])
                h.text = "Z-Plane_%s" % str(90)
            elif h.name == "Actor_Label":
                h.actor.actor.position = np.array([position[0]-40, position[1]-10, position[2]])
                h.text = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.GetItemText(self.cur_ActorIndex)
            else:
                h.actor.actor.position = position
        #return plane




        # TODO Tie this to a button.
    def remove_highlighter_plane(self):
        for i in self.highlighter_calls:
            # Remove from scene3d.
            i.remove()
            #Remove's the entire vtk_data_source and all nested objects of that instance.
            #TODO Still need to figure out proper mayavi object removal. 09\25\20
            #Makes highlighterplane work correctly.
            #print("Parent", i.parent)
            #i.parent.parent.remove()
        # Clear reference list.
        self.highlighter_calls.clear()


    #Position, orientation, and #TODO origin functions.
    #TODO This is a numpy function. Allocate accordingly?
    def set_z_to_single_value(self, coords, value, index=None):
        if index is None:
            coords_array = coords
            coords_array_z = coords[:, 2]
            coords[:, 2] = np.full((len(coords_array_z), 1), value)[:, 0]
            return coords_array
        else:
            coords_array = self.mlab_calls[index].mlab_source.points
            coords_array_z = coords_array[:, 2]
            coords_array[:, 2] = np.full((len(coords_array_z), 1), value)[:, 0]
            self.mlab_calls[index].mlab_source.points = coords_array
        return coords_array


    def set_actor_positions(self, position=np.array([0,0,0]), actors=None, rando=False):
        self.remove_trait('position')

        def random_position():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            pos = np.asarray(list1, dtype=np.float16)
            return pos

        if actors == 'all':
            for vtk_data_source in self.scene3d.engine.scenes[0].children:
                if rando is True:
                    pos = random_position()
                else:
                    pos = position
                print("VTKDATA TYPE:", type(vtk_data_source))
                if isinstance(vtk_data_source, type(mayavi.sources.array_source.ArraySource())):
                    vtk_data_source.children[0].children[0].ipw.slice_position = 0

                #assert len(vtk_data_source.children[0].children) > 0, "List is empty."

                elif len(vtk_data_source.children[0].children) is not 0:
                    if not isinstance(vtk_data_source.children[0].children[0], type(mayavi.core.module_manager.ModuleManager())):
                        vtk_data_source.children[0].children[0].actor.actor.position = pos


                elif len(vtk_data_source.children[0].children) is not 0:
                    if isinstance(vtk_data_source.children[0].children[0], type(mayavi.core.module_manager.ModuleManager())):
                        for k in vtk_data_source.children[0].children[0].children:
                            if isinstance(k.actor, mayavi.components.actor.Actor):
                                k.actor.actor.position = pos
                            else:
                                pass   #k.actor.position = pos

            #Patch, was missing one. #TODO figure out -- look at set_actor_orientations for answer.
            if rando is True:
                pos = random_position()
            else:
                pos = position
            self.highlighter_calls[0].actor.actor.position = pos

                    #print("SECONDCHILD:", vtk_data_source.children[0].children[0])
        elif actors == 'music':
            for i in self.mlab_calls:
                if rando is True:
                    pos = random_position()
                else:
                    pos = position
                i.actor.actor.position = pos

        elif actors == 'highlighter':
            for j in self.highlighter_calls:
                if rando is True:
                    pos = random_position()
                else:
                    pos = position
                j.actor.actor.position = pos ####Current Actor's Current Z-Plane's Position



        self.add_trait('position', Array())
        for l in range(0, len(self.actors)):
            self.sources[l].actor.actor.sync_trait('position', self, mutual=False)
        self.on_trait_change(self.highlighter_plane_chase, 'position')
        self.on_trait_change(self.select_moved_actor, 'position')
        print("Position trait one-way RE-synced: actor.position ---to---> mayavi_view.position.")

    def set_actor_orientations(self, orientation=np.array([0,0,0]), actors=None, rando=False):

        def random_orientation():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            ori = np.asarray(list1, dtype=np.float16)
            return ori

        if actors == 'all':
            for vtk_data_source in self.scene3d.engine.scenes[0].children:
                if rando is True:
                    ori = random_orientation()
                else:
                    ori = orientation
                print("VTKDATA TYPE:", type(vtk_data_source))
                if isinstance(vtk_data_source, type(mayavi.sources.array_source.ArraySource())):
                    vtk_data_source.children[0].children[0].ipw.slice_position = 0

                elif type(vtk_data_source.children[0].children[0]) is not type(mayavi.core.module_manager.ModuleManager()):
                    vtk_data_source.children[0].children[0].actor.actor.orientation = ori

                elif isinstance(vtk_data_source.children[0].children[0], type(mayavi.core.module_manager.ModuleManager())):
                    for k in vtk_data_source.children[0].children[0].children:
                        if isinstance(k.actor, mayavi.components.actor.Actor):
                            k.actor.actor.orientation = ori
                        else:
                            pass   #k.actor.position = pos
                    #print("SECONDCHILD:", vtk_data_source.children[0].ch   ildren[0])

        elif actors == 'music':
            for i in self.mlab_calls:
                if rando is True:
                    ori = random_orientation()
                else:
                    ori = orientation
                i.actor.actor.orientation = ori

        elif actors == 'highlighter':
            for j in self.highlighter_calls:
                if rando is True:
                    ori = random_orientation()
                else:
                    ori = orientation
                j.actor.actor.orientation = ori ####Current Actor's Current Z-Plane's Position


    def set_text_positions(self, pos=np.array([0, 0, 0]), default=True, rando=False):

        def random_position():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            pos = np.asarray(list1, dtype=np.float16)
            return pos


        if default is True and rando is False:
            for l in range(0, len(self.text3d_calls)):
                self.text3d_calls[l].actor.actor.position = self.text3d_default_positions[l]
        elif rando is True and default is False:
            for m in range(0, len(self.text3d_calls)):
                self.text3d_calls[m].actor.actor.position = random_position()
        elif rando and default is False:
            for n in range(0, len(self.text3d_calls)):
                self.text3d_calls[n].actor.actor.position = pos

    #Basic Point Cloud transformation functions.
    def standard_reorientation(self, points, scale=1.):
        # TODO Maximum rescaling check.
        # TODO scale_function?  Need check to avoid float values.
        # TODO Scaling needs to be done with respect to musical, i.e. a musical key, and within the grid's available space.

        #TODO MAJOR: There is a 'scale' trait within an mlab actor. Use this for scaling? (it scales the size of points up as well..)

        points = midiart3D.transform_points_by_axis(points, positive_octant=True)
        points = midiart3D.delete_redundant_points(points, stray=False)
        points = points * scale
        return points


    def trim(self, points, axis='y', trim=0):
        Points_Odict = midiart3D.get_planes_on_axis(points, axis, ordered=True)

        # Trim (Trim by index in the list. An in-place operation.)
        [Points_Odict.pop(i) for i in list(Points_Odict.keys())[:trim]]

        # Restore to a coords_array.
        Restored_Points = midiart3D.restore_coords_array_from_ordered_dict(Points_Odict)
        return Restored_Points


    def zoom_to_coordinates(self, picker):
        print("Point", picker.point_id)
        picker.tolerance = 0.01
        picked = picker.actors
        print("Picker", picked)
        #print(picker.trait_names())
        print("Selection Point:", picker.pick_position)

        mproll = self.parent.pianorollpanel.pianoroll

        self.ret_x = picker.pick_position[0] * self.cpqn  #Account for cpqn here.
        self.ret_y = picker.pick_position[1]
        self.ret_z = picker.pick_position[2]

        #In scrollunits, which should == to pixels.

        #TODO..Conversions for cells, coords, and scrollunits?
        #10 pixels per cell
        #ScrollRate = Pixels/Scrollunit

        #Pixels to Cell --- User Grid.XYToCell()
        #Cell to Pixels -- Cell Row\Col * 10

        #Cell to ScrollUnits -- Cell * 10 / ScrollRate
        #Measure to ScrollUnits -- Measure * (Cell * PixelsperCell-->10 * CellsperMeasure-->(timesig_numerator*cellsperqrtrnote))

        #Cell to Mayavi_Coords --  Synced as ints.
        #MayaviCoords to Cell -- Synced as ints.

        #( 160 * 10) / (160 / 4 * (4 * 10)
        self.cur_scroll_x = (int(self.ret_x) *10) / mproll.GetScrollPixelsPerUnit()[0]  #Scrollrate / cells per measure ()
        self.cur_scroll_y = ((127-int(self.ret_y)) * 10) / mproll.GetScrollPixelsPerUnit()[1]   #Scrollrate Y / cells per two octaves == 24
        #TODO Fix this limit cap.
        if self.cur_scroll_y > 1040:   #Caps of scrolling at the bottom, so the rectangle doesn't go funky.
            self.cur_scroll_y = 1040    #Sash position affects this because num of pixels in client view relates to ViewStart().

        print("Coord", self.ret_x, self.ret_y, self.ret_z)
        if mproll is not None:

            #Zooms on middle click.  #TODO Math is not exact yet...
            mproll.Scroll(self.cur_scroll_x, self.cur_scroll_y)
            self.new_reticle_box()
        else:
            pass


    ###DEFINE MUSIC ANIMATION
    def animate(self, time_length, bpm=None, i_div=4, sleep=None):
        #TODO Re-doc this.
        """
            I_div should be 2 or 4. Upon a division of greater than 4, say 8, the millisecond delay becomes so small,
        that it is almost not even read properly, producing undesired results.
        Animation function that gives the impression of rendering 3D music. Does not play music.

        :param time_length:     Length of the piece to be rendered in the animation display: this determines the range
                                of the animation.
        :param bpm:             Beats per minutes of the music as an integer: this allows for the calculation of the
                                functions delay, and determines the speed of the animation scroll.

        For best results, select your bpm from the following list: (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30,
        32, 40, 48, 50, 60, 75, 80, 96, 100, 120, 125, 150, 160, 200, 240, 250, 300, 375, 400, 480, 500, 600, 625, 750,
        800, 1000, 1200, 1250, 1500, 1875, 2000, 2400, 2500, 3000, 3750, 4000, 5000, 6000, 7500, 10000, 12000, 15000,
        20000, 30000, 60000.)

        :param i_div:           Number of planescrolls per second: this determines the fineness of your animation.

        :return:

        IMPORTANT MATH:
        What is the equation for fps given the bpm and the frames per beat?

        VARIABLES:
        bpmm = beats per measure

        steps value = 1/i_div

        4 steps == 1 Measure

        i_div*bpmm = frames per measure
        fpm/bpmm = frames per beat

        COMPLETE LOGIC:
        **(bpm * ((i_div*bpmm)/bpmm))/60 = fps **

        Therefore, fpb == i_div.

        REDUCED EQUATION:
        (bpm * fpb)/60 = fps  (time signature does not matter here.)

        EXAMPLE:
        150*4 = 600fpm / 60s = 10fps
        10fps
        """
        import time
        if bpm is None or 0:
            bpm_delay = 100000
            nano_delay = 0
        else:
            bpm_delay = 10
            nano_delay = (60000000 / bpm / i_div)

        @mayavi.tools.animator.animate(delay=bpm_delay, ui=False)   #@mlab.animate, same thing.
        def animate_plane_scroll(x_length, delay, sleep=sleep):
            """
                Mlab animate's builtin delay has to be specified as an integer in milliseconds with a minimum of 10,
            and also could not be removed, so we subtracted .01 seconds (or 10 milliseconds) in a workaround delay of
            our own in order to compensate.

            :param x_length:    Length of the range of the animation plane along the x-axis.
                                (See music21.stream.Stream.highestTime)
            :param delay:       Int in microseconds.
            :return: N/A
            """
            #The "+ 1" in this range is a compensation value. For some unknown reason, the correct range is not being
            # fully animated. It's always 2 'i' range values off (which is 8 iterations if i_div is 4 because we're
            # incrementing at fractional step values) The desired range is still x_length, we just made it go a little
            #over that to make darn sure the whole range is captured, which makes it work as desired.
            for i in np.arange(0, (x_length + 1), 1/i_div):
                # print("%f %d" % (i, time.time_ns()))
                interval = delay
                t = int(time.time() * 1000000) % (interval)
                s = (interval - t)
                if sleep is None:
                    sleep = s / 1000000
                else:
                    sleep = 0
                time.sleep(sleep)  # Increasing this number speeds up plane scroll.  - .003525  .0035   .0029775025

                # print("timesleep:", (delay-.01))
                # self.image_plane_widget.ipw.slice_index = int(round(i))
                print(i)
                print(i == x_length * i_div)
                #print("Frame:", i)
                #j = self.image_plane_widget.ipw.slice_position - 1
                if i == x_length:   #Because we animate ACROSS our desired range max, we make sure that this condition is met.
                    #Destroy the volume_slice and rebuild it at the end of the animating generator function.
                    self.reset_volume_slice(self.grid3d_span)
                    #Fire a "loop_end" flag so we can turn off "movie_maker.record" if we intend to animate without generating frames.
                    self.loop_end = True
                    #Might change this later, for playback stuff.
                    if self.loop_end is True:
                        self.scene.scene.movie_maker.record = False

                    self.m_v.scene3d.anti_aliasing_frames = 8
                    #pass
                    return i, print("True")
                else:
                    self.image_plane_widget.ipw.slice_position = i    ###/i_div

                    yield ###print(i)

        #Leave for now.
        # mlab.start_recording()
        # mlab.animate(animate_plane_scroll, ms_delay, ui=True)
        # print(secs_delay)
        #animate_plane_scroll(int(time_length), int(nano_delay))

        self.animate1 = animate_plane_scroll(int(time_length), int(nano_delay))
        self.animate1._stop_fired()
        self.loop_end = False
        #self.i_list = [i for i in self.animate1]
        print("Animaties")

        # animate1.timer.Stop()
        # input("Press Enter.")
        # animate1.timer.Start()


    #Grid Constructor
    def insert_piano_grid_text_timeplane(self, length):
        ###Piano
        # MayaviPianoBlack = music21.converter.parse(r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\FL Midi Files\MidiPianoBlack.mid")
        # MayaviPianoWhite = music21.converter.parse(r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\FL Midi Files\MidiPianoWhite.mid")
        # #Acquire Piano Numpy Coordinates
        # PianoBlackXYZ = midiart3D.extract_xyz_coordinates_to_array(MayaviPianoBlack)
        # PianoWhiteXYZ = midiart3D.extract_xyz_coordinates_to_array(MayaviPianoWhite)
        PianoBlackNotes = MusicObjects.piano_black_notes()
        PianoWhiteNotes = MusicObjects.piano_white_notes()
        # Render Piano
        self.scene3d.disable_render = True
        mlab.points3d(PianoBlackNotes[:, 0], PianoBlackNotes[:, 1], (PianoBlackNotes[:, 2] / 4), color=(0, 0, 0),
                      mode='cube', scale_factor=1)
        mlab.points3d(PianoWhiteNotes[:, 0], PianoWhiteNotes[:, 1], (PianoWhiteNotes[:, 2] / 4), color=(1, 1, 1),
                      mode='cube', scale_factor=1)
        # mlab.outline()

        # Render Grid
        x1 = np.array(range(0, 127), dtype=np.float16)
        x2 = np.zeros(127)
        x3 = np.zeros(127)
        Grid = np.column_stack((x1, x2, x3))
        #mlab.points3d(Grid[:, 0], Grid[:, 1], Grid[:, 2], color=(1, 0, 0), mode="2dthick_cross", scale_factor=.75)
        mlab.points3d(Grid[:, 1], Grid[:, 0], Grid[:, 2], color=(1, 0, 0), mode="2ddash", scale_factor=1)
        mlab.points3d(Grid[:, 1], Grid[:, 2], Grid[:, 0], color=(1, 0, 0), mode="2ddash", scale_factor=1)

        ###---##Extended X Axis....
        x4 = np.array(range(0, int(length)), dtype=np.float16)
        x5 = np.zeros(int(length))
        x6 = np.zeros(int(length))
        Xdata = np.column_stack((x4, x5, x6))
        mlab.points3d(Xdata[:, 0], Xdata[:, 1], Xdata[:, 2], color=(1, 0, 0), mode="2dthick_cross", scale_factor=.75)

        # GridText
        x_txt = mlab.text3d(int(length), 0, 0, "X_Time-Rhythm-Duration.", color=(0, 1, 0), scale=4)
        y_txt = mlab.text3d(0, 127, 0, "Y_Frequency-Pitch.", color=(0, 1, 0), scale=4)
        z_txt = mlab.text3d(0, 0, 127, "Z_Dynamics-Velocity//Ensemble-Track.", color=(0, 1, 0), scale=4)
        self.text3d_calls.append(x_txt)
        self.text3d_default_positions.append(x_txt.actor.actor.position)
        self.text3d_calls.append(y_txt)
        self.text3d_default_positions.append(y_txt.actor.actor.position)
        self.text3d_calls.append(z_txt)
        self.text3d_default_positions.append(z_txt.actor.actor.position)
        # Grid Frequency Midpoint
        # mlab.text3d(0, 64, 0, "<---Midpoint.", color=(1, 0, 1), scale=10)

        # Add Measure Number Text to X Axis
        for i, m in enumerate(range(0, int(length), 4)):
            measures = mlab.text3d(m - 1, 0, -2, str(i+1), color=(1, 1, 0), scale=1.65)   #TODO m-1 lines up measures perfectly. When cpqn is fixed, remember to scale this value accordingly.
            self.text3d_calls.append(measures)
            self.text3d_default_positions.append(measures.actor.actor.position)
        self.volume_slice = self.insert_volume_slice(length)
        self.scene3d.disable_render = True



    ###OPENING ANIMATION
    ###-----------------
    ###Script Widget Shrink and Initial Camera Angle
    def establish_opening(self):
        scene = self.scene
        # scene.scene.x_minus_view()
        #self.image_plane_widget = self.engine.scenes[0].children[6].children[0].children[0]
        print("IPW TYPE:", type(self.image_plane_widget))
        self.image_plane_widget.ipw.origin = array([0., 0.0, 0.0])
        self.image_plane_widget.ipw.point1 = array([0.0, 127., 0.0])
        self.image_plane_widget.ipw.point2 = array([0.0, 0.0, 127.])
        self.image_plane_widget.ipw.slice_position = 1      #These calls eliminate those "white lines" created in the
        self.image_plane_widget.ipw.slice_position = 0      #construction and repositioning of the volume_slice.
        scene.scene.z_plus_view()
        scene.scene.camera.position = [-75.6380940108963, 154.49428308844531, 497.79655837964555]
        scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.04985772050601139, 0.9771694895609155, -0.20652843963290976]
        scene.scene.camera.clipping_range = [210.11552421145498, 882.5056024983969]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()



    ####TRAITS FUNCTIONS
    #-------------------
    ##-------------------------------------
    ###---------------------------------------------------------

    @on_trait_change('cur_changed_flag')
    def sync_positions_and_update(self):
        #On Current Actor activation.

        #self.remove_trait('position')
        print("Cur:", self.cur_ActorIndex)
        #print("GlyphSources:", self.sources)
        print("Sources length:", len(self.sources))
        #Note: There is the option to remove trait_syncing.
        #NOTE: removing a sync didn't seem to be working.....
        if self.cur_ActorIndex < 0:
            return
        print("self.cur", self.cur_ActorIndex)
        self.sources[self.cur_ActorIndex].actor.actor.sync_trait('position', self, mutual=False)
        print("Position trait one-way synced: actor.position ---to---> mayavi_view.position.")
        self.actors[self.cur_ActorIndex].sync_trait('cur_z', self, mutual=False)
        print("Cur_z trait one-way synced: actor.cur_z ---to---> mayavi_view.cur_z.")
        if len(self.sources) == 1 and self.cur_ActorIndex == 0:
            pass
        else:
            self.highlighter_transformation()
            self.new_reticle_box()
            #pass

    @on_trait_change('position')  #Split for a tested reason.
    def highlighter_actor_chase(self):
        # Align Highlighter on position change.
        if self.cur_ActorIndex < 0:
            return
        else:
            self.highlighter_transformation()
            self.new_reticle_box()

    @on_trait_change('position')  #Split for a tested reason.
    def select_moved_actor(self):
        #Select Actor in list box on position change.
        print("Actors Length:", len(self.actors))
        if len(self.actors) is not 0:
            alb = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox
            for i in range(0, len(self.actors)):
                #If it's selected, unselect it.
                if alb.IsSelected(i):
                    self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.Select(i, on=0)
        else:
            pass
        self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.Select(self.cur_ActorIndex)

        #Then, select the actor whose position was just changed by dragging the actor in the mayavi view.
        #TODO Causes a red error on startup and at some color loading because of pos changes, but non-breaking.
            ###This: >>> "4:19:02 AM: Error: Couldn't retrieve information about list control item 0."

    @on_trait_change('cur_z')
    def highlighter_plane_chase(self):
        # Align Z-value
        if self.cur_ActorIndex < 0:
            return
        self.highlighter_transformation()
        print("Highlighter Aligned")
        self.new_reticle_box()


    @on_trait_change('actor_deleted_flag')
    def colors_menu_delete(self):
        #If the deleted actor wasn't part of a colors import, this block won't do anything.
        if self.deleting_actor == '':
            pass
        else:
            #If all instances of a colors import are deleted, delete the export menu button for it.
            ref_list = [self.actors[j].colors_instance for j in range(0, len(self.actors))]
            if self.deleting_actor in ref_list:
                pass
            else:
                item_id = self.parent.menuBar.colors.FindItem(self.deleting_actor[-1])
                self.parent.menuBar.colors.Delete(item_id)
            print("Deletion Check...")


    @on_trait_change('actor_deleted_flag')
    def reset_index_attributes(self):
        #Reset actor.index attributes.
        for k in range(0, len(self.actors)):
            self.actors[k].index = k
        print("actor.index attributes reset")

    @on_trait_change('cpqn_changed_flag')
    def OnCellsPerQuarterNote_Changed(self):
        #self.highlighter_transformation()
        self.new_reticle_box()
        print("Establishing New Reticle Box...")

        #Reset orange reticle box. CHECK
        #Scale_factor for all actors.
        #Reset x-axis scaling?

        #for i in self.actors:


    ###Trait Sub-Functions
    ##-----------------------------------------------
    #@on_trait_change('cpqn_changed_flag')
    def new_reticle_box(self, zplane=None):
        if zplane is not None:
            pass
        else:
            zplane = 0   ###self.cur_z
#        if self.parent.parentpianorollpanel:

        #TODO Needs Cells per quarter note factored in. ----Once CellsPerQuarterNote is fixed.

        mproll = self.parent.pianorollpanel.pianoroll
        if mproll is not None:
            s_h = mproll.GetScrollPos(wx.HORIZONTAL)
            s_v = mproll.GetScrollPos(wx.VERTICAL)
            s_linex = mproll.GetScrollLineX()   #Set to 160 in pianroll (the grid), the equivalent of scrolling a full measure of columns..
            s_liney = mproll.GetScrollLineY()   #Set to 120, the equivalent of scrolling 2 octaves of rows.
            client_size = mproll.GetClientSize()
            print("CLIENT_SIZE", client_size)
            client_rect = mproll.GetClientRect()
            print("CLIENT_RECT", client_rect)

            #s_r = mproll.GetScroll

            #GRID CELL COORDINATES (Y, X)
            bottomleft = mproll.XYToCell((s_h * s_linex), (s_v * s_liney) + client_size[1] - 18)
            print("RETICLE_BOTTOM_LEFT", bottomleft)

            bottomright = mproll.XYToCell((s_h * s_linex) + client_size[0] -60, (s_v * s_liney) + client_size[1] - 18)
            print("RETICLE_BOTTOM_RIGHT", bottomright)

            topleft = mproll.XYToCell((s_h * s_linex), (s_v * s_liney))  #0 times whatever your scroll rate is equal to zero, so the top left at start is (0, 0)

            topright = mproll.XYToCell((s_h * s_linex) + client_size[0] -60, (s_v * s_liney))

            #Limiter, so the reticle doesn't turn into a triangle because of going below the grid area with (-1, -1) values...
            #If bottom would go below 0, (to -1, as it has been), then force it be zero and adjust top_left and top_right based on client_size from there.
            if bottomleft[1] == -1 and bottomright[1] == -1:

                topleft = mproll.XYToCell(mproll.CalcUnscrolledPosition(0, 0)) #New Topleft
                topright = mproll.XYToCell(mproll.CalcUnscrolledPosition(client_size[0], 0)) #New Topright
                #bottomright = mproll.XYToCell(mproll.CalcUnscrolledPosition(0,0)[0], )
                #Bottom is ( , 127)
                bottomleft = (127, topleft[1]) #New Bottomleft
                bottomright = (127, topright[1]) #New Bottomright

                print("RETICLE_BOTTOM_LEFT2", bottomleft)
                print("RETICLE_BOTTOM_RIGHT2", bottomright)
            else:
                pass




            reticle = np.asarray(np.vstack(((topleft[1], 127-topleft[0], 0),
                                 (topright[1], 127-topright[0], 0),
                                 (bottomright[1], 127-bottomright[0], 0),
                                 (bottomleft[1], 127-bottomleft[0], 0),
                                 (topleft[1], 127-topleft[0], 0))), dtype=np.float32)
            #In place slice reassignment.
            reticle[:, 0] = reticle[:, 0] / self.parent.pianorollpanel.pianoroll._cells_per_qrtrnote  #TODO Once cpqn is fixed. CHECK-- Now that cpqn is fixed, create a trait event for it so that this reticle--
                                                                                                      #TODO---(among other things) updates automatically when cpqn is changed.
            #Traits notification
            self.grid_reticle.mlab_source.trait_set(points=reticle)

            #Points Update
            #self.grid_reticle.mlab_source.points = reticle



            #TODO ALWAYS is behind be one update....FIXED!!!!
            #Compensatory scroll here.
            #self.cur_scroll_x = (int(self.ret_x) * 10) / mproll.GetScrollPixelsPerUnit()[0]
            #self.cur_scroll_y = ((127 - int(self.ret_y)) * 10) / mproll.GetScrollPixelsPerUnit()[1]
            #mproll.Scroll(1, 1)
            #mproll.Scroll(0, 0)
            #self.parent.pianorollpanel.pianoroll.Scroll(s_linex - 1, s_liney - 1)
            #self.parent.pianorollpanel.pianoroll.Scroll(s_linex, s_liney)

        else:
            pass


    def remove_grid_reticle(self):
        for i in self.highlighter_calls:
            if i == self.grid_reticle:
                i.remove()
                self.highlighter_calls.remove(i)


    def highlighter_transformation(self):
        for i in self.highlighter_calls:
            pos = self.sources[self.cur_ActorIndex].actor.actor.position
            i_z = pos[2]
            i_y = pos[1]
            i_x = pos[0]
            i_z_zerod = (i_z * -1) + i_z
            i_z_transformed = i_z_zerod + self.cur_z
            i_z_restored = i_z_transformed + i_z
            if i.name == "Z_Label":
                i_x_zerod = (i_x * -1) + i_x
                i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label.
                i_x_restored = i_x_transformed + i_x
                i.actor.actor.position = (i_x_restored, i_y, i_z_restored)
                i.text = "Z-Plane_%s" % self.cur_z
            elif i.name == "Actor_Label":
                i_x_zerod = (i_x * -1) + i_x
                i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label.
                i_x_restored = i_x_transformed + i_x
                i_y_zerod = (i_y * -1) + i_y
                i_y_transformed = i_y_zerod - 10
                i_y_restored = i_y_transformed + i_y
                i.actor.actor.position = (i_x_restored, i_y_restored, i_z_restored)  #Actor Label acts as "origin marker."
                i.text = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.GetItemText(self.cur_ActorIndex)
                #Actor label gets the same color as the "Current Actor's" color.
                i.actor.property.color = self.CurrentActor().color
            else:
                i.actor.actor.position = np.array([i_x, i_y, i_z_restored])


    ###
    ######------------------------------------------------


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

        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMusic21ConverterParseDialog, id=new_id1)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMusicodeDialog, id=new_id2)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMIDIArtDialog, id=new_id3)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMIDIArt3DDialog, id=new_id4)
        # TODO These aren't working as desired.....
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_actors_listbox, id=new_id5)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_zplanes, id=new_id6)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_pianorollpanel, id=new_id7)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_pycrust, id=new_id8)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_mayavi_view, id=new_id9)
        self.parent.mayavi_view_control_panel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_mainbuttonspanel, id=new_id10)

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
        #F10 is already used.... goes to the menubar
        entries[9].Set(wx.ACCEL_NORMAL, wx.WXK_F11, new_id10)

        accel = wx.AcceleratorTable(entries)
        self.parent.mayavi_view_control_panel.SetAcceleratorTable(accel)



if __name__ == '__main__':
    pass


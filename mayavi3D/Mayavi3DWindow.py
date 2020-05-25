
import sys, os

from midas_scripts import musicode, midiart, midiart3D, music21funcs

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'

import mayavi
from numpy import array
import numpy as np
import random
import music21





from mayavi import mlab, modules, sources, core, components
from mayavi.components import actor
from mayavi.sources import array_source
from mayavi.core import module_manager
#from mayavi.modules import image_plane_widget

from mayavi3D import MusicObjects

from gui import PianoRoll

import copy

from traits.api import HasTraits, Range, Instance, on_trait_change, Float, String, Int, Dict

from traitsui.api import View, Item, HGroup
from traits.trait_numeric import Array
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

#from traits.trait_types import Button

# from traits.trait_numeric import AbstractArray
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

    _points = Array(dtype=np.int)
    _array3D = Array(dtype=np.int8, shape=(5000, 128, 128))
    _stream = Any()  #TODO For exporting, finish.

    #For trait flagging.
    array3Dchangedflag = Int()
    pointschangedflag = Int()
    streamchangedflag = Int()

    ##For trait-syncing.
    cur_z = Int(90)  #         #Synced one-way to mayavi_view.cur_z trait.
    color = Tuple(0., 1., 0.)  #Synced two_way with the pipeline's current_actor.property.color trait.
    position = Array()         #Synced two-way with the pipeline's current_actor.actor.actor.position trait.


    # cur = Int()


    def __init__(self, mayavi_view, index):
        HasTraits.__init__(self)
        self.index = index
        self.mayavi_view = mayavi_view

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

    #def change_color(self, color):

    ##WORKING INSTANCE
    @on_trait_change("array3Dchangedflag")
    def actor_array3D_changed(self):
        print("actor_array3D_changed")
        print("actor_index  ", self.index)
        self._points = np.argwhere(self._array3D >= 1.0)

        self.mayavi_view.sources[self.index].mlab_source.trait_set(points=self._points)

    # def insert_array_data(self, array_2d, color=(0., 0., 0.), mode="cube", scale_factor=.25):
    # I don't think this is needed.
    # self.parent.pianorollpanel.zplanesctrlpanel.ZPlanesListBox.UpdateFilter()
    @on_trait_change("pointschangedflag")
    def actor_points_changed(self):
        print("actor_points_changed")
        print("actor_index ", self.index)
        new_array3D = np.zeros(self._array3D.shape, dtype=np.float64) #TODO Int 8 here?
        for p in self._points:
            new_array3D[p[0], p[1], p[2]] = 1.0
        self._array3D = new_array3D
        self.mayavi_view.sources[self.index].mlab_source.trait_set(points=self._points)
        print("sources trait_set after actor_points_changed")

    @on_trait_change('color')
    def show_color(self):
        print("COLOR TRAIT CHANGED:", self.color)

    @on_trait_change('position')
    def show_position(self):
        print("POSITION TRAIT CHANGED:", self.position)
        self.mayavi_view.cur = self.index #TODO Change mayavi_view.cur to curActorIndex




# mlab.options.offscreen = True

class Mayavi3idiView(HasTraits):
    scene3d = Instance(MlabSceneModel, ())
    view = View(Item('scene3d', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
                resizable=True)
    actor = Any()
    actors = List(Actor)

    cur = Int()
    cur_z = Int()
    cur_changed_flag = Int()

    position = Array()  #Synced one_way 'from' the pipeline current actor's position.(highlighter plane purposes)


    def __init__(self, parent):
        HasTraits.__init__(self)

        #self.on_trait_event(self._array3D_changed, 'array3Dchangedflag')
        self.parent = parent
        self.engine = self.scene3d.engine
        self.engine.start()  # TODO What does this do?
        self.scene = self.engine.scenes[0]   #TODO Refactor the name of this variable? (self.skene?)

        # Common Scene Properties #TODO Should these be traits? (I think grid3d_span should be...at least)
        self.grid3d_span = 127  # For right now.
        self.bpm = 540  # TODO Set based on music21.tempo.Metronome object.
        self.i_div = 2  #Upon further review, i_div IS frames per beat. I'll change this variable name later.
        #self.time_sig = '4/4' #TODO Set based on music21.meter.TimeSignature object.

        #Stream
        self.stream = music21.stream.Stream()



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

        self.midi = music21.converter.parse(r".\resources\Spark4.mid")
        #self.midi = midiart3D.extract_xyz_coordinates_to_array(self.midi)




        #TODO These become buttons.
        #self.Points = midiart3D.get_points_from_ply(r".\resources\sphere.ply")
        self.Points = MusicObjects.earth()
        self.Points = self.standard_reorientation(self.Points, 1.3)
        self.Points = np.asarray(self.Points, dtype=np.int64)
        self.Points = np.asarray(self.Points, dtype=np.float64)
        self.Points = self.trim(self.Points, axis='y', trim=0)
        self.Points = midiart3D.transform_points_by_axis(self.Points, positive_octant=True)
        #print("Points", self.Points[:, 2])



        self.SM_Span = self.midi.highestTime
        self.grid3d_span = self.SM_Span
        self.Points_Span = self.Points.max()
        #Draw Grid
        self.insert_piano_grid_text_timeplane(self.SM_Span)
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
        self.establish_highlighter_plane(0, color=(0, 1, 0), length=self.SM_Span)


        #self.points = self.Points


        # @mlab.show
        # self.scene3d.disable_render = False

        #self.insert_titles()     ##I had a 2nd call for a work session where I lost the camera. I may not need this now...
        self.establish_opening()     #TODO Write in a pass statement for when calls to this function are made from within the program; camera issue. Now Redundant?
        self.animate(160, self.SM_Span, i_div=2)
        #print("Animate")

        #Animator Instance. Instantiated upon the invocation of self.animate after which the animation is immediately stopped here.
        #self.animate1._stop_fired() #TODO Redundant. _stop_fired() now called within Animate after invocation of animate_plane_scroll.
        #print("Animation Stopped")

        ###RECORD python Scripts
        #mlab.start_recording(ui=True)


        self.insert_titles()
        #self.insert_note_text("3-Dimensional Music", 0, 164, 0, color=(1,0,1), opacity=.12, orient_to_camera=False, scale=3

    def redraw_mayaviview(self):
        mlab.clf()
        self.create_3dmidiart_display()

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
            return self.actors[self.cur]

    def append_actor(self, name, color):
        # self.add_trait(actor_name,Actor())
        print("append_actor")
        print('1')

        self.cur = len(self.actors)
        a = Actor(self, self.cur)

        #self.actor = a

        #TODO Can ALL this v here v go into the actor's init?
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

        # TODO self.on_trait_change(self.actor_stream_changed, 'actors.streamchangedflag')

        #TODO Move this to actor class?
        self.on_trait_change(self.actor_list_changed, 'actors[]')

        a.name = name
        a.color = color

        #Traits syncing goes here, if desired. (can't go in actor init, because the actor hasn't been appended to any lists yet...)
        #Simplifies access to the pipeline's properties\traits by configuring our "Actor()" class to have these directly.
        self.sources[self.cur].actor.property.sync_trait('color', a, mutual=True)
        print("Colors synced.")
        self.sources[self.cur].actor.actor.sync_trait('position', a, mutual=True)
        print("Position synced.")

        self.cur_changed_flag = not self.cur_changed_flag

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


    #TODO def actor_stream_changed(self):
        #print("actor_stream_changed")


    def actor_list_changed(self):
        print("actor_list_changed")


    ###MAYAVI_VIEW INSERT AND MANIPULATION FUNCTIONS
    #-------------------
    ##----------------------------------------------
    ###---------------------------------------------------------------------------------------

    def insert_array_data(self, array_2d, color=(0, 0, 0), mode="cube", name='', scale_factor=.25):
        # print(array_2d)
            #color = lambda x: super().actors[super().cur].color
        print("insert_array_data")
        mlab_data = mlab.points3d(array_2d[:, 0], array_2d[:, 1], array_2d[:, 2], color=self.actors[self.cur].color, mode=mode, name=name,
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
        text_stream = musicode.mc.translate(mc, text)
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
        self.insert_note_text("The Midas 3idiArt Display", 0, 137, 0, color=(1, 1, 0), orient_to_camera=True,
                              scale=7)
        ###Note: affected by top_mayaviview_split sash position.
        self.title = self.insert_title("3-Dimensional Music", color=(1, 0, 1), height=.82, opacity=.12, size=.65)

    #Volume Slice Functions
    def insert_volume_slice(self, length=127):
        # Time_ScrollPlane
        # x,y,z = np.mgrid[0:127, 0:127, 0:127]
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
        #self.loop_end = False
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
                                         color=(1,1,1), line_width=2.5, name="White Edges", opacity=.35, tube_radius=None)
        self.highlighter_calls.append(plane_edges)
        #self.mlab_calls.append(plane_edges)
        if grandstaff:
            stafflines = MusicObjects.grand_staff(z_value=z_points, length=length)
            gclef = MusicObjects.create_glyph(r".\resources\TrebleClef.png", y_shift=59, z_value = z_points)
            fclef = MusicObjects.create_glyph(r".\resources\BassClef.png", y_shift=44.3, z_value = z_points)
            #for j in grandstaff:
            #Grand Staff Lines
            self.gscalls = mlab.plot3d(stafflines[:, 0], stafflines[:, 1], stafflines[:, 2], color=(0,1,0), name="Staff Lines", opacity=.65, tube_radius=None)
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
        z_label = mlab.text3d(-40, 0, 0, "Z-Plane_%s" % z_marker, color=(.55, .55, .55), name="Z_Label", orient_to_camera=False, scale=4)
        self.highlighter_calls.append(z_label)
        #INITIAL Highlighter positions.
        #self.cur_z = 90  #Matches position variable.
        for h in self.highlighter_calls:
            if h.name == "Z_Label":
                h.actor.actor.position = np.array([position[0]-40, position[1], position[2]])
                h.text = "Z-Plane_%s" % str(90)
            else:
                h.actor.actor.position = position
        #return plane


    # TODO Tie this to a button.
    def remove_highlighter_plane(self):
        for i in self.highlighter_calls:
            # Remove from scene3d.
            i.remove()
        # Clear reference list.
        self.highlighter_calls.clear()


    #Position, orientation, and #TODO origin functions.
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

        def random_position():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            pos = np.asarray(list1, dtype=np.float64)
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

                elif type(vtk_data_source.children[0].children[0]) is not type(mayavi.core.module_manager.ModuleManager()):
                    vtk_data_source.children[0].children[0].actor.actor.position = pos

                elif isinstance(vtk_data_source.children[0].children[0], type(mayavi.core.module_manager.ModuleManager())):
                    for k in vtk_data_source.children[0].children[0].children:
                        if isinstance(k.actor, mayavi.components.actor.Actor):
                            k.actor.actor.position = pos
                        else:
                            pass   #k.actor.position = pos

                    #print("SECONDCHILD:", vtk_data_source.children[0].ch   ildren[0])
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


    def set_actor_orientations(self, orientation=np.array([0,0,0]), actors=None, rando=False):

        def random_orientation():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            ori = np.asarray(list1, dtype=np.float64)
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
            pos = np.asarray(list1, dtype=np.float64)
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
            #over that to make darn sure the whole range is captured.
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
        mlab.points3d(PianoBlackNotes[:, 0], PianoBlackNotes[:, 1], (PianoBlackNotes[:, 2] / 4), color=(0, 0, 0),
                      mode='cube', scale_factor=1)
        mlab.points3d(PianoWhiteNotes[:, 0], PianoWhiteNotes[:, 1], (PianoWhiteNotes[:, 2] / 4), color=(1, 1, 1),
                      mode='cube', scale_factor=1)
        # mlab.outline()

        # Render Grid
        x1 = np.array(range(0, 127), dtype=np.float64)
        x2 = np.zeros(127)
        x3 = np.zeros(127)
        Grid = np.column_stack((x1, x2, x3))
        mlab.points3d(Grid[:, 0], Grid[:, 1], Grid[:, 2], color=(1, 0, 0), mode="2dthick_cross", scale_factor=.75)
        mlab.points3d(Grid[:, 1], Grid[:, 0], Grid[:, 2], color=(1, 0, 0), mode="2ddash", scale_factor=1)
        mlab.points3d(Grid[:, 1], Grid[:, 2], Grid[:, 0], color=(1, 0, 0), mode="2ddash", scale_factor=1)

        ###---##Extended X Axis....
        x4 = np.array(range(0, int(length)), dtype=np.float64)
        x5 = np.zeros(int(length))
        x6 = np.zeros(int(length))
        Xdata = np.column_stack((x4, x5, x6))
        mlab.points3d(Xdata[:, 0], Xdata[:, 1], Xdata[:, 2], color=(1, 0, 0), mode="2dthick_cross", scale_factor=.75)

        # GridText
        x_txt = mlab.text3d(int(length), 0, 0, "X_Time-Rhythm-Duration.", color=(0, 1, 0), scale=4)
        y_txt = mlab.text3d(0, 127, 0, "Y_Frequency-Pitch.", color=(0, 1, 0), scale=4)
        z_txt = mlab.text3d(0, 0, 127, "Z_Dynamics-Velocity-Ensemble.", color=(0, 1, 0), scale=4)
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
            measures = mlab.text3d(m, 0, -2, str(i+1), color=(1, 1, 0), scale=1.65)
            self.text3d_calls.append(measures)
            self.text3d_default_positions.append(measures.actor.actor.position)
        self.volume_slice = self.insert_volume_slice(length)



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
    def sync_positions(self):

        #self.remove_trait('position')
        print("Cur:", self.cur)
        print(self.sources)
        print("Sources length:", len(self.sources))
        #Note: There is the option to remove trait_syncing.
        #NOTE: removing a sync didn't seem to be working.....
        if self.cur < 0:
            return
        print("self.cur", self.cur)
        self.sources[self.cur].actor.actor.sync_trait('position', self, mutual=False)
        print("Position trait one-way synced: actor.position ---to---> mayavi_view.position.")
        self.actors[self.cur].sync_trait('cur_z', self, mutual=False)
        print("Cur_z trait one-way synced: actor.cur_z ---to---> mayavi_view.cur_z.")
        if len(self.sources) == 1 and self.cur == 0:
            pass
        else:
            for i in self.highlighter_calls:
                pos = self.sources[self.cur].actor.actor.position
                i_z = pos[2]
                i_y = pos[1]
                i_x = pos[0]
                i_z_zerod = (i_z * -1) + i_z
                i_transformed = i_z_zerod + self.cur_z
                i_restored = i_transformed + i_z
                if i.name == "Z_Label":
                    i_x_zerod = (i_x * -1) + i_x
                    i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label.
                    i_x_restored = i_x_transformed + i_x
                    i.actor.actor.position = (i_x_restored, i_y, i_restored)
                    i.text = "Z-Plane_%s" % self.cur_z

                else:
                    i.actor.actor.position = np.array([i_x, i_y, i_restored])


    @on_trait_change('position')
    def highlighter_actor_chase(self):
        # Align Positions
        if self.cur < 0:
            return
        else:
            for i in self.highlighter_calls:
                pos = self.position
                i_z = pos[2]
                i_y = pos[1]
                i_x = pos[0]
                # Zero, transform, restore for z value
                i_z_zerod = (i_z * -1) + i_z
                i_transformed = i_z_zerod + self.cur_z
                i_restored = i_transformed + i_z
                # Zero, transform, restore for x value
                if i.name == "Z_Label":
                    i_x_zerod = (i_x * -1) + i_x
                    i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label.
                    i_x_restored = i_x_transformed + i_x
                    i.actor.actor.position = (i_x_restored, i_y, i_restored)
                    i.text = "Z-Plane_%s" % self.CurrentActor().cur_z
                else:
                    i.actor.actor.position = (i_x, i_y, i_restored)
        for i in range(0, len(self.actors)):
            alb = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox
            #If it's selected, unselect it.
            if alb.IsSelected(i):
                self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.Select(i, on=0)
        #Then, select the actor whose position was just changed by dragging the actor in the mayavi view.
        self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.Select(self.cur)


    @on_trait_change('cur_z')
    def highlighter_plane_chase(self):
        # Align Z-value
        if self.cur < 0:
            return
        for i in self.highlighter_calls:
            pos = self.sources[self.cur].actor.actor.position
            i_z = pos[2]
            i_y = pos[1]
            i_x = pos[0]
            ##--Z
            #Convert to zero, #Transform from zero, #Add original value back
            i_z_zerod = (i_z*-1) + i_z
            i_transformed = i_z_zerod + self.cur_z
            i_restored = i_transformed + i_z
            ##--X
            #Zero, transform, restore for x value
            if i.name == "Z_Label":
                i_x_zerod = (i_x * -1) + i_x
                i_x_transformed = i_x_zerod - 40 #Always will be minus 40 for this label.
                i_x_restored = i_x_transformed + i_x
                i.actor.actor.position = np.array([i_x_restored, i_y, i_restored])
                i.text = "Z-Plane_%s" % self.cur_z
            else:
                i.actor.actor.position = np.array([i_x, i_y, i_restored])
            print("Highlighter Aligned")




if __name__ == '__main__':
    pass


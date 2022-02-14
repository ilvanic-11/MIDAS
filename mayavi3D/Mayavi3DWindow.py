import copy
import random
import threading
import asyncio

import music21
import wx    # TODO how to do simpler imports (i.e. just what we need instead of all of wx)
import time
import numpy as np
# import numpy_indexed as npi

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
import mayavi
# import copy
# import cv2
# import sys, os

from midas_scripts import midiart, midiart3D   # ,  music21funcs
# from gui import PianoRoll

from numpy import array
from mayavi import mlab,  sources, core, components   # modules
from mayavi.components import actor
from mayavi.sources import array_source
from mayavi.core import module_manager
from mayavi.tools import animator
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene
from mayavi3D import MusicObjects

from traits.api import on_trait_change, String, Any, HasTraits, Instance, Bool
#, Float, Int, HasTraits, Range, Instance, Button
from traitsui.api import View, Item   #, Group
from traits.trait_numeric import Array
from traits.trait_types import List, Tuple, Int   #, Any
from tvtk.pyface.scene_editor import SceneEditor

# from traitsui.api import View, Item, HGroup
# from mayavi.modules import image_plane_widget
# from traits.trait_types import Button
# from traits.trait_numeric import AbstractArray
# from traits.trait_types import Function
# from traits.trait_types import Any
# from traits.trait_types import Str
#
# from traits.trait_types import Method
# from vtkmodules import vtkRenderingCore


class Actor(HasTraits):
    # For general purposes as traits.
    name = String()

    _points = Array(dtype=np.float32)

    _array4D = Array()   #dtype=np.int8, shape=(5000, 128, 128, 4)
    #_array4D = Array(dtype=np.int8, shape=(5000, 128, 128, 4))
    #5000  #[x, y, z] coordinates of [on\off, Duration, Velocity, Smallest-Allowed-Duration(SAD)?, color?] values.
    #Velocity doesn't need to be a uniquely stored element on the 4th dimension. It's already our z-value.
    #Example CurrentActor()._array4D[x,y,z] == np.array([0,0,0,0,0]). We have 5 elements here. We already have velocity,
    #so I changed it to 4 elements.
    #Edit: I was wrong, velocity needs to be an independent value because of the track<--to\\from-->velocity modes I
    #       wish to establish. HOWEVER, Smallest ALlowed Duration is derived inherently from Cells Per Quarter Note and
    #Note Duration. Thus, SAD is redundant.

    _stream = Any()  # TODO For exporting, finish. Not used atm.

    # an array3d for *Experiment stuff
    # _draw_array3D = Array(dtype=np.int8, shape=(5000, 128, 128))

    # For trait flagging.
    array4Dchangedflag = Int()
    pointschangedflag = Int()
    # streamchangedflag = Int()

    # For trait-syncing.
    cur_z = Int(90)
    # Synced one-way to mayavi_view.cur_z trait.
    previous_z = None

    color = Tuple(1., 0., 0.)  # Synced two_way with the pipeline's current_actor.property.color trait.
                               #Because of this, we didn't need a change_color() function.
    position = Array()         # Synced two-way with the pipeline's current_actor.actor.actor.position trait.

    # cur = Int()


    def __init__(self, mayavi_view, index):
        HasTraits.__init__(self)
        self.index = index
        self.m_v = mayavi_view
        self.toplevel = self.m_v.parent

        self.colors_instance = ""  #Denotes to what instance of a loaded color image this actor belongs. (call1, call2, etc.)
        self.part_num = 0  #For stream.Part purposes, used in colors function.
        self.priority = 0
        self.cpqn = self.toplevel.pianorollpanel.pianoroll._cells_per_qrtrnote
        self.old_cpqn = None

        #Our _array4D allows us vectorized access to individual point coordinates via the power of numpy.
        self._array4D = np.zeros(dtype=np.int8, shape=(self.m_v.grid_cells_length, 128, 128, 5))

        #TODO Pages workaround for CPQN-changed data loss.
        self._array_pages = []

        self._all_points = None
        self._cur_plane = None


        #*
        #Working Attempt at individual array3Ds for every zplane.
        #self._array3D_dict = OrderedDict(zip([i for i in range(0, 128, 1)],
        #                          [self._array3D[:, :, i] for i in range(0, 128, 1)]))
        #Restore method.   ***Would I need to restore?
        #np.dstack([self._array3D_dict[i] for i in self._array3D_dict.keys()])
        #*



        #TODO This will mess up.     ???


        #self.get_ON_points_as_odict()

        #??? Necessary?
        points =  self.get_points_with_all_data()

        # #Todo Delete? Redundant? 04/13/2021
        # ##Copied from traits_update function. I need these class attributes.
        # try:
        #     #An OrderedDict.
        #     self._all_points = midiart3D.get_planes_on_axis(points, array=True)
        #
        # except IndexError:
        #
        #     points = np.array(
        #         [[0, 0, 0]])  # A temporary origin point that acts as a fill, so that get_planes on axis executes.
        #
        #     self._all_points = midiart3D.get_planes_on_axis(points, array=True)
        #
        # try:
        #     #The key value value pair of above Odict accessed by current zplane.
        #
        #     self._cur_plane = self._all_points[self.cur_z]  # Key error can happen here.... #TODO FIX
        #     #print("Type_Cur_Plane", type(self._cur_plane))
        #
        #     print(self._cur_plane)
        #
        #     # Account for cpqn. All 'x' values.  X axis "slice" item assignment here.
        #     self._cur_plane[:, 0] = self._cur_plane[:, 0] / self.cpqn
        #
        #     #print("HERE, BABY")
        #     self._all_points[self.cur_z] = self._cur_plane
        #
        # except Exception as e:
        #     print(e)
        #     print("Exception: Your 'points' do not have this --'%s'-- zplane value" % self.cur_z, e)


        #_array3D = np.full([2500, 128, 128, 3], np.array([0, 1, 90]))

        #CHANGE the float dtype from 64 to 16 manually on init.
        #self._points.dtype = np.float16
        #print("_Points", self._points, self._points.dtype)

    #3d numpy array---> True\False map of existing coords for rapid access.


    def change_array4D(self, array4D):
        self._array4D = array4D
        self.array4Dchangedflag = not self.array4Dchangedflag


    #2d numpy array---> List of actual coordinates
    def change_points(self, points):
        #TODO Make into pianoroll property. 12/31/2021
        print("points_shape", points.shape)
        pr = self.m_v.parent.pianorollpanel.pianoroll

        duration_ratio = pr.GetMusic21DurationRatio()

        #If we don't have durations data, (say, from a point cloud or picture), supply it anyway.
        if points.shape[1] < 4:
            #NOTE: substitute_durations1/substitute_duration2 == desired music21.duration.quarterLength
            #See music21.note.Note().duration.quarterLength.as_integer_ratio()
            substitute_durations1 = np.full((len(points), 1),
                                                  duration_ratio[0], dtype=np.float16)
            print("substitute_durations1", substitute_durations1)
            substitute_durations2 = np.full((len(points), 1),
                                                  duration_ratio[1], dtype=np.float16)
            print("substitute_durations2", substitute_durations2)

            #music21 NOTE: 1.0 is 1 quarternote in quarterLength duration units.
            #A point should now be : [x, y, z, d1, d2]

            print("points_shape2", points.shape)
            self._points = np.hstack([points, substitute_durations1, substitute_durations2])
            #self._points = np.r_['1,2,0', points, substitute_durations1, substitute_durations2]
            #self._points.dtype = np.float16
            print("_points_dtype", self._points.dtype)
            print("Change_points:", self._points)
            print("Change_points_shape:", self._points.shape)
        else:
            self._points = points
            #self._points.dtype = np.float16
        self.pointschangedflag = not self.pointschangedflag


    def get_points_with_all_data(self, z=None, _array4D=None):
        """
            This function is intended to expand the power of np.argwhere for musical purposes with our data setup.
        It's functionality concatenates the duration data extracted from an _array4D onto the points acquired from
        np.argwhere. (i.e instead of points  np.array([[x, y, z]]) we get instead points np.array([[x, y, z, d1, d2]]).
        As Midas scales, new data may be concatenated as needed to our coords_array structuring of points.

        Furthermore, it will be an intended feature that the two duration values always be at the end of the _array4D
        and our new coords_arrays. Therefore, new arrays will always look like :
        np.array([[x, y, z, a, b, c, ..., d1, d2]]) pending the addition of new data per note.

        :param _array4D:       This usually will be the m_v.CurrentActor()._array4D, but may be user-supplied else-wise.
        :param z:              If z is specified, only operate on the current zplane, else operate on entire _array4D.
        :return:               Our new coords_array of points with duration data.
        """
        if _array4D is None:
            _array4D = self._array4D
        else:
            _array4D = _array4D

        points = np.argwhere(_array4D[:, :, :, 0] == 1.0) if z is None else np.argwhere(_array4D[:, :, z, 0] == 1.0)
        print("Z", z)
        #This if statement isn't working....
        if z:
            _z = np.full((len(points), 1), z, dtype=np.int8) #int, because floats cannot be indices.
            points = np.column_stack([points, _z])
        print("BITCH")

        # if z is None:
        #     #z = self.cur_z
        #     points = np.argwhere(_array4D[:, :, :, 0] == 1.0)
        # else:
        #     #z = z
        #     points = np.argwhere(_array4D[:, :, z, 0] == 1.0)

        print("POINTS", points)
        print("POINTS_dtype", points.dtype)
        # if points.size == 0:
        #     return
        #else:
        _dur1 = []
        _dur2 = []
        for point in points:
            print("-point-", point)
            #print("-point_data_in_array4D", _array4D[point[0], point[1], point[2]])
            _dur1.append(_array4D[point[0], point[1], point[2], 2])
            _dur2.append(_array4D[point[0], point[1], point[2], 3])
        _dur_array1 = np.array(_dur1, dtype=np.float32).reshape((len(points), 1))  #was 16?
        _dur_array2 = np.array(_dur2, dtype=np.float32).reshape((len(points), 1))  #was 16?
        print("durray1", _dur_array1)
        print("durray2", _dur_array2)
        #(len(points), 1)
        #points = np.r_['1,2,0', points, _dur_array1, _dur_array2]
        points = np.hstack([points, _dur_array1, _dur_array2])

        #points.dtype = np.float32
        print("POINTS; get_points_with_all_data", points)
        print("Points_dtype:", points.dtype)
        return points


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


    @on_trait_change("array4Dchangedflag")
    def actor_array4D_changed(self):
        #print("actor_index  ", self.index)

        #Reacquire cpqn
        self.cpqn = self.toplevel.pianorollpanel.pianoroll._cells_per_qrtrnote
        #print("_POINTS Type", type(self._points), self._points.dtype)

        #CORE
        self.get_ON_points_as_odict()  #Returns an OrderedDict()
        self._points = midiart3D.restore_coords_array_from_ordered_dict(self._all_points)
        #self._points = midiart3D.delete_select_points(self._points, [[0, 0, 0]], tupl=False)

        print("r4Dchangedflag_points", self._points) #[[x,y,z,d1,d2]
                                                      #[x,y,z,d1,d2]
                                                      #[x,y,z,d1,d2]   #vstacked?
                                                      #[x,y,z,d1,d2]]

        try:
            #THIS IS WHERE WE WILL GET A WORKING VERSION OF DISPLAYING DURATIONS. IT WILL BE BASED ON CHOP_UP_NOTES()
            points = np.column_stack([self._points[:,0], self._points[:,1], self._points[:,2]]) #[x,y,z]
            #points = np.vstack([points, new_points])
            print("DISPLAY_POINTS:", points)
            self.m_v.sources[self.index].mlab_source.trait_set(
                points=points)  # TODO Redundant? Traitset happens on x axis item slice reassignment above.
            #NOTE: Cannot trait_set with an empty array, one without points. Clear instead? Workaround?
        except Exception as e:
            print("Error Here; array_4d_changed", e)
            pass
        print("actor_array4D_changed")


    #Named weird, I don't frickin care right now.
    def get_ON_points_as_odict(self):
        """

        :return:
        """
        #points = np.argwhere(self._array4D[:, :, :, 0] == 1.0)

        points = self.get_points_with_all_data()

        try:
             #An OrderedDict.
            self._all_points = midiart3D.get_planes_on_axis(points, array=True)

        except IndexError:
            points = np.array(
                [[0, 0, 0]])  # A temporary origin point that acts as a fill, so that get_planes_on_axis executes.
            # TODO Write in methods to delete this, so that midi exports don't have a useless note in every file?
            self._all_points = midiart3D.get_planes_on_axis(points, array=True)

        # print("ARRAYCHECK", cur_plane[0])
        # print("ARRAYTYPECHECK", type(cur_plane[0]))

        try:
            #The zplane 'value' where self.cur_z is the 'key.
            self._cur_plane = self._all_points[self.cur_z]  # Key error can happen here.... #TODO FIX?
            print(self._cur_plane)

            # CRITICAL: Account for cpqn. All 'x' values.  X axis "Slice" item assignment here.
            # CRITICAL: CPQN Compensation here.
            self._cur_plane[:, 0] = self._cur_plane[:, 0] / self.cpqn   #TODO For selection sending between Actors, bool condition needed here to shut this off for those sends.

            # CRITICAL: Insert compensation into _all_points.
            #Reinsert into _all_points via key access.
            self._all_points[self.cur_z] = self._cur_plane
        except Exception as e:
            print(e)
            print("Exception; get_ON_points_as_odict: Your 'points' do not have this --'%s'-- zplane value." % self.cur_z, e)
        #return self._all_points


    @on_trait_change("pointschangedflag")
    def actor_points_changed(self):
        cpqn = self.toplevel.pianorollpanel.pianoroll._cells_per_qrtrnote
        #print("CPQN", cpqn)

        new_array4D = np.zeros(self._array4D.shape, dtype=np.int8)
        for p in np.arange(0, len(self._points), 1):   #TODO MAJOR self._points WILL CONTAIN our core update data. However, the
                                                       # m_v traits set will not.  04/11/2021
            #CORE --- A Values-Setting Operation
            try:
                ##IN ORDER
                #ON
                new_array4D[int(self._points[p][0]), int(self._points[p][1]), int(self._points[p][2])][0] = 1.0   #TODO Account for cpqn.  * cpqn

                #VELOCITY
                new_array4D[int(self._points[p][0]), int(self._points[p][1]), int(self._points[p][2])][1] = \
                    int(self._points[p][2])
                #2 BECAUSE z IS our velocity from imported points.

                #DURATION
                #SUPER NOTE!
                # --Duration needs two values that work together as a ratio on order to acquire an appropriate
                # --float value for music21.duration.quarterLength.
                # --See music21.duration.quarterLength.as_integer_ratio().
                # --THIS allows us to maintain our _array4D as dtype of int8, saving memory.
                #DUR1
                new_array4D[int(self._points[p][0]), int(self._points[p][1]), int(self._points[p][2])][2] \
                    = int(self._points[p][3])

                #DUR2
                new_array4D[int(self._points[p][0]), int(self._points[p][1]), int(self._points[p][2])][3] \
                    = int(self._points[p][4])

                #PianoRoll SetCellSizes  based on new duration data
                #self.toplevel.pianorollpanel.pianoroll.SetCellSize(127-p[1], p[0],
                                                                   #(self._points[p][3]/self._points[p][4]), 1)


                #    int(self._points[p][3] * 10000)
                #print("DURATION:", int(self._points[p][3] * 10000))

                #SMALLEST ALLOWED NOTE --- ?? This is inherently derived from duration and cpqn. Eliminate?
                #cell_draw_size = duration.quarterLength * cpqn
                #new_array4D[int(self._points[p][0]), int(self._points[p][1]), int(self._points[p][2])][4] = \


            except Exception as e:
                print("EXCEPTION; actor_points_changed:", e)

        self.m_v.parent.pianorollpanel.pianoroll.cur_array4d = self._array4D = new_array4D

        #self._points[:, 0] = self._points[:, 0]

        #TODO MAJOR NOTE: trait_set only takes standard coords_arrays. SOOO, with our new core data update, we have
        # handle every individual case with this new line:
        update_points = np.r_['1,2,0', self._points[:, 0], self._points[:, 1], self._points[:, 2]]
        #print("UPDATE_POINTS", update_points)

        self.m_v.sources[self.index].mlab_source.trait_set(points=update_points)
        #print("sources trait_set after actor_points_changed")

        print("actor_points_changed")


    @on_trait_change('color')
    def show_color(self):
        #print("COLOR TRAIT CHANGED:", self.color)
        pass


    @on_trait_change('position')
    def show_position(self):
        #TODO Doc and refigure this. 12/02/2021
        #print("POSITION TRAIT CHANGED:", self.position)
        self.m_v.cur_ActorIndex = self.index



# mlab.options.offscreen = True
class Mayavi3idiView(HasTraits):
    scene3d = Instance(MlabSceneModel, ())

    #scene2 = Instance(MlabSceneModel, ())

    view = View(Item('scene3d', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
                resizable=True)

    actor = Any()
    actors = List(Actor)
    #center = Tuple()
    #point1 = Array()
    #point2 = Array()
    normal = Array()

    cur_ActorIndex = Int()
    previous_ActorIndex = None
    cur_z = Int()

    cpqn = Int(1)   #Startup cpqn
    old_cpqn = None

    cpqn_changed_flag = Bool()

    cur_changed_flag = Int()

    actor_deleted_flag = Bool()

    position = Array()  #Synced one_way 'from' the pipeline current actor's position.(highlighter plane purposes)

    # Stream
    stream = music21.stream.Stream()

    def __init__(self, parent):
        HasTraits.__init__(self)

        #self.on_trait_event(self._array4D_changed, 'array4Dchangedflag')
        self.parent = parent

        self.engine = self.scene3d.engine
        self.engine.start()  # TODO What does this do?
        self.scene = self.engine.scenes[0]
        self.figure = self.scene3d.mayavi_scene

        #TODO Write new handlers that deal with imports that exceed this value. 12/02/2021
        self.grid_cells_length = 256  #512  #1250 #2500   #Rename to "grid_cells_x_max"?
        #NOTE: If this is a high number, colors imports will be unusably slow.

        # Common Scene Properties #TODO Should these be traits? (I think grid3d_span should be...at least)
        self.grid3d_span = 254  # For right now.
        self.bpm = 160  # TODO Set based on music21.tempo.Metronome object.  #TODO Make into a trait? 03/15/2021
        self.frames_per_beat = 2  #Upon further review, i_div IS frames per beat.
        #self.time_sig = '4/4' #TODO Set based on music21.meter.TimeSignature object.  Make this a trait???

        #Durations flags.
        self.durations = True
        self.durations_in_first_empty = False

        #Calls for colors ---for importing and exporting.
        self.colors_calling = False
        self.colors_call = 0   #No color calls yet. #TODO Make this part of the actor class in new method that doesn't include the actor listbox name.
        self.colors_name = ""
        self.colors_increment = 1

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
        self.scene.scene.movie_maker.record = False

        #Imports Colors
        #SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT?
        self.clr_dict_list = midiart.get_color_palettes(r".\resources\color_palettes")
        #print("B palm.")
        #Append FLStudioColors to clr_dict_list
        self.clr_dict_list.update([("FLStudioColors", midiart.FLStudioColors)])
        #Set FL colors default variable here.
        self.current_color_palette = self.clr_dict_list["FLStudioColors"]
        #Division to float colors here.
        self.current_mayavi_palette = midiart.convert_dict_colors(self.current_color_palette, both=True) #invert=False)#
        #NOTE: These two attributes are modified by the MidiartDialog() function --> OnChangeColor().

        #print("C palm.")


        self.quick_plane = True  #TODO create toggle


        #TODO Should this be in main MIDAS_wx?
        self.current_palette_name = "FLStudioColors"   #Palette on startup.


        #Grid Construct
        self.mlab_calls = []  #TODO Note: mlab.clf() in the pyshell does not clear this list. Also, rename to mlab_calls? 12/01/2021
        self.text3d_calls = []
        self.text3d_default_positions = []
        self.highlighter_calls = []

        self.volume_slice = True   #Determines slice as actual mlab.volume_slice if True, else mlab.mesh (surface) if False.
        self.slice = None
        self.slice_edges = None

        self.sources = list()
        #TODO I don't like "sources" as the name of this list. Sources is actually a trait in the mayavi pipeline somewhere....
        #TODO Also, sources and mlab_calls are virtually the same thing. Delete one?

        #self.append_actor("0")

    #TODO For exporting
    def Append_Streams(self):
        pass

    #Interactive Visualization Establisher.
    #@on_trait_change('scene3d.engine.current_scene.scene.activated')
    @on_trait_change('scene3d.activated')
    def create_3dmidiart_display(self):
        # if figure is None:
        #     figure = self.scene3d.mayavi_scene
        # else:
        #     figure = figure

        self.scene3d.disable_render = True


        #self.scene.render_window.line_smoothing = True

        #self.midi = music21.converter.parse(r".\resources\Spark4.mid")
        #self.midi = midiart3D.extract_xyz_coordinates_to_array(self.midi)


        #TODO These become buttons.
        #self.Points = midiart3D.get_points_from_ply(r".\resources\sphere.ply")
        # self.Points = MusicObjects.earth()
        # self.Points = self.standard_reorientation(self.Points, 1.3)
        # self.Points = np.asarray(self.Points, dtype=np.int16)
        # self.Points = np.asarray(self.Points, dtype=np.float16)
        # self.Points = self.trim(self.Points, axis='y', trim=0)
        # self.Points = midiart3D.transform_points_by_axis(self.Points, positive_octant=True)
        #print("Points", self.Points[:, 2])


        #self.SM_Span = self.midi.highestTime
        #self.grid3d_span = self.SM_Span
        #self.Points_Span = self.Points.max()
        #Draw Grid
        self.insert_piano_grid_text_timeplane(self.grid3d_span, figure=None)
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
        self.establish_highlighter_plane(0, color=(0, 1, 0), length=self.grid3d_span, figure=None)

        #self.points = self.Points

        # @mlab.show
        # self.scene3d.disable_render = False

        #self.insert_titles()     ##I had a 2nd call for a work session where I lost the camera. I may not need this now...

        #self.establish_opening()     #TODO Write in a pass statement for when calls to this function are made from within the program; camera issue. Now Redundant?
        self.animate(self.grid3d_span, 160, frames_per_beat=2)
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
        #new_picker = vtkRenderingCore.vtkPointPicker()

        #TODO ERROR---this doesn't trigger after deleting and redrawing the mayavi view. July 30th, 2020.
        #TODO Does mlab.clf() eliminate the picker object?

        self.scene3d.disable_render = False

    #This did a double picker add, so not what we want. (this trait is fired twice on Midas load.)
    # @on_trait_change('scene3d.engine.current_scene.scene.activated')
    # def real_picker_rebind(self):
    #     self.scene.on_mouse_pick(self.zoom_to_coordinates, type='point', button='Middle')

    @on_trait_change('scene3d.activated')
    def rebind_picker(self):

        #self.scene.on_mouse_pick(self.zoom_to_coordinates, type='point', button='Middle', remove=True)
        self.scene.on_mouse_pick(self.parent.zoom_to_coordinates, type='point', button='Middle', remove=False)

    # @mlab.clf
    # def clear_lists(self):
    #     self.sources.clear()
    #     self.mlab_calls.clear()
    #     self.highlighter_calls.clear()
    #     self.text3d_calls.clear()
    #     self.text3d_default_positions.clear()



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


        self.cur_ActorIndex = len(self.actors)
        a = Actor(self, self.cur_ActorIndex)


        #self.actor = a

        #TODO Can ALL this v-here-v go into the actor's init?
        # self.sources.append(None)
        self.actors.append(a)
        appending_data = self.insert_array_data(a._array4D, color=color, mode="cube", name=name, scale_factor=1.0)
        self.sources.append(appending_data)
        self.mlab_calls.append(appending_data)


        #TODO Move this to actor class?
        #TODO Dahfuq was this?! 11/08/20
        self.on_trait_change(self.actor_stream_changed, 'actors.streamchangedflag')
        #self.on_trait_change(self.actor_list_changed, 'actors[]')



        #Traits syncing goes here, if desired. (can't go in actor init, because the actor hasn't been appended to any lists yet...)
        #Simplifies access to the pipeline's properties\traits by configuring our "Actor()" class to have these directly.
        self.sources[self.cur_ActorIndex].actor.property.sync_trait('color', a, mutual=True)
        self.sources[self.cur_ActorIndex].actor.actor.sync_trait('position', a, mutual=True)


        a.name = name
        a.color = color

        #This is\was intended to handle a micro-case where the actor_label in the highlighter plane wasn't updating
        #after ALL actors had been deleted and THEN  the new_actor button is clicked.
        # if len(self.actors) != 0:
        #     if self.colors_calling is False:
        #         self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.Activate_Actor(self.cur_ActorIndex)
        #     else:
        #         pass
        # else:
        #     pass

        #print("Flag 2")
        self.cur_changed_flag = not self.cur_changed_flag

        #self.scene3d.disable_render = False

    @on_trait_change('cur')
    def current_actor_changed(self):
        pass
        #print("current_actor_changed")



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
        #print("actor_stream_changed")
        pass


    def actor_list_changed(self):
        #print("actor_list_changed")
        pass

    ###MAYAVI_VIEW INSERT AND MANIPULATION FUNCTIONS
    #-------------------
    ##----------------------------------------------
    ###---------------------------------------------------------------------------------------

    def insert_array_data(self, array_2d, color=None, figure=None, mode="cube", name='', scale_factor=.25, ):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        # print(array_2d)
            #color = lambda x: super().actors[super().cur].color
        #print("insert_array_data")
        if color is None:
            color = self.actors[self.cur_ActorIndex].color
        else:
            color = color
        mlab_data = self.scene.scene.mlab.points3d(array_2d[:, 0], array_2d[:, 1], array_2d[:, 2],
                                  color=color, figure=figure, mode=mode, name=name,
                                  scale_factor=scale_factor)
        #mlab.points3d
        return mlab_data


    def insert_music_data(self, in_stream, color=(0., 0., 0.), figure=None, mode="cube", name='', scale_factor=1):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        array_data = midiart3D.extract_xyz_coordinates_to_array(in_stream)
        array_data = array_data.astype(float)
        # print(array_data)
        mlab_data = self.scene3d.mlab.points3d(array_data[:, 0], array_data[:, 1], array_data[:, 2],
                                  color=color, figure=figure, mode=mode, name=name,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data


    def insert_text_data(self, mc, text, color=(0., 0., 0.), figure=None, mode="cube", name='', scale_factor=1):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        text_stream = self.parent.musicode.mc.translate(mc, text)
        text_array = midiart3D.extract_xyz_coordinates_to_array(text_stream)
        mlab_data = self.scene3d.mlab.points3d(text_array[:, 0], text_array[:, 1], text_array[:, 2], color=color, figure=figure,
                                  mode=mode, name=name,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data


    ###TITLES and NOTE inserts.
    def insert_note_text(self, text, x=0, y=154, z=0, color=(0, 0, 1), figure=None, opacity=1, orient_to_camera=True, scale=3):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        mlab_t3d = mlab.text3d(text=text, x=x, y=y, z=z, color=color, figure=figure, opacity=opacity,
                               orient_to_camera=orient_to_camera, scale=scale)
        self.text3d_calls.append(mlab_t3d)
        self.text3d_default_positions.append(mlab_t3d.actor.actor.position)
        # TODO
        ## def insert_image_data(self, imarray_2d, color=(0,0,0), mode="cube", scale_factor = 1):


    ###SCENE TITLEd
    def insert_title(self, text, color=(1, .5, 0), figure=None, height=.7, opacity=1.0, size=1):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        return mlab.title(text=text, color=color, figure=figure, height=height, opacity=opacity, size=size)


    # Leave this here for now.
    def insert_titles(self):
        self.insert_note_text("The Midas Display", 0, 137, 0, color=(1, 1, 0), orient_to_camera=True,
                              scale=7)
        ###Note: affected by top_mayaviview_split sash position.
        self.title = self.insert_title("3-Dimensional Music", color=(1, 0, 1), height=.82, opacity=.12, size=.65)



    #Volume Slice Functions
    # def insert_volume_slice(self, ):
    #     # Time_ScrollPlane
    #     # x,y,z = np.mgrid[0:127, 0:127, 0:127]
    #     self.scene3d.disable_render = True
    #
    #     self.scene3d.disable_render = False
    #     return self.volume_slice


    def insert_volume_slice(self,length=127, volume_slice=None, figure=None):
        figure = self.scene3d.mayavi_scene if figure is None else figure

        if volume_slice is None:
            volume_slice = self.volume_slice  #Equals class variable
        else:
            volume_slice = volume_slice       #Equals user set variable.
            self.volume_slice = volume_slice  #Reset stored class variable.

        self.scene3d.disable_render = True

        if volume_slice is True:
            if self.grid3d_span is not None:
                length = self.grid3d_span
            else:
                length = length
            xh, yh, zh = np.mgrid[0:int(length), 0:254, 0:254]
            # Scalars_1 = (x+y+z)
            Scalars_2 = np.zeros((int(length), 254, 254))
            # xtent = np.array([0, 127, 0, 127, 0, 127])
            self.image_plane_widget = mlab.volume_slice(xh, yh, zh, Scalars_2, figure=figure, opacity=.7, plane_opacity=.7, plane_orientation='x_axes',
                              transparent=True)

            #if self.volume_slice is not None:
            self.slice = self.image_plane_widget.parent.parent
            print(self.image_plane_widget)

            self.anchor_volume_slice()
            # self.image_plane_widget.ipw.origin = array([0., 0., 0.])
            # self.image_plane_widget.ipw.point1 = array([0.0, 127., 0.0])
            # self.image_plane_widget.ipw.point2 = array([0.0, 0.0, 127.])
            # self.image_plane_widget.ipw.slice_position = 1
            # self.image_plane_widget.ipw.slice_position = 0

            # Makes it impossible to rotate the planescroll
            self.image_plane_widget.ipw.margin_size_x = 0
            self.image_plane_widget.ipw.margin_size_y = 0


        else:
            x1, y1, z1 = (0, 0, 0)  # | => pt1
            x2, y2, z2 = (0, 127, 0)  # | => pt2
            x3, y3, z3 = (0, 0, 127)  # | => pt3
            x4, y4, z4 = (0, 127, 127)  # | => pt4

            self.slice = mlab.mesh([[x1, x2],
                                    [x3, x4]],  # | => x coordinate
                                   [[y1, y2],
                               [y3, y4]],  # | => y coordinate
                                   [[z1, z2],
                               [z3, z4]],  # | => z coordinate
                                   color=(0,0,1), figure=figure, line_width=5.0, mode='sphere', name="Blue Surface",
                                   opacity=.625, scale_factor=2,
                                   tube_radius=None)

            linebox2 = MusicObjects.line_square2()
            self.slice_edges = mlab.plot3d(linebox2[:, 0], linebox2[:, 1], linebox2[:, 2] + .25,
                                    color=(1, 1, 1), figure=figure, line_width=.5, name="Slice Edges", opacity=1.,
                                    tube_radius=None)

        self.scene3d.disable_render = False

        #self.image_plane_widget.ipw.sync_trait('point1', self, mutual=False)
        #self.image_plane_widget.ipw.sync_trait('point2', self, mutual=False)
        #self.image_plane_widget.ipw.poly_data_algorithm.sync_trait('normal', self, mutual=False)
        #self.on_trait_change(self.anchor_volume_slice, 'point1')
        #self.on_trait_change(self.anchor_volume_slice, 'point2')
        #self.on_trait_change(self.anchor_volume_slice, 'normal')


        #center,normal trait of ipw is 'read-only', so mutual can only be False for this.
        #"Center trait one-way - synced: ipw.center - --to - --> mayavi_view.center."

        return self.slice, self.slice_edges


    def reset_volume_slice(self, length=127, volume_slice=False):

        if volume_slice is None:
            volume_slice = self.volume_slice  #Equals class variable
        else:
            volume_slice = volume_slice       #Equals user set variable.

        if self.grid3d_span is not None:
            length = self.grid3d_span
        else:
            length = length
        self.slice.remove()
        if self.slice_edges is not None:
            self.slice_edges.remove()
        self.insert_volume_slice(length=length, volume_slice=volume_slice)
        self.volume_slice = volume_slice

        #self.insert_volume_slice(length)


    #Highlighter Plane functions.
    def establish_highlighter_plane(self, z_points=0, z_marker=90, position = np.array([0, 0, 90]), color=(0, 1, 0),
                                    figure=None, grandstaff=True, length=None):
        figure = self.scene3d.mayavi_scene if figure is None else figure

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
                           [x3, x4]],  # | => (x, coordinate

                          [[y1, y2],
                           [y3, y4]],  # | => y, coordinate

                          [[z1, z2],
                           [z3, z4]],  # | => z) coordinate

                                  color=color, figure=figure, line_width=5.0, mode='sphere', name="Green Surface",
                          opacity=.125, scale_factor=1, tube_radius=None)  # black#extent=(-50, 128, -50, 128, 114, 114)
        #self.mlab_calls.append(plane)
        #TODO This is a mayavi bug. I had to name the .name trait in a separate line. 04/09/2021
        plane.name = "Green Surface"
        self.highlighter_calls.append(plane)
        #print("GREEN_HIGHLIGHTER_PLANE_INDEX", self.highlighter_calls.index(plane))
        #White Edges
        plane_edges = mlab.plot3d(linebox[:, 0], linebox[:, 1], linebox[:, 2]+.25,
                                         color=(1,1,1), figure=figure, line_width=.5, name="White Edges", opacity=1.,
                                         tube_radius=None)
        plane_edges.name = "White Edges"
        self.highlighter_calls.append(plane_edges)
        #self.mlab_calls.append(plane_edges)
        if grandstaff:
            stafflines = MusicObjects.grand_staff(z_value=z_points, length=length)
            gclef = MusicObjects.create_glyph(r".\resources\TrebleClef.png", y_shift=59, z_value = z_points)
            fclef = MusicObjects.create_glyph(r".\resources\BassClef.png", y_shift=44.3, z_value = z_points)
            #for j in grandstaff:
            #Grand Staff Lines
            self.gscalls = mlab.plot3d(stafflines[:, 0], stafflines[:, 1], stafflines[:, 2], color=(0,1,0),
                                       figure=figure, line_width=.5, name="Staff Lines", opacity=1., tube_radius=None)
            self.gscalls.name = "Staff Lines"
            #Treble Clef
            self.gclef_call = self.scene3d.mlab.points3d(gclef[:, 0], gclef[:, 1], gclef[:, 2], color=(0,1,0), figure=figure,
                                            mode='cube', name="Treble Clef", opacity=.015, scale_factor=.25)
            #Bass Clef
            self.fclef_call = self.scene3d.mlab.points3d(fclef[:, 0], fclef[:, 1], fclef[:, 2], color=(0,1,0), figure=figure,
                                            mode='cube', name="Bass Clef", opacity=.015, scale_factor=.25)
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

        a_label = mlab.text3d(-40, -10, 90, "Actor_None",
                              color=(0.6196078431372549, 0.8196078431372549, 0.6470588235294118), # (0, 1., .75) (158, 209, 165)
                              figure=figure,
                              name="Actor_Label",
                              orient_to_camera=False,
                              scale=4)
        z_label = mlab.text3d(-40, 0, 90, "Z-Plane_%s" % z_marker, color=(.55, .55, .55), figure=figure,
                              name="Z_Label", orient_to_camera=False, scale=4)
        self.highlighter_calls.append(a_label)
        self.highlighter_calls.append(z_label)

        self.initial_reticle = np.asarray(np.vstack(((0, 127 - 0, 0),
                                                     (147, 127 - 0, 0), #149
                                                     (147, 127 - 24, 0), #149, 22
                                                     (0, 127 - 24, 0),   #22
                                                     (0, 127 - 0, 0))), dtype=np.float32)
        ##Red Grid Reticle Box
        self.grid_reticle = mlab.plot3d(self.initial_reticle[:, 0],  self.initial_reticle[:, 1],
                                        self.initial_reticle[:, 2], color=(1,.42, 0), figure=figure, line_width=2.,
                                        name="Red Edges", opacity=1., tube_radius=None, tube_sides=12)
        self.grid_reticle.name = "Red Edges"
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
            # elif h.name == "Red Edges":
            #      h.actor.actor.trait_set(position = np.array([0., 0., 0.]))
            else:
                h.actor.actor.position = position


    def set_grid_reticle_position(self, z):
        self.grid_reticle.actor.actor.trait_set(position=z)
        #self.grid_reticle.actor.actor.position = np.array([0, 0, z])
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
            self.highlighter_transformation(labels_only=True)

                    #print("SECONDCHILD:", vtk_data_source.children[0].children[0])
        elif actors == 'music':
            for i in self.mlab_calls:
                if rando is True:
                    pos = random_position()
                else:
                    pos = position
                i.actor.actor.position = pos
            self.highlighter_transformation()

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


    def generate_plane_scroll2(self, x_length=None, bpm=None, frames_per_beat=None, volume_slice=None):
        generation = []
        x_length = self.grid3d_span if x_length is None else x_length
        bpm = self.bpm if bpm is None else bpm
        frames_per_beat = self.frames_per_beat if frames_per_beat is None else frames_per_beat
        volume_slice = self.volume_slice if volume_slice is None else volume_slice
        #                    # Equals class variable                   # Equals user set variable.

        fps = (bpm * frames_per_beat) / 60  # frames_per_second
        dbf = 1 / fps


        sleep = dbf  ####/frames_per_beat    #TODO CHECK THIS MATH just one more....time..... :p Nice. :)
        print("SLEEPIES", sleep)
        if volume_slice:
            ipw = self.image_plane_widget.ipw
            ipw2 = None
        else:
            ipw = self.slice.actor.actor
            ipw2 = self.slice_edges.actor.actor
        for i in np.arange(1, (x_length + 1), 1 / frames_per_beat):
            generation.append(i)
        return generation


    ###DEFINE MUSIC ANIMATION
    #@asyncio.coroutine
    def generate_plane_scroll(self, x_length=None, bpm=None, frames_per_beat=None):  #volume_slice=None
        """
            Mlab animate's builtin delay has to be specified as an integer in milliseconds with a minimum of 10,
        and also could not be removed, so we subtracted .01 seconds (or 10 milliseconds) in a workaround delay of
        our own in order to compensate. #Todo Delete after next commit. Fixed with InfiniteTimer.

        :param x_length:    Length of the range of the animation plane along the x-axis.
                            (See music21.stream.Stream.highestTime)
        :return: N/A
        """




        x_length = self.grid3d_span if x_length is None else x_length
        bpm = self.bpm if bpm is None else bpm
        frames_per_beat = self.frames_per_beat if frames_per_beat is None else frames_per_beat
        #volume_slice = self.volume_slice if volume_slice is None else volume_slice
        #                    # Equals class variable                   # Equals user set variable.



        fps = (bpm * frames_per_beat) / 60   #frames_per_second
        dbf = 1 / fps                        #delay_between_frames

        #dbf = 1 / fps                        #delay_between_frames
        #fps = (bpm * frames_per_beat) / 60   #frames_per_second
        #bpm = 60/(fpb*dbf)

        # Todo calculate into generate_plane_scroll() and add to yield_midi() function in Playback.
        #Calculate nano_delay for sleep call based on bpm and frames_per_beat input.
        # if bpm is None or 0:
        #     #bpm_delay = 100000
        #     nano_delay = 0
        # else:
        #     #bpm_delay = 10
        #     nano_delay = (60000000 / bpm / frames_per_beat)
        # #print("%f %d" % (i, time.time_ns()))
        # interval = nano_delay
        # t = int(time.time() * 1000000) % (interval)
        # s = (interval - t)
        # if sleep is None:
        #     sleep = s / 1000000
        # else:
        #     sleep = 0
        # sleep = sleep / frames_per_beat

        sleep = dbf   ####/frames_per_beat    #TODO CHECK THIS MATH just one more....time..... :p Nice. :)
        print("SLEEPIES", sleep)
        # The "+ 1" in this range is a compensation value. For some unknown reason, the correct range is not being
        # fully animated. It's always 2 'i' range values off (which is 8 iterations if i_div is 4 because we're
        # incrementing at fractional step values) The desired range is still x_length, we just made it go a little
        # over that to make darn sure the whole range is captured, which makes it work as desired.


        print("Volume_Bool:", self.volume_slice)
        if self.volume_slice is True:
            print("Volume_Bool:", self.volume_slice)
            ipw = self.image_plane_widget.ipw
            ipw2 = None
        else:
            print("Volume_Bool:", self.volume_slice)
            ipw = self.slice.actor.actor
            ipw2 = self.slice_edges.actor.actor


        for i in np.arange(1, (x_length + 1), 1 / frames_per_beat):   #Start at 0 or 1?

            #print("Sleep", sleep)

             # Increasing this number speeds up plane scroll.  - .003525  .0035   .0029775025

            # print("timesleep:", (delay-.01))
            # self.image_plane_widget.ipw.slice_index = int(round(i))

            #print(i)
            #print(i == x_length * frames_per_beat)

            # print("Frame:", i)
            # j = self.image_plane_widget.ipw.slice_position - 1
            if i == x_length:  # Because we animate ACROSS our desired range max, we are making darn sure that this
                # condition is met.
                # Destroy the volume_slice and rebuild it at the end of the animating generator function.
                self.reset_volume_slice(self.grid3d_span, volume_slice=True)
                # Fire a "loop_end" flag so we can turn off "movie_maker.record" if we intend to animate without generating frames.
                self.loop_end = True
                # Might change this later, for playback stuff.
                if self.loop_end is True:
                    self.scene.scene.movie_maker.record = False

                self.scene3d.anti_aliasing_frames = 8  # TODO Check this again.
                # pass
                return i #print("True")

            else:
                # # self.scene3d.disable_render=True
                # #self.scene3d.render_window.make_current()

                time.sleep(sleep)  #If our first tick generated is 1, which it is, and our starting position is 0
                                   #then time.sleep needs to happen in between 0 and our first tick.
                                   #Ergo, here.....

                if self.volume_slice == True:
                    #ipw.trait_set(slice_position=i)  ##
                    ipw.slice_position = i                  #/i_div
                    ## self.scene3d.disable_render=False
                    print("IPW", i)

                elif self.volume_slice == False:
                    pos = np.array([i, 0, 0])
                    ##ipw.trait_set(position=pos)
                   # print("IPW", ipw)
                    ##ipw2.trait_set(position=pos)
                   # print("IPW2", ipw2)
                    # # self.scene3d.disable_render=False
                    ipw2.position = ipw.position = pos
                    print("IPW", i)
                    print("IPW2", i)
                yield

                                  #And NOT here....!

                # #print("IPW_Current_Thread", threading.currentThread())
                # #print("IPW_Current_Thread_Name", threading.currentThread().getName())
                # #print("IPW_allThreads", threading.enumerate())
                # #print("IPW_allThreadsCount", threading.active_count())
                #from asyncio.sleep(sleep)
                ###print(i)


    def animate(self, time_length, bpm=None, frames_per_beat=4):
        #TODO Re-doc this.
        """
            This function defines an animator.Animator()-decorated generator function, creates an instance of it, and
        stops it immediately.

        Notes:
            Frames_per_beat. should be 2 or 4. Upon a division of greater than 4, say 8, the millisecond delay becomes
        so small, that it is almost not even read properly, producing undesired results.
        Animation function that gives the impression of rendering 3D music. Does not play music. #Todo in progress....

        :param time_length:         Length of the piece to be rendered in the animation display: this determines the
                                    range of the animation.

        :param bpm:                 Beats per minutes of the music as an integer: this allows for the calculation of the
                                    functions delay, and determines the speed of the animation scroll.

        For best results, select your bpm from the following list: (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30,
        32, 40, 48, 50, 60, 75, 80, 96, 100, 120, 125, 150, 160, 200, 240, 250, 300, 375, 400, 480, 500, 600, 625, 750,
        800, 1000, 1200, 1250, 1500, 1875, 2000, 2400, 2500, 3000, 3750, 4000, 5000, 6000, 7500, 10000, 12000, 15000,
        20000, 30000, 60000.)

        :param frames_per_beat:     Number of planescrolls per beat: this determines the fineness of your animation.

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

        REDUCED EQUATION: (Frames per Second from Beats per Minute and Frames per Beat)
        (bpm * fpb)/60 = fps  (time signature does not matter here.)

        DELAY BETWEEN FRAMES:
        1/fps = dbf

        EXAMPLE:
        150*4 = 600fpm / 60s = 10fps
        10fps
        """


        @mayavi.tools.animator.animate(delay=0, ui=False, support_movie=False)   #@mlab.animate, same thing.
        #Mlab's animator is maintained, as in unchanged\not edited. 04/05/2021  #TODO Create derived, it is changed again. 04/09/2021
        def animate_plane_scroll(x_length=time_length, bpm=bpm, frames_per_beat=frames_per_beat):
            for scroll in self.generate_plane_scroll(x_length=x_length, bpm=bpm, frames_per_beat=frames_per_beat):
                yield scroll
        #Leave for now.
        # mlab.start_recording()
        # mlab.animate(generate_plane_scroll, ms_delay, ui=True)
        # print(secs_delay)
        #generate_plane_scroll(int(time_length), int(nano_delay))

        self.animate1 = animate_plane_scroll(int(time_length), bpm, frames_per_beat=2)
        #self.parent.planescroll_animator = Animator(0, )

        #self.animate1.timer = InfiniteTimer(0, self.animate1.__next__)
        self.animate1._stop_fired()
        self.loop_end = False
        #self.i_list = [i for i in self.animate1]
        print("Animaties")

        # animate1.timer.Stop()
        # input("Press Enter.")
        # animate1.timer.Start()


    #Grid Constructor
    def insert_piano_grid_text_timeplane(self, length, volume_slice=None, figure=None):   ###figure=None,
        figure = self.scene3d.mayavi_scene if figure is None else figure

        if volume_slice is None:
            volume_slice = self.volume_slice  # Equals class variable
        else:
            volume_slice = volume_slice  # Equals user set variable.

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
        self.scene3d.mlab.points3d(PianoBlackNotes[:, 0], PianoBlackNotes[:, 1], (PianoBlackNotes[:, 2] / 4), color=(0, 0, 0),
                      figure=figure, mode='cube', scale_factor=1)
        self.scene3d.mlab.points3d(PianoWhiteNotes[:, 0], PianoWhiteNotes[:, 1], (PianoWhiteNotes[:, 2] / 4), color=(1, 1, 1),
                      figure=figure, mode='cube', scale_factor=1)
        # mlab.outline()

        # Render Grid
        x1 = np.array(range(0, 127), dtype=np.float16)
        x2 = np.zeros(127)
        x3 = np.zeros(127)
        Grid = np.column_stack((x1, x2, x3))
        #self.scene3d.mlab.points3d(Grid[:, 0], Grid[:, 1], Grid[:, 2], color=(1, 0, 0), mode="2dthick_cross", scale_factor=.75)
        self.scene3d.mlab.points3d(Grid[:, 1], Grid[:, 0], Grid[:, 2], color=(1, 0, 0), figure=figure, mode="2ddash", scale_factor=1)
        self.scene3d.mlab.points3d(Grid[:, 1], Grid[:, 2], Grid[:, 0], color=(1, 0, 0), figure=figure, mode="2ddash", scale_factor=1)

        ###---##Extended X Axis....
        x4 = np.array(range(0, int(length)), dtype=np.float16)
        x5 = np.zeros(int(length))
        x6 = np.zeros(int(length))
        Xdata = np.column_stack((x4, x5, x6))
        self.scene3d.mlab.points3d(Xdata[:, 0], Xdata[:, 1], Xdata[:, 2], color=(1, 0, 0), figure=figure,
                      mode="2dthick_cross", scale_factor=.75)

        # GridTe
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
            measures = mlab.text3d(m - 1, 0, -2, str(i+1), color=(1, 1, 0), figure=figure, scale=1.65)
            #TODO m-1 lines up measures perfectly. When cpqn is fixed, remember to scale this value accordingly.
            self.text3d_calls.append(measures)
            self.text3d_default_positions.append(measures.actor.actor.position)

        self.insert_volume_slice(length=length, volume_slice=volume_slice, figure=figure)
        # if self.volume_slice is True:
        #     self.slice, self.slice_edges = self.insert_volume_slice(length=length, volume_slice=volume_slice)[0], self.insert_volume_slice(length=length, volume_slice=volume_slice)[1]
        # else:
        #     self.slice = self.insert_volume_slice(length=length, volume_slice=volume_slice)
        #self.volume_slice = self.insert_volume_slice(length)
        self.scene3d.disable_render = True


    ###OPENING ANIMATION
    ###-----------------
    ###Script Widget Shrink and Initial Camera Angle
    def establish_opening(self):
        #scene = self.scene
        # scene.scene.x_minus_view()
        #self.image_plane_widget = self.engine.scenes[0].children[6].children[0].children[0]
        print("IPW TYPE:", type(self.image_plane_widget))

        self.anchor_volume_slice()
        # self.image_plane_widget.ipw.origin = array([0., 0.0, 0.0])
        # self.image_plane_widget.ipw.point1 = array([0.0, 127., 0.0])
        # self.image_plane_widget.ipw.point2 = array([0.0, 0.0, 127.])
        # self.image_plane_widget.ipw.slice_position = 1      #These calls eliminate those "white lines" created in the
        # self.image_plane_widget.ipw.slice_position = 0      #construction and repositioning of the volume_slice.

        self.scene.scene.z_plus_view()
        self.scene.scene.camera.position = [-75.6380940108963, 154.49428308844531, 497.79655837964555]
        self.scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        self.scene.scene.camera.view_angle = 30.0
        self.scene.scene.camera.view_up = [0.04985772050601139, 0.9771694895609155, -0.20652843963290976]
        self.scene.scene.camera.clipping_range = [210.11552421145498, 882.5056024983969]
        self.scene.scene.camera.compute_view_plane_normal()
        self.scene.scene.render()


    ####TRAITS FUNCTIONS
    #-------------------
    ##-------------------------------------
    ###---------------------------------------------------------

    @on_trait_change('cur_changed_flag')
    def sync_positions_and_update(self):
        #On Current Actor activation.

        #self.remove_trait('position')
        #print("Cur:", self.cur_ActorIndex)
        #print("GlyphSources:", self.sources)
        #print("Sources length:", len(self.sources))
        #Note: There is the option to remove trait_syncing.
        #NOTE: removing a sync didn't seem to be working.....
        if self.cur_ActorIndex < 0:
            self.parent.pianorollpanel.pianoroll._table._cur_actor = None
            return
        self.parent.pianorollpanel.pianoroll._table._cur_actor = self.actors[self.cur_ActorIndex]
        #print("self.cur", self.cur_ActorIndex)
        self.sources[self.cur_ActorIndex].actor.actor.sync_trait('position', self, mutual=False)
        #print("Position trait one-way synced: actor.position ---to---> mayavi_view.position.")
        self.actors[self.cur_ActorIndex].sync_trait('cur_z', self, mutual=False)
        #print("Cur_z trait one-way synced: actor.cur_z ---to---> mayavi_view.cur_z.")
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
            #print("Flag 5?")
            #print("Colors_calling", self.colors_calling)
            print("Colors_increment:", self.colors_increment)

            #This block may not be necessary now.
            # if self.colors_calling is True:
            #     print("Colors_increment:", self.colors_increment)
            #     if self.colors_increment != 16:
            #         pass
            #     else:
            #         print("Flag 6")
            #         print("Highlighter_transformation already called, passing....")
            #         #self.highlighter_transformation()

            #This was a fun detail; it stopped 16 weird extra self.highlighter_transformation() calls at the end
            #of a colors load
            if self.colors_calling is True and self.scene3d.disable_render is False:  #self.scene3d.disable_render?
                return
            else:
                #print("Flag 7")
                self.highlighter_transformation()
            #self.highlighter_transformation()
            self.new_reticle_box()


    @on_trait_change('position')  #Split for a tested reason.
    def select_moved_actor(self):
        #Select Actor in list box on position change.
        #print("Actors Length:", len(self.actors))
        alb = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox
        if len(self.actors) is not 0:
            for i in range(0, len(self.actors)):
                #If it's selected, unselect it.
                if alb.IsSelected(i):
                    alb.Select(i, on=0)
        else:
            pass

        alb.Select(self.cur_ActorIndex, on=1)
        alb.Focus(self.cur_ActorIndex)
        #Then, select the actor whose position was just changed by dragging the actor in the mayavi view.
        #TODO Causes a red error on startup and at some color loading because of pos changes, but non-breaking.
            ###This: >>> "4:19:02 AM: Error: Couldn't retrieve information about list control item 0."


    @on_trait_change('cur_z')
    def highlighter_plane_chase(self):
        # Align Z-value
        if self.cur_ActorIndex < 0:
            return
        print("Flag 4?")
        self.highlighter_transformation()
        #print("Highlighter Aligned")
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
            #print("Deletion Check...")


    @on_trait_change('actor_deleted_flag')
    def reset_index_attributes(self):
        #NOTE: This function has weird pycharm introspection quirks. An if-else statement wasn't working when it should,
        #'self.actors' is throwing a ""Expected type 'Sized', got 'List' instead"" warning, among others. Beware.

        alb = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox

        #Reset actor.index attributes.
        for k in range(0, len(self.actors)):
            self.actors[k].index = k
        #print("actor.index attributes reset")
        print("actor.index attributes reset.")

        # .filter has nothing to do with each actors "index." It has to do with values calculated in tandem with the
        # GTLP.actor_scrolled position.
        ##This call reduces the ordered range of elements in .filter by one, because deletion.
        alb.filter = [f for f in range(0, len(alb.filter), 1)]
        print("Scroll filter list reset.", self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.filter)

        print("Actors length:", len(self.actors))

        #If-else syntax failed here in one case, so rewrote as single line. Logic left for reference.
        # self.parent.pianorollpanel.last_actor = 0 if len(self.actors) == 0 else self.parent.pianorollpanel.last_actor
        # print("No actors, 'prp.last_actor' set to 0") if len(self.actors) == 0 else None

        #Same thing. Easier to read, takes up more lines.
        if len(self.actors) == 0:
            self.parent.pianorollpanel.last_actor = 0
            print("No actors, 'prp.last_actor' set to 0")
        else:
            pass





        #alb.filter.remove()


    @on_trait_change('cpqn_changed_flag')
    def OnCellsPerQuarterNote_Changed(self):
        #self.highlighter_transformation()
        self.new_reticle_box()
        #print("Establishing New Reticle Box...")

        #Reset orange reticle box. CHECK
        #Scale_factor for all actors.
        #Reset x-axis scaling?

        #for i in self.actors:


    # @on_trait_change('image_plane_widget.ipw.poly_data_algorithm.normal')
    # def print_ass(self):
    #     print("ASS")

    #@on_trait_change('normal')
    def anchor_volume_slice(self):
        # If it's the movable volume_slice, not the 'surface' version....
        self.scene3d.disable_render =True
        #self.on_trait_change(self.anchor_volume_slice, 'origin', remove=True)

        if self.volume_slice is False:
            pass
        else:
            if self.image_plane_widget.ipw.center[1] == 63.5 and self.image_plane_widget.ipw.center[2] == 63.5:
                pass
            else:

                # print("Anchoring2...")
                x = self.image_plane_widget.ipw.center[0]
                #x2 = self.image_plane_widget.ipw.point2[0]
                #x3 = self.image_plane_widget.ipw.origin[0]
                #po_copy = copy.deepcopy(self.image_plane_widget.ipw.plane_orientation)

                self.image_plane_widget.ipw.trait_set(trait_change_notify=False, plane_orientation=1)  #TODO Figure out how to flag a trait's changed
                                                                                   # even though we didn't change it.
                self.image_plane_widget.ipw.trait_set(trait_change_notify=True, plane_orientation=3)  # so we don't have to y then x here.
    #            self.image_plane_widget.ipw._plane_orientation_changed('x_axes', 'x_axes')

                #self.image_plane_widget.ipw.poly_data_algorithm.normal = np.array([1., 0., 0.])

                self.image_plane_widget.ipw.trait_set(origin=array([x, 0.0, 0.0]))
                self.image_plane_widget.ipw.trait_set(point1=array([x, 127., 0.0]))
                self.image_plane_widget.ipw.trait_set(point2=array([x, 0.0, 127.]))
                # # ..and if it's accidentally spun out of position--
                # print("Anchoring...")

                #These calls eliminate those "white after-effect lines" created in the
                # construction and repositioning of the volume_slice.
                self.image_plane_widget.ipw.slice_position = x+1
                #self.image_plane_widget.ipw.trait_set(slice_position=x+.0000000001)
                # --re-anchor it back into position.
                self.image_plane_widget.ipw.slice_position = x
                #self.image_plane_widget.ipw.trait_set(slice_position=x)
                # print("Anchored.")
                # self.scene.scene.render()
        self.scene3d.disable_render = False
        #self.resync_origin()


    ###Trait Sub-Functions
    ##-----------------------------------------------
    #@on_trait_change('cpqn_changed_flag')
    def new_reticle_box(self, zplane=None):
        if zplane is not None:
            pass
        else:
            zplane = 0   ###self.cur_z  0
#        if self.parent.parentpianorollpanel:

        #TODO Needs Cells per quarter note factored in. ----Once CellsPerQuarterNote is fixed.

        mproll = self.parent.pianorollpanel.pianoroll
        if mproll is not None:
            s_h = mproll.GetScrollPos(wx.HORIZONTAL)
            s_v = mproll.GetScrollPos(wx.VERTICAL)
            s_linex = mproll.GetScrollLineX()   #Set to 160 in pianroll (the grid), the equivalent of scrolling a full measure of columns..
            s_liney = mproll.GetScrollLineY()   #Set to 120, the equivalent of scrolling 2 octaves of rows.
            client_size = mproll.GetClientSize()
            # print("CLIENT_SIZE", client_size)
            client_rect = mproll.GetClientRect()
            # print("CLIENT_RECT", client_rect)

            cpqn = self.parent.pianorollpanel.pianoroll._cells_per_qrtrnote
            #s_r = mproll.GetScroll

            #GRID CELL COORDINATES (Y, X)
            bottomleft = mproll.XYToCell((s_h * s_linex), (s_v * s_liney) + client_size[1] - 18)    #18 (techincally 20) IS THE PIXEL HIGHT IF THE LABEL BAR AT THE TOP.
            # print("RETICLE_BOTTOM_LEFT", bottomleft)

            bottomright = mproll.XYToCell((s_h * s_linex) + client_size[0] - 58, (s_v * s_liney) + client_size[1] - 18)    #60 IS THE PIXEL WIDGTH OF THE PIANO
            # print("RETICLE_BOTTOM_RIGHT", bottomright)

            topleft = mproll.XYToCell((s_h * s_linex), (s_v * s_liney))  #0 times whatever your scroll rate equals zero, so the top left at start is (0, 0)
            # print("RETICLE_TOP_LEFT", topleft)

            topright = mproll.XYToCell((s_h * s_linex) + client_size[0] - 58, (s_v * s_liney))
            # print("RETICLE_TOP_RIGHT", topright)

            #Limiter, so the reticle doesn't turn into a triangle because of going below the grid area with (-1, -1) values...
            #If bottom would go below 0, (to -1, as it has been), then force it be zero and adjust top_left and top_right based on client_size from there.
            if bottomleft[0] == -1 and bottomleft[1] == -1 and topright[0] == -1 and topright[1] == -1 and \
                    bottomright[0] == -1 and bottomright[1] == -1:      #Both bottom and right side.
                print("FIXED POINT")
                topleft = mproll.XYToCell(mproll.CalcUnscrolledPosition(0, 0))  # New Topleft
                bottomleft = (127, topleft[1]) #New Bottomleft
                topright = (topleft[0], self.grid_cells_length -1)
                bottomright = (127, self.grid_cells_length -1)
            elif bottomleft[1] == -1 and bottomright[1] == -1:  #Bottom glitch.

                topleft = mproll.XYToCell(mproll.CalcUnscrolledPosition(0, 0)) #New Topleft
                topright = mproll.XYToCell(mproll.CalcUnscrolledPosition(client_size[0]-58, 0)) #New Topright
                #bottomright = mproll.XYToCell(mproll.CalcUnscrolledPosition(0,0)[0], )
                #Bottom is ( , 127)
                bottomleft = (127, topleft[1]) #New Bottomleft
                bottomright = (127, topright[1]) #New Bottomright

                # print("RETICLE_TOP_RIGHT  1", topright)
                # print("RETICLE_TOP_LEFT  1", topleft)
                # print("RETICLE_BOTTOM_LEFT  1", bottomleft)
                # print("RETICLE_BOTTOM_RIGHT  1", bottomright)

            elif bottomright[0] == -1 and topright[0] == -1:    #Right side glitch.
                print("OVER THE HEDGE")
                topleft = mproll.XYToCell(mproll.CalcUnscrolledPosition(0, 0))  # New Topleft
                bottomleft = mproll.XYToCell(mproll.CalcUnscrolledPosition(0, client_size[1] - 18))
                    #(127, topleft[1])  # New Bottomleft
                #topright = mproll.XYToCell(mproll.CalcUnscrolledPosition(client_size[0] - 58, bottomleft[1]))
                #topright = mproll.XYToCell(mproll.CalcUnscrolledPosition(client_size[0] - 58, 0))  # New Topright
                topright = (topleft[0],self.grid_cells_length -1)
                bottomright = (bottomleft[0], self.grid_cells_length -1)
                # bottomright = mproll.XYToCell(mproll.CalcUnscrolledPosition(0,0)[0], )
                # Bottom is ( , 127)

                    #mproll.CalcUnscrolledPosition(client_size[1]-18, 127)  # New Bottomright

                # print("RETICLE_TOP_RIGHT  2", topright)
                # print("RETICLE_TOP_RIGHT  2", topleft)
                # print("RETICLE_BOTTOM_LEFT  2", bottomleft)
                # print("RETICLE_BOTTOM_RIGHT  2", bottomright)


                pass

            else:

                pass

            # print("TOPRIGHT", topright[0])
            # print("BOTTOMRIGHT", bottomright[0])
            # print("BOTTOMLEFT", bottomleft[0])
            # print("TOPLEFT", topleft[0])
            # print("TOPRIGHT", topright[0])
            #
            # print("----")
            #
            # print("TOPRIGHT", topright[1])
            # print("BOTTOMRIGHT", bottomright[1])

            reticle = np.asarray(np.vstack(((topleft[1], 127-topleft[0], zplane),
                                 (topright[1], 127-topright[0], zplane),
                                 (bottomright[1], 127-bottomright[0], zplane),
                                 (bottomleft[1], 127-bottomleft[0], zplane),
                                 (topleft[1], 127-topleft[0], zplane))), dtype=np.float32)

            #In place slice reassignment.
            reticle[:, 0] = reticle[:, 0] / cpqn #TODO Once cpqn is fixed. CHECK-- Now that cpqn is fixed, create a trait event for it so that this reticle--
                                                                                                      #TODO---(among other things) updates automatically when cpqn is changed. --FIXED, DONE!
            #Traits notification
            self.grid_reticle.mlab_source.trait_set(points=reticle)
            self.parent.mayaviviewcontrolpanel.Refresh()
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


    def highlighter_transformation(self, labels_only=False):
        print("Highlighter transforming....")
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
                i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label. Moved left for readability.
                i_x_restored = i_x_transformed + i_x
                i.actor.actor.position = (i_x_restored, i_y, i_z_restored)
                i.text = "Z-Plane_%s" % self.cur_z
            elif i.name == "Actor_Label":
                i_x_zerod = (i_x * -1) + i_x
                i_x_transformed = i_x_zerod - 40  # Always will be minus 40 for this label as well.
                i_x_restored = i_x_transformed + i_x
                i_y_zerod = (i_y * -1) + i_y
                i_y_transformed = i_y_zerod - 10  # Actor Label lowered here, to just below the grid.
                i_y_restored = i_y_transformed + i_y
                i.actor.actor.position = (i_x_restored, i_y_restored, i_z_restored)  #Actor Label acts as "origin marker."
                i.text = self.parent.pianorollpanel.actorsctrlpanel.actorsListBox.GetItemText(self.cur_ActorIndex)
                #Actor label gets the same color as the "Current Actor's" color.
                i.actor.property.color = self.CurrentActor().color
            else:
                if labels_only is True:
                    pass
                else:
                    i.actor.actor.position = np.array([i_x, i_y, i_z_restored])

    #def z_and_actor_move(self):

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

        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMusic21ConverterParseDialog,
                                                id=new_id1)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMusicodeDialog,
                                                id=new_id2)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMIDIArtDialog,
                                                id=new_id3)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.OnMIDIArt3DDialog,
                                                id=new_id4)
        # TODO These aren't working as desired.....
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_actors_listbox,
                                                id=new_id5)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_zplanes,
                                                id=new_id6)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_pianorollpanel,
                                                id=new_id7)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_pycrust,
                                                id=new_id8)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_mayavi_view,
                                                id=new_id9)
        self.parent.mayaviviewcontrolpanel.Bind(wx.EVT_MENU, self.parent.mainbuttonspanel.focus_on_mainbuttonspanel,
                                                id=new_id10)

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
        # F10 is already used.... goes to the menubar
        entries[9].Set(wx.ACCEL_NORMAL, wx.WXK_F11, new_id10)

        accel = wx.AcceleratorTable(entries)
        self.parent.mayaviviewcontrolpanel.SetAcceleratorTable(accel)

class MayaviMiniView(HasTraits):
    scene_mini = Instance(MlabSceneModel, ())

    view = View(Item('scene_mini', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
                resizable=True)

    def __init__(self, parent):
        HasTraits.__init__(self)


if __name__ == '__main__':
    pass


import sys, os

from midas_scripts import musicode, midiart, midiart3D, music21funcs

import mayavi
from numpy import array
import numpy as np
import random
import music21

from traits.etsconfig.api import ETSConfig

ETSConfig.toolkit = 'wx'

from mayavi import mlab, modules, sources, core, components
from mayavi.components import actor
from mayavi.sources import array_source
from mayavi.core import module_manager
#from mayavi.modules import image_plane_widget

from mayavi3D import MusicObjects

from gui import PianoRoll

import copy

from traits.api import HasTraits, Range, Instance, on_trait_change, Float

from traitsui.api import View, Item, HGroup
from traits.trait_numeric import Array
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

from traits.trait_types import Button
# from traits.trait_numeric import AbstractArray
# from traits.trait_types import Function
# from traits.trait_types import Any
from traits.trait_types import Int
# from traits.trait_types import Str
from mayavi.tools import animator
import cv2
# from traits.trait_types import Method
# from traits.trait_types import List
from traits.trait_types import Any

#Attempt to put animator traits ui pop into our scene3d
# import types
# from functools import wraps
# try:
#     from decorator import decorator
#     HAS_DECORATOR = True
# except ImportError:
#     HAS_DECORATOR = False
#
# from pyface.timer.api import Timer
# from traits.api import Any, HasTraits, Button, Instance, Range
# from traitsui.api import View, Group, Item


# mlab.options.offscreen = True

class Mayavi3idiView(HasTraits):
    scene3d = Instance(MlabSceneModel, ())
    points = Array(dtype=np.int)
    array3D = Array(dtype=np.float, shape=(5000, 128, 127))
    arraychangedflag = Int()
    ass = Float
    #button = Button()
    view = View(Item('scene3d', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False),
                resizable=True)

#TRAITSUI Shit for hack animation ui attempt.
#     start = Button('Start Animation')
#     stop = Button('Stop Animation')
#     delay = Range(10, 100000, 500,
#                   desc='frequency with which timer is called')
#     # The internal timer we manage.
#     timer = Any
#     Group(Item('start'),
#           Item('stop'),
#           show_labels=False),
#     Item('_'),
#     Item(name='delay'),
#     title = 'Animation Controller',
#     buttons = ['OK']
#
#

    def __init__(self):
        HasTraits.__init__(self)
        #self.on_trait_event(self.array3D_changed, 'arraychangedflag')

        self.engine = self.scene3d.engine
        self.engine.start()  # TODO What does this do?
        self.scene = self.engine.scenes[0]   #TODO Refactor the name of this variable? (self.scene?)

        ###Set Scene Background Color
        self.scene.scene.background = (0.0, 0.0, 0.0)



        #Imports Colors
        self.clr_dict_list = midiart.get_color_palettes(r".\resources\color_palettes")

        self.mlab_calls = []  #TODO Note: mlab.clf() in the pyshell does not clear this list.
        self.text3d_calls = []
        self.text3d_default_positions = []

        self.highlighter_calls = []

        # Trait Functions
        # print("BUTTON", type(self.button))


        # READY-MADE POINTS
        # self.pointies = AbstractArray
        # self.points1 = midiart3D.get_points_from_ply(r"C:\Users\Isaac's\Downloads\dodecahedron.ply")
        # self.pointies = self.points1
        # self.points2 = midiart3D.get_points_from_ply(r"C:\Users\Isaac's\Downloads\sphere.ply")
        # self.points3 = np.array([[0, 0, 0]])
        #self.on_trait_event(self.points_changed(), ('grid_to_stream', 'stream_to_grid'))


    @on_trait_change('scene3d.activated')
    def create_3dmidiart(self):

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
        self.Points_Span = self.Points.max()
        self.insert_piano_grid_text_timeplane(self.SM_Span)

        ###SELECT OBJECT

        #ACTOR EXAMPLES
        self.music = self.insert_music_data(self.midi, color=(1, .5, 0), mode="sphere", scale_factor=1)

        self.model = self.insert_array_data(self.Points, color=(0, 0, 1), mode="sphere", scale_factor=2.5)
        self.text = self.insert_text_data("Script-Ease", "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz         ?,;':-.!\"()[]/   0123456789", color=(0, .5, 1), mode='arrow', scale_factor=2)
        random.randint(0, 88)
        self.double = (x, y) = midiart.separate_pixels_to_coords_by_color(cv2.imread(r".\resources\BobMandala.png"), 0,
                                    nn=True, display=False, clrs=self.clr_dict_list['75_crimso-11-1x'])


        #Highlighter Plane
        self.plane = self.establish_highlighter_plane(114, color=(0, 1, 0), length=self.SM_Span)


        #self.points = self.Points


        # @mlab.show
        # self.scene3d.disable_render = False

        #self.insert_titles()     ##I had a 2nd call for a work session where I lost the camera. I may not need this now...
        self.establish_opening()     #TODO Write in a pass statement for when calls to this function are made from within the program; camera issue.
        self.animate(160, self.SM_Span, i_div=2)
        print("Animate")

        #Animator Instance. Instantiated upon the invocation of self.animate after which the animation is immediately stopped here.
        self.animate1._stop_fired()
        print("Animation Stopped")

        #Movie Recording
        self.scene.scene.movie_maker.record = False

        ###RECORD python Scripts
        #mlab.start_recording(ui=True)


        self.insert_titles()
        #self.insert_note_text("3-Dimensional Music", 0, 164, 0, color=(1,0,1), opacity=.12, orient_to_camera=False, scale=30)



    def del_mlab_actor(self, actor): #TODO Write from scenes[0].children stuff. In progress....
        del(actor)


    ##WORKING INSTANCE
    @on_trait_change('arraychangedflag')
    def array3D_changed(self):
        #print("array3D_changed")
        self.points = np.argwhere(self.array3D >= 1)
        self.model.mlab_source.trait_set(points=self.points)

    #@on_trait_change('points')
    #def points_changed(self):
        #print("points_changed")


    def insert_array_data(self, array_2d, color=(0., 0., 0.), mode="cube", scale_factor=.25):
        # print(array_2d)

        mlab_data = mlab.points3d(array_2d[:, 0], array_2d[:, 1], array_2d[:, 2], color=color, mode=mode,
                             scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data


    # TODO Is this necessary??!?!
    def insert_music_data(self, in_stream, color=(0., 0., 0.), mode="cube", name=None, scale_factor=1):
        array_data = midiart3D.extract_xyz_coordinates_to_array(in_stream)
        array_data = array_data.astype(float)
        # print(array_data)
        mlab_data = mlab.points3d(array_data[:, 0], array_data[:, 1], array_data[:, 2], color=color, mode=mode,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data

    def insert_text_data(self, mc, text, color=(0., 0., 0.), mode="cube", name=None, scale_factor=1):
        text_stream = musicode.mc.translate(mc, text)
        text_array = midiart3D.extract_xyz_coordinates_to_array(text_stream)
        mlab_data = mlab.points3d(text_array[:, 0], text_array[:, 1], text_array[:, 2], color=color, mode=mode,
                                  scale_factor=scale_factor)
        self.mlab_calls.append(mlab_data)
        return mlab_data

    def establish_highlighter_plane(self, z_axis, color, grandstaff=True, length=127):
        x1, y1, z1 = (0, 0, z_axis)  # | => pt1
        x2, y2, z2 = (0, 127, z_axis)  # | => pt2
        x3, y3, z3 = (length, 0, z_axis)  # | => pt3
        x4, y4, z4 = (length, 127, z_axis)  # | => pt4
        linebox = MusicObjects.line_square(length=length, z_axis=z_axis)
        plane = mayavi.mlab.mesh([[x1, x2],
                                 [x3, x4]],  # | => x coordinate

                                  [[y1, y2],
                                  [y3, y4]],  # | => y coordinate

                                  [[z1, z2],
                                  [z3, z4]],  # | => z coordinate

                                  color=color, line_width=5.0, mode='sphere', opacity=.25,   #extent=(-50, 128, -50, 128, 114, 114)
                                  scale_factor=1, tube_radius=None)  # black
        self.mlab_calls.append(plane)
        self.highlighter_calls.append(plane)
        plane_edges = mayavi.mlab.plot3d(linebox[:, 0], linebox[:, 1], linebox[:, 2]+.25,
                                         color=(1,1,1), line_width=2.5, opacity=.35, tube_radius=None)
        self.mlab_calls.append(plane_edges)
        self.highlighter_calls.append(plane_edges)
        if grandstaff:
            stafflines = MusicObjects.grand_staff(z_value=z_axis, length=length)
            gclef = MusicObjects.create_glyph(r".\resources\TrebleClef.png", y_shift=59, z_value = z_axis)
            fclef = MusicObjects.create_glyph(r".\resources\BassClef.png", y_shift=44.3,  z_value = z_axis)
            #for j in grandstaff:
            self.gscalls = mlab.plot3d(stafflines[:, 0], stafflines[:, 1], stafflines[:, 2], color=(0,1,0), opacity=.65, tube_radius=None)
            self.gclef_call = mlab.points3d(gclef[:, 0], gclef[:, 1], gclef[:, 2], color=(0,1,0), mode='cube', opacity=.015, scale_factor=.25)
            self.fclef_call = mlab.points3d(fclef[:, 0], fclef[:, 1], fclef[:, 2], color=(0,1,0), mode='cube', opacity=.015, scale_factor=.25)
            self.mlab_calls.append(self.gscalls)
            self.highlighter_calls.append(self.gscalls)
            self.mlab_calls.append(self.gclef_call)
            self.highlighter_calls.append(self.gclef_call)
            self.mlab_calls.append(self.fclef_call)
            self.highlighter_calls.append(self.fclef_call)
            #self.gclef_call.actor.actor.position = np.array([0, 59, 0])
            #self.fclef_call.actor.actor.position = np.array([0, 44.3, 0])
        return plane

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

    def set_actor_positions(self, pos=np.array([0,0,0]), actors=None, rando=False):

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
                i.actor.actor.position = pos
        # elif actors == 'highlighter':
        #     for j in self.highlighter_calls:
        #         j.actor.actor.position = ####Current Actor's Current Z-Plane's Position



    def set_text_positions(self, pos=np.array([0, 0, 0]), default=True, rando=False):

        def random_position():
            list1 = list()
            for i in range(0, 3, 1):
                i = random.randint(-357, 357)
                list1.append(i)
            pos = np.asarray(list1, dtype=np.float64)
            return pos

        # TODO Learn where these smaller text3d mlab calls are stored in the scene. CHECK---use glyph.parent.parent.parent....
        if default is True and rando is False:
            for l in range(0, len(self.text3d_calls)):
                self.text3d_calls[l].actor.actor.position = self.text3d_default_positions[l]
        elif rando is True and default is False:
            for m in range(0, len(self.text3d_calls)):
                self.text3d_calls[m].actor.actor.position = random_position()
        elif rando and default is False:
            for n in range(0, len(self.text3d_calls)):
                self.text3d_calls[n].actor.actor.position = pos
    ##Randomize
    # Midas.GetTopWindow().mayaviview.set_actor_positions(actors='music', rando=True)
    # Midas.GetTopWindow().mayaviview.set_text_positions(default=False, rando=True)

    ##Default
    # Midas.GetTopWindow().mayaviview.set_actor_positions(all=True)
    # Midas.GetTopWindow().mayaviview.set_text_positions(default=True, rando=False)

    def update_3Dpoints(self, row, col, val):
        try:

            page = self.GetTopLevelParent().pianorollpanel.currentPage
            layer = self.GetTopLevelParent().pianorollpanel.pianorollNB.FindPage(page)
            self.array3D[col, 127 - row, layer] = val



        except Exception as e:
            print(e)
            pass

    ###DEFINE MUSIC ANIMATION
    def animate(self, time_length, bpm=None, i_div=4):
        """ I_div should be 2 or 4. Upon a division of greater than 4, say 8, the millisecond delay becomes so small,
        that it is almost not even read properly, producing undesired results.
        Animation function that gives the impression of rendering 3D music. Does not play music.
        :param time_length: Length of the piece to be rendered in the animation display: this determines the range of the animation.
        :param bpm: Beats per minutes of the music as an integer: this allows for the calculation of the functions delay, and determines the speed of the animation scroll.
        For best results, select your bpm from the following list: (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 24, 25, 30, 32, 40, 48, 50, 60, 75, 80, 96, 100, 120, 125, 150, 160, 200, 240, 250,
        300, 375, 400, 480, 500, 600, 625, 750, 800, 1000, 1200, 1250, 1500, 1875, 2000, 2400, 2500, 3000, 3750, 4000,
        5000, 6000, 7500, 10000, 12000, 15000, 20000, 30000, 60000.)
        :param i_div: Number of planescrolls per second: this determines the fineness of your animation.
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
        def animate_plane_scroll(x_length, delay):
            """
            Mlab animate's builtin delay has to be specified as an integer in milliseconds with a minimum of 10, and also could
            not be removed, so we subtracted .01 seconds (or 10 milliseconds) in a workaround delay of our own in order to compensate.
            :param x_length: Length of the range of the animation plane along the x-axis. (See music21.stream.Stream.highestTime)
            :param delay: Int in microseconds.
            :return: N/A
            """
            for i in np.arange(0, x_length * i_div, 1 / i_div):
                # print("%f %d" % (i, time.time_ns()))
                interval = delay
                t = int(time.time() * 1000000) % (interval)
                s = (interval - t)
                time.sleep(
                    s / 1000000)  # Increasing this number speeds up plane scroll.  - .003525  .0035   .0029775025
                # print("timesleep:", (delay-.01))
                # self.image_plane_widget.ipw.slice_index = int(round(i))
                self.image_plane_widget.ipw.slice_position = i
                yield

        # mlab.start_recording()
        # mlab.animate(animate_plane_scroll, ms_delay, ui=True)
        # print(secs_delay)
        #animate_plane_scroll(int(time_length), int(nano_delay))

        self.animate1 = animate_plane_scroll(int(time_length), int(nano_delay))
        #self.animate1._stop_fired()
        print("Animate")

        # animate1.timer.Stop()
        # input("Press Enter.")
        # animate1.timer.Start()


    def standard_reorientation(self, points, scale=1.):
        # TODO Maximum rescaling check.
        # TODO scale_function?  Need check to avoid float values.

        points = midiart3D.transform_points_by_axis(points, positive_octant=True)
        points = midiart3D.delete_redundant_points(points, stray=False)
        points = points * scale

        # TODO Scaling needs to be done with respect to musical, i.e. a musical key, and within the grid's available space.

        return points

    def trim(self, points, axis='y', trim=0):
        Points_Odict = midiart3D.get_planes_on_axis(points, axis, ordered=True)

        # Trim (Trim by index in the list. An in-place operation.)
        [Points_Odict.pop(i) for i in list(Points_Odict.keys())[:trim]]

        # Restore to a coords_array.
        Restored_Points = midiart3D.restore_coords_array_from_ordered_dict(Points_Odict)
        return Restored_Points

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
            measures = mlab.text3d(m, 0, -2, str(i), color=(1, 1, 0), scale=1.65)
            self.text3d_calls.append(measures)
            self.text3d_default_positions.append(measures.actor.actor.position)
        # Time_ScrollPlane
        # x,y,z = np.mgrid[0:127, 0:127, 0:127]
        xh, yh, zh = np.mgrid[0:int(length), 0:254, 0:254]
        # Scalars_1 = (x+y+z)
        Scalars_2 = np.zeros((int(length), 254, 254))
        # xtent = np.array([0, 127, 0, 127, 0, 127])
        mlab.volume_slice(xh, yh, zh, Scalars_2, opacity=.7, plane_opacity=.7, plane_orientation='x_axes',
                          transparent=True)


    ###TITLES and NOTE inserts.
    def insert_note_text(self, text, x=0, y=154, z=0, color=(0, 0, 1), opacity=1, orient_to_camera=True, scale=3):
        mlab_t3d = mlab.text3d(text=text, x=x, y=y, z=z, color=color, opacity=opacity, orient_to_camera=orient_to_camera, scale=scale)
        self.text3d_calls.append(mlab_t3d)
        self.text3d_default_positions.append(mlab_t3d.actor.actor.position)

        # TODO
        ## def insert_image_data(self, imarray_2d, color=(0,0,0), mode="cube", scale_factor = 1):

    ###SCENE TITLEd
    def insert_title(self, text, color=(1, .5, 0), height=.7, opacity=1.0, size=1):
        return mlab.title(text=text, color=color, height=height, opacity=opacity, size=size)

        ###OPENING ANIMATION
        ###-----------------
        ###Script Widget Shrink and Initial Camera Angle
        ##scene = engine.scenes[0]

    #Leave this here for now.
    def insert_titles(self):
        self.insert_note_text("The Midas 3idiArt Display", 0, 137, 0, color=(1, 1, 0), orient_to_camera=True,
                              scale=7)
        ###Note: affected by basesplit sash position.
        self.title = self.insert_title("3-Dimensional Music", color=(1, 0, 1), height=.82, opacity=.12, size=.65)

    def establish_opening(self):
        scene = self.scene
        # scene.scene.x_minus_view()
        self.image_plane_widget = self.engine.scenes[0].children[6].children[0].children[0]
        print("IPW TYPE:", type(self.image_plane_widget))
        self.image_plane_widget.ipw.origin = array([0., 61.0834014, 61.0834014])
        self.image_plane_widget.ipw.point1 = array([0., 191.9165986, 61.0834014])
        self.image_plane_widget.ipw.point2 = array([0., 61.0834014, 191.9165986])
        self.image_plane_widget.ipw.origin = array([0., 61.0834014, 61.0834014])
        self.image_plane_widget.ipw.point1 = array([0., 191.9165986, 61.0834014])
        self.image_plane_widget.ipw.point2 = array([0., 61.0834014, 191.9165986])
        self.image_plane_widget.ipw.origin = array([0., -0.08159137, -0.08159137])
        self.image_plane_widget.ipw.point1 = array([0.00000000e+00, 1.30751606e+02, -8.15913691e-02])
        self.image_plane_widget.ipw.point2 = array([0.00000000e+00, -8.15913691e-02, 1.30751606e+02])
        self.image_plane_widget.ipw.origin = array([0., -0.08159137, -0.08159137])
        self.image_plane_widget.ipw.point1 = array([0.00000000e+00, 1.30751606e+02, -8.15913691e-02])
        self.image_plane_widget.ipw.point2 = array([0.00000000e+00, -8.15913691e-02, 1.30751606e+02])
        scene.scene.z_plus_view()
        scene.scene.camera.position = [-201.04834404780013, 218.73207704519143, 691.9206335681282]
        scene.scene.camera.focal_point = [165.35402886721414, 64.41148341088073, 58.87512414905907]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.0708887660270095, 0.977771522682754, -0.1973262077926211]
        scene.scene.camera.clipping_range = [427.34240240330246, 1152.4000330423432]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()
        scene.scene.camera.position = [-233.62298945718277, 202.27617754671678, 677.0781885058548]
        scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.0708887660270095, 0.977771522682754, -0.1973262077926211]
        scene.scene.camera.clipping_range = [427.34240240330246, 1152.4000330423432]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()
        scene.scene.camera.position = [-170.032494984329, 175.49326460191904, 567.2107860446939]
        scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.0708887660270095, 0.977771522682754, -0.1973262077926211]
        scene.scene.camera.clipping_range = [298.9018858281444, 1020.716069078924]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()
        scene.scene.camera.position = [-117.4783673208135, 153.35862580456552, 476.41127987844527]
        scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.0708887660270095, 0.977771522682754, -0.1973262077926211]
        scene.scene.camera.clipping_range = [192.7526985759473, 911.8863467951057]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()
        scene.scene.camera.position = [-75.6380940108963, 154.49428308844531, 497.79655837964555]
        scene.scene.camera.focal_point = [132.7793834578315, 47.95558391240606, 44.03267908678528]
        scene.scene.camera.view_angle = 30.0
        scene.scene.camera.view_up = [0.04985772050601139, 0.9771694895609155, -0.20652843963290976]
        scene.scene.camera.clipping_range = [210.11552421145498, 882.5056024983969]
        scene.scene.camera.compute_view_plane_normal()
        scene.scene.render()



if __name__ == '__main__':
    pass


from importlib import reload
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from midas_scripts import musicode, midiart, midiart3D, music21funcs
from numpy import array
import numpy as np
import music21
from Mayavi3D import MusicObjects
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'
from numpy import ogrid, sin
from numpy import sqrt, sin, mgrid
from traits.api import HasTraits, Instance
from traitsui.api import View, Item
from numpy import linspace, pi, cos, sin
from mayavi import mlab
from mayavi.sources.api import ArraySource
from mayavi.modules.api import IsoSurface
from traits.api import HasTraits, Range, Instance, \
                    on_trait_change
from traitsui.api import View, Item, HGroup
from mayavi.core.ui.api import MlabSceneModel, SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene
from traits.trait_types import Button
from traits.trait_numeric import AbstractArray
from traits.trait_types import Function
from traits.trait_types import Method
#-------------------------------------------------------------------------------
def curve(n_mer, n_long):
    phi = linspace(0, 2*pi, 2000)
    return [ cos(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            sin(phi*n_mer) * (1 + 0.5*cos(n_long*phi)),
            0.5*sin(n_long*phi),
            sin(phi*n_mer)]

def trim(Points, axis='y', trim=0):
    Points_Odict = midiart3D.get_planes_on_axis(Points, axis, ordered=True)

    # Trim (Trim by index in the list. An in-place operation.)
    [Points_Odict.pop(i) for i in list(Points_Odict.keys())[:trim]]

    # Restore to a coords_array.
    Restored_Points = midiart3D.restore_coords_array_from_ordered_dict(Points_Odict)
    return Restored_Points

class MayaviView(HasTraits):

    scene = Instance(MlabSceneModel, ())

    # The layout of the panel created by traits.
    view = View(Item('scene', editor=SceneEditor(),
                    resizable=True,
                    show_label=False),
                resizable=True)

    def __init__(self):
        HasTraits.__init__(self)
        x, y, z = ogrid[-10:10:100j, -10:10:100j, -10:10:100j]
        scalars = sin(x*y*z)/(x*y*z)
        src = ArraySource(scalar_data=scalars)
        self.scene.mayavi_scene.add_child(src)
        src.add_module(IsoSurface())

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())
    meridional = Range(1, 30,  6)
    transverse = Range(0, 30, 11)
    button = Button("Balls")
    method = Method()
    #self.points = AbstractArray #TODO Necessary to establish points here?

    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        self.points = AbstractArray
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot = self.scene.mlab.plot3d(x, y, z, t, colormap='Spectral')
        print("PLOT SOURCE", type(self.plot.mlab_source))
        self.points1 = midiart3D.get_points_from_ply(r"C:\Users\Isaac's\Downloads\dodecahedron.ply")
        self.points = self.points1
        self.points2 = midiart3D.get_points_from_ply(r"C:\Users\Isaac's\Downloads\sphere.ply")
        self.bird = self.scene.mlab.points3d(self.points1[:, 0], self.points1[:, 1], self.points1[:, 2],
                                     color=(0.8666666666666667, 0.6549019607843137, 0.8392156862745098), mode='cube',
                                     scale_factor=3)

    @on_trait_change('meridional,transverse')
    def update_plot(self):
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot.mlab_source.trait_set(x=x, y=y, z=z, scalars=t)


    @on_trait_change('button')
    def change_points(self):
        if midiart.array_to_lists_of(self.points) ==  midiart.array_to_lists_of(self.points2):
            self.points = self.points1
        else:
            self.points = self.points2
        #x, y, z = sphera[:, 0], sphera[:, 1], sphera[:, 2]
        self.bird.mlab_source.trait_set(points=self.points)

    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=250, width=300, show_label=False),
                HGroup(
                        '_', 'meridional', 'transverse',
                    ), Item('button')
                )

class ActorViewer(HasTraits):
    # The scene model.
    scene = Instance(MlabSceneModel, ())

    ######################
    # Using 'scene_class=MayaviScene' adds a Mayavi icon to the toolbar,
    # to pop up a dialog editing the pipeline.
    view = View(Item(name='scene',
                     editor=SceneEditor(scene_class=MayaviScene),
                     show_label=False,
                     resizable=True,
                     height=500,
                     width=500),
                resizable=True
                )

    def __init__(self, **traits):
        HasTraits.__init__(self, **traits)
        self.generate_data()

    def generate_data(self):
        # Create some data
        X, Y = mgrid[-2:2:100j, -2:2:100j]
        R = 10 * sqrt(X ** 2 + Y ** 2)
        Z = sin(R) / R

        self.scene.mlab.surf(X, Y, Z, colormap='gist_earth')

class Mayavi3idiView(HasTraits):
    scene3d = Instance(MlabSceneModel, ())
    view = View(Item('scene3d', editor=SceneEditor(scene_class=MayaviScene), resizable=True, show_label=False), resizable=True)
    def __init__(self):
        HasTraits.__init__(self)
        #animator = Mayavi3DAnimator()
        #self.scene3d.disable_render = True
        #self.scene3d.engine = awesome3idi.engine
        # -1
        try:
            self.scene3d.engine = mayavi.engine
            self.engine = self.scene3d.engine
            # self.engine = MayaviView.scene.engine
        except NameError:
            from mayavi.api import Engine
            #self.scene3d.engine = Engine()
            self.engine = self.scene3d.engine
            self.engine.start()
            #self.engine = self.scene3d.engine
        print("SCENESLIST LENGTH:", len(self.engine.scenes))
        if len(self.engine.scenes) == 0:
            self.engine.new_scene()
        # if len(self.engine.scenes) == 1:
        #     self.engine.close_scene(self.engine.scenes[0])
        #     print("HAS SCENES STILL:", self.engine.scenes)
        #     self.engine.new_scene()

        print("mayavi type FUUUUUCK")
        print(type(self.engine))
        print("Which Scene???? 3DAni", self.engine.scenes[0].name)
        # title_engine = str(self.engine)
        # self.title_engine = str(type(self.engine))
        # self.title_engine_dirs = str(dir(self.engine)[0])
        # print(str(self.title_engine_dirs))
        # -------------------------------------------
        # scene.scene.light_manager = <tvtk.pyface.light_manager.LightManager object at 0x000002AC462F4BF8>
        # engine.new_scene()

        ###ESTABLISH SCENE
        self.scene = self.engine.scenes[0]
        print("Which??? Fuck", self.scene.name)
        ###Set Scene Background Color
        self.scene.scene.background = (0.0, 0.0, 0.0)
        print(self.scene.scene.background)
        # if self.scene.scene.camera:
        #     print("HAS CAMERA (or something")



        SM_Midi = music21.converter.parse(r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\Game Midi Downloads\Spark4.mid")
        SparkMidi1 = midiart3D.extract_xyz_coordinates_to_array(SM_Midi)
        SparkMidiData = SparkMidi1.astype(float)
        Points = midiart3D.get_points_from_ply(r"C:\Users\Isaac's\3D Objects\Structure Scans\Zach Bday\ZachPose5.ply")
        Points = self.standard_reorientation(Points, 2)
        Points = trim(Points, axis='y', trim=5)
        Points = midiart3D.transform_points_by_axis(Points, positive_octant=True)
        Points_Span = Points.max()

        SM_Span = SparkMidiData.max()
        self.insert_piano_grid_text_timeplane(SM_Span)
        self.insert_array_data(SparkMidiData, color=(1, .5, 0), mode="sphere", scale_factor=1)
        self.insert_array_data(Points, color=(1, 0, .5), mode="sphere", scale_factor=1)
        self.insert_title("LICK MY FUCKING NINE", color=(0, .5, 1), size=1)
        self.insert_note_text("FUUUUUUUUUUUUUUUUUUUUCK", scale=30)
        #mlab.start_recording(ui=True)
        #@on_trait_change('scene3d.activated')
        #@mlab.show
        self.scene3d.disable_render = False
        def execute_process():
            self.establish_opening()
            self.animate(150, SM_Span, i_div=4)
        #execute_process()
        #self.scene3d.engine.scenes[0] = self.engine.scenes[0]
    # #self.scene3d.engine.copy_traits(self.engine)
    # # for i in range(0, 9, 1):
    # #     self.scene3d.engine.scenes[0].add_child(self.engine.scenes[0].children[i])


    def standard_reorientation(self, Points, scale=1):
        # The order is :
        ##1. Rotation
        ##2. Delete unecessary planes.
        ##3. Rescale.
        ##4. Transform.

        # TODO Maximum rescaling check.
        # TODO scale_function?  Need check to avoid float values.

        Points = midiart3D.transform_points_by_axis(Points, positive_octant=True)

        Points = midiart3D.delete_redundant_points(Points, stray=False)

        Points = Points * scale

        # TODO Scaling needs to be done with respect to musical, i.e. a musical key, and within the grid's available space.

        return Points



    def insert_piano_grid_text_timeplane(self, length):
        from mayavi import mlab
        ###Piano
        # MayaviPianoBlack = music21.converter.parse(r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\FL Midi Files\MidiPianoBlack.mid")
        # MayaviPianoWhite = music21.converter.parse(r"C:\Users\Isaac's\Desktop\Neo Mp3s-Wavs-and-Midi\FL Midi Files\MidiPianoWhite.mid")
        # #Acquire Piano Numpy Coordinates
        # PianoBlackXYZ = midiart3D.extract_xyz_coordinates_to_array(MayaviPianoBlack)
        # PianoWhiteXYZ = midiart3D.extract_xyz_coordinates_to_array(MayaviPianoWhite)
        PianoBlackNotes = MusicObjects.PianoBlackNotes()
        PianoWhiteNotes = MusicObjects.PianoWhiteNotes()
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
        mlab.text3d(int(length), 0, 0, "X_Time-Rhythm-Duration.", color=(0, 1, 0), scale=4)
        mlab.text3d(0, 127, 0, "Y_Frequency-Pitch.", color=(0, 1, 0), scale=4)
        mlab.text3d(0, 0, 127, "Z_Dynamics-Velocity.", color=(0, 1, 0), scale=4)

        # Grid Frequency Midpoint
        # mlab.text3d(0, 64, 0, "<---Midpoint.", color=(1, 0, 1), scale=10)

        # Add Measure Number Text to X Axis
        for i, m in enumerate(range(0, int(length), 4)):
            mlab.text3d(m, 0, -2, str(i), color=(1, 1, 0), scale=1.65)

        # Time_ScrollPlane
        # x,y,z = np.mgrid[0:127, 0:127, 0:127]
        xh, yh, zh = np.mgrid[0:int(length), 0:254, 0:254]
        # Scalars_1 = (x+y+z)
        Scalars_2 = np.zeros((int(length), 254, 254))
        # xtent = np.array([0, 127, 0, 127, 0, 127])
        mlab.volume_slice(xh, yh, zh, Scalars_2, opacity=.7, plane_opacity=.7, plane_orientation='x_axes',
                          transparent=True)

        ###SELECT OBJECT

    def insert_music_data(self, in_stream, color=(0, 0, 0), mode="cube", scale_factor=1):
        from mayavi import mlab
        # mlab.points3d(GypsyData[:, 0], GypsyData[:, 1], GypsyData[:, 2], color=(1, .5, 0), mode="cube", scale_factor=1)
        # mlab.points3d(SparkImageData[:, 0], SparkImageData[:, 1], SparkImageData[:, 2], color=(1, .5, 0), mode="cube", scale_factor=1)
        array_data = midiart3D.extract_xyz_coordinates_to_array(in_stream)
        # print(array_data)
        mlab.points3d(array_data[:, 0], array_data[:, 1], array_data[:, 2], color=color, mode=mode,
                      scale_factor=scale_factor)

    def insert_array_data(self, array_2d, color=(0, 0, 0), mode="cube", scale_factor=.25):
        from mayavi import mlab
        print(array_2d)
        mlab.points3d(array_2d[:, 0], array_2d[:, 1], array_2d[:, 2], color=color, mode=mode, scale_factor=scale_factor)

    def insert_note_text(self, text, x=0, y=154, z=0, color=(0, 0, 1), scale=3):
        from mayavi import mlab
        mlab.text3d(text=text, x=x, y=y, z=z, color=color, scale=scale)

        # TODO
        ## def insert_image_data(self, imarray_2d, color=(0,0,0), mode="cube", scale_factor = 1):

    ###SCENE TITLE
    def insert_title(self, title, color=(1, .5, 0), size=200):

        mlab.title(text=title, color=color, size=size)

        ###OPENING ANIMATION
        ###-----------------
        ###Script Widget Shrink and Initial Camera Angle
        ##scene = engine.scenes[0]

    def establish_opening(self):
        scene = self.scene
        scene.scene.x_minus_view()
        self.image_plane_widget = self.engine.scenes[0].children[6].children[0].children[0]
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

    ###DEFINE MUSIC ANIMATION
    def animate(self, time_length, bpm=None, i_div=4):
        from mayavi import mlab
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

        @mlab.animate(delay=bpm_delay, ui=True)
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
        animate1 = animate_plane_scroll(int(time_length), int(nano_delay))
        animate1.timer.Stop()
        input("Press Enter.")
        animate1.timer.Start()
        #mlab.figure()
        #mlab.show()

#-------------------------------------------------------------------------------
# Wx Code
import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Mayavi in a Wx notebook')
        self.notebook = wx.aui.AuiNotebook(self, id=-1,
                style=wx.aui.AUI_NB_TAB_SPLIT | wx.aui.AUI_NB_CLOSE_ON_ALL_TABS
                        | wx.aui.AUI_NB_LEFT)

        self.mayavi_view = MayaviView()

        # The edit_traits method opens a first view of our 'MayaviView'
        # object
        self.control = self.mayavi_view.edit_traits(
                        parent=self,
                        kind='subpanel').control
        self.notebook.AddPage(page=self.control, caption='Display 1')

        self.mayavi_view2 = MayaviView()

        # The second call to edit_traits opens a second view
        self.control2 = self.mayavi_view2.edit_traits(
                        parent=self,
                        kind='subpanel').control
        self.notebook.AddPage(page=self.control2, caption='Display 2') 
        
        #This 3rd call displays OUR MUSIC SHIT
        # self.mayavi_view3idi = Visualization()
        #
        # # The second call to edit_traits opens a second view
        # self.control3idi = self.mayavi_view3idi.edit_traits(
        #                 parent=self,
        #                 kind='subpanel').control
        # self.notebook.AddPage(page=self.control3idi, caption='Display 3idi')

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook,1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Show(True)

if __name__ == '__main__':
    #asshat = Mayavi3idiView()
    #a = ActorViewer()
    #a.configure_traits()
    visualization = Visualization()
    visualization.configure_traits()
    #app = wx.App()
    #frame = MainWindow(None, wx.ID_ANY)
    #app.MainLoop()















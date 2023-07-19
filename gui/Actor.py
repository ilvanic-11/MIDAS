from traits.api import on_trait_change, String, Any, HasTraits, Instance, Bool
from traits.trait_numeric import Array
from traits.trait_types import List, Tuple, Int

import numpy as np
import torch

from midas_scripts import midiart, midiart3D


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
        self._array4D = torch.from_numpy(self._array4D)

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

        duration_ratio = pr.GetMusic21DurationRatio() #TODO Make global. 06/20/2022

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
        #This if statement isn't working....???
        if z:
            _z = np.full((len(points), 1), z, dtype=np.int8) #int, because floats cannot be indices.
            points = np.column_stack([points, _z])
            print("Baziznitch!!!!!!")
        else:
            pass
        print("BOOM!")


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
            _dur1.append(_array4D[point[0], point[1], point[2], 2])  #DURATION VALUE Numerator
            _dur2.append(_array4D[point[0], point[1], point[2], 3])  #DURATION VALUE Denominator
        _dur_array1 = np.array(_dur1, dtype=np.float32).reshape((len(points), 1))  #was float16?
        _dur_array2 = np.array(_dur2, dtype=np.float32).reshape((len(points), 1))  #was float16?
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
        self.get_ON_points_as_odict()  #Returns an OrderedDict() as self._all_points
        self._points = midiart3D.restore_coords_array_from_ordered_dict(self._all_points)
        #self._points = midiart3D.delete_select_points(self._points, [[0, 0, 0]], tupl=False)

        print("r4Dchangedflag_points", self._points) #[[x,y,z,d1,d2]
                                                      #[x,y,z,d1,d2]
                                                      #[x,y,z,d1,d2]   #vstacked?
                                                      #[x,y,z,d1,d2]]

        try:
            #THIS IS WHERE WE WILL GET A WORKING VERSION OF DISPLAYING DURATIONS. IT WILL BE BASED ON CHOP_UP_NOTES()
            points = np.column_stack([self._points[:, 0], self._points[:, 1], self._points[:, 2]]) #[x,y,z]
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

        if self.m_v.z_flag is True:
            points = self.get_points_with_all_data(self.cur_z)
        else:
            points = self.get_points_with_all_data()

        #points = self.get_points_with_all_data(self.cur_z) if self.m_v.z_flag is True else self.get_points_with_all_data()



        try:
             #An OrderedDict.
            self._all_points = midiart3D.get_planes_on_axis(points, array=True)


        except IndexError:
            points = np.array(
                [[0, 0, 0]])  # A temporary origin point that acts as a fill, so that get_planes_on_axis executes.
            # TODO Write in methods to delete this, so that midi exports don't have a useless note in every file?
            self._all_points = midiart3D.get_planes_on_axis(points, array=True)

        print("_ALL_POINTS", self._all_points)
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


        print("_ARRAY4D.SHAPE", self._array4D.shape)

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


        #TODO MAJOR NOTE: trait_set only takes standard coords_arrays. SOOO, with our new core data update, we have to
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

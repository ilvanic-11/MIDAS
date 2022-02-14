# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# Name:         midiart3D.py
# Purpose:      This is the pianoroll_mainbuttons_split file for 3idiart functions
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    MIDAS is Copyright © 2017-2019 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-19 Michael Scott Cuthbert and the music21
#				Project
#				mayavi #TODO: Add mayavi copyright info
#
# License:      LGPL or BSD, see license.txt
#------------------------------------------------------------------------------------


###############################################################################
# TABLE OF CONTENTS
#
# 3IDIART_FUNCTIONS
# ------------------
#3D-1.  def EXTRACT_XYZ_COORDINATES_TO_ARRAY in_stream)
#3D-2.  def EXTRACT_XYZ_COORDINATES_TO_STREAM( coords_array)
#3D-3.  def INSERT_INSTRUMENT_INTO_PARTS( in_stream, midi_num=0)
#3D-4.  def PARTITION_INSTRUMENTS_BY_RANDOM( in_stream)
#3D-5.  def ROTATE_POINT_ABOUT_AXIS( x, y, z, axis, degrees)
#3D-6.  def ROTATE_ARRAY_POINTS_ABOUT_AXIS( points, axis, degrees)
#3D-7.  def GET_POINTS_FROM_PLY(file_path, height)
#3D-8.  def WRITE_POINTS_FROM_PLY( coords_array, file_path):
#3D-9.  def DELETE_REDUNDANT_POINTS( coords_array, stray=True):
#3D-10. def DELETE_SELECT_POINTS( coords_array, choice_list)
#3D-11. def GET_PLANES_ON_AXIS( coords_array, axis="z")
#3D-12. def RESTORE_COORDS_ARRAY_FROM_ORDERED_DICT(planes_odict)
#3D-13. def TRANSFORM_POINTS_BY_AXIS(coords_array, offset=0, axis='y', center_axis=False, positive_octant=False)
#3D-14. def SET_Z_TO_SINGLE_VALUE(  #In Mayavi3DWindow now?
#3D-15. def GET_POINT_INDEX(coords_array, point_selection)



###############################################################################

import music21
from music21 import *
from midas_scripts import music21funcs, midiart
#from midas_scripts import midiart
import numpy
import numpy as np
import numpy_indexed as npi
import os
import errno
import copy
import math
import open3d
from collections import OrderedDict
import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy, numpy_to_vtkIdTypeArray
import statistics


#3IDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#3D-1.
def extract_xyz_coordinates_to_array( in_stream, velocities=90.0):
    #TODO rename this function?
    """
         This functions extracts the int values of the offsets, pitches, and velocities of a music21 stream's notes and
    puts them into a common 2d numpy coords_array as floats.
    :param in_stream:               Music21 input stream. (for 3d purposes the stream must contain stream.Parts)
    :return: note_coordinates:      A numpy array comprising x=note.offset, y=note.pitch.ps, and z=note.volume.velocity
                                    data, as well as a=note.duration data.
    """

    # import vtk
    # Create lists and arrays for coordinate integer values.
    temp_stream = music21funcs.notafy(in_stream)
    substitute_volumes = list((np.full((1, len(in_stream.flat.notes)), velocities, dtype=np.float32))[0])
    #print("Substitute Velocities", substitute_volumes)
    volume_list = []
    pitch_list = []
    offset_list = []
    #TODO Duration list?
    duration_list_1 = []
    duration_list_2 = []
    #Gather data all at once, turn them into floats, and put them into lists.-- (.offets are floats by default)
    for XYZ in temp_stream.flat.notes:
        #if XYZ.volume.velocity is None:
            #XYZ.volume.velocity = round(XYZ.volume.realized * 127)

        #if XYZ.volume.velocity is None:
            #print("There are no velocity values for these notes. Assign velocity values.")
            #return None
        offset_list.append(float(XYZ.offset))
        pitch_list.append(float(XYZ.pitch.ps))  #midi
        #TODO Condition check here?
        duration_list_1.append(XYZ.duration.quarterLength.as_integer_ratio()[0])
        duration_list_2.append(XYZ.duration.quarterLength.as_integer_ratio()[1])
        if XYZ.volume.velocity is not None:
            volume_list.append(float(XYZ.volume.velocity))
        else:
            pass
    if len(volume_list) == 0:
        print("There were no velocity values for these notes. Velocities set to volume.realized * 127.")
        volume_list = substitute_volumes
    #Create a numpy array with the the concatenated x,y,z data as its elements.
    note_coordinates = np.r_['1, 2, 0', offset_list, pitch_list, volume_list, duration_list_1, duration_list_2]
    new_coordinates = np.array(note_coordinates, dtype=np.float32)
    del(note_coordinates)
    print("New coords", new_coordinates)
    #Save memory.
    #note_coordinates.dtype = np.float16
    #print(type(note_coordinates))
    if len(new_coordinates) != 0:
        print("Coordinates Created.")
    else:
        print("Coords failed.")
    return new_coordinates

#3D-2.
def extract_xyz_coordinates_to_stream( coords_array, part=False, durations=False):
    """
        This function takes a numpy array of coordinates, x, y, z , and turns those it into a music21
    stream with those coordinates as .offset, .pitch.ps, and .volume.velocity values for x, y, and z.
    ---Note for user: If note.quarterLength and note.volume.velocity are unassigned, they default to 1.0 and None
    respectively.---
    In addition, extra values may be extracted from\added to the coords_array in the form of duration,
    smallestallowednote, and possibly color data.

    :param coords_array:        A 2D Numpy array of coordinate data. --->np.array([x, y, z, a, b, c, d])
                                Objects involved: music21.note.Note(), music21.pitch.Pitch(), music21.volume.Volume(),
                                music21.duration.Duration()
                                n1 = music21.note.Note()
                                x == n1.offset
                                y == n1.pitch.ps
                                z == n1.volume.velocity
                                a == n1.duration
                                b == unused.....
    :param part:                A bool kwarg of separate_notes_to_parts_by_velocity() being used or not.
    :param durations:           Bool determing whether to extract durations from the coords_array. Off by default
                                as point clouds\pictures do not inherently position duration values.
    :return: parts_stream:      A music21 stream.
    """

    #Assign lists, variables, etc.
    out_stream = music21.stream.Stream()
    #note_list = list()
    #Get offset, pitch and velocity values x,y, and z.
    # offset_list = list()
    # pitch_list = list()
    # velocity_list = list()
    #duration_list = list()
    #quarterLength_list = list()
    #Extract coordinate data from numpy array.
    for i in range(0, (len(coords_array))):
        newpitch = music21.pitch.Pitch()                #Pitch
        newpitch.ps = (float(coords_array[i][1]))
        newdur = music21.duration.Duration()            #Duration
        if durations:
            newdur.quarterLength = (float(coords_array[i][3]) / coords_array[i][4])
        else:
            pass
        newnote = music21.note.Note(newpitch)           #Note
        newnote.offset = (float(coords_array[i][0]))    #Time as offset
        if durations:
            newnote.duration = newdur
        else:
            pass
        newnote.volume.velocity = (float(coords_array[i][2]))       #Velocity
        #note_list.append(copy.deepcopy(newnote))
        # TODO n.duration = make_contiguous_notes() # from an array
        #n.quarterLength =
        # print("notepitch ", newnote.pitch.midi)
        # print("offset ", newnote.offset)
        # print("duration ", newnote.duration)
        # print("velocity", newnote.volume.velocity)
        out_stream.insert(newnote.offset, copy.deepcopy(newnote))
    # print('Are we here?!')
    parts_stream = music21funcs.separate_notes_to_parts_by_velocity(out_stream, part)
    # print("How bout here?")
    return parts_stream

#3D-3.
def insert_instrument_into_parts( in_stream, midi_num=0):
    """
        Note: Some ints will not produce an instrument.Instrument, and instead will throw an error. Perhaps this class
    is still developing? This function assigns musical instruments to the parts of a music21 stream. It assigns only one
    instrument to all
    of them.
    :param in_stream:   Stream to be modified.
    :param midi_num:    music21.instrument.Instrument.midiProgram number assigning which programmed instruments to
                        the iterated parts.
    :return:            stream
    """
    instru = music21.instrument.instrumentFromMidiProgram(midi_num)
    for p in in_stream.getElementsByClass(music21.stream.Part):
        p.insert(p.offset, instru)
    return in_stream

#3D-4.
def partition_instruments_by_random( in_stream):
    """
        This function executes inPlace where an instrument object is inserted into the beginning of every stream.Part
    in the top m21.stream.Stream with a randomly assigned m21.instrument.instrument().midiProgram value. The working
    values are shown in the below list. This list is subject to change upon updates to music21.
    :param in_stream:  music21.stream.Stream with Parts.
    :return:           in_stream
    """

    import music21
    import random
    midinums = [0, 6, 7, 8, 19, 16, 20, 21, 22, 48, 40, 41, 42, 43, 46, 24, 26, 32, 33, 35, 105, 24, 104, 106,
                107,
                73, 72, 74, 75, 77, 78, 79, 68, 69, 71, 70, 65, 64, 65, 66, 67, 109, 111, 61, 60, 56, 57, 58,
                11,
                12, 13, 9, 14, 14, 15, 114, 47, 108, 115, 113, 116, 52]
    mp_set = set(midinums)
    midi_list = list(mp_set)
    for p in in_stream.getElementsByClass(music21.stream.Part):
        # for i in random.choices(mPSet):
        p.insert(p.offset, music21.instrument.instrumentFromMidiProgram(random.choice(midi_list)))
    return in_stream


#3D-5.
def rotate_point_about_axis( x, y, z, axis, degrees):
    """
        This function is a base function for performing coordinate rotations on points. It takes one point and uses
    trigonometry (sohcahtoa) to rotate that point as if around an axis, changing its value accordingly.
    :param x:           The x axis value.
    :param y:           The y axis value.
    :param z:           The z axis value.
    :param axis:        The axis of rotation.
    :param degrees:     Degrees (0-360) of rotation.
    :return:            New x,y,z value.
    """

    if axis == "x":
        new_y = (y * (math.cos(math.radians(degrees)))) - (z * (math.sin(math.radians(degrees))))
        new_z = (y * (math.sin(math.radians(degrees)))) + (z * (math.cos(math.radians(degrees))))
        new_x = x
    elif axis == "y":
        new_z = (z * (math.cos(math.radians(degrees)))) - (x * (math.sin(math.radians(degrees))))
        new_x = (z * (math.sin(math.radians(degrees)))) + (x * (math.cos(math.radians(degrees))))
        new_y = y
    elif axis == "z":
        new_x = (x * (math.cos(math.radians(degrees)))) - (y * (math.sin(math.radians(degrees))))
        new_y = (x * (math.sin(math.radians(degrees)))) + (y * (math.cos(math.radians(degrees))))
        new_z = z
    else:
        print("Your axis is incorrect. Please specify either 'x', 'y', or 'z'.")
        return
    return (new_x, new_y, new_z)

#3D-6.
def rotate_array_points_about_axis( points, axis, degrees):
    """
        This function uses rotate_point_about_axis on a large scale of points.
    :param points:      Coords_array of points.
    :param axis:        Axis of rotation.
    :param degrees:     Degrees (0-360) of rotation.
    :return:            A new numpy coords_array.
    """
    # new_points = np.array(points)
    # Centers all points around origin before rotating.
    print("Here1")
    t_x = (max(points[:, 0]) + min(points[:, 0])) / 2
    t_y = (max(points[:, 1]) + min(points[:, 1])) / 2
    t_z = (max(points[:, 2]) + min(points[:, 2])) / 2
    print("Here2")
    points[:, 0] -= t_x
    points[:, 1] -= t_y
    points[:, 2] -= t_z
    axl = []
    ayl = []
    azl = []
    print("Here3")
    for i in range(len(points)):
        ax, ay, az = rotate_point_about_axis(points[i][0], points[i][1], points[i][2], axis, degrees)
        axl.append(ax)
        ayl.append(ay)
        azl.append(az)
    print("Here4")
    print(azl)
    r_points = np.r_['1, 2, 0', axl, ayl, azl]
    # Transforms points back to original position.
    r_points[:, 0] += t_x
    r_points[:, 1] += t_y
    r_points[:, 2] += t_z
    print("Here5")
    return r_points


#3D-7.
def get_points_from_ply( file_path, height=127):
    """
        Returns a 2D numpy array of coordinates from a .ply file, adjusted into floating point value, and transformed
    based on the users input. Input can be positive or negative. For 3idiArt purposes, object values should all be
    positive.
    :param file_path:   File path.
    :param height:      Value up to 127. (Preferably not lower than 50)
    :return:            2d numpy array.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

    ply = open3d.io.read_point_cloud(file_path)
    Data = numpy.asarray(ply.points)
    Data = Data + (0 - Data.min())
    Data = Data * (height/Data.max())
    Data = np.asarray(Data,  int)
    Data = np.asarray(Data, float)
    return Data


#3D-8. #TODO figure out other pointcloud writing method....
   #TODO figure out more Surface Reconstruction Methods.


def write_ply_from_points( coords_array, file_path):

    """
        Function in progress.....TODO FINISH IT!!
    :param coords_array:
    :param file_path:
    :return:
    """


    Poly = vtk.vtkPolyData()
    Pointz = vtk.vtkPoints()
    Coords = vtk.util.numpy_support.numpy_to_vtk(coords_array)
    Surf = vtk.vtkSurfaceReconstructionFilter()
    Contour = vtk.vtkContourFilter()
    Plywriter = vtk.vtkPLYWriter()
    Pointz.SetData(Coords)
    Poly.SetPoints(Pointz)
    Surf.SetInputData(Poly)
    Contour.SetInputConnection(Surf.GetOutputPort())
    Plywriter.SetInputConnection(Contour.GetOutputPort())
    Plywriter.SetFileName(file_path)
    Plywriter.Write()

    # Big_Cloud = open3d.PointCloud(coords_array)
    # Big_Cloud.points = open3d.Vector3dVector(coords_array)
    # open3d.write_point_cloud(file_path, Big_Cloud)



#3D-9.
def delete_redundant_points( coords_array, stray=True):
    """
        This function deletes duplicate points, as well as a possible stray value which ends up being the last value in
    the coords_array.
    :param coords_array:    A 2D numpy array of coordinates.
    :param stray:           Deletes the last value (a stray) of the coords_array.
    :return:                New coords_array.
    """

    set_list = midiart.array_to_lists_of(coords_array, tupl=True)
    assert set_list is not None, print("Set_list", set_list, "Your zplane does not have any notes yet.")  #Todo zplane? 01/02/2022
    #big_set = set(set_list)
    #print("Set_List", set_list)
    big_dict = OrderedDict.fromkeys(set_list)
    little_set = list(big_dict)
    #little_set = list(big_set)
    array = np.array(little_set)
    #array = np.unique(coords_array, 2)
    if stray:
        array = np.delete(array, (len(array)-1), 0)
    else:
        pass
    return array

#3D-10.
def delete_select_points(coords_array, choice_list, tupl=False):
    """
        Deletes user defined list of points, specified as a list of lists.
    :param coords_array:    Operand coords_array.
    :param choice_list:     Specified points to be deleted.
    :return:                New coords_array.
    """
    #from midas_scripts import midiart

    if coords_array.ndim == 3:
        dim = 3
    else:
        dim = 2
    set_list = midiart.array_to_lists_of(coords_array, tupl=tupl)
    new_list = [i for i in set_list if i not in choice_list]
    # new_list = list()
    # for i in set_list:
    #     if i not in choice_list:
    #         new_list.append(i)
    new_array = midiart.lists_of_to_array(new_list, dim)
    return new_array


#3D-11.
def get_planes_on_axis(coords_array, axis="z", ordered=False, clean=True, array=False):
    """
        This function acquires all the "planes" (2d instances of data) along a specified axis and puts them into an
    Ordered Dict. The order of the dict can be set.
    #TODO Write this doc string better.
    :param coords_array:    Operand coords array.
    :param axis:            Axis along which the planes will be derived.
    :param ordered:         If ordered=True, the points are set in order numerological order, else they remain as found
                            from original data..
    :param clean:           If true, redundant\duplicate coords will be deleted.
    :param array:           If true, dict values will be 2D arrays of coords instead of lists of coords.
    :return:                An Ordered Dictionary.
    """

    if clean == True:
        coords_array = delete_redundant_points(coords_array, stray=False)
        print("Redundant points removed.")
        #TODO See if stray will still need to be true for scans.
    else:
        pass

    #planes_list = list()

    if axis is "z":
        axis = 2
    elif axis is "y":
        axis = 1
    else:
        axis = 0

    axis_list = [z for z in coords_array[:, axis].flatten()]  #is .flatten() necessary? It ran without it...
    if ordered:
        axis_list.sort()
        planes_dict = OrderedDict.fromkeys(i for i in axis_list)
    else:
        planes_dict = OrderedDict.fromkeys(i for i in coords_array[:, axis].flatten())


    for i in planes_dict.keys():
        if array is True:
            planes_list = [j for j in coords_array if j[axis] == i]
            planes_dict[i] = np.array(planes_list)
        else:
            planes_list = [j for j in midiart.array_to_lists_of(coords_array, tupl=False) if j[axis] == i]
            planes_dict[i] = planes_list

    #print(planes_dict.keys())
    #print("Then use np.array on the value to reassert as numpy coordinate data.")
    return planes_dict


#3D-12.
def restore_coords_array_from_ordered_dict(planes_odict):
    """
        The sister function to get_planes_on_axis, this function restores those planes from an Ordered Dict back into a
    coords_array.
    :param planes_odict:    An Ordered Dict of 2d numpy arrays.
    :return:                A coords_array.
    """
    key_list = [i for i in planes_odict.values()]
    key_tupl = tuple(key_list)
    new_coords = np.vstack(key_tupl)
    return new_coords


#Basic Point Cloud transformation functions.
def standard_reorientation(points, scale=1., clean=False):
    # TODO Maximum rescaling check.
    # TODO scale_function?  Need check to avoid float values.
    # TODO Scaling needs to be done with respect to musical, i.e. a musical key, and within the grid's available space.

    #TODO MAJOR: There is a 'scale' trait within an mlab actor. Use this for scaling? (it scales the size of points up as well..)


    points = transform_points_by_axis(points, positive_octant=True)
    if clean:
        points = delete_redundant_points(points, stray=True)
    else:
        points = delete_redundant_points(points, stray=False)

    points = scale_points(points=points, scale=scale)
    return points


def scale_points(points, scale=2.):
    coords = np.r_['1, 2, 0', points[:, 0], points[:, 1], points[:, 2]]
    coords = coords * scale
    coords = np.asarray(coords, int)
    for i in range(0, 3, 1):
        points[:, i] = coords[:, i]
    return points


def trim(points, axis='y', trim=0):

    Points_Odict = get_planes_on_axis(points, axis, ordered=True)

    # Trim (Trim by index in the list. An in-place operation.)
    [Points_Odict.pop(i) for i in list(Points_Odict.keys())[:trim]]

    # Restore to a coords_array.
    Restored_Points = restore_coords_array_from_ordered_dict(Points_Odict)
    return Restored_Points


#3D-13.
def transform_points_by_axis(coords_array, offset=0, axis='y', center_axis=False, positive_octant=False):
    """
        This function moves points in a point cloud in a + or - direction on a selected axis. If center_axis is true,
    object is moved to zero on that axis. If positive_octant is true, all axes are centered in the positive octant.
    Operates inPlace.
    :param coords_array:    2D numpy array of coordinates.
    :param axis:            Axis of "x", "y", and "z" in the manner of a Euclidian grid.
    :param offset:          Value for points to be moved on an axis.
    :param center_axis:     If true, centers that particular axis so the object is adjacent to that axis's zero; all
                            values  are subracted by the min of that axis.
    :param positive_octant: If True, centers all axes in the positive octant.
    :return:                coords_array. Function operates in place. Be wary of losing previous numpy variables.
    """
    offset = offset
    axis = axis
    if center_axis is True or positive_octant is True:
        offset = 0
    if axis == "x":
        ax = 0
    elif axis == "y":
        ax = 1
    elif axis == "z":
        ax = 2
    else:
        print("No axis selected. Either you're centering, or have variable input error.")
        return None
    axis_array = coords_array[:, ax]
    if center_axis:
        coords_array[:, ax] = axis_array - axis_array.min()
    elif positive_octant:
        for i in range(0, 3, 1):
            axis_array = coords_array[:, i]
            coords_array[:, i] = axis_array - axis_array.min()
    else:
        axis_array = coords_array[:, ax]
        coords_array[:, ax] = axis_array + offset  # Numpy math is conducted in place.
    return coords_array


#Position, orientation, and #TODO origin functions.
#TODO This is a numpy function. Allocate accordingly?
#3D-14.
def set_z_to_single_value(value, self=None, coords=None,  actor=None):
    """
        This function takes in a coords_array and changes all the (*, *, z, *, *, *) z values to the designated 'value'
    argument.

    Note: The music21funcs module has functionally identical methods called set_stream_velocities() and , only it operates
    on a music21 stream.
    Note: This previously was a class function, but was moved here because of it being inherently numpy.
          self=Midas.mayavi_view can be passed within the Midas application's pycrust for ease of use.
    :param coords:      Operand coords_array.
    :param value:       Value to which to change all z values.
    :param actor:       In the Midas application, this is the desired actor on which to operate.
    :return:            A modified coords_array.
    """
    if actor is None:
        coords_array = coords
        coords_array_z = coords[:, 2]
        coords[:, 2] = np.full((len(coords_array_z), 1), value)[:, 0]
        return coords_array
    else:   #For use within the Midas application when running.
        try:
            Midas = self
        except Exception as e:
            print(e)
            return
        coords_array = Midas.mlab_calls[actor].mlab_source.points
        coords_array_z = coords_array[:, 2]
        coords_array[:, 2] = np.full((len(coords_array_z), 1), value)[:, 0]
        Midas.mlab_calls[actor].mlab_source.points = coords_array
    return coords_array

#3D-15.
def get_point_indices(coords_array, point_selection=None, _array4D=None, z=None, selected_zplane_only=False, on_points=False):
    """
        This function acquires the value(s) of the indices of a point or selection of points in a provided coords_array
    along the 1rst axis. Advanced use in Midas allowed involving the input of a Midas.m_v.CurrentActor()._array4D
    in order to acquire on_points automatically. Clever use might involve zipping or enumerating the acquired result
    indices with coords_array for a variety of uses.

    #Standard use case:
    >>>coords_array = np.array([[1,2,3], [4,5,6], [7,8,9], [10,11,12]], dtype=np.float32)
    >>>point_selection = np.array([[ 4.,  5.,  6.], [ 7.,  8.,  9.]], dtype=np.float64)  #6
    >>>#Expected Result: Indices === np.array([1])
    >>>midiart3D.get_point_indices(coords_array, point_selection, z=6, selected_zplane_only=True, on_points=False)
    >>>#Expected Result: Indices === np.array([1, 2])
    >>>midiart3D.get_point_indices(coords_array, point_selection, selected_zplane_only=False, on_points=False)


    #Advanced use 1 in the pycrust of Midas:
    >>>midiart3D.get_point_indices(Midas.mayavi_view.CurrentActor()._points, point_selection=None, _array4D=Midas.mayavi_view.CurrentActor()._array4D, z=None, selected_zplane_only=False, on_points=True)

    #Proof 1
    >>>indices = _
    >>>len(indices)
    >>>len(Midas.mayavi_view.CurrentActor()._points)
    >>>len(midiart3D.delete_redundant_points(Midas.mayavi_view.CurrentActor()._points))
    >>>len(midiart3D.delete_redundant_points(Midas.mayavi_view.CurrentActor()._points, stray=False))

    #Advanced use 2 in the pycrust of Midas:
    >>>midiart3D.get_point_indices(Midas.mayavi_view.CurrentActor()._points, point_selection=None, _array4D=Midas.mayavi_view.CurrentActor()._array4D, z=Midas.mayavi_view.cur_z, selected_zplane_only=True, on_points=True)


    :param coords_array:        Our host coords_array in which we search.
    :param point_selection:     A list of lists\\tuples, a tuple of lists\\tuples, a 2D
                                np.array([[x,y,z], ....[x,y,z]]) point or 2D coords_array
                                of points with equivalent np.dtype to coords_array. (i.e np.float32, since our points
                                are usually float32 in Midas.)
    :param z:                   If on_points is True and selected_zplane_only is True,
                                z is the zplane valued required for concatenating a
    :param on_points:           Bool determining if to get on_points from np.argwhere using _array4D.
    :return:                    An array of indices.
    """
    #Split this up.

    if on_points is True:
        #Redundant use case. Point_selection not applied in this if block.
        assert _array4D is not None, "If on_points is true, you must supply an _array4D as an argument."
        if selected_zplane_only is False:
            point_selection = np.argwhere(_array4D[:,:,:,0]==1.0) #3 element arrays.
            point_selection = np.array(point_selection, dtype=coords_array.dtype) #Forces the correct dtype.
            print("point_selection_dtype", point_selection.dtype)
        if selected_zplane_only is True:
            assert z is not None, "If selected_zplane_only is True, 'z' must be supplied as an argument." \
                                  "(i.e. Midas.mayavi_view.cur_z)"
            z = z
            point_selection = np.argwhere(_array4D[:,:,z,0]==1.0) #2 element arrays
            print("Point_Selection1", point_selection)
            _z = np.full((len(point_selection), 1), z, dtype=coords_array.dtype) #Should ideally be float32
            #hstacked to 3 element arrays, search ready
            point_selection = np.array(np.hstack([point_selection, _z]), dtype=coords_array.dtype) #float 32 forced.
            print("point_selection_dtype", point_selection.dtype)

    else:
        # Manually defined, handles single or even multiple points for which we desire indices.
        point_selection = np.array([np.array(i, dtype=coords_array.dtype) for i in point_selection],
                                   dtype=coords_array.dtype)
        print("Point_Selection2", point_selection)
        if selected_zplane_only:
            assert z is not None, "If selected_zplane_only is True, 'z' must be supplied as an argument." \
                                  "(i.e. Midas.mayavi_view.cur_z)"
            dict_selection = get_planes_on_axis(point_selection, axis="z", array=True)
            #all_points = restore_coords_array_from_ordered_dict(dict_selection)
            point_selection = np.array(dict_selection[z], dtype=coords_array.dtype)
            print("Point_selection", point_selection)
        else:
            pass

    # Making sure it's our (x,y,z) point, and not (x,y,z, a, b) in which we can't search for x,y,z...
    search_points = np.column_stack([coords_array[:, 0], coords_array[:, 1], coords_array[:, 2]])
    #Search for indices.
    selection_index = npi.indices(search_points, [i for i in point_selection], axis=0, missing='mask')
    return selection_index


#Todo
def separate_coords_to_plane():
    pass


#TODO Learn more vtk.
#TODO Vtk update, revisit. 11/26/2020
#3D-
def make_vtk_points_mesh( points):
    """
        Create a PolyData object from a numpy array containing just points
    """
    if points.ndim != 2:
        points = points.reshape((-1, 3))
    npoints = points.shape[0]
    # Make VTK cells array
    cells = np.hstack((np.ones((npoints, 1)),
                       np.arange(npoints).reshape(-1, 1)))
    cells = np.ascontiguousarray(cells, dtype=np.int64)
    vtkcells = vtk.vtkCellArray()
    vtkcells.SetCells(npoints, numpy_to_vtkIdTypeArray(cells, deep=True))
    # Convert points to vtk object
    vtkPoints = vtk.vtkPoints()
    vtkPoints.SetData(numpy_to_vtk(points))
    # Create polydata
    pdata = vtk.vtkPolyData()
    pdata.SetPoints(vtkPoints)
    pdata.SetVerts(vtkcells)
    return pdata


def BPM_to_FPS(bpm, i_div, timesig = None):
    """
        This function calculates a fps value from a bpm value.
        We ask: What is the equation for fps given the bpm and the frames per beat?
    For our purposes:
    bpmm = beats per measure
    steps value = 1/i_div
    4 steps == 1 Measure
    i_div*bpmm = frames per measure
    fpm/bpmm = frames per beat
    **(bpm * ((i_div*bpmm)\bpmm))\60 = fps **
    Therefore, fpb == i_div.
    (bpm * fpb)\60 = fps
    :param bpm:     Beats per minute
    :param bpmm:    Beats per measure.
    :param i_div:   Frames per beat. (Think of this like quarternotes, eighth notes, 16th, etc....)
    :return:        Frames per second.
    """
    if timesig is None:
        timesig = music21.meter.TimeSignature('4/4')
    else:
        timesig = music21.meter.TimeSignature(timesig)
    bpmm = timesig.barDuration.quarterLength

    #fpm == 4/i_div
    fps = (bpm * i_div)/60
    #modulo = (bpm * fps) % 60
    return fps
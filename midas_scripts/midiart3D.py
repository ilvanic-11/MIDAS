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

#3D-. def ARRAY_TO_LISTS_OF( coords_array, tupl=True)
#3D-. def LISTS_OF_TO_ARRAY( list)

###############################################################################

import music21
from music21 import *
from midas_scripts import music21funcs
#from midas_scripts import midiart
import numpy as np
import copy
import math
import open3d
from collections import OrderedDict
import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy, numpy_to_vtkIdTypeArray
import statistics
from midas_scripts import midiart

#3IDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#3D-1.
def extract_xyz_coordinates_to_array( in_stream, velocities=90.0):
    """
        This functions extracts the int values of the offsets, pitches, and velocities of a music21 stream's notes and
    puts them into a common 2d numpy coords_array as floats.

    :param in_stream:               Music21 input stream. (for 3d purposes the stream must contain stream.Parts)
    :return: note_coordinates:      A numpy array comprised of x=note.offset, y=pitch.midi, and z=volume.velocity.
    """

    # import vtk
    # Create lists and arrays for coordinate integer values.
    temp_stream = music21funcs.notafy(in_stream)
    substitute_volumes = list((np.full((1, len(in_stream.flat.notes)), velocities, dtype=np.float16))[0])
    #print("Substitute Velocities", substitute_volumes)
    volume_list = list()
    pitch_list = list()
    offset_list = list()
    #TODO Duration list?
    #Gather data all at once, turn them into floats, and put them into lists.-- (.offets are floats by default)
    for XYZ in temp_stream.flat.notes:
        #if XYZ.volume.velocity is None:
            #XYZ.volume.velocity = round(XYZ.volume.realized * 127)

        #if XYZ.volume.velocity is None:
            #print("There are no velocity values for these notes. Assign velocity values.")
            #return None
        offset_list.append(float(XYZ.offset))
        pitch_list.append(float(XYZ.pitch.midi))
        if XYZ.volume.velocity is not None:
            volume_list.append(float(XYZ.volume.velocity))
        else:
            pass
    if len(volume_list) == 0:
        print("There were no velocity values for these notes. Velocities set to volume.realized * 127.")
        volume_list = substitute_volumes
    #Create a numpy array with the the concatenated x,y,z data as its elements.
    note_coordinates = np.r_['1, 2, 0', offset_list, pitch_list, volume_list]
    new_coordinates = np.array(note_coordinates, dtype=np.float16)
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
def extract_xyz_coordinates_to_stream( coords_array, part=False):
    """
        This function takes a numpy array of coordinates, 3 x, y, z values per coordinates, and turns it into a music21
    stream with those coordinates as .offset, .pitch, and .volume.velocity values for x, y, and z. ---Note for user.
    If note.quarterLength and note.volume.velocity are unassigned, they default to 1.0 and None respectively.

    :param coords_array:        A 2D Numpy array of coordinate data.
    :param part:                A bool kwarg of separate_notes_to_parts_by_velocity().
    :return: parts_stream:      A music21 stream.
    """

    #Assign lists, variables, etc.
    out_stream = music21.stream.Stream()
    note_list = list()
    #Get offset, pitch and velocity values x,y, and z.
    # offset_list = list()
    # pitch_list = list()
    # velocity_list = list()
    #duration_list = list()
    #quarterLength_list = list()
    #Extract coordinate data from numpy array.
    for i in range(0, (len(coords_array))):
        newpitch = music21.pitch.Pitch()
        newpitch.ps = (float(coords_array[i][1]))
        newnote = music21.note.Note(newpitch)
        newnote.offset = (float(coords_array[i][0]))
        newnote.volume.velocity = (float(coords_array[i][2]))
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
        new_y = y * round(math.cos(math.radians(degrees))) - z * round(math.sin(math.radians(degrees)))
        new_z = y * round(math.sin(math.radians(degrees))) + z * round(math.cos(math.radians(degrees)))
        new_x = x
    elif axis == "y":
        new_z = z * round(math.cos(math.radians(degrees))) - x * round(math.sin(math.radians(degrees)))
        new_x = z * round(math.sin(math.radians(degrees))) + x * round(math.cos(math.radians(degrees)))
        new_y = y
    elif axis == "z":
        new_x = x * round(math.cos(math.radians(degrees))) - y * round(math.sin(math.radians(degrees)))
        new_y = x * round(math.sin(math.radians(degrees))) + y * round(math.cos(math.radians(degrees)))
        new_z = z
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
    t_x = (max(points[:, 0]) + min(points[:, 0])) / 2
    t_y = (max(points[:, 1]) + min(points[:, 1])) / 2
    t_z = (max(points[:, 2]) + min(points[:, 2])) / 2
    points[:, 0] -= t_x
    points[:, 1] -= t_y
    points[:, 2] -= t_z
    axl = list()
    ayl = list()
    azl = list()
    for i in range(len(points)):
        ax, ay, az = rotate_point_about_axis(points[i][0], points[i][1], points[i][2], axis, degrees)
        axl.append(ax)
        ayl.append(ay)
        azl.append(az)
    print(azl)
    r_points = np.r_['1, 2, 0', axl, ayl, azl]
    # Transforms points back to original position.
    r_points[:, 0] += t_x
    r_points[:, 1] += t_y
    r_points[:, 2] += t_z
    return r_points


#3D-7.
def get_points_from_ply( file_path, height=127):
    """
        Returns a 2D numpy array of coordinates from a .ply file, adjusted into floating point value, and transformed
    based on the users input. Input can be positive or negative. For 3idiArt purpoes, object values should all be
    positive.

    :param file_path:   File path.
    :param height:      Value up to 127. (Preferably not lower than 50)
    :return:            2d numpy array.
    """
    import open3d
    import numpy
    import numpy as np
    import os
    import errno
    if not os.path.exists(file_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

    ply = open3d.read_point_cloud(file_path)
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
    #big_set = set(set_list)
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
def delete_select_points( coords_array, choice_list):
    """
        Deletes user defined list of points, specified as a list of lists.

    :param coords_array:    Operand coords_array.
    :param choice_list:     Specified points to be deleted.
    :return:                New coords_array.
    """
    from midas_scripts import midiart
    if coords_array.ndim == 3:
        dim = 3
    else:
        dim = 2
    set_list = midiart.array_to_lists_of(coords_array, tupl=True)
    new_list = list()
    for i in set_list:
        if i not in choice_list:
            new_list.append(i)
    new_array = midiart.lists_of_to_array(new_list, dim)
    return new_array


#3D-11.
def get_planes_on_axis( coords_array, axis="z", ordered=False, clean=True):
    """
        This function acquires all the "planes" (2d instances of data) along a specified axis and puts them into an
    Ordered Dict. The order of the dict can be set.

    :param coords_array:    Operand coords array.
    :param axis:            Axis along which the planes will be derived.
    :param ordered:         If ordered=True, the planes are set in order chronological order, else they remain as found
                            from original data.. #TODO More testing? Some examples seem not to be ordered correctly....
    :param clean:           If true, redundant\duplicate coords will be deleted.
    :return:                An Ordered Dictionary.
    """


    if clean == True:
        coords_array = delete_redundant_points(coords_array, stray=False) #TODO See if stray will still need to be true for scans.
    else:
        pass

    planes_list = list()

    if axis is "z":
        axis = 2
    elif axis is "y":
        axis = 1
    else:
        axis = 0

    axis_list = [z for z in coords_array[:, axis].flatten()]
    planes_dict = OrderedDict.fromkeys(i for i in coords_array[:, axis].flatten())
    if ordered:
        axis_list.sort()
        planes_dict = OrderedDict.fromkeys(i for i in axis_list)

    for i in planes_dict.keys():
        planes_list = list()
        for j in midiart.array_to_lists_of(coords_array, tupl=False):
            if j[axis] == i:
                planes_list.append(j)
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
    key_list = list()
    for i in planes_odict.values():
        key_list.append(i)
    key_tupl = tuple(key_list)
    new_coords = np.vstack(key_tupl)
    return new_coords


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


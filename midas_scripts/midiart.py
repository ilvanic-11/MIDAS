# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------
# Name:         midiart.py
# Purpose:      This is the top file for midiart functions
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    MIDAS is Copyright © 2017-2021 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-2021 Michael Scott Cuthbert and the music21
#               Project
# License:      LGPL or BSD, see license.txt
# ------------------------------------------------------------------------------------


###############################################################################
# TABLE OF CONTENTS
#
# MIDIART_FUNCTIONS
# ------------------
# MA-1.  def PRINT_CHORDS_IN_PIECE(stream)
# MA-2a. def MAKE_MIDI_FROM_PIXELS(pixels, granularity, connect, keychoice)
# MA-2b. def SET_TO_NN_COLORS((im_array, clrs=None, FL=True)
# MA-2c. def SET_PARTS_TO_MIDI_CHANNELS(in_stream, fptf)
# MA-3.  def MAKE_PIXELS_FROM_MIDI()
# MA-4.  def STRIP_MIDI_BY_CHORDS(stream, directory)
# MA-5.  def STRIP_MIDI_BY_PITCHRANGE(stream, directory, range_l, range_h)
# MA-6.  def STAGGER_PITCH_RANGE(in_stream, stepsize=1, ascending=True, starting_offset=None, range_l=0, range_h=128)
# MA-7. TODO def STAGGER_OFFSET_RANGE()
# MA-8.  def TRANSCRIBE_COLOR_IMAGE_TO_MIDIART(img, height, granularity, midi_path, connect, keychoice=None)
# MA-9   def TRANSCRIBE_GRAYSCALE_IMAGE_TO_MIDIART(img, granularity, connect, keychoice=None, note_pxl_value=255,
                                                # output_path=None)
# MA-10. def TRANSCRIBE_IMAGE_EDGES_TO_MIDIART(( img, height, granularity, midi_path, connect, keychoice=None)
# MA-11. def EXTRACT_SUB_MELODIES(stream, keep_dur=False, chop_durs=False, offset_interval=0.25)
# MA-12. TODO Revise? def GET_RANDOM_MELODY(in_stream)
# MA-13. def SECTIONALIZE_IMAGE_ARRAY(image_array, sec_root)
# MA-14. def RECONSTRUCT_IMAGE_SECTIONS(array_list)
# MA-15. def LISTS_OF_TO_ARRAY(lizt, dim=2)
# MA-16. def ARRAY_TO_LISTS_OF(coords_array, tupl=True)
# MA-17. def SEPARATE_PIXELS_TO_COORDS_BY_COLOR(image, z_value, nn=False, dimensionalize=None, display=False, clrs=None, num_dict=False)
# MA-18. def GET_COLOR_PALETTES(mypath=None, ncp=False)
# MA-19. def CONVERT_DICT_COLORS(colors_dict)
# MA-20. def CONVERT_RGB_TO_NCP(palettes=None)
# MA-21. def CV2_TUPLE_RECONVERSION(image, inPlace=False, conversion ='Edges')
# MA-22. def CREATE_MIDI_HEADER(midifile)
###############################################################################

import music21
import mido
import random

# This setlocale stuff had to do with an open3D error I encountered at the time, hence why it's place right before that
# import here.
import locale
locale.setlocale(locale.LC_ALL, 'en_US')

import open3d
import numpy as np
import cv2
import math
import statistics
#import fractions
import copy
from midas_scripts import music21funcs
import numpy

#import mayavi     #TODO Why hashing this out break Midas? Then, also, why is this import here?  04/04/2023 It doesn't break Midas anymore....
# (one reason, it's used in Preferences. General note: imports need to be cleaned up.)
from mayavi import mlab
from collections import OrderedDict
import os
import shutil


##Color Pallettes
#------------------------
##--------------------------------------------
# FLStudioColors = {   #Inverted from before..
#     1:  (165, 209, 158),  # "Green"),
#     2:  (186, 211, 159),  # "Pale Green"),
#     3:  (208, 214, 161),  # "Teal"),
#     4:  (216, 202, 163),  # "Light Blue"),
#     5:  (219, 184, 165),  # "Blue"),
#     6:  (222, 167, 168),  # "Violet"),
#     7:  (222, 167, 188),  # "Purple"),
#     8:  (222, 167, 209),  # "Fuschia"),
#     9:  (214, 167, 221),  # "Pink"),
#     10: (192, 165, 219),  # "Red"),
#     11: (169, 163, 217),  # "Red-Orange"),
#     12: (162, 175, 214),  # "Orange"),
#     13: (160, 193, 212),  # "Orange-Yellow"),
#     14: (158, 210, 209),  # "Yellow"),
#     15: (158, 209, 189),  # "Yellow-Green"),
#     16: (157, 209, 169)  # "Light-Green")
# }

#SAVE THIS, I'm testing something over the long term... #TODO 1\21\2021
#SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
FLStudioColors = {
    1: (158, 209, 165),  # "Green"),
    2: (159, 211, 186),  # "Pale Green"),
    3: (161, 214, 208),  # "Teal"),
    4: (163, 202, 216),  # "Light Blue"),
    5: (165, 184, 219),  # "Blue"),
    6: (168, 167, 222),  # "Violet"),
    7: (188, 167, 222),  # "Purple"),
    8: (209, 167, 222),  # "Fuschia"),
    9: (221, 167, 214),  # "Pink"),
    10: (219, 165, 192),  # "Red"),
    11: (217, 163, 169),  # "Red-Orange"),
    12: (214, 175, 162),  # "Orange"),
    13: (212, 193, 160),  # "Orange-Yellow"),
    14: (209, 210, 158),  # "Yellow"),
    15: (189, 209, 158),  # "Yellow-Green"),
    16: (169, 209, 157)  # "Light-Green")
}

# FLStudioMayaviColors = {
#     1:  (0.6470588235294118, 0.8196078431372549, 0.6196078431372549 ),
#     2:  (0.7294117647058823, 0.8274509803921568, 0.6235294117647059 ),
#     3:  (0.8156862745098039, 0.8392156862745098, 0.6313725490196078 ),
#     4:  (0.8470588235294118, 0.792156862745098,  0.6392156862745098 ),
#     5:  (0.8588235294117647, 0.7215686274509804, 0.6470588235294118 ),
#     6:  (0.8705882352941177, 0.6549019607843137, 0.6588235294117647 ),
#     7:  (0.8705882352941177, 0.6549019607843137, 0.7372549019607844 ),
#     8:  (0.8705882352941177, 0.6549019607843137, 0.8196078431372549 ),
#     9:  (0.8392156862745098, 0.6549019607843137, 0.8666666666666667 ),
#     10: (0.7529411764705882, 0.6470588235294118, 0.8588235294117647 ),
#     11: (0.6627450980392157, 0.6392156862745098, 0.8509803921568627 ),
#     12: (0.6352941176470588, 0.6862745098039216, 0.8392156862745098 ),
#     13: (0.6274509803921569, 0.7568627450980392, 0.8313725490196079 ),
#     14: (0.6196078431372549, 0.8235294117647058, 0.8196078431372549 ),
#     15: (0.6196078431372549, 0.8196078431372549, 0.7411764705882353 ),
#     16: (0.615686274509804,  0.8196078431372549, 0.6627450980392157 )}

#DITTO
#SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
FLStudioMayaviColors = {
    1: (0.6196078431372549, 0.8196078431372549, 0.6470588235294118),
    2: (0.6235294117647059, 0.8274509803921568, 0.7294117647058823),
    3: (0.6313725490196078, 0.8392156862745098, 0.8156862745098039),
    4: (0.6392156862745098, 0.792156862745098, 0.8470588235294118),
    5: (0.6470588235294118, 0.7215686274509804, 0.8588235294117647),
    6: (0.6588235294117647, 0.6549019607843137, 0.8705882352941177),
    7: (0.7372549019607844, 0.6549019607843137, 0.8705882352941177),
    8: (0.8196078431372549, 0.6549019607843137, 0.8705882352941177),
    9: (0.8666666666666667, 0.6549019607843137, 0.8392156862745098),
    10: (0.8588235294117647, 0.6470588235294118, 0.7529411764705882),
    11: (0.8509803921568627, 0.6392156862745098, 0.6627450980392157),
    12: (0.8392156862745098, 0.6862745098039216, 0.6352941176470588),
    13: (0.8313725490196079, 0.7568627450980392, 0.6274509803921569),
    14: (0.8196078431372549, 0.8235294117647058, 0.6196078431372549),
    15: (0.7411764705882353, 0.8196078431372549, 0.6196078431372549),
    16: (0.6627450980392157, 0.8196078431372549, 0.615686274509804)}


##MIDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def filter_notes(stream, key="", chord=None, offset_range=None, in_place=True):
    #TODO Rename card.
    """
        Removes notes from a stream if they are not pitches that are part of the given key or chord form.

    :param stream:      The operand stream.
    :param key:         String indicating a music21.key.Key object for the chosen key.
    :param chord:       String indicating a music21.chord.Chord() object for the chosen chord. (i.e "CEG", "BDF").
    :param in_place:    A boolean for to either operate directly on the input stream or return a deepcopy.
    :return
    """

    s = stream if in_place is True else copy.deepcopy(stream)
    # if in_place:
    #     s = stream
    # else:
    #     s = copy.deepcopy(stream)


    print(f"Key is: {key}")
    if key == "":
        key = None
        keysig = None
    else:
        keysig = music21.key.Key(key)



    # Create the list of allowed pitches.
    allowedPitches = list()
    if key == None and chord is None:
        allowedPitches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Because a chord is a finer selection then an entire key, this parameter overrides 'key'
    # with that fineness and modifies the allowedPitches list accordingly.
    elif chord:
        allowedPitches = [i.pitchClass for i in chord.pitches]

    elif (type(keysig) is music21.key.Key):
        for p in music21.scale.Scale.extractPitchList(keysig.getScale()):
            allowedPitches.append(p.pitchClass)
    # print(f"AllowedPitches: {allowedPitches}")

    # remove notes that aren't in allowed pitches
    if offset_range is None:
        for n in list(s.recurse()):
            if type(n) is music21.chord.Chord:
                for p in n.pitches:
                    if p.pitchClass not in allowedPitches:
                        print(f"removed_pitch:{p}")
                        n.remove(p)
            elif type(n) is music21.note.Note:
                # print(f"n.pitch.pitchClass: {n.pitch.pitchClass}")
                if (n.pitch.pitchClass not in allowedPitches):
                    s.remove(n, recurse=True)
                    print(f"removed_note:{n}")
    else:
        for n in list(s.recurse()):
            if offset_range[0] <= n.offset < offset_range[1]:
                #print(f"n.pitch.pitchClass: {n.pitch.pitchClass}")
                if type(n) is music21.chord.Chord:
                    for p in n.pitches:
                        if p.pitchClass not in allowedPitches:
                            print(f"removed_pitch_within_range:{p}")
                            n.remove(p)
            #if offset_range[0] <= n.offset < offset_range[1]:
                elif type(n) is music21.note.Note:
                    if n.pitch.pitchClass not in allowedPitches:
                        #print("removing..")
                        s.remove(n, recurse=True)
                        print(f"removed_note_within_range:{n}")

        # s.show('txt')

    print("HERE1")
    #Some cleanup so that s.write works properly because of a 'divide by zero' error that happens if we don't.
    s = delete_nonpitch_chords(s)
    print("HERE2")

    return s

    # if in_place:
    #     stream = s
    # else:
    #     return s

def delete_nonpitch_chords(in_stream, in_place=True):
    """
        The purpose of this function is to remove the actual music21.chord.Chord() objects from the stream if\when
    their "pitch" values are negated\deleted as is the case in the use of filter_notes. This function then will allow
    for said stream's stream.write() method to execute.
    :param in_stream:       Operand stream.
    :param in_place:        Bool determining whether to return in_stream or a deep copy.
    :return:
    """
    s = in_stream if in_place else copy.deepcopy(in_stream)

    for i in s.flat.notes:
        if len(i.pitches) == 0:
            s.remove(i, recurse=True)

    return s



def progressify_directory(directory, progression_stream=None, progression=None, stretch=True, write=True, file_path=None):
    """

    :param directory:
    :param progression_stream:
    :param progression:
    :param write:
    :param file_path:
    :return:
    """
    subdir = ""
    parsed = []
    filepaths = []
    for subd, dirs, files in os.walk(directory):
        subdir += subd
        parsed += [music21.converter.parse(subd + os.sep + file) for file in files]
        filepaths += [subd + os.sep + file for file in files]

    if stretch is True:
        print("Finding highest time...")
        highTime = 0
        #parsons =[]
        print("Parsed", parsed)
        highTime += max([i.highestTime for i in parsed])
        #parsons += parsed
        print("Highest Time is...", highTime)
        stretch = highTime
    else:
        pass
    # for subdir, dirs, files in os.walk(directory):
    range_increment = 1
    for file in range(len(parsed)):
        zero_holder = "_00" if int(range_increment) < 10 else "_0"
        # print os.path.join(subdir, file)
        # if filepath.endswith(".asm"):
        #print(filepath)
        path = subdir + os.sep + os.path.basename(filepaths[file]).partition('.mid')[0] + "_PROGRESSIFIED_" + zero_holder + str(range_increment) + ".mid"\
            if file_path is None else file_path
        progressify(vm_stream=parsed[file],     #, #music21.converter.parse(filepath, forceSource=False)
                    progression_stream=progression_stream,
                    progression=progression,
                    stretch=stretch,
                    write=write,
                    file_path=path,
                    range_increment=range_increment)
                    #directory=True
        range_increment += 1



#######
def progressify(vm_stream, progression_stream=None, progression=None, stretch=True,  write=True, file_path=None, range_increment=1):  #, directory=False):
    """
    #TODO Rewrite docs for the entire process. 02/21/2023

    The purpose of this function is the first step in making a piece of visual music midi have the
    same musical progression as a user-specified selection of chords or the same progression as one taken directly from
    a piece of music parsed via the music21 chordify() method. The output of of this function is a tuple containing all
    the necessary data to do exactly that. Our output has chords, offsets, durations, our offset ranges, and finally
    our chopping template; this template is a an instance of midi notes condensed to "C5" on the piano, that give us
    our chop\slicing offsets.
    "(ps_chords, ps_offsets, ps_durations, offset_ranges_list, progression_stream2)

    Progression example: [Suspended 2, Minor 9th, Minor, Minor, Major 7th, Major, Fifth Octave, Fifth 9th]

    Sample workflow:  (to aquire the 'progression' parameter)
    *note_names, = "BABCDEFGGFEDCBAB"
    notes =     [music21.note.Note(i) for i in note_names]
    chord_forms_string_selections = [music21funcs.chord_strings[random.randint(0, len(music21funcs.chord_strings))]for i in notes]
    chords = [music21funcs.note_to_chord(i[0], i[1]) for i in zip(notes, chord_forms_string_selections)]
    progression = chords
    NOTE: This sample workflow ^ must be executed one line at a time, for some reason.

    Sample workflow in for midifiles in a folder: (for example, after split_midi_channels() is used.
    >>>

    ####[music21funcs.chord_dict
    #TODO snap_to_key() function. DONE

    :param vm_in_stream:            Our original visual music image that we wish to be filtered for more musicality.
    :param progression_stream:      A user-selected\created instance of music21.converter.parsed() music.
    :param progression:             A user-selected list of music21.chord.Chord() objects.
    :return:                        pvm_tuple; A tuple of lists.
    """

    #Get a very basic measure-based progression_stream from progression
    if progression_stream is None:
        assert progression is not None, "You must have either a progression or a progression stream."
        progression_stream = music21.stream.Stream(progression)
        offsets = [i for i in range(0, len(progression)*4, 4)]
        for i in range(len(progression_stream)):
            progression_stream[i].offset = offsets[i]
            progression_stream[i].duration.quarterLength = 4  #In a scenario with 16 measures worth of chords, having
                                                              #all the durations equal 4 makes our highestTime equal 64 instead of 61

    #1. Make lengths the same by stretching vm_stream to match progression_stream.
    if stretch is not None and stretch is not False and stretch is not True:
        #stretch_factor = stretch
        vm_stream_highestTime = stretch
        print("vm_stream_highestTime", vm_stream_highestTime)
        stretch_factor = progression_stream.highestTime / vm_stream_highestTime
        music21funcs.restretch_by_factor(vm_stream, stretch_factor)  #In_place is True here.
    elif stretch is True:
        stretch_factor = progression_stream.highestTime / vm_stream.highestTime
        music21funcs.restretch_by_factor(vm_stream, stretch_factor)  #In_place is True here.
    else:
        pass

    #2. Chordify progression_stream.
    #This gets us several things: groups of chords and their respective offsets and durations. These will be established
    #as variables for later use, below for technical reasons.
    #Todo Is makeMeasures necessary?
    progression_stream.makeMeasures()
    progression_stream2 = progression_stream.chordify()

    # MASSIVE CHORDIFY BUG (According to stream.show('txt') that requires fixing by writing to file and THEN re-parsing
    # back into a stream via converter.parse. I don't know if it's chordify() or .write, but the midi output is correct,
    # while stream.show('txt') is wrong. Once written and then reparsed, show('txt') AND the midi match.
    progression_stream2.write("mid", r"C:\Users\Isaac's\Midas\Kivy\resources\intermediary_path\Chop_Template_Score.mid")
    progression_stream2 = music21.converter.parse(
        r"C:\Users\Isaac's\Midas\Kivy\resources\intermediary_path\Chop_Template_Score.mid")

    #print("PS_CHORDS")
    ps_chords = [j for j in progression_stream2.flat.notes]# Had notes only, previously, giving us WAY too many offsets.
    ps_durations = [j.duration.quarterLength for j in progression_stream2.flat.notes]
    ps_offsets = [i.offset for i in progression_stream2.flat.notes]  # list(progression_stream.recurse())?
    ps_offsets_and_ht = [i.offset for i in progression_stream2.flat.notes]
    ps_offsets_and_ht.append(progression_stream2.highestTime)

    #We need an offsets range list because we need to be able to select all notes within ranges between one offset
    #and the next. If we select based only on starting offset, instead of a range-end too, it is possible to miss
    #desired notes for our core operation.
    offset_ranges_list = [[ps_offsets_and_ht[i], ps_offsets_and_ht[i + 1]] for i in range(0, len(ps_offsets_and_ht) - 1)]

    #2.5
    #We consense our progression stream to notes at "C5" with progression_stream's new chordified offsets. This gives us
    #our slicing stencil!
    #If in place were TRUE here, it would retroactively change our ps_chords list.
    progression_stream3 = condense_to_c5(progression_stream2, in_place=False)

    #And then we write it.
    progression_stream3.write("mid", r"C:\Users\Isaac's\Midas\resources\intermediary_path\Chop_Template_Score.mid")
    vm_stream.write("mid", r"C:\Users\Isaac's\Midas\resources\intermediary_path\Restretched_Stencil.mid")


    #3. Slice vm_stream for core filter operation.
    # We USE the data from this function to get a TEMPLATE for the slicing that happens in FL STUDIO using
    # FL's CHOP tool.

    sliced_stream = vm_stream.sliceAtOffsets(offsetList=ps_offsets, addTies=False, inPlace=False)  #ADD TIES MUST BE FALSE FOR OUR PURPOSES HERE, FOR THE HOLY LOVE OF VISUAL MUSIC!

    pvm_tuple = (ps_chords, ps_offsets, ps_durations, offset_ranges_list, progression_stream2, vm_stream)

    #print("CHORDS", ps_chords)
    #sliced_stream = music21funcs.notafy(sliced_stream)

    #4. CORE #TODO Clean up.
    # After slicing, we filter the undesired notes out of our sliced ranges based on our chords.
    filter_ranges(chopped_stream=sliced_stream, pvm_tuple=pvm_tuple)  #This functions operates in place.

    #5. SOLUTION TO PREVIOUS WORKAROUND
    final_stream = music21funcs.notafy(sliced_stream)
    notafied_sliced_filtered_stream = final_stream

    file_path = None if write is False else file_path
    zero_holder = "_00" if int(range_increment) < 10 else "_0"
    zero_holder += str(range_increment)
    if write:
        # if directory:
        #     write_target = file_path + zero_holder
        # else:
        write_target = r".\resources\intermediary_path" + os.sep + "Progressified_Visual_Music_%s.mid" % zero_holder\
            if file_path is None else file_path
        #assert file_path is not None, "Please designate a write path and file name."
        final_stream.write('mid', write_target)

    #NOTE:  #PREVIOUS WORKAROUND!!
    #music21.stream.Stream().sliceAtOffsets isn't accurate enough. So we will be doing a workaround.
    # sliceAtOffsets gets us our operand data, the midi out of which we will be filtering notes we don't need,
    # based on our progression from progression_stream.
    #Once sliceAtOffsets becomes %100 accurate, FL Studio's chop tool won't be needed.

    return (ps_chords,
            ps_offsets,
            ps_durations,
            offset_ranges_list,
            progression_stream2,
            vm_stream,
            notafied_sliced_filtered_stream)  #<-----This be the friggy diggy.



def condense_to_c5(progression_stream, in_place=True):  #pvm_tuple=None,
    """
        This function takes a stream, or a copy.deepcopy of a stream if in_place is False, and returns it with all the
    notes and chords in the stream having their pitch values changed INTO the value for "C4" (C5 in FL Studio.) The
    purposes for this function is to allow for the notes in FL Studio to be used as a chop template of notes. See the FL
    help manual here -->: https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/pianoroll_chp.htm
    Specifically, the section captioned "Guide for making Chop / Arpeggiator patterns" at the bottom of that page.

    :param progression_stream:          Input operand stream.
    :param in_place:
    :return:
    """
    s = progression_stream if in_place is True else copy.deepcopy(progression_stream)
    #for n in progression_stream.flat.getElementsByClass(["Chord"]):
    for n in list(s.recurse()):
        if type(n) is music21.chord.Chord:
            for p in n.pitches:
                n.remove(p)
            n.add(music21.pitch.Pitch("C4"))
        if type(n) is music21.note.Note:
            p = music21.pitch.Pitch("C4")
            n.pitch = p
    return s


## #4. Core
def filter_ranges(chopped_stream, pvm_tuple = None, progression = None):
    """
        Upon acquiring the correctly FL Studio-chopped vm_stream, we filter our 'ranges' of notes in order to create
    our 'progression image,' essentially. In actuality, our workaround method creates our correct filtered progression
    image, but we use it in conjunction with FL tools once again ("Select Overlapping Notes" and "Invert Selection") and
    our ORIGINAL colored to do the final filter inside of FL Studio.

    And thus we create an image of music with a progression that makes it sound good!

    If progression is not None, we assume our chopped_stream will be chopped by measures, and that each "chord" in our
    progression is exactly one measure in length.

    our note subraction.
    :param vm_stream:
    :param pvm_tuple:       A tuple of lists of specific music21 information involving, chords, offsets, and ranges.
                            "(ps_chords, ps_offsets, ps_durations, offset_ranges_list, progression_stream2)"
    :return:                Returns inPlace our chopped vm_music stream, filtered. It basically acts as a stencil.
                            This stencil method will be refined if music21's sliceAtOffsets becomes perfect.
    """

    if progression is not None:
    #Our progression choice, indeed our list of chords must length-match our range slices.
        assert len(progression) == len(pvm_tuple[3])
        for i in range(0, len(progression)):
            filter_notes(chopped_stream, chord=progression[i], offset_range=pvm_tuple[3][i], in_place=True)
    else:
        pass

    # #This loop will operate on the stream multiple times, just on a different range of notes in the stream.
    for i in range(0, len(pvm_tuple[3])):
        filter_notes(chopped_stream, chord=pvm_tuple[0][i], offset_range=pvm_tuple[3][i], in_place=True)
    return chopped_stream  #Chopped and Filtered. Woven.


#######


def snap_to_key(in_stream, key, snap_up=True):
    """
        This function takes a music21 stream and snaps all the pitches in all of the notes and chords in the stream
    to the pitches found in the input string 'key'.

    :param in_stream:   Operand music21.stream.Stream() object.
    :param key:         A string denoting your musical key.
    :param snap_up:     A boolean denoting whether to predominantly snap "upwards" or "downwards" depending on the note.
                        (For example, if we are trying to snap all notes to the key of C# major, and we happen on a
                        D natural, we could either go to the C# OR the D# and it would still be in the key of C# major.
                        This is the case scenario where the interval difference between possible note snap destinations
                        is the same. So we work with it.) True snaps upwards.
    :return:            Our in_stream, modified in place.
    """

    key = music21.key.Key(key)


    #Get matched and non-matched dictionary
    #key = music21.key.Key(key)
    key_concrete_scale = music21.scale.ConcreteScale(pitches=[pitch for pitch in key.pitches])
    print("Key_Concrete_Scale", key_concrete_scale.pitches)

    ##All notes pitchClasses. We will use this to derive key-nonmatching notes.
    chromatic_reference = set([i for i in range(12)])
    print("CHR_Ref", chromatic_reference)
    #Scale notes in key
    scale_notes = set([i.pitchClass for i in key_concrete_scale.pitches])
    print("Scale_notes", scale_notes)
    #The set.difference() between the two.
    difference = chromatic_reference.difference(scale_notes)
    print("Difference", difference)

    #Match method
    #match = key_concrete_scale.match(in_stream)
    #print("KCS", key_concrete_scale)
    #matched, nonmatched = (match['matched'], match['notMatched'])
    #print("matched", matched)
    #print("Nonmatched", nonmatched)

    #nonmatched_pitchclasses = [pc.pitchClass for pc in nonmatched]
    non_key_matched_pitchclasses = [pc for pc in difference]
    print("NM_pitchClasses", non_key_matched_pitchclasses)

    #Transform to C
    #TODO Does match happen before or after transform? I don't think it matters, but keep this note here just in case.
    #transform_value = int(key.getTonic().pitchClassString)
    #music21.note.Note(key.getTonic().step).pitch.pitchClass
    #print("T_value", transform_value)

    #print("Stream before transpose:")
    #in_stream.show('txt')
    #in_stream.transpose(-1 * transform_value, inPlace=True)
    #print("Stream after transpose:")
    #in_stream.show('txt')

    print("NM_pitchClasses_2", non_key_matched_pitchclasses)


    #allowedPitches = []
    #match_dict ={}
    for n in in_stream.flat.notes:
        if type(n) is music21.chord.Chord:
            for p in range(0, len(n.pitches)):
                if n.pitches[p].pitchClass in non_key_matched_pitchclasses:
                    #print("Matched_Pitch_Class", n.pitches[p].pitchClass)
                    if snap_up:
                        snap = n.pitches[p].pitchClass + 1 if n.pitches[p].pitchClass + 1 <= 11 else 0
                        n[p].transpose(1, inPlace=True) if snap not in difference else None
                    else:
                        snap = n.pitches[p].pitchClass - 1 if n.pitches[p].pitchClass - 1 <= 0 else 11
                        n[p].transpose(-1, inPlace=True) if snap not in difference else None
                        #= music21.pitch.Pitch(n.pitches[p].step)  #This is why we use the transform method. Need more checks? (The enharmonics are a problem for using .step())
                    #match_dict.update([(n.pitches[p].pitchClass, n[p])])
        elif type(n) is music21.note.Note:
            if n.pitch.pitchClass in non_key_matched_pitchclasses:
                if snap_up:
                    snap = n.pitch.pitchClass + 1 if n.pitch.pitchClass + 1 <= 11 else 0
                    n.pitch.transpose(1, inPlace=True) if snap not in difference else None
                else:
                    snap = n.pitch.pitchClass - 1 if n.pitch.pitchClass - 1 <= 0 else 11
                    n.pitch.transpose(-1, inPlace=True) if snap not in difference else None

                #= music21.pitch.Pitch(n.step)

    #print("Match_Dict", match_dict)

    #TODO Finish.
    # for p in music21.scale.Scale.extractPitchList(key.getScale()):
    #     allowedPitches.append(p.pitchClass)

    #Transpose back from C to "key."
    #in_stream.transpose(transform_value, inPlace=True)

    for i in in_stream.flat.notes:
        for pitch in i.pitches:
            assert pitch.pitchClass not in difference, "Snap failed here: --> %i" % str(pitch.pitchClass) + '___' + str(i)
            #if pitch.pitchClass in difference:

    #in_stream.makeAccidentals
    return in_stream


# MA-2.
def make_midi_from_colored_pixels(pixels, granularity, connect=False, colors=None):
    """
        Make midiart from pixels.  Splits into colors of FLStudio piano roll.  #TODO Redoc this. 12/01/20
    :param pixels: 			The 2D array of pixel values. each element of 2D array must be a tuple with RGB values (R,G,B)
    :param granularity: 	like music21's quarterlength.  4=each 'pixel' is whole note, 1=quarternote, 0.5=eightnote etc.
    :param connect: 		True means connect adjacent notes.
    :param colors			The dict of colors to use.  if colors=None, will use FLStudio Piano Roll colors
    :return:                music21.stream.Stream
    """

    if len(pixels) > 128:
        raise ValueError("The .png file size is too large.")
        return None

    # Establish variables.
    #part_stream = music21.stream.Stream()
    out_stream = music21.stream.Stream()

    if colors == None:
        colors = FLStudioColors

    colors_constraints = [colors[c] for c in range(1 , 17)]

    for q in colors:
        part = music21.stream.Part()
        part.partsName = q
        #part.partName = q
        #part.offset = 0

        for y in range(0, len(pixels)):
            for x in range(0, len(pixels[y])):
                if tuple(pixels[y][x].flatten()) == colors[q]:
                    print(tuple(pixels[y][x].flatten()), "TRUE!?!", tuple(pixels[y][x].flatten()) == colors[q])
                    newpitch = music21.pitch.Pitch()
                    newpitch.ps = 127 - y
                    n = music21.note.Note(newpitch)

                    n.offset = x
                    totalduration = granularity

                    if connect:
                        print("X+1", x+1)
                        print("len(pixels[y]", len(pixels[y]))
                        print("Is this true???", (x+1) < len(pixels[y]))
                        while (x + 1) < len(pixels[y]) and tuple(pixels[y][x + 1].flatten()) == colors[q]:
                            totalduration = totalduration + granularity

                            substitution = tuple([random.randint(0, 255) for i in range(0, 3)])
                            while substitution in colors_constraints:
                                substitution = tuple([random.randint(0, 255) for i in range(0, 3)])

                            pixels[y][x + 1] = substitution

                            x = x + 1
                        print("Connected!")
                    d = music21.duration.Duration()
                    d.quarterLength = totalduration
                    n.duration = d
                    part.insert(n.offset * granularity, copy.deepcopy(n))

        out_stream.insert(part.offset, copy.deepcopy(part))

    # print("Stream created.")
    # out_stream.show('txt')
    return out_stream

#TODO I don't like the word "grayscale" here. It should just be "black and white," as this function is used mainly for QR codes.
def make_midi_from_grayscale_pixels(pixels, granularity, connect=False, note_pxl_value=255):
    """
        Make midi picture from greyscale\blackandwhite image.

    :param pixels: 		    The 2D array of pixel values. Each element is a single grayscale value.  0=Black, 255=White.
    :param granularity:     like music21's quarterlength. 4= 'pixel' is whole note, 1=quarternote, 0.5=eightnote etc.
    :param connect: 		True means connect adjacent notes.
    :param note_pxl_value:  note_pxl_value determines which pixels will count as notes.
                            0=Black, 255=White, or any gray value 0-255.
    :return:                music21.stream.Stream
    """

    out_stream = music21.stream.Stream()
    for y in range(0, len(pixels)):
        for x in range(0, len(pixels[y])):
            if pixels[y][x] == note_pxl_value:
                newpitch = music21.pitch.Pitch()
                newpitch.ps = 127 - y
                n = music21.note.Note(newpitch)
                # n.pitch.midi = 127 - y
                totalduration = granularity
                n.offset = x
                if connect:
                    while (x + 1) < len(pixels[y]) and pixels[y][x + 1] == note_pxl_value:
                        totalduration = totalduration + granularity

                        pixels[y][x + 1] = abs(note_pxl_value - 1)
                        x = x + 1

                d = music21.duration.Duration()
                d.quarterLength = totalduration
                n.duration = d
                out_stream.insert(n.offset * granularity, n)

    return out_stream


###TODO Figure out threshold ranges. K-D Trees stuff. (by threshold ranges, at the time, I was processing the how-to of this function in a different way then it ended up 09/25/20)
def set_to_nn_colors(im_array, clrs=None):
    """
        This function takes a 3D numpy color array(i.e an image), and reduces\\converts all of the color tuples of that
    image to 16 possible different colors. For Visual Music purposes, this allows for display in FL studio with those
    16 colors.

    :param im_array:    A 3D numpy image array.
    :param clrs:        A user defined dictionary of colors, allowing for greater possibility of colors for future
                        applications. If clrs=None, will default to using the FLStudio Piano Roll colors

    :return:
    """
    if clrs == None:
        clrs = FLStudioColors
    elif type(clrs) == dict:
        clrs = clrs
    else:   #If not a dict, but a list of 16 color tuples generated randomly
        l_clrs = array_to_lists_of(clrs)
        clrs = dict.fromkeys(b for b in range(len(l_clrs)))
        for cr in range(0, len(l_clrs)):
            for qv in l_clrs:
                clrs[cr] = qv

    # REMOVE redundant points. (otherwise, the kd search will be a disaster.)
    # shift_cloud = im_array.reshape((-1, 3))
    # clean_cloud = musicode.mc.delete_redundant_points(shift_cloud)

    # Place operand coords_array into open3d point cloud.
    pcloud = open3d.geometry.PointCloud()
    p_lizt = list()
    for ix in range(1, len(clrs)):
        p_lizt.append(clrs[ix])
    p_array = np.array(p_lizt)
    pcloud.points = open3d.utility.Vector3dVector(p_array)
    #Note -- ".utility" doesn't work on laptop --> It's possible the open3d on laptop hasn't been updated.
    kd_tree = open3d.geometry.KDTreeFlann(pcloud)

    # work_cloud = musicode.mc.array_to_lists_of(clean_cloud)
    # for x in range(1, len(work_cloud)):
    im_list = list()
    for x in range(len(im_array)):
        for y in range(len(im_array[x])):
            im_dex = np.array(im_array[x][y], dtype=np.float16)
            # im_list.append(im_dex)
            # for i in im_list:
            k_idx_list = kd_tree.search_knn_vector_3d(im_dex, 1)
            index = k_idx_list[1][0] + 1
            im_array[x][y] = clrs[index]
    # work_array = np.array(work_cloud)
    # final_array = work_array.reshape(im_array.shape)
    # return final_array
    return im_array


def set_parts_to_midi_channels(in_stream, output_file):  # TODO Should be a music21funcs function?
    """
        Assuming that notes are allocated to particular parts in a music21 stream, this function takes those parts and
    allocates them to specific midi channels in a midifile. This changes how midi data is imported in DAWS and the like.

    :param in_stream:       Stream with 16 parts that we are turning into a midi file.
    :param output_file:     Full path to output midi full.
    :return:                Writes music21.stream.Stream data to a midifile. This function doesn't return anything.
    """
    #print("TyPe", type(in_stream[0]))
    #part_name_0 = copy.deepcopy(in_stream[0].partName)
    #print("PART", part_name_0)
    #TODO Create conditional call for the execution of these cleanups.
    #offset_dict, offsets, dict_list = music21funcs.get_offsets_dictionary(copy.deepcopy(in_stream[0]))
    #if music21funcs.check_for_offset_duplicates(offset_dict) is True:

    # in_stream_0 = copy.deepcopy(in_stream[0])
    # in_stream_0.makeMeasures(inPlace=True)
    # print(in_stream_0.getOverlaps())
    #print("Before Love.", len(in_stream.getOverlaps()))

    #offset_dict, offsets, dict_list = music21funcs.get_offsets_dictionary(in_stream[0].flat)
        # print("HERE_11")
        # maxxi = max([j.duration.quarterLength for j in in_stream[0].flat.notes]) #This ---*
        # print("Maxxi", maxxi)
        # highest_dur_notes = [i for i in in_stream[0].flat.notes
        #                if i.duration.quarterLength == maxxi]   #*---- had to be removed from here for this to work right.
        # print("Highest_Duration_Notes", highest_dur_notes)
        # if len(highest_dur_notes) == 0:
        #     check = ['empty_list']   #If this function works properly, I should never see this print.
        #     print("Check_0", check)
        #     pass
        # else:
        #     first_highest_dur_note = highest_dur_notes[0]
        #     #fhdn_offset = first_highest_dur_note.offset   #start of span
        #     #fhdn_highestTime = first_highest_dur_note.duration.quarterLength   #end of span
        #     check = [k for k in in_stream[0].flat.notes if k.pitch.ps == first_highest_dur_note.pitch.ps]
        #     print("CHECK", check, len(check))
        #
        #
        # print("HERE_7")
        # # if len(in_stream[0].getOverlaps()) == 0:   #The logic here is backwards on purpose; I am unable to explain why.
        # #     print("In_Stream[0] had duplicates, initiating workaround.")
        # if len(check) != 1:
        #     chordified = in_stream[0].chordify(removeRedundantPitches=False)
        #     print("HERE_7.5")
        #     notafied = music21funcs.notafy(chordified) #, part=True, inPlace=True, chordifyFirst=True, specialMerge=True)
        #     print("HERE_7.6")
        #     merged = music21funcs.merge_contiguous_notes(notafied)
        #     print("HERE_7.7")
        #     for i in in_stream[0].flat.notes:
        #         in_stream[0].remove(i)   #Remove all notes inplace.
        #     for j in merged.flat.notes:
        #         in_stream[0].insert(j.offset, j)    #Insert new notes inplace.
        # else:
        #     print("In_Stream[0] had NO duplicates, passing...")
        #     pass
        # print("HERE_8")
        #
        #
        # # in_stream[0] = repair_part
        # #in_stream[0].partName = part_name_0
        # print("partName", in_stream[0].partName)
        # for i in range(len(in_stream)):
        #     #print("allParts", in_stream.partsName)
        #     print("allPart", in_stream[i].partName)

    # Create the operand .mid file from in_stream.
    in_stream.write('mid', output_file)  # Include filename.mid in fptf.
    #in_stream[0].write('mid', output_file+"_TEST11.mid")

    # Change stream to list of miditracks (if one wishes to view the data.
    ##Given a Stream, Score, Part, etc., that may have substreams
    ##(i.e., a hierarchy), return a list of MidiTrack objects.
    # midi_view1 = midi.translate.streamHierarchyToMidiTracks(in_stream, acceptableChannelList=None)
    # print(midi_view1)

    # Establish clrs_list for reference call.
    clrs_list = list()
    for i in range(1, 17):
        clrs_list.append(i)

    # Create music21.midi.MidiFile() object.
    sparky = music21.midi.MidiFile()
    sparky.open(output_file, attrib='rb')
    # sparky.tracks
    sparky.read()
    # sparky.tracks
    # for i in range(1, len(sparky.tracks)):
    for j in clrs_list:
        if len(sparky.tracks) < 18:   #Todo Better way to write this.
            sparky.tracks[j - 1].setChannel(j)
        elif len(sparky.tracks) > 16:
            print("Check your .mid file data. There may be an extra track at the beginning or another problem.")

    # if t < 17:
    #     t += 1
    sparky.close()
    sparky.open(output_file, attrib='wb')
    sparky.write()
    sparky.close()


# MA-3.
def make_pixels_from_midi(in_stream, color=(255, 255, 255), background_color=(0,0,0), gran=16):
    """
        This function takes the musical offset and pitch data from a music 21 stream and converts those values back to a
    numpy image array.    ....gran was originally 16, for whatever reason.

    :param in_stream:
    :return:            numpy array
    """

    # temp_stream = musicode.mc.notafy(in_stream)
    # volume-z_list = list()

    max_list = []
    for n in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        if type(n) is music21.chord.Chord:
            for i in n.notes:
                max_list.append(i.pitch.ps)
        elif type(n) is music21.note.Note:
            max_list.append(n.pitch.ps)
    max_ray = np.array([max_list])
    print("HIGHEST_NOTE_PITCH", max_ray.max(initial=None))

    a = np.full((127, (int(in_stream.highestTime * gran)), 3), background_color)
    # b = np.zeros((127, int(in_stream.highestTime), 3))
    # b = np.rot90(a, 1, (0, 1))
    in_stream.makeMeasures(inPlace=True)
    temp_stream = music21funcs.notafy(in_stream)
    for n in temp_stream.flat.notes:
        # if xy.volume.velocity is None:
        #     print("There are no velocity values for these notes. Assign velocity values.")
        #     return None
        x = int(n.offset * gran)
        y = n.pitch.midi

        i = 0
        while i < n.duration.quarterLength * gran:
            a[y + i][x] = color  ### = 1
            while i != 126:
                i += 1
    b = np.rot90(a, 2)
    c = np.fliplr(b)
    return c


# MA-4.
def strip_midi_by_chords(in_stream, directory):
    """
        Function for stripping columns of notes that comprise a music21.stream.Stream into a list of streams with those
    same columns of notes, i.e vertical strips of notes.
    
    :param in_stream:
    :param directory:
    :return:
    """
    num = 0
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        for c in m.getElementsByClass(["Chord", "Note"]):
            temp = music21.stream.Stream()
            temp_measure = music21.stream.Measure()
            temp_measure.offset = m.offset
            temp_measure.number = m.number
            temp_measure.insert(c.offset, c)
            temp.insert(temp_measure.offset, temp_measure)
            print("---")
            temp.write("mid", directory + "\\" + repr(num) + ".mid")
            num = num + 1


# MA-5.
def strip_midi_by_pitchrange(in_stream, range_l, range_h, directory=None):
    """
        Function for stripping rows of notes based on pitch that comprise a music21.stream.Stream into a list of streams
    with those same rows of notes, i.e horizontal strips of notes.

    :param in_stream:
    :param range_l:
    :param range_h:
    :param directory:
    :return:
    """
    num = 0
    temp_stream = music21.stream.Stream()
    notelist = list()

    for m in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        # print("Measure ", repr(m.number))

        if type(m) is music21.chord.Chord:
            for p in m.pitches:
                newnote = music21.note.Note(p)
                newnote.offset = m.offset
                newnote.duration = m.duration
                notelist.append(newnote)
        elif type(m) is music21.note.Note:
            notelist.append(m)

    # temp_measure = stream.Measure()
    # temp_measure.offset = m.offset
    # temp_measure.number = m.number

    for n in notelist:
        # print("Note midi value: ", repr(n.pitch.midi))
        if n.pitch.midi >= range_l and n.pitch.midi <= range_h:
            # print("inserting: m=", repr(m.measureNumber))
            # temp_measure.insert(n.offset, n)
            # print(" m.offset=",repr(m.offset),", m.num=",repr(m.measureNumber),",
            #temp.offset=",repr(temp_measure.offset),", temp.num=",repr(temp_measure.measureNumber))

            temp_stream.insert(n.offset, copy.deepcopy(n))
    print("---")
    if directory is not None:
        temp_stream.makeMeasures()
        temp_stream.write("mid", directory + "\\" + repr(range_l) + "-" + repr(range_h) + ".mid")
    else:
        temp_stream.makeMeasures(inPlace=True)
        return temp_stream


# MA-6.
def stagger_pitch_range(in_stream, stepsize=1, ascending=True, starting_offset=None, range_l=0, range_h=128):
    """
        This functions staggers notes in a manner similar to the italicizing of text. 	So, every subsequent horizontal
    strip of notes above\below where you want to start gets cumulatively shifted in offset, as if arpeggiated, allowing
    for a staggered appearance.

    :param in_stream:       Input stream.
    :param stepsize:        Quarter length of offset step for arpeggiation.
    :param ascending:       True = ascending appegiation, False = descending arpeggiation
    :param starting_offset: Default None uses the starting offset of the first note of lowest pitch if ascending=True,
                            or highest if ascending=False. Otherwise, directly specify starting offset.
    :param range_l:         Low range is specified by the starting note's offset.
    :param range_h:         Determines # of strips to be arpeggiated in relation to the starting note's offset.
    :return:                Returns a new music21.stream.Stream() object.
    """

    # Step 1
    notelist = list()
    # notelist2 = list()
    # in_stream = in_stream.makeMeasures()
    for c in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        if type(c) is music21.chord.Chord:
            for p in c.pitches:
                newnote1 = music21.note.Note(p)
                newnote1.offset = c.offset
                newnote1.duration = c.duration
                notelist.append(newnote1)
        elif type(c) is music21.note.Note:
            notelist.append(c)
    # print("Notelist")
    for n in notelist:
        print(n)
    # Step Frickin 2: Starting Offset
    if starting_offset is not None:
        start = starting_offset
    else:
        if ascending == True:
            current_lowest = music21.note.Note()
            current_lowest.offset = in_stream.highestTime
            current_lowest.pitch.midi = range_h
            for n in notelist:
                if n.pitch.midi >= range_l and n.pitch.midi <= range_h:
                    if n.pitch.midi <= current_lowest.pitch.midi and n.offset < current_lowest.offset:
                        current_lowest = n
            start = current_lowest.offset
        else:
            current_highest = music21.note.Note()
            current_highest.offset = in_stream.highestTime
            current_highest.pitch.midi = range_l
            for n in notelist:
                if n.pitch.midi >= range_l and n.pitch.midi <= range_h:
                    if n.pitch.midi >= current_highest.pitch.midi and n.offset < current_highest.offset:
                        current_highest = n
            start = current_highest.offset

    # print("start=%d" % start)
    # Step Frickin 3
    temp_stream = music21.stream.Stream()
    # temp_measure = stream.Measure()
    # temp_measure.offset = m.offset
    # temp_measure.number = m.number
    start_p = range_l if ascending else range_h
    stop_p = range_h if ascending else range_l
    step_p = 1 if ascending else -1

    for o in range(start_p, stop_p, step_p):
        notez = strip_midi_by_pitchrange(in_stream, o, o)
        if notez.flat.hasElementOfClass("Note"):  # if "notes" has actual notes in it:
            for l in notez.flat.notes:
                # print(l)
                new_note_offset = start + l.offset - notez[0].offset
                temp_stream.insert(new_note_offset, copy.deepcopy(l))
            start = start + stepsize
    temp_stream.makeMeasures(inPlace=True)
    return temp_stream


# MA-7. TODO: def stagger_offset_range():

# MA-8.
def transcribe_colored_image_to_midiart(img, granularity=1, connect=False, keychoice=None, colors=None,
                                        output_path=None):
    """
        This function is the commonly called transcribe function for creating musical images.

    :param im_path:         A file path or numpy array of an image.
    :param granularity:     quarterLength value determines the offset and duration values of all the notes transcribed.
    :param connect:         The contiguity feature. Notes chopped by default. True connects adjacent notes contiguously.
    :param keychoice:       The key of the piece, specified as a string(i.e. "C" for C Major or "C#m" for C Sharp Minor)
    :param colors:#TODO Fix:If True, note_pxl_value becomes irrelevant, and this enables use of the image's color tupls.
    :param output_path:     Directory to which output will be written, specified as a string. If None, does not write
                            to file.
    :return:                Returns a music21.stream.Stream() object.
    """
    if type(img) == str:
        img = cv2.imread(img, cv2.IMREAD_COLOR)

    if img.ndim != 3:
        print("Incorrect numpy array format.  Colored image numpy array should have shape (x,y,3).")
        print(f" Your input img had shape {img.shape}.")
        return None

    if len(img) > 127:
        print("The .png file size is too large. Scaling to height of 127.")
        height = 127
        width = int(127 / len(img) * len(img[0]))
        img = cv2.resize(img, (width, height), cv2.INTER_AREA)
    print("Image check:", img)
    img_nn = set_to_nn_colors(img, colors)
    print("NN_check:", img_nn)
    s = make_midi_from_colored_pixels(img_nn, granularity, connect, colors)
    print("Stream Created.", s)
    s.show('txt')
    filter_notes(s, keychoice, in_place=True)
    if output_path is not None:
        set_parts_to_midi_channels(s, output_path)

    return s

# MA-9.
def transcribe_grayscale_image_to_midiart(img, granularity, connect, keychoice=None, note_pxl_value=255,
                                          output_path=None):
    """
        This function is the commonly called transcribe function for creating musical QR codes, but can be used for an
    image as well.

    :param img:             A file path or numpy array of an image.
    :param granularity:     quarterLength value determining the offset and duration values of all the notes transcribed.
    :param connect:         Contiguity feature. Notes chopped by default. "True" connects adjacent notes contiguously.
    :param keychoice:       The key of the piece, specified as a string(i.e. "C" for C Major or "C#m" for C Sharp Minor)
    :param note_pxl_value:  When not doing clrs, images are converted to having black and white pixels. A value of 255
                            or 0 will determine what of those pixels from the image will be turned into notes.
    :param output_path:     Directory + filename to which output will be written, specified as a string.

    :return:                Returns a music21.stream.Stream() object.
    """

    if type(img) == str:
        img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    if img.ndim != 2:
        print("Incorrect numpy array format.  Grayscale image numpy array should have shape (x,y).")
        print(f" Your input img had shape {img.shape}.")
        return None

    if len(img) > 127:
        print("The .png file size is too large. Scaling to height of 127.")
        height = 127
        width = int(127 / len(img) * len(img[0]))
        img = cv2.resize(img, (width, height), cv2.INTER_AREA)

    s = make_midi_from_grayscale_pixels(img, granularity, connect, note_pxl_value)
    print("Stream Created.")
    filter_notes(s, keychoice, in_place=True)

    if output_path is not None:
        s.write('mid', output_path)

    return s


# MA-10.
def transcribe_image_edges_to_midiart(image_path, height, granularity, midi_path, connect, keychoice=None,
                                      note_pxl_value=255, clrs=False):
    """
        This function is the commonly called function for creating musical edge-detected images. It inherits parameters
    from "make_midi_from_pixels."

    :param image_path:      A filepath or numpy array of an image.
    :param height:
    :param granularity:
    :param midi_path:       Directory to which output will be written, specified as a string. i.e r"C:\\Users\ah\arg..."
    :param connect:         The contiguity feature. Notes are chopped by default. Connect=True connects adjacent notes
                            contiguously.
    :param keychoice:       The key of the piece, specified as a string(i.e. "C" for C Major or "C#m" for C Sharp Minor)
    :param note_pxl_value:  When not doing clrs, images are converted to having black and white pixels. A value of 255
                            or 0 will determine what of those pixels from the image will be turned into notes.
    :param clrs:            If True, note_pxl_value becomes irrelevant, and this enables use of the image's color tupls.
    :return:                Returns a music21.stream.Stream() object.
    """
    if type(image_path) == numpy.ndarray:
        img = image_path
        small = cv2.resize(image_path, (int(height / len(img) * len(img[0])), height), cv2.INTER_AREA)
    elif type(image_path) == str:
        # If a file path,
        img = cv2.imread(image_path, 0)
        small = cv2.resize(img, (int(height / len(img) * len(img[0])), height), cv2.INTER_AREA)

    edges = cv2.Canny(small, 100, 200)

    s = make_midi_from_grayscale_pixels(edges, granularity, connect, note_pxl_value)

    filter_notes(s, keychoice, in_place=True)

    s.write('mid', midi_path)
    return s


# MA-11.
def extract_sub_melodies(stream, keep_dur=False, chop_durs=False, offset_interval=0.25):
    """
        This function creates a list of streams that are the random permutations of possible melodies of the notes found
    within the input music21 stream. Each note in the input m21 stream will only be used once in that random creation
    of melodies.

    :param stream:          Input music21 stream.
    :param keep_dur:        If true, notes longer than offset interval will be chopped up into individual notes of
                            duration = offset interval.
    :param chop_durs:       If chop_durs = True, notes will be chopped up into notes with duration = offset interval.
    :param offset_interval: quarterLength value determining "get_next_note" search. (4=whole note, 2=halfnote,
                            1=quarternote, 0.5=eighthnote,etc.)
    :return:                Returns a list of streams/
    """

    # """
    # keep_dur:
    # offset_interval: in quarterLengths
    #
    # """

    def get_next_note(in_stream, current_offset):
        # """
        #
        # :param
        # :param in_stream:         The music 21 stream to be input into the function.
        # :param current_offset:    Current_offset is the offset input to indicate where to start looking for the
        #                           "next note."
        # :param offset_interval:   Granularity, the offset_interval is\uses the quarterLength feature of music21, to
        #                           indicate how far to search for the "next note" after the "current offset."
        # :return:
        # """
        # This function needs to know:
        # Stream
        # Random selection of specified Notes and Offsets
        # Specified offsets for repopulation
        print("current_offset ", current_offset)
        z = None
        if current_offset > in_stream.flat.highestOffset:
            print(" No more notes")
            return "no more"

        notelist = []
        objs_at_current_offset = in_stream.flat.getElementsByOffset(current_offset, mustBeginInSpan=(not keep_dur))
        for e in objs_at_current_offset:
            if type(e) is music21.chord.Chord:
                print("Chord")
                for p in e.pitches:
                    newnote = music21.note.Note(p)
                    newnote.offset = e.offset
                    newnote.duration = e.duration
                    notelist.append(newnote)
                    print("note ", newnote.pitch)
                    print("offset ", newnote.offset)
                    print("duration ", newnote.duration)

            elif type(e) is music21.note.Note:
                print("Note")
                newnote = music21.note.Note(e.pitch)
                newnote.offset = e.offset
                newnote.duration = e.duration
                notelist.append(newnote)
                newnote.show('txt')

            else:
                print(e)

        if (len(notelist) > 0):
            x = random.choice(notelist)
            print("Choose: ", x.pitch)

            # need to remove the chosen note from in_stream
            for e in objs_at_current_offset:
                if type(e) is music21.chord.Chord:
                    try:
                        e.remove(x.pitch)
                        print("removing from chord ", x.pitch)
                        print(" num remaining notes in chord", len(e.pitches))

                        if (len(e.pitches) == 0):
                            print("removing empty chord")
                            in_stream.remove(e, recurse=True)
                    except ValueError:
                        print("Not in this chord.")
                elif type(e) is music21.note.Note and e.pitch == x.pitch:
                    print("removing single note", e.pitch)
                    in_stream.remove(e, recurse=True)

            return x
        elif current_offset < in_stream.flat.highestOffset:
            return "more"
        else:
            return "no more"

    stream_list = []

    new_stream = copy.deepcopy(stream)
    print("start")
    if (chop_durs):
        new_stream = music21funcs.chop_up_notes(new_stream, offset_interval)

    done = False
    while not done:
        s = music21.stream.Stream()
        current_offset = 0

        n = get_next_note(new_stream, current_offset)
        while n != "no more":

            if n != "more":
                s.insert(current_offset, n)
            current_offset = current_offset + offset_interval
            n = get_next_note(new_stream, current_offset)
        stream_list.append(s)
        print("Submelody: ")
        s.show("txt")
        print("Remaining Notes: ")
        new_stream.flat.show('txt')
        print("Are we done?")
        if len(new_stream.flat.notes) == 0:
            done = True

    return stream_list


# TODO Requires revising, possibly is redundant.
# MA-12.
def get_random_melody(in_stream):
    """
        A smaller function than extract_sub_melodies, this function creates a stream of one melody at random from an
    input stream.

    :param in_stream:   Stream from which a random melody will be derived.
    :return:            A new music21.stream.Stream() object.
    """

    neu_stream = music21.stream.Stream()
    for z in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        newballs = copy.deepcopy(z)
        newballs.offset = z.offset
        notelist = []
        if type(z) is music21.chord.Chord:
            for p in z.pitches:
                newnote = music21.note.Note(p)
                newnote.offset = z.offset
                newnote.duration = z.duration
                notelist.append(newnote)
                print("note ", newnote.pitch)
                print("offset ", newnote.offset)
                print("duration ", newnote.duration)
            x = random.choice(notelist)
            x.show('txt')
            neu_stream.insert(x)

        elif type(z) is music21.note.Note:
            neu_stream.insert(z)
    neu_stream.makeMeasures()
    # new_stream.makeMeasures()
    return neu_stream


# MA-13. #TODO Optimize for better sectionalizing.
def sectionalize_image_array(image_array, sec_root):
    """
        #TODO Needs to be redone.
        This functions creates smaller, proportional "tiles" of an input image array that can be indexed.

    :param image_array:     An input cv2-read image array.
    :param sec_root:        The square root of the # of desired sections. If you want 64 sections, set sec_root to 8.
    :return:                A list of smaller, evenly shaped arrays that piece back together to form the original image.
    """

    # Initial split, right down the middle. (Or more, for very large images with high resolution.
    i_split = sec_root
    split1 = np.array_split(image_array, i_split)
    # Establish lists, for calling.
    split_arrays = list()
    split_arrays2 = list()
    split_arrays3 = list()
    for i in range(0, int(i_split), 1):
        j = np.rot90(split1[i], 1, (0, 1))
        split_arrays.append(j)
    for k in split_arrays:
        el = np.array_split(k, i_split)
        split_arrays2.append(el)
    for m in split_arrays2:
        for n in m:
            o = np.rot90(n, 1, (1, 0))
            split_arrays3.append(o)
    return split_arrays3


# MA-14.
def reconstruct_image_sections(array_list):
    """

        Sister function to sectionalize_image_array. This function takes the tiles created from that function and puts
    them back together into a new image\array. If no changes were made to any of the "tiles", than the output of this
    function will match exactly the input of sectionalize_image_array. Note: If changes are to be made to the sections,
    which is part of this function's goal, those sections Must retain their exact number of pixels, or the
    reconstruction will fail.

    :param array_list:  List off sectionalized tile numpy arrays that are pieces of a larger whole.
    :return:            Reconstructed image_array.
    """
    join_list = list()
    array_list.reverse()
    new_join = list()
    em = 0
    en = int(math.sqrt(len(array_list)))
    while en <= len(array_list):
        # for j in range(0, int(math.sqrt(len(a
        joinez = array_list[em: en]
        # joinez.reverse()
        np_join = np.hstack(joinez)
        join_list.append(np_join)
        # for el in range(em, en):
        # tuple1 = tuple(array_list[em: en])
        em += int(math.sqrt(len(array_list)))
        en += int(math.sqrt(len(array_list)))

    join_list.reverse()
    re_image1 = np.vstack(join_list)
    # TODO Create work arounds for the oddly"shaped" images.
    #
    # if join_list[1].shape[0] != join_list[0].shape[0]:
    #     random_r = np.array([[[59047302, 12736756, 37869375]]])
    #     joinsert = np.insert(join_list[1], -1, random_r, axis=0)
    #     new_join.append(join_list[0])
    #     new_join.append(joinsert)
    #     re_image = np.vstack(new_join)
    #     final_image = musicode.mc.delete_select_points(re_image, [59047302, 12736756, 37869375])
    #     return final_image
    # else:
    return re_image1


# Picture-wise, hstack for horizontal.
# Picture-wise, vstack for vertical.

# MA-15.
# TODO Test this function.
def lists_of_to_array(lizt, dim=2):
    """
        Lists_of_to_array() is the sister function of array_to_lists_of().
    This takes coordinate lists (2D numpy arrays) or color lists of cv2.imreads (3D arrays) and turns them back into numpy
    arrays with the appropriate shape and ndim. More advanced use may use more dimensions. This is not supported yet.

    :param lizt:    A python list of array coordinates or color tuples. (typically)
    :param dim:     Number of desired dimensions. 2 by default, otherwise will probably be 3,
                    in order to return lizt to original cv2 numpy array.
    :return:        Numpy array.
    """

    # for q in lists:
    #     r = np.array(q)
    array = np.array(lizt, ndmin=dim)
    if array.ndim == 3:
        # def print_factors(x):
        # This function takes a number and prints the factors
        # print("The factors of", x, "are:")
        f_list = list()
        for i in range(1, array.shape[1] + 1):
            if array.shape[1] % i == 0:
                f_list.append(i)

        # change this value for a different result.
        # num = 320
        # uncomment the following line to take input from the user
        # num = int(input("Enter a number: "))
        # print_factors(num)
        new_array = array.reshape((statistics.median_low(f_list), statistics.median_high(f_list), 3))
        return new_array
    else:
        return array


# MA-16.
# TODO Test this function.
def array_to_lists_of(coords_array, tupl=True):
    """
        Array_to_lists_of() is the sister function of lists_of_to_array().
    It is a conversion function that turns numpy arrays into a list of coordinate lists\\tuples or color lists\\tuples.
    This functionality is contingent upon the input arrays ndim.
    Useful for compare calls between numpy data without wanting to use .any() or .all(), among other uses.

    :param coords_array:    Input 2D coordinate array or cv2.imread 3D array of color tuples. (i.e. a picture)
    :param tupl:            Determines whether or not you want the parent list with the data set as lists or tuples.
    :return:                A List of lists or list of tuples.
    """

    assert type(coords_array) == numpy.ndarray, "Your coords_array is not a numpy array."
    if coords_array.ndim == 2:
        lok = list()
        for i in coords_array:
            key = list()
            for e in i.flatten():
                key.append(e)
            if tupl:
                lok.append(tuple(key))
            else:
                lok.append(key)
        # print(*lok, sep="\n")
        return lok
    elif coords_array.ndim == 3:
        p_list = list()
        for x in range(len(coords_array)):
            for y in range(len(coords_array[x])):
                pnts = list()
                xy_pnts = coords_array[x][y]
                for i in xy_pnts.flatten():
                    pnts.append(i)
                if tupl:
                    p_list.append(tuple(pnts))
                else:
                    p_list.append(pnts)
        return p_list
    else:
        print("Suggested ndim should be 2 or 3.")
        return None


# MA-17.
def separate_pixels_to_coords_by_color(image, z_value, nn=False, dimensionalize=None, display=False, clrs=None,
                                       num_dict=False): ###, stream=False):
    """
        Created originally for testing purposes, this function takes an input image and returns an Ordered Dictionary of
    coordinate arrays separated by color value. It has the added options of displaying a mayavi mlab visualization and
    dimensionalizing it along the z axis from the starting point of z_value, a value between 0-127. Use of nearest
    neighbor functionality vastly expedites this process; see midiart.set_to_nn_colors().
    Note: this function has a builtin conversion for the color palette. It is meant to be supplied with palettes of
    colors that have (255, 255, 255) for white, instead of (1, 1, 1).

    :param image:           Input image, either filepath, or cv2.imread(filepath). If stream=True, input is treated as
                            a stream.
    :param z_value:         Z axis plane on which to place the image.
    :param nn:              If true, sets colors in image to their nearest neighbors determined by the FL studio color
                            palette or selected palette..
    :param dimensionalize:  Value denoting space along z axis between separated parts.
    :param display:         Displays a standard mayavi mlab visualization of image.
    :param clrs:            16-colors palette to use. FL studio colors used by default when None.
    :param num_dict         If True, returns a dict with INTS as keys, else COLOR STRINGS as keys.
    :return:                Returns odict, an Ordered Dictionary of coordinates organized by color, and an mlab_list,
                            a list of variables corresponding to the mlab calls made if display=True.
    """
    #Clrs check
    if clrs is None:
        clrs = FLStudioColors
    else:
        clrs = clrs
    #Type check for input image.
    if type(image) != numpy.ndarray:
        cv2.imread(image)
    #Set to nn if desired.
    if nn:
        image = set_to_nn_colors(image, clrs)
    else:
        pass
    #Create Lists
    clrs_list = list()
    mlab_list = list()
    #Get colors from image and place in clrs_list.
    for y in range(0, len(image)):
            for x in range(0, len(image[y])):
                #Colors tuples converted immediately to mayavi float colors here via dividing by 255 #TODO Is this necessary?!?!?!?
                clr = (tuple((image[y][x] / 255).flatten()))
                clrs_list.append(clr)
    #Create an ordered dict using clrs_list. The colors as keys will be kept in order, and duplicates will be discarded.
    odict1 = OrderedDict.fromkeys([i for i in clrs_list])
    #print("Length:", len(odict1))
    #Up to here is fast.

    for q in odict1.keys():
        clr_list = []   # A new clr_list for each key, one for each clr.
        #Loop for colors again.
        for y in range(0, len(image)):
            for x in range(0, len(image[y])):
                #Get the color
                clr = (tuple((image[y][x] / 255).flatten()))
                #If it compares to the key, place a tuple(x,y) for the location of that color into clr_list.
                if clr == q:
                    clr_list.append((x, 127-y))  #127- thing for inverted wx grid iterations
                    #Exit loop.
        #Turn that q clr_list into an np.array().
        odict1[q] = np.array(clr_list)
                    #arglist.append([j for j in odict1.keys()])
        #r = np.array(odict1[q])
        # color = list(q).reverse()

    for r in odict1.keys():
        #Horizontally stack the np.array() previously created with user-defined z-value
        #----[[od_x, od_y], ->hstacked with z<- ===  [[od_x, od_y, *od_z]
        #----[od_xx, od_y]] ->hstacked with z<- ===  [od_x, od_y, *od_z]]
        odict1[r] = np.hstack((odict1[r], np.full((len(odict1[r][:, 0]), 1), z_value)))
        #If display is true, use coords for mlab calls and append them to a list.
        if display:
            ##SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT
            #Color tuple used here is reversed for displaying correct colors.
            actor = mlab.points3d(odict1[r][:, 0], odict1[r][:, 1], odict1[r][:, 2], color=(r[-1], r[-2], r[-3]), mode='cube', scale_factor=1)
            mlab_list.append(actor)
        if dimensionalize is not None:
            z_value += dimensionalize
    print("Odict1", odict1)
    print("Clrs:", clrs)

    if num_dict:
        #TODO This logic needs to go INSIDE the separte_pixels_to_coords_by_color function.
        # DONE
        numdict = OrderedDict().fromkeys([num for num in clrs.keys()])

        #Conversion to Mayavi floats.
        m_clrs = convert_dict_colors(clrs, invert=False)

        #m_clrs = clrs
        for c in m_clrs.keys():
            for e in odict1.keys():
                if m_clrs[c] == e:
                    numdict[c] = odict1[e]
        # for d in num_dict.keys():
        #     if num_dict[d] is None:
        #         del (num_dict[d])

    if display is True:
        mlab.show()
        return odict1, mlab_list
    elif num_dict is True and display is False:
        return numdict
    else:
        return odict1



# MA-18
def get_color_palettes(mypath=None, ncp=False):
    """
        This function creates a dictionary of dictionaries of colors derived from Midas's color_palettes folder. One can
    specify another folder of colors if desired. The colors in the desired folder should be .jpgs or .pngs of 1x16
    pixels of different colors.

    Colors acquired from: ----> https://lospec.com/palette-list

    :param mypath:  Should generally be r".\\Midas\\resources\\color_palettes folder".
    :param ncp:     If True, create FL studio ".ncp" files from the created palettes. Folder is default specified.
    :return:        A dictionary of dictionaries of color tuples.

    Note: For ncp=True, once you have created the ncp files for use with FL Studio, you must place them in the
    appropriate FL \\Note color palettes\ folder.
    """
    if mypath is None:
        mypath = r".\resources\color_palettes\\"

    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    dict_list = {}
    for j in files:
        #print("Color_palette_file:", j)
        name = os.path.splitext(os.path.basename(j))[0]
        dict = {}
        k = cv2.imread(j)   #cv2.imread reads in colors as BGR instead of RGB. Hence all these bug comments....
        #11/30/2021--
        #https: // note.nkmk.me / en / python - opencv - bgr - rgb - cvtcolor /
        #k = cv2.cvtColor(k, cv2.COLOR_BGR2RGB) #This line is special. Does the same thing as swapping 0 and 2 below.
        for i, x in enumerate(k[0]):
            #print("Tuple_X", tuple(x))
            dict[i+1] = tuple([x[0], x[1], x[2]]) #0 and 2 here. tuple(x)  #COULD IT BE HERE?!?!?! WHERE IT ALL GETS FIIIIXED!?!?!?!?!  #SWAP HERE ------- See trello card: --> https://trello.com/c/O67MrqpT?  #TODO This was the color inversion bug that was hard to fix.
            #YES. Inverting, here at a root point, fixes the writing of the rest of my colors_dict code.
            #TODO BEWARE: Write in a case that handles the incidental inverting of your ncps.
        dict_list[name] = dict
    if ncp is True:
        convert_rgb_to_ncp(dict_list)
    else:
        pass
    return dict_list


def get_color_pngs(mypath=None, as_path=True):
    """
        This function creates a dictionary of either images read in by cv2.imread OR the fullpathtofile of those images
    as VALUES and their respective name as KEYS.
    :param mypath:          The path to the color palettes folder. If not None, must be user-specified.
    :param as_path:         If as_path, The values of the dictionary keys will be paths instead of cv2.imread(paths)
    :return:                A dictionary of color palette paths or images.
    """
    if mypath is None:
        mypath = r".\resources\color_palettes\\"

    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    dict_list = {}
    for j in files:
        name = os.path.splitext(os.path.basename(j))[0]
        if as_path is True:
            k = j
        else:
            k = cv2.imread(j)
        dict_list[name] = k
    return dict_list



def get_color_attributions(mypath=None):
    """
        This function returns a dict of color palette names as KEYS and the respective attributions text string as the
    values.
    :param mypath:      The path to the color palettes folder. If not None, must be user-specified.
    :return:            A dictionary of names\\strings as keys\\values respectively.
    """
    if mypath is None:
        mypath = r".\resources\color_palettes\\"

    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    file = open(r".\resources\ColorPaletteAttributions.txt", 'r', encoding="utf8")
    lines = file.readlines()
    file.close()
    names = [os.path.splitext(os.path.basename(j))[0] for j in files]
    attributions_dictionary = dict(zip(names, lines))
    # for j in files:
    #     name = os.path.splitext(os.path.basename(j))[0]
    return attributions_dictionary



# MA-19.
def convert_dict_colors(colors_dict, invert=False, both=False):
    """
        This function takes a dict of colors as input and divides the dict color tuple values by 255 for use in the
        mayavi view. Resulting values are floats thus:
        (0.0 <= a floating point number <= 1.0)
    :param colors_dict:     Dict of colors, usually of 16 colors.
    :param invert:          Parameter to switch the "R" value with the "B" value in the tuple, if true.
    :parama both:           If true, both convert and invert will occur.
    :return:                A deep copy of the input Dictionary.
    """
    new_dict = copy.deepcopy(colors_dict)
    if both is True:
        print("Both is True. Converting to floats AND swapping R with B.")
        for i in new_dict.keys():
            #print(colors_92[i])
            new_color = tuple([new_dict[i][2]/255, new_dict[i][1]/255, new_dict[i][0]/255])  ## Converts the color tuple to mayavi floats.
            new_dict[i] = new_color
    else:
        if invert is False:
            print("Invert is False. Converting to floats only.")
            for i in new_dict.keys():
                #print(colors_92[i])
                new_color = tuple([new_dict[i][0]/255, new_dict[i][1]/255, new_dict[i][2]/255])  ## Converts the color tuple to mayavi floats.
                new_dict[i] = new_color
        if invert is True:
            print("Invert is True. Swapping R with B only.")
            for i in new_dict.keys():
                #print(colors_92[i])
                new_color = tuple([new_dict[i][2], new_dict[i][1], new_dict[i][0]])
                new_dict[i] = new_color

    return new_dict


#TODO Make dedicated? Redundant?
def invert_dict_colors(colors_dict, inPlace=False):
    if inPlace:
        new_dict = colors_dict
    else:
        new_dict = copy.deepcopy(colors_dict)

    for i in new_dict.keys():
        #print(colors_92[i])
        new_color = tuple([new_dict[i][2], new_dict[i][1], new_dict[i][0]])  ## Inverts the color tuple.
        new_dict[i] = new_color

    return new_dict


# MA-20.
def convert_rgb_to_ncp(palettes=None):
    """
        This function takes dictionaries of rgb color tuples and converts them to the ncp 'color0 = hexadecimal' format
    used for colors inside of FL Studio. It then writes that ncp to file in a designated Midas folder.
    :param palettes:        A dictionary of 16 color tuples with keys 1-16 for each value.
    :return:
    """
    #TODO Doc string.
    if palettes is None:
        palettes = get_color_palettes()
    else:
        palettes = palettes
    for i in palettes.keys():
        new_file = open(os.getcwd() + os.sep + 'resources' + os.sep + 'color_palettes' + os.sep + 'ncp_palettes'
                        + os.sep + i + ".ncp", "w")
        text_list = []
        num = 0
        for j in palettes[i]:
            color_num = 'Color%s' % num
            string = '=FF%02x%02x%02x' % (palettes[i][j])  #Except that this works.
            upper_string = string.upper()
            final_string = color_num + upper_string + '\n'
            text_list.append(final_string)
            num += 1
            #new_file.write()
        new_file.writelines(text_list)
        new_file.close()

        #print(i)


# MA-21.
def cv2_tuple_reconversion(image, inPlace=False, conversion ='Edges'):
    """
        Function to take the cv2.Canny transformation function of opencv-python, and return the equivalent 'original'
    format np.array for the 'edges'. (same for monochrome, or whatever prior cv transformation the user performed.)
    ---(i.e. Canny, cvtColor(image, cv2.COLOR_BGR2GRAY))
    The 'original' "image" is a 3D array(technically a 2D of 3-value color tuples), while a Canny array is a 2D array of
    single values ---the result of the edge detection--- which is not the same data format as the 'original'. Hence
    this function.

    :param image:       A cv2.imread(r"filepath") image.
    :param inPlace:     Bool determining whether to operate on original image in place and return it, or to return a
                        new one.
    :param conversion   Kwarg in
    :return:            A 3D np.array (2D of color tuples, most likely will be black and white).
    """
    print("IMAGE_CHECK", image[-1, -1])
    if conversion == "Edges":
        new_image = cv2.Canny(image, 100, 200)
    elif conversion == "Monochrome":
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (thresh, new_image) = cv2.threshold(new_image, 127, 255, cv2.THRESH_BINARY)
    #elif conversion == "Some other cv2 conversion s(*t, tbd at a later date":
        #new_image = that conversion

    #image = image
    #new_array =
    if inPlace is True:
        for row in range(0, len(new_image)):
            for col in range(0, len(new_image[row])):
                if new_image[row, col] == 255:
                    image[row, col] = np.asarray([255, 255, 255], dtype=np.uint8)
                elif new_image[row, col] == 0:
                    #print("ROW, COL - Here", image[row, col])
                    image[row, col] = np.asarray([0, 0, 0], dtype=np.uint8)
        return (new_image, image) #image here had an operation INPLACE, so we return that per this code block.

    else:
        return_image = copy.deepcopy(image)
        for row in range(0, len(new_image)):
            for col in range(0, len(new_image[row])):
                if new_image[row, col] == 255:
                    return_image[row, col] = np.asarray([255, 255, 255], dtype=np.uint8)
                elif new_image[row, col] == 0:
                    #print("ROW, COL - Here", return_image[row, col])
                    return_image[row, col] = np.asarray([0, 0, 0], dtype=np.uint8)
        return (new_image, return_image) #return image is a deep copy, so we return that instead here.


#########################
#Direct MIDI functions #TODO EXPAND AND REORGANIZE THIS--include music21.midi.Midifile() functions AND mido.MidiFile() functions. (April 3rd, 2021)
#########################

# MA-22.
def create_midi_header(midifile=None, bpm=None, timesig=None, keysig=False, as_track=False):
    """
        This function creates the first track of common midifiles, establishing necessary information for the midi file
    such as tempo, time signature and key signature. It has the added option of allowing the user to manipulate said
    parameters of tempo, time signature and key signature.
    :param midifile:     If not None, path to a midifile as str  r"midifile".
    :param bpm:          If not None, desired tempo in beats per minute to set within the midifile.
    :param timesig:      If not None, desired time siganture as tuple (numerator, denominator). (ie. (4, 4) as default)
    :param keysig:       Key signature specified by the following valid values as strings:
                         A A#m Ab Abm Am B Bb Bbm Bm C C# C#m Cb Cm D D#m Db Dm E Eb Ebm Em F F# F#m Fm G G#m Gb Gm
    :param as_track:     If true, return a mido.MidiTrack() instead of a midifile.
    :return:             mido.MidiFile() or mido.MidiTrack()
    """
    mm_timesig = mido.MetaMessage(type='time_signature', numerator=4, denominator=4)  #TODO They said their default was fixed. It isn't. --> https://mido.readthedocs.io/en/latest/meta_message_types.html#time-signature-0x58
    if timesig is not None:
       assert type(timesig) is tuple, print('Time signature must provided in the form of tuple(numerator, denominator).')
    mm_timesig.numerator = timesig[0] if timesig is not None else mm_timesig.numerator
    mm_timesig.denominator = timesig[1] if timesig is not None else mm_timesig.denominator
    #Todo Look into 'smpte_offset' type in place of mm_timesig?
    mm_tempo = mido.MetaMessage(type='set_tempo')
    mm_tempo.tempo = mido.bpm2tempo(bpm) if bpm is not None else mm_tempo.tempo
    mm_eot = mido.MetaMessage(type='end_of_track')
    mm_list = [mm_tempo, mm_timesig, mm_eot]
    if keysig:
        mm_keysig = mido.MetaMessage(type='key_signature', key=keysig)
        mm_list.insert(0, mm_keysig)

    m_track = mido.MidiTrack(mm_list)

    if midifile is None:
        midifile = mido.MidiFile()
        midifile.tracks.insert(0, m_track)
    else:
        #Todo STUDY the headers of midifiles that are to go through midas and re-evaluate methods here accordingly.
        midifile = mido.MidiFile(midifile)
        midifile.tracks[0] = m_track
    if as_track:
        return m_track
    else:
        return midifile

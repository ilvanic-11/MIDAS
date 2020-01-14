# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# Name:         music21funcs.py
# Purpose:      This is the top file for extra music21 functions. These are functions
#				that operate directly on music21 Streams.
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    MIDAS is Copyright © 2017-2019 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-19 Michael Scott Cuthbert and the music21
#               Project
# License:      LGPL or BSD, see license.txt
#------------------------------------------------------------------------------------


###############################################################################
# TABLE OF CONTENTS
#
#TRANSPOSE_FUNCTIONS
#-----------------------------
#Tr-1.  def TRANSPOSE_MEASURE(in_stream, measure_number, degree)
#Tr-2.  def TRANSPOSE_ALL_MEASURES_BY_RANDOM(in_stream)
#Tr-3.  def TRANSPOSE_MEASURES_BY_LETTERS(in_stream, letters, degree)
#Tr-4.  def TRANSPOSE_NOTES_BY_RANDOM(in_stream, measure_range_low, measure_range_high, interval_lower_limit, interval_upper_limit)
#Tr-5.  def TRANSPOSE_CHORD_IN_KEY(in_chord, int_num, key)
#Tr- TODO
#
##MODIFICATION_FUNCTIONS
#--------------------------------
#M-1.   def ALTER_MEASURE_OFFSET(in_stream, range_l, range_h, offset_number)
#M-2.   def ALTER_MEASURE_DURATION(in_stream, in_stream, range_l, range_h, duration_len)
#M-3.   def STRETCH_BY_MEASURE(in_stream, range_l, range_h, ratio)
#M-4.   def ARPEGGIATE_CHORDS_IN_STREAM(in_stream, arp_factor)
#TODO: M-5. REPLACE_CHORDS()
#M-6. CHOP_UP_NOTES(stream, offset_interval)
#TODO: M-7 MAKE_CONTIGUOUS_NOTES()
#
##SYNTHESIS_FUNCTIONS
#-----------------------------
#Syn-1. def SET_CHORD_OCTAVE(in_chord, octave)
#Syn-2. def MAKE_CHORD_FROM_NOTE(in_stream, in_chord, inv)
#Syn-3. def MAKE_CHORD_FROM_NOTE_2(in_stream, in_chord, inv)
#Syn-4. def MAKE_NOTES_FROM_STRING_OF_NUMBERS(in_string, keychoice=None, note_length = 1)
#Syn-5. def FIBONACCI_TO_MUSIC(range_l, range_h, scale_mode, base, note_length = 1, spaces=False)
#Syn-   def fibonacci_range_mm(l, h)
#Syn-   def base10toN(num, base)

#MUSIC21_FUNCTIONS\CLASSES
#-------------------------------------
#M21-1. def DELETE_REDUNDANT_NOTES( in_stream, force_sort=False)
#M21-2. def NOTAFY(in_stream)
#M21-3. def SEPARATE_NOTES_TO_PARTS_BY_VELOCITY( in_stream)
#M21-4. def SET_STREAM_VELOCITIES( in_stream, vel)
#M21-5. def CHANGE_VELOCITIES_BY_RANGELIST(in_stream, volume_list)
#M21-. TODO: music21.clash.Clash() A music21 object for housing multiple notes of same pitch and offset with different velocities.
# 		Similar to music21.chord.Chord. (redundant, might use stream.Parts instead for simplicity)
#M21-.6 TODO:  MUSIC21.CONVERTER.PARSE(notafy=True)
#M21-.7 def CHANGE_VELOCITES_BY_DURATION(in_stream, dur_choice=None, vel_choice=None)
#M21-.8 def MAKE_MUSICODE(in_stream, musicode_name, shorthand, full_path=None)
#M21-.9 def CHANGE_MIDI_CHANNELS_TO_ONE_CHANNEL(midi_file, channel=1)
#M21-.10 def SPLIT_MIDI_CHANNELS(midi_file, file_path, name, to_file=False)
#M21-.11 def PRINT_CHORDS_IN_PIECE(in_stream)
##GUI_FUNCTIONS (Generally Private)
#----------------------------------
#GUI-1. def STREAM_TO_MATRIX( stream)
#GUI-2. def MATRIX_TO_STREAM( matrix, connect, cell_note_size)
###############################################################################

import os
import music21
import copy
import random
import numpy as np
import math
import fractions
from collections import OrderedDict

##TRANSPOSE_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#Tr-1.
def transpose_measure( in_stream, measure_number, degree):
    """
    Use mList = [i for i in in_stream.getElementsByClass(stream.Measure) for indexing reference.
    This function transposes a selected measure by a selected generic degree. (i.e 2 will transpose everything up to it's 2nd.)
    Octave is irrelevant in this function. Was mainly created for practice.
    :param stream: stream to loop through
    :param measureNumber: Number of the measure to transpose
    :param degree: Integer degree (or interval) to transpose to. (i.e. (CEG) with a degree of 3 will transpose to (EGB))
    :return: Occurs in place. Returns nothing.
    """
    new_stream = music21.stream.Stream()
    measures = in_stream.getElementsByClass(music21.stream.Measure)
    for n in measures[measure_number].flat.notes:

        i = music21.interval.GenericInterval(degree)
        n.show('txt')

        if n.isChord:
            for p in n.pitches:
                p.transpose(i, inPlace=True)
        else:
            n.pitch.transpose(i, inPlace=True)
    # 	new_stream.insert(n.offset, copy.deepcopy(n))
    # return new_stream

#Tr-2.
def transpose_all_measures_by_random( in_stream):
    """
    Transposes all Measures in the music21 stream by a random interval 1-7
    Currently only transposes up in pitch.
    :params stream:  the music21 stream to perform transposing in
    :return:
    """
    s=copy.deepcopy(in_stream)
    for m in s.getElementsByClass(music21.stream.Measure):
        r = random.randint(1, 7)
        #logger.debug("Random: %d", r)
        for n in m.flat.notes:
            i = music21.interval.GenericInterval(r)
            #n.show('txt')
            if n.isChord:
                for p in n.pitches:
                    p.transpose(i, inPlace=True)
            else:
                n.pitch.transpose(i, inPlace=True)
    return s

#Tr-3.
def transpose_measures_by_letters( in_stream, letters, degree):
    """
    This transposes measures by a user-defined selection of "letters" (i.e. ("i", "L", "O", "p", "e", "t" "1", "0")
    where the letters themselves ARE the musicode measure to be transposed. (musicode letter translations are by default one measure in length.)
    :param in_stream: Translated musicode through which to loop.
    :param letter: All instances of single letter/letters/lists of letters to be transposed. 0 does not equal root C.
    :param degree: Degree of transposition.
    :return:
    """
    measures = in_stream.getElementsByClass(music21.stream.Measure)
    for m in measures:
        l = m.getElementsByClass(music21.ElementWrapper)
        if len(l._elements):
            if (l._elements[0].obj.split(":")[1].strip() in letters):
                for n in m.flat.notes:
                    i = music21.interval.GenericInterval(degree)
                    if n.isChord:
                        for p in n.pitches:
                            p.transpose(i, inPlace=True)
                    else:
                        n.pitch.transpose(i, inPlace=True)

#Tr-4.
def transpose_notes_by_random( in_stream, measure_range_low, measure_range_high, interval_lower_limit, interval_upper_limit):
    """
    Transposes all Measures in the music21 stream by a random interval 1-7.
    Currently only transposes up in pitch. #TODO Expand.
    :params stream:  the music21 stream to perform transposing in
    :measure_num: the number of the measure in the stream where transposing will be done
    :interval_lower_limit:  lower limit of how far the random transpose can go
    :interval_upper_limit:  upper limit of how far the random transpose can go
    :return:
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        if (m.number >= measure_range_low and m.number <= measure_range_high):
            for n in m.flat.notes:
                r = random.randint(interval_lower_limit, interval_upper_limit)
                #logger.info("Random: %d", r)
                if (r != 0):
                    i = music21.interval.GenericInterval(r)
                    # n.show('txt')
                    if n.isChord:
                        for p in n.pitches:
                            p.transpose(i, inPlace=True)

                    else:
                        n.pitch.transpose(i, inPlace=True)

#Tr-5.
def transpose_chord_in_key(in_chord, int_num, key):
    """
    This function takes a chord and a key and transposes the chord according to the key.
    :param in_chord: User-introduced chord.
    :param intv_num: Generic interval(i.e 3=third, 7=seventh, etc.)
    :param key: Key to be specified.
    :param octave: Octave to be specified by an Int.
    :return: Returns ch = music21.chord.Chord(modified in_chord)
    """
    i = music21.interval.GenericInterval(int_num)
    ch = music21.chord.Chord()
    k = key.Key(key)
    for p in in_chord.pitches:
        i.transposePitchKeyAware(p, k, inPlace=True)
        ch.add(p, runSort=True)
        ch.sortDiatonicAscending(inPlace=True)
    return in_chord

##MODIFICATION_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#M-1.
def alter_measure_offset( in_stream, range_l, range_h, offset_number):
    """
    Alters all music21 object offsets in selected measure or range of measures.
    Calls makeMeasures(,inPlace=True) before finalizing.
    :param in_stream: Translated Musicode.
    :param range_l: Starting measure number to edit.
    :param range_h: Ending measure number up to which to edit.
    :param offset_number: Offset in quarter notes. (1 = One quarternote, Negative numbers and fractions are allowed.)
    :return: Stream
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        if (m.number >= range_l and m.number <= range_h):
            for n in m.flat.notes:
                m.setElementOffset(n, n.offset + offset_number)
    in_stream.makeMeasures()
    return in_stream

#M-2.
def alter_measure_duration( in_stream, range_l, range_h, duration_len):
    """
    Alters all object durations in selected measures or range of measures.
    :param in_stream: Translated Musicode.
    :param range_l: Starting measure number to edit.
    :param range_h: Ending measure number up to which to edit.
    :param duration_len: Duration in quarterlength. (1 = one quarter note. Can do many division smaller than a quarter note. Negative numbers are allowed.)
    :return: Stream
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        if (m.number >= range_l and m.number <= range_h):
            for n in m.flat.notes:
                d = music21.duration.Duration(duration_len)
                n.duration = d
    in_stream.makeMeasures()
    return in_stream

#M-3. TODO NEEDS FIXING!!
def stretch_by_measure( in_stream, range_l, range_h, ratio, stretchDurations=True):
    """

    :param in_stream:
    :param range_l:
    :param range_h:
    :param ratio:
    :return:
    """
    print("Ratio=")
    print(ratio)
    if in_stream.getElementsByClass(music21.stream.Measure) is None:
        print("In function 'stretch_by_measure', in_stream has no measures. Cannot stretch.")
        return None
    temp = music21.stream.Stream()
    m_num = 0
    l = list()
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        if (m.number >= range_l and m.number <= range_h):
            for n in m.flat.notes:
                l.append(m)
                temp.insert(n.offset + (m_num * 4), n)
            m_num = m_num + 1

    print("in_stream")
    in_stream.show('txt')

    in_stream.remove(l)
    print("after removing")
    in_stream.show('txt')

    print("Temp")
    temp.show('txt')

    for n in temp.flat.notes:
        print(n.offset)
        temp.setElementOffset(n, n.offset * ratio)
        if (stretchDurations):
            d = music21.duration.Duration(n.duration.quarterLength * ratio)
            n.duration = d

    in_stream.insert(range_l*4, temp)
    print("in_stream before MakeMeasures")
    in_stream.show('txt')
    in_stream.makeMeasures(inPlace=True)

    print("in_stream after MakeMeasures")
    in_stream.show('txt')

    return in_stream

#M-4.
def arpeggiate_chords_in_stream( in_stream, stepsize=1, ascending=True):
    """
    This iterates for the stream.chord.Chord objects and turns them into arpeggiated
    instances of the chord with the same notes, but different offsets.
    :param in_stream: In-stream.
    :param stepsize: Stepsise factor of arpeggiation of notes in found chords.
    :return: in_stream
    """
    s = notafy(in_stream).flat
    newstream= music21.stream.Stream()
    map = s.offsetMap()
    offsets = set([o.offset for o in map])
    print(offsets)
    for j in offsets:
        notes = sorted(s.getElementsByOffset(j), key=lambda x:x.pitch.midi, reverse=(not ascending))
        print("offset=%d" % j)
        print(notes)
        step = 0
        for a in notes:
            newstream.insert(a.offset + stepsize * step, a)
            step += 1 # step = step +1
    return newstream

#M-5.  TODO.
# def replace_chords_selection()
# #def replace_chord( in_stream, selected_chord, replacement_chord, inversion):
# def replace_musicode()
#     """
#
#     :param in_stream: Stream over which to be iterated for chords.
#     :param selected_chord: Iteration of one type of chord.
#     :param replacement_chord: Chord type with which to replace selection of chord type.
#     :param inversion: Inversion of replacement chords. (1-3 for triads, 1-4 for 7ths, etc.)

#     :return:
#     """

#M-6.
def chop_up_notes(in_stream, offset_interval):
    """
    This function takes an in_stream and evenly dices all of the notes in it. The offset interval determines the size of this dicing.
    :param in_stream: Operand music21.stream object.
    :param offset_interval: Size of chopped up notes.
    :return: New music21.stream object. (part, score, stream, voice etc.)
    """
    new_stream = music21.stream.Stream()
    for n in in_stream.flat.notes:
        # n.show('txt')
        # print("n.duration.quarterLength %f" % n.duration.quarterLength)
        # print ("offset_interval", offset_interval)
        if n.duration.quarterLength > offset_interval:
            o = n.offset
            print(" N offset = %f" % n.offset)
            while (o < n.duration.quarterLength + n.offset):
                print(" o = ", o)
                new = copy.deepcopy(n)
                new.offset = o + offset_interval
                new.duration.quarterLength = offset_interval
                o = o + offset_interval
                new_stream.insert(new.offset, new)

        else:

            new_stream.insert(n.offset, n)
    return new_stream

# M-7.
def merge_contiguous_notes(in_stream ):
    """This function takes a stream of noticeably "chopped up notes" (see sister function) and reconnects or "glues"
    those notes (back) together in a contiguous manner.
    :param in_stream: input stream
    :param max_note_size: maximum note size to make when combining contiguous notes in quarterlength
    :return: new stream
    """
    import numpy as np
    new_stream = music21.stream.Stream()
    s = notafy(in_stream)
    m = np.array(stream_to_matrix(s))
    print(m)
    new = matrix_to_stream(m, connect=True)
    return new



##SYNTHESIS_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#Syn-1.
def set_chord_octave(in_chord, octave):
    """
    Sets the octaves of chords. Some music21 chords don't have octaves, so a simple call helps sometimes.
    :param in_chord: Chord object with pitches.
    :param octave: Octave of pitches in chord.
    :return: in_chord
    "NOTE: Only works well for triads and sevenths, chord bigger than one octave will not need this."
    """
    for p in in_chord.pitches:
        p._setOctave(octave)
    return in_chord


#Syn-2.
def make_chords_from_notes(in_stream, in_chord, inv):
    """
    For singular notes in a music21 stream, this function takes those notes and turns them into chords with that note
    forming the 'root' of the new chord.
    :param in_stream: Stream with notes for changing.
    :param in_chord: Chord called to replace note.
    :param inv: Chord's inversion, if any.
    :return:
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        for n in m.flat.notes:
            if type(n) is music21.note.Note:
                if n.pitch.name in (in_chord.findRoot().name):
                    o = n.pitch.octave
                    new = copy.deepcopy(in_chord)
                    for p in new.pitches:
                        p.octave = p.implicitOctave - 4 + o
                    new.duration = n.duration
                    new.quarterLength = n.quarterLength
                    new.inversion(inv)
                    print(new)
                    m.insertIntoNoteOrChord(n.offset, new, chordsOnly=True)
    in_stream.makeMeasures()
    for c in in_stream.flat.notes:
        if type(c) is music21.chord.Chord:
            c.removeRedundantPitches()
    return in_stream

#Syn-3.
def make_chords_from_notes_2(in_stream, in_chord, inv):
    """
    Same as make_chords_from_notes, albeit written slightly different.
    :param in_stream: Stream with notes for changing.
    :param in_chord: Chord called to replace note.
    :param inv: Chord's inversion, if any.
    :return:
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        for n in m.flat.notes:
            if type(n) is music21.note.Note:
                if n.pitch.name in (in_chord.findRoot().name):
                    o = n.pitch.octave
                    new = copy.deepcopy(in_chord)
                    for p in new.pitches:
                        p.octave = p.implicitOctave - 4 + o
                    new.duration = n.duration
                    new.quarterLength = n.quarterLength
                    new.inversion(inv)
                    print(new)
                    x = n.offset
                    m.remove(n)
                    m.insert(x, new)
    in_stream.makeMeasures()
    return in_stream


#Syn-4.
def make_notes_from_string_of_numbers(in_string, keychoice=None, note_length = 1):
    if keychoice == "":
        keychoice = None
        keysig = None
    else:
        keysig = music21.key.Key(keychoice)
    allowedPitches = list()
    print("Key is: ")
    print(keysig)
    if keychoice == None:
        allowedPitches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    elif (type(keysig) is music21.key.Key):
        for p in music21.scale.Scale.extractPitchList(keysig.getScale()):
            allowedPitches.append(p.pitchClass)
    allowedPitches[-1] = 12
    print(allowedPitches)

    out_stream = music21.stream.Stream()
    for k in in_string:
        if k.isnumeric():
            k = int(k)
            if k >= len(allowedPitches):
                k = k % len(allowedPitches)
            n = music21.note.Note()
            n.pitch.ps = allowedPitches[int(k)]
            n.duration.quarterLength = note_length
            out_stream.append(n)
        elif k == " ":
            r = music21.note.Rest()
            r.duration.quarterLength = note_length
            out_stream.append(r)
    return out_stream

#Syn-5.
def fibonacci_to_music(range_l, range_h, scale_mode, base, note_length = 1, spaces=False):   ### ###chords=True
    """
    :param range_l: Starting low range value for fibonacci function.
    :param range_h Ending high range value for fibonacci function.
    :param scale_mode: Cm for C minor scale E for E major scale, None for Chromatic, this sets the scale mode of pitches to which to assign acquired numbers from this function.
    :param base: The mathematical base of the numbers acquired; after acquisition, they will be concatenated, varying the number of notes created and the range of pitches allowed.
    :param note_length: The rhythmic density of the notes created, specified by music21's quarterLength property.
    :param spaces: If true, space are place between each fibonacci number.
    :return:
    """

    fibonacci_array = fibonacci_range_mm(range_l, range_h)
    new_fib_array = [base10toN(int(j), base) for j in fibonacci_array]
    if spaces:
        new_fibonacci = " ".join(new_fib_array)
    else:
        new_fibonacci = "".join(new_fib_array)
    print("new_fibonacci", new_fibonacci)
    fibonacci_stream = make_notes_from_string_of_numbers(new_fibonacci, keychoice=scale_mode, note_length=note_length)
    return fibonacci_stream

#Syn-6.
def array_to_music(list_array, scale_mode, base, note_length = 1, spaces=False):    ###chords=True
    """
    Same as fibonacci_to_array, only this function allows a user-specified or random input of numbers
    :param list_array: Numpy 1D array of numbers, can be int or float.
    :param scale_mode: Cm for C minor scale E for E major scale, None for Chromatic, this sets the scale mode of pitches to which to assign acquired numbers from this function.
    :param base: The mathematical base of the numbers acquired; after acquisition, they will be concatenated, varying the number of notes created and the range of pitches allowed.
    :param note_length: The rhythmic density of the notes created, specified by music21's quarterLength property.
    :return:
    """

    array = np.array(list_array)
    print("array", array)
    #new_array2 = [base10toN(int(j), base) for j in array]
    new_list = []
    for j in array:
        if j != " ":
            new_list.append(base10toN(int(j), base))
    new_array = np.array(new_list)
    print("new_array", new_array)
    #TODO Spaces shit.
    if spaces:
        fin_list = " ".join(new_array)
    else:
        fin_list = "".join(new_array)
    print("fin_list", fin_list)
    out_stream = make_notes_from_string_of_numbers(fin_list, keychoice=scale_mode, note_length=note_length)
    return out_stream

#Syn-

def base10toN(num, base):
    """Change ``num'' to given base
    Upto base 36 is supported."""
    converted_string, modstring = "", ""
    currentnum = num
    if not 1 < base < 37:
        raise ValueError("base must be between 2 and 36")
    if not num:
        return '0'
    while currentnum:
        mod = currentnum % base
        currentnum = currentnum // base
        converted_string = chr(48 + mod + 7 * (mod >= 10)) + converted_string
    return converted_string

#Syn-
def fibonacci_range_mm(l, h):
    n = np.arange(l, h)
    sqrt5 = np.sqrt(5)
    phi = (1 + sqrt5)/2
    #fibonacci = np.array((phi**n - (-1/phi)**n)/sqrt5, dtype=np.int64)
    fibonacci = np.rint((phi**n - (-1/phi)**n)/sqrt5)
    print("Fibonacci", fibonacci)
    return fibonacci

        # if len(fibonacci) > 91:
        #     return fibonacci2
        # else:
        #     return fibonacci
 # def Fibonacci(n):
    #     if n < 0:
    #         print("Incorrect input")
    #         # First Fibonacci number is 0
    #     elif n == 1:
    #         return 0
    #     # Second Fibonacci number is 1
    #     elif n == 2:
    #         return 1
    #     else:
    #         return Fibonacci(n - 1) + Fibonacci(n - 2)
##MUSIC21_FUNCTIONS\CLASSES (NEW, for later)
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#M21-1.
#TODO Needs fixing.
def delete_redundant_notes( in_stream, greatest_dur=False):
    """
    This function takes all the notes of a music21 stream and deletes redundant notes of the same pitch at the
    same offset while allowing the user to chose which duplicate note to keep based on duration.quarterLength.
    The method here uses in_stream.getElementsByOffset, python's min() and max() functions, the "set" feature of an ordered dict,
    and some nested setting and getting that loops over music21 streams.
    :param in_stream: Stream with notes.
    :param greatest_dur: Boolean determing whether to choose the duplicate note(s) with longest duration or the shortest.
    :return: new_stream. Returns a new music21 stream with just notes.
    """


    #notes_list is a list of lists of notes found at the offets of our iteration.

    #First, we eliminate chord objects notafy(), a function that basically flattens chords(all chord objects become respective note objects).
    #This way, we are working with just notes in a stream.

    # A stream with just note objects, no chord objects.
    notafied_stream = notafy(in_stream.flat.notes) ##TODO Do I need flat.notes here?

    # dicts_list is a list of Ordered Dictionaries (from collections import Ordered Dict) of pitches(keys) and notes(values)
    # created for every offsets found in our iteration.
    dict_list = list()

    #Our list of offsets. List(set([list])) eliminates duplicate offsets.
    offsets = list(set([i[1] for i in notafied_stream.offsetMap()]))

    for l in offsets:
        pitches_list = list()
        notes_list = list()
        matched_list = list()
        ord_dict = OrderedDict()
        for i in notafied_stream.getElementsByOffset(l):
            if type(i) is music21.note.Note:
                pitches_list.append(i.pitch.ps)
                notes_list.append(i)
            matched_list.append([k for k in notes_list if k.pitch.ps == i.pitch.ps])
        for j in zip(pitches_list, matched_list):
            ord_dict.update([j])  	#Pitches become the keys of the OrderedDict, and notes with matching pitches become the values of those keys for every offset "l".
        dict_list.append(ord_dict)

    # NOW REBUILD STREAM!!!
    new_stream = music21.stream.Stream()
    for x in range(0, len(offsets), 1):
        for y in dict_list[x].values():
            for z in y:			##The DURATION call happens here.
                if greatest_dur is True:
                    dur = max([z.quarterLength for z in y])
                    if z.quarterLength == dur:
                        new_stream.insert(offsets[x], copy.deepcopy(z))
                elif greatest_dur is False:
                    dur = min([z.quarterLength for z in y])
                    if z.quarterLength == dur:
                        new_stream.insert(offsets[x], copy.deepcopy(z))
    return new_stream


    #del (new_stream)
    #greatest_dur = False

    # elements_list.append(set_list)

    #For those sets, make them ordered dicts for later to pair with notes as values.
    # for m in elements_list:
    # 	ord_dict = OrderedDict.fromkeys(n for n in m)
    # 	list_of_dicts.append(ord_dict)
    #
    # for r in offsets:
    # 	note_list = list()
    # 	for t in list_of_dicts:
    # 		for o in notafied_stream.flat.getElementsByOffset(r):
    # 			note_list.append(o)
    #
    #
    # 	for y in ord_dict.keys():
    # 		if o.pitch.ps == y:
    # 			ord_dict[y] = o

#M21-2.
def notafy( in_stream):
    """
    Returns a copy of the in_stream but with all 'chord' objects replaced with
    separate 'note' objects for each note in the chord. Basically, it is a chord.flatten() function.
    :param in_stream: Operand stream.
    :return: new_stream
    """
    new_stream = music21.stream.Stream()
    for i in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        notelist = list()
        if type(i) is music21.chord.Chord:
            for p in i.pitches:
                newnote = music21.note.Note(p)
                newnote.offset = i.offset
                newnote.duration = i.duration
                if i.volume.velocity:
                    newnote.volume.velocity = i.volume.velocity
                else:
                    print("No velocity info for chord. ")
                notelist.append(newnote)
            for x in notelist:
                new_stream.insert(i.offset, copy.deepcopy(x))
        elif type(i) is music21.note.Note:
            new_stream.insert(i.offset, copy.deepcopy(i))

    return new_stream

#M21-3.
def separate_notes_to_parts_by_velocity( in_stream):
    """
    This function is required for extract_XYZ_coordinates_to_stream. It separates all the notes of a stream into parts
    with "part.partsName"s set equal to all the possible velocities of in_stream. This allows for the separation of those
    notes with those velocities into those specified parts within the stream.
    :param in_stream: Stream to be modified.
    :return: Stream with parts.
    """
    part_stream = music21.stream.Stream()
    velocity_list = list()
    end_stream = music21.stream.Stream()
    #Create a set of non-duplicate velocities.
    for h in in_stream.flat.notes:
        velocity_list.append(h.volume.velocity)
    velocity_set = sorted(set(velocity_list))
    #print("vel_set", velocity_set)
    #print("At this point?")
    #Create a stream with parts equal to the number of non duplicate velocities.
    #Assign the names of those Parts as equal to the values of the set velocities; they are ints.
    # for x1 in range(0, len(velocity_set)):
    for k in velocity_set:
        parts1 = music21.stream.Part()
        parts1.partsName = k
        part_stream.insert(0.0, copy.deepcopy(parts1))
    #print("Parts_Stream", part_stream)
    #part_stream.show('txt')
    #Insert notes of same velocity value into stream.Part of the same value name.
    for s in part_stream.getElementsByClass(music21.stream.Part):
        for q in in_stream.flat.notes:
            if q.volume.velocity == s.partsName:
                #print("ShowParts", s)
                s.insert(q.offset, copy.deepcopy(q))
                #print("PartswithNotes", s)
            else:
                #print("And this one?")
                pass
        #print("Did we reach this?")
        end_stream.insert(s.offset, copy.deepcopy(s))
    return end_stream

#M21-4.
def set_stream_velocities( in_stream, vel):
    """
    Simple call for setting the velocites in a stream. Here for reference.
    :param in_stream: Operand stream.
    :param vel: Value to which to set stream note velocites.
    :return: In_stream. Operates in place.
    """
    for i in in_stream.flat.notes:
        i.volume.velocity = vel
    return in_stream

#M21-5. #TODO Needs revision. What purpose does this serve? Must len(volume_list) be == len([o for o in in_stream.flat.notes])?
def change_velocities_by_rangelist(in_stream, volume_list):
    # volume_list = list()
    # for i in range(vel_l, vel_h, vel_s):
    #     volume_list.append(i)
    # print('vol_list', volume_list)
    """
    Changes the
    :param in_stream:
    :param volume_list: Use range(0, desired velocity limited)
    :return:
    """
    v = 0
    for o in in_stream.flat.notes:
        o.volume.velocity = volume_list[v]
        print(o.volume.velocity)
        v += 1
        if len(in_stream.flat.notes) > len(volume_list):
            v = 0
    return in_stream

#M21-6.
def change_velocities_by_duration(in_stream, dur_choice=None, vel_choice=None):
    #Create a set of duration choices.
    duration_list = list()
    vel_list = list()
    new_vel_list = list()
    for i in in_stream.flat.notes:
        duration_list.append(i.duration.quarterLength)
        vel_list.append(i.volume.velocity)
    duration_set = set(duration_list)
    print("Duration Choices are:", duration_set)
    print("Velocities were: ", vel_list)
    for x in in_stream.flat.notes:
        if x.duration.quarterLength == dur_choice:
            x.volume.velocity = vel_choice
        new_vel_list.append(x.volume.velocity)
    print("Velocities are now: ", new_vel_list)
    return in_stream

#M21-7.
def make_musicode(in_stream, musicode_name, shorthand, full_path=None):
    #Latin_Script = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz          ?,;':-.!\"()[]/   0123456789"

    ##This block executes to save to local "midas/resources/musicode_libraries/" folder.
    set_path = r"musicode_libraries\\"       #TODO Should resources be named something else? Regardless, this relative path is set.
    if full_path is None:
        full_path = set_path
        absFilePath = os.path.dirname(os.path.abspath(set_path))
        resource_path = absFilePath + "\\resources\\" + full_path
        os.mkdir(resource_path + musicode_name + "\\\\")    #TODO What should we do if directory already exists?
        full_new_musicode_path = resource_path + musicode_name + "\\\\"
        #print(resource_path + musicode_name + "\\")
        #print(full_new_musicode_path)
    else:   ##This block executes to save to specified fullpath.
        full_new_musicode_path = full_path
    if os.path.exists(full_new_musicode_path) == False:
        os.mkdir(full_new_musicode_path)
    if in_stream.hasMeasures is False:
        in_stream.makeMeasures()
    assert in_stream.hasMeasures(), "There are no measures in this stream. Call 'in_stream.makeMeasures().'"
    assert in_stream[0].isMeasure, "This first index is not a music21.stream.Measure() object."
    for j in in_stream:   #j will be an iteration of measures, since we just established them.
        print(j)
        j.write("mid",  full_new_musicode_path + "musicode" + "_" + shorthand + "_" + str(j.measureNumber) + ".mid")

#M21-8.
def change_midi_channels_to_one_channel(midi_file, channel=1):

    a_file = music21.midi.MidiFile()
    a_file.open(midi_file, attrib="rb")
    a_file.read()
    for j in a_file.tracks:
        j.setChannel(channel)
    a_file.close()
    a_file.open(midi_file, attrib="wb")
    a_file.write()
    a_file.close()


#M21-9.
def split_midi_channels(midi_file, file_path, name, to_file=False):

    ##Read Midi File
    a_file = music21.midi.MidiFile()
    a_file.open(midi_file, attrib="rb")
    a_file.read()

    ##Access and separate tracks and name stream.Parts accordingly.
    a_stream = music21.midi.translate.midiTracksToStreams(a_file.tracks)
    #note_tracks = [m for m in a_file.tracks if m.hasNotes()]
    note_tracks_channels = []
    for m in a_file.tracks:
        if m.hasNotes():
            if len(m.getChannels()) > 1:
                note_tracks_channels.append(m.getChannels()[1])
            else:
                note_tracks_channels.append(m.getChannels())
    print("NTCs", note_tracks_channels)
    index_list = []
    for indexes in a_file.tracks:
        if indexes.hasNotes():
            index_list.append(indexes)
    print("IndexList", index_list)
    print("Note_track Length:", len(note_tracks_channels))

    for s in a_stream:
        print("Firstfirst partname", s.partName)


    # for t in note_tracks:
    #     print("Notetrack Channel:", t.getChannels())

    # for h in note_tracks_channels:
    #     for i in a_stream:
    #         i.partName = h

    for z in range(0, len(index_list)):
        a_stream[z].partName = note_tracks_channels[z]

    #a_file.close()
    #a_stream.show('txt')
    for p in a_stream:
        print("Changed partname:", p.partName)
    if to_file:
        for v in a_stream:
            final_midis = music21.midi.MidiFile()
            print("Changed partname:", v.partName)
            v.write("mid", file_path + "\\" + name + "_" + "%s" % v.partName + ".mid")
            final_midis.open(file_path + "\\" + name + "_" + "%s" % v.partName + ".mid", attrib='rb')
            final_midis.read()
            final_midis.tracks[0].setChannel(v.partName)
            final_midis.close()
            final_midis.open(file_path + "\\" + name + "_" + "%s" % v.partName + ".mid", attrib='wb')
            final_midis.write()
    else:
        return a_stream

# M21-1.
def print_chords_in_piece(in_stream):
	"""Use .flat and .makeMeasures to acquire appropriate callable stream
	:param in_stream:
	:return:
	"""
	ret_str = ""
	s = in_stream.chordify().flat.makeMeasures()
	ret_str += "[offset] [dur]   [pitches] : [common name]\n"
	for m in s.getElementsByClass(music21.stream.Measure):
		ret_str += "Measure " + repr(m.number) + "\n"
		for c in m.getElementsByClass("Chord"):
			if isinstance(c.offset, fractions.Fraction) or isinstance(c.duration.quarterLength, fractions.Fraction):
				ret_str += "  " + repr(float(format(float(c.offset), ".3f"))).ljust(6) + " " + repr(
					float(format(float(c.duration.quarterLength), ".3f"))).ljust(6) + " " + "["
			else:
				ret_str += "  " + repr(c.offset).ljust(6) + " " + repr(c.duration.quarterLength).ljust(
					6) + " " + "["
			for p in c.pitches:
				ret_str += repr(p.nameWithOctave)
			ret_str += "] : " + c.pitchedCommonName + "\n"

	#print(ret_str)
	return ret_str
# a_headers = [n for n in a_file.tracks if not n.hasNotes()]   ## Unnecessary because of midi.MidiFile()

def print_show_streamtxt(in_stream):
    filename = "Temp_Stream_Print.txt"
    set_path = r"intermediary_path"
    absFilePath = os.path.dirname(os.path.abspath(set_path))
    resourcePath = absFilePath + "\\resources\\" + set_path
    masterPath = resourcePath + "\\" + filename
    in_stream.write('txt', masterPath)
    file_read = open(masterPath, "r+")
    ret_str = str(file_read.read())
    in_stream.show('txt')
    return ret_str

def print_midi_data(in_stream):
    filename = "Temp_Midi.mid"
    set_path = r"intermediary_path"
    absFilePath = os.path.dirname(os.path.abspath(set_path))
    resourcePath = absFilePath + "\\resources\\" + set_path
    masterPath = resourcePath + "\\" + filename
    in_stream.write('mid', masterPath)
    midiFile = music21.midi.MidiFile()
    midiFile.open(masterPath, attrib='rb')
    midiFile.read()
    midistring = str(midiFile)
    midiFile.close()
    return midistring

#M21-. TODO
#def music21.clash.Clash? Khord? Vhord? Music21 object for housing multiple notes with different velocities at the same offset.


#GUI_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#GUI-1.
def stream_to_matrix(in_stream, cells_per_qrtrnote=4):
    """
    Converts a music21 stream into a 2D numpy array of shape (x, 128) where x is the highestTime of the stream.

    The piano roll grid indexes beginning at the top left, e.g.:
    [ (0,0) (1,0) (2,0) (3,0) ... ]
    | (0,1) (1,1) (2,1) (3,1) ... |
    | (0,2) (1,2) (2,2) (3,2) ... |
    | (0,3) (1,3) (2,3) (3,3) ... |

    but midi pitches begin at 0 for the low C0 note and go up the piano roll.
    So the y index of the matrix will be subtracted from 128.

    :param in_stream: 			music21.Stream object
    :param cell_note_size:  note duration that each cell/pixel represents
    :return: 				np.array
    """

    #helper function
    def _matrix_set_notes(matrix, y, x_start, x_end):
        for x in range(x_start, x_end):
            #print("y={}, s={}, e={}".format(y, x_start, x_end))
            matrix[x][128 - y] = 1


    matrix = np.zeros((math.ceil(in_stream.highestTime) * cells_per_qrtrnote, 128), dtype=np.int)

    for n in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        if type(n) is music21.chord.Chord:
            for p in n.pitches:
                x_start = int(cells_per_qrtrnote * n.offset)
                x_end = x_start + int(cells_per_qrtrnote * n.duration.quarterLength)
                _matrix_set_notes(matrix, p.midi, x_start, x_end)
        elif type(n) is music21.note.Note:
            x_start = int(cells_per_qrtrnote * n.offset)
            x_end = x_start + int(cells_per_qrtrnote * n.duration.quarterLength)
            _matrix_set_notes(matrix, n.pitch.midi, x_start, x_end)
    #print(matrix)
    return matrix

#GUI-2.
def matrix_to_stream(matrix, connect=True, cells_per_qrtrnote=4):
    """
    Converts an npArray of shape (x,128) into a music21 stream.
    x-axis is note offsets and durations
    y index is midi pitches

    The piano roll grid indexes beginning at the top left, e.g.:
    [ (0,0) (1,0) (2,0) (3,0) ... ]
    | (0,1) (1,1) (2,1) (3,1) ... |
    | (0,2) (1,2) (2,2) (3,2) ... |
    | (0,3) (1,3) (2,3) (3,3) ... |

    but midi pitches begin at 0 for the low C0 note and go up the piano roll.
    So the y index of the matrix will be subtracted from 128.

    :param matrix: 	npArray of shape (x, 128) with only possible values of 1 and 0.
    :param connect:  Connect adjacent cells of the matrix into a single longer note in the stream
    :param cells_per_qrtrnote:  number of pixels/cells per quarter note
    :return: music21 stream
    """
    s = music21.stream.Stream()
    for x in range(0, matrix.shape[0]):
        for y in range(0, matrix.shape[1]):
            if (matrix[x, y] == 1):
                if connect:
                    n = music21.note.Note()
                    n.pitch.midi = 128 - y
                    n.offset = x / cells_per_qrtrnote
                    j = x
                    d = 0
                    while (j < len(matrix) and matrix[j, y] == 1):
                        d += 1
                        matrix[j, y] = 0
                        j += 1
                    n.duration.quarterLength = d / cells_per_qrtrnote
                    s.insert(n.offset, n)
                else:
                    n = music21.note.Note()
                    n.pitch.midi = 128 - y
                    n.offset = x / cells_per_qrtrnote
                    n.duration.quarterLength = 1 / cells_per_qrtrnote
                    s.insert(n.offset, n)
    s.makeMeasures(inPlace=True)
    return s
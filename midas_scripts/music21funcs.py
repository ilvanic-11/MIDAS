# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# Name:         music21funcs.py
# Purpose:      This is the top file for extra music21 functions. These are functions
#				that operate directly on music21 Streams.
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    MIDAS is Copyright © 2017-2024 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-24 Michael Scott Cuthbert and the music21
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
import mido
#from midas_scripts import musicode
from collections import OrderedDict

chord_strings = ["Augmented", "Diminished", "Fifth", "Fifth 9th", "Fifth Octave", "Major", "Major 7th", "Minor",
                 "Minor 7th", "Minor 9th", "Octave", "Suspended 2", "Suspended 4"]
advanced_strings = ["6", "6add9", "6sus4", "7", "7#5", "7#5#9", "7#5b9", "7#9", "7#11", "7add11", "7add13", "7b5", "7b5b9",
                    "7b9", "7sus4", "9", "9#5", "9#11", "9b5", "9b13", "9sus4", "11", "11b9", "13", "13#9", "13b5b9",
                    "13b9", "add9", "aug", "augsus4", "m6", "m6add9", "m7", "m7add11", "m7add13", "m7b5", "m7b9", "m9",
                    "m9b5", "m9-Maj7", "m11", "m13",  "madd9", "Maj7", "Maj7#5", "Maj7#11", "Maj7add13", "Maj7b5",
                    "Maj9", "Maj9#5", "Maj9#11", "Maj9sus4", "Maj11", "Maj13", "MajB5", "Major", "mb5", "minor",
                    "m-Maj7", "m-Maj7add11", "m-Maj7add13", "m-Maj11", "m-Maj13", "sus2", "sus4", "tri"]
# chords_forms = [(0, 4, 4), (0, 3, 3), (0, 7), (0, 7, 7,), (0, 7, 5), (0, 4, 3), (0, 4, 3, 4), (0, 3, 4),  #subsequent steps
#                     (0, 3, 4, 3), (0, 3, 4, 3, 4), (0, 12), (0, 2, 5), (0, 5, 2)]
chords_forms = [(0, 4, 8), (0, 3, 6), (0, 7), (0, 7, 14), (0, 7, 12), (0, 4, 7), (0, 4, 7, 11), (0, 3, 7),    #Accumulative steps
                    (0, 3, 7, 10), (0, 3, 7, 10, 14), (0, 12), (0, 2, 7), (0, 5, 7)]
advanced_chords_forms = [[0, 4, 7, 9], [0, 4, 7, 9, 14], [0, 5, 7, 9], [0, 4, 7, 10], [0, 4, 8, 10], [0, 4, 8, 10, 15],
                         [0, 4, 8, 10, 13], [0, 4, 7, 10, 15], [0, 4, 7, 10, 18], [0, 4, 7, 10, 17], [0, 4, 7, 10, 21],
                         [0, 4, 6, 10], [0, 4, 6, 10, 13], [0, 4, 7, 10, 13], [0, 5, 7, 10], [0, 4, 7, 10, 14],
                         [0, 4, 8, 10, 14], [0, 4, 7, 10, 14, 18], [0, 4, 6, 10, 14], [0, 4, 7, 10, 14, 20],
                         [0, 5, 7, 10, 14], [0, 4, 7, 10, 14, 17], [0, 4, 7, 10, 13, 17], [0, 4, 7, 10, 14, 21],
                         [0, 4, 7, 10, 15, 21], [0, 4, 6, 10, 13, 21], [0, 4, 7, 10, 13, 21], [0, 4, 7, 14], [0, 4, 8],
                         [0, 5, 8], [0, 3, 7, 9], [0, 3, 7, 9, 14], [0, 3, 7, 10], [0, 3, 7, 10, 17], [0, 3, 7, 10, 21],
                         [0, 3, 6, 10], [0, 3, 7, 10, 13], [0, 3, 7, 10, 14], [0, 3, 6, 10, 14], [0, 3, 7, 11, 14],
                         [0, 3, 7, 10, 14, 17], [0, 3, 7, 10, 14, 21], [0, 3, 7, 14], [0, 4, 7, 11], [0, 4, 8, 11],
                         [0, 4, 7, 11, 18], [0, 4, 7, 11, 21], [0, 4, 6, 11], [0, 4, 7, 11, 14], [0, 4, 8, 11, 14],
                         [0, 4, 7, 11, 14, 18], [0, 5, 7, 11, 14], [0, 4, 7, 11, 14, 17], [0, 4, 7, 11, 14, 21],
                         [0, 4, 6], [0, 4, 7], [0, 3, 6], [0, 3, 7], [0, 3, 7, 11], [0, 3, 7, 11, 17],
                         [0, 3, 7, 11, 21], [0, 3, 7, 11, 14, 17], [0, 3, 7, 11, 14, 21], [0, 2, 7], [0, 5, 7],
                         [0, 3, 6, 9]]
chord_strings.extend([i for i in advanced_strings])
chords_forms.extend([i for i in advanced_chords_forms])
chord_dict = OrderedDict([i for i in zip(chord_strings, chords_forms)])



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

    :param stream:          stream to loop through
    :param measureNumber:   Number of the measure to transpose
    :param degree:          Integer degree (or interval) to transpose to. (i.e. (CEG) with a degree of 3 will transpose
                            to (EGB))
    :return:                Occurs in place. Returns nothing.
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


#Tr-2.
def transpose_all_measures_by_random( in_stream):
    """
        Transposes all Measures in the music21 stream by a random interval 1-7
    Currently only transposes up in pitch.

    :params stream:     The music21 stream in which to perform transposing.
    :return:            Returns a modified copy.deepcopy of in_stream.
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
    where the letters themselves ARE the musicode measure to be transposed. (musicode letter translations are by default
    one measure in length.)

    :param in_stream:   Translated musicode through which to loop.
    :param letter:      All instances of single letter/letters/lists of letters to be transposed.
                        0 does not equal root C.
    :param degree:      Degree of transposition.
    :return:            Operates in place, returns none.
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
        Transposes all Measures in the music21 stream by a random interval 1-7. Currently only transposes up in pitch.
        #TODO Expand.

    :params stream:         The music21 stream in which to perform transposing.
    :measure_num:           The number of the measure in the stream where transposing will occur.
    :interval_lower_limit:  Lower limit of how far the random transpose can go.
    :interval_upper_limit:  Upper limit of how far the random transpose can go.
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

    :param in_chord:    User-introduced chord.
    :param intv_num:    Generic interval(i.e 3=third, 7=seventh, etc.)
    :param key:         Key to be specified.
    :param octave:      Octave to be specified by an Int.
    :return:            Returns ch = music21.chord.Chord(modified in_chord)
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

    :param in_stream:       Translated Musicode.
    :param range_l:         Starting measure number to edit.
    :param range_h:         Ending measure number up to which to edit.
    :param offset_number:   Offset in quarter notes. (1 = One quarternote, Negative numbers and fractions are allowed.)
    :return:                Stream
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

    :param in_stream:       Translated Musicode.
    :param range_l:         Starting measure number to edit.
    :param range_h:         Ending measure number up to which to edit.
    :param duration_len:    Duration in quarterlength. (1 = one quarter note. Can do many division smaller than a
                            quarter note. Negative numbers are allowed.)
    :return:                Stream.
    """
    for m in in_stream.getElementsByClass(music21.stream.Measure):
        if (m.number >= range_l and m.number <= range_h):
            for n in m.flat.notes:
                d = music21.duration.Duration(duration_len)
                n.duration = d
    in_stream.makeMeasures()
    return in_stream

def compress_durations(in_stream):
    for i in in_stream.flat.notes:
        if i.duration.quarterLength > 7.875:
            i.duration.quarterLength = 7
    return in_stream

#M-3. TODO NEEDS FIXING!!
def stretch_by_measure( in_stream, range_l, range_h, ratio, stretchDurations=True):
    """
        For every measure in a range range_l to range_h in a music21.stream.Stream, proportionally stretch the offsets
    of each note in those measures. Option added to stretch the durations of those notes in the same manner. Used in
    align_musicode_with_melody().

    :param in_stream:   Operand stream.
    :param range_l:     Low limit of selected range.
    :param range_h:     High limit of selected range.
    :param ratio:       Ratio value for stretching. 2 doubles. .5 cuts in half.
    :return:            Operates in place, returns in_stream.
    """
    print("Ratio=")
    print(ratio)
    assert in_stream.getElementsByClass(music21.stream.Measure) is not None, \
        print("In function 'stretch_by_measure', in_stream has no measures. Cannot stretch.")

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

    in_stream.remove(l)  # This is cool.
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


def restretch_by_factor(in_stream, factor, in_place=True):
    """
        This function restretches (it can also compress) the musical(midi) data in a stream by refactoring all the
    notes' offsets and durations by a user specified amount.
    :param in_stream:           Operand stream.
    :param factor:              Multiplication refactoring value.
    :param in_place:            Bool determing whether to return in_stream or a deep copy.
    :return:
    """
    # starting_point * (target_highestTime / current_highestTime)
    s = in_stream if in_place else copy.deepcopy(in_stream)

    for i in list(s.recurse()):
        i.duration.quarterLength = i.duration.quarterLength * factor
        i.offset = i.offset * factor

    return s


#M-4.
def arpeggiate_chords_in_stream(in_stream, stepsize=1, ascending=True):
    """
        This iterates for the stream.chord.Chord objects and turns them into arpeggiated
    instances of the chord with the same notes, but different offsets.

    :param in_stream:   In-stream.
    :param stepsize:    Stepsise factor of arpeggiation of notes in found chords.
    :return:            in_stream
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
def chop_up_notes(in_stream, offset_interval=1):
    """
        This function takes an in_stream and evenly dices all of the notes in it. The offset interval determines the
    size of this dicing.
    (i.e. An offset interval of 1 on a whole note would chop it up into four quarter notes.)

    :param in_stream:           Operand music21.stream object.
    :param offset_interval:     Size of chopped up notes.
    :return:                    New music21.stream object. (part, score, stream, voice etc.)
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
def merge_contiguous_notes(in_stream, part=False, skip=False, inPlace=False):
    """
        This function takes a stream of noticeably "chopped up notes" (see sister function) and reconnects or "glues"
    those notes (back) together in a contiguous manner.

    :param in_stream:       input stream
    :param max_note_size:   maximum note size to make when combining contiguous notes in quarterlength
    :return:                new stream
    """
    import numpy as np
    new_stream = music21.stream.Stream() if part is False else music21.stream.Part()
    if skip:
        #Skip the notafy.
        m = np.array(stream_to_matrix(in_stream))
        print(m)
        new = matrix_to_stream(m, connect=True)
    else:
        s = notafy(in_stream)
        m = np.array(stream_to_matrix(s))
        print(m)
        new = matrix_to_stream(m, connect=True)
    for i in in_stream.flat.notes:
        in_stream.remove(i, recurse=True)
    if inPlace:
        for j in new.flat.notes:
            in_stream.insert(j.offset, j)
        return in_stream
    else:
        for j in new.flat.notes:
            new_stream.insert(j.offset, j)
        return new_stream


##SYNTHESIS_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#Syn-1.
def set_chord_octave(in_chord, octave):
    """
        Sets the octaves of chords. Some music21 chords don't have octaves, so a simple call helps sometimes.

    :param in_chord:    Chord object with pitches.
    :param octave:      Octave of pitches in chord.
    :return:            in_chord

    "NOTE: Only works well for triads and sevenths, chord bigger than one octave will not need this."
    """
    for p in in_chord.pitches:
        p._setOctave(octave)
    return in_chord


#Syn-2. #Todo Review these.
def make_chords_from_notes(in_stream, in_chord, inv):
    """
        For singular notes in a music21 stream, this function takes those notes and turns them into chords with that
    note forming the 'root' of the new chord.

    :param in_stream:   Stream with notes for changing.
    :param in_chord:    Chord called to replace note.
    :param inv:         Chord's inversion, if any.
    :return:            Operates in place, returns in_stream.
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
            c.removeRedundantPitches()  #TODO removeRedundantPitches causes .write problems. 02/21/2023
    return in_stream


#Syn-3.
def make_chords_from_notes_2(in_stream, in_chord, inv):
    """
        Same as make_chords_from_notes, albeit written slightly different.

    :param in_stream:   Stream with notes for changing.
    :param in_chord:    Chord called to replace note.
    :param inv:         Chord's inversion, if any.
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


def make_chords_from_notes_3(in_stream, chord_form_list, inv_list=None):
    """
        This function is intended and designed to operate on a music21 stream sequence of already-existing,
    non-overlapping notes only; no chords.
    (for example: a music21.stream.Stream() object with notes 'appended' one by one.)

    :param in_stream:           Our operand stream with sequential non-overlapping notes.
    :param chord_form_list:     A list of strings denoting chord types (i.e "Fifth 9th", "Fifth Octave", "Major",
                                                                        "Major 7th", "Minor", etc.)
    :param inv_list:            A list of integers denoting which inversion of each chord to use. Since we are composing
                                , and therefore deciding, our chords, we can also choose our chords' inversions.
    :return:                    A new_stream full of our new chords that replaced our sequence of root notes.
    """

    error_string = "For proper use, the # of chords in your chord_form_list " \
        "should match the # of notes you're turning into chords." \
        "The same length should hold true for your inversion list."
    if inv_list is not None:
        assert len(in_stream.flat.notes) == len(chord_form_list) == len(inv_list), \
        "%s" % error_string
    else:
        assert len(in_stream.flat.notes) == len(chord_form_list), \
        "%s" % error_string
    new_stream = music21.stream.Stream()
    notes_from_stream = [i for i in in_stream.flat.notes]
    for i in range(len(notes_from_stream)):
        chord_from_note = note_to_chord(notes_from_stream[i], chord_form_list[i], inv=inv_list[i] if inv_list is not None else None)
        new_stream.insert(chord_from_note.offset, chord_from_note)
    return new_stream

def note_to_chord(music21note, chord_form, inv=None):
    """

    :param music21note:
    :param chord_form:
    :param inv:
    :return:
    """
    #TODO Finish chord_dict, #inv optionCHECK , and DOC!
    chord_formula = chord_dict[chord_form]
    chord_from_note = music21.chord.Chord([music21note.pitch.midi + i for i in chord_formula])
    chord_from_note.duration = music21note.duration
    chord_from_note.volume.velocity = music21note.volume.velocity if music21note.volume.velocity is not None else 90
    chord_from_note.offset = music21note.offset

    if inv is not None:
        assert inv == len(chord_form),  "Your inversion selection does not match the size of your chord."
        chord_from_note.inversion(inv)

    return chord_from_note


#Syn-4.
def make_notes_from_numbers(input, note_length = 1, base=None):
    """
        This function takes a string or list of numbers on input and makes music21 notes from each of them individually where
    the music.note.Note().pitch.midi value is set equal that digit.

    #Example use:
    >>>make_notes_from_numbers("123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ", base=36)
    The keychoice=None was removed from the parameters inputs; keychoice can be done with the function
    --> midiart.filter_notes_by_key()

    #TODO NEEDS Finishing. The range of possible pitch values is only within a single octave at present. (i.e. The--
    #TODO --handling of 10 = A, 11=B, 12=C for higher base numbers should equal a pitch higher than one octave)

    :param in_string:
    :param keychoice:
    :param note_length:
    :return:
    """
    # if keychoice == "":
    #     keychoice = None
    #     keysig = None
    # else:
    #     keysig = music21.key.Key(keychoice)
    # allowedPitches = list()
    # print("Key is: ")
    # print(keysig)
    # if keychoice == None:
    #     allowedPitches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # elif (type(keysig) is music21.key.Key):
    #     for p in music21.scale.Scale.extractPitchList(keysig.getScale()):
    #         allowedPitches.append(p.pitchClass)
    # allowedPitches[-1] = 12  #Dahfuq is this line?!
    # print(allowedPitches)

    if type(input) == list:
        pass
    elif type(input) == str:
        input = [i for i in input]  #This won't deal with numbers that have multiple digits.

    out_stream = music21.stream.Stream()
    for k in input:
        if k == " ":
            r = music21.note.Rest()
            r.duration.quarterLength = note_length
            out_stream.append(r)

        else:# k.isnumeric():   #This won't work if 'ABCDEF' count as numbers for higher bases.
            k = int(k, base if base is not None else 10)
            #if k >= len(allowedPitches):
                #k = k % len(allowedPitches)
            n = music21.note.Note()
            n.pitch.ps = k #allowedPitches[int(k)]
            n.duration.quarterLength = note_length
            out_stream.append(n)

    return out_stream


#Syn-4-2.
def make_notes_from_string_of_numbers_2(in_string, keychoice=None, note_length = 1):
    """
        This function takes a string of numbers on input and makes music21 notes from each of them individually where
    the music.note.Note().pitch.midi value is set equal that digit.

    #TODO NEEDS Finishing. The range of possible pitch values is only within a single octave at present. (i.e. The--
    #TODO --handling of 10 = A, 11=B, 12=C for higher base numbers should equal a pitch higher than one octave)

    :param in_string:
    :param keychoice:
    :param note_length:
    :return:
    """
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
        This function takes a range of fibonacci numbers(acquired from music21funcs.fibonacci_range_mm()  ) and provides
    an option to change the base of this range of fib numbers. Then, from this new range of new-base fib numbers, for
    every individual digit we create a music21.note.Note() with the digit itself as the note's pitch. (Executed in
    music21funcs.make_notes_from_string_of_numbers()).

    :param range_l:         Starting low range value for fibonacci function.
    :param range_h:         Ending high range value for fibonacci function.
    :param scale_mode:      Cm for C minor scale E for E major scale, None for Chromatic, this sets the scale mode of
                            pitches to which to assign acquired numbers from this function.
    :param base:            The mathematical base of the numbers acquired; after acquisition, they will be concatenated,
                            varying the number of notes created and the range of pitches allowed.
    :param note_length:     The rhythmic density of the notes created, specified by music21's quarterLength property.
    :param spaces:          If true, space are place between each fibonacci number.
    :return:                A new "fibonacci" stream.
    """

    fibonacci_array = fibonacci_range_mm(range_l, range_h)
    new_fib_array = [base10toN(int(j), base) for j in fibonacci_array]
    if spaces:
        new_fibonacci = " ".join(new_fib_array)
    else:
        new_fibonacci = "".join(new_fib_array)
    print("new_fibonacci", new_fibonacci)
    fibonacci_stream = make_notes_from_numbers(new_fibonacci, note_length=note_length, base=base) #keychoice=scale_mode,
    return fibonacci_stream


#Syn-6.
def array_selection_to_music(list_array, scale_mode, base, note_length = 1, spaces=False):    ###chords=True
    """
        This function performs similiar to fibonacci_to_array, only this function allows a user-specified or random
    input of numbers instead of just the fibonacci range. The base is still able to be changed.

    :param list_array:      Numpy 1D array of numbers, can be int or float.
    :param scale_mode:      Cm for C minor scale E for E major scale, None for Chromatic, this sets the scale mode of
                            pitches to which to assign acquired numbers from this function.
    :param base:            The mathematical base of the numbers acquired; after acquisition, they will be concatenated,
                            varying the number of notes created and the range of pitches allowed.
    :param note_length:     The rhythmic density of the notes created, specified by music21's quarterLength property.
    :return:                Returns a music21.stream.Stream.
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
    out_stream = make_notes_from_numbers(fin_list, note_length=note_length, base=base) #keychoice=scale_mode,
    return out_stream


#Syn-
def base10toN(num, base):
    """
        This functions changes a ``num'' number to given base. Up to base 36 is supported.
    #TODO Make able to support floats.

    :param num:     Operand int.
    :param base:    Base to which to be changed.
    :return:        Returns a string. #TODO Should be int? float?
    """

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
    """
        This function returns all the numbers in the fibonacci sequence from specified low range (l) to high range (h).

    :param l:   Low end of range.
    :param h:   High end of range.
    :return:    numpy.array
    """

    n = np.arange(l, h)
    sqrt5 = np.sqrt(5)
    phi = (1 + sqrt5)/2
    #fibonacci = np.array((phi**n - (-1/phi)**n)/sqrt5, dtype=np.int64)
    fibonacci = np.rint((phi**n - (-1/phi)**n)/sqrt5)
    print("Fibonacci", fibonacci)
    return fibonacci


##MUSIC21_FUNCTIONS\CLASSES (NEW, for later)
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


#M21-1.
#TODO Needs WAY fixing.
#TODO Needs a complete redo. But since music21's .write("mid") function has it's own quirks, it's not priority.
def delete_redundant_notes(in_stream, greatest_dur=False):
    """
        This function takes all the notes of a music21 stream and deletes redundant notes of the same pitch at the
    same offset while allowing the user to choose which duplicate note to keep based on duration.quarterLength. The
    method here uses in_stream.getElementsByOffset, python's min() and max() functions, the "set" feature of an ordered
    dict, and some nested setting and getting that loops over music21 streams.

    :param in_stream:       Stream with notes.
    :param greatest_dur:    Boolean determining whether to choose the duplicate note(s) with longest duration or the
                            shortest.
    :return: new_stream.    Returns a new music21 stream with just notes.
    """

    offset_dict, offsets, dict_list = get_offsets_dictionary(in_stream)

    #TODO FINISH!
    # NOW REBUILD STREAM!!!
    # new_stream = music21.stream.Stream()
    # for x in range(0, len(offsets), 1):
    #     for y in dict_list[x].values():
    #         for z in y:			##The DURATION call happens here.
    #             if greatest_dur is True:
    #                 dur = max([z.quarterLength for z in y])
    #                 if z.quarterLength == dur:
    #                     new_stream.insert(offsets[x], copy.deepcopy(z))
    #             elif greatest_dur is False:
    #                 dur = min([z.quarterLength for z in y])
    #                 if z.quarterLength == dur:
    #                     new_stream.insert(offsets[x], copy.deepcopy(z))
    # return new_stream


def get_offsets_dictionary(in_stream):
    #TODO Docs.
    """

    :param in_stream:
    :return:
    """
    # notes_list is a list of lists of notes found at the offets of our iteration.

    # First, we eliminate chord objects with notafy(), a function that basically flattens chords(all chord objects become
    # respective note objects).
    # This way, we are working with just notes in a stream.
    # A stream with just note objects, no chord objects.
    notafied_stream = notafy(in_stream.flat.notes)  ##TODO Do I need flat.notes here?

    # dicts_list is a list of Ordered Dictionaries of pitches(keys) and notes(values)
    # created for every offsets found in our iteration.
    dict_list = list()
    offset_dict = OrderedDict()

    # Our list of offsets. List(set([list])) eliminates duplicate offsets.
    # offsets = list(set([i[1] for i in notafied_stream.offsetMap()]))
    offsets = OrderedDict.fromkeys(i.offset for i in notafied_stream.offsetMap())

    # for i in range(0, len(offsets)):
    #     if type(notafied_stream.getElementsByOffset(i)) is music21.note.Note:
    #         pitches_list.append(notafied_stream.getElementsByOffset(i).pitch.ps)
    #         notes_list.append(notafied_stream.getElementsByOffset(i))
    # matched_list.append([k for k in notes_list if k.pitch.ps == notafied_stream.getElementsByOffset(i).pitch.ps])

    for l in offsets:
        pitches_list = list()
        notes_list = list()
        matched_list = list()
        pitch_dicts = OrderedDict()
        for i in notafied_stream.getElementsByOffset(l):
            if type(i) is music21.note.Note:
                pitches_list.append(i.pitch.ps)
                notes_list.append(i)
            # This line becomes operationally expensive the farther in the loop it goes.
            # Upon further review, this line is actually clever. It gets us all of the notes that match our pitch, which
            # is what we want
            # unique_pitches_dict = OrderedDict.fromkeys([i for i in pitches_list])

            matched_list.append([k for k in notes_list if k.pitch.ps == i.pitch.ps])  # Clever because it matches "i";
            # That's where we are in the current loop.
        for j in zip(pitches_list, matched_list):
            pitch_dicts.update([
                                   j])  # Pitches become the keys of OrderedDicts, and notes with matching pitches become the values of those keys for every offset "l".

        # TRY TURNING this dict_list into an OrderedDict instead of it being a list. 01/24/2023
        dict_list.append(pitch_dicts)
    for j in zip([o for o in offsets.keys()], dict_list):
        offset_dict.update([j])
    # print("DICT_LIST", dict_list)
    print("OFFSET_DICT", offset_dict)
    return offset_dict, offsets, dict_list
    # s1 = music21.stream.Stream()
    # s1._findLayering()
    # s1.makeChords()


def check_for_offset_duplicates(offset_dict):
    for i in offset_dict:
        # print(i)
        for j in offset_dict[i]:
            if len(offset_dict[i][j]) == 1:
                #print(len(offset_dict[i[j]]))
                pass
            else:
                print("This stream has duplicate notes, DISCONTINUING!")  # for k in j:
                return True# print(len(k))#0print(len(j))
    print("This stream has NO duplicate notes, PASSING!")  # for k in j:
    return False


#TODO Finish!!! REDO.
def delete_redundant_notes2(in_stream, greatest_dur=True):
    """
        A simple instance of deleting the notes that are overlapping, except for the a selected one.
    :param in_stream:
    :return:
    """
    #Make notes only, no chord objects.
    notafied_stream = notafy(in_stream)

    #Ending container stream
    new_stream = music21.stream.Stream()

    #Find our overlaps
    overlaps = notafied_stream.getOverlaps()
    print("Overlaps", overlaps)

    ##Get a list of existing unique offsets; getOverlaps() does this for us.
    unique_offset_list = [j for j in overlaps] #***revise   #in OrderedDict.fromkeys([i.offset for i in in_stream.flat.notes])]
    print("UOL", unique_offset_list)

    ##For every unique offset, get the unique, existing pitches.
    note_list = []
    for p in unique_offset_list:    #***revise
        for r in notafied_stream.getElementsByOffset(p):
            note_list.append(r)
        #type(notafied_stream.getElementsByOffset(o)) == music21.note.Note]
    print("Note_List", note_list)
    note_list_ids = [i.id for i in note_list]
    print("Note_ids", note_list_ids)


    # unique_pitch_dict = OrderedDict.fromkeys([x.pitch.ps for x in note_list])
    # print("UPD", unique_pitch_dict)

    selection_list = []
    # for h in unique_pitch_dict:
    for i in overlaps:          #unique offsets
        print("Set_Check", set([q.quarterLength for q in overlaps[i]]))
        if len(set([q.quarterLength for q in overlaps[i]])) > 1: #If all the durations of the overlaps are NOT the same
            if greatest_dur is True:
                dur = max([note.quarterLength for note in overlaps[i]])
                for j in overlaps[i]:   #overlaps at those offsets
                    print("Dur", dur)
                    if j.quarterLength == dur:
                        selection_list.append(j)
                            #new_stream.insert(i, copy.deepcopy(j))
            elif greatest_dur is False:
                dur = min([note.quarterLength for note in overlaps[i]])
                for j in overlaps[i]:   #overlaps at those offsets
                    if j.quarterLength == dur:
                        selection_list.append(j)
                        #new_stream.insert(i, copy.deepcopy(j))
        else:
            ## If all the durations of the overlaps ARE the same (same pitch, offset, AND duration...
            ## Just pick the first one.
            selection_list.append(overlaps[i][0])

            #new_stream.insert(i, copy.deepcopy(overlaps[i][0]))
    print("Selection_List", selection_list)
    #print("Selection_List_ID1", selection_list[0].id)

    #REINSERT all the notes that didn't have overlaps; i.e all our original, non-overlapping notes.
    for i in note_list:
        if i.offset not in overlaps:
            new_stream.insert(i.offset, i)
    #Insert the notes from our selection list.
    for i in selection_list:
        new_stream.insert(i.offset, i)
    return new_stream



#TODO in_place = True\False
#M21-2.
def notafy(in_stream, part=False, inPlace=False, chordifyFirst=False, specialMerge=False):
    """
        Returns a copy of the in_stream but with all 'chord' objects replaced with
    separate individual 'note' objects for each note in the chord. Basically, it is a chord.flatten() function.

    :param in_stream:   Operand stream.
    :return:            new_stream
    """
    work_stream = in_stream.chordify(removeRedundantPitches=False) if chordifyFirst else in_stream

    new_stream = music21.stream.Stream() if part is False else music21.stream.Part()
    print("IN_STREAM_LENGTH1", len(work_stream.flat.notes))
    for i in work_stream.flat.getElementsByClass(["Chord", "Note"]):
        notelist = list()
        if type(i) is music21.chord.Chord:
            #i.removeRedundantPitches(inPlace=True)
            pitches = i.pitches                     #All pitches
            pitches = list(pitches)
            pitches.sort()                          #All pitches sorted
            pitches = OrderedDict.fromkeys(pitches) #All unique pitches, the set of
            for p in pitches:                     #i.
                newnote = music21.note.Note(p)
                newnote.offset = i.offset
                newnote.duration = i.duration
                if i.volume.velocity:
                    newnote.volume.velocity = i.volume.velocity
                else:
                    #print("No velocity info for chord. ")
                    #pass
                    i.volume.velocity = 90
                notelist.append(newnote)
            for x in notelist:
                new_stream.insert(i.offset, copy.deepcopy(x))
        elif type(i) is music21.note.Note:
            #print("note here")
            new_stream.insert(i.offset, copy.deepcopy(i))
        in_stream.remove(i) if inPlace else None  #, recurse=True

    print("IN_STREAM_LENGTH2", len(in_stream.flat.notes))
    print("HERE A")
    if inPlace:
        for j in new_stream.flat.notes:
            print("in_stream here????")
            in_stream.insert(j.offset, copy.deepcopy(j))
        print("IN_STREAM_LENGTH3", len(in_stream.flat.notes))
        if specialMerge:
        # A specific use-case requiring an inPlace operation of chordify, notafy, AND merge_contiguous notes.
            #in_stream = \
            merge_contiguous_notes(in_stream, part=True, skip=True, inPlace=True)
        print("HERE B")
        return in_stream
    else:
        # print("NEW_STREAM BITCH:", new_stream)
        # new_stream.show('txt')
        print("HERE C")
        real_new_stream = copy.deepcopy(new_stream)
        print("New_Stream", new_stream)
        print("real_new_Stream", real_new_stream)
        return real_new_stream


#music21.stream.Stream().chordify()
# def slice_at_offsets(in_stream, offsetList, in_place=True):
# # list of start, start+dur, element, all in abs offset time
#
#     returnObj = copy.deepcopy(in_stream) if not in_place else in_stream
# # make a copy
#
#
#     offsetMap = in_stream.offsetMap(returnObj)
#     print("offsetMap", offsetMap)
#
#     offsetList = [music21.common.numberTools.opFrac(o) for o in offsetList]
#     print("offsetList", offsetList)
#
#     for ob in offsetMap:
#         # if target is defined, only modify that object
#         e, oStart, oEnd, unused_voiceCount  = ob
#         # if target is not None and id(e) != id(target):
#         #     continue
#
#         cutPoints = []
#         oStart = music21.common.numberTools.opFrac(oStart)
#         oEnd = music21.common.numberTools.opFrac(oEnd)
#
#         for o in offsetList:
#             if o > oStart and o < oEnd:
#                 cutPoints.append(o)
#         # environLocal.printDebug(['cutPoints', cutPoints, 'oStart', oStart, 'oEnd', oEnd])
#         if cutPoints:
#             # remove old
#             #eProc = returnObj.remove(e)
#             eNext = e
#             oStartNext = oStart
#             for o in cutPoints:
#                 oCut = o - oStartNext
#                 unused_eComplete, eNext = eNext.splitAtQuarterLength(oCut,
#                     retainOrigin=True)
#                     #addTies=addTies,
#                     #displayTiedAccidentals=displayTiedAccidentals)
#                 # only need to insert eNext, as eComplete was modified
#                 # in place due to retainOrigin option
#                 # insert at o, not oCut (duration into element)
#                 returnObj.coreInsert(o, eNext)
#                 oStartNext = o
#     returnObj.coreElementsChanged()
#     if in_place is False:
#         return returnObj




#M21-3.


def separate_notes_to_parts_by_velocity(in_stream, part=False):
    """
        This function is required for extract_XYZ_coordinates_to_stream. It separates all the notes of a stream into
    parts with their respective "part.partsName" properties set equal to all the possible velocities of in_stream.
    This allows for the separation of those notes with those particular velocities into the same-named specified parts
    within the stream.

    :param in_stream:   Stream to be modified.
    :param part:        Bool determining if 'end_stream' will be a music21.stream.Part().
    :return:            Stream with parts.
    """
    part_stream = music21.stream.Stream()
    velocity_list = list()
    if part is True:
        end_stream = music21.stream.Part()
    else:
        end_stream = music21.stream.Stream()

    #Create a set of non-duplicate velocities.
    for h in in_stream.flat.notes:
        velocity_list.append(h.volume.velocity)
    velocity_set = sorted(set(velocity_list))  #Todo An OrderedDict could be used here....

    #Create a stream with parts equal to the number of non duplicate velocities.
    #Assign the names of those Parts as equal to the values of the set velocities; they are ints.
    for k in velocity_set:
        parts1 = music21.stream.Part()
        parts1.partsName = k
        part_stream.insert(0.0, copy.deepcopy(parts1))

    #Insert notes of same velocity value into stream.Part of the same value name.
    for s in part_stream.getElementsByClass(music21.stream.Part):
        for q in in_stream.flat.notes:
            if q.volume.velocity == s.partsName:
                s.insert(q.offset, copy.deepcopy(q))
            else:
                pass
        end_stream.insert(s.offset, copy.deepcopy(s))
    return end_stream


def merge_notes_to_one_part(in_stream, part=False, by_velocity=None, append_header=False):
    """
        This function takes an in_stream and allocates all notes into one part within the stream. It has the added
    option of changing all the velocity values of the notes to one value as well. This
    music21.stream.Part() can either be returned alone if part==True or it can be returned appended inside
    a music21.stream.Stream() parent. If by_velocity is not None, it

    :param in_stream:       Operand music21.stream .Stream() or .Part().
    :param part:            If True, return a .Part() else return a .Stream().
    :param by_velocity:     If not None, this int will become the part.partName property of the returned part. It will
                            also determine the velocity to which to change the notes.
    :param append_header:   If true, adds music21.meter.TimeSignature() and music21.tempo.MetronomeMark() objects to the
                            head of the returned stream. (Useful for creating editable midi files.)
    :return:                A music21.stream .Stream() or .Part()
    """
    #Establish part
    part_stream = music21.stream.Part()
    #Name it.
    if by_velocity:
        part_stream.partName = by_velocity
    else:
        pass
    #Extract notes and possibly change velocity values
    for i in in_stream.flat.getElementsByClass(["Chord", "Note"]):
        if by_velocity is not None:
            i.volume.velocity = by_velocity
        else:
            pass
        part_stream.insert(i.offset, copy.deepcopy(i))

    if part is True:
        end_stream = part_stream
        if append_header:
            add_timesig_and_metronome(end_stream)
    else:
        end_stream = music21.stream.Stream()
        end_stream.append(part_stream)
        if append_header:
            add_timesig_and_metronome(end_stream)
    pass
    return end_stream



#M21-4.
def set_note_velocities(in_stream, vel):
    """
        Simple call for setting the all the velocites in a stream to a single value.

    :param in_stream:   Operand stream.
    :param vel:         Value to which to set stream note velocites.
    :return:            In_stream. Operates in place.
    """
    for i in in_stream.flat.notes:
        i.volume.velocity = vel
    return in_stream


#M21-5. #TODO Needs revision. What purpose does this serve? Must len(volume_list) be == len([o for o in in_stream.flat.notes])?
def change_velocities_by_rangelist(in_stream, volume_list):
    """
        Changes the velocities of notes in a stream as input to the values found in a user-specified volume list. Using
    subscripting it would be equivalent to in_stream-note[0].volume.velocity = volume_list[0] for the entire range. If
    the length of the volume_list is less then the length of the range of notes, the remaining notes velocities are set
    to zero. #TODO Change this?

    :param in_stream:   Operand stream.
    :param volume_list: Use range(0, desired velocity limited)
    :return:            Operates in place, returns in_stream.
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
    """
        For every note in a stream with a selected duration, this function changes those notes' velocity to the specified
    velocity choice 'vel_choice'.

    :param in_stream:   Operand stream.
    :param dur_choice:  Choice of duration value. #TODO Would a range of durations be better in a workflow?
    :param vel_choice:  Choice of velocity value.
    :return:            Operates in place, returns in_stream.
    """
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
def change_midi_channels_to_one_channel(midi_file, channel=1):
    """
        This function takes a midi file on input and changes the "channel"
    property of every track in midi_file to a user-selected value between 1 and 16. This operation occurs in place.

    :param midi_file:   Midi file input.
    :param channel:     User selected channel value.
    :return:            midi_file
    """

    a_file = music21.midi.MidiFile()
    a_file.open(midi_file, attrib="rb")
    a_file.read()
    for j in a_file.tracks:
        j.setChannel(channel)
    a_file.close()
    a_file.open(midi_file, attrib="wb")
    a_file.write()
    a_file.close()


def get_highest_time_from_directory(directory):
    """
        This function takes all the midifiles from a directory, parses them using music21.converter.parse, acquires each
    of their highestTime properties in a list, and finally returns the max([highestTimes..,..,..]) of that list.
    :param directory:       Operand directory.
    :return:                Int max value of a list.
    """
    for subdir, dirs, files in os.walk(directory):
        highTime = 0
        # for file in files:
        parsons = ([music21.converter.parse(subdir + os.sep + file).highestTime for file in files])
        print("Parse", parsons)
        highTime += max(parsons)
        print("Highest Time is...", highTime)
        print("Subdir", subdir, type(subdir))
        stretch = highTime
        return stretch


#M21-8.
def split_midi_channels(midi_file_or_stream, directory, name): ###, to_file=False, from_stream=False):
    """
        This function uses music21 and takes a midi file on input and separates* all the "channels" of the midi file
    into either parts in a stream, or a directory of written .mid files, one midi file for each said "channel." The
    files\\parts are also conveniently named by the channel.

    *Note-- Loading a midi_file created from midiart.make_midi_from_pixels, a midi image, can be a slow process.

    :param midi_file:   Midi .mid file to be split, denoted by a string filepath.
    :param directory:   Folder to which new output midi files will be saved.
    :param name:        Name of all the files with addends "_1", "_2"....etc. appended to each.
                        (i.e. midi_file_1.mid, midi_file_2.mid....)
    :param to_file:     If true, writes files to the selected directory. If false, splits the midi to named parts in a
                        stream where the part.Name property of these parts equals the channel value.
    :return:            Midi .mid files written to directory OR a stream with parts separated and named by channel.
    """

    ##Read Midi File
    a_file = music21.midi.MidiFile()
    a_file.open(midi_file_or_stream, attrib="rb")
    a_file.read()
    for z in range(len([i for i in a_file.tracks if i.hasNotes()])):

        # Get the z-th track from a_file.tracks
        first_track = a_file.tracks[z]

        # Create a new MidiFile object
        new_midi_file = music21.midi.MidiFile()

        # Create a MidiTrack object and set its events to the events from the first track
        midi_track = music21.midi.MidiTrack(index=z)
        midi_track.events = first_track.events

        # Add the track to the new MidiFile
        new_midi_file.tracks.append(midi_track)

        #Output file naming
        zero_holder = "_00" if int(z) < 10 else "_0"
        re_name = os.path.splitext(os.path.basename(name))[0]
        output_name = directory + "\\" + re_name + "_SPLIT" + zero_holder + "%s" % z + ".mid"

        # Write the new MidiFile to a MIDI file
        new_midi_file.open(output_name, 'wb')
        new_midi_file.write()
        new_midi_file.close()

    # ##Get indices and channels from tracks.
    # a_stream = music21.midi.translate.midiTracksToStreams(a_file.tracks)
    #
    # ##Access and separate tracks and name stream.Parts accordingly.
    # parse_stream = music21.converter.parse(midi_file_or_stream)
    # parse_stream.write("mid", midi_file_or_stream)
    #
    # #note_tracks = [m for m in a_file.tracks if m.hasNotes()]
    # note_tracks_channels = []
    # for m in a_file.tracks:
    #     if m.hasNotes():
    #         if len(m.getChannels()) > 1:
    #             note_tracks_channels.append(m.getChannels()[1])
    #         else:
    #             note_tracks_channels.append(m.getChannels())
    # #print("NTCs", note_tracks_channels)
    #
    # index_list = []
    # for indexes in a_file.tracks:
    #     if indexes.hasNotes():
    #         index_list.append(indexes)
    #
    # print("IndexList", index_list)
    # print("Note_track Length:", len(note_tracks_channels))
    #
    # for s in a_stream:
    #     print("First Partname", s.partName)
    #
    # for z in range(0, len(index_list)):
    #     parse_stream[z].partName = note_tracks_channels[z]
    #
    # a_file.close()
    #
    # #a_stream.show('txt')
    # for p in parse_stream:
    #     print("Changed partname:", p.partName)
    #
    #
    # if to_file:
    #     for part in parse_stream:
    #         zero_holder = "_00" if int(part.partName) < 10 else "_0"
    #         final_midis = music21.midi.MidiFile()
    #         output_name = directory + "\\" + name + zero_holder + "%s" % part.partName + ".mid"
    #
    #         print("Changed partname:", part.partName)
    #         part.write("mid", output_name)
    #
    #         new_part_stream = music21.converter.parse(output_name)
    #         new_part_stream.write("mid", output_name)
    #
    #         final_midis.open(output_name, attrib='rb')
    #         final_midis.read()
    #         print("PART_NAME", part.partName)
    #
    #         #CORE of the Function: this is what makes the colors work in FL Studio.
    #         final_midis.tracks[0].setChannel(part.partName)
    #         final_midis.close()
    #
    #         final_midis.open(output_name, attrib='wb')
    #         final_midis.write()
    #         final_midis.close()
    # else:
    #     return parse_stream


##Data Analysis Functions.
# M21-9.
def print_chords_in_piece(in_stream):
    """
        Use .flat and .makeMeasures to acquire appropriate callable stream
    :param in_stream:   Operand music21.stream.Stream().
    :return:            String.
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


# M21-10.
def print_show_streamtxt(in_stream):
    """
        This function creates and returns a string from the .show() method of the in_stream

    :param in_stream:   Operand stream.
    :return:            String.
    """

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


# M21-11.
def print_midi_data(in_stream):
    """
        This function takes a stream, converts it to a midifile using music21.midi.MidiFile(), and then returns all the
    read midi messages as a string.

    :param in_stream:   Operand stream.
    :return:            String.
    """
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


#M21-
def fill_measure_end_gaps(measure, timeSig=None, inPlace=True):
    """
        This function takes a music21.stream.measure as input and fills in empty "duration" gaps at the
    beginning AND\OR end of a measure. It does not operate on empty gaps "in-between" notes or elements in a measure.

    :param measure:     A music21.stream.Measure object, with or without a time Signature object.
    :param timeSig:     The time signature specifier, this can be a string as '4/4' or a music21.meter.TimeSignature()
                        object. Time signature value will default to '4/4' if not specified.
    :param inPlace:     If true, returns same input measure, else returns a deepcopy.
    :return:            measure or copy.deepcopy(measure)
    """

    #A check against multiple timeSignatures within measure.
    time_list = []
    for i in measure.flat.getElementsByClass(music21.meter.TimeSignature):
        time_list.append(i)
    if len(time_list) != 1: #Todo is this a good check?  ==?
        print("You have zero or more than one time signature object in this measure."
              "/n If zero, input timeSig will be used.")

    #timeSig input Checks.
    if timeSig is None and measure.flat.hasElementOfClass(music21.meter.TimeSignature):
        timeSig = [i for i in measure.flat.getElementsByClass(music21.meter.TimeSignature)][0]
    elif type(timeSig) is str:  #If specified as a string, create a music21.meter.TimeSignature object from that string.
        timeSig = music21.meter.TimeSignature(timeSig)
    else:   #If none specified.
        timeSig = music21.meter.TimeSignature('4/4')


    new_measure = copy.deepcopy(measure)
    r1_set = None
    r2_set = None
    for i in range(0, 1):
        # Operation 1 -- Ends
        if measure.highestTime != timeSig.barDuration.quarterLength:
            d1 = music21.duration.Duration(timeSig.barDuration.quarterLength - measure.highestTime)
            r1 = music21.note.Rest()
            r1.duration = d1
            r1_set = r1
        #Operation 2 -- Beginnings
        if measure.lowestOffset != 0:
            d2 = music21.duration.Duration(measure.lowestOffset - 0)
            r2 = music21.note.Rest()
            r2.duration = d2
            r2_set = r2
        if inPlace is True:
            if r1_set is not None:
                measure.append(r1_set)
            else:
                pass
            if r2_set is not None:
                measure.insert(0, r2_set)
            else:
                pass
            return measure
        elif inPlace is False:
            if r1_set is not None:
                new_measure.append(r1_set)
            else:
                pass
            if r2_set is not None:
                new_measure.insert(0, r2_set)
            else:
                pass
            return new_measure


def empty_measure(timeSig="4/4"):
    """
        This simple call creates an empty measure whose entire duration is filled with a rest object and which possesses
    a music21.ElementWrapper(obj =" ") with string " " as its object. Used for musicode purposes when calling for a
    space in a musicode translation.

    :param timeSig:     String indicating the time signature denoted as '4/4', '3/4', etc.
    :return:            Returns the created empty measure.
    """
    time = music21.meter.TimeSignature(timeSig)
    space_wrapper = music21.ElementWrapper(obj=" ")
    space_measure = music21.stream.Measure()
    d1 = music21.duration.Duration(time.barDuration.quarterLength) #Correct rest duration for different timesigs  scenarios.
    rest = music21.note.Rest()
    rest.duration = d1
    space_measure.append(rest)
    space_measure.append(space_wrapper)
    return space_measure

#TODO Add keysignature.
def add_timesig_and_metronome(in_stream, bpm=120, timesig="4/4"):
    tempo = music21.tempo.MetronomeMark(number=bpm)
    tempo.priority = -2
    in_stream.insert(0, tempo)
    time_sig = music21.meter.TimeSignature(value=timesig)
    time_sig.priority = -1
    in_stream.insert(0, time_sig)
    return in_stream


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
    So the y index of the matrix will be subtracted from 128. (127?)

    :param in_stream: 			music21.Stream object
    :param cell_note_size:      note duration that each cell/pixel represents
    :return: 				    np.array
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

    :param matrix: 	            npArray of shape (x, 128) with only possible values of 1 and 0.
    :param connect:             Connect adjacent cells of the matrix into a single longer note in the stream
    :param cells_per_qrtrnote:  number of pixels/cells per quarter note
    :return:                    music21 stream
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



def about_midas():
    a_s = '-----Welcome to MIDAS, the MIDI-Intermediary Digital Art Suite.-----\n\n'
    a_0 = '     Your Visual Music GUI and Toolkit.\n'
    a_1 = '     Using knowledge and techniques of python, music21, numpy, opencv-python, open3d, vtk, mayavi, and pyo, this gui toolkit provides a musical engineer \n'
    a_2 = 'with the ability to transform text, images, and point clouds into musical data for composing, production and visualization purposes. \n'
    a_3 = 'MIDAS incorporates strong musicological analyses displays as well as grants the user the ability to rapidly manipulate their musical data via \n'
    a_4 = 'a unique, simple user interface and input\output methods to and from other programs such as FL Studio, MuseScore, NotePad++, Word, Paint\PicPick, Meshlab, and even Blender. \n'
    a_5 = '     The MIDAS installation possesses a path called "intermediary_path" assigned as a variable, and this path is the traffic hub for said data manipulation; the transformation and manipulation \n'
    a_6 = 'of all files and data that go through this toolkit ideally will use the "intermediary_path". This path is established for ease of using this embedded \n'
    a_7 = 'python interpreter and it can be assigned as an output for all your other programs. \n'
    a_8 = '     Since Midas focuses heavily on musical data, its primary input\\output filetype is a .mid midi file. Midas does possess the ability, however, \n'
    a_9 = 'to do input and output of .txt, .jpg, .png, and .ply file types. Using all these in conjunction with intermediary_path and a developing library of Midas tools, creativity via rapid development and production \n'
    a_10 = 'of Visual Music is now in your hands.  \n\n'

    a_11 = '----We hope you enjoy MIDAS.----\n'

    about = str(a_s + a_1 + a_2 + a_3 + a_4 + a_5 + a_6 + a_7 + a_8 + a_9 + a_10 + a_11)
    print(about)
    return about


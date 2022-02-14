# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# Name:         musicode.py
# Purpose:      This is the main file for musicode classes and utilities
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    musicode is Copyright © 2017-2019 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-19 Michael Scott Cuthbert and the music21
#               Project
# License:      LGPL or BSD, see license.txt
#------------------------------------------------------------------------------------
#
# TABLE OF CONTENTS
#Instructions: Highlight "#Tr-1." and press ctrl F. Then use the next\previous arrows to bounce around the .py quickly.

#MUSIC_FUNCTIONS--------------------------
# A. B. C.----------

####### A.
##TRANSPOSE_FUNCTIONS
#-----------------------------
#Tr-1.  def TRANSPOSE_MEASURE(in_stream, measure_number, degree)
#Tr-2.  def TRANSPOSE_ALL_MEASURES_BY_RANDOM(in_stream)
#Tr-3.  def TRANSPOSE_MEASURES_BY_LETTERS(in_stream, letters, degree)
#Tr-4.  def TRANSPOSE_NOTES_BY_RANDOM(in_stream, measure_range_low, measure_range_high, interval_lower_limit, interval_upper_limit)
#Tr-5.  def TRANSPOSE_CHORD_IN_KEY(in_chord, int_num, key)
#Tr- TODO


####### B.
##MODIFICATION_FUNCTIONS
#--------------------------------
#M-1.   def ALTER_MEASURE_OFFSET(in_stream, range_l, range_h, offset_number)
#M-2.   def ALTER_MEASURE_DURATION(in_stream, in_stream, range_l, range_h, duration_len)
#M-3.   def STRETCH_BY_MEASURE(in_stream, range_l, range_h, ratio)
#M-4.   def ARPEGGIATE_CHORDS_IN_STREAM(in_stream, arp_factor)
#TODO M-5. REPLACE_CHORDS()
#M-6. CHOP_UP_NOTES(stream, offset_interval)
#TODO M-7 MAKE_CONTIGUOUS_NOTES()


####### C.
##SYNTHESIS_FUNCTIONS
#-----------------------------
#Syn-1. def SET_CHORD_OCTAVE(in_chord, octave)
#Syn-2. def MAKE_CHORD_FROM_NOTE(in_stream, in_chord, inv)
#Syn-3. def MAKE_CHORD_FROM_NOTE_2(in_stream, in_chord, inv)


##UNIDIART_FUNCTIONS
#-------------------
#UA-1.  def TRANSLATE(musicode, string)
#UA-2.  def TRANSLATE_FROM_TEXT_FILE(musicode, filename)
#UA-3.  def TRANSLATE_LETTER(c, musicode, num) ???
#UA-4.  def TRANSLATE_EACH_LETTER_TO_RANDOM_MUSICODE(text)
#UA-5.  def ALIGN_MUSICODE_WITH_MELODY(melody_stream, musicode)
#TODO UA-6.   def CHANGE_MUSICODE


##MIDIART_FUNCTIONS
#------------------
#MA-1.  def PRINT_CHORDS_IN_PIECE(stream)
#MA-2.  def MAKE_MIDI_FROM_PIXELS(pixels, granularity, connect, keychoice)
#MA-3. TODO def MAKE_PIXELS_FROM_MIDI()
#MA-4.  def STRIP_MIDI_BY_CHORDS(stream, directory)
#MA-5.  def STRIP_MIDI_BY_PITCHRANGE(stream, directory, range_l, range_h)
#MA-6.  def STAGGER_PITCH_RANGE(in_stream, stepsize=1, ascending=True, starting_offset=None, range_l=0, range_h=128)
#MA-7. TODO def STAGGER_OFFSET_RANGE()
#MA-8.  def TRANSCRIBE_IMAGE_TO_MIDIART(img, height, granularity, midi_path, connect, keychoice=None)
#MA-9.  def TRANSCRIBE_IMAGE_EDGES_TO_MIDIART((self, img, height, granularity, midi_path, connect, keychoice=None)
#MA-10. def EXTRACT_SUB_MELODIES(stream, keep_dur=False, chop_durs=False, offset_interval=0.25)
#MA-11. TODO Revise? def GET_RANDOM_MELODY(in_stream)
#MA-
#MA-
#MA-


##3IDIART_FUNCTIONS
#------------------
#3D-1.  def EXTRACT_XYZ_COORDINATES_TO_ARRAYself, in_stream)
#3D-2.  def EXTRACT_XYZ_COORDINATES_TO_STREAM(self, coords_array)
#3D-3.  def INSERT_INSTRUMENT_INTO_PARTS(self, in_stream, midi_num=0)
#3D-4.  def PARTITION_INSTRUMENTS_BY_RANDOM(self, in_stream)
#3D-5.  def ROTATE_POINT_ABOUT_AXIS(self, x, y, z, axis, degrees)
#3D-6.  def ROTATE_ARRAY_POINTS_ABOUT_AXIS(self, points, axis, degrees)
#3D-7.  def GET_POINTS_FROM_PLY(file_path, height)
#3D-8.  def WRITE_POINTS_FROM_PLY(self, coords_array, file_path):
#3D-9.  def DELETE_REDUNDANT_POINTS(self, coords_array, stray=True):
#3D-10. def DELETE_SELECT_POINTS(self, coords_array, choice_list)
#3D-11. def ARRAY_TO_LISTS_OF(self, coords_array, tupl=True)
#3D-12. def LISTS_OF_TO_ARRAY(self, list)
#3D-13. def GET_PLANES_ON_AXIS(self, coords_array, axis="z")

##MUSIC21_FUNCTIONS\CLASSES (NEW ONES)
#(to be done at MIT?)
#-------------------------------------
#M21-1. def DELETE_REDUNDANT_NOTES(self, in_stream, force_sort=False)
#M21-2. def NOTAFY(in_stream)
#M21-3. def SEPARATE_NOTES_TO_PARTS_BY_VELOCITY(self, in_stream)
#M21-4. def SET_STREAM_VELOCITIES(self, in_stream, vel)
#M21-5. def CHANGE_VELOCITIES_BY_RANGELIST(in_stream, volume_list)
#M21-. TODO music21.clash.Clash() A music21 object for housing multiple notes of same pitch and offset with different velocities.
    # Similar to music21.chord.Chord. (redundant, might use stream.Parts instead for simplicity)
#M21-. TODO  MUSIC21.CONVERTER.PARSE(notafy=True)


##GUI_FUNCTIONS (Generally Private)
#----------------------------------
#GUI-1. def _STREAM_TO_MATRIX(self, stream)
#GUI-2. def _MATRIX_SET_NOTES(self, matrix, y, x_start, x_end)
#GUI-3. def _MATRIX_TO_STREAM(self, matrix, connect, cell_note_size)


#DEMO_FUNCTIONS
#--------------
#D-1.   def DEMO_1(self, text_file)

########################################################################################################################

from music21 import *
import g
import re
import os
import copy
import random
import numpy

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Musicode:


    def __init__(self):
        self._setup_midi_dictionaries()
        #if not g.musicode_path:


    # The path to the top level of Musicode midi Libraries
    #musicode_path = r"Z:\10_Musicode_Libraries"
    #musicode_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\10_Musicode_Libraries"
    #musicode_path = r"C:\Users\Isaac's\Desktop\MIDAS Old Shit\The Musicode Project-20180203T204228Z-001\musicode\Kivy\musicode_libraries"
    musicode_path = r".\musicode_libraries"
    #musicode_path = r"C:\Users\iplovanic\Desktop\10_Musicode Libraries"
    #musicode_path = r"C:\Users\iplovanic\Desktop\MIDAS\10_Musicode_Libraries"

    am_dict = dict() #Animuse dictionary
    asciiX_dict = dict()  #Asciipher dictionary
    asciiY_dict = dict()  #Asciipher dictionary
    bp_dict = dict() #BraillePulse dictionary
    mm_dict = dict() #Metamorse dictionary
    ptX_dict = dict() #POWerTap_X dictionary
    ptY_dict = dict() #POWerTap_Y dictionary
    se_dict = dict() #Script-Ease dictionary
    splyce_dict = dict() #Splyce dictionary
    boX_dict = dict() # Baud-Onkadonk dictionary
    boY_dict = dict() # Baud-Onkadonk dictionary

    shorthand = {
                 "Animuse"        : "am",
                 "Asciipher_X"    : "asciiX",
                 "Asciipher_Y"    : "asciiY",
                 "BraillePulse"   : "bp",
                 "MetaMorse"      : "mm",
                 "POWerTap_X"     : "ptX",
                 "POWerTap_Y"     : "ptY",
                 "Script-Ease"    : "se",
                 "Splyce"         : "splyce",
                 "Baud-Onkadonk_X": "boX",
                 "Baud-Onkadonk_Y": "boY",
                 }
    #"Baud-Onkadonk_X     : "bo_X",
    #"Baud-Onkadonk_Y       : "bo_Y",
    dictionaries = {
                 "Animuse"        : am_dict,
                 "Asciipher_X"    : asciiX_dict,
                 "Asciipher_Y"    : asciiY_dict,
                 "BraillePulse"   : bp_dict,
                 "MetaMorse"      : mm_dict,
                 "POWerTap_X"     : ptX_dict,
                 "POWerTap_Y"     : ptY_dict,
                 "Script-Ease"    : se_dict,
                 "Splyce"         : splyce_dict,
                 "Baud-Onkadonk_X" : boX_dict,
                 "Baud-Onkadonk_Y" : boY_dict,
                }
#"Baud-Onkadonk_X      : boX_dict"
#"Baud-Onkadonk_Y      : boY_dict"

    def add_to_dict(self, char, musicode, full_path_to_file):
        """
        Making this function public in case someone wants to modify the dicts
        :param dict:
        :param full_path_to_file:
        :return:
        """
        import music21
        #print("Importing: %s" % full_path_to_file)
        m = stream.Measure()
        w = music21.ElementWrapper("".join([musicode, " : ", char]))
        te = music21.expressions.TextExpression(char)
        te.style.fontSize = 18
        te.style.absoluteY = 40
        te.style.alignHorizontal = 'center'

        m.append(w)
        m.append(te)
        m.duration = duration.Duration(4.0)
        imported_mid = converter.parse(full_path_to_file)
        si = imported_mid.flat.notesAndRests
        #insert notes into new measure
        for el in si:
            m.insert(el)
        #insert rest to fill up remainder of measure
        if (m.highestTime < 4):
            rest = note.Rest(quarterLength=(4-m.highestTime))
            m.append(rest)
        self.dictionaries[musicode][char] = m


    def _setup_midi_dictionaries(self):
        self._setup_am_dict()
        self._setup_asciiX_dict()
        self._setup_asciiY_dict()
        self._setup_bp_dict()
        self._setup_mm_dict()
        self._setup_ptX_dict()
        self._setup_ptY_dict()
        self._setup_splyce_dict()
        self._setup_se_dict()
        self._setup_boX_dict()
        self._setup_boY_dict()

    def _setup_letters_and_numbers(self, musicode):
        sh = self.shorthand.get(musicode)
        mdict = self.dictionaries[musicode]
        for pack in ("Lowercase", "Uppercase", "Numbers"):
            directory = self.musicode_path + "\\" + musicode + "\\" + sh + "_" + pack
            filenames = next(os.walk(directory))[2]
            for file in filenames:
                my_search = re.search(r"musicode_%s_(\w|\number).mid"% sh, file)
                if my_search:
                    self.add_to_dict(my_search.group(1), musicode, directory+"\\"+file)
        # Add a measure of rest for the space character (' ')
        r = stream.Measure()
        r.duration = duration.Duration(4.0)
        rest = note.Rest(quarterLength=4.0)
        r.insert(rest)
        mdict[' '] = r
    #end _setup_letters_and_numbers()

    def _setup_am_dict(self):
        self._setup_letters_and_numbers("Animuse")
        punct_dir = self.musicode_path + "\\Animuse\\am_Punctuation\\"
        self.add_to_dict("/", "Animuse", "".join([punct_dir, "musicode_am_forwardslash.mid"]))
        self.add_to_dict("]", "Animuse", "".join([punct_dir, "musicode_am_closebracket.mid"]))
        self.add_to_dict(")", "Animuse", "".join([punct_dir, "musicode_am_closeparenthesis.mid"]))
        self.add_to_dict(":", "Animuse", "".join([punct_dir, "musicode_am_colon.mid"]))
        self.add_to_dict(",", "Animuse", "".join([punct_dir, "musicode_am_comma.mid"]))
        self.add_to_dict('\"', "Animuse", "".join([punct_dir, "musicode_am_doublequotationmark.mid"]))
        self.add_to_dict("!", "Animuse", "".join([punct_dir, "musicode_am_exclamationmark.mid"]))
        self.add_to_dict("-", "Animuse", "".join([punct_dir, "musicode_am_hyphen.mid"]))
        self.add_to_dict("[", "Animuse", "".join([punct_dir, "musicode_am_openbracket.mid"]))
        self.add_to_dict("(", "Animuse", "".join([punct_dir, "musicode_am_openparenthesis.mid"]))
        self.add_to_dict(".", "Animuse", "".join([punct_dir, "musicode_am_period.mid"]))
        self.add_to_dict(";", "Animuse", "".join([punct_dir, "musicode_am_semicolon.mid"]))
        self.add_to_dict("\'", "Animuse", "".join([punct_dir, "musicode_am_singlequotationmark.mid"]))
        self.add_to_dict("?", "Animuse", "".join([punct_dir, "musicode_am_questionmark.mid"]))


    def _setup_se_dict(self):
        self._setup_letters_and_numbers( "Script-Ease")
        punct_dir = self.musicode_path + "\\Script-Ease\\se_Punctuation\\"
        self.add_to_dict("/", "Script-Ease", "".join([punct_dir, "musicode_se_forwardslash.mid"]))
        self.add_to_dict("]", "Script-Ease", "".join([punct_dir, "musicode_se_closebracket.mid"]))
        self.add_to_dict(")", "Script-Ease", "".join([punct_dir, "musicode_se_closeparenthesis.mid"]))
        self.add_to_dict(":", "Script-Ease", "".join([punct_dir, "musicode_se_colon.mid"]))
        self.add_to_dict(",", "Script-Ease", "".join([punct_dir, "musicode_se_comma.mid"]))
        self.add_to_dict('\"', "Script-Ease", "".join([punct_dir, "musicode_se_doublequotationmark.mid"]))
        self.add_to_dict("!", "Script-Ease", "".join([punct_dir, "musicode_se_exclamationmark.mid"]))
        self.add_to_dict("-", "Script-Ease", "".join([punct_dir, "musicode_se_hyphen.mid"]))
        self.add_to_dict("[", "Script-Ease", "".join([punct_dir, "musicode_se_openbracket.mid"]))
        self.add_to_dict("(", "Script-Ease", "".join([punct_dir, "musicode_se_openparenthesis.mid"]))
        self.add_to_dict(".", "Script-Ease", "".join([punct_dir, "musicode_se_period.mid"]))
        self.add_to_dict(";", "Script-Ease", "".join([punct_dir, "musicode_se_semicolon.mid"]))
        self.add_to_dict("\'", "Script-Ease", "".join([punct_dir, "musicode_se_singlequotationmark.mid"]))
        self.add_to_dict("?", "Script-Ease", "".join([punct_dir, "musicode_se_questionmark.mid"]))

    def _setup_asciiX_dict(self):
        self._setup_letters_and_numbers( "Asciipher_X")
        punct_dir = self.musicode_path + "\\Asciipher_X\\asciiX_Punctuation\\"
        self.add_to_dict("\'", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_singlequotationmark.mid"]))
        self.add_to_dict("/", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_forwardslash.mid"]))
        self.add_to_dict("]", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_closebracket.mid"]))
        self.add_to_dict(")", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_closeparenthesis.mid"]))
        self.add_to_dict(":", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_colon.mid"]))
        self.add_to_dict(",", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_comma.mid"]))
        self.add_to_dict("!", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_exclamationmark.mid"]))
        self.add_to_dict("-", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_hyphen.mid"]))
        self.add_to_dict("[", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_openbracket.mid"]))
        self.add_to_dict("(", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_openparenthesis.mid"]))
        self.add_to_dict('\"', "Asciipher_X", "".join([punct_dir, "musicode_asciiX_doublequotationmark.mid"]))
        self.add_to_dict(".", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_period.mid"]))
        self.add_to_dict(";", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_semicolon.mid"]))
        self.add_to_dict("?", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_questionmark.mid"]))# HDXF TGHS,M

    def _setup_asciiY_dict(self):
        self._setup_letters_and_numbers( "Asciipher_Y")
        punct_dir = self.musicode_path + "\\Asciipher_Y\\asciiY_Punctuation\\"
        self.add_to_dict("\'", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_singlequotationmark.mid"]))
        self.add_to_dict("/", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_forwardslash.mid"]))
        self.add_to_dict("]", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_closebracket.mid"]))
        self.add_to_dict(")", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_closeparenthesis.mid"]))
        self.add_to_dict(":", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_colon.mid"]))
        self.add_to_dict(",", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_comma.mid"]))
        self.add_to_dict("!", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_exclamationmark.mid"]))
        self.add_to_dict("-", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_hyphen.mid"]))
        self.add_to_dict("[", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_openbracket.mid"]))
        self.add_to_dict("(", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_openparenthesis.mid"]))
        self.add_to_dict('\"', "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_doublequotationmark.mid"]))
        self.add_to_dict(".", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_period.mid"]))
        self.add_to_dict(";", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_semicolon.mid"]))
        self.add_to_dict("?", "Asciipher_Y", "".join([punct_dir, "musicode_asciiY_questionmark.mid"]))

    def _setup_bp_dict(self):
        self._setup_letters_and_numbers( "BraillePulse")
        punct_dir = self.musicode_path + "\\BraillePulse\\bp_Punctuation\\"
        self.add_to_dict("\'", "BraillePulse", "".join([punct_dir, "musicode_bp_singlequotationmark.mid"]))
        self.add_to_dict("/", "BraillePulse", "".join([punct_dir, "musicode_bp_forwardslash.mid"]))
        self.add_to_dict(":", "BraillePulse", "".join([punct_dir, "musicode_bp_colon.mid"]))
        self.add_to_dict(",", "BraillePulse", "".join([punct_dir, "musicode_bp_comma.mid"]))
        self.add_to_dict(".", "BraillePulse", "".join([punct_dir, "musicode_bp_decimalpoint.mid"]))
        self.add_to_dict("!", "BraillePulse", "".join([punct_dir, "musicode_bp_exclamationmark.mid"]))
        self.add_to_dict("-", "BraillePulse", "".join([punct_dir, "musicode_bp_hyphen.mid"]))
        self.add_to_dict("(", "BraillePulse", "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
        self.add_to_dict(")", "BraillePulse", "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
        self.add_to_dict("[", "BraillePulse", "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
        self.add_to_dict("]", "BraillePulse", "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
        self.add_to_dict('\"', "BraillePulse", "".join([punct_dir, "musicode_bp_doublequotationmark.mid"]))
        self.add_to_dict(".", "BraillePulse", "".join([punct_dir, "musicode_bp_period.mid"]))
        self.add_to_dict(";", "BraillePulse", "".join([punct_dir, "musicode_bp_semicolon.mid"]))
        self.add_to_dict("?", "BraillePulse", "".join([punct_dir, "musicode_bp_questionmark.mid"]))

    def _setup_mm_dict(self):
        self._setup_letters_and_numbers( "MetaMorse")
        punct_dir = self.musicode_path + "\\MetaMorse\\mm_Punctuation\\"
        self.add_to_dict("/", "MetaMorse", "".join([punct_dir, "musicode_mm_forwardslash.mid"]))
        self.add_to_dict("]", "MetaMorse", "".join([punct_dir, "musicode_mm_closebracketparenthesis.mid"]))
        self.add_to_dict(")", "MetaMorse", "".join([punct_dir, "musicode_mm_closebracketparenthesis.mid"]))
        self.add_to_dict(":", "MetaMorse", "".join([punct_dir, "musicode_mm_colon.mid"]))
        self.add_to_dict(",", "MetaMorse", "".join([punct_dir, "musicode_mm_comma.mid"]))
        self.add_to_dict('\"', "MetaMorse", "".join([punct_dir, "musicode_mm_doublequotationsmark.mid"]))
        self.add_to_dict("!", "MetaMorse", "".join([punct_dir, "musicode_mm_exclamationmark.mid"]))
        self.add_to_dict("-", "MetaMorse", "".join([punct_dir, "musicode_mm_hyphen.mid"]))
        self.add_to_dict("[", "MetaMorse", "".join([punct_dir, "musicode_mm_openbracketparenthesis.mid"]))
        self.add_to_dict("(", "MetaMorse", "".join([punct_dir, "musicode_mm_openbracketparenthesis.mid"]))
        self.add_to_dict(".", "MetaMorse", "".join([punct_dir, "musicode_mm_period.mid"]))
        self.add_to_dict(";", "MetaMorse", "".join([punct_dir, "musicode_mm_semicolon.mid"]))
        self.add_to_dict("\'", "MetaMorse", "".join([punct_dir, "musicode_mm_singlequotationmark.mid"]))
        self.add_to_dict("?", "MetaMorse", "".join([punct_dir, "musicode_mm_questionmark.mid"]))

    def _setup_ptX_dict(self):
        self._setup_letters_and_numbers( "POWerTap_X")
        punct_dir = self.musicode_path + "\\POWerTap_X\\ptX_Punctuation\\"
        self.add_to_dict("/", "POWerTap_X", "".join([punct_dir, "musicode_ptX_forwardslash.mid"]))
        self.add_to_dict(":", "POWerTap_X", "".join([punct_dir, "musicode_ptX_colon.mid"]))
        self.add_to_dict(",", "POWerTap_X", "".join([punct_dir, "musicode_ptX_comma.mid"]))
        self.add_to_dict('\"', "POWerTap_X", "".join([punct_dir, "musicode_ptX_doublequotationmark.mid"]))
        self.add_to_dict("!", "POWerTap_X", "".join([punct_dir, "musicode_ptX_exclamationmark.mid"]))
        self.add_to_dict("-", "POWerTap_X", "".join([punct_dir, "musicode_ptX_hyphen.mid"]))
        self.add_to_dict("[", "POWerTap_X", "".join([punct_dir, "musicode_ptX_openclosebracket.mid"]))
        self.add_to_dict("]", "POWerTap_X", "".join([punct_dir, "musicode_ptX_openclosebracket.mid"]))
        self.add_to_dict("(", "POWerTap_X", "".join([punct_dir, "musicode_ptX_opencloseparenthesis.mid"]))
        self.add_to_dict(")", "POWerTap_X", "".join([punct_dir, "musicode_ptX_opencloseparenthesis.mid"]))
        self.add_to_dict(".", "POWerTap_X", "".join([punct_dir, "musicode_ptX_period.mid"]))
        self.add_to_dict(";", "POWerTap_X", "".join([punct_dir, "musicode_ptX_semicolon.mid"]))
        self.add_to_dict("\'", "POWerTap_X", "".join([punct_dir, "musicode_ptX_singlequotationmark.mid"]))
        self.add_to_dict("?", "POWerTap_X", "".join([punct_dir, "musicode_ptX_questionmark.mid"]))

    def _setup_ptY_dict(self):
        self._setup_letters_and_numbers( "POWerTap_Y")
        punct_dir = self.musicode_path + "\\POWerTap_Y\\ptY_Punctuation\\"
        self.add_to_dict("/", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_forwardslash.mid"]))
        self.add_to_dict(":", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_colon.mid"]))
        self.add_to_dict(",", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_comma.mid"]))
        self.add_to_dict('\"', "POWerTap_Y", "".join([punct_dir, "musicode_ptY_doublequotationmark.mid"]))
        self.add_to_dict("!", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_exclamationmark.mid"]))
        self.add_to_dict("-", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_hyphen.mid"]))
        self.add_to_dict("[", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_openclosebracket.mid"]))
        self.add_to_dict("]", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_openclosebracket.mid"]))
        self.add_to_dict("(", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_opencloseparenthesis.mid"]))
        self.add_to_dict(")", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_opencloseparenthesis.mid"]))
        self.add_to_dict(".", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_period.mid"]))
        self.add_to_dict(";", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_semicolon.mid"]))
        self.add_to_dict("\'", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_singlequotationmark.mid"]))
        self.add_to_dict("?", "POWerTap_Y", "".join([punct_dir, "musicode_ptY_questionmark.mid"]))

    def _setup_splyce_dict(self):
        self._setup_letters_and_numbers("Splyce")
        punct_dir = self.musicode_path + "\\Splyce\\splyce_Punctuation\\"
        self.add_to_dict("/", "Splyce", "".join([punct_dir, "musicode_splyce_forwardslash.mid"]))
        self.add_to_dict("]", "Splyce", "".join([punct_dir, "musicode_splyce_closebracket.mid"]))
        self.add_to_dict(")", "Splyce", "".join([punct_dir, "musicode_splyce_closeparenthesis.mid"]))
        self.add_to_dict(":", "Splyce", "".join([punct_dir, "musicode_splyce_colon.mid"]))
        self.add_to_dict(",", "Splyce", "".join([punct_dir, "musicode_splyce_comma.mid"]))
        self.add_to_dict('\"', "Splyce", "".join([punct_dir, "musicode_splyce_doublequotationmark.mid"]))
        self.add_to_dict("!", "Splyce", "".join([punct_dir, "musicode_splyce_exclamationmark.mid"]))
        self.add_to_dict("-", "Splyce", "".join([punct_dir, "musicode_splyce_hyphen.mid"]))
        self.add_to_dict("[", "Splyce", "".join([punct_dir, "musicode_splyce_openbracket.mid"]))
        self.add_to_dict("(", "Splyce", "".join([punct_dir, "musicode_splyce_openparenthesis.mid"]))
        self.add_to_dict(".", "Splyce", "".join([punct_dir, "musicode_splyce_period.mid"]))
        self.add_to_dict(";", "Splyce", "".join([punct_dir, "musicode_splyce_semicolon.mid"]))
        self.add_to_dict("\'", "Splyce", "".join([punct_dir, "musicode_splyce_singlequotationmark.mid"]))
        self.add_to_dict("?", "Splyce", "".join([punct_dir, "musicode_splyce_questionmark.mid"]))

    #TODO Baud-Onkadonk
    def _setup_boX_dict(self):
        self._setup_letters_and_numbers("Baud-Onkadonk_X")
        punct_dir = self.musicode_path + "\\Baud-Onkadonk_X\\boX_Punctuation\\"
        self.add_to_dict("/", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_forwardslash.mid"]))
        #self.add_to_dict("]", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_closebracket.mid"]))
        self.add_to_dict(")", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_closeparenthesis.mid"]))
        self.add_to_dict(":", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_colon.mid"]))
        self.add_to_dict(",", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_comma.mid"]))
        self.add_to_dict('\"', "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_doublequotationmark.mid"]))
        self.add_to_dict("!", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_exclamationmark.mid"]))
        self.add_to_dict("-", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_hyphen.mid"]))
        #self.add_to_dict("[", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_openbracket.mid"]))
        self.add_to_dict("(", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_openparenthesis.mid"]))
        self.add_to_dict(".", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_period.mid"]))
        self.add_to_dict(";", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_semicolon.mid"]))
        self.add_to_dict("\'", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_singlequotationmark.mid"]))
        self.add_to_dict("?", "Baud-Onkadonk_X", "".join([punct_dir, "musicode_boX_questionmark.mid"]))

    def _setup_boY_dict(self):
        self._setup_letters_and_numbers("Baud-Onkadonk_Y")
        punct_dir = self.musicode_path + "\\Baud-Onkadonk_Y\\boY_Punctuation\\"
        self.add_to_dict("/", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_forwardslash.mid"]))
        #self.add_to_dict("]", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_closebracket.mid"]))
        self.add_to_dict(")", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_closeparenthesis.mid"]))
        self.add_to_dict(":", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_colon.mid"]))
        self.add_to_dict(",", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_comma.mid"]))
        self.add_to_dict('\"', "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_doublequotationmark.mid"]))
        self.add_to_dict("!", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_exclamationmark.mid"]))
        self.add_to_dict("-", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_hyphen.mid"]))
        #self.add_to_dict("[", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_openbracket.mid"]))
        self.add_to_dict("(", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_openparenthesis.mid"]))
        self.add_to_dict(".", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_period.mid"]))
        self.add_to_dict(";", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_semicolon.mid"]))
        self.add_to_dict("\'", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_singlequotationmark.mid"]))
        self.add_to_dict("?", "Baud-Onkadonk_Y", "".join([punct_dir, "musicode_boY_questionmark.mid"]))

###########MUSIC_FUNCTIONS###########

##TRANSPOSE_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#Tr-1.
    def transpose_measure(self, in_stream, measure_number, degree):
        """
        :param stream: stream to loop through
        :param measureNumber: Number of the measure to transpose
        :param degree: integer degree (or interval) to transpose
        :return:
        """
        measures = in_stream.getElementsByClass(stream.Measure)
        for n in measures[measure_number].flat.notes:

            i = interval.GenericInterval(degree)
            n.show('txt')

            if n.isChord:
                for p in n.pitches:
                    p.transpose(i, inPlace=True)
                n.pitch.transpose(i, inPlace=True)

#Tr-2.
    def transpose_all_measures_by_random(self, in_stream):
        """
        Transposes all Measures in the music21 stream by a random interval 1-7
        Currently only transposes up in pitch.
        :params stream:  the music21 stream to perform transposing in
        :return:
        """
        import music21
        s=copy.deepcopy(in_stream)
        for m in s.getElementsByClass(stream.Measure):
            r = random.randint(1, 7)
            logger.debug("Random: %d", r)
            for n in m.flat.notes:
                i = interval.GenericInterval(r)
                #n.show('txt')
                if n.isChord:
                    for p in n.pitches:
                        p.transpose(i, inPlace=True)
                else:
                    n.pitch.transpose(i, inPlace=True)
        return s

#Tr-3.
    def transpose_measures_by_letters(self, in_stream, letters, degree):
        """
        :param in_stream: Translated musicode through which to loop.
        :param letter: All instances of single letter/letters/lists of letters to be transposed. 0 does not equal root C.
        :param degree: Degree of transposition.
        :return:
        """
        import music21
        measures = in_stream.getElementsByClass(stream.Measure)
        for m in measures:
            l = m.getElementsByClass(music21.ElementWrapper)
            if len(l._elements):
                if (l._elements[0].obj.split(":")[1].strip() in letters):
                    for n in m.flat.notes:
                        i = interval.GenericInterval(degree)
                        if n.isChord:
                            for p in n.pitches:
                                p.transpose(i, inPlace=True)
                        else:
                            n.pitch.transpose(i, inPlace=True)

#Tr-4.
    def transpose_notes_by_random(self, in_stream, measure_range_low, measure_range_high, interval_lower_limit, interval_upper_limit):
        """
        Transposes all Measures in the music21 stream by a random interval 1-7.
        Currently only transposes up in pitch.
        :params stream:  the music21 stream to perform transposing in
        :measure_num: the number of the measure in the stream where transposing will be done
        :interval_lower_limit:  lower limit of how far the random transpose can go
        :interval_upper_limit:  upper limit of how far the random transpose can go
        :return:
        """
        import music21
        for m in in_stream.getElementsByClass(stream.Measure):
            if (m.number >= measure_range_low and m.number <= measure_range_high):
                for n in m.flat.notes:
                    r = random.randint(interval_lower_limit, interval_upper_limit)
                    logger.info("Random: %d", r)
                    if (r != 0):
                        i = interval.GenericInterval(r)
                        # n.show('txt')
                        if n.isChord:
                            for p in n.pitches:
                                p.transpose(i, inPlace=True)

                        else:
                            n.pitch.transpose(i, inPlace=True)

#Tr-5.
    def transpose_chord_in_key(in_chord, int_num, key):
        """
        :param in_chord: User-introduced chord.
        :param intv_num: Generic interval(i.e 3=third, 7=seventh, etc.)
        :param key: Key to be specified.
        :param octave: Octave to be specified by an Int.
        :return: Returns ch = music21.chord.Chord(modified in_chord)
        """
        import music21
        i = music21.interval.GenericInterval(int_num)
        ch = music21.chord.Chord()
        k = music21.key.Key(key)
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
    def alter_measure_offset(self, in_stream, range_l, range_h, offset_number):
        """
        Alters all music21 object offsets in selected measure or range of measures.
        Calls makeMeasures(,inPlace=True) before finalizing.
        :param in_stream: Translated Musicode.
        :param range_l: Starting measure number to edit.
        :param range_h: Ending measure number up to which to edit.
        :param offset_number: Offset in quarter notes. (1 = One quarternote, Negative numbers and fractions are allowed.)
        :return: Stream
        """
        for m in in_stream.getElementsByClass(stream.Measure):
            if (m.number >= range_l and m.number <= range_h):
                for n in m.flat.notes:
                    m.setElementOffset(n, n.offset + offset_number)
        in_stream.makeMeasures()
        return in_stream

#M-2.
    def alter_measure_duration(self, in_stream, range_l, range_h, duration_len):
        """
        Alters all object durations in selected measures or range of measures.
        :param in_stream: Translated Musicode.
        :param range_l: Starting measure number to edit.
        :param range_h: Ending measure number up to which to edit.
        :param duration_len: Duration in quarterlength. (1 = one quarter note. Can do many division smaller than a quarter note. Negative numbers are allowed.)
        :return: Stream
        """
        for m in in_stream.getElementsByClass(stream.Measure):
            if (m.number >= range_l and m.number <= range_h):
                for n in m.flat.notes:
                    d = duration.Duration(duration_len)
                    n.duration = d
        in_stream.makeMeasures()
        return in_stream

#M-3. TODO NEEDS FIXING!!
    def stretch_by_measure(self, in_stream, range_l, range_h, ratio, stretchDurations=True):
        """
        :param in_stream:
        :param range_l:
        :param range_h:
        :param ratio:
        :return:
        """
        print("Ratio=")
        print(ratio)
        if in_stream.getElementsByClass(stream.Measure) is None:
            print("In function 'stretch_by_measure', in_stream has no measures. Cannot stretch.")
            return None
        temp = stream.Stream()
        m_num = 0
        l = list()
        for m in in_stream.getElementsByClass(stream.Measure):
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
                d = duration.Duration(n.duration.quarterLength * ratio)
                n.duration = d

        in_stream.insert(range_l*4, temp)
        print("in_stream before MakeMeasures")
        in_stream.show('txt')
        in_stream.makeMeasures(inPlace=True)

        print("in_stream after MakeMeasures")
        in_stream.show('txt')

        return in_stream

#M-4.
    def arpeggiate_chords_in_stream(self, in_stream, stepsize=1, ascending=True):
        """

        :param in_stream: In-stream.
        :param stepsise: Stepsise factor of arpeggiation of notes in found chords.
        :param starting_offset: Chord's starting offsets.
        :return: in_stream
        """
        s = g.mc.notafy(in_stream).flat
        newstream= stream.Stream()
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
    # #def replace_chord(self, in_stream, selected_chord, replacement_chord, inversion):
    #     """
    #
    #     :param in_stream: Stream over which to be iterated for chords.
    #     :param selected_chord: Iteration of one type of chord.
    #     :param replacement_chord: Chord type with which to replace selection of chord type.
    #     :param inversion: Inversion of replacement chords. (1-3 for triads, 1-4 for 7ths, etc.)

    #     :return:
    #     """

#M-6.
    def chop_up_notes(self, stream, offset_interval):
        new_stream = stream.Stream()
        for n in stream.flat.notes:
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
# TODO def make_contiguous_notes(self, in_stream, inPlace=True):
    # for l in in_stream.flat.notes:


##SYNTHESIS_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#Syn-1.
    def set_chord_octave(in_chord, octave):
        """
        :param in_chord: Chord object with pitches.
        :param octave: Octave of pitches in chord.
        :return: in_chord
        "NOTE: Only works well for triads and sevenths, chord bigger than one octave will not need this."
        """
        for p in in_chord.pitches:
            p._setOctave(octave)
        return in_chord

#Syn-2.
    def make_chord_from_note(in_stream, in_chord, inv):
        """
        :param in_stream: Stream with notes for changing.
        :param in_chord: Chord called to replace note.
        :param inv: Chord's inversion, if any.
        :return:
        """
        import music21
        import copy
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
    def make_chord_from_note_2(in_stream, in_chord, inv):
        """
        :param in_stream: Stream with notes for changing.
        :param in_chord: Chord called to replace note.
        :param inv: Chord's inversion, if any.
        :return:
        """
        import music21
        import copy
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


# UNIDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#UA-1.
    def translate(self, musicode, string):
        """
        Translates a string into a selected musicode.
        :param musicode: The musicode to translate into
        :param string: The string text to translate
        :return: music21 stream containing the translated text.
        """
        s = stream.Part()
        num = 0
        for c in string:
            new_measure = self._translate_letter(c, musicode, num)
            s.append(new_measure)
            num = num + 1
        return s

#UA-2.
    def translate_from_text_file(self, musicode, file_name):
        """
        Translates input from a text file.
        :param text: the file name
        :return: stream
        """
        # TODO: Find a way to add option to split each line of text into a different midi track
        import music21

        file = open(file_name, "r")
        s = stream.Part()
        num = 0
        line = 0
        ss = stream.Part()
        w = music21.ElementWrapper("Line: %d" % line)
        ss.insert(w)
        c = file.read(1)
        while c:
            if c == "\n":
                s.insert(ss)
                ss = stream.Part()
                line = line + 1
                w = music21.ElementWrapper("Line: %d " % line)
                ss.insert(w)
            else:
                new_measure = self._translate_letter(c, musicode, num)
                ss.append(new_measure)
                num = num + 1
            c = file.read(1)
        # for note in ss.flat.notes:
        #     note.show('txt')
        if (len(ss.flat.notes) != 0):
            s.insert(ss)
        return s

    # TODO def _translate_word

    # TODO def _translate_sentence

#UA-3.
    def _translate_letter(self, c, musicode, num):
        new_measure = stream.Measure()
        # m.show('txt')
        # print("letter:" + c + "\n")

        rt = (self.dictionaries[musicode].get(c))
        if rt:
            new_measure = copy.deepcopy(rt)
        else:
            new_measure = copy.deepcopy(self.dictionaries[musicode].get(" "))
        new_measure.number = num
        return new_measure

#UA-4.
    def translate_each_letter_to_random_musicode(self, text):
        """
        Translates the text into a stream where each letter is a random Musicode
        :param text: The text to be translated
        :return: stream
        """
        s = stream.Part()
        num = 0
        musicodes = list(self.dictionaries.keys())
        for c in text:
            musicode = musicodes[random.randint(0, len(musicodes) - 1)]
            new_measure = self._translate_letter(c, musicode, num)
            new_measure.number = num
            s.append(new_measure)
            num = num + 1
        return s

#UA-5.
    def align_musicode_with_melody(self, melody, musicode):
        import copy
        import music21
        s = music21.stream.Stream()

        m = 0
        musicode_measures = musicode.getElementsByClass(music21.stream.Measure)
        for n in melody.flat.notes:
            if m < len(musicode_measures):
                ms = music21.stream.Stream()
                copied_measure = copy.deepcopy(musicode_measures[m])
                # 1. Set musicode offset to match note offset.

                # 2. Set musicode duration to match note duration. Use stretch function.
                temp = music21.stream.Stream()
                for y in musicode_measures[m].flat.notes:
                    temp.insert(y)
                m_dur = temp.highestTime
                n_dur = float(n.quarterLength)

                ms.insert(0, copied_measure)
                copied_measure.number = 0

                ms.show('txt')
                new_measure = g.mc.stretch_by_measure(ms, 0, 0, (n_dur / (m_dur)))
                # print("cunt")
                new_measure.show('txt')
                # 3. Set musicode root notes pitch to match note pitch. Use transpose key aware.
                # A. Get interval between musicode root note pitch and current melody note's pitch.
                if type(new_measure.flat.notes[0]) is music21.chord.Chord:
                    p1 = new_measure.flat.notes[0].root()
                else:
                    p1 = new_measure.flat.notes[0]
                if type(n) is music21.chord.Chord:
                    print("Melody must be notes; it cannot be chords.")
                    return None
                else:
                    p2 = n
                i = music21.interval.notesToGeneric(p1, p2)
                # B. GET KEY.
                if len(melody.getKeySignatures()) != 1:
                    print("You have no key signature, or more than one.")
                    return None
                else:
                    k = melody.getKeySignatures()[0].asKey()
                # C. Tranapose Key aware all of new measure by THAT interval.
                for z in new_measure.flat.notes:
                    if type(z) is music21.note.Note:
                        i.transposePitchKeyAware(z.pitch, k, inPlace=True)
                    elif type(z) is music21.chord.Chord:
                        for p in z.pitches:
                            i.transposePitchKeyAware(p, k, inPlace=True)
                    else:
                        print("You fucked up. Type of z is wrong.")
                        print(type(z))
                    new_measure.show('txt')
                # 4. Insert into stream.
                s.insert(n.offset, new_measure)

            m = m + 1

        s.makeMeasures()
        return s

#UA-6.
    #def change_musicode(self, in_stream, musicode_sh?):


##MIDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#MA-1.
    def print_chords_in_piece(self, in_stream):
        import fractions
        from fractions import Fraction
        """Use .flat and .makeMeasures to acquire appropriate callable stream

        :param in_stream:
        :return:
        """
        ret_str = ""
        s = in_stream.chordify().flat.makeMeasures()
        ret_str += "[offset] [dur]   [pitches] : [common name]\n"
        for m in s.getElementsByClass(stream.Measure):
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

        print(ret_str)
        return ret_str

#MA-2.
    def make_midi_from_pixels(self, pixels, granularity, connect, keychoice=None, note_pxl_value=255, clrs=True):
        import copy
        from collections import OrderedDict
        """
        Make midi picture, b***h.  Black and white if Clrs=False. White = note, black = nothing.
        :param pixels: The 2D array of pixel values.  0=black, 255=white.  ---invert=True
        :param granularity: like the quarterlength thingy. 4=each 'pixel' is whole note, 2=halfnote, 1=quarternote, 0.5=eighthnote,etc.
        :return: stream
        """
        ##Establish input filters.
        if keychoice == "":
            keychoice = None
            keysig = None
        else:
            keysig = key.Key(keychoice)
        allowedPitches = list()
        print("Key is: ")
        print(keysig)
        if keychoice == None:
            allowedPitches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        elif (type(keysig) is key.Key):
            for p in scale.Scale.extractPitchList(keysig.getScale()):
                allowedPitches.append(p.pitchClass)
        print(allowedPitches)
        # if (pixels.ndim != 2) and clrs is False:
        #     print(r"You did it wrong!\n")
        #return None

        if len(pixels) > 127:
            print("Too big, asshole. Fix it\n")
            raise ValueError("The .png file size is too large.")
            return None

        #Establish variables.
        s_stream = stream.Stream()
        part_stream = stream.Stream()
        end_stream = stream.Stream()
        #note_list = list()
        #y_list = list()
        #x_list = list()
        # for y in range(0, len(pixels)):
        #     y_list.append(y)
        #     # print(n.pitch.midi)
        # for x in range(0, len(pixels[0])):
        #     x_list.append(x)
        #note_dict = OrderedDict.fromkeys(m for m in pixels2)
        #clrs_dict = OrderedDict.fromkeys(o for o in range(1, 17))
        #Create parts with names of FL clrs.keys().
        if clrs is True:
            clrs = {
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
            #pixels2 = g.mc.array_to_lists_of_2(pixels, tupl=True)
            #Create stream with parts and parts names.
            for k in clrs:
                parts1 = stream.Part()
                parts1.partsName = k
                part_stream.insert(0.0, copy.deepcopy(parts1))
        #Up to here works.
        #Dictionary sets(kills) your notes....use lists.
            #Get notes for the number of coordinate colors in im_array at specific offsets and pitches.
                  #for ex in note_dict.keys():
            #for t in pixels2:
            # if i == u:
                # note_dict[u] = n
                # print(note_dict)
            # print(note_list)
            # for d in note_list:
            #     print("D_offset", d.offset)
            for l in part_stream.getElementsByClass(stream.Part):
                #for x in note_list:
                #for c in pixels2:
                for y in range(0, len(pixels)):
                    for x in range(0, len(pixels[y])):
                        newpitch = pitch.Pitch()
                        newpitch.ps = 127 - y
                        #y_list.append(y)
                        n = note.Note(newpitch)
                        if n.pitch.pitchClass in allowedPitches:
                            n.offset = x
                            totalduration = granularity
                            d = duration.Duration()
                            d.quarterLength = totalduration
                            n.duration = d
                            #note_list.append(n)
                            for q in clrs:
                                if tuple(pixels[y][x].flatten()) == clrs[q] and q == l.partsName:   ##ex == clrs[q] and q == l.partsName:  ##if q.volume.velocity == l.partsName:
                                    l.insert(n.offset * granularity, copy.deepcopy(n))
                                else:
                                    pass
                end_stream.insert(l.offset, copy.deepcopy(l))
            print("Stream created.")
            #end_stream.show('txt')
            return end_stream    # part_stream.insert(offsetx * granularity, n)
        #Below here works.
        elif clrs is False:
            for y in range(0, len(pixels)):
                for x in range(0, len(pixels[y])):
                    if pixels[y][x] == note_pxl_value:
                        newpitch = pitch.Pitch()
                        newpitch.ps = 127 - y
                        n = note.Note(newpitch)
                        #n.pitch.midi = 127 - y
                        if (n.pitch.pitchClass in allowedPitches):
                            totalduration = granularity
                            offsetx = x
                            if connect and clrs is False:
                                while (x + 1) < len(pixels[y]) and pixels[y][x + 1] == note_pxl_value:
                                    totalduration = totalduration + granularity

                                    pixels[y][x + 1] = abs(note_pxl_value - 1)
                                    x = x + 1

                            d = duration.Duration()
                            d.quarterLength = totalduration
                            n.duration = d
                            s_stream.insert(offsetx * granularity, n)
            return s_stream

        # channels_dict = OrderedDict.fromkeys(b for b in range(1, 17))
        #  for i in channels_dict:
        #     for j in channels_dict[i]:

        # for y in range(0, len(pixels)):
        #     for x in range(0, len(pixels[y])):
        #         for u in note_dict:
        #             if pixels[y][x] == note_dict.keys:
        #                 n = note.Note()
        #                 n.pitch.midi = 127 - y
        #                 # el = music21.ElementWrapper(t)
        #                 if n.pitch.pitchClass in allowedPitches:
        #                     totalduration = granularity
        #                     offsetx = x
        #                     d = duration.Duration()
        #                     d.quarterLength = totalduration
        #                     n.duration = d
        #                     # n.append(el)
        #                     note_dict[u] = n
        #                 # note_list.append(n)

        # for k in velocity_set:
        #     parts1 = stream.Part()
        #     parts1.partsName = k
        #     part_stream.insert(0.0, copy.deepcopy(parts1))
        #     # print("Parts_Stream", part_stream)
        #     # part_stream.show('txt')
        #     # Insert notes of same velocity value into stream.Part of the same value name.
        # for s in part_stream.getElementsByClass(stream.Part):
        #     for q in in_stream.flat.notes:
        #         if q.volume.velocity == s.partsName:
        #             # print("ShowParts", s)
        #             s.insert(q.offset, copy.deepcopy(q))
        #             # print("PartswithNotes", s)
        #         else:
        #             # print("And this one?")
        #             pass
        #     # print("Did we reach this?")
        #     end_stream.insert(s.offset, copy.deepcopy(s))
        # return end_stream

        ###for q in s.flat.notes:
        # s.insert(offsetx * granularity, n)
        # print("ShowParts", s)
        # print("PartswithNotes", s)
        # else:
        # print("And this one?")
        # pass
        # print("Did we reach this?")

        # if connect:
        #     while (x + 1) < len(pixels[y]) and pixels[y][x + 1] == note_pxl_value:
        #         totalduration = totalduration + granularity
        #
        #         pixels[y][x + 1] = abs(note_pxl_value - 1)
        #         x = x + 1


        ##COLOR RESEARCH
        #NOTE: The variable "sparky" is maintained by python, so a file can be closed and reopened for
        #(wb)writing after finishing with (rb)reading. Implement into make_midi_from_pixels() or a
        # transcribe function for use with color thresholds.


        #Method--OLD Notes:

        ###Solve CV2 Rotation problem.
        # c_test = cv2.imread(r"C:\Users\Isaac's\Desktop\Pictures-Photos\Circle_Test.png")
        # c_rot = cv2.imread(r"C:\Users\Isaac's\Desktop\Pictures-Photos\Circle_Test-rot-90.png")
        # c2_rot = np.rot90(c_test, 1, (0,1))
        # c_rot == c2_rot
        ##Use np.flip() as well.


        ###Iterate for color tuples.
        # for i in blarg[0, 0]...... Fucking whatever gets us the color tuples.
        # for i in c_rot:
        #     for q in i:
        #         print(q)

        ###Establish thresholds with if statements....
        #   if tuple[0...1...2] (255, 255, 255) is >=< whatever threshold:
        #       fuck a duck.

        # NOTES: (are edges "extrapolated" or actually part of the cv2 read?)

        # NEW METHOD

###TODO Figure out threshold ranges. K-D Trees shit.
    def set_to_nn_colors(self, im_array, clrs=None, FL=True):
        import open3d
        import numpy
        import numpy as np
        import cv2
        #import vtk
        from musicode import g
        from collections import OrderedDict

        if FL:
            clrs = {
            1: (158, 209, 165),   # "Green"),
            2: (159, 211, 186),   # "Pale Green"),
            3: (161, 214, 208),   # "Teal"),
            4: (163, 202, 216),   #"Light Blue"),
            5: (165, 184, 219),   #"Blue"),
            6: (168, 167, 222),   #"Violet"),
            7: (188, 167, 222),   #"Purple"),
            8: (209, 167, 222),   #"Fuschia"),
            9: (221, 167, 214),   #"Pink"),
            10: (219, 165, 192),  #"Red"),
            11: (217, 163, 169),  #"Red-Orange"),
            12: (214, 175, 162),  #"Orange"),
            13: (212, 193, 160),  #"Orange-Yellow"),
            14: (209, 210, 158),  #"Yellow"),
            15: (189, 209, 158),  #"Yellow-Green"),
            16: (169, 209, 157)  #"Light-Green")
        }
        else:
            l_clrs = g.mc.array_to_lists_of(clrs)
            clrs = dict.fromkeys(b for b in range(len(l_clrs)))
            for cr in range(0, len(l_clrs)):
                for qv in l_clrs:
                    clrs[cr] = qv

        # REMOVE redundant points. (otherwise, the kd search will be a disaster.)
        #shift_cloud = im_array.reshape((-1, 3))
        #clean_cloud = g.mc.delete_redundant_points(shift_cloud)

        # Place operand coords_array into open3d point cloud.
        pcloud = open3d.geometry.PointCloud()
        p_lizt = list()
        for ix in range(1, len(clrs)):
            p_lizt.append(clrs[ix])
        p_array = np.array(p_lizt)
        pcloud.points = open3d.Vector3dVector(p_array)
        kd_tree = open3d.geometry.KDTreeFlann(pcloud)


        #work_cloud = g.mc.array_to_lists_of(clean_cloud)
        #for x in range(1, len(work_cloud)):
        im_list = list()
        for x in range(len(im_array)):
            for y in range(len(im_array[x])):
                im_dex = np.array(im_array[x][y], dtype=np.float64)
                #im_list.append(im_dex)
                #for i in im_list:
                k_idx_list = kd_tree.search_knn_vector_3d(im_dex, 1)
                index = k_idx_list[1][0] + 1
                im_array[x][y] = clrs[index]
                #work_array = np.array(work_cloud)
                #final_array = work_array.reshape(im_array.shape)
        #return final_array
        return im_array


        ##nparray.reshape((-1, 3))
        #Note:if we rip out coords\colors in order, and we put them back in order, we will get the original image back.
        #Reshape colors_array for iteration.
        #new_colors = np.reshape(im_array, (im_array.shape))

        ##(2, IntVector[2, 1], DoubleVector[3, 12])



        ###music21.midi.translate.midiTracksToStreams(midiTracks, ticksPerQuarter=None, quantizePost=True, inputM21=None,
        ##**keywords) Given a list of midiTracks, populate this Stream with a Part for each track.

    def set_parts_to_midi_channels(self, in_stream, fptf):
        #Create the operand .mid file from in_stream.
        in_stream.write('mid', fptf) #Include filename.mid in fptf.
        #Change stream to list of miditracks (if one wishes to view the data.
            ##Given a Stream, Score, Part, etc., that may have substreams
            ##(i.e., a hierarchy), return a list of MidiTrack objects.
        # midi_view1 = midi.translate.streamHierarchyToMidiTracks(in_stream, acceptableChannelList=None)
        # print(midi_view1)
        #Establish clrs_list for reference call.
        clrs_list = list()
        for i in range(1, 17):
            clrs_list.append(i)
        #Create music21.midi.MidiFile() object.
        sparky = midi.MidiFile()
        sparky.open(fptf, attrib='rb')
        sparky.tracks
        sparky.read()
        sparky.tracks
        # for i in range(1, len(sparky.tracks)):
        for j in clrs_list:
            if len(sparky.tracks) < 17:
                sparky.tracks[j-1].setChannel(j)
            elif len(sparky.tracks) > 16:
                print("Check your .mid File data. There may be an extra track at the beginning or another problem.")

            # if t < 17:
            #     t += 1
        sparky.close()
        sparky.open(fptf, attrib='wb')
        sparky.write()
        sparky.close()




    #End notes:
    #music21.converter.parse() ruins channel allocation?
    #Open file in FL Studio by drag opening in to channel rack or by file-->open fptf.
        #Drag opening maintains the colors, but does not separate the notes into separate tracks.
        #File->Open OR File->import midi file will separate the notes into channels by track. (there is a "create one channel per track" option, but it was malfunctioning at present.



    ###  # for j in in_stream.getElementsByClass(stream.Part):
    #     for q in clrs_list:
    #         if i == q:


    ###Set channel based on threshold ranges. With the midi file-writing feature


# 255, 255, 255 color grid coords_array?

# a = np.arange(0, 256, 1).reshape((256, 1))
# b = a
# c = b
# my255 = np.column_stack((a, b, c))

#MA-3.
    def make_pixels_from_midi(self, in_stream, color=[255, 255, 255], gran=16):
        """
        ....gran was originally 16, for whatever reason.
        :param in_stream:
        :return: numpy array
        """
        import music21
        import numpy as np
        # temp_stream = g.mc.notafy(in_stream)
        # volume-z_list = list()

        a = np.zeros((127, (int(in_stream.highestTime * gran)), 3))
        #b = np.zeros((127, int(in_stream.highestTime), 3))
        #b = np.rot90(a, 1, (0, 1))
        temp_stream = g.mc.notafy(in_stream)
        for n in temp_stream.flat.notes:
            # if xy.volume.velocity is None:
            #     print("There are no velocity values for these notes. Assign velocity values.")
            #     return None
            x = int(n.offset * gran)
            y = n.pitch.midi

            i = 0
            while i < n.duration.quarterLength * gran:
                a[y + i][x] = color    ### = 1
                while i != 126:
                    i += 1
        b = np.rot90(a, 2, (0, 1))
        c = np.fliplr(b)
        return c

        # im_list = list()
        # for i in a.flatten():
        #     if i == 0:
        #         im_list.append([0, 0, 0])
        #     elif i == 1:
        #         im_list.append([255, 255, 255])
        # im_array = np.array(im_list, dtype=np.float64, ndmin=3)
        # im_array.reshape(127, int(in_stream.highestTime * 16), 3)
        # return im_array

#MA-4.
    def strip_midi_by_chords(self, in_stream, directory):
        num = 0
        for m in in_stream.getElementsByClass(stream.Measure):
            for c in m.getElementsByClass(["Chord", "Note"]):
                temp = stream.Stream()
                temp_measure = stream.Measure()
                temp_measure.offset = m.offset
                temp_measure.number = m.number
                temp_measure.insert(c.offset, c)
                temp.insert(temp_measure.offset, temp_measure)
                print("---")
                temp.write("mid", directory + "\\" + repr(num) + ".mid" )
                num = num+1
				
#MA-5.
    def strip_midi_by_pitchrange(self, in_stream, range_l, range_h, directory=None):
        import copy
        num = 0
        temp_stream = stream.Stream()
        notelist = list()

        for m in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            #print("Measure ", repr(m.number))

                if type(m) is chord.Chord:
                    for p in m.pitches:
                        newnote = note.Note(p)
                        newnote.offset = m.offset
                        newnote.duration = m.duration
                        notelist.append(newnote)
                elif type(m) is note.Note:
                    notelist.append(m)

            # temp_measure = stream.Measure()
            # temp_measure.offset = m.offset
            # temp_measure.number = m.number

        for n in notelist:
            #print("Note midi value: ", repr(n.pitch.midi))
            if n.pitch.midi >= range_l and n.pitch.midi <= range_h:
                #print("inserting: m=", repr(m.measureNumber))
                #temp_measure.insert(n.offset, n)
                #print(" m.offset=",repr(m.offset),", m.num=",repr(m.measureNumber),", temp.offset=",repr(temp_measure.offset),", temp.num=",repr(temp_measure.measureNumber))


                temp_stream.insert(n.offset, copy.deepcopy(n))
        print("---")
        if directory is not None:
              temp_stream.makeMeasures()
              temp_stream.write("mid", directory + "\\" + repr(range_l) + "-" + repr(range_h) + ".mid")
        else:
              temp_stream.makeMeasures(inPlace=True)
              return temp_stream

#MA-6.
    def stagger_pitch_range(self, in_stream, stepsize=1, ascending=True, starting_offset=None, range_l=0, range_h=128):
        """

        :param in_stream: Input stream.
        :param stepsize: Quarter length of offset step for arpeggiation.
        :param ascending:  True = ascending appegiation, False = descending arpeggiation
        :param starting_offset: Default of none uses the starting offset of the first note of lowest pitch if ascending=True, or highest if ascending=False.
                                Otherwise, directly specify starting offset
        :param range_l:
        :param range_h:
        :return:
        """
        #Step Fucking 1
        import music21
        import copy
        notelist = list()
        #notelist2 = list()
        #in_stream = in_stream.makeMeasures()
        for c in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            if type(c) is chord.Chord:
                for p in c.pitches:
                    newnote1 = note.Note(p)
                    newnote1.offset = c.offset
                    newnote1.duration = c.duration
                    notelist.append(newnote1)
            elif type(c) is note.Note:
                notelist.append(c)
        #print("Notelist")
        for n in notelist:
            print(n)
        #Step Fucking 2: Starting Offset
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

        #print("start=%d" % start)
        # Step Fucking 3
        temp_stream = music21.stream.Stream()
        # temp_measure = stream.Measure()
        # temp_measure.offset = m.offset
        # temp_measure.number = m.number
        start_p = range_l if ascending else range_h
        stop_p = range_h if ascending else range_l
        step_p = 1 if ascending else -1

        for o in range(start_p, stop_p, step_p):
            notez = self.strip_midi_by_pitchrange(in_stream, o, o)
            if notez.flat.hasElementOfClass("Note"):  # if "notes" has actual notes in it:
                for l in notez.flat.notes:
                    #print(l)
                    new_note_offset = start + l.offset - notez[0].offset
                    temp_stream.insert(new_note_offset, copy.deepcopy(l))
                start = start + stepsize
        temp_stream.makeMeasures(inPlace=True)
        return temp_stream

#MA-7. TODO
    # def stagger_offset_range():


#MA-8.
    #TODO Rework and re-partition into separate functions, also clean up both "image" and "edges" functions.
    def transcribe_image_to_midiart(self, im_path, midi_path, granularity, connect, keychoice=None, note_pxl_value=255, clrs=False, write=False):
        import cv2
        import numpy
        if type(im_path) == numpy.ndarray and im_path.ndim == 2:
            img = im_path
        elif type(im_path) == str:
            img = cv2.imread(im_path, 0)
        else:
            print("Not a filepath or numpy array.")
            return None
        if clrs is False:
            for x in range(0, len(img)):
                for y in range(0, len(img[x])):
                    if img[x][y] != 255:
                        img[x][y] = 0
        # np.set_printoptions(threshold=np.inf)
        print(img)
        if len(img) > 127:
            print("Too big, asshole. Fix it\n")
            raise ValueError("The .png file size is too large.")
        s = g.mc.make_midi_from_pixels(img, granularity, connect, keychoice, note_pxl_value, clrs)
        if write == True:
            s.write('mid', midi_path)
        else:
            pass
        return s

#MA-9.
    def transcribe_image_edges_to_midiart(self, image_path, height, granularity, midi_path, connect, keychoice=None, note_pxl_value=255, clrs=False):
        import cv2
        import numpy
        if type(image_path) == numpy.ndarray:
            img = image_path
            small = cv2.resize(image_path, (int(height / len(img) * len(img[0])), height), cv2.INTER_AREA)
        elif type(image_path) == str:
            #If a file path,
            img = cv2.imread(image_path, 0)
            small = cv2.resize(img, (int(height / len(img) * len(img[0])), height), cv2.INTER_AREA)
        edges = cv2.Canny(small, 100, 200)
        s = g.mc.make_midi_from_pixels(edges, granularity, connect, keychoice, note_pxl_value, clrs)
        s.write('mid', midi_path)
        return s

#MA-10.
    def extract_sub_melodies(self, stream, keep_dur=False, chop_durs=False, offset_interval=0.25):
    # """
    #keep_dur: If true, notes longer than offset interval will be chopped up into
    #individual notes of duration = offset interval.
    #offset_interval: in quarterLengths (4=whole note, 2=halfnote, 1=quarternote, 0.5=eighthnote,etc.)
    #
    # """
        import music21
        def get_next_note(in_stream, current_offset):
            # """
            #
            # :param self:
            # :param in_stream: The music 21 stream to be input into the function.
            # :param current_offset: Current_offset is the offset input to indicate where to start looking for the "next note."
            # :param offset_interval: Granularity, the offset_interval is\uses the quarterLength feature of music21, to indicate how far to search for the "next note" after the "current offset."
            # :return:
            # """
            #This function needs to know:
            #Stream
            #Random selection of specified Notes and Offsets
            #Specified offsets for repopulation
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
                        newnote = note.Note(p)
                        newnote.offset = e.offset
                        newnote.duration = e.duration
                        notelist.append(newnote)
                        print("note ", newnote.pitch)
                        print("offset ", newnote.offset)
                        print("duration ", newnote.duration)

                elif type(e) is music21.note.Note:
                    print ("Note")
                    newnote = note.Note(e.pitch)
                    newnote.offset = e.offset
                    newnote.duration = e.duration
                    notelist.append(newnote)
                    newnote.show('txt')

                else:
                    print (e)

            if (len(notelist) > 0):
                x = random.choice(notelist)
                print ("Choose: ", x.pitch)

                # need to remove the chosen note from in_stream
                for e in objs_at_current_offset:
                    if type(e) is music21.chord.Chord:
                        try:
                            e.remove(x.pitch)
                            print("removing from chord ", x.pitch)
                            print(" num remaining notes in chord", len(e.pitches))

                            if (len(e.pitches) == 0):
                                print("removing empty chord")
                                in_stream.remove(e,recurse=True)
                        except ValueError:
                            print("Not in this chord.")
                    elif type(e) is music21.note.Note and e.pitch == x.pitch:
                        print("removing single note", e.pitch)
                        in_stream.remove(e,recurse=True)

                return x
            elif current_offset < in_stream.flat.highestOffset:
                return "more"
            else:
                return "no more"


        stream_list = []

        new_stream = copy.deepcopy(stream)
        print ("start")
        if (chop_durs):
            new_stream = self.chop_up_notes(new_stream, offset_interval)

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
            print ("Submelody: ")
            s.show("txt")
            print ("Remaining Notes: ")
            new_stream.flat.show('txt')
            print ("Are we done?")
            if len(new_stream.flat.notes) == 0:
                done = True

        return stream_list

#MA-11.
#TODO Requires revising, possibly is redundant.
    def get_random_melody(self, in_stream):
        import music21
        import random
        import copy
        #random.seed(2222)
        neu_stream = music21.stream.Stream()
        for z in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            newballs = copy.deepcopy(z)
            newballs.offset = z.offset
            notelist = []
            if type(z) is music21.chord.Chord:
                for p in z.pitches:
                    newnote = note.Note(p)
                    newnote.offset = z.offset
                    newnote.duration = z.duration
                    notelist.append(newnote)
                    print ("note ", newnote.pitch)
                    print ("offset ", newnote.offset)
                    print ("duration ", newnote.duration)
                x = random.choice(notelist)
                x.show('txt')
                neu_stream.insert(x)

            elif type(z) is note.Note:
                neu_stream.insert(z)
        neu_stream.makeMeasures()
            #new_stream.makeMeasures()
        return neu_stream

#MA-12. #TODO Optimize for better sectionalizing.
    def sectionalize_image_array(self, image_array, sec_root):
        """
        :param image_array: An input cv2-read image array.
        :param sec_root: The square root of the number of desired sections. If you want 64 sections, select 8.
        :return: A list of smaller, evenly shaped arrays that, when piece together form the original image.
        """
        import numpy
        import numpy as np
        #Initial split, right down the middle. (Or more, for very large images with high resolution.
        # if len(image_array) >= (len(image_array[1])*2):
        #     i_split = sec/4
        # else:
        #     i_split = sec/2
        #sec = sec/4
        i_split = sec_root
        split1 = np.array_split(image_array, i_split)
        #Establish lists, for calling.
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

#MA-#TODO
    def reconstruct_image_sections(self, array_list):
        import math
        import numpy
        import numpy as np
        import statistics
        join_list = list()
        array_list.reverse()
        new_join = list()
        em = 0
        en = int(math.sqrt(len(array_list)))
        while en <= len(array_list):
            # for j in range(0, int(math.sqrt(len(a
            joinez = array_list[em: en]
            #joinez.reverse()
            np_join = np.hstack(joinez)
            join_list.append(np_join)
            # for el in range(em, en):
            # tuple1 = tuple(array_list[em: en])
            em += int(math.sqrt(len(array_list)))
            en += int(math.sqrt(len(array_list)))
            #Picture-wise, hstack for horizontal.
        join_list.reverse()
        re_image1 = np.vstack(join_list)
        #TODO Create work arounds for the oddly"shaped" images.
        #
        # if join_list[1].shape[0] != join_list[0].shape[0]:
        #     random_r = np.array([[[59047302, 12736756, 37869375]]])
        #     joinsert = np.insert(join_list[1], -1, random_r, axis=0)
        #     new_join.append(join_list[0])
        #     new_join.append(joinsert)
        #     re_image = np.vstack(new_join)
        #     final_image = g.mc.delete_select_points(re_image, [59047302, 12736756, 37869375])
        #     return final_image
        #else:
        return re_image1
        #Picture-wise, vstack for vertical.

##Sample work.
    # fptf1 = r"C:\Users\Isaac's\Desktop\Pictures-Photos\BobMandala.png"
    # mandala = cv2.imread(fptf1)
    # splitala = g.mc.sectionalize_image_array(mandala, 2)
    # blitala = splitala[0: 2]
    # blitala2 = splitala[2: 4]
    # litala = np.hstack((blitala[0], blitala[1]))
    # slitala = np.hstack((blitala2[0], blitala2[1]))
    # peace_mandala = np.vstack((slitala, litala))

    # array_list = splitala
    # join_list = list()
    # array_list.reverse()
    # em = 0
    # en = int(math.sqrt(len(array_list)))
    # while en <= len(array_list):
    #     for j in range(0, int(math.sqrt(len(array_list)))):
    #         join = array_list[em: en]
    #         np_join = np.hstack((join[0], join[1]))
    #         join_list.append(np_join)
    #         #for el in range(em, en):
    #         #tuple1 = tuple(array_list[em: en])
    #         em += en
    #         en += en

        # ass1 = join_list[1]
        # ass2 = np.insert(ass1, -1, random_r, axis=0)
        #renala = cv2.resize(mandala, (128, 128))

#3IDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#3D-1.
    def extract_xyz_coordinates_to_array(self, in_stream):
        """
        :param in_stream: Music21 input stream. (for 3d purposes the stream must contain stream.Parts)
        :return: note_coordinates: A numpy array comprised of x=note.offset, y=pitch.midi, and z=volume.velocity.
        """
        import music21
        import numpy as np
        #import vtk
        #Create lists and arrays for coordinate integer values.
        temp_stream = g.mc.notafy(in_stream)
        volume_list = list()
        pitch_list = list()
        offset_list = list()
        #Gather data all at once, turn them into floats, and put them into lists.-- (.offets are floats by default)
        for XYZ in temp_stream.flat.notes:
            if XYZ.volume.velocity is None:
                print("There are no velocity values for these notes. Assign velocity values.")
                return None
            offset_list.append(float(XYZ.offset))
            pitch_list.append(float(XYZ.pitch.midi))
            volume_list.append(float(XYZ.volume.velocity))
           #Create a numpy array with the the concatenated x,y,z data its elements.
        note_coordinates = np.r_['1, 2, 0', offset_list, pitch_list, volume_list]
        return note_coordinates

#3D-2.
    def extract_xyz_coordinates_to_stream(self, coords_array):
        #set_duration=None
        """
        This function takes a numpy array of coordinates, 3 x, y, z values per coordinates, and turns
        it into a music21 stream with those coordinates as .offset, .pitch, and .volume.velocity values for x, y, and z.
        ---Note for user. If note.quarterLength and note.volume.velocity are unassigned, they default to 1.0 and None respectively.
        :param coords_array: A 2D Numpy array of coordinate data.
        :return: parts_stream: A music21 stream.
        """
        import music21
        import numpy
        import numpy as np
        import copy
        import musicode as mc
        import g
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
        parts_stream = g.mc.separate_notes_to_parts_by_velocity(out_stream)
        # print("How bout here?")
        return parts_stream

#3D-3.
    def insert_instrument_into_parts(self, in_stream, midi_num=0):
        """
        Note: Some ints will not produce an instrument.Instrument, and instead will throw an error. Perhaps this class is still developing?
        This function assigns musical instruments to the parts of a music21 stream. It assigns only one instrument to all of them.
        :param in_stream: Stream to be modified.
        :param midi_num: music21.instrument.Instrument.midiProgram number assigning which programmed instruments to the iterated parts.
        :return: stream
        """
        import music21
        instru = music21.instrument.instrumentFromMidiProgram(midi_num)
        for p in in_stream.getElementsByClass(stream.Part):
            p.insert(p.offset, instru)
        return in_stream

#3D-4.
    def partition_instruments_by_random(self, in_stream):
        """
        This function executes inPlace where an instrument object is inserted into the beginning of every stream.Part in the main
        m21.stream.Stream with a randomly assigned music21.instrument.instrument().midiProgram value. The working values are shown in the below list.
        This list is subject to change upon updates to music21.
        :param in_stream:
        :return:
        """
        midinums = [0, 6, 7, 8, 19, 16, 20, 21, 22, 48, 40, 41, 42, 43, 46, 24, 26, 32, 33, 35, 105, 24, 104, 106,
                    107,
                    73, 72, 74, 75, 77, 78, 79, 68, 69, 71, 70, 65, 64, 65, 66, 67, 109, 111, 61, 60, 56, 57, 58,
                    11,
                    12, 13, 9, 14, 14, 15, 114, 47, 108, 115, 113, 116, 52]
        mp_set = set(midinums)
        midi_list = list(mp_set)
        for p in in_stream.getElementsByClass(stream.Part):
            # for i in random.choices(mPSet):
            p.insert(p.offset, instrument.instrumentFromMidiProgram(random.choice(midi_list)))
        return in_stream


#3D-5.
    def rotate_point_about_axis(self, x, y, z, axis, degrees):
        import math

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
    def rotate_array_points_about_axis(self, points, axis, degrees):
        """

        :param points:
        :param axis:
        :param degrees:
        :return:
        """
        import numpy as np
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
            ax, ay, az = self.rotate_point_about_axis(points[i][0], points[i][1], points[i][2], axis, degrees)
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

        # np_1 = np.insert(new_p, 0, ax_array, axis=1)
        #     #print(new_points)
        # np_2 = np.insert(np_1, 1, ay_array, axis=1)
        # np_3 = np.insert(np_2, 2, az_array, axis=1)
        return np_3

#3D-7.
    def get_points_from_ply(self, file_path, height=127):
        """
        Returns a 2D numpy array of coordinates from a .ply file, adjust into floating point value, and transformed based on the users input.
        Input can be positive or negative. For 3idiArt purpoes, object values should all be positive.
        :param file_path:
        :param height: Value up to 127. (Preferably not lower than 50)
        :param trans:
        :return: 2d numpy array.
        """

        import open3d
        import numpy
        import numpy as np
        ply = open3d.read_point_cloud(file_path)
        Data = numpy.asarray(ply.points)
        Data2 = Data + (0 - Data.min())
        Data3 = Data2 * (height/Data2.max())
        Data4 = np.asarray(Data3,  int)
        Data5 = np.asarray(Data4, float)

        # if height is None:
        #     height = 127
        # Data3 = Data2 * (height/Data2)
        # Data3 = Data2.round()
        #Rotate into place. (because scanning, .ojb files, and .ply files......)
        #Data6 = np.rot90(Data5, 1, (0, 1))
            #Since it's a 2Darray, just rearrange the calls
        return Data5

#3D-8. #TODO figure out other pointcloud writing method....
       #TODO figure out more Surface Reconstruction Methods.
    def set_ply_from_points(self, coords_array, file_path):
        #import open3d
        import numpy as np
        import numpy
        import vtk
        from vtk.util.numpy_support import vtk_to_numpy
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
    def delete_redundant_points(self, coords_array, stray=True):
        import numpy as np
        from collections import OrderedDict
        set_list = g.mc.array_to_lists_of(coords_array, tupl=True)
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
    def delete_select_points(self, coords_array, choice_list):
        import numpy as np
        #from collections import OrderedDict
        if coords_array.ndim == 3:
            dim = 3
        else:
            dim = 2
        set_list = g.mc.array_to_lists_of(coords_array, tupl=True)
        new_list = list()
        for i in set_list:
            if i not in choice_list:
                new_list.append(i)
        new_array = g.mc.lists_of_to_array(new_list, dim)
        return new_array

#3D-11.
    #TODO Test this function.
    def array_to_lists_of(self, coords_array, tupl=True):
        # import numpy
        # import numpy as np
        """
        Sister function of lists_of_to_array().
        This function turns numpy arrays into a list of coordinate lists\tuples or color lists\tuples.
        This functionality is conginent upon the input arrays ndim.
        Useful for compare calls requiring numpy data without wanting to use .any() or .all()...

        :param coords_array: Input 2D coordinate array or cv2.imread 3D array of color tuples. (i.e. a picture)
        :param tupl: Determines whether or not you want the parent list populated with the data as lists or tuples.
        :return: List.
        """
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
            #print(*lok, sep="\n")
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
            print("Suggested ndim should be 2 or three.")
            return None

#3D-12.
    #TODO Test this function.
    def lists_of_to_array(self, lizt, dim=2):
        """
        Sister function of array_to_lists_of().
        Takes coordinate lists or color lists of cv2.imreads and turns them
        back into numpy arrays with the appropriate shape and ndim.
        More advanced use may use more dimensions. This is not supported yet.
        :param lizt: A python list of array coordinates or color tuples. (typically)
        :param dim: Number of desired dimensions. 2 by default, otherwise will probably be 3,
        to return lizt to original cv2 numpy array.
        :return: Numpy array.
        """
        import numpy as np
        import statistics
        # for q in lists:
        #     r = np.array(q)
        array = np.array(lizt, ndmin=dim)
        if array.ndim == 3:
            #def print_factors(x):
            # This function takes a number and prints the factors
            #print("The factors of", x, "are:")
            f_list = list()
            for i in range(1, array.shape[1] + 1):
                if array.shape[1] % i == 0:
                    f_list.append(i)

            # change this value for a different result.
            #num = 320
            # uncomment the following line to take input from the user
            # num = int(input("Enter a number: "))
            #print_factors(num)
            new_array = array.reshape(statistics.median_low(f_list), statistics.median_high(f_list), 3)
            return new_array
        else:
            return array

#3D-13.
    def get_planes_on_axis(self, coords_array, axis="z", set_it=False):
        from collections import OrderedDict
        planes_list = list()
        if axis is "z":
            axis = 2
        elif axis is "y":
            axis = 1
        else:
            axis = 0
        axis_set = set(z for z in coords_array[:, axis].flatten())
        planes_dict = OrderedDict.fromkeys(i for i in coords_array[:, axis].flatten())
        if set_it:
            planes_dict = OrderedDict.fromkeys(i for i in axis_set)
        for i in planes_dict.keys():
            planes_list = list()
            for j in g.mc.array_to_lists_of(coords_array, tupl=False):
                if j[axis] == i:
                    planes_list.append(j)
                planes_dict[i] = planes_list
        print("Call for plane key by:")
        print(planes_dict.keys())
        print("Then use np.array on the value to reassert as numpy coordinate data.")
        return planes_dict

#3D-14.
    #def delete_nonsurface_points(self, coords_array()):


        # for i in g.mc.array_to_lists_of(coords_array):
        #     for j in planes_dict.keys():
        #         if j == i[2]:
        #             planes_dict.key = planes_list.append(i)
        #
        # if i[:, 2] in axis_set:
        #     plane_list = list()



            # for i in coords_array:
            #     if i[:,2] in list(axis_set):     , plane_list.append(i))

        # dict(zip([j for j in list(z_set)], [i for i in coords_array]))


#3D-
    def make_vtk_points_mesh(self, points):
        import vtk
        import numpy as np
        from vtk.util.numpy_support import numpy_to_vtk
        from vtk.util.numpy_support import vtk_to_numpy
        from vtk.util.numpy_support import numpy_to_vtkIdTypeArray
        """ Create a PolyData object from a numpy array containing just points """
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

        ##Research:
        ##"https://vtk.org/gitweb?p=VTK.git;a=blob;f=Examples/Modelling/Python/reconstructSurface.py"
        ##"https://vtk.org/Wiki/VTK/Examples/Python/PLYWriter"
        ##EXAMPLE V
    # big_ted = g.mc.get_points_from_ply(file_someshit)
    # pure_ted = g.mc.delete_redundant_points(big_ted, stray=True)
    # VTK_Ted = g.mc.make_vtk_points_mesh(pure_ted)
    # surf = vtk.vtkSurfaceReconstructionFilter()
    # surf.SetInputData(VTK_Ted)
    #
    # cf = vtk.vtkContourFilter()
    # cf.SetInputConnection(surf.GetOutputPort())
    # cf.SetValue(0, 0.0)
    #
    # # Sometimes the contouring algorithm can create a volume whose gradient
    # # vector and ordering of polygon (using the right hand rule) are
    # # inconsistent. vtkReverseSense cures this problem.
    # reverse = vtk.vtkReverseSense()
    # reverse.SetInputConnection(cf.GetOutputPort())
    # reverse.ReverseCellsOn()
    # reverse.ReverseNormalsOn()
    #
    # map = vtk.vtkPolyDataMapper()
    # map.SetInputConnection(reverse.GetOutputPort())
    # map.ScalarVisibilityOff()
    #
    # surfaceActor = vtk.vtkActor()
    # surfaceActor.SetMapper(map)
    # surfaceActor.GetProperty().SetDiffuseColor(1.0000, 0.3882, 0.2784)
    # surfaceActor.GetProperty().SetSpecularColor(1, 1, 1)
    # surfaceActor.GetProperty().SetSpecular(.4)
    # surfaceActor.GetProperty().SetSpecularPower(50)
    #
    # # Create the RenderWindow, Renderer and both Actors
    # ren = vtk.vtkRenderer()
    # renWin = vtk.vtkRenderWindow()
    # renWin.AddRenderer(ren)
    # iren = vtk.vtkRenderWindowInteractor()
    # iren.SetRenderWindow(renWin)
    #
    # # Add the actors to the renderer, set the background and size
    # ren.AddActor(surfaceActor)
    # ren.SetBackground(1, 1, 1)
    # renWin.SetSize(400, 400)
    # ren.GetActiveCamera().SetFocalPoint(0, 0, 0)
    # ren.GetActiveCamera().SetPosition(1, 0, 0)
    # ren.GetActiveCamera().SetViewUp(0, 0, 1)
    # ren.ResetCamera()
    # ren.GetActiveCamera().Azimuth(20)
    # ren.GetActiveCamera().Elevation(30)
    # ren.GetActiveCamera().Dolly(1.2)
    # ren.ResetCameraClippingRange()
    #
    # iren.Initialize()
    # renWin.Render()
    # iren.Start()

    ##MUSIC21_FUNCTIONS\CLASSES (NEW, for later)
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#M21-1.

    def delete_redundant_notes(self, in_stream, force_sort=False):
        """
        First parse stream with converter.parse. Then, summon for notes and chords and use method removeRedundantPitches from the chord module and then sortAscending
        ----keep_hdur_notes=False
        :param in_stream: Stream with notes.
        :return: New stream.
        """
        # off = list()
        # pit = list()
        # vel = list()
        # dur = list()
        for i in in_stream.flat.notes:
            if type(i) is chord.Chord:
                i.removeRedundantPitches(inPlace=True)
            if force_sort is True:
                i.sortAscending(inPlace=True)
        return in_stream
        # off.append(i.offset)
        # pit.append(i.pitch.midi.ps)
        # vel.append(i.volume.velocity)

#M21-2.
    def notafy(self, in_stream):
        import copy
        new_stream = stream.Stream()
        for i in in_stream.flat.getElementsByClass(["Chord", "Note"]):
            notelist = list()
            if type(i) is chord.Chord:
                for p in i.pitches:
                    newnote = note.Note(p)
                    newnote.offset = i.offset
                    newnote.duration = i.duration
                    if i.volume.velocity:
                        newnote.volume.velocity = i.volume.velocity
                    else:
                        print("No velocity info for chord. ")
                    notelist.append(newnote)
                for x in notelist:
                    new_stream.insert(i.offset, copy.deepcopy(x))
            elif type(i) is note.Note:
                new_stream.insert(i.offset, copy.deepcopy(i))

        return new_stream

#M21-3.
    def separate_notes_to_parts_by_velocity(self, in_stream):
        """
        :param self:
        :param in_stream: Stream to be modified.
        :return: Stream with parts.
        """
        import music21
        import copy
        part_stream = stream.Stream()
        velocity_list = list()
        end_stream = stream.Stream()
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
            parts1 = stream.Part()
            parts1.partsName = k
            part_stream.insert(0.0, copy.deepcopy(parts1))
        #print("Parts_Stream", part_stream)
        #part_stream.show('txt')
        #Insert notes of same velocity value into stream.Part of the same value name.
        for s in part_stream.getElementsByClass(stream.Part):
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
    def set_stream_velocities(self, in_stream, vel):
        for i in in_stream.flat.notes:
            i.volume.velocity = vel
        return in_stream

#M21-5.
    def change_velocities_by_rangelist(in_stream, volume_list):
        # volume_list = list()
        # for i in range(vel_l, vel_h, vel_s):
        #     volume_list.append(i)
        # print('vol_list', volume_list)

        v = 0
        for o in in_stream.flat.notes:
            o.volume.velocity = volume_list[v]
            print(o.volume.velocity)
            v += 1
            if len(in_stream.flat.notes) > len(volume_list):
                v = 0
        return in_stream

#M21-. TODO
    #def music21.clash.Clash? Khord? Vhord? Music21 object for housing multiple notes with different velocities at the same offset.


#GUI_FUNCTIONS (Generally Private)
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#GUI-1.
    def _stream_to_matrix(self, stream):
        matrix = [["0"] * int(16 * stream.highestTime) for _ in range(0, 128)]

        for z in stream.flat.getElementsByClass(["Chord", "Note"]):
            if type(z) is chord.Chord:
                for p in z.pitches:
                    x_start = int(16 * z.offset)
                    x_end = x_start + int(16 * z.duration.quarterLength)
                    self._matrix_set_notes(matrix, p.midi, x_start, x_end)
            elif type(z) is note.Note:
                x_start = int(16 * z.offset)
                x_end = x_start + int(16 * z.duration.quarterLength)
                self._matrix_set_notes(matrix, z.pitch.midi, x_start, x_end)

        return matrix

#GUI-2.
    def _matrix_set_notes(self, matrix, y, x_start, x_end):
        for x in range(x_start, x_end):
            matrix[len(matrix) - 1 - y][x] = 1

#GUI-3.
    def _matrix_to_stream(self, matrix, connect, cell_note_size):
        s = stream.Stream()
        for x in range(0, matrix.shape[0]):
            for y in range(0, matrix.shape[1]):
                if (matrix[x, y] == 1):
                    if connect:
                        n = note.Note()
                        n.pitch.midi = y
                        n.offset = x / (1 / cell_note_size)
                        j = x
                        d = 0
                        while (j < len(matrix) and matrix[j, y] == 1):
                            d += cell_note_size
                            matrix[j, y] = 0
                            j += 1
                        n.duration.quarterLength = d
                        s.insert(n.offset, n)
                    else:
                        n = note.Note()
                        n.pitch.midi = y
                        n.offset = x / (1 / cell_note_size)
                        n.duration.quarterLength = cell_note_size
                        s.insert(n.offset, n)
        s.makeMeasures(inPlace=True)
        return s


#DEMO_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

#D-1.
    def demo_1(self, text_file):
        """
        Creates a song with some shit.
        # bass line  = POWerTap
        # melody     = Script-Ease
        # melody2    = MetaMorse
        # harmony    = BraillePulse

        :param: text_file
        :return: stream.Stream() of translated musicode(s).
        """

        '''There's only one advice.
        That's worth more than another.
        A life time of choices sends you somewhere.
        So treasure the voice of your mother.'''

        #TODO: Figure out how FLStudio handles mid with multiple Parts.  And music21's Scores(), Parts(), Streams() etc.
        #TODO: Figure out function for allocating assorted musicodes per translated line of text file.

        s = stream.Stream()
        bass = stream.Part()
        melody = stream.Part()
        melody2 = stream.Part()
        harmony = stream.Part()


        bass = self.translate_from_text_file("POWerTap_X", text_file)
        melody = self.translate_from_text_file("Script-Ease", text_file)
        melody2 = self.translate_from_text_file("MetaMorse", text_file)
        harmony = self.translate_from_text_file("BraillePulse", text_file)

        #TODO - some random transposing, alter duration, alter offset

        s.insert(bass)
        s.insert(melody)
        s.insert(melody2)
        s.insert(harmony)

        return s


g.mc = Musicode()


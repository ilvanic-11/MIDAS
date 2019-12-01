# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# Name:         musicode.py
# Purpose:      This is the topsplit file for musicode classes and utilities
#
# Authors:      Zachary Plovanic
#               Isaac Plovanic
#
# Copyright:    musicode is Copyright © 2017 Isaac Plovanic and Zachary Plovanic 
#               music21 is Copyright © 2013-17 Michael Scott Cuthbert and the music21
#               Project
# License:      LGPL or BSD, see license.txt
#------------------------------------------------------------------------------
'''

'''


from music21 import *
import g
import re
import os
import copy
import random


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
    musicode_path = r"C:\Users\Zach-X\Desktop\FL SDK\Isaac's_Patterns_and_Shit\Musicode Midi Libraries"
    #musicode_path = r"C:\Users\Isaac's\Desktop\Isaac's Synth Music Source Folder\FL\Tower Projects File\10_Musicode Libraries"
    #musicode_path = r"C:\Users\iplovanic\Desktop\10_Musicode Libraries"
    am_dict = dict() #Animuse dictionary
    asciiX_dict = dict()  #Asciipher dictionary
    asciiY_dict = dict()  #Asciipher dictionary
    bp_dict = dict() #BraillePulse dictionary
    mm_dict = dict() #Metamorse dictionary
    ptX_dict = dict() #POWerTap_X dictionary
    ptY_dict = dict() #POWerTap_Y dictionary
    se_dict = dict() #Script-Ease dictionary
    splyce_dict = dict() #Splyce dictionary
    
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
                 }
    
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
                }


    def add_to_dict(self, char, musicode, full_path_to_file):
        """
        Making this function public in case someone wants to modify the dicts
        :param dict:
        :param full_path_to_file:
        :return:
        """
        import music21
        print("Importing: %s" % full_path_to_file)
        m = stream.Measure()
        w = music21.ElementWrapper("".join([musicode, " : ", char]))
        m.append(w)
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
        self.add_to_dict(".", "Animuse", "".join([punct_dir, "musicode_am_exclamationmark.mid"]))
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
        self.add_to_dict(".", "Script-Ease", "".join([punct_dir, "musicode_se_exclamationmark.mid"]))
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
        self.add_to_dict("?", "Asciipher_X", "".join([punct_dir, "musicode_asciiX_questionmark.mid"]))

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
            num = num+1
        return s

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
                line = line+1
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


    def transpose_all_measures_by_random(self, in_stream):
        """
        Transposes all Measures in the music21 stream by a random interval 1-7
        Currently only transposes up in pitch.
        :params stream:  the music21 stream to perform transposing in
        :return:
        """
        import music21
        for m in in_stream.flat.getElementsByClass(stream.Measure) :
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

    def demo(self, text_file):
        """
        Creates a song with some shit.
        # bass line  = POWerTap
        # melody     = Script-Ease
        # melody2    = MetaMorse
        # harmony    = BraillePulse

        :param text_file: 
        :return: 
        """

        #TODO: Figure out how FLStudio handles mid with multiple Parts.  And music21's Scores(), Parts(), Streams() etc.
        s = stream.Stream()
        bass = stream.Part()
        melody = stream.Part()
        melody2 = stream.Part()
        harmony = stream.Part()


        bass = self.translate_from_text_file("POWerTap_X", text_file)
        melody = self.translate_from_text_file("Script-Ease", text_file)
        melody2 = self.translate_from_text_file("MetaMorse", text_file)
        harmony = self.translate_from_text_file("BraillePulse", text_file)

        #do some random transposing, alter duration, alter offset shit

        s.insert(bass)
        s.insert(melody)
        s.insert(melody2)
        s.insert(harmony)

        return s



    # def transpose_only_letter(stream, letter, degree):
    #     """ Transposes in place all of the specified letter by the specified number of degrees
    #     :return:
    #     """

    # def alter_note_durations
    # def alter_note_starting_offsets

musicode.mc = Musicode()


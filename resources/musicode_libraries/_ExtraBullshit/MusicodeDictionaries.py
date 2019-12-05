#! /usr/bin/env python3

#class Musicode:
    #import music21
    #import glob
from music21 import*
import glob



   # The path to the top level of Musicode mid"]))i Libraries
Musicode_Path = r"C:\Users\Isaac's\Desktop\Isaac's Synth Music Source Folder\FL\Tower Projects File\10_Musicode Libraries"

am_dict = dict() #Animuse dictionary
ascii_dict = dict() #Asciipher dictionary
bp_dict = dict() #BraillePulse dictionary
mm_dict = dict() #Metamorse dictionary
pt_dict = dict() #POWerTap dictionary
splyce_dict = dict() #Splyce dictionary

shorthand = {
             "Animuse"      : "am",
             "Asciipher"    : "ascii",
             "BraillePulse" : "bp",
             "MetaMorse"    : "mm",
             "POWerTap"     : "pt",
             "Splyce"       : "splyce",
             }

dictionaries = {
             "Animuse"      : am_dict,
             "Asciipher"    : ascii_dict,
             "BraillePulse" : bp_dict,
             "MetaMorse"    : mm_dict,
             "POWerTap"     : pt_dict,
             "Splyce"       : splyce_dict,
                }

def setupMidiDictionaries():
    setup_am_dict()
    setup_ascii_dict()
    setup_bp_dict()
    setup_mm_dict()
    setup_pt_dict()
    setup_splyce_dict()


def setup_LettersNumbers( dict, musicode):
    import glob
    import re
    import os
    import music21
    sh = shorthand.get(musicode)

    for pack in ("Lowercase", "Uppercase", "Numbers"):
        directory = Musicode_Path + "\\" + musicode + "\\" + sh + "_" + pack
        filenames = next(os.walk(directory))[2]
        for file in filenames:
            my_search = re.search(r"musicode_%s_(\w|\number).mid"% sh, file)
            if my_search:
                add_to_dict(my_search.group(1),dict, directory+"\\"+file)

    # Add a measure of rest for the space character (' ')
    r = music21.stream.Measure()
    r.duration = music21.duration.Duration(4.0)
    rest = music21.note.Rest(quarterLength=4.0)
    r.insert(rest)
    dict[' '] = r


#end setup_LettersNumbers()


def add_to_dict(char, dict, full_path_to_file):
    import music21
    print("Importing: %s" % full_path_to_file)
    m = music21.stream.Measure()
    m.duration = music21.duration.Duration(4.0)
    imported_mid = music21.converter.parse(full_path_to_file)
    si = imported_mid.flat.notesAndRests

    #insert notes into new measure
    for el in si:
        m.insert(el)

    #insert rest to fill up remainder of measure
    if (m.highestTime < 4):
        rest = music21.note.Rest(quarterLength=(4-m.highestTime))
        m.append(rest)
    dict[char] = m


def setup_am_dict(): #TODO Rename Backslashes to forward slashes
    setup_LettersNumbers( am_dict, "Animuse")
    punct_dir = Musicode_Path + "\\Animuse\\am_Punctuation\\"
    add_to_dict("/", am_dict, "".join([punct_dir, "musicode_am_forwardslash.mid"]))
    add_to_dict("]", am_dict, "".join([punct_dir, "musicode_am_closebracket.mid"]))
    add_to_dict(")", am_dict, "".join([punct_dir, "musicode_am_closeparenthesis.mid"]))
    add_to_dict(":", am_dict, "".join([punct_dir, "musicode_am_colon.mid"]))
    add_to_dict(",", am_dict, "".join([punct_dir, "musicode_am_comma.mid"]))
    add_to_dict('\"', am_dict, "".join([punct_dir, "musicode_am_doublequotationmark.mid"]))
    add_to_dict("!", am_dict, "".join([punct_dir, "musicode_am_exclamationmark.mid"]))
    add_to_dict("-", am_dict, "".join([punct_dir, "musicode_am_hyphen.mid"]))
    add_to_dict("[", am_dict, "".join([punct_dir, "musicode_am_openbracket.mid"]))
    add_to_dict("(", am_dict, "".join([punct_dir, "musicode_am_openparenthesis.mid"]))
    add_to_dict(".", am_dict, "".join([punct_dir, "musicode_am_period.mid"]))
    add_to_dict(";", am_dict, "".join([punct_dir, "musicode_am_semicolon.mid"]))
    add_to_dict("\'", am_dict, "".join([punct_dir, "musicode_am_singlequotationmark.mid"]))


def setup_ascii_dict():
    setup_LettersNumbers( ascii_dict, "Asciipher")
    punct_dir = Musicode_Path + "\\Asciipher\\ascii_Punctuation\\"
    add_to_dict("\'", ascii_dict, "".join([punct_dir, "musicode_ascii_singlequotationmark.mid"]))
    add_to_dict("/", ascii_dict, "".join([punct_dir, "musicode_ascii_forwardslash.mid"]))
    add_to_dict("]", ascii_dict, "".join([punct_dir, "musicode_ascii_closebracket.mid"]))
    add_to_dict(")", ascii_dict, "".join([punct_dir, "musicode_ascii_closeparenthesis.mid"]))
    add_to_dict(":", ascii_dict, "".join([punct_dir, "musicode_ascii_colon.mid"]))
    add_to_dict(",", ascii_dict, "".join([punct_dir, "musicode_ascii_comma.mid"]))
    add_to_dict("!", ascii_dict, "".join([punct_dir, "musicode_ascii_exclamationmark.mid"]))
    add_to_dict("-", ascii_dict, "".join([punct_dir, "musicode_ascii_hyphen.mid"]))
    add_to_dict("[", ascii_dict, "".join([punct_dir, "musicode_ascii_openbracket.mid"]))
    add_to_dict("(", ascii_dict, "".join([punct_dir, "musicode_ascii_openparenthesis.mid"]))
    add_to_dict('\"', ascii_dict, "".join([punct_dir, "musicode_ascii_doublequotationmark.mid"]))
    add_to_dict(".", ascii_dict, "".join([punct_dir, "musicode_ascii_period.mid"]))
    add_to_dict(";", ascii_dict, "".join([punct_dir, "musicode_ascii_semicolon.mid"]))

def setup_bp_dict():
    setup_LettersNumbers( bp_dict, "BraillePulse")
    punct_dir = Musicode_Path + "\\BraillePulse\\bp_Punctuation\\"
    add_to_dict("\'", bp_dict, "".join([punct_dir, "musicode_bp_singlequotationmark.mid"]))
    add_to_dict("/", bp_dict, "".join([punct_dir, "musicode_bp_forwardslash.mid"]))
    add_to_dict(":", bp_dict, "".join([punct_dir, "musicode_bp_colon.mid"]))
    add_to_dict(",", bp_dict, "".join([punct_dir, "musicode_bp_comma.mid"]))
    add_to_dict(".", bp_dict, "".join([punct_dir, "musicode_bp_decimalpoint.mid"]))
    add_to_dict("!", bp_dict, "".join([punct_dir, "musicode_bp_exclamationmark.mid"]))
    add_to_dict("-", bp_dict, "".join([punct_dir, "musicode_bp_hyphen.mid"]))
    add_to_dict("(", bp_dict, "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
    add_to_dict(")", bp_dict, "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
    add_to_dict("[", bp_dict, "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
    add_to_dict("]", bp_dict, "".join([punct_dir, "musicode_bp_openclosebracketparenthesis.mid"]))
    add_to_dict('\"', bp_dict, "".join([punct_dir, "musicode_bp_doublequotationmark.mid"]))
    add_to_dict(".", bp_dict, "".join([punct_dir, "musicode_bp_period.mid"]))
    add_to_dict(";", bp_dict, "".join([punct_dir, "musicode_bp_semicolon.mid"]))


def setup_mm_dict():
    setup_LettersNumbers( mm_dict, "MetaMorse")
    punct_dir = Musicode_Path + "\\MetaMorse\\mm_Punctuation\\"
    add_to_dict("/", mm_dict, "".join([punct_dir, "musicode_mm_forwardslash.mid"]))
    add_to_dict("]", mm_dict, "".join([punct_dir, "musicode_mm_closebracketparenthesis.mid"]))
    add_to_dict(")", mm_dict, "".join([punct_dir, "musicode_mm_closebracketparenthesis.mid"]))
    add_to_dict(":", mm_dict, "".join([punct_dir, "musicode_mm_colon.mid"]))
    add_to_dict(",", mm_dict, "".join([punct_dir, "musicode_mm_comma.mid"]))
    add_to_dict('\"', mm_dict, "".join([punct_dir, "musicode_mm_doublequotationsmark.mid"]))
    add_to_dict("!", mm_dict, "".join([punct_dir, "musicode_mm_exclamationmark.mid"]))
    add_to_dict("-", mm_dict, "".join([punct_dir, "musicode_mm_hyphen.mid"]))
    add_to_dict("[", mm_dict, "".join([punct_dir, "musicode_mm_openbracketparenthesis.mid"]))
    add_to_dict("(", mm_dict, "".join([punct_dir, "musicode_mm_openbracketparenthesis.mid"]))
    add_to_dict(".", mm_dict, "".join([punct_dir, "musicode_mm_period.mid"]))
    add_to_dict(";", mm_dict, "".join([punct_dir, "musicode_mm_semicolon.mid"]))
    add_to_dict("\'", mm_dict, "".join([punct_dir, "musicode_mm_singlequotationmark.mid"]))

def setup_pt_dict():
    setup_LettersNumbers( pt_dict, "POWerTap")
    punct_dir = Musicode_Path + "\\POWerTap\\pt_Punctuation\\"
    add_to_dict("/", pt_dict, "".join([punct_dir, "musicode_pt_forwardslash.mid"]))
    add_to_dict(":", pt_dict, "".join([punct_dir, "musicode_pt_colon.mid"]))
    add_to_dict(",", pt_dict, "".join([punct_dir, "musicode_pt_comma.mid"]))
    add_to_dict('\"', pt_dict, "".join([punct_dir, "musicode_pt_doublequotationmark.mid"]))
    add_to_dict("!", pt_dict, "".join([punct_dir, "musicode_pt_exclamationmark.mid"]))
    add_to_dict("-", pt_dict, "".join([punct_dir, "musicode_pt_hyphen.mid"]))
    add_to_dict("[", pt_dict, "".join([punct_dir, "musicode_pt_openclosebracket.mid"]))
    add_to_dict("]", pt_dict, "".join([punct_dir, "musicode_pt_openclosebracket.mid"]))
    add_to_dict("(", pt_dict, "".join([punct_dir, "musicode_pt_opencloseparenthesis.mid"]))
    add_to_dict(")", pt_dict, "".join([punct_dir, "musicode_pt_opencloseparenthesis.mid"]))
    add_to_dict(".", pt_dict, "".join([punct_dir, "musicode_pt_period.mid"]))
    add_to_dict(";", pt_dict, "".join([punct_dir, "musicode_pt_semicolon.mid"]))
    add_to_dict("\'", pt_dict, "".join([punct_dir, "musicode_pt_singlequotationmark.mid"]))

def setup_splyce_dict():
    setup_LettersNumbers( splyce_dict, "Splyce")
    punct_dir = Musicode_Path + "\\Splyce\\splyce_Punctuation\\"
    add_to_dict("/", splyce_dict, "".join([punct_dir, "musicode_splyce_forwardslash.mid"]))
    add_to_dict("]", splyce_dict, "".join([punct_dir, "musicode_splyce_closebracket.mid"]))
    add_to_dict(")", splyce_dict, "".join([punct_dir, "musicode_splyce_closeparenthesis.mid"]))
    add_to_dict(":", splyce_dict, "".join([punct_dir, "musicode_splyce_colon.mid"]))
    add_to_dict(",", splyce_dict, "".join([punct_dir, "musicode_splyce_comma.mid"]))
    add_to_dict('\"', splyce_dict, "".join([punct_dir, "musicode_splyce_doublequotationmark.mid"]))
    add_to_dict("!", splyce_dict, "".join([punct_dir, "musicode_splyce_exclamationmark.mid"]))
    add_to_dict("-", splyce_dict, "".join([punct_dir, "musicode_splyce_hyphen.mid"]))
    add_to_dict("[", splyce_dict, "".join([punct_dir, "musicode_splyce_openbracket.mid"]))
    add_to_dict("(", splyce_dict, "".join([punct_dir, "musicode_splyce_openparenthesis.mid"]))
    add_to_dict(".", splyce_dict, "".join([punct_dir, "musicode_splyce_period.mid"]))
    add_to_dict(";", splyce_dict, "".join([punct_dir, "musicode_splyce_semicolon.mid"]))
    add_to_dict("'", splyce_dict, "".join([punct_dir, "musicode_splyce_singlequotationmark.mid"]))

def translate(musicode, string):
    import music21
    import copy
    s = music21.stream.Part()
    num = 0
    for c in string:
        new_measure = music21.stream.Measure()

        #m.show('txt')
        new_measure = copy.deepcopy(dictionaries[musicode].get(c))
        new_measure.number = num
        s.append(new_measure)
        num = num+1
    return s


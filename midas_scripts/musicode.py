# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
# Name:         musicode.py
# Purpose:      This is the pianoroll_mainbuttons_split file for musicode
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
#MUSICODE_FUNCTIONS
#-------------------
#UA-1.  def TRANSLATE(musicode, string)
#UA-2.  def TRANSLATE_FROM_TEXT_FILE(musicode, filename)
#UA-3.  def TRANSLATE_LETTER(c, musicode, num) ???
#UA-4.  def TRANSLATE_EACH_LETTER_TO_RANDOM_MUSICODE(text)
#UA-5.  def ALIGN_MUSICODE_WITH_MELODY(melody_stream, musicode)
#TODO UA-6.   def CHANGE_MUSICODE

###############################################################################

import copy
import music21
import re
import os
import random
#from midas_scripts import music21funcs
from midas_scripts import music21funcs
from collections import OrderedDict
from traits.api import HasTraits
from traits.trait_types import Any
import shutil


class Musicode():

	def __init__(self):
		self.user_Created = music21.stream.Part()
		self.musicode_name = "User_Generated"
		self.sh = "ug"
		self.full_new_musicode_path = ""  #This is established when a new musicode is created with make_musicode(). #TODO Make a default? Or leave so export throws an error?
		#print("userCreated on Init:", self.userCreated)
		self._setup_midi_dictionaries()
		## The function "make_musicode" appends to this and allows the user to translate from it and\or export\write from it.
		# An instantiation of musicode.Musicode() occurs in the MIDAS_wx.py init.

		# Establish operating data for the make_musicode() function.
		self.Latin_Script = '''AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz  ?,;\':-.!\"()[]/  0123456789'''
		# Latin_Script = ['A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J',
		# 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U',
		# 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', ' ', ' ', ('questionmark'), ('comma'), ('semicolon'),
		# ('singlequotationmark'), ('colon'), ('hyphen'), ('period'), ('exclamationmark'), ('doublequotationmark'),
		# ('openparenthesis'), ('closeparenthesis'), ('openbracket'), ('closebracket'), ('forwardslash'), ' ', ' ',
		# '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		#print(self.Latin_Script)

		self.Punct_Workaround = OrderedDict.fromkeys(([j for j in '''?,;\':-.!\"()[]/''']))
		self.Punct_Symbols = '''?,;\':-.!\"()[]/'''
		self.Punct_Names = ['questionmark', 'comma', 'semicolon', 'singlequotationmark', 'colon', 'hyphen', 'period',
							'exclamationmark',
							'doublequotationmark', 'openparenthesis', 'closeparenthesis', 'openbracket', 'closebracket',
							'forwardslash']
		for l in range(0, len(self.Punct_Symbols)):
			self.Punct_Workaround[self.Punct_Symbols[l]] = self.Punct_Names[l]
		print("Punct_Dict:", self.Punct_Workaround)


	set_path = r"musicode_libraries"
	absFilePath = os.path.dirname(os.path.abspath(set_path))
	libraryPath = absFilePath + "\\resources\\" + set_path
	musicode_path = libraryPath
	# The path to the top level of Musicode midi Libraries
	#musicode_path = r"C:\Users\Zach-X\PycharmProjects\MIDAS\resources\musicode_libraries"
	#musicode_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\10_Musicode_Libraries"  #TODO Needs to be localized to installation folders.
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

	def add_to_dict(self, char, musicode, full_path_to_file):
		"""
			This function is made public in case someone wants to modify the dicts.
		:param dict:
		:param full_path_to_file:
		:return:
		"""
		#print("Importing: %s" % full_path_to_file)
		m = music21.stream.Measure()
		w = music21.ElementWrapper("".join([musicode, " : ", char]))
		te = music21.expressions.TextExpression(char)
		te.style.fontSize = 18
		te.style.absoluteY = 40
		te.style.alignHorizontal = 'center'

		m.append(w)
		m.append(te)
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
		r = music21.stream.Measure()
		r.duration = music21.duration.Duration(4.0)
		rest = music21.note.Rest(quarterLength=4.0)
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

	# UNIDIART_FUNCTIONS
	# --------------------------------------
	# -----------------------------------------------------------------------
	# ----------------------------------------------------------------------------------------------------------------------

	#UA-1.
	def translate(self, musicode, string):
		"""

			Translates a string into a selected musicode.

		:param musicode: 	The musicode to translate into
		:param string: 		The string text to translate
		:return: 			music21 stream containing the translated text.
		"""
		if musicode != self.musicode_name:		#When you use "User_Selected" as a musicode choice,
			s = music21.stream.Part()			#you can only use the measures you've created using make_musicode.
			num = 0
			for c in string:
				new_measure = self._translate_letter(c, musicode, num)
				s.append(new_measure)
				num = num + 1
		elif musicode == self.musicode_name:
			s = music21.stream.Part()
			num = 0
			for c in string:
				new_measure = self._translate_letter(c, musicode, num)
				print("New_Measure:", new_measure)
				s.append(new_measure)
				num = num + 1

		#else:
			#for c in string:

		return s

	#UA-2.
	def translate_from_text_file(self, musicode, file_name):
		"""
			Translates input from a text file.

		:param text: 	The file name.
		:return: 		Stream.
		"""
		# TODO: Find a way to add option to split each line of text into a different midi track

		file = open(file_name, "r")
		s = music21.stream.Part()
		num = 0
		line = 0
		ss = music21.stream.Part()
		w = music21.ElementWrapper("Line: %d" % line)
		ss.insert(w)
		c = file.read(1)
		while c:
			if c == "\n":
				s.insert(ss)
				ss = music21.stream.Part()
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

	#UA-3.
	def _translate_letter(self, c, musicode, num = None):
		"""
			Translates a single "letter" string into a selected musicode. Adapted to user-generated musicode from the
		make_musicode() function.

		:param c: 			A single string instance. (i.e  "y" or "!")
		:param musicode: 	The desired Musicode to be called.
		:param num: 		The measure's measureNumber.
		:return:
		"""
		#new_measure = music21.stream.Measure()
		# m.show('txt')
		# print("letter:" + c + "\n")

		if musicode == self.musicode_name:
			#self.dictionaries.update(User_Generated=self.userCreated)
			print("C:", c)
			print("Here")
			#print("Here 2:", self.userCreated)
			#self.userCreated.show()
			for measure in self.user_Created:
				#print("How bout here?")
				#print("User_Created:", self.userCreated.show('txt'))
				element_wrapper = measure[-1]
				if type(element_wrapper) == music21.note.Rest:
					element_wrapper = measure[-2]
				if type(element_wrapper) == music21.bar.Barline:
					element_wrapper = measure[-3]
				if element_wrapper.obj == c:
					new_measure = copy.deepcopy(measure)
					#print("New_Measure:", new_measure)
					return new_measure
				elif element_wrapper.obj not in c:
					print("Your user-generated musicode does not have this '%s' string character:" % c)


		elif musicode != self.musicode_name:
			#self.dictionaries.update(User_Generated=self.userCreated)
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
			Translates the text into a stream where each letter is a random Musicode.

		:param text: 	The text to be translated.
		:return: 		Stream.
		"""
		s = music21.stream.Part()
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
	def align_musicode_with_melody(self, melody_stream, musicode_stream, keysig=None):
		"""

			This function takes a composed melody and intertwines it with a translated instance of musicode. See picture
		#TODO figure out pictures with doc strings. In the alignment process, spaces are ignored.
		The number of melody_stream.flat.notes must match the number of musicode_stream.getElementsByClass(-
		--stream.Measure).

		:param melody_stream: 	The selected melody for alignment. Generally acquired from a composed instance of midi
								converted with converter.parse.
		:param musicode_stream: The text to be aligned with the melody. Acquired from musicode.mc.translate("Musicode",
								"String")
		:return: 				New music21.stream.Stream object of aligned melody stream.
		#TODO The keyAware transpostion of the letters in the measures needs work with respect to bass and root of chords.
		"""

		if type(melody_stream) == music21.stream.Score:
			melody_stream = melody_stream.pop(0)    #Converter.parse returns a score with parts. We want the stream.Part which has our just-composed melody.
		keysig = music21.key.Key(keysig)		#If keysig == None, key.Key will default to C.
		melody_stream.insertAndShift(0.0, keysig)     #Inserts key.Key at begining of part stream.
		s = music21.stream.Stream()
		m = 0
		musicode_measures = musicode_stream.getElementsByClass(music21.stream.Measure)
		for n in melody_stream.flat.notes:
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
				new_measure = music21funcs.stretch_by_measure(ms, 0, 0, (n_dur / (m_dur)))
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
				if len(melody_stream.getKeySignatures()) != 1:
					print("You have no key signature, or more than one.")
					return None
				else:
					k = melody_stream.getKeySignatures()[0].asKey()
				# C. Transpose Key aware all of new measure by THAT interval.
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

	def create_directories(self):
		if os.path.exists(self.full_new_musicode_path) is False:
			os.mkdir(self.full_new_musicode_path)
		os.mkdir(self.full_new_musicode_path + "\\" + self.sh + "_" + "Uppercase\\")
		os.mkdir(self.full_new_musicode_path + "\\" + self.sh + "_" + "Lowercase\\")
		os.mkdir(self.full_new_musicode_path + "\\" + self.sh + "_" + "Numbers\\")
		os.mkdir(self.full_new_musicode_path + "\\" + self.sh + "_" + "Punctuation\\")

	# M21-7.
	def make_musicode(self, in_stream, musicode_name = "User_Generated", shorthand = "sh", filepath=None, selection=None, write=True, timeSig='4/4'):
		"""
		This function take a string and an input stream with equal lengths (number of measures equals number of string characters)
		 and conjoins them to create a user-generated assingment of musicodes to be called by said string character.
		 Choice included to write to file and to provide a selection. Selection should ideally match input stream, although
		 creativity is highly encouraged!

		:param in_stream: Operand music21.stream.Stream() object with musicode data in measures to be written to file.
		:param musicode_name: The name of your user-created and designed 'musicode' to be generated from said stream of measures.
		:param shorthand: The abbreviation for your musicode. (i.e, The builtin musicode "Animuse" uses the shorthand 'am'.)
		:param filepath: If this is none, the musicode will be saved in the ...\\Midas\resources\musicode_libraries folder.
		:param selection: If none, select is automatically the Latin_Script established as--
		 #Latin_Script = '''AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz  ?,;\':-.!\"()[]/  0123456789'''
		:param write: If true, directories are established appropriately and function writes to them accordingly.
		:param timeSig: Determines the time signature for the measures of your new musicode. Primarily affects measure length.
		:return: Returns a stream containing your musicode with its assigned element wrappers for quick acces.
		"""

		#Immediately update name variables.
		self.musicode_name = musicode_name
		self.sh = shorthand

		# User selection condition check.
		if selection is not None:   		##NOTE: If your selection is None, this code assumes that you are
			selection = selection			#creating a musicode FOR EVERY character in the Latin_Script.
		elif selection is None:
			selection = self.Latin_Script
		print("User Selection:", selection)

		#Critical: Selection == in_stream Length Check:
		# if len(selection) != len(in_stream):
		# 	print("Your selected string assignement does not match the length of your created musicode.")
		# 	return None

		#Establish local function(s):


		# Establish Writing Path Name (created on call of function whether writing or not, overwritten if already existing)
		#if write is not False:
		set_path = r"musicode_libraries\\"  # TODO Should resources be named something else? Regardless, this relative path is set.
		if filepath is None:  #Then we write to the r".\Midas\resources\musicode_libraries\ folder.
			filepath = set_path
			absFilePath = os.path.dirname(os.path.abspath(set_path))
			resource_path = absFilePath + "\\resources\\" + filepath
			if os.path.exists(resource_path + musicode_name + "\\\\") is True:  #Catch for fileexists error. Remove and rewrite, since will be commonly called.
				shutil.rmtree(resource_path + musicode_name + "\\\\", ignore_errors=True)  #Caution with this?
			os.mkdir(resource_path + musicode_name + "\\\\")  # TODO What should we do if directory already exists? Overwrite?
			self.full_new_musicode_path = resource_path + musicode_name + "\\\\"
			self.create_directories()		#* Create Directories within Path since write and file_path are true, and we're writing to it.
		# print(resource_path + musicode_name + "\\")
		# print(full_new_musicode_path)
		else:  ##This block executes to save to specified fullpath.
			self.full_new_musicode_path = filepath
			self.create_directories()        #Create directories...*
		# else:
		# 	pass

		#Assert for measures.
		if in_stream.hasMeasures() is False:
			in_stream.makeMeasures(inPlace=True)
		assert in_stream.hasMeasures(), "There are no measures in this stream. Call 'in_stream.makeMeasures().'"
		assert in_stream[0].isMeasure, "This first index is not a music21.stream.Measure() object."

		# and write to established directories:
		print("Selection Length:", len(selection))
		print("HERE:", selection)

		#Latin_Stream Assign with appropriate element wrappers assigned to measures.
		latin_elwrap_list = []
		selection_elwrap_list = []
		latin_measures_list =[]

		#List appended with element wrappers for all latin script characters.
		for j in range(0, len(self.Latin_Script)):  #Has len 80: j will be an iteration of measures, since we just established them.
			k = music21.ElementWrapper(obj=str(self.Latin_Script[j]))
			latin_elwrap_list.append(k)

		#List appended with element wrapers for 'selected' characters IN ORDER of selection.
		for jk in range(0, len(selection)):
			for elwrap in latin_elwrap_list:  #s will be after h
				if selection[jk] == elwrap.obj:  #TODO No it doesn't...acquire them in order of iteration over selection.
					selection_elwrap_list.append(elwrap)

		#assert len(latin_elwrap_list) == len(selection), "Elementwrapper list and selection not equal."
		print("Selection Elwrap", selection_elwrap_list)

		#List appended with measures that have the 'selected' element-wrapper characters
		#and
		#In_stream's measures having those same 'selected' element-wrappers characters appended.
		for el in range(0, len(selection)):
			print("OUR Letter Selection:", selection[el])
			# Append measures of the new musicode stream with a music21.ElementWrapper containing
			# the symbols name as it's .obj as a string.
			if selection_elwrap_list[el].obj in selection:
				in_stream[el].append(selection_elwrap_list[el]) #TODO in_stream used beyond here? Redundancy?
				latin_measures_list.append(in_stream[el])
		print("Latin Measures List:", latin_measures_list)

		#We now have our measures with the correct element-wrapped string character in them in the order of "selection."

		# Make a TimeSignature object. Does not get appended to a stream.
		time = music21.meter.TimeSignature(timeSig)
		#new_stream.append(timeSig)

		#Make new stream with measures derived from selection:
		new_stream = music21.stream.Stream()

		# Note: The default last element of a measure after stream.makeMeasures()
		# is a barline, so workarounds were done.
		print("In_STREAM:")
		in_stream.show('txt')
		for l in latin_measures_list:
			element_wrapper = l[-1]  # Last element in each measure
			if type(element_wrapper) == music21.bar.Barline:
				element_wrapper = l[-2]
			elif type(element_wrapper) == music21.note.Rest: #Check against newly added rests.
				element_wrapper = l[-3]
			if element_wrapper.obj in selection:  #Selection check for new_measure.
				new_stream.append(l)
				print("Measure Number", l.measureNumber)
				print("Measure\\ElementWrapper", l, element_wrapper)
			# wrapper_list.append(stringz)

		print("NEW_STREAM:")
		new_stream.show('txt')

		# new_stream.makeMeasures(inPlace=True)  #NOTE: makeMeasures destroys Elementwrappers??
		#Handle incomplete measure\gaps issue with added rests and
		#Reset measures in new_stream, rewriting its measure numbers in the process, just in case.
		for m in range(0, len(new_stream)):
			new_stream[m].number = m + 1
			music21funcs.fill_measure_end_gaps(new_stream[m], time, inPlace=True)

		print("New_Stream After Rests added:")
		new_stream.show('txt')

		print("NS Length:", len(new_stream))

		for j in range(0, len(selection)):
			# new_stream[j].append(wrapper_list[j])
			element_wrapper = new_stream[j][-1]  # The last element in each measure.
			if type(element_wrapper) == music21.note.Rest:
				element_wrapper = new_stream[j][-2]
			if type(element_wrapper) == music21.bar.Barline:
				element_wrapper = new_stream[j][-3]
			# print(new_stream[j].measureNumber, stringz.obj)
			print("X", [new_stream[j]])
			# A check against writing empty measures and whether to write at all.
			if element_wrapper.obj is not ' ' and write is not False:
				if new_stream[j].hasElementOfClass(music21.note.Note) or new_stream[j].hasElementOfClass(
						music21.chord.Chord):
					if element_wrapper.obj.islower() and element_wrapper.obj not in self.Punct_Names:
						new_stream[j].write("mid",
											self.full_new_musicode_path + "\\" + shorthand + "_" + "Lowercase\\" + "musicode" + "_" + shorthand + "_" + str(
												element_wrapper.obj) + ".mid")
					elif element_wrapper.obj in self.Punct_Names or element_wrapper.obj in self.Punct_Symbols:
						new_stream[j].write("mid",
											self.full_new_musicode_path + "\\" + shorthand + "_" + "Punctuation\\" + "musicode" + "_" + shorthand + "_" + str(
												self.Punct_Workaround[element_wrapper.obj]) + ".mid")
					elif element_wrapper.obj.isupper():
						new_stream[j].write("mid",
											self.full_new_musicode_path + "\\" + shorthand + "_" + "Uppercase\\" + "musicode" + "_" + shorthand + "_" + str(
												element_wrapper.obj) + ".mid")
					elif element_wrapper.obj.isdigit():
						new_stream[j].write("mid",
											self.full_new_musicode_path + "\\" + shorthand + "_" + "Numbers\\" + "musicode" + "_" + shorthand + "_" + str(
												element_wrapper.obj) + ".mid")
				else:
					pass
				# print(j, stringz.obj)

		# Account for the " " space string manually, so user is encouraged not to set a musicode for a space.
		# Append "space_measure" to user-generated musicode.
		space_measure = music21funcs.empty_measure(timeSig)
		new_stream.append(space_measure)
		print("FINAL_NEW_STREAM:")
		new_stream.show('txt')
		self.user_Created = new_stream
		return new_stream

	#UA-6.
		#def change_musicode( in_stream, musicode_sh?):


mc = Musicode()
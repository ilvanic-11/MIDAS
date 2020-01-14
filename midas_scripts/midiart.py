# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------
# Name:         midiart.py
# Purpose:      This is the top file for midiart functions
#
# Authors:      Zachary Plovanic - Lead Programmer
#               Isaac Plovanic - Creator, Director, Programmer
#
# Copyright:    MIDAS is Copyright © 2017-2019 Isaac Plovanic and Zachary Plovanic
#               music21 is Copyright © 2006-19 Michael Scott Cuthbert and the music21
#               Project
# License:      LGPL or BSD, see license.txt
# ------------------------------------------------------------------------------------


###############################################################################
# TABLE OF CONTENTS
#
# MIDIART_FUNCTIONS
# ------------------
# MA-1.  def PRINT_CHORDS_IN_PIECE(stream)
# MA-2a.  def MAKE_MIDI_FROM_PIXELS(pixels, granularity, connect, keychoice)
# MA-2b. def SET_TO_NN_COLORS((im_array, clrs=None, FL=True)
# MA-2c. def SET_PARTS_TO_MIDI_CHANNELS(in_stream, fptf)
# MA-3.  def MAKE_PIXELS_FROM_MIDI()
# MA-4.  def STRIP_MIDI_BY_CHORDS(stream, directory)
# MA-5.  def STRIP_MIDI_BY_PITCHRANGE(stream, directory, range_l, range_h)
# MA-6.  def STAGGER_PITCH_RANGE(in_stream, stepsize=1, ascending=True, starting_offset=None, range_l=0, range_h=128)
# MA-7. TODO def STAGGER_OFFSET_RANGE()
# MA-8.  def TRANSCRIBE_IMAGE_TO_MIDIART(img, height, granularity, midi_path, connect, keychoice=None)
# MA-9.  def TRANSCRIBE_IMAGE_EDGES_TO_MIDIART(( img, height, granularity, midi_path, connect, keychoice=None)
# MA-10. def TRANSCRIBE_IMAGE_CLRS_TO_MIDIART(image, outfile) #TODO More parameters.
# MA-11. def EXTRACT_SUB_MELODIES(stream, keep_dur=False, chop_durs=False, offset_interval=0.25)
# MA-12. TODO Revise? def GET_RANDOM_MELODY(in_stream)
# MA-13. def SECTIONALIZE_IMAGE_ARRAY(image_array, sec_root)
# MA-14. def RECONSTRUCT_IMAGE_SECTIONS(array_list)
###############################################################################

import music21
import random
import open3d
import numpy as np
import cv2
import math
import statistics
import fractions
import copy
from midas_scripts import music21funcs
import numpy

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

##MIDIART_FUNCTIONS
# --------------------------------------
# -----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


def filter_notes_by_key(stream, key, in_place=True):
	"""
	Removes notes from a stream, if they are not pitches that are part of the given key)
	:param stream: the input stream to operate on
	:param key: music21.key.Key object for the chosen key
	:param in_place: boolean to either operate directly on the input stream or return a deepcopy
	:return
	"""

	if in_place:
		s = stream
	else:
		s = copy.deepcopy(stream)

	print(f"Key is: {key}")
	if key == "":
		key = None
		keysig = None
	else:
		keysig = music21.key.Key(key)

	# Create the list of allowed pitches.
	allowedPitches = list()
	if key == None:
		allowedPitches = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
	elif (type(keysig) is music21.key.Key):
		for p in music21.scale.Scale.extractPitchList(keysig.getScale()):
			allowedPitches.append(p.pitchClass)
	#print(f"AllowedPitches: {allowedPitches}")

	#remove notes that aren't in allowed pitches
	for n in list(s.recurse()):
		if type(n) is music21.chord.Chord:
			for p in n.pitches:
				if (p.pitchClass not in allowedPitches):
					print(f"removed_pitch:{p}")
					n.remove(p)
		elif type(n) is music21.note.Note:
			#print(f"n.pitch.pitchClass: {n.pitch.pitchClass}")
			if (n.pitch.pitchClass not in allowedPitches):
				s.remove(n, recurse=True)
				print(f"removed_note:{n}")
	#s.show('txt')
	if in_place:
		stream = s
	return s

# MA-2.
def make_midi_from_colored_pixels(pixels, granularity, connect=False, colors=None):
	"""
	Make midiart from pixels.  Splits into colors of FLStudio piano roll.
	:param pixels: 			The 2D array of pixel values. each element of 2D array must be a tuple with RGB values (R,G,B)
	:param granularity: 	like music21's quarterlength.  4=each 'pixel' is whole note, 1=quarternote, 0.5=eightnote etc.
	:param connect: 		True means connect adjacent notes.
	:param colors			The list of colors to use.  if colors=None, will use FLStudio Piano Roll colors
	:return: music21.stream.Stream
	"""

	if len(pixels) > 128:
		raise ValueError("The .png file size is too large.")
		return None
	# Establish variables.

	part_stream = music21.stream.Stream()
	out_stream = music21.stream.Stream()

	if colors == None:
		colors = FLStudioColors

	for q in colors:
		part = music21.stream.Part()
		part.partsName = q
		part.offset = 0

		for y in range(0, len(pixels)):
			for x in range(0, len(pixels[y])):
				if tuple(pixels[y][x].flatten()) == colors[q]:
					newpitch = music21.pitch.Pitch()
					newpitch.ps = 127 - y
					n = music21.note.Note(newpitch)

					n.offset = x
					totalduration = granularity

					if connect:
						while (x + 1) < len(pixels[y]) and tuple(pixels[y][x+1].flatten()) == colors[q]:
							totalduration = totalduration + granularity

							pixels[y][x + 1] = (-1,-1,-1)
							x = x + 1

					d = music21.duration.Duration()
					d.quarterLength = totalduration
					n.duration = d
					part.insert(n.offset * granularity, copy.deepcopy(n))

		out_stream.insert(part.offset, copy.deepcopy(part))

	#print("Stream created.")
	# out_stream.show('txt')
	return out_stream



def make_midi_from_grayscale_pixels(pixels, granularity, connect=False, note_pxl_value=255):
	"""
	Make midi picture
	:param pixels: 			The 2D array of pixel values. each element is a single grayscale value.  0=Black, 255=White.
	:param granularity: 	like music21's quarterlength.  4=each 'pixel' is whole note, 1=quarternote, 0.5=eightnote etc.
	:param connect: 		True means connect adjacent notes.
	:param note_pxl_value:  note_pxl_value determines which pixels will count as notes.
								0=Black, 255=White, or any gray value 0-255.
	:
	:return: music21.stream.Stream
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
# NOTE: The variable "sparky" is maintained by python, so a file can be closed and reopened for
# (wb)writing after finishing with (rb)reading. Implement into make_midi_from_pixels() or a
# transcribe function for use with color thresholds.


# Method--OLD Notes:

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
def set_to_nn_colors(im_array, clrs=None):
	"""
	This function takes a 3D numpy color array(i.e an image), and converts all of the color tuples of that image to
	16 different colors. This allows for display in FL studio with those 16 colors.

	:param im_array: A 3D numpy image array.
	:param clrs: A user defined dictionary of colors, allowing for greater possibility of colors for future applications.
				 If clrs=None, will default to using the FLStudio Piano Roll colors

	:return:
	"""
	if clrs == None:
		clrs = FLStudioColors
	else:
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
	pcloud.points = open3d.Vector3dVector(p_array)
	kd_tree = open3d.geometry.KDTreeFlann(pcloud)

	# work_cloud = musicode.mc.array_to_lists_of(clean_cloud)
	# for x in range(1, len(work_cloud)):
	im_list = list()
	for x in range(len(im_array)):
		for y in range(len(im_array[x])):
			im_dex = np.array(im_array[x][y], dtype=np.float64)
			# im_list.append(im_dex)
			# for i in im_list:
			k_idx_list = kd_tree.search_knn_vector_3d(im_dex, 1)
			index = k_idx_list[1][0] + 1
			im_array[x][y] = clrs[index]
		# work_array = np.array(work_cloud)
		# final_array = work_array.reshape(im_array.shape)
	# return final_array
	return im_array


def set_parts_to_midi_channels(in_stream, output_file): #TODO Should be a music21funcs function?
	"""
	Assuming that notes are allocated to particular parts in a music21 stream, this function takes those parts and
	allocates them to specific midi channels in a midifile.
	This changes how midi data is imported in DAWS and the like.
	:param in_stream: Stream we are turning into a midi file.
	:param output_file: Full path to output midi full.
	:return: Writes music21.stream.Stream data to a midifile. This function doesn't return anything.
	"""

	# Create the operand .mid file from in_stream.
	in_stream.write('mid', output_file)  # Include filename.mid in fptf.

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
	#sparky.tracks
	sparky.read()
	#sparky.tracks
	# for i in range(1, len(sparky.tracks)):
	for j in clrs_list:
		if len(sparky.tracks) < 17:
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
def make_pixels_from_midi(in_stream, color=[255, 255, 255], gran=16):
	"""
	This function takes the musical offset and pitch data from a music 21 stream and converts those values back to a numpy image array.
	....gran was originally 16, for whatever reason.
	:param in_stream:
	:return: numpy array
	"""

	# temp_stream = musicode.mc.notafy(in_stream)
	# volume-z_list = list()

	a = np.zeros((127, (int(in_stream.highestTime * gran)), 3))
	# b = np.zeros((127, int(in_stream.highestTime), 3))
	# b = np.rot90(a, 1, (0, 1))
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
	Function for stripping columns of notes that comprise a music21.stream.Stream into a list of streams with those same columns of notes, i.e vertical strips of notes.
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
	Function for stripping rows of notes based on pitch that comprise a music21.stream.Stream into a list of streams with those same rows of notes, i.e horizontal strips of notes.
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
			# print(" m.offset=",repr(m.offset),", m.num=",repr(m.measureNumber),", temp.offset=",repr(temp_measure.offset),", temp.num=",repr(temp_measure.measureNumber))

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
	This functions staggers notes in a manner similar to the italicizing of text. 	So, every subsequent horizontal strip of notes above\below where you want to start
	gets cumulatively shifted in offset, as if arpeggiated, allowing for a staggered appearance.
	:param in_stream: Input stream.
	:param stepsize: Quarter length of offset step for arpeggiation.
	:param ascending:  True = ascending appegiation, False = descending arpeggiation
	:param starting_offset: Default of none uses the starting offset of the first note of lowest pitch if ascending=True, or highest if ascending=False.
							Otherwise, directly specify starting offset.
	:param range_l: Low range is specified by the starting note's offset.
	:param range_h: High range determines how many strips are to be arpeggiated in relation to the starting note's offset.
	:return: Returns a new music21.stream.Stream() object.
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
	# Step Fucking 2: Starting Offset
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
	# Step Fucking 3
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
def transcribe_colored_image_to_midiart(img, granularity=1, connect=False, keychoice=None, colors=None, output_path=None):
	"""
	This function is the commonly called transcribe function for creating musical images.
	:param im_path: A file path or numpy array of an image.
	:param granularity: quarterLength value that determines the offset and duration values of all the notes transcribed.
	:param connect: The contiguity feature. Notes are chopped by default. Connect=True connects adjacent notes contiguously.
	:param keychoice: The key of the piece, specified as a string (i.e. "C" for C Major or "C#m" for C Sharp Minor)
	:param colors: If clrs=True, note_pxl_value becomes irrelevant, and this enables the use of color tuples found in the image.
	:param output_path: Directory to which output will be written, specified as a string.

	:return: Returns a music21.stream.Stream() object.
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

	img_nn = set_to_nn_colors(img, colors)
	s = make_midi_from_colored_pixels(img_nn, granularity, connect, colors)
	filter_notes_by_key(s, keychoice, in_place=True)
	if output_path is not None:
		set_parts_to_midi_channels(s, output_path)

	return s


def transcribe_grayscale_image_to_midiart(img, granularity, connect, keychoice=None, note_pxl_value=255, output_path=None):
	"""
	This function is the commonly called transcribe function for creating musical images.
	:param img: A file path or numpy array of an image.
	:param granularity: quarterLength value that determines the offset and duration values of all the notes transcribed.
	:param connect: The contiguity feature. Notes are chopped by default. Connect=True connects adjacent notes contiguously.
	:param keychoice: The key of the piece, specified as a string (i.e. "C" for C Major or "C#m" for C Sharp Minor)
	:param note_pxl_value: When not dealing clrs, images are converted to having black and white pixels.
						A value of 255 or 0 will determine what of those pixels from the image will be turned into note
	:param output_path: Directory to which output will be written, specified as a string.

	:return: Returns a music21.stream.Stream() object.
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

	filter_notes_by_key(s, keychoice, in_place=True)

	if output_path is not None:
		s.write('mid', output_path)

	return s


# MA-9.
def transcribe_image_edges_to_midiart(image_path, height, granularity, midi_path, connect, keychoice=None, note_pxl_value=255, clrs=False):
	"""
	This function is the commonly called function for creating musical edge-detected images. It inherits parameters from "make_midi_from_pixels."
	:param image_path: A filepath or numpy array of an image.
	:param height:
	:param granularity:
	:param midi_path: Directory to which output will be written, specified as a string. i.e r"C:\\Users\Blah\blarg...."
	:param connect: The contiguity feature. Notes are chopped by default. Connect=True connects adjacent notes contiguously.
	:param keychoice: The key of the piece, specificed as a string (i.e. "C" for C Major or "C#m" for C Sharp Minor)
	:param note_pxl_value:  When not dealing clrs, images are converted to having black and white pixels. A value of 255 or 0 will determine what of those pixels from the image will be turned into notes.
	:param clrs: If clrs= True, note_pxl_value becomes irrelevant, and this enables the use of color tuples found in the image.
	:return: Returns a music21.stream.Stream() object.
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

	filter_notes_by_key(s, keychoice, in_place=True)

	s.write('mid', midi_path)
	return s



# MA-11.
def extract_sub_melodies(stream, keep_dur=False, chop_durs=False, offset_interval=0.25):
	"""
	This function creates a list of streams that are the random permutations of possible melodies of the notes found within the input music21 stream.
	Each note in the input m21 stream will only be used once in that random creation of melodies.
	:param stream: Input music21 stream.
	:param keep_dur: If true, notes longer than offset interval will be chopped up into
	individual notes of duration = offset interval.
	:param chop_durs: If chop_durs = True, notes will be chopped up into notes with duration = offset interval.
	:param offset_interval: quarterLength value determining "get_next_note" search. (4=whole note, 2=halfnote, 1=quarternote, 0.5=eighthnote,etc.)
	:return: Returns a list of streams/
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
		# :param in_stream: The music 21 stream to be input into the function.
		# :param current_offset: Current_offset is the offset input to indicate where to start looking for the "next note."
		# :param offset_interval: Granularity, the offset_interval is\uses the quarterLength feature of music21, to indicate how far to search for the "next note" after the "current offset."
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


# MA-12.
# TODO Requires revising, possibly is redundant.
def get_random_melody(in_stream):
	"""
	A smaller function than extract_sub_melodies, this function creates a stream of one melody at random from an input stream.
	:param in_stream: Stream from which a random melody will be derived.
	:return: A new music21.stream.Stream() object.
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
	This functions creates smaller, proportional "tiles" of an input image array that can be indexed. Used with the wxMidas grid.
	:param image_array: An input cv2-read image array.
	:param sec_root: The square root of the number of desired sections. If you want 64 sections, set sec_root to 8.
	:return: A list of smaller, evenly shaped arrays that, when pieced back together form the original image.
	"""
	# Initial split, right down the middle. (Or more, for very large images with high resolution.
	# if len(image_array) >= (len(image_array[1])*2):
	#     i_split = sec/4
	# else:
	#     i_split = sec/2
	# sec = sec/4
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


# MA-13
def reconstruct_image_sections(array_list):
	"""
	Sister function to sectionalize_image_array. This function takes the tiles created from that function and puts them back together into a new image\array.
	If no changes were made to any of the "tiles", than the output of this function will match exactly the input of sectionalize_image_array.
	Note: If changes are to be made to the sections, which is part of this function's goal, those sections Must retain their exact number of pixels, or the reconstruction will fail.
	:param array_list: List off sectionalized tile numpy arrays that are pieces of a larger whole.
	:return: Reconstructed image_array.
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

# MA-14.
# TODO Test this function.
def lists_of_to_array(lizt, dim=2):
	"""
	Sister function of array_to_lists_of().
	Takes coordinate lists (2D numpy arrays) or color lists of cv2.imreads (3D arrays) and turns them
	back into numpy arrays with the appropriate shape and ndim.
	More advanced use may use more dimensions. This is not supported yet.
	:param lizt: A python list of array coordinates or color tuples. (typically)
	:param dim: Number of desired dimensions. 2 by default, otherwise will probably be 3,
	in order to return lizt to original cv2 numpy array.
	:return: Numpy array.
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
		new_array = array.reshape(statistics.median_low(f_list), statistics.median_high(f_list), 3)
		return new_array
	else:
		return array


# MA-15.
# TODO Test this function.
def array_to_lists_of(coords_array, tupl=True):
	"""
	Sister function of lists_of_to_array().
	This function turns numpy arrays into a list of coordinate lists\tuples or color lists\tuples.
	This functionality is contingent upon the input arrays ndim.
	Useful for compare calls requiring numpy data without wanting to use .any() or .all()...among other uses.

	:param coords_array: Input 2D coordinate array or cv2.imread 3D array of color tuples. (i.e. a picture)
	:param tupl: Determines whether or not you want the parent list populated with the data as lists or tuples.
	:return: A List of lists or tuples.
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
		print("Suggested ndim should be 2 or three.")
		return None


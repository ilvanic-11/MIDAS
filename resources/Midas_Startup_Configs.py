from importlib import reload
print("Imported function", reload)
from traits.etsconfig.api import ETSConfig
#ETSConfig.toolkit = 'wx'
import mayavi
print("Imported", mayavi)
from mayavi import mlab
print("Imported", mlab)
import numpy
import numpy as np
print("Imported (and as 'np')", numpy)
import sympy
print("Imported", sympy)
import music21
print("Imported", music21)
import open3d
print("Imported", open3d)
import cv2
print("Imported", cv2)
import vtk
print("Imported", vtk)
import tvtk
print("Imported", tvtk)
from midas_scripts import musicode
print("Imported", musicode)
from midas_scripts import midiart
print("Imported", midiart)
from midas_scripts import midiart3D
print("Imported", midiart3D)
from midas_scripts import music21funcs
print("Imported", music21funcs)
import os
print("Imported", os)
import collections
print("Imported", collections)
import re
print("Imported", re)
import copy
print("Imported", copy)

###Main path.
script = "Midas_Startup_Configs.py"
intermediary_path = "intermediary_path"
script_path = os.path.dirname(os.path.abspath(script))
resource_path = script_path + "\\resources\\"
full_configs_path = resource_path + script
#print(str(resource_path + intermediary_path + "\\"))
intermediary_path = resource_path + intermediary_path + "\\"

###My local paths.
if script_path == "C:\\Users\\Isaac's\\Midas":
      musicode_path = r'''C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\musicode_path\\'''
      midiart_path = r'''C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\midiart_path\\'''
      colormidiart_path = r'''C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\midiartcolor_path\\'''
      thridiart_path = r'''C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\midiart3D_path\\'''
      test_path = r'''C:\Users\Isaac\'s\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\\'''
      scratch_path = r'''C:\Users\Isaac's\Desktop\Scratch\\'''
else:
      pass



print("Successfully imported all paths.")
print('\n')
print("----Welcome to MIDAS, the Music-Intermediary Digital Art Suite.----")
print('\n')
print('     Using knowledge and techniques of python, music21, numpy, opencv-python, open3d, vtk, and mayavi, this gui toolkit provides a musical engineer \n'
      'with the ability to transform text, images, and point clouds into musical data for composing, production and visualization purposes. \n'
      'MIDAS incorporates strong musicological analyses displays as well as grants the user the ability to rapidly manipulate their musical data via input\output methods \n'
      'to and from other programs such as MuseScore, FL Studio, NotePad++, Word, Paint\PicPick, and even Blender. \n'
      'The MIDAS installation possesses a path called "intermediary_path" assigned as a variable, and this path is the traffic hub for said data manipulation; the transformation and manipulation \n'
      'of all files and data that go through this toolkit ideally will use the "intermediary_path".\n'
      'This path is established for ease of using this embedded python interpreter and it can be assigned as an output for all your other programs.\n\n'
      '----We hope you enjoy MIDAS.----')
print('\n')


midas_test = music21.stream.Stream()
n1 = music21.note.Note("C")
n2 = music21.note.Note("E")
n3 = music21.note.Note("A")
chord1 = music21.chord.Chord("D F A")
chord2 = music21.chord.Chord("G B D")
dur1 = music21.duration.Duration()
dur2 = music21.duration.Duration()
dur1.quarterLength = 3
dur2.quarterLength = 4
midas_test.append(n1)
midas_test.append(n2)
midas_test.append(n3)
midas_test.append(chord1)
midas_test.append(chord2)


##Call
# exec(open(r"%s" % full_path).read())
#exec(open(str(os.getcwd()) + "\\resources\\" + "Midas_Startup_Configs.py").read())
#import musicode
#import g
#g.mc = musicode.Musicode()
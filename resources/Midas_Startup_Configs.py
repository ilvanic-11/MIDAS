from importlib import reload
print("Imported function", reload)
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

#g.mc = musicode.Musicode()
musicode_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\Musicode Fun!\\"
midiart_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\Midi-Art Fun!\\"
colormidiart_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\ColorMidiArt Fun!\\"
thridiart_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\3idiArt Fun!\\"
test_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\\"
scratch_path = r"C:\Users\Isaac's\Desktop\Scratch\\"
#intermediary_path = r"C:\Users\Isaac's\Desktop\Isaacs_Synth_Music_Source_Folder\FL\Workflow\9_Scribed_Musicode_Midi\Midas Intermediary\\"
intermediary_path = r"Midas\resources\intermediary_path\\"
print("Successfully imported all paths.")
##Call
# import os
# script = "Midas_Startup_Configs.py"
# script_path = os.path.dirname(os.path.abspath(script))
# full_path = script_path + "\\resources\\" + script
# exec(open(r"%s" % full_path).read())

#import musicode
#import g

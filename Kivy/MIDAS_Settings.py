#Separate file to hold all the settings that the user chooses in the GUI
import os
from midas_scripts import midiart

print("CWD_KIVY_FILEPATH", r".\resources")
print("CWD_KIVY_FILEPATH", os.getcwd())


###MIDAS_kivy Settings###
musicode_name = ""
noteHeight = 127
#granularity would be "Note Durations", but left as "8th Note" so user will still get a result on startup if
# they haven't made a manually selection yet.
granularity = "8th Note"
connectNotes = True #Since FL Studio has it's own Chop, it is faster to set this to True and achieve the same results.
key = ""
key_list = ["A", "A#m", "Ab", "Abm", "Am", "B", "Bb", "Bbm", "Bm", "C", "C#", "C#m", "Cb", "Cm", "D", "D#m", "Db", "Dm", "E", "Eb", "Ebm", "Em", "F", "F#", "F#m", "Fm", "G", "G#m" ,"Gb", "Gm"]
color = "FLStudioColors"
filepath = r".\resources\intermediary_path"
font_name = r".\resources\terminat.ttf"   ##C:\Users\Isaac's\Midas\Kivy\resources\terminat.ttf
#granularity_num = None


###Image Resources###

#image = r"C:\Users\Isaac's\Desktop\PicPick AutoSave-T\Image 1533.png"

welcome = r".\resources\welcome_banner.png"
welcome_default = r".\resources\welcome_banner.png"

image = r".\resources\MIDAS_Mobile_splash.png"
last_image = ""
default_image = r".\resources\MIDAS_Mobile_splash.png"


piano = r".\resources\ThePiano16.png"
phatpiano = r".\resources\ThePhatPiano16.png"
phatpiano2 = r".\resources\ThePhatPiano32.png"

musicode_banner = r".\resources\musicode_banner.png"
musicodes_visual = r".\resources\musicodes_visual.png"

midiart_banner = r".\resources\midiart_banner.png"
midiart_visual = r".\resources\midiart_visual.png"

credits_banner = r".\resources\credits_banner.png"
credits_visual = r".\resources\credits_visual.png"

support_banner = r".\resources\support_banner.png"

button_normal = r".\resources\coffee_button_background.png"
button_down = r".\resources\button_pressed_modified.png"
button_default = r".\resources\button_pressed_default.png"
#compensation_banner = r".\resources\image_view_button_placeholder.png"


clr_dict_list = midiart.get_color_palettes(r".\resources\color_palettes")
#clr_dict_list.update([("FLStudioColors", midiart.FLStudioColors)])
#current_color_palette = clr_dict_list["FLStudioColors"]
current_color_palette = clr_dict_list['000_flstudio-16-1x']
#urrent_mayavi_palette = midiart.convert_dict_colors(current_color_palette, both=True)





#Use this with ncp=True to refresh color_palettes AND FL ncp files:
#PLACE the ncp files INSIDE this:
#-->  C:\Users\<your_home_folder_name>\Documents\Image-Line\Data\FL Studio\Settings\Note color presets    folder.
#This functionality is not intended for FL Studio Mobile; it is intended instead for FL Studio >= 20
#midiart.get_color_palettes(r".\resources\color_palettes", ncp=True)
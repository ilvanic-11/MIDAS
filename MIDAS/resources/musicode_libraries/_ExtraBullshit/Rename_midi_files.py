
shorthand = {
             "Animuse"        : "am",
             "Asciipher_X"    : "asciix",
             "Asciipher_Y"    : "asciiy",
             "BraillePulse"   : "bp",
             "MetaMorse"      : "mm",
             "POWerTap_X"     : "ptx",
             "POWerTap_Y"     : "pty",
             "Splyce"         : "splyce",
             }

newshorthand = {
             "Animuse"        : "am",
             "Asciipher_X"    : "asciiX",
             "Asciipher_Y"    : "asciiY",
             "BraillePulse"   : "bp",
             "MetaMorse"      : "mm",
             "POWerTap_X"     : "ptX",
             "POWerTap_Y"     : "ptY",
             "Splyce"         : "splyce",
             }
Musicode_Path = r"C:\Users\Isaac's\Desktop\Isaac's Synth Music Source Folder\FL\Tower Projects File\10_Musicode Libraries"

import re
import os
for musicode in ("POWerTap_X", "POWerTap_Y", "Asciipher_X", "Asciipher_Y"):
    sh = shorthand[musicode]

    for pack in ("Lowercase", "Uppercase", "Numbers", "Punctuation"):
        directory = Musicode_Path + "\\" + musicode + "\\" + sh + "_" + pack
        filenames = next(os.walk(directory))[2]
        for file in filenames:
            my_search = re.search(r"musicode_%s_(\w+|\number+).mid"% sh, file)
            if my_search:
                newname = "musicode_" + newshorthand[musicode] + "_" + my_search.group(1) + ".mid"
                print(file + " | " + newname +"\n")
                os.rename(directory+"\\"+file, directory+"\\"+newname)
        newdir = Musicode_Path + "\\" + musicode + "\\" + newshorthand[musicode] + "_" + pack
        os.rename(directory, newdir)

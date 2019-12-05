test_path = r"C:\Users\Isaac's\Desktop\Isaac's Synth Music Source Folder\FL\Tower Projects File\9_Scribed Musicode Midi\\"

#All Musicode Quick Translate Script
    #Instructions:
        #1. Replace "MCQW" with the name of your poem/file to be translated. Find and replace all.
        #2. Replace "Insert_Text_Here" with "text" to be translated.
        #3. Run program.
        #4. Find exported midi in export directory. Import to desired DAW.
MCQW_bp = translate("BraillePulse", "Insert_Text_Here")
MCQW_bp.write("mid", test_path + "MCQW_bp.mid")
MCQW_mm = translate("MetaMorse", "Insert_Text_Here")
MCQW_mm.write("mid", test_path + "MCQW_mm.mid")
MCQW_am = translate("Animuse", "Insert_Text_Here")
MCQW_am.write("mid", test_path + "MCQW_am.mid")
MCQW_asciiX = translate("Asciipher_X", "Insert_Text_Here")
MCQW_asciiX.write("mid", test_path + "MCQW_asciiX.mid")
MCQW_asciiY = translate("Asciipher_Y", "Insert_Text_Here")
MCQW_asciiY.write("mid", test_path + "MCQW_asciiY.mid")
MCQW_ptX = translate("POWerTap_X", "Insert_Text_Here")
MCQW_ptX.write("mid", test_path + "MCQW_ptX.mid")
MCQW_ptY= translate("POWerTap_Y", "Insert_Text_Here")
MCQW_ptY.write("mid", test_path + "MCQW_ptY.mid")
MCQW_splyce = translate("Splyce", "Asshat")


bw = midiart.transcribe_bw_image_to_midiart(r"test\testimages\front_small.png", 1, False, "C", 255)
a = ""
for x in bw.recurse():
    a += str(x)
print(a)
import unittest
import music21
from midas_scripts import  midiart   ###, midiart3D, music21funcs, musicode
import cv2
import numpy as np

class TestMIDAS(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class MIDASTestCases(TestMIDAS):

    # define all the test cases here
    # def test_transpose_measure_by_random(self):
    #     # do your shit
    #     s = musicode.mc.translate("Animuse", "testicles")
    #     t = musicode.mc.transpose_all_measures_by_random(s)
    #
    #     self.assertIsNotNone(t)
    #     self.assertNotEqual(s,t)

    def test_whateveryouwant(self):
        pass


    def tearDown(self):
        pass



class MidiartTestCases(TestMIDAS):

    def test_filter_notes_by_key(self):
        self.maxDiff = None
        s = music21.converter.parse("tinyNotation: A#4 B4 C#4 C4 D#4 D4 E4 E4 F#4 F4")
        s.insert(music21.chord.Chord(["A5","B5","B#5","C5","C#5","D5","D#5"]))

        expected_str = self.get_file_text(r"test\teststrings\output_filter_notes_by_key_01.txt")
        filtered = midiart.filter_notes_by_key(s,"C", in_place=False)
        actual_str = self.stream_string(filtered)
        self.assertEqual(actual_str, expected_str)

        #test it in_place
        midiart.filter_notes_by_key(s,"C", in_place=True)
        inplace_str = self.stream_string(s)
        self.assertEqual(actual_str, inplace_str)

    def test_transcribe_greyscale_image_to_midiart(self):

        #
        bw = midiart.transcribe_grayscale_image_to_midiart(r"test\testimages\front_small.png", 1, False, "C", 255)
        expected_str = self.get_file_text(r"test\teststrings\output_transcribe_bw_image_01.txt")
        actual_str = self.stream_string(bw)
        self.assertEqual(expected_str, actual_str)

        #test with no key
        bw = midiart.transcribe_grayscale_image_to_midiart(r"test\testimages\front_small.png", 1, False, None, 255)
        expected_str = self.get_file_text(r"test\teststrings\output_transcribe_bw_image_02.txt")
        actual_str = self.stream_string(bw)
        self.assertEqual(expected_str, actual_str)

        #test bigger granularity, Connect, and using 0 (white) for pixel_note_value
        bw = midiart.transcribe_grayscale_image_to_midiart(r"test\testimages\front_small.png", 2, True, None, 0)
        expected_str = self.get_file_text(r"test\teststrings\output_transcribe_bw_image_03.txt")
        actual_str = self.stream_string(bw)
        self.assertEqual(expected_str, actual_str)

    def stream_string(self, stream):
        s = ""
        for x in stream.recurse():
            s += str(x)
        return s

    def get_file_text(self, file):
        f = open(file, "r")
        s = f.read()
        f.close()
        return s


def suite():
    return (unittest.TestLoader.loadTestsFromTestCase(MIDASTestCases) and
            unittest.TestLoader.loadTestsFromTestCase(MidiartTestCases)
            )

if __name__ == '__main__':
    unittest.main()
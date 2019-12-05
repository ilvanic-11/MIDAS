import unittest
import music21
from midas_scripts import musicode, midiart, midiart3D, music21funcs

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

    def test_whateverthefuckyouwant(self):
        pass



class TestMidiart(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class MidiartTestCases(TestMidiart):

    def test_filter_notes_by_key(self):
        s = music21.converter.parse("tinyNotation: A#4 B4 C#4 C4 D#4 D4 E4 E4 F#4 F4")
        s.insert(music21.chord.Chord(["A5","B5","B#5","C5","C#5","D5","D#5"]))

        expected_str = "<music21.stream.Measure 1 offset=0.0>" \
                       "<music21.clef.BassClef>" \
                       "<music21.meter.TimeSignature 4/4>" \
                       "<music21.note.Note A#>" \
                       "<music21.note.Note C#>" \
                       "<music21.chord.Chord C#5 D#5>" \
                       "<music21.stream.Measure 2 offset=4.0>" \
                       "<music21.note.Note D#>" \
                       "<music21.stream.Measure 3 offset=8.0>" \
                       "<music21.note.Note F#>" \
                       "<music21.bar.Barline style=final>"

        actual_str = ""
        filtered = midiart.filter_notes_by_key(s,"C", in_place=False)
        for x in filtered.recurse():
            actual_str += str(x)
        self.assertEqual(actual_str, expected_str)

        #test it in_place
        midiart.filter_notes_by_key(s,"C", in_place=True)
        inplace_str = ""
        for x in s.recurse():
            inplace_str += str(x)
        self.assertEqual(actual_str, inplace_str)


def suite():
    return (unittest.TestLoader.loadTestsFromTestCase(MIDASTestCases) and
            unittest.TestLoader.loadTestsFromTestCase(MidiartTestCases)
            )

if __name__ == '__main__':
    unittest.main()
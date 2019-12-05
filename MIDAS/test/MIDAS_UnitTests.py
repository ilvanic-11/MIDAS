

import unittest

class TestMIDAS(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class TestCases(TestMIDAS):

    # define all the test cases here
    def test_transpose_measure_by_random(self):
        # do your shit
        s = musicode.mc.translate("Animuse", "testicles")
        t = musicode.mc.transpose_all_measures_by_random(s)

        self.assertIsNotNone(t)
        self.assertNotEqual(s,t)

    def test_whateverthefuckyouwant(self):






def suite():

    return unittest.TestLoader.loadTestsFromTestCase(TestCases)

if __name__ == '__main__':
    unittest.main()
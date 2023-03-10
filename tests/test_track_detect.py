from pathlib import Path
import unittest

import cv2

from detect_track import detect_track

class TestTrackDetect(unittest.TestCase):
    def test_1(self):
        file = Path(__file__).parent / "data" / "track_test_41.png"
        im = cv2.imread(str(file))
        result = detect_track(im)
        self.assertEqual(result, 41)

    def test_none_1(self):
        file = Path(__file__).parent / "data" / "track_test_none_1.png"
        im = cv2.imread(str(file))
        result = detect_track(im)
        self.assertEqual(result, None)

    def test_none_2(self):
        file = Path(__file__).parent / "data" / "track_test_none_2.png"
        im = cv2.imread(str(file))
        result = detect_track(im)
        self.assertEqual(result, None)

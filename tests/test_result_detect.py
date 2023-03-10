from pathlib import Path
import unittest

import cv2

from mktools_client.trim_numbers import im2resulttime

class TestResultDetect(unittest.TestCase):
    def test_1(self):
        file = Path(__file__).parent / "data" / "result_test_1.png"
        im = cv2.imread(str(file))
        result = im2resulttime(im)
        self.assertEqual(result['sum'], "240154")
        self.assertEqual(result['laps'][0], "055095")
        self.assertEqual(result['laps'][1], "052334")
        self.assertEqual(result['laps'][2], "052725")

    def test_none(self):
        file = Path(__file__).parent / "data" / "result_test_none.png"
        im = cv2.imread(str(file))
        result = im2resulttime(im)
        self.assertEqual(result, None)

from pathlib import Path
import unittest

import cv2

from mktools_client.image.ta_result import detect_ta_result, validate_ta_result

class TestResultDetect(unittest.TestCase):
    def test_1(self):
        file = Path(__file__).parent / "data" / "result_test_1.png"
        im = cv2.imread(str(file))
        result = detect_ta_result(im)
        self.assertEqual(result['sum'], "240154")
        self.assertEqual(result['laps'][0], "055095")
        self.assertEqual(result['laps'][1], "052334")
        self.assertEqual(result['laps'][2], "052725")
        self.assertEqual(validate_ta_result(result), True)

    def test_none(self):
        file = Path(__file__).parent / "data" / "result_test_none.png"
        im = cv2.imread(str(file))
        result = detect_ta_result(im)
        self.assertEqual(result, None)

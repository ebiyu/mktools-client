from functools import cache
from pathlib import Path

import cv2
import numpy as np

@cache
def load_template_images():
    template_images = [None]
    for i in range(1, 81):
        template_images.append(cv2.imread(str(Path(__file__).parent.parent / "data" /  f"tracks/{i}.png")))
    return template_images

def get_ta_area_2bin(frame, inverse=False):
    """
    TAのコース名部分を切り出して二値化する
    """
    cropped = frame[950:1030, 500:1260, :]
    cropped_gray= cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    mode = cv2.THRESH_OTSU + (cv2.THRESH_BINARY_INV if inverse else cv2.THRESH_BINARY)
    _, cropped_bin = cv2.threshold(cropped_gray, None, 255, mode)
    return cropped_bin

def detect_track(frame, prev_im=None):
    template_images = load_template_images()

    differences = [1] # それぞれのコースとどれだけ離れているか 1がmax
    for track_id, im in enumerate(template_images):
        if im is None:
            continue

        # 差分を計算してリストに格納する
        frame_ta_area = get_ta_area_2bin(frame)
        template_ta_area = get_ta_area_2bin(im)
        diff = np.logical_xor(frame_ta_area, template_ta_area)
        diff_rate = np.count_nonzero(diff) / diff.size

        differences.append(diff_rate)

    result_difference = min(differences)
    track_id = differences.index(result_difference)
    is_ok = result_difference < 0.001

    if prev_im is not None:
        color = (0, 0, 255) if is_ok else (128, 128, 128)
        cv2.rectangle(prev_im, (500, 950), (1260, 1030), color, 5)
        cv2.putText(
            prev_im,
            f'{track_id} (diff: {result_difference:.5f})',
            (1280, 915), 
            fontFace=cv2.FONT_HERSHEY_TRIPLEX,
            fontScale=1.0,
            color=color,
            thickness=2,
            lineType=cv2.LINE_4,
        )

    # 正解判定の閾値
    if is_ok:
        return track_id
    else:
        return None

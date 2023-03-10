from functools import cache
from pathlib import Path

import cv2
import numpy as np

@cache
def load_template_images():
    template_images = [None]
    for i in range(1, 81):
        template_images.append(cv2.imread(str(Path(__file__).parent / "data" /  f"tracks/{i}.png")))
    return template_images

def detect_track(frame, prev_im=None):
    template_images = load_template_images()

    im1 = template_images[1]
    assert im1.shape[0] == 1080
    assert im1.shape[1] == 1920

        
    # detect TA
    im1_cropped = im1[940:1045, 500:1260, :]
    frm_cropped = frame[940:1045, 500:1260, :]
    diff = cv2.subtract(im1_cropped, frm_cropped)
    diff_gray= cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, diff_bin = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
    diff_bin_gray = cv2.cvtColor(diff_bin, cv2.COLOR_BGR2GRAY)

    is_ta = np.count_nonzero(diff_bin_gray) < diff_bin_gray.size * 0.2

    # 画像の表示
    if is_ta:
        differences = [1]
        for i, im in enumerate(template_images):
            if im is None:
                continue
            im_cropped = im[915:1045, 1280:1480, :]
            frm_cropped = frame[915:1045, 1280:1480, :]
            diff = cv2.subtract(im_cropped, frm_cropped)
            diff_gray= cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, diff_bin = cv2.threshold(diff, 3, 255, cv2.THRESH_BINARY)
            differences.append(np.count_nonzero(diff_bin) / diff_bin.size)

        is_ok = min(differences) < 0.05
        if is_ok:
            i = differences.index(min(differences))
            if prev_im is not None:
                cv2.rectangle(prev_im, (1280, 915), (1480, 1045), (0, 0, 255), 5)
                cv2.putText(prev_im, str(i), (1280, 915), 
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1.0,
                        color=(0, 0, 255),
                        thickness=2,
                        lineType=cv2.LINE_4)
            return i
        else:
            if prev_im is not None:
                cv2.rectangle(prev_im, (1280, 915), (1480, 1045), (0, 0, 0), 5)
            return None

if __name__ == '__main__':

    # カメラをオープンする
    capture = cv2.VideoCapture(0)

    # カメラがオープン出来たか？
    camera_opened = capture.isOpened()

    while camera_opened:

        # フレーム画像の取得
        ret, frame = capture.read()
        frame_copy = frame.copy()

        i = detect_track(frame, frame_copy)

        cv2.imshow("Image", frame_copy)

        if cv2.waitKey(1) != -1:
            break

    capture.release()
    cv2.destroyAllWindows()

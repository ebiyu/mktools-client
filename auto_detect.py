from collections import deque

import device
import cv2

from trim_numbers import im2resulttime
from api import register_record, get_token
from detect_track import detect_track

#track = int(input("Please input track ID > "))
track = -1
get_token()

print(device.getDeviceList())

# カメラをオープンする
capture = cv2.VideoCapture(0)

# カメラがオープン出来たか？
camera_opened = capture.isOpened()

class ResultQueue:
    def __init__(self, maxlen):
        self.queue = deque(maxlen=maxlen)

    def put(self, val):
        self.queue.append(val)

    def get(self):
        """
        ダメだったらNone
        """
        l = list(self.queue)
        if len(l) == 0:
            return None
        ret = l[0]
        for val in l[1:]:
            if val != ret:
                return None
        return ret

track_queue = ResultQueue(5)

def sixdigit2sec(txt):
    m = int(txt[0])
    s = int(txt[1:3])
    f = int(txt[3:])
    return m * 60 + s + f / 1000

def format_6digit(txt):
    m = txt[0]
    s = txt[1:3]
    f = txt[3:]
    return f"{m}'{s}\"{f}"
    pass

detecting = False
while camera_opened:

    # フレーム画像の取得
    ret, frame = capture.read()
    prev_im = frame.copy()
    

    #detected_track = detect_track(frame)
    track_queue.put(detect_track(frame))

    if track_queue.get() is not None:
        track = track_queue.get()

    result = im2resulttime(frame)
    if result is not None:
        sum_secs = sixdigit2sec(result["sum"])
        sum_secs_lap = 0
        for txt in result["laps"]:
            sum_secs_lap += sixdigit2sec(txt)
        
        if abs(sum_secs - sum_secs_lap) < 0.01:
            if not detecting:
                register_record(result["sum"], track, "/".join(map(format_6digit, result["laps"])))
                print(result)
            detecting = True
        else:
            detecting = False
    else:
        detecting = False

    # 画像の表示

    cv2.putText(prev_im, f"track: {track}", (10, 50), 
    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
            fontScale=1.0,
            color=(0, 0, 255),
            thickness=2,
            lineType=cv2.LINE_4)
    cv2.imshow("Image", prev_im)

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()

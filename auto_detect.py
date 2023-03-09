import device
import cv2

from trim_numbers import im2resulttime
from api import register_record, get_token

track = int(input("Please input track ID > "))
get_token()

print(device.getDeviceList())

# カメラをオープンする
capture = cv2.VideoCapture(0)

# カメラがオープン出来たか？
camera_opened = capture.isOpened()

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
    
    # 画像の表示
    cv2.imshow("Image", frame)

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

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()

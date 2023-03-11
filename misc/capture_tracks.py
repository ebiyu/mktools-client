import datetime

import device
import cv2

if __name__ == "__main__":
    print(device.getDeviceList())

    # カメラをオープンする
    capture = cv2.VideoCapture(0)

    # カメラがオープン出来たか？
    camera_opened = capture.isOpened()

    track_id = 81
    while camera_opened:

        # フレーム画像の取得
        ret, frame = capture.read()
        
        # 画像の表示
        cv2.imshow("Image", frame)

        if cv2.waitKey(1) != -1:
            # キー入力で終了
            cv2.imwrite(f"tracks/{track_id}.png", frame)
            track_id += 1
            if track_id > 88:
                break

    capture.release()
    cv2.destroyAllWindows()

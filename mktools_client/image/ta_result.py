import cv2
import numpy as np

def digits2num(arr):
    # 上 左上 右上 中央 左下 右下 下
    segments = [
        (1, 1, 1, 0, 1, 1, 1),  #0
        (0, 0, 1, 0, 0, 1, 0),  #1
        (1, 0, 1, 1, 1, 0, 1),  #2
        (1, 0, 1, 1, 0, 1, 1),  #3
        (0, 1, 1, 1, 0, 1, 0),  #4
        (1, 1, 0, 1, 0, 1, 1),  #5
        (1, 1, 0, 1, 1, 1, 1),  #6
        (1, 0, 1, 0, 0, 1, 0),  #7
        (1, 1, 1, 1, 1, 1, 1),  #8
        (1, 1, 1, 1, 0, 1, 1),  #9
    ]
    for i, right in enumerate(segments):
        if tuple(arr) == right:
            return i
    return -1

def img2num(im, reverse=False):
    cropped_image_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    h, w = cropped_image_gray.shape
    t = w // 4
    ret, cropped_image_bin = cv2.threshold(cropped_image_gray, 0, 255, cv2.THRESH_OTSU)

    segments = [
        # x1, y1, x2, y2
        (0, w, 0, t), # 上
        (0, t, 0, h // 2), # 左上
        (w - t, w, 0, h // 2), # 右上
        (0, w, h // 2 - t // 2, h // 2 + t // 2), # 中央
        (0, t, h // 2, h), # 左下
        (w - t, w, h // 2, h), # 右下
        (0, w, h - t, h), # 下
    ]
    on_arr = []
    for i, (x1, x2, y1, y2) in enumerate(segments):
        if x2 - x1 > y2 - y1:
            x1 += t // 2
            x2 -= t // 2
        else:
            y1 += t // 2
            y2 -= t // 2

        cropped_segment_image_bin = cropped_image_bin[y1:y2, x1:x2]
        is_on = np.count_nonzero(cropped_segment_image_bin) > cropped_segment_image_bin.size / 2
        if reverse:
            is_on = not is_on
        on_arr.append(1 if is_on else 0)
    return digits2num(on_arr)

def im2time_noofset(im, *, offset_y=0, preview=False):
    assert im.shape[0] == 1080
    assert im.shape[1] == 1920

    if preview:
        im_copy = im.copy()

    start_points = [
        (1566, 224 + offset_y),
        (1615, 224 + offset_y),
        (1649, 224 + offset_y),
        (1698, 224 + offset_y),
        (1733, 224 + offset_y),
        (1767, 224 + offset_y),
    ]

    start_points_sub_x = [
        1579,
        1618,
        1648,
        1686,
        1715,
        1744,
    ]

    start_points_sub_y = [
        316 + offset_y,
        382 + offset_y,
        448 + offset_y,
    ]

    result_sum = []
    for x, y in start_points:
        w = 30
        h = 45
        num = img2num(im[y:y+h, x:x+w, :])
        if num == -1:
            return None
        result_sum.append(str(num))

        if preview:
            cv2.rectangle(im_copy, (x, y), (x + w, y  + h), (0, 255, 0), 1)
            cv2.putText(im_copy, str(num), (x, y), 
            fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    fontScale=1.0,
                    color=(0, 0, 255),
                    thickness=2,
                    lineType=cv2.LINE_4)

    result_laps = []
    for y in start_points_sub_y:
        result_current_lap = []
        for x in start_points_sub_x:
            w = 25
            h = 38
            num = img2num(im[y:y+h, x:x+w, :], reverse=True)
            if num == -1:
                return None
            result_current_lap.append(str(num))

            if preview:
                cv2.rectangle(im_copy, (x, y), (x + w, y  + h), (0, 255, 0), 1)
                cv2.putText(im_copy, str(num), (x, y), 
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                        fontScale=1.0,
                        color=(0, 0, 255),
                        thickness=2,
                        lineType=cv2.LINE_4)
        result_laps.append(result_current_lap)

    if preview:
        cv2.imshow("Image", im_copy)
        cv2.waitKey()
    return {
        "sum": "".join(result_sum),
        "laps": ["".join(lap) for lap in result_laps],
    }

def im2resulttime(im, *,preview=False):
    return im2time_noofset(im, preview=preview) or im2time_noofset(im, offset_y=-45, preview=preview)

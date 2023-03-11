from logging import getLogger
from collections import deque

from .image.ta_result import detect_ta_result, validate_ta_result
from .image.ta_track import detect_track

logger = getLogger(__name__)

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


class Reader:
    track = None
    result = None
    track_queue = ResultQueue(5)

    def process_frame(self, im, im_prev):
        detected_track = detect_track(im, im_prev)
        self.track_queue.put(detected_track)

        if self.track_queue.get() is not None:
            self.track = self.track_queue.get()

        result = detect_ta_result(im, im_prev)
        if validate_ta_result(result):
            self.result = result
        else:
            self.result = None

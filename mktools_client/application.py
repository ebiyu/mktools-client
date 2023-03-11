import tkinter as tk
from tkinter import ttk
from time import sleep
from logging import getLogger
import threading

import cv2
import device
from PIL import Image, ImageOps, ImageTk

from .reader import Reader
from .api import register_record, get_track_info
from .util import format_6digit

logger = getLogger(__name__)

# windows dpi workaround
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2) 
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass


class Application(tk.Frame):
    record_sent = False
    track_info_txt_list = None

    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill=tk.BOTH)

        master.title("mktools-client")
        master.geometry("800x600")

        self.video_loop_id = None

        self.device_list = list(map(lambda x:x[0], device.getDeviceList()))
        self.active_capture_index = None
        self.capture = None

        cv2.CV_CAP_PROP_FPS = 60

        button_frm = tk.Frame(self, width=400)
        button_frm.pack(expand=False, fill=tk.Y, anchor=tk.E, side=tk.RIGHT)

        self.video_text_var = tk.StringVar()
        select = ttk.Combobox(button_frm, textvariable=self.video_text_var, state="readonly", values=self.device_list)
        select.bind("<<ComboboxSelected>>", self.on_device_change)
        select.pack(padx=10, pady=10)

        button = tk.Button(button_frm, text="Open Preview", command=self.open_subwin)
        button.pack(padx=10, pady=10)

        self.track_info_var = tk.StringVar()
        track_info_label = tk.Label(button_frm, textvariable=self.track_info_var, justify='left')
        track_info_label.pack(padx=10, pady=10)

        # create canvas
        self.video_button = tk.Button(self, borderwidth=0)
        self.video_button.pack(expand=True, fill=tk.BOTH, anchor=tk.E)

        self.subwin = None
        self.sub_video_button = None

        self.reader = Reader()

        self.running = True
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    def on_device_change(self, *args, **kwargs):
        # TODO: handle args
        if self.video_text_var.get() not in self.device_list:
            return

        next_capture_index = self.device_list.index(self.video_text_var.get())
        if self.active_capture_index == next_capture_index:
            return

        if self.capture is not None:
            self.capture.release()

        self.active_capture_index = next_capture_index
        self.capture = cv2.VideoCapture(self.active_capture_index)

    def open_subwin(self):
        if self.sub_video_button is not None:
            return

        self.subwin = tk.Toplevel()
        self.subwin.title("mktools-preview")
        self.subwin.state("zoomed")
        self.subwin.protocol("WM_DELETE_WINDOW", self.on_delete_subwin)

        self.sub_video_button = tk.Button(self.subwin)
        self.sub_video_button.pack(expand=True, fill=tk.BOTH)

    def on_delete_subwin(self):
        self.sub_video_button = None
        self.subwin.destroy()
        self.subwin = None

    def draw_on_sub_canvas(self, im):
        if self.sub_video_button is None:
            return

        cv_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        canvas_width = self.sub_video_button.winfo_width()
        canvas_height = self.sub_video_button.winfo_height()

        # resize image
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        photo_image = ImageTk.PhotoImage(image=pil_image)
        self.sub_video_button.config(image=photo_image)
        # this must be stored to class to prevent from being destroied
        self.photo_image_sub = photo_image

    def draw_on_canvas(self, im):
        cv_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        canvas_width = self.video_button.winfo_width()
        canvas_height = self.video_button.winfo_height()

        # resize image
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        photo_image = ImageTk.PhotoImage(image=pil_image)
        self.video_button.config(image=photo_image)
        # this must be stored to class to prevent from being destroied
        self.photo_image = photo_image

    def start(self):
        while self.running:
            self.update_video()

            self.update_idletasks()
            self.update()

    def update_video(self):
        if self.capture is None: return

        ret, im = self.capture.read()
        if not ret: return

        im_prev = im.copy()
        self.reader.process_frame(im, im_prev)
        if self.reader.track:
            def fetch_func():
                try:
                    track_info = get_track_info(self.reader.track)
                except:
                    logger.exception("Error in track API")

                self.track_info_txt_list = [
                    f"{track_info['name_en']}",
                    f"WR: {format_6digit(track_info.get('wr')) or '-'}",
                    f"My best: {format_6digit(track_info.get('best_score')) or '-'}",
                ]

            self.track_info_txt_list = None
            t = threading.Thread(target=fetch_func)
            t.start()

        if self.track_info_txt_list:
            self.track_info_var.set('\n'.join(self.track_info_txt_list))
            cv2.putText(
                im,
                ' / '.join(self.track_info_txt_list),
                (10, 50), 
                fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                fontScale=1.0,
                color=(0, 0, 255),
                thickness=2,
                lineType=cv2.LINE_4,
            )
        else:
            self.track_info_var.set("")

        if self.reader.track and self.reader.result:
            if not self.record_sent:
                def register_func():
                    register_record(
                        time=self.reader.result["sum"],
                        track=self.reader.track,
                        comment="/".join(map(format_6digit, self.reader.result["laps"])),
                    )
                    logger.info(f"sent: {self.reader.result}")

                t = threading.Thread(target=register_func)
                t.start()
                self.record_sent = True
        else:
            self.record_sent = False

        self.draw_on_canvas(im_prev)
        self.draw_on_sub_canvas(im)

    def quit(self):
        self.running = False
        self.master.destroy()

def launch_app():
    win = tk.Tk()
    app = Application(master=win)
    app.start()

import tkinter as tk
from time import sleep
import threading

import cv2
from PIL import Image, ImageOps, ImageTk

from .image.ta_result import detect_ta_result

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
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=True, fill=tk.BOTH)

        master.title("mktools-client")
        master.geometry("800x600")

        self.video_loop_id = None

        self.capture = cv2.VideoCapture(0)

        cv2.CV_CAP_PROP_FPS = 60

        button_frm = tk.Frame(self, width=400)
        button_frm.pack(expand=False, fill=tk.Y, anchor=tk.E, side=tk.RIGHT)

        button = tk.Button(button_frm, text="Open Preview", command=self.open_subwin)
        button.pack(padx=10, pady=10)

        # create canvas
        self.video_button = tk.Button(self, borderwidth=0)
        self.video_button.pack(expand=True, fill=tk.BOTH, anchor=tk.E)

        self.subwin = None
        self.sub_video_button = None

        self.running = True
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

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
            ret, im = self.capture.read()
            if not ret:
                continue

            im_prev = im.copy()
            detect_ta_result(im, im_prev)

            self.draw_on_canvas(im_prev)
            self.draw_on_sub_canvas(im)

            self.update_idletasks()
            self.update()

    def quit(self):
        self.running = False
        self.master.destroy()

def launch_app():
    win = tk.Tk()
    app = Application(master=win)
    app.start()

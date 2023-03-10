import tkinter as tk
from time import sleep

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
        self.pack()

        #master.state("zoomed")
        master.title("mktools-client")
        master.geometry("800x600")

        self.video_loop_id = None

        self.capture = cv2.VideoCapture(0)

        cv2.CV_CAP_PROP_FPS = 60

        # create canvas
        self.canvas = tk.Canvas(master)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.subwin = tk.Toplevel()
        self.subwin.title("MKview")
        self.subwin.state("zoomed")
        self.sub_canvas = tk.Canvas(self.subwin)
        self.sub_canvas.pack(expand=True, fill=tk.BOTH)

        self.video_loop()

    def video_loop(self):
        _, im = self.capture.read()

        im_prev = im.copy()
        detect_ta_result(im, im_prev)

        self.draw_on_canvas(im_prev)
        self.draw_on_sub_canvas(im)

        self.video_loop_id = self.after(10, self.video_loop)

    def draw_on_sub_canvas(self, im):
        cv_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        canvas_width = self.sub_canvas.winfo_width()
        canvas_height = self.sub_canvas.winfo_height()

        # resize image
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        # this must be stored to class to prevent from being destroied
        self.photo_image_sub = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.sub_canvas.create_image(
            0, 0,
            image=self.photo_image_sub,
            anchor='nw'
        )

    def draw_on_canvas(self, im):
        cv_image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv_image)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # resize image
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        # this must be stored to class to prevent from being destroied
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
            0, 0,
            image=self.photo_image,
            anchor='nw'
        )

def launch_app():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()

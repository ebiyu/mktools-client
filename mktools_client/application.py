import tkinter as tk
from time import sleep

import cv2
from PIL import Image, ImageOps, ImageTk

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

        # create canvas
        self.canvas = tk.Canvas(master)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.video_loop()

    def video_loop(self):
        _, frame = self.capture.read()

        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

        self.video_loop_id = self.after(10, self.video_loop)

def launch_app():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()

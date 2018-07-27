import tkinter
from tkinter import *
import cv2
import PIL.Image
import PIL.ImageTk
import time

from imgCrop import ImgCrop


class App:
    def __init__(self, window, window_title, video_source='vlc-output_16.mp4'):
        self.video_source = video_source
        self.window = window
        self.window.resizable(False, False)
        self.window.geometry("1024x640")
        self.window.title(window_title)

        self.UI_render()
        self.delay = 10000000
        self.window.mainloop()

    def open(self):
        if self.delay > 15:
            self.delay = 15
            self.video_source = self.stream_entry.get()
            self.vid = ImgCrop(stream_path=self.video_source)
            self.update()
            self.btn_start_text.set('Stop')
        else:
            self.vid.stop_cropping()
            self.delay = 100000000000
            self.btn_start_text.set('Start')

    def UI_render(self):
        #================= Left panel ===================
        vidFrame = Frame(self.window, width=820, highlightbackground="grey",
                         highlightcolor="grey", highlightthickness=1)
        vidFrame.pack(side=LEFT, fill=Y, padx=1, pady=2)

        self.canvas = tkinter.Canvas(
            vidFrame, width=800, height=600)
        self.canvas.pack(anchor=tkinter.CENTER, expand=True)

        streamF = Frame(vidFrame)
        streamF.pack(side=BOTTOM)

        entryText = tkinter.StringVar()
        self.stream_entry = Entry(streamF, width=30, textvariable=entryText)
        self.stream_entry.pack(side=LEFT)
        entryText.set("vlc-output_16.mp4")
        self.btn_start_text = tkinter.StringVar()
        self.btn_start = tkinter.Button(
            streamF, textvariable=self.btn_start_text, width=10, command=self.open)
        self.btn_start_text.set('Start')
        self.btn_start.pack(side=LEFT)

        #================= Right panel ===================
        rightFrame = Frame(self.window, highlightbackground="grey",
                           highlightcolor="grey", highlightthickness=1)
        rightFrame.pack(side=LEFT, fill=BOTH, padx=1, pady=2)

        # stream_id
        stream_idF = Frame(rightFrame)
        stream_idF.pack(side=TOP, fill=BOTH, expand=False)
        stream_idL = Label(stream_idF, text="cam_id:", width=8)
        stream_idL.pack(side=LEFT, anchor=W, pady=2, padx=5)
        self.stream_id_entry = Entry(stream_idF, width=10)
        self.stream_id_entry.insert(0, 16)
        self.stream_id_entry.pack(side=RIGHT, pady=2, padx=5)

        # x1
        x1F = Frame(rightFrame)
        x1F.pack(side=TOP, fill=BOTH, expand=False)
        x1L = Label(x1F, text="x1:", width=3)
        x1L.pack(side=LEFT, anchor=W, pady=2, padx=5)
        self.x1_entry = Entry(x1F, width=10)
        self.x1_entry.insert(0, 500)
        self.x1_entry.pack(side=RIGHT, pady=2, padx=5)

        # y1
        y1F = Frame(rightFrame)
        y1F.pack(side=TOP, fill=BOTH, expand=False)
        y1L = Label(y1F, text="y1:", width=3)
        y1L.pack(side=LEFT, anchor=W, pady=2, padx=5)
        self.y1_entry = Entry(y1F, width=10)
        self.y1_entry.insert(0, 450)
        self.y1_entry.pack(side=RIGHT, pady=2, padx=5)

        # width
        widthF = Frame(rightFrame)
        widthF.pack(side=TOP, fill=BOTH, expand=False)
        widthL = Label(widthF, text="width:", width=5)
        widthL.pack(side=LEFT, anchor=W, pady=2, padx=5)
        self.width_entry = Entry(widthF, width=10)
        self.width_entry.insert(0, 600)
        self.width_entry.pack(side=RIGHT, pady=2, padx=5)

        # height
        heightF = Frame(rightFrame)
        heightF.pack(side=TOP, fill=BOTH, expand=False)
        heightL = Label(heightF, text="height:", width=5)
        heightL.pack(side=LEFT, anchor=W, pady=2, padx=5)
        self.height_entry = Entry(heightF, width=10)
        self.height_entry.insert(0, 600)
        self.height_entry.pack(side=RIGHT, pady=2, padx=5)

        # resize
        self.resize_var = IntVar()
        self.resize_cbtn = Checkbutton(
            rightFrame, text="Resize to 416x416", variable=self.resize_var, onvalue=1, offvalue=0)
        self.resize_var.set(True)
        self.resize_cbtn.pack(side=TOP)

        self.btn_crop_text = tkinter.StringVar()
        self.btn_crop = tkinter.Button(
            rightFrame, textvariable=self.btn_crop_text, width=30, command=self.crop_imgs)
        self.btn_crop_text.set('Crop')
        self.btn_crop.pack(side=TOP, padx=2)

        # self.btn_snapshot = tkinter.Button(
        #     rightFrame, text="Snapshot", width=50, command=self.snapshot)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") +
                        ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def crop_imgs(self):
        if self.vid.croping:
            self.vid.stop_cropping()
            self.btn_crop_text.set('Crop')
        else:
            if self.resize:
                self.vid.crop_imgs(416, 416)
            else:
                self.vid.crop_imgs(0, 0)
            self.btn_crop_text.set('Stop')

    def update(self):
        try:
            self.resize = self.resize_var.get()
            s_id = int(self.stream_id_entry.get())
            x = int(self.x1_entry.get())
            y = int(self.y1_entry.get())
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            self.vid.set_cropping_box(s_id, x, y, w, h)
        except:
            pass
        ret, frame = self.vid.get_frame()
        if ret:
            w = 800
            h = int((w / self.vid.width) * self.vid.height)
            image = PIL.Image.fromarray(frame).resize(
                (w, h), resample=PIL.Image.BILINEAR)
            self.photo = PIL.ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "Image Cropper -_-")

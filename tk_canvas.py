import tkinter as tk
import tkinter.ttk as ttk
from tk_widget import Widget
from PIL import Image, ImageTk
import cv2
import numpy as np
import copy

class Canvas(Widget):
  def __init__(self, window, count=1, width = 700, height = 510):
    super().__init__(window)
    self.window = window
    self.canvas = None
    self.frame = object
    self.width = width
    self.height = height
    self.photo_w = self.width
    self.photo_h = self.height-10
    self.x = (count%5) * 30 + 30
    self.y = (count%10) * 50
    self.filename = "제목없음"
    self.count = count
    self.origin = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
    self.cv2_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
    self.canvas_img = np.full(shape=(self.height, self.width, 3), fill_value=255, dtype=np.uint8)
    self.paper = None
    self.changed = False
    self.cancel_li = []
    self.reload_li = []
  
  def get_filename(self, filename="제목없음"):
    if filename != "제목없음":
      r_index = filename.rindex('/')
      self.filename = filename[r_index+1:]
    self.name = self.filename  + " - " + str(self.count)
  
  def get_canvas(self, filename="제목없음"):
    self.get_filename(filename)
    frame, frame2 = self.get_widget(count=self.count)
    self.frame = frame
    canvas = self.make_canvas(frame2, filename=filename)
    self.canvas = canvas
    label2 = tk.Label(frame2, relief="raised", height=1)
    label2.pack(side="top", fill="x")

    def drag(event):
      x = sizegrip.winfo_x() + event.x
      y = sizegrip.winfo_y() + event.y
      sz_width = sizegrip.winfo_reqwidth()
      sz_height = sizegrip.winfo_reqheight()
      self.width = x + sz_width
      self.height = y + sz_height
      canvas.configure(width = self.width, height = self.height)

      sizegrip.place(x = canvas.winfo_x() + canvas.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                    y = canvas.winfo_y() + canvas.winfo_reqheight() + 32)
      self.changed = True
      
      if self.paper is not None :
        self.canvas.delete("all")
        self.canvas.create_image(self.width//2, self.height//2, image=self.paper)


    sizegrip = ttk.Sizegrip(frame)
    sizegrip.place(x = canvas.winfo_rootx() + canvas.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                  y = canvas.winfo_rooty() + canvas.winfo_reqheight() + 32)

    sizegrip.bind("<ButtonRelease-1>", drag)

  def make_canvas(self, _parent, filename="제목없음"):
    self.canvas = tk.Canvas(_parent)
    self.canvas.pack(side="top")
    if filename != "제목없음":
      self.origin = cv2.imread(filename)
      self.cv2_img = cv2.imread(filename)
      self.paint_canvas(self.cv2_img)
    else:
      self.canvas.configure(width=self.width, height=self.height, relief="raised", bg="white")
    
    return self.canvas

  def paint_canvas(self, img, mode=None):
    c_img = copy.copy(self.canvas_img)
    if mode != "c":
      self.cancel_li.append(c_img)
    elif mode == "c":
      self.reload_li.append(c_img)
    self.canvas_img  = copy.copy(img)
    h, w = img.shape[:2]
    if not self.changed and w > self.width or h > self.height:
      if h > w and self.width > self.height or h < w and self.width < self.height:
        _width = self.height
        _height = self.width
        self.width = _width
        self.height =_height
      else:
        _width = self.width
        _height = self.height
      if _width/w <= (_height-10)/h:
        self.photo_h = (int)((_width/w) * h)
        src = cv2.resize(img, dsize = (_width, self.photo_h))
      elif _width/w > (_height-10)/h:
        self.photo_w = (int)(((_height-10)/h) * w)
        src = cv2.resize(img, dsize = (self.photo_w, _height-10))
    else:
      src = img
    tk_img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
    photo = Image.fromarray(tk_img)   
    # self.paper : Prevent PhotoImage object being garbage collected!!!
    self.paper = ImageTk.PhotoImage(image=photo, master=self.canvas)
    self.canvas.configure(width=self.width, height=self.height, relief="raised")
    self.canvas.create_image(self.width//2, self.height//2, image=self.paper)

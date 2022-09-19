import tkinter as tk
import tkinter.ttk as ttk
from tk_mouse import MouseEvent
from PIL import Image, ImageTk
import cv2
import numpy as np
import copy

class Get_Frame(MouseEvent):
  def __init__(self, window, count=1, width = 1000, height = 510, x = 30, y = 0):
    super().__init__(window)
    self.window = window
    self.frame = None
    self.canvas = None
    self.width = width
    self.height = height
    self.photo_w = self.width
    self.photo_h = self.height-10
    self.x = (count%5) * 30 + 30
    self.y = (count%10) * 50
    self.filename = "제목없음"
    self.name = str()
    self.count = count
    self.origin = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
    self.cv2_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
    self.canvas_img = np.full(shape=(self.height, self.width, 3), fill_value=255, dtype=np.uint8)
    self.paper=None
    self.changed = False
    self.cancel_li = []
    self.reload_li = []
  
  def get_filename(self, filename="제목없음"):
    if filename != "제목없음":
      r_index = filename.rindex('/')
      self.filename = filename[r_index+1:]
    self.name = self.filename  + " - " + str(self.count)
  
  def make_Widget(self, filename="제목없음", mode="canvas", title=None, _resizable=True):
    if title is None:
      self.get_filename(filename)
    else:
      self.name = title

    frame = tk.Frame(self.window, bd=1)
    self.frame = frame
    frame.place(x=self.x, y=self.y)
    f_MouseEvent = MouseEvent(self.window)
    f_MouseEvent.set_widget(frame)

    frame1 = tk.Frame(frame, relief="solid", bd=1)
    frame1.pack(side="top", fill="x")
    frame1.bind("<Button-1>", f_MouseEvent.click)
    frame1.bind("<B1-Motion>", f_MouseEvent.move)
    frame1.bind("<ButtonRelease-1>", f_MouseEvent.release)
    label1 = tk.Label(frame1, text=self.name, height=1)
    label1.pack(side="left")    
    label1.bind("<Button-1>", f_MouseEvent.click)
    label1.bind("<B1-Motion>", f_MouseEvent.move)
    label1.bind("<ButtonRelease-1>", f_MouseEvent.release)  
    button = tk.Button(frame1, text="X", height=1, relief="flat", overrelief="flat", command=f_MouseEvent.close)
    button.pack(side="right")  
    frame2 = tk.Frame(frame, relief="solid", bd=1)
    frame2.pack(side="top", fill="both")

    if mode == "canvas":
      _child = self.make_canvas(frame2, filename=filename)
    elif mode == "filter":
      scale=tk.Scale(frame2, orient="horizontal",
                          tickinterval=10, from_=0, to=100, resolution=1, 
                          showvalue=True, length=self.width, width=10, sliderlength=15)
      scale.grid(row=1, column=1, columnspan=5)
      filter_button = tk.Button(frame2, text="확인")
      filter_button.grid(row=2, column=3)
      return scale, filter_button

    label2 = tk.Label(frame2, relief="raised", height=1)
    label2.pack(side="top", fill="x")

    if not _resizable :
      return

    def drag(event):
      x = sizegrip.winfo_x() + event.x
      y = sizegrip.winfo_y() + event.y
      sz_width = sizegrip.winfo_reqwidth()
      sz_height = sizegrip.winfo_reqheight()
      self.width = x + sz_width
      self.height = y + sz_height
      _child.configure(width = self.width, height = self.height)

      sizegrip.place(x = _child.winfo_x() + _child.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                    y = _child.winfo_y() + _child.winfo_reqheight() + 32)

      if self.paper is not None :
        self.canvas.delete("all")
        self.canvas.create_image(self.width//2, self.height//2, image=self.paper)
      self.changed = True

    sizegrip = ttk.Sizegrip(frame)
    sizegrip.place(x = _child.winfo_rootx() + _child.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                  y = _child.winfo_rooty() + _child.winfo_reqheight() + 32)

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
    h, w, c = img.shape
    if not self.changed:
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

from email.mime import image
import tkinter as tk
import tkinter.ttk as ttk
from turtle import bgcolor
from tk_mouse import MouseEvent
from PIL import Image, ImageTk
import cv2
import numpy as np

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
    self.tk_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
  
  def get_filename(self, filename="제목없음"):
    if filename != "제목없음":
      r_index = filename.rindex("/")
      self.filename = filename[r_index+1:]
    self.name = self.filename  + " - " + str(self.count)
  
  def paint_canvas(self, img):
    self.cv2_img = img
    h, w, c = img.shape
    if h > w :
      self.width = 400
      self.height = 710
    if self.width/w <= (self.height-10)/h:
      self.photo_h = (int)((self.width/w) * h)
      src = cv2.resize(img, dsize = (self.width, self.photo_h))
    elif self.width/w > (self.height-10)/h:
      self.photo_w = (int)(((self.height-10)/h) * w)
      src = cv2.resize(img, dsize = (self.photo_w, self.height-10))

    self.tk_img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    photo = Image.fromarray(self.tk_img)
    paper = ImageTk.PhotoImage(image=photo, master=self.canvas)
    self.canvas.configure(width=self.width, height=self.height, relief="raised")
    self.canvas.create_image(self.width//2, self.height//2, image=paper)

    self.makeBlob(photo, paper) 

  def makeBlob(self, Image, PhotoImage, _format="RGB"):
    blob = Image.make_blob(format=_format)
    painting = None
    for i in range(0, self.photo_w):
      for j in range(0, self.photo_h):
        r = blob[i*3*self.photo_w + j*3 + 0]
        g = blob[i*3*self.photo_w + j*3 + 1]          
        b = blob[i*3*self.photo_w + j*3 + 2]
        painting = PhotoImage.put("#%02x%02x%02x" %(r, g, b), (j, i))
    return painting

  def make_Frame(self, filename="제목없음"):
    self.get_filename(filename)

    frame = tk.Frame(self.window, bd=1, bg="blue")
    self.frame = frame
    frame.place(x=self.x, y=self.y)
    f_MouseEvent = MouseEvent(self.window)
    f_MouseEvent.set_widget(frame)

    frame1 = tk.Frame(frame, relief="solid", bd=1, bg="red")
    frame1.pack(side="top", fill="x")
    frame1.bind("<Button-1>", f_MouseEvent.click)
    frame1.bind("<B1-Motion>", f_MouseEvent.move)
    frame1.bind("<ButtonRelease-1>", f_MouseEvent.release)
    frame2 = tk.Frame(frame, relief="solid", bd=1, bg="yellow")
    frame2.pack(side="top", fill="both")

    label1 = tk.Label(frame1, text=self.name, height=1)
    label1.pack(side="left")
    
    button = tk.Button(frame1, text="X", height=1, relief="flat", overrelief="flat", command=f_MouseEvent.close)
    button.pack(side="right")

    canvas = tk.Canvas(frame2)
    self.canvas = canvas
    canvas.pack(side="top")
    if filename != "제목없음":
      self.origin = cv2.imread(filename)
      self.cv2_img = self.origin
      self.paint_canvas(self.cv2_img)
    else:
      canvas.configure(width=self.width, height=self.height, relief="raised", bg="white")
    
    label2 = tk.Label(frame2, height=1, bg="black")
    label2.pack(side="top", fill="x")

    def drag(event):
      x = sizegrip.winfo_x() + event.x
      y = sizegrip.winfo_y() + event.y
      sz_width = sizegrip.winfo_reqwidth()
      sz_height = sizegrip.winfo_reqheight()

      canvas.configure(width = x + sz_width, height = y + sz_height)

      sizegrip.place(x = canvas.winfo_x() + canvas.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                    y = canvas.winfo_y() + canvas.winfo_reqheight() + 30)

    sizegrip = ttk.Sizegrip(frame)
    sizegrip.place(x = canvas.winfo_x() + canvas.winfo_reqwidth() - sizegrip.winfo_reqwidth(),
                  y = canvas.winfo_y() + canvas.winfo_reqheight() + 30)
    sizegrip.bind("<ButtonRelease-1>", drag)





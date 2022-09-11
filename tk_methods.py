import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
from tk_mouse import Event
import cv2
from PIL import Image, ImageTk

class Methods(Event):

  def __init__(self, window):
    super().__init__(window)
    self.window = window
    self.path = "C:\\Users\\user\\desktop"
    self.width = 1000
    self.height = 500
    self.point_x = 50
    self.point_y = 0
  
  def new_open(self, filename="제목없음"):
    self.count_open()
    _name = self.get_filename(filename=filename)

    self.point_x = 50 + (50 * self.count_frames)
    self.point_y = 0 + (50 * self.count_frames)

    frame = tk.Frame(self.window, width=self.width, height=self.height, bd=1)
    frame.place(x=self.point_x, y=self.point_y)
    self.call_widget(frame)
    frame.widgetName = _name + "_root"

    frame1 = tk.Frame(frame, relief="solid", bd=1)
    frame1.pack(side="top", fill="x")
    frame1.bind("<ButtonRelease-1>", self.move)
    frame2 = tk.Frame(frame, relief="solid", bd=1)
    frame2.pack(side="top", fill="both")

    label1 = tk.Label(frame1, text=_name, height=1)
    label1.pack(side="left")
    
    button = tk.Button(frame1, text="X", height=1, relief="flat", overrelief="flat", command=frame.destroy)

    button.pack(side="right")

    if filename != "제목없음":
      canvas = tk.Canvas(frame2, width=self.width, height=self.height, relief="raised")
      src = cv2.imread(filename)
      src = cv2.resize(src, (self.width, self.height))
      tk_img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
      photo = Image.fromarray(tk_img)
      photo = ImageTk.PhotoImage(image=photo, master=canvas)
      canvas.create_image(0, 0, image=photo)
      
    else:
      canvas = tk.Canvas(frame2, width=self.width, height=self.height, relief="raised", bg="white")

    canvas.pack(side="top")
    label2 = tk.Label(frame2, height=1)
    label2.pack(side="bottom")

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

  def file_open(self):
    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 파일", "*.*"),
                                                    ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    self.new_open(filename=_filename)

  def close(self):
    self.window.quit()
    self.window.destroy()
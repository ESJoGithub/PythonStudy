import tkinter as tk
import tkinter.ttk as ttk
from mouse import MouseEvent
from PIL import Image, ImageTk

class Get_Frame(MouseEvent):
  def __init__(self, window, count=1, width = 1000, height = 500, x = 30, y = 0):
    super().__init__(window)
    self.window = window
    self.width = width
    self.height = height
    self.x = (count%5) * 30 + 30
    self.y = (count%10) * 50
    self.filename = "제목없음"
    self.name = str()
    self.count = count

  
  def get_filename(self, filename="제목없음"):
    if filename != "제목없음":
      r_index = filename.rindex("/")
      self.filename = filename[r_index+1:]
    self.name = self.filename  + " - " + str(self.count)
  
  def make_Frame(self, filename="제목없음", rgb_img=None):
    self.get_filename(filename)

    frame = tk.Frame(self.window, width=self.width, height=self.height, bd=1)
    frame.place(x=self.x, y=self.y)
    self.widget = frame

    frame1 = tk.Frame(frame, relief="solid", bd=1)
    frame1.pack(side="top", fill="x")
    frame1.bind("<ButtonRelease-1>", self.move)
    frame2 = tk.Frame(frame, relief="solid", bd=1)
    frame2.pack(side="top", fill="both")

    label1 = tk.Label(frame1, text=self.name, height=1)
    label1.pack(side="left")
    
    button = tk.Button(frame1, text="X", height=1, relief="flat", overrelief="flat", command=frame.destroy)
    button.pack(side="right")

    canvas = tk.Canvas(frame2)
    canvas.pack(side="top")

    if rgb_img is not None:
      photo = Image.fromarray(rgb_img)
      photo = ImageTk.PhotoImage(image=photo, master=canvas)
      canvas.configure(width=self.width, height=self.height, relief="raised")
      temp_width= self.width//2
      temp_height= self.height//2
      canvas.create_image(temp_width, temp_height, image=photo)
      
    else:
      canvas.configure(width=self.width, height=self.height, relief="raised", bg="white")

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

    return frame, canvas




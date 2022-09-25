import tkinter as tk
from tk_event import Widget_Event

class Widget():
  def __init__(self, window, width = 1000, height = 510, x = 0, y = 0):
    self.window = window
    self.widget = object
    self.width = width
    self.height = height
    self.x = 0
    self.y = 0
    self.name = str()

  def get_widget(self, title=None, count=1, mode="widget"):
    if title is not None:
      self.name = title

    main_frame = tk.Frame(self.window, bd=1)
    self.widget = main_frame
    main_frame.place(x=self.x, y = self.y)
    f_Event = Widget_Event(self.window, count = count)
    f_Event.set_widget(self.widget)
    frame1 = tk.Frame(main_frame, relief="solid", bd=1)
    frame1.pack(side="top", fill="x")
    if mode== "canvas":
      frame1.bind("<Button-1>", f_Event.canvas_click)
    else:
      frame1.bind("<Button-1>", f_Event.click)
    frame1.bind("<B1-Motion>", f_Event.move)
    frame1.bind("<ButtonRelease-1>", f_Event.release)
    label1 = tk.Label(frame1, text=self.name, height=1)
    label1.pack(side="left")    
    label1.bind("<Button-1>", f_Event.click)
    label1.bind("<B1-Motion>", f_Event.move)
    label1.bind("<ButtonRelease-1>", f_Event.release)  
    button = tk.Button(frame1, text="X", height=1, relief="flat", overrelief="flat", command=f_Event.close)
    button.pack(side="right")  
    frame2 = tk.Frame(main_frame, relief="solid", bd=1)
    frame2.pack(side="top", fill="both")

    return main_frame, frame2
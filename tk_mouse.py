import tkinter as tk
import tkinter.ttk as ttk

class Event():
  def __init__(self, window):
    self.window = window
    self.widget = window
    self.filename = "제목없음"
    self.count_frames = 0
  
  def count_open(self):
    self.count_frames = self.count_frames + 1

  def get_filename(self, filename="제목없음"):
    if filename != "제목없음":
      r_index = filename.rindex("/")
      self.filename = filename[r_index+1:]

    _name = self.filename  + " - " + str(self.count_frames)

    return _name

  def call_widget(self, obj):
    self.widget = obj

  def move(self, event):
    point_x = event.x_root - self.widget.winfo_rootx()
    point_y = event.y_root - self.widget.winfo_rooty()

    if point_x < 0: 
      point_x = 0
    if point_y < 0:
      point_y = 0
    elif point_x + self.widget.winfo_width() > self.window.winfo_width():
      point_x = self.window.winfo_width() - self.widget.winfo_width()
    elif point_y + self.widget.winfo_height() > self.window.winfo_height():
      point_y = self.window.winfo_height() - self.widget.winfo_height()
    
    self.widget.place(x = point_x, y = point_y)
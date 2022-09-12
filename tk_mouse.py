import tkinter as tk
import tkinter.ttk as ttk

class MouseEvent:
  def __init__(self, window):
    self.window = window
    self.widget = window
  
  def get_widget(self, event):
    pass

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
  

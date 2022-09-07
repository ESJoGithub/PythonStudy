import tkinter as tk

class methods:
  def __init__(self, window):
    self.window = window

  def close(self):
    self.window.quit()
    self.window.destroy()    


import tkinter as tk
from tkinter import filedialog
from tk_frame import Get_Frame
import cv2
from PIL import Image, ImageTk
import numpy as np

class Methods(Get_Frame):
  def __init__(self, window):
    super().__init__(window)
    self.window = window
    self.count_frames = 0
    self.framelist = []
    self.path = "C:\\Users\\user\\desktop"
    self.origin = np.zeros(shape=(1000, 500, 3))
  
  def set_width(self, width = 1000):
    self.width = width
  
  def set_height(self, height = 500):
    self.height = height
  
  def count_open(self):
    self.count_frames = self.count_frames + 1

  def new_open(self):
    self.count_open()
    sub_window = Get_Frame(self.window, self.count_frames)
    sub_window.make_Frame()
    self.framelist.append(sub_window.widget)

  def file_open(self):
    self.count_open()
    sub_window = Get_Frame(self.window, self.count_frames)
    
    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 파일", "*.*"),
                                                    ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    frame, canvas, self.origin, tk_img = sub_window.make_Frame(filename=_filename)
    self.framelist.append(frame)

  def close(self):
    self.window.quit()
    self.window.destroy()
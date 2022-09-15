from distutils.command.install_egg_info import safe_name
from statistics import mode
import tkinter as tk
from tkinter import VERTICAL, filedialog
from tk_frame import Get_Frame
import cv2
from PIL import Image, ImageTk
import numpy as np


class Methods(Get_Frame):
  def __init__(self, window):
    super().__init__(window)
    self.window = window
    self.sub_window = None
    self.count_frames = 0
    self.path = "C:\\Users\\user\\desktop"
    self.origin_img = np.zeros(shape=(1, 1, 3))


  def count_open(self):
    self.count_frames = self.count_frames + 1

  def new_open(self):
    self.count_open()
    sub_window = Get_Frame(self.window, self.count_frames)
    sub_window.make_Frame()

  def file_open(self):
    self.count_open()
    sub_window = Get_Frame(self.window, self.count_frames)
    self.sub_window = sub_window
    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 파일", "*.*"),
                                                    ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    sub_window.make_Frame(filename=_filename)

  def rotation(self, mode=1):
    cv2_img = self.sub_window.cv2_img
    img_90 = self.rotate_img(cv2_img)
    if mode == 1:
      self.sub_window.paint_canvas(img_90)
    elif mode == 2:
      img_180 = self.rotate_img(img_90)
      self.sub_window.paint_canvas(img_180)
    elif mode == 3:
      img_180 = self.rotate_img(img_90)
      img_270 = self.rotate_img(img_180)
      self.sub_window.paint_canvas(img_270)

  def rotate_img(self, _img):
    _height, _width, _channel = _img.shape
    rotated_img = np.zeros(shape=(_width, _height, _channel), dtype=np.uint8)
    for y in range(_height):
      y1 = (_height-1)-y
      for x in range(_width):
        rotated_img[x][y] = _img[y1][x]
    return rotated_img
  
  def symmetric(self, mode = "y"):
    cv2_img = self.sub_window.cv2_img
    _height, _width, _channel = cv2_img.shape
    symeetic_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
    if mode == "y":
      for y in range(_height):
        for x in range(_width):
          x1 = (_width-1) - x
          symeetic_img[y][x]= cv2_img[y][x1]
    else:
      for y in range(_height):
        y1 = (_height-1)-y
        symeetic_img[y] = cv2_img[y1]
    self.sub_window.paint_canvas(symeetic_img)

  def close(self):
    self.window.quit()
    self.window.destroy()
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
    self.reload_li = []

  def count_open(self):
    self.count_frames = self.count_frames + 1

  def new_open(self):
    self.count_open()
    sub_window = Get_Frame(self.window, self.count_frames)
    self.sub_window = sub_window
    self.sub_window.make_Widget(mode="canvas")

  def file_open(self):
    self.count_open()
    self.sub_window = Get_Frame(self.window, self.count_frames)

    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 파일", "*.*"),
                                                    ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    self.sub_window.make_Widget(filename=_filename, mode="canvas")

  def cancel(self):
    img = self.sub_window.cancel_li.pop()
    self.sub_window.reload_li.append(img)
    self.sub_window.cv2_img = img
    self.sub_window.paint_canvas(img)

  def reload(self):
    img = self.sub_window.reload_li.pop()
    self.sub_window.cancel_li.append(img)
    self.sub_window.cv2_img = img
    self.sub_window.paint_canvas(img)

  def rotation(self, mode=1):
    cv2_img = self.sub_window.cv2_img
    self.cancel_li.append(cv2_img) 
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

  '''window.winfo_with() 윈도우 안에서 오른쪽 끝, window.winfo_height() 윈도우 안에서 최 하단'''
  def filter_menu(self, mode="blur"):
    filter_widget = Get_Frame(self.window, width=300)
    filter_widget.x = self.window.winfo_width() - 310
    filter_widget.y = self.window.winfo_y() - self.window.winfo_rooty() + 50
    scale, filter_button = filter_widget.make_Widget(mode="filter", title="이미지조정", _resizable=False)
    pix = scale.get()
    if mode == "blur":
      filter_button.config(command=lambda: self.blur(_pix=pix))
  
  '''index에 연산을 바로 집어넣지 말자...'''
  def blur(self, _pix):
    cv2_img = self.sub_window.cv2_img
    print(_pix)
    if _pix == 0 :
      self.sub_window.paint_canvas(cv2_img)
      return

    _height, _width, _channel = cv2_img.shape
    filtered_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)

    if _pix > _width//2 or _width > _height//2:
      if _width > _height:
        _pix = _height//2
      else:
        _pix = _width//2

    for y in range(_height):
      for x in range(_width):
        count = 0
        sum = [0, 0, 0]
        y_s = y-_pix%2
        y_e = y+_pix%2+1
        x_s = x-_pix%2
        x_e = x+_pix%2+1
        for f_y in range(y_s, y_e):
          if f_y < 0 or f_y > _height-1 :
            continue
          for f_x in range(x_s, x_e):
            if f_x < 0 or f_x > _width - 1:
              continue          
            sum += cv2_img[f_y][f_x][:]
            count += 1          
          filtered_img[y][x][:] = [int(S/count) for S in sum] 
    self.sub_window.paint_canvas(filtered_img)

  def close(self):
    self.window.quit()
    self.window.destroy()
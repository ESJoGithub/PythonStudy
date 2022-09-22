import tkinter as tk
from tkinter import filedialog
from tk_canvas import Canvas
from tk_run_widgets import Run_widget
import cv2
from PIL import Image, ImageTk
import numpy as np
import copy

class Methods():
  def __init__(self, window):
    self.window = window
    self.sub_window = None
    self.count_frames = 0
    self.path = "C:\\Users\\user\\desktop"
    self.reload_li = []

  def count_open(self):
    self.count_frames += 1
  
  def new_open(self):
    self.count_open()
    sub_window = Canvas(self.window, self.count_frames)
    self.sub_window = sub_window
    self.sub_window.get_canvas()

  def file_open(self):
    self.count_open()
    self.sub_window = Canvas(self.window, self.count_frames)

    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 파일", "*.*"),
                                                    ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    self.sub_window.get_canvas(filename=_filename)

  def cancel(self):
    img = self.sub_window.cancel_li.pop()
    self.sub_window.paint_canvas(img, mode = "c")

  def reload(self):
    img = self.sub_window.reload_li.pop()
    self.sub_window.paint_canvas(img)

  def reset_photo_size(self):
    pass

  def reset_canvas_size(self):
    size_widget = Canvas(self.window, width=300)
    size_widget.x = self.window.winfo_width() - 320
    size_widget.y = self.window.winfo_y() - self.window.winfo_rooty() + 60
    size_widget = size_widget.make_Widget(mode="canvas_resize", title="캔버스 크기 조정", _resizable=False)
    def confirm():
      self.sub_window.changed = True
      self.sub_window.width = int()
      self.sub_window.height = int()
      self.sub_window.canvas.create_image(self.width//2, self.height//2, image=self.paper)

  def rotation(self, mode=1):
    canvas_img = self.sub_window.canvas_img
    img_90 = self.rotate_img(canvas_img)
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
    canvas_img = self.sub_window.canvas_img
    _height, _width, _channel = canvas_img.shape
    symeetic_img = np.zeros(shape=(_height, _width, _channel), dtype=np.uint8)
    if mode == "y":
      for y in range(_height):
        for x in range(_width):
          x1 = (_width-1) - x
          symeetic_img[y][x]= canvas_img[y][x1]
    else:
      for y in range(_height):
        y1 = (_height-1)-y
        symeetic_img[y] = canvas_img[y1]
    self.sub_window.paint_canvas(symeetic_img)

  def filter_menu(self, mode="blur"):
    _widget = Run_widget(self.window)
    filter_button=_widget.get_Scale(mode="blur")
    if mode=='blur':
      filter_button.config(command=lambda : self.blur(_pix=_widget.scale.get()))

  '''index에 연산을 바로 집어넣지 말자...'''
  def blur(self, _pix):
    if _pix == 0 :
      self.sub_window.paint_canvas(img)
      return
    img = self.sub_window.canvas_img
    '''
    제대로 동작하나 연산 속도가 매우 느림 성능 향상 방안 고민 필요
    _height, _width, _channel = img.shape
    filtered_img = np.zeros(shape=img.shape, dtype=np.uint8)
    _index = _pix//2
    for y in range(_height):
      for x in range(_width):
        count = 0
        sum = [0, 0, 0]
        y_s = y - _index
        y_e = y + _index + 1
        x_s = x - _index
        x_e = x + _index + 1
        for f_y in range(y_s, y_e):
          if f_y < 0 or f_y > _height-1 :
            continue
          for f_x in range(x_s, x_e):
            if f_x < 0 or f_x > _width - 1:
              continue          
            sum += img[f_y][f_x][:]         
            count += 1          
        filtered_img[y][x][:] = [s//count for s in sum]'''
    filtered_img = cv2.blur(img, (int(_pix), int(_pix)))
    self.sub_window.paint_canvas(filtered_img)

  def close(self):
    self.window.quit()
    self.window.destroy()

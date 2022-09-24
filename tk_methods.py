from tkinter import filedialog
from tk_canvas import Canvas
from tk_run_widgets import Run_widget
from tk_controller import Controller
import cv2
import numpy as np
import copy

class Methods(Controller):
  def __init__(self, window):
    self.window = window
    self.path = "C:\\Users\\user\\desktop"
    self.reload_li = []
    self.checked = False
    self.confirmed = False
    self.wg_count = 0
    self.count_frames = 0
    self.canvas = object

  def count_open(self):
    """미니 윈도우 호출 횟수, 파일명 설정 및 미니 윈도우 객체 구분을 위해 활용"""
    self.count_frames += 1
  
  def new_open(self):
    """New Empty Canvas Open"""
    self.count_open()                                                                         # frame count + 1
    canvas_widget = Canvas(self.window, self.count_frames)                                    # make widget object for canvas
    self.canvas = canvas_widget
    canvas_widget.get_canvas()                                                                # make canvas
    Controller.get_subwind(None, subwin=copy.copy(canvas_widget), count = self.count_frames)  # add to sub_windows dict

  def file_open(self):
    """New Image Open"""
    self.count_open()                                                                         # frame count + 1
    canvas_widget = Canvas(self.window, self.count_frames)                                    # make widget object for canvas
    self.canvas = canvas_widget
    # Imagefile open & get Imgagefile name
    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))
    canvas_widget.get_canvas(filename=_filename)                                              # make canvas & create Image on canvas
    Controller.get_subwin(None, subwin=copy.copy(canvas_widget), count = self.count_frames)   # add to sub_windows dict

  def cancel(self):
    """작업 취소 내역"""
    img = self.canvas.cancel_li.pop()
    self.canvas.paint_canvas(img, mode = "c")

  def reload(self):
    """작업 취소 시 작업 취소 전 실행 내역"""
    img = self.canvas.reload_li.pop()
    self.canvas.paint_canvas(img)

  def gray_menu(self):
    r2G = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1
    g_button = r2G.get_radio()
    g_button.config(command=lambda: self.rgb_2Gray(r2G_value=r2G.radio_G.get()))

  def rgb_2Gray(self, r2G_value):
    if self.checked :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None

    _h, _w, _c = _img.shape
    gray_img = np.zeros(shape=(_h, _w, 1), dtype=np.uint8)

    if r2G_value == 0:
      for y in range(_h):
        for x in range(_w):
          gray_img[y, x] = ((_img[y, x, 0].astype(np.uint16) + _img[y, x, 1].astype(np.uint16)
                            + _img[y, x, 2].astype(np.uint16))/3).astype(np.uint8)
      self.canvas.paint_canvas(gray_img, mode=_mode)
      self.checked = True  
      return

    if r2G_value == 1:
      g_list = [0.114, 0.587, 0.299]
    elif r2G_value == 2:
      g_list = [0.0722, 0.7152, 0.2126]
    elif r2G_value == 3:
      g_list = [0, 0, 1]
    elif r2G_value == 4:
      g_list = [0, 1, 0]
    else:
      g_list = [1, 0, 0]    

    for y in range(_h):
      for x in range(_w):
        gray_img[y, x] = (_img[y, x, 0]*g_list[0]+_img[y, x, 1]*g_list[1]+_img[y, x, 2]*g_list[2])
    self.canvas.canvas.paint_canvas(gray_img, mode=_mode)
    self.checked = True  

  def binary_menu(self):
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1
    bi_btn = _widget.get_Scale(title = "흑백 이미지 필터", start=0, end=255, term=1, tick=50)
    bi_btn.config(command=lambda : self.rgb_2binary(bar=_widget.scale.get()))    

  def rgb_2binary(self, bar=str(122)):
    if self.confirmed :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None
    _bar = int(bar)
    _img = copy.copy(self.canvas.canvas_img)
    _h, _w, _c = _img.shape
    binary_img = np.zeros(shape=(_h, _w, 1), dtype=np.uint8)
    for y in range(_h):
      for x in range(_w):
        _value = ((_img[y, x, 0].astype(np.uint16) + _img[y, x, 1].astype(np.uint16)  + _img[y, x, 2].astype(np.uint16))/3).astype(np.uint8)
        if _value > _bar:
          binary_img[y,x] = 255
        else:
          binary_img[y,x] = 0
    self.canvas.paint_canvas(binary_img, mode=_mode)
    self.confirmed = True

  def reset_photo_size(self):
    pass

  def reset_canvas_size(self):
    size_widget = Canvas(self.window, width=300)
    size_widget.x = self.window.winfo_width() - 320
    size_widget.y = self.window.winfo_y() - self.window.winfo_rooty() + 60
    size_widget = size_widget.make_Widget(mode="canvas_resize", title="캔버스 크기 조정", _resizable=False)
    def confirm():
      self.canvas.changed = True
      self.canvas.width = int()
      self.canvas.height = int()
      self.canvas.canvas.create_image(self.width//2, self.height//2, image=self.paper)

  def rotation(self, mode=1):
    canvas_img = self.canvas.canvas_img
    img_90 = self.rotate_img(canvas_img)
    if mode == 1:    
      self.canvas.paint_canvas(img_90)
    elif mode == 2:
      img_180 = self.rotate_img(img_90)
      self.canvas.paint_canvas(img_180)
    elif mode == 3:
      img_180 = self.rotate_img(img_90)
      img_270 = self.rotate_img(img_180)
      self.canvas.canvas.paint_canvas(img_270)

  def rotate_img(self, _img):
    _height, _width, _channel = _img.shape
    rotated_img = np.zeros(shape=(_width, _height, _channel), dtype=np.uint8)
    for y in range(_height):
      y1 = (_height-1)-y
      for x in range(_width):
        rotated_img[x][y] = _img[y1][x]
    return rotated_img
  
  def symmetric(self, mode = "y"):
    canvas_img = self.canvas.canvas_img
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
    self.canvas.paint_canvas(symeetic_img)

  def filter_menu(self):
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1  
    filter_button=_widget.get_Scale()
    filter_button.config(command=lambda : self.blur(_pix=_widget.scale.get()))

  '''index에 연산을 바로 집어넣지 말자...'''
  def blur(self, _pix):
    _img = self.canvas.canvas_img
    if _pix == 0 :
      self.canvas.paint_canvas(_img)
      return
    else:
      filtered_img = cv2.blur(_img, (int(_pix), int(_pix)))
      self.canvas.paint_canvas(filtered_img)

    '''cv2.blur 대체 코드
    : 제대로 동작하지만 연산 속도가 매우 느림. 성능 향상 방안 고민 필요(numpy 활용 등)
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

  def sharpen(self):
    _img = self.canvas.canvas_img
    _filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    _sharpen = cv2.filter2D(_img, -1, kernel=_filter)
    self.canvas.paint_canvas(_sharpen)    

    '''cv2.fiter2D 대체 코드
    _h, _w, _c = _img.shape
    _padding = np.zeros(shape=(_h+2, _w+2, _c), dtype='uint8')
    for y in range(_h):
      p_y = y+1
      for x in range(_w):
        p_x = x+1
        _padding[p_y, p_x] = _img[y, x]
    _sharpen = np.zeros(shape=_img.shape, dtype='uint8')
    for y in range(1, _h+1):
      y_ = y-1
      _y = y+1
      for x in range(1, _w+1):
        x_ = x-1
        _x = x+1              
        _sharpen[y_, x_][0] = _padding[y, x][:]*5 - (_padding[y_, x][:] + _padding[y, x_][:] +_padding[y, _x][:] + _padding[_y, x][:])

    self.canvas.paint_canvas(_sharpen)'''

  def close(self):
    self.window.quit()
    self.window.destroy()

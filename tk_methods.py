from re import S
from tkinter import filedialog
from tk_canvas import Canvas
from tk_run_widgets import Run_widget
from tk_controller import Controller
import cv2
import numpy as np
import copy

from tk_widget import Widget

class Methods(Controller):
  def __init__(self, window):
    self.window = window
    self.path = "C:\\Users\\user\\desktop"
    self.reload_li = []
    self.gray_chk = False
    self.bi_chk = False
    self.ls_chk = False
    self.ct_chk = False
    self.sat_chk = False
    self.hue_chk = False
    self.wg_count = 0
    self.count_frames = 0
    self.canvas = object
  
  def reset(self):
    self.gray_chk = False
    self.bi_chk = False
    self.ls_chk = False
    self.ct_chk = False
    self.sat_chk = False
    self.hue_chk = False

  def count_open(self):
    """미니 윈도우 호출 횟수, 파일명 설정 및 미니 윈도우 객체 구분을 위해 활용"""
    self.count_frames += 1
  
  def new_open(self):
    """New Empty Canvas Open"""
    self.reset()
    self.count_open()                                                                         # frame count + 1
    canvas_widget = Canvas(self.window, self.count_frames)                                    # make widget object for canvas
    self.canvas = canvas_widget
    canvas_widget.get_canvas()                                                                # make canvas
    Controller.get_subwind(None, subwin=copy.copy(canvas_widget), count = self.count_frames)  # add to sub_windows dict

  def file_open(self):
    """New Image Open"""
    self.reset()
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

  '''index에 연산을 바로 집어넣지 말자... 에러 가능성이 있음
    오버플로우를 방지할 수 있도록 이미지 type 선정에 신중해야 함.
  '''
  def gray_menu(self):
    """make Radiobutton widget for RGB2GRAY"""
    r2G = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.gray_chk = False
    g_button = r2G.get_radio()
    g_button.config(command=lambda: self.rgb_2gray(r2G_value=r2G.radio_G.get()))              # "확인 버튼"과 rgb_2gray 함수 호출 연결 

  def rgb_2gray(self, r2G_value):
    # 기존에 GRAY처리 이력이 있다면 직전 이미지를 GRAY처리에 사용하고 실행취소 목록에 넣지 않음, 
    # 기존에 GRAY처리 이력이 없다면 현재 이미지를 GRAY처리에 사용
    if self.gray_chk :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None

    _h, _w = _img.shape[:2]
    temp_img = _img.astype(np.float16)
    gray_img = np.zeros(shape=(_h, _w, 1), dtype=np.float16)

    # RGB 색상비율에 따른 흑백처리
    if r2G_value == 0:
      for y in range(_h):
        for x in range(_w):
          gray_img[y, x] = ((temp_img[y, x, 0] + temp_img[y, x, 1] + temp_img[y, x, 2])/3)
      gray_img = gray_img.astype(np.uint8)
      self.canvas.paint_canvas(gray_img, mode=_mode)
      self.gray_chk = True  
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
    gray_img = gray_img.astype(np.uint8)
    self.canvas.paint_canvas(gray_img, mode=_mode)
    self.gray_chk = True  

  def binary_menu(self):
    """make Scale widget for RGB2Binary"""
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.bi_chk = False
    bi_btn = _widget.get_Scale(title = "흑백 이미지 필터", start=0, end=255, term=1, tick=50)  
    bi_btn.config(command=lambda : self.rgb_2binary(bar=_widget.scale.get()))                 # "확인 버튼"과 rgb_2binaray 함수 호출 연결     

  def rgb_2binary(self, bar=str(122)):
    # 기존에 이진처리 이력이 있다면 직전 이미지를 Binary처리에 사용하고 실행취소 목록에 넣지 않음, 
    # 기존에 이진처리 이력이 없다면 현재 이미지를 Binary처리에 사용
    if self.bi_chk :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None
    _bar = int(bar)                                                                           # scale 위젯에서 받은 이진처리 기준 값
    _h, _w, _c = _img.shape
    binary_img = np.zeros(shape=(_h, _w, 1), dtype=np.uint8)
    # RGB 색상을 균등한 비율로 GRAY처리한 후 기준값보다 크면 255, 기준값보다 작으면 0으로 처리
    # GRAY 이미지라면 기존 값을 기준으로 처리
    for y in range(_h):
      for x in range(_w):
        _value = _img[y, x]
        if _c == 3:
          _value = ((_img[y, x, 0].astype(np.uint16) + _img[y, x, 1].astype(np.uint16)  + _img[y, x, 2].astype(np.uint16))/3).astype(np.uint8)
        if _value > _bar:
          binary_img[y,x] = 255
        else:
          binary_img[y,x] = 0
    self.canvas.paint_canvas(binary_img, mode=_mode)
    self.bi_chk = True

  def hsv_control(self, mode="Hue"):
    if mode == "Hue":
      _title = "색조 조정"
      _start = -180
      _end = 180
      _tick = 90
      self.hue_chk
    else:
      _title = "채도 조정"
      _start = -100
      _end = 100
      _tick = 50
      self.sat_chk = False
    
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1  

    spin_btn=_widget.get_Scale(title = _title, start=_start, end=_end, term=1, tick=_tick)
    spin_btn.config(command=lambda : self.set_HSV(mode=mode, _val= _widget.scale.get()))

  def set_HSV(self, mode="Hue", _val="0"):
    if self.sat_chk :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None

    _h, _w, _c = _img.shape
    _val = int(_val)
    if _c == 1:
      return
    filtered_img = np.zeros(shape=_img.shape, dtype="uint8")
    for _y in range(_h):
      for _x in range(_w):
        r = _img[_y, _x, 2]/255.0
        g = _img[_y, _x, 1]/255.0
        b = _img[_y, _x, 0]/255.0

        listRGB = [r, g, b]
        v = max(listRGB)
        c_min = min(listRGB)
        delta = v - c_min
  
        s = 0  
        if v != 0:
          s = delta/v        
        if mode == "saturation":
          s = (_val+100)/100 * s
          if s > 1 :
            s = 1
          elif s < 0:
            s = 0
        
        h = 0
        if delta == 0:
          h = 0
        elif v == r:
          h = 60*(g-b)/delta
        elif v == g:
          h = 60*((b-r)/delta + 2)
        elif v ==b:
          h = 60*((r-g)/delta + 4)
        
        if h < 0 :
          h += 360  

        if mode == "Hue":
          h = (_val+h) % 360

        c = v*s
        x = c * (1-np.abs((h/60)%2-1))
        m = v-c

        listBGR=[0.0, 0.0, 0.0]
        if 0 <= h < 60:
          listBGR = [0, x, c]
        elif 60 <= h <120:
          listBGR = [0, c, x]
        elif 120 <= h <180:
          listBGR = [x, c, 0]    
        elif 180 <= h <240:
          listBGR = [c, x, 0]   
        elif 240 <= h <300:
          listBGR = [c, 0, x]
        else:
          listBGR = [x, 0, c]

        temp = np.round((listBGR+m)*255)
        temp = temp.clip(0, 255)
        filtered_img[_y, _x][:] = temp.astype(np.uint8)
    self.canvas.paint_canvas(filtered_img, mode=_mode)
    if mode == "Hue":
      self.hue_chk = True
    else:
      self.sat_chk = True           

  def rgb_2HSV(self):
    _img = self.canvas.canvas_img
    _h, _w, _c = _img.shape
    if _c == 1:
      return
    hsv_img = np.zeros(shape=_img.shape, dtype="uint8")
    for y in range(_h):
      for x in range(_w):
        r = _img[y, x, 2]/255.0
        g = _img[y, x, 1]/255.0
        b = _img[y, x, 0]/255.0

        listRGB = [r, g, b]
        c_max = max(listRGB)
        c_min = min(listRGB)
        delta = c_max - c_min

        s = 0  
        if c_max != 0:
          s = delta/c_max

        h = 0
        if delta == 0:
          h = 0
        elif c_max == r:
          h = 60*(g-b)/delta
        elif c_max == g:
          h = 60*((b-r)/delta + 2)
        elif c_max ==b:
          h = 60*((r-g)/delta + 4)
        
        if h < 0 :
          h += 360  

        hsv_img[y][x][:]=[h/2, s*255, c_max*255]
    self.canvas.paint_canvas(hsv_img)

  def hsv_2rgb(self):
    hsv_img = self.canvas.canvas_img
    _h, _w, _c = hsv_img.shape
    if _c == 1:
      return
    _img = np.zeros(shape=hsv_img.shape, dtype="uint8")
    for _y in range(_h):
      for _x in range(_w):
        h = hsv_img[_y, _x, 0]*2
        s = hsv_img[_y, _x, 1]/255.0
        v = hsv_img[_y, _x, 2]/255.0
        c = v*s
        x = c * (1-np.abs((h/60)%2-1))
        m = v-c
        listBGR=[0, 0, 0]
        if 0 <= h < 60:
          listBGR = [0, x, c]
        elif 60 <= h <120:
          listBGR = [0, c, x]
        elif 120 <= h <180:
          listBGR = [x, c, 0]    
        elif 180 <= h <240:
          listBGR = [c, x, 0]   
        elif 240 <= h <300:
          listBGR = [c, 0, x]
        else:
          listBGR = [x, 0, c]
        _img[_y, _x][:] = np.round((listBGR+m)*255).astype(np.uint8)
    self.canvas.paint_canvas(_img)         

  def brightness_control(self):
    """make Scale widget for brightness_control"""
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.ls_chk = False
    br_btn = _widget.get_Scale(title = "명암조절", start=-255, end=255, term=1, tick=255)  
    br_btn.config(command=lambda : self.lightNShade(bar=_widget.scale.get()))                    # "확인 버튼"과 contrast 함수 호출 연결     

  def lightNShade(self, bar=str(0)):
    if self.ls_chk :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None
    _bar = int(bar)                                                                           # scale 위젯에서 받은 명암처리 기준 값
    _filter = np.full(shape=_img.shape, fill_value=_bar, dtype=np.int16)
    filtered_img = np.zeros(shape=_img.shape, dtype=np.int32)
    filtered_img = _img + _filter
    filtered_img = filtered_img.clip(0, 255)
    filtered_img = filtered_img.astype(np.uint8)
    self.canvas.paint_canvas(filtered_img, mode=_mode)
    self.ls_chk = True

  def contrast_control(self):
    """make Scale widget for brightness_control"""
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.ct_chk = False
    br_btn = _widget.get_Scale(title = "명암조절", start=0, end=10, term=0.1, tick=1)  
    br_btn.config(command=lambda : self.contrast(bar=_widget.scale.get())) 
  
  def contrast(self, bar=str(1)):
    if self.ct_chk :
      _img = copy.copy(self.canvas.cancel_li[-1])
      _mode = "c"
    else:
      _img = self.canvas.canvas_img
      _mode = None
    _bar = int(bar)
    temp_img = _img.astype(np.float32)                                                                          # scale 위젯에서 받은 기준 값
    filtered_img = np.zeros(shape=_img.shape, dtype=np.float32)
    filtered_img = temp_img + (temp_img-128) * _bar
    filtered_img = filtered_img.clip(0, 255)
    filtered_img = filtered_img.astype(np.uint8)
    self.canvas.paint_canvas(filtered_img, mode=_mode)    
    self.ct_chk = True    

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
    if mode == 1:                                  # 90 degrees Clockwise
      self.canvas.paint_canvas(img_90)
    elif mode == 2:                                # 180 degrees
      img_180 = self.rotate_img(img_90)
      self.canvas.paint_canvas(img_180)
    elif mode == 3:                                # 90 degrees Counter Colckwise
      img_180 = self.rotate_img(img_90)
      img_270 = self.rotate_img(img_180)
      self.canvas.paint_canvas(img_270)

  def rotate_img(self, _img):
    """rotate current img 90 degrees"""
    _h, _w = _img.shape[:2]
    rotated_img = np.zeros(shape=(_img.shape), dtype=np.uint8)
    for y in range(_h):
      y1 = (_h-1)-y                                # reversed y-index -> x-index for rotated_img 인덱스 값을 구해야 하므로 h - 1
      for x in range(_w):
        rotated_img[x][y] = _img[y1][x]            # x-index -> y-index for rotated_img
    return rotated_img
  
  def symmetric(self, mode = "y"):
    _img = self.canvas.canvas_img
    _h, _w = _img.shape[:2]
    symeetic_img = np.zeros(shape=(_img.shape), dtype=np.uint8)

    if mode == "y":                                # flip canvas vertical      
      for y in range(_h):
        for x in range(_w):
          x1 = (_w-1) - x
          symeetic_img[y][x]= _img[y][x1]
    else:                                          # flip canvas horizontal
      for y in range(_h):
        y1 = (_h-1)-y
        symeetic_img[y] = _img[y1]
    self.canvas.paint_canvas(symeetic_img)

  def set_blur(self):
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1  
    filter_button=_widget.get_Scale()
    filter_button.config(command=lambda : self.blur(_pix=_widget.scale.get()))

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
    _h, _w = img.shape[:2]
    filtered_img = np.zeros(shape=img.shape, dtype=np.uint8)
    _index = _pix//2
    for y in range(_h):
      for x in range(_w):
        count = 0
        sum = [0, 0, 0]
        y_s = y - _index
        y_e = y + _index + 1
        x_s = x - _index
        x_e = x + _index + 1
        for f_y in range(y_s, y_e):
          if f_y < 0 or f_y >= _h :
            continue
          for f_x in range(x_s, x_e):
            if f_x < 0 or f_x >= _w:
              continue          
            sum += img[f_y, f_x][:]         
            count += 1          
        filtered_img[y, x][:] = [s//count for s in sum]'''

  def sharpen(self):
    _img = self.canvas.canvas_img

    _h, _w = _img.shape[:2]
    temp_img = _img.astype(np.int32)                        # 합산 값의 범위가 -255*4 ~ 255*5로 추정되므로 오버플로우를 방지해야 함
    _sharpen = np.zeros(shape=_img.shape, dtype='int32')    # 합산 값의 범위가 -255*4 ~ 255*5로 추정되므로 오버플로우를 방지해야 함
    for y in range(_h):
      y_ = y-1
      _y = y+1
      if y_ < 0 or _y >= _h:
        continue
      for x in range(_w):
        x_ = x-1
        _x = x+1
        if x_ < 0 or _x >= _w:
          continue       
        _sharpen[y, x][:] = temp_img[y, x][:]*5 - temp_img[_y, x][:] - temp_img[y, x_][:] - temp_img[y, _x][:] - temp_img[_y, x][:]
    _sharpen = _sharpen.clip(0, 255)
    _sharpen = _sharpen.astype(np.uint8)
    self.canvas.paint_canvas(_sharpen)

  def close(self):
    self.window.quit()
    self.window.destroy()

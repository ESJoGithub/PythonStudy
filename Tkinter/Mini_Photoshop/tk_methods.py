from re import M, X
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog

from soupsieve import select
from tk_canvas import Canvas
from tk_run_widgets import Run_widget
from tk_event import Widget_Event
from tk_controller import Controller
import cv2
import numpy as np
import copy

class Methods(Controller):

  def __init__(self, window):
    self.window = window
    self.path = "C:\\Users\\user\\desktop"
    self.gray_chk = False
    self.bi_chk = False
    self.ls_chk = False
    self.ct_chk = False
    self.sat_chk = False
    self.hue_chk = False
    self.wg_count = 0
    self.count_frames = 0
    self.event_call = False
    self.Event = None
    self._color = "black"
    self.text = None


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
    Controller.current_can = canvas_widget
    
    canvas_widget.get_canvas()                                                                # make canvas
    Controller.get_subwin(subwin=copy.copy(canvas_widget), count = self.count_frames)        # add to sub_windows dict

  def file_open(self):
    """New Image Open"""
    self.reset()
    self.count_open()                                                                         # frame count + 1
    canvas_widget = Canvas(self.window, self.count_frames)                                    # make widget object for canvas
    Controller.current_can = canvas_widget

    # Imagefile open & get Imgagefile name
    _filename = filedialog.askopenfilename(initialdir=self.path, title="열기", 
                                          filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                    ("JPG", "*.jpg;*.jpeg"),
                                                    ("비트맵 파일", "*.btm"),
                                                    ("PNG", "*.png"),
                                                    ("TIF", "*.tif"),
                                                    ("GIF", "*.gif")))

    canvas_widget.get_canvas(filename=_filename)                                              # make canvas & create Image on canvas
    Controller.get_subwin(subwin=copy.copy(canvas_widget), count = self.count_frames)         # add to sub_windows dict

  def file_save(self, mode="save"):
    if Controller.current_can.paper is None:
      error = tk.Toplevel(self.window)
      error.title("오류메시지")
      error.geometry("300x100+450+400")
      error.resizable(False, False)
      error_msg = tk.Message(error, text="저장할 내용이 없습니다.", width=300, aspect=300, anchor="center")
      error_msg.place(relx=0.25, rely=0.2)
      btn = tk.Button(error, text="닫기", command=error.destroy)
      btn.place(relx=0.42, rely=0.6)
    
    def confirm():
      save_alert.destroy()
      _img = Controller.current_can.canvas_img
      _filename = Controller.current_can.filename.replace(".", str(Controller.current_can.count) + ".")
      savefile=self.path+"\\"+_filename
      cv2.imwrite(filename=savefile, img=_img)

    def confirmas():
      _img = Controller.current_can.canvas_img
      _filename = Controller.current_can.filename.replace(".", str(Controller.current_can.count) + ".")
      savefile = filedialog.asksaveasfilename(initialdir=self.path, title="다른 이름으로 저장",  initialfile=_filename, 
                                              filetypes=(("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                        ("JPG", "*.jpg;*.jpeg"),
                                                        ("비트맵 파일", "*.btm"),
                                                        ("PNG", "*.png"),
                                                        ("TIF", "*.tif"),
                                                        ("GIF", "*.gif")))
      cv2.imwrite(filename=savefile, img=_img)

    if mode == "save":
      _title = "저장"
      _confirm = confirm
    else:
      _title = "다른 이름으로 저장"
      _confirm =confirmas
  
    save_alert = tk.Toplevel(self.window)
    save_alert.title(_title)
    save_alert.geometry("300x100+450+400")
    save_alert.resizable(False, False)
    save_msg = tk.Message(save_alert, text="변경 사항을 저장하시겠습니까?", width=300, aspect=300, anchor="center")
    save_msg.place(relx=0.19, rely=0.2)
    btn_confirm = tk.Button(save_alert, text="예", padx=22, command=_confirm)
    btn_confirm.place(relx=0.2, rely=0.6)
    btn_cancel = tk.Button(save_alert, text="아니오", padx=10, command=save_alert.destroy)
    btn_cancel.place(relx=0.57, rely=0.6)

  def event_clear(self):
    if self.event_call:
      img = Controller.current_can.canvas_img
      Controller.current_can.paint_canvas(img, mode="c")

    try:
      Controller.current_can.canvas.unbind("<Button-1>", Controller.binding1)
    except: 
      pass
    try:
      Controller.current_can.canvas.unbind("<B1-Motion>", Controller.binding2)
    except:
      pass
    try:
      Controller.current_can.canvas.unbind("<ButtonRelease-1>", Controller.binding3)
    except:
      pass
    try:
      Controller.current_can.canvas.unbind("<Button-3>", Controller.binding4)
    except:
      pass

  def select_event(self, mode="select"):
    self.event_clear()
    select_Event = Widget_Event(self.window)
    self.Event = select_Event
    self.event_call = True
    select_Event.mode = mode
    if mode == "select" or mode == "copy":
      _cursor = "sizing"
      select_Event.color = "gray50"
      Controller.binding3 = Controller.current_can.canvas.bind("<ButtonRelease-1>", select_Event.select_released)
    elif mode == "crop":
      _cursor = "tcross"
      select_Event.color = "black"
      Controller.binding3 = Controller.current_can.canvas.bind("<ButtonRelease-1>", select_Event.crop_released)

    Controller.current_can.canvas.config(cursor=_cursor)
    Controller.binding1 = Controller.current_can.canvas.bind("<Button-1>", select_Event.select_click)
    Controller.binding2 = Controller.current_can.canvas.bind("<B1-Motion>", select_Event.select_drag)
    self.event_call = select_Event.call

  def text_box(self):
    t_x = 0
    t_y = 0
    def select_Text(event):
      nonlocal t_x , t_y
      t_x = event.x
      t_y = event.y
    Controller.binding1 = Controller.current_can.canvas.bind("<Button-1>", select_Text)
    Controller.current_can.canvas.config(cursor="xterm")

    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 2
    txt_btn = _widget.get_text()
    txt_btn.config(command=lambda : self.type_text(_widget.txt_box.get(1.0, "end"), t_x, t_y))

  def type_text(self, val, s_x = 0, s_y = 0):
    if self.text is not None:
      Controller.current_can.canvas.delete(self.text)
    self.text = Controller.current_can.canvas.create_text(s_x, s_y, text=val,  font = ("맑은고딕", 10), fill =self._color[1])

  def mk_shape(self, mode=0):
    self.event_clear()

    fig_Event = Widget_Event(self.window)
    self.Event = fig_Event
    self.event_call = True
    fig_Event.mode = mode
    self.color_choice()
    fig_Event.color = self._color[1]

    Controller.current_can.canvas.config(cursor="tcross")
    Controller.binding1 = Controller.current_can.canvas.bind("<Button-1>", fig_Event.click)
    Controller.binding2 = Controller.current_can.canvas.bind("<B1-Motion>", fig_Event.drag_fig)
    Controller.binding3 = Controller.current_can.canvas.bind("<ButtonRelease-1>", fig_Event.release_fig)
    self.event_call = fig_Event.call

  def cancel(self):
    """작업 취소 내역"""
    img = Controller.current_can.cancel_li.pop()
    Controller.current_can.paint_canvas(img, mode = "c")

  def reload(self):
    """작업 취소 시 작업 취소 전 실행 내역"""
    img = Controller.current_can.reload_li.pop()
    Controller.current_can.paint_canvas(img)

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
      _img = copy.copy(Controller.current_can.cancel_li[-1])
      _mode = "c"
    else:
      _img = Controller.current_can.canvas_img
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
      Controller.current_can.paint_canvas(gray_img, mode=_mode)
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
    Controller.current_can.paint_canvas(gray_img, mode=_mode)
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
      _img = copy.copy(Controller.current_can.cancel_li[-1])
      _mode = "c"
    else:
      _img = Controller.current_can.canvas_img
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
    Controller.current_can.paint_canvas(binary_img, mode=_mode)
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
      _img = copy.copy(Controller.current_can.cancel_li[-1])
      _mode = "c"
    else:
      _img = Controller.current_can.canvas_img
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
    Controller.current_can.paint_canvas(filtered_img, mode=_mode)
    if mode == "Hue":
      self.hue_chk = True
    else:
      self.sat_chk = True           

  def rgb_2HSV(self):
    _img = Controller.current_can.canvas_img
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
    Controller.current_can.paint_canvas(hsv_img)

  def hsv_2rgb(self):
    hsv_img = Controller.current_can.canvas_img
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
    Controller.current_can.paint_canvas(_img)         

  def brightness_control(self):
    """make Scale widget for brightness_control"""
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.ls_chk = False
    br_btn = _widget.get_Scale(title = "밝기조절", start=-255, end=255, term=1, tick=255)  
    br_btn.config(command=lambda : self.lightNShade(bar=_widget.scale.get()))                    # "확인 버튼"과 contrast 함수 호출 연결     

  def lightNShade(self, bar=str(0)):
    if self.ls_chk :
      _img = copy.copy(Controller.current_can.cancel_li[-1])
      _mode = "c"
    else:
      _img = Controller.current_can.canvas_img
      _mode = None
    _bar = int(bar)                                                                           # scale 위젯에서 받은 명암처리 기준 값
    _filter = np.full(shape=_img.shape, fill_value=_bar, dtype=np.int16)
    filtered_img = np.zeros(shape=_img.shape, dtype=np.int32)
    filtered_img = _img + _filter
    filtered_img = filtered_img.clip(0, 255)
    filtered_img = filtered_img.astype(np.uint8)
    Controller.current_can.paint_canvas(filtered_img, mode=_mode)
    self.ls_chk = True

  def contrast_control(self):
    """make Scale widget for brightness_control"""
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1                                                                        # 위젯 호출 횟수. 위젯들 간 위치 설정을 위해 활용(0부터 시작하므로 위젯 객체 생성 후 +1)
    self.ct_chk = False
    br_btn = _widget.get_Scale(title = "명암대비", start=0, end=10, term=0.1, tick=1)  
    br_btn.config(command=lambda : self.contrast(bar=_widget.scale.get())) 
  
  def contrast(self, bar=str(1)):
    if self.ct_chk :
      _img = copy.copy(Controller.current_can.cancel_li[-1])
      _mode = "c"
    else:
      _img = Controller.current_can.canvas_img
      _mode = None
    _bar = int(bar)
    temp_img = _img.astype(np.float32)                                                                          # scale 위젯에서 받은 기준 값
    filtered_img = np.zeros(shape=_img.shape, dtype=np.float32)
    filtered_img = temp_img + (temp_img-128) * _bar
    filtered_img = filtered_img.clip(0, 255)
    filtered_img = filtered_img.astype(np.uint8)
    Controller.current_can.paint_canvas(filtered_img, mode=_mode)    
    self.ct_chk = True    

  def reset_photo_size(self):
    _img = Controller.current_can.canvas_img
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1
    size_btn = _widget.get_photosize(title="이미지 사이즈 조정", _img = _img)
    size_btn.config(command=lambda : self.photo_size(_widget.check, _widget.spin.get(),_widget.spin1.get(), _widget.spin2.get()))

  def photo_size(self, check, ratio, width, height):
    ratio, width, height = int(ratio), int(width), int(height)
    _img = Controller.current_can.canvas_img
    resized_img = None
    if check:
      size = ratio/100
      _h, _w, _c =  _img.shape
      re_h = int(np.ceil(_h*size))
      re_w = int(np.ceil(_w*size))
      resized_img = np.zeros(shape=(re_h, re_w, _c), dtype = "uint8")

      _size = 1/size
      for y in range(re_h):
        r_y = int(y*_size)
        for x in range(re_w):
          r_x = int(x*_size)
          resized_img[y, x] = _img[r_y][r_x]
    else:
      _h, _w, _c = _img.shape
      resized_img = np.zeros(shape=(height, width, _c), dtype = "uint8")
      step_y = _h/height
      step_x = _w/width

      for y in range(height):
        y_idx = int(step_y * y)
        if y_idx > _h-1:
          y_idx = _h-1
        y_img = _img[y_idx]
        for x in range(width):
          x_idx = int(step_x * x)
          if x_idx > _w-1:
            x_idx = x-1
          resized_img[y, x] = y_img[x_idx]
    Controller.current_can.paint_canvas(resized_img)

  def reset_canvas_size(self):
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1
    size_btn = _widget.get_Spin(title="캔버스 사이즈 조정")
    size_btn.config(command=lambda : self.canvas_size(_w = _widget.spin1.get(), _h = _widget.spin2.get()))

  def canvas_size(self, _w, _h):
    _w = int(_w)
    _h = int(_h)
    _temp = Controller.current_can
    _temp.canvas.configure(width = _w, height = _h)

    _temp.sizegrip.place(x = _temp.canvas.winfo_x() + _temp.canvas.winfo_reqwidth() - _temp.sizegrip.winfo_reqwidth(),
                        y = _temp.canvas.winfo_y() + _temp.canvas.winfo_reqheight() + 32)
    if _temp.paper is not None :
        _temp.canvas.delete("all")
        _temp.canvas.create_image(_w//2, _h//2, image=_temp.paper)
    Controller.current_can = _temp

  def rotation(self, mode=1):
    canvas_img = Controller.current_can.canvas_img
    img_90 = self.rotate_img(canvas_img)
    if mode == 1:                                  # 90 degrees Clockwise
      Controller.current_can.paint_canvas(img_90)
    elif mode == 2:                                # 180 degrees
      img_180 = self.rotate_img(img_90)
      Controller.current_can.paint_canvas(img_180)
    elif mode == 3:                                # 90 degrees Counter Colckwise
      img_180 = self.rotate_img(img_90)
      img_270 = self.rotate_img(img_180)
      Controller.current_can.paint_canvas(img_270)

  def rotate_img(self, _img):
    """rotate current img 90 degrees"""
    _h, _w, _c = _img.shape
    rotated_img = np.zeros(shape=(_w, _h, _c), dtype=np.uint8)
    for y in range(_h):
      y1 = (_h-1)-y                                # reversed y-index -> x-index for rotated_img 인덱스 값을 구해야 하므로 h-1
      for x in range(_w):
        rotated_img[x][y] = _img[y1][x]            # x-index -> y-index for rotated_img
    return rotated_img
  
  def symmetric(self, mode = "y"):
    _img = Controller.current_can.canvas_img
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
    Controller.current_can.paint_canvas(symeetic_img)

  def set_blur(self):
    _widget = Run_widget(self.window, count=self.wg_count)
    self.wg_count += 1  
    filter_button=_widget.get_Scale()
    filter_button.config(command=lambda : self.blur(_pix=_widget.scale.get()))

  def blur(self, _pix):
    _img = Controller.current_can.canvas_img
    if _pix == 0 :
      Controller.current_can.paint_canvas(_img)
      return
    else:
      filtered_img = cv2.blur(_img, (int(_pix), int(_pix)))
      Controller.current_can.paint_canvas(filtered_img)

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
    _img = Controller.current_can.canvas_img

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
    Controller.current_can.paint_canvas(_sharpen)

  def color_choice(self):
    self._color = colorchooser.askcolor()
    print(self._color)

  def close(self):
    self.window.quit()
    self.window.destroy()
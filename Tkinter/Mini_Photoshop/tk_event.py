import tkinter as tk
import copy
from matplotlib.pyplot import fill
import numpy as np
from tk_controller import Controller

class Widget_Event(Controller):
  def __init__(self, window, count=1):
    self.window = window
    self.widget = object
    self.drag_start = []
    self.start = []
    self.end = []
    self.paste_pos = []
    self.dragging = False
    self.count = count
    self.select_range = None
    self.shape = None
    self.r_frame = None
    self.alert = None
    self.call = True
    self.r_click = False
    self.selected = 0
    self.mode = "select"
    self.color = "black"
    self.px = 1
    self.selected_img = None
    self.deselected_img = None
    self.s_x = 0
    self.s_y = 0

  def set_widget(self, widget):
    self.widget = widget

  def click(self, event):
    self.dragging = True
    self.call = False
    self.start = [event.x, event.y]
    self.drag_start = [event.x_root, event.y_root]

  def canvas_click(self, event):
    self.click(event)
    Controller.show_subwin(str(self.count))

  def move(self, event):
    if self.dragging:
      point_x = self.widget.winfo_x() + (event.x_root - self.window.winfo_x() - self.drag_start[0]) - self.start[0]
      point_y = self.widget.winfo_y() + (event.y_root - self.window.winfo_y() - self.drag_start[1]) - 60
      max_x = self.window.winfo_width() - 100
      max_y = self.window.winfo_height() - 100
      if point_x < 0: 
        point_x = 0
      if point_y < 0:
        point_y = 0
      if point_x <= max_x and point_y > max_y:
        point_y = max_y
      if point_x > max_x and point_y <= max_y:
        point_x = max_x
      if point_x > max_x and point_y > max_y:
        point_x = max_x
        point_y = max_y

      self.drag_start=[point_x, point_y]
      self.widget.place(x = self.drag_start[0], y = self.drag_start[1])
  
  def value_Check(self, value=str(), _min=0, _max=3840):
    if value.isdigit():
      valid = False
      if int(_min) <= int(value) <= int(_max):
        valid = True
    elif value == "":
      valid = True
    return valid
  
  def mk_alert(self, title, msg):
    alert = tk.Toplevel(self.window)
    alert.title(title)
    alert.geometry("300x100+450+400")
    alert.resizable(False, False)
    self.alert = alert
    _var = tk.StringVar()
    _var.set(msg)
    alert_msg = tk.Message(self.alert, textvariable=_var, width=300, aspect=300, anchor="center")
    alert_msg.pack(pady=20)
    
  def value_error(self):
    self.mk_alert(title="오류메시지", msg="잘못된 범위의 값을 입력하였습니다.")
    btn = tk.Button(self.alert, text="닫기", command=self.alert.destroy)
    btn.place(relx=0.42, rely=0.6)

  def release(self, event):
      self.widget.place(x = self.drag_start[0], y = self.drag_start[1])
      self.dragging = False
  
  def close(self):
      self.widget.destroy()

  def select_click(self, event):
    self.start = [event.x, event.y]
    self.selected += 1
    self.call = False
    if self.r_frame is not None:
      self.r_frame.destroy()
  
  def select_drag(self, event):
    if self.selected == 1:
      Controller.current_can.canvas.delete(self.select_range)
      self.select_range = Controller.current_can.canvas.create_rectangle(self.start[0], 
                          self.start[1], event.x, event.y, outline=self.color)
    elif self.selected == 2:
      Controller.current_can.canvas.config(cursor="fleur")
      try:
        Controller.current_can.canvas.unbind_all("<Button-3>")      
      except:
        pass
      Controller.current_can.move_img(img_mv = self.selected_img, img_bg = self.deselected_img, p_x = event.x, p_y = event.y)
    else:
      self.select_reset()

  def select_released(self, event):
    self.end = [event.x, event.y]
    Controller.current_can.canvas.config(cursor="arrow")
    self.select()

  def crop_released(self, event):
    self.end = [event.x, event.y]
    self.mk_alert(title="잘라내기", msg="해당 영역만 남기고 삭제하시겠습니까?")
    btn_confirm = tk.Button(self.alert, text="예", padx=22, command=self.select)
    btn_confirm.place(relx=0.2, rely=0.6)
    btn_cancel = tk.Button(self.alert, text="아니오", padx=10, command=self.select_reset)
    btn_cancel.place(relx=0.57, rely=0.6)
    Controller.current_can.canvas.unbind("<Button-1>", Controller.binding1)
    Controller.current_can.canvas.bind("<Button-1>", self.select_reset)
    Controller.current_can.canvas.config(cursor="arrow")

  def select(self):
    s_x = self.start[0]
    s_y = self.start[1]
    e_x = self.end[0]
    e_y = self.end[1]

    if s_x > e_x :
      temp = s_x
      s_x = e_x
      e_x = temp
    if s_y > e_y :
      temp = s_y
      s_y = e_y
      e_y = temp

    c_img = copy.copy(Controller.current_can.canvas_img)
    _h, _w, _c = c_img.shape

    y_idx_s = (Controller.current_can.height-_h)//2
    x_idx_s = (Controller.current_can.width-_w)//2
    
    if s_x <= x_idx_s:
      s_x = 0
    elif x_idx_s < s_x < _w + x_idx_s:
      s_x = s_x - x_idx_s
    else:
      s_x = _w
    if e_x <= x_idx_s:
      e_x = 0
    elif x_idx_s < e_x < _w + x_idx_s:
      e_x = e_x - x_idx_s
    else:
      e_x = _w
  
    if s_y <= y_idx_s:
      s_y = 0
    elif y_idx_s < s_y < _h + y_idx_s:
      s_y = s_y - y_idx_s
    else:
      s_y = _h
    if e_y <= y_idx_s:
      e_y = 0
    elif y_idx_s < e_y < _h + y_idx_s:
      e_y = e_y - y_idx_s
    else:
      e_y = _h

    self.s_x = s_x
    self.s_y = s_y

    selected_img = np.zeros(shape=(e_y - s_y, e_x - s_x, _c), dtype="uint8")
    deselected_img = copy.copy(c_img)
    for y in range(s_y, e_y):
      y_idx = y-s_y
      for x in range(s_x, e_x):
        x_idx = x - s_x
        selected_img[y_idx, x_idx] = c_img[y, x]
        deselected_img[y, x][:] = 255

    if self.mode == "crop":
      Controller.current_can.paint_canvas(selected_img)
      self.select_reset()
    elif self.mode == "select" and self.selected == 1:
      self.selected_img = selected_img
      self.deselected_img = deselected_img
      Controller.binding4 = Controller.current_can.canvas.bind("<Button-3>", self.copy_menu)
    elif self.mode == "select" and self.selected == 2:
      if self.r_click:
        self.r_click = False
        self.select_reset()
        return
      Controller.current_can.move_img(img_mv = self.selected_img, img_bg = self.deselected_img, p_x = self.end[0], p_y = self.end[1], save=True)
      self.select_confirm()

  def select_confirm(self):
    self.mk_alert(title="이미지 이동", msg="이동하시겠습니까?")
    btn_confirm = tk.Button(self.alert, text="예", padx=22, command=self.select_reset)
    btn_confirm.place(relx=0.2, rely=0.6)
    btn_cancel = tk.Button(self.alert, text="아니오", padx=10, command=self.select_cancel)
    btn_cancel.place(relx=0.57, rely=0.6)

  def select_cancel(self):
    if len(Controller.current_can.cancel_li) >0 :
      c_img = Controller.current_can.cancel_li.pop()
    Controller.current_can.paint_canvas(img = c_img, mode="c")
    self.select_reset()

  def mk_Rclick(self, event, text, command):
    pos_x = event.x_root - self.window.winfo_x() - 8
    pos_y = event.y_root - self.window.winfo_y() - 50
    self.paste_pos=[event.x, event.y]
    self.r_click = True
    self.r_frame = tk.Frame(self.window, bd=1)
    self.r_frame.place(x=pos_x, y=pos_y)
    btn_copy = tk.Button(self.r_frame, text=text, width=10, relief="flat", overrelief="sunken", command=command)
    btn_copy.pack()

  def copy_menu(self, event):
    self.mk_Rclick(event, text="복사", command=self.copy_chk)

  def paste_menu(self, event):
    self.mk_Rclick(event, text="붙여넣기", command=self.paste)

  def copy_chk(self):
    self.r_frame.destroy()
    self.mk_alert(title="복사", msg="복사되었습니다.")
    btn = tk.Button(self.alert, text="닫기", command=self.copy_confirm)
    btn.place(relx=0.42, rely=0.6)

  def copy_confirm(self):
    self.r_click = False
    self.select_reset(mode="copy")
    Controller.binding4 = Controller.current_can.canvas.bind("<Button-3>", self.paste_menu)
  
  def paste(self):
    Controller.current_can.canvas.delete(self.select_range)
    self.r_frame.destroy()
    self.r_click = False
    s_h, s_w = self.selected_img.shape[:2]
    self.paste_pos[0] = self.paste_pos[0] + s_w//2
    self.paste_pos[1] = self.paste_pos[1] + s_h//2
    Controller.current_can.move_img(img_mv = self.selected_img, img_bg = self.deselected_img, p_x = self.paste_pos[0], p_y = self.paste_pos[1])

  def select_reset(self, mode=None):
    self.selected = 0
    if self.alert is not None:
      self.alert.destroy()
    Controller.current_can.canvas.config(cursor="arrow")
    if mode != "copy":
      Controller.current_can.canvas.delete(self.select_range)
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

  def drag_fig(self, event):
    if self.dragging:
      if self.mode == 1 :
        Controller.current_can.canvas.create_line(self.start[0], self.start[1], event.x, event.y, fill=self.color, width=self.px, smooth=True)
        self.start = [event.x, event.y]
      elif self.mode == 2 :
        Controller.current_can.canvas.delete(self.shape)
        self.shape = Controller.current_can.canvas.create_line(self.start[0], self.start[1], event.x, event.y, fill=self.color, width=self.px)
      elif self.mode == 3:
        s_x, s_y = self.start
        e_x = event.x
        e_y = event.y
        if s_x > e_x:
          temp = s_x
          s_x = e_x
          e_x = temp
        if s_y > e_y:
          temp = s_y
          s_y = e_y
          e_y = temp
        point_x = e_x - s_x
        Controller.current_can.canvas.delete(self.shape)
        self.shape = Controller.current_can.canvas.create_polygon(point_x, s_y, s_x, e_y, e_x, e_y, outline=self.color, fill="white", width=self.px)
      elif self.mode == 4:
        Controller.current_can.canvas.delete(self.shape)
        self.shape = Controller.current_can.canvas.create_rectangle(self.start[0], self.start[1], event.x, event.y, outline=self.color, width=self.px)
      elif self.mode == 5:
        Controller.current_can.canvas.delete(self.shape)
        self.shape = Controller.current_can.canvas.create_oval(self.start[0], self.start[1], event.x, event.y, outline=self.color, width=self.px)
      
  def release_fig(self, event):
    Controller.current_can.canvas_save()
    self.select_reset()

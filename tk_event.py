import tkinter as tk
import copy
from turtle import width
import numpy as np
import cv2
from PIL import Image, ImageTk
from soupsieve import select
from tk_controller import Controller

class Widget_Event(Controller):
  def __init__(self, window, count=1):
    self.window = window
    self.widget = object
    self.drag_pos = []
    self.start = []
    self.end = []
    self.dragging = False
    self.count = count
    self.select_range = object
    self.selected = 0
    self.alert = None
    self.mode = "select"
    self.color = "black"
    self.selected_img = None
    self.deselected_img = None
    self.mv = None

  def set_widget(self, widget):
    self.widget = widget

  def click(self, event):
    self.dragging = True
    pos_x = event.x_root
    pos_y = event.y_root
    self.drag_pos = [pos_x, pos_y]

  def canvas_click(self, event):
    self.dragging = True
    pos_x = event.x_root
    pos_y = event.y_root
    self.drag_pos = [pos_x, pos_y]
    Controller.show_subwin(str(self.count))

  def move(self, event):
    if self.dragging:
      point_x = self.widget.winfo_x() + (event.x_root - self.window.winfo_x() - self.drag_pos[0]) - self.widget.winfo_height()//3
      point_y = self.widget.winfo_y() + (event.y_root - self.window.winfo_y() - self.drag_pos[1]) - 60
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

      self.drag_pos=[point_x, point_y]
      self.widget.place(x = self.drag_pos[0], y = self.drag_pos[1])
  
  def value_Check(self, value=str(), _min=0, _max=3840):
    if value.isdigit():
      valid = False
      if int(_min) <= int(value) <= int(_max):
        valid = True
    elif value == "":
      valid = True
    return valid
  
  def value_error(self):
    error = tk.Toplevel(self.window)
    error.title("오류메시지")
    error.geometry("300x100+450+400")
    error.resizable(False, False)
    error_msg = tk.Message(error, text="잘못된 범위의 값을 입력하였습니다.", width=300, aspect=300, anchor="center")
    error_msg.place(relx=0.17, rely=0.2)
    btn = tk.Button(error, text="닫기", command=error.destroy)
    btn.place(relx=0.42, rely=0.6)

  def release(self, event):
      self.widget.place(x = self.drag_pos[0], y = self.drag_pos[1])
      self.dragging = False
  
  def close(self):
      self.widget.destroy()

  def select_click(self, event):
    pos_x = event.x
    pos_y = event.y
    self.start = [pos_x, pos_y]
    self.selected += 1
  
  def select_right_click(self, event):
    pass
  
  def select_drag(self, event):
    if self.selected == 1:
      pos_x = event.x
      pos_y = event.y
      Controller.current_can.canvas.delete(self.select_range)
      self.select_range = Controller.current_can.canvas.create_rectangle(self.start[0], 
                          self.start[1], pos_x, pos_y, outline=self.color)
    elif self.selected == 2:
      pos_x = event.x
      pos_y = event.y
      _temp = Controller.current_can
      self.mv = _temp.move_paint(img_mv = self.selected_img, img_bg = self.deselected_img, p_x = pos_x, p_y = pos_y)
    else:
      self.select_reset()

  def select_released(self, event):
    pos_x = event.x
    pos_y = event.y
    self.end = [pos_x, pos_y]
    Controller.current_can.canvas.config(cursor="fleur")
    self.select()

  def crop_released(self, event):
    pos_x = event.x
    pos_y = event.y
    self.end = [pos_x, pos_y]
    alert = tk.Toplevel(self.window)
    alert.geometry("300x100+450+400")
    alert.resizable(False, False)
    self.alert = alert
    _var = tk.StringVar()
    _var.set("해당 영역만 남기고 삭제하시겠습니까?")
    alert_msg = tk.Message(self.alert, textvariable=_var, width=300, aspect=300, anchor="center")
    alert_msg.pack(pady=20)
    btn_confirm = tk.Button(alert, text="예", padx=22, command=self.select)
    btn_confirm.place(relx=0.2, rely=0.6)
    btn_cancel = tk.Button(alert, text="아니오", padx=10, command=self.select_reset)
    btn_cancel.place(relx=0.57, rely=0.6)
    Controller.current_can.canvas.unbind("<Button-1>")
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

    _temp = Controller.current_can
    c_img = copy.copy(_temp.canvas_img)
    _h, _w, _c = c_img.shape

    y_idx_s = (_temp.height-_h)//2
    x_idx_s = (_temp.width-_w)//2
    
    if s_x <= x_idx_s:
      s_x = 0
    else:
      s_x = s_x - x_idx_s
    if e_x - x_idx_s >= _w:
      e_x = _w
    elif e_x - x_idx_s > 0:
      e_x = e_x - x_idx_s
    else :
      e_x = 0
  
    if s_y <= y_idx_s:
      s_y = 0
    else:
      s_y = s_y - y_idx_s
    if e_y - y_idx_s >= _h:
      e_y = _h
    elif e_y - y_idx_s > 0:
      e_y = e_y - y_idx_s
    else:
      e_y = 0

    self.s_x = s_x
    self.s_y = s_y
    selected_img = np.zeros(shape=(e_y-s_y, e_x-s_x, _c), dtype="uint8")
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
    elif self.mode == "select" and self.selected == 2:
      self.select_confirm()

  def select_reset(self):
    self.selected = 0
    self.alert.destroy()
    Controller.current_can.canvas.config(cursor="arrow")

    Controller.current_can.canvas.delete(self.select_range)
    Controller.current_can.canvas.unbind("<Button-1>", Controller.binding1)
    Controller.current_can.canvas.unbind("<B1-Motion>", Controller.binding2)
    Controller.current_can.canvas.unbind("<ButtonRelease-1>", Controller.binding3)

  def select_confirm(self):
    alert = tk.Toplevel(self.window)
    alert.geometry("300x100+450+400")
    alert.resizable(False, False)
    self.alert = alert
    _var = tk.StringVar()
    _var.set("이동하시겠습니까?")
    alert_msg = tk.Message(self.alert, textvariable=_var, width=300, aspect=300, anchor="center")
    alert_msg.pack(pady=20)
    btn_confirm = tk.Button(alert, text="예", padx=22, command=self.select_reset)
    btn_confirm.place(relx=0.2, rely=0.6)
    btn_cancel = tk.Button(alert, text="아니오", padx=10, command=self.select_cancel)
    btn_cancel.place(relx=0.57, rely=0.6)

  def select_cancel(self):
    _temp = Controller.current_can
    c_img = copy.copy(_temp.canvas_img)
    Controller.current_can.paint_canvas(img = c_img, mode="c")
    self.select_reset()



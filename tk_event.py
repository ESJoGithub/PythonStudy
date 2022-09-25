import tkinter as tk
from tk_controller import Controller

class Widget_Event(Controller):
  def __init__(self, window, count=1):
    self.window = window
    self.widget = object
    self.drag_pos = []
    self.dragging = False
    self.count = count
  
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
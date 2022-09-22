import tkinter as tk

class Widget_Event:
  def __init__(self, window):
    self.window = window
    self.pWidget = None
    self.widget = None
    self.drag_pos = []
    self.dragging = False
  
  def set_widget(self, widget):
    self.widget = widget
  
  def set_pWidget(self, pWidget):
    self.pWidget = pWidget

  def click(self, event):
    self.dragging = True
    pos_x = event.x_root
    pos_y = event.y_root
    self.drag_pos = [pos_x, pos_y]

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
  
  def value_Check(self):
    if self.isdigit():
      if (int(self) <= 3840 and int(self) >= 0):
        valid = True
    elif self == "":
      valid = True
    return valid
  
  def value_error(self):
    error_msg = tk.Message(self.window, text="잘못된 범위의 값을 입력하였습니다.", width=100, relief="solid")
    error_msg.pack()

  def release(self, event):
      self.widget.place(x = self.drag_pos[0], y = self.drag_pos[1])
      self.dragging = False
  
  def close(self):
      self.widget.destroy()
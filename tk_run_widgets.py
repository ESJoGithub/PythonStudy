import tkinter as tk
from tk_widget import Widget

class Run_widget(Widget):
  def __init__(self, window, count=0, width = 300, height=200, x = 10, y = 50):
    super().__init__(window)
    self.window = window
    self.width = width
    self.height = height
    self.scale = None
    self.count=0
    self.x = self.window.winfo_width() - (width+x)
    self.y = self.window.winfo_y() - self.window.winfo_rooty() + (count*height) + y
    '''window.winfo_with() 윈도우 안에서 오른쪽 끝, window.winfo_height() 윈도우 안에서 최 하단'''

  def get_Scale(self, mode="blur", title = "이미지 필터", start=0.0, end=100.0, term=1.0, tick=10.0):
    frame, frame2 = self.get_widget(title)
    scale=tk.Scale(frame2, orient="horizontal",
                  tickinterval=tick, from_=start, to=end, resolution=term, 
                  showvalue=True, length=self.width, width=10, sliderlength=15)
    scale.grid(row=1, column=1, columnspan=5)
    self.scale = scale
    filter_button = tk.Button(frame2, text="확인")
    filter_button.grid(row=2, column=3)
    self.count += 1
    return filter_button

  def get_Spin(self, title="캔버스 사이즈 조정"):
    frame, frame2 = self.get_widget(title)

    validate_command=(frame2.register(self.value_Check), "%P")
    invalid_command=(frame2.register(self.value_error), "%P")

    label_w = tk.Label(frame2, text="너비 : ", anchor="e")
    label_w.grid(row=1, column=1)
    _width_size = tk.Spinbox(frame2)
    _width_size.config(from_=10, to=self.window_winfo_width(), increment=1,
                      textvariable=self.width,
                      validate="key", 
                      validatecommand=validate_command,
                      invalidcommand=invalid_command)
    _width_size.grid(row=1, column=2)
    label_px1 = tk.Label(frame2, text="픽셀", anchor="w")
    label_px1.grid(row=1, column=3)
    label_h = tk.Label(frame2, text="높이 : ", anchor="e")   
    label_h.grid(row=1, column=4)                   
    _height_size = tk.Spinbox(frame2)
    _height_size.config(from_=10, to=self.window_winfo_height(), increment=1,
                      textvariable=self.height,
                      validate="key", 
                      validatecommand=validate_command,
                      invalidcommand=invalid_command)
    _height_size.grid(row=1, column=5)                      
    label_px2 = tk.Label(frame2, text="픽셀", anchor="w")
    label_px2.grid(row=1, column=6)
    size_button = tk.Button(frame2, text="확인")
    size_button.grid(row=2, column=3, columnspan=2) 
    return frame

import tkinter as tk
from tk_widget import Widget

class Run_widget(Widget):
  def __init__(self, window, count=0, width = 300, height=130, x = 10, y = 50):
    super().__init__(window)
    self.window = window
    self.width = width
    self.height = height
    self.scale = None
    self.radio_G = None
    self.spin1 = None
    self.spin2 = None
    self.spin3 = None
    self.spin4 = None
    self.x = self.window.winfo_width() - ((count//6+1)*(width+x))
    self.y = self.window.winfo_y() - self.window.winfo_rooty() + (count%6*height) + y
    '''window.winfo_with() 윈도우 안에서 오른쪽 끝, window.winfo_height() 윈도우 안에서 최 하단'''

  def get_Scale(self, title = "이미지 필터", start=0.0, end=100.0, term=1.0, tick=10.0):
    frame2 = self.get_widget(title)[1]
    scale=tk.Scale(frame2, orient="horizontal",
                  tickinterval=tick, from_=start, to=end, resolution=term, 
                  showvalue=True, length=self.width, width=10, sliderlength=15)
    scale.grid(row=1, column=1, columnspan=5)
    self.scale = scale
    filter_button = tk.Button(frame2, text="확인")
    filter_button.grid(row=2, column=3)
    return filter_button

  def get_radio(self, title = "RGB -> Gray"):
    frame2 = self.get_widget(title)[1]
    radio_G = tk.IntVar()
    self.radio_G = radio_G
    default_Btn = tk.Radiobutton(frame2, text="Default", value=0, variable=radio_G, width=10, height=2)
    dark_Btn = tk.Radiobutton(frame2, text="Darker", value=1, variable=radio_G, width=11, height=2)
    rgb_Btn = tk.Radiobutton(frame2, text="RGB-Gray", value=2, variable=radio_G, width=10, height=2)
    r_Btn = tk.Radiobutton(frame2, text="R-Gray", value=3, variable=radio_G, width=10, height=2)
    g_Btn = tk.Radiobutton(frame2, text="G-Gray", value=4, variable=radio_G, width=10, height=2)
    b_Btn = tk.Radiobutton(frame2, text="B-Gray", value=5, variable=radio_G, width=10, height=2)
    rgb_Btn.grid(row=1, column=5, columnspan=2)
    default_Btn.grid(row=1, column=1, columnspan=2)
    dark_Btn.grid(row=1, column=3, columnspan=2)
    r_Btn.grid(row=2, column=1, columnspan=2)
    g_Btn.grid(row=2, column=3, columnspan=2)
    b_Btn.grid(row=2, column=5, columnspan=2)
    g_button = tk.Button(frame2, text="확인")
    g_button.grid(row=3, column=3, columnspan=2)
    return g_button

  def get_Spin(self, title="캔버스 사이즈 조정"):
    frame2 = self.get_widget(title)[1]
    frame2.config(height=200)
    set_width = self.window.winfo_width()
    set_height = self.window.winfo_height()
    _val1=(frame2.register(self.value_Check), "%P", 0, set_width)
    _val2=(frame2.register(self.value_Check), "%P", 0, set_height)
    _inv=(frame2.register(self.value_error))
    _w_1 = tk.Label(frame2, text=" 너비(width) 입력", padx=5, pady=2, anchor="w")
    _w_2 = tk.Label(frame2, text="픽셀(pixel)      ", padx=2, pady=2, anchor="w")
    spin_width = tk.Spinbox(frame2, from_=0, to=set_width, increment=1, validate="key", 
                            validatecommand=_val1, invalidcommand=_inv, wrap=True)
    spin_width.grid(row=1, column=2)
    _w_1.grid(row=1, column=1)
    _w_2.grid(row=1, column=3, columnspan=2)
    _h_1 = tk.Label(frame2, text=" 높이(height) 입력", padx=5, pady=2, anchor="w")
    _h_2 = tk.Label(frame2, text="픽셀(pixel)      ", padx=2, pady=2, anchor="w")
    spin_height = tk.Spinbox(frame2, from_=0, to=set_height, increment=1, validate="key", 
                          validatecommand=_val2, invalidcommand=_inv, wrap=True)
    spin_height.grid(row=2, column=2)
    _h_1.grid(row=2, column=1)
    _h_2.grid(row=2, column=3, columnspan=2)

    spin_btn = tk.Button(frame2, text="확인")
    spin_btn.grid(row=4, column=2)
    self.spin1, self.spin2 = spin_width, spin_height
    return spin_btn

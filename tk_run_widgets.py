import tkinter as tk
from turtle import width
from tk_widget import Widget
from tk_event import Widget_Event

class Run_widget(Widget):
  def __init__(self, window, count=0, width = 300, height=137, x = 10, y = 50):
    super().__init__(window)
    self.window = window
    self.width = width
    self.height = height
    self.scale = None
    self.radio_G = None
    self.spin = None
    self.spin1 = None
    self.spin2 = None
    self.check = True
    self.x = self.window.winfo_width() - ((count//6+1)*(width+x))
    self.y = self.window.winfo_y() - self.window.winfo_rooty() + (count%6*height) + y
    '''window.winfo_with() 윈도우 안에서 오른쪽 끝, window.winfo_height() 윈도우 안에서 최 하단'''

  def get_Scale(self, title = "이미지 필터", start=0.0, end=100.0, term=1.0, tick=10.0):
    frame2 = self.get_widget(title)[1]
    scale=tk.Scale(frame2, orient="horizontal",
                  tickinterval=tick, from_=start, to=end, resolution=term, 
                  showvalue=True, length=self.width, width=10, sliderlength=15)
    scale.grid(row=1, column=1, columnspan=5, pady=5)
    self.scale = scale
    filter_button = tk.Button(frame2, text="확인")
    filter_button.grid(row=2, column=3, pady=7)
    return filter_button

  def get_radio(self, title = "RGB -> Gray"):
    frame2 = self.get_widget(title)[1]
    radio_G = tk.IntVar()
    self.radio_G = radio_G
    default_Btn = tk.Radiobutton(frame2, text="Default", value=0, variable=radio_G, width=10, height=2)
    dark_Btn = tk.Radiobutton(frame2, text="Darker", value=1, variable=radio_G, width=11, height=2)
    rgb_Btn = tk.Radiobutton(frame2, text="RGB-Gray", value=2, variable=radio_G, width=10, height=2)
    r_Btn = tk.Radiobutton(frame2, text="R-Gray", value=3, variable=radio_G, width=10)
    g_Btn = tk.Radiobutton(frame2, text="G-Gray", value=4, variable=radio_G, width=10)
    b_Btn = tk.Radiobutton(frame2, text="B-Gray", value=5, variable=radio_G, width=10)
    rgb_Btn.grid(row=1, column=5, columnspan=2, padx=2.5)
    default_Btn.grid(row=1, column=1, columnspan=2)
    dark_Btn.grid(row=1, column=3, columnspan=2)
    r_Btn.grid(row=2, column=1, columnspan=2, pady=1.5)
    g_Btn.grid(row=2, column=3, columnspan=2)
    b_Btn.grid(row=2, column=5, columnspan=2, padx=2.5)
    g_button = tk.Button(frame2, text="확인")
    g_button.grid(row=3, column=1, columnspan=6, pady = 5.3)
    return g_button

  def get_Spin(self, title="캔버스 사이즈 조정"):
    frame2 = self.get_widget(title)[1]
    frame2.config(height=200)
    set_width = self.window.winfo_width()
    set_height = self.window.winfo_height()
    spin_Event = Widget_Event(self.window)
    _val1=(frame2.register(spin_Event.value_Check), "%P", 0, set_width)
    _val2=(frame2.register(spin_Event.value_Check), "%P", 0, set_height)
    _inv=(frame2.register(spin_Event.value_error))
    _w_1 = tk.Label(frame2, text=" 너비(width) 입력", padx=5, pady=7, anchor="w")
    _w_2 = tk.Label(frame2, text="픽셀(pixel)      ", padx=2, pady=7, anchor="w")
    spin_width = tk.Spinbox(frame2, from_=0, to=set_width, increment=1, validate="key", 
                            validatecommand=_val1, invalidcommand=_inv, wrap=True, width=12)
    spin_width.grid(row=1, column=2)
    _w_1.grid(row=1, column=1)
    _w_2.grid(row=1, column=3, columnspan=2, padx=3)
    _h_1 = tk.Label(frame2, text=" 높이(height) 입력", padx=5, pady=7, anchor="w")
    _h_2 = tk.Label(frame2, text="픽셀(pixel)      ", padx=2, pady=7, anchor="w")
    spin_height = tk.Spinbox(frame2, from_=0, to=set_height, increment=1, validate="key", 
                          validatecommand=_val2, invalidcommand=_inv, wrap=True, width=12)
    spin_height.grid(row=2, column=2)
    _h_1.grid(row=2, column=1)
    _h_2.grid(row=2, column=3, columnspan=2, padx=3)

    spin_btn = tk.Button(frame2, text="확인")
    spin_btn.grid(row=3, column=1, columnspan=4, pady = 7)
    self.spin1, self.spin2 = spin_width, spin_height

    return spin_btn

  def get_photosize(self, title="이미지 사이즈 조정", _img=None):

    frame2 = self.get_widget(title)[1]
    set_width = self.window.winfo_width()
    set_height = self.window.winfo_height()
    photo_h, photo_w = _img.shape[:2]
    max_ratio = 100
    if photo_w > photo_h:
      max_ratio = set_width*100//photo_w
    else:
      max_ratio = set_height*100//photo_h

    ratio_text = tk.StringVar()
    width_text = tk.StringVar()
    height_text = tk.StringVar()
    ratio_text.set("100")
    width_text.set(str(photo_w))
    height_text.set(str(photo_h))

    chk_val = tk.BooleanVar()

    def command_set():
      if chk_val.get() :
        self.check = True
        self.spin.config(state=tk.NORMAL)
        self.spin.config(command=lambda: value_set(mode=0))
        self.spin1.config(command=lambda: value_set(mode=1))
        self.spin2.config(command=lambda: value_set(mode=2))
      elif not chk_val.get():
        self.check = False
        self.spin.config(state=tk.DISABLED)
        self.spin1.config(command=reset)
        self.spin2.config(command=reset)

    def value_set(mode=0):
      if mode == 0:
        _ratio= int(self.spin.get())
        _w = photo_w*_ratio//100
        _h = photo_h*_ratio//100
        width_text.set(str(_w))
        height_text.set(str(_h))
      elif mode == 1:
        _w = int(self.spin1.get())
        _ratio = _w* 100 // photo_w
        _h = photo_h*_ratio//100
        ratio_text.set(str(_ratio))
        height_text.set(str(_h))
      elif mode == 2:
        _h = int(self.spin2.get())
        _ratio = _h* 100 // photo_h
        _w = photo_w*_ratio//100
        ratio_text.set(str(_ratio))
        width_text.set(str(_w))
    
    def reset():
      pass

    size_Event = Widget_Event(self.window)
    _val_r=(frame2.register(size_Event.value_Check), "%P", 0, max_ratio)
    _val1=(frame2.register(size_Event.value_Check), "%P", 0, set_width)
    _val2=(frame2.register(size_Event.value_Check), "%P", 0, set_height)
    _inv=(frame2.register(size_Event.value_error))

    _chk = tk.Label(frame2, text="비율\n유지", padx=9, width=5)
    _r_1 = tk.Label(frame2, text="비율 입력:", pady=3, anchor="e", width=10)
    _r_2 = tk.Label(frame2, text="% ", anchor="w", width=10)
    ratio =  tk.Spinbox(frame2, from_=0, to=max_ratio, increment=1, validate="key",
                        validatecommand=_val_r, invalidcommand=_inv, wrap=True, width=10,
                        textvariable=ratio_text)
    self.spin = ratio
    _chk.grid(row=1, rowspan=2, column=1)
    _r_1.grid(row=1, column=2)
    ratio.grid(row=1, column=3, columnspan=2)
    _r_2.grid(row=1, column=5, padx=3)

    _w_1 = tk.Label(frame2, text="너비(width):", padx=3, pady=3, anchor="e", width=10)
    _w_2 = tk.Label(frame2, text="픽셀(pixel)", padx=2, pady=3, anchor="w", width=10)
    spin_width = tk.Spinbox(frame2, from_=0, to=set_width, increment=1, validate="key", 
                            validatecommand=_val1, invalidcommand=_inv, wrap=True, width=10,
                            textvariable=width_text)
    self.spin1 = spin_width
    _w_1.grid(row=2, column=2)
    spin_width.grid(row=2, column=3, columnspan=2)
    _w_2.grid(row=2, column=5, padx=3)

    _h_1 = tk.Label(frame2, text="높이(height):", padx=3, pady=3, anchor="e", width=10)
    _h_2 = tk.Label(frame2, text="픽셀(pixel)", padx=2, pady=3, anchor="w", width=10)
    spin_height = tk.Spinbox(frame2, from_=0, to=set_height, increment=1, validate="key", 
                            validatecommand=_val2, invalidcommand=_inv, wrap=True, width=10,
                            textvariable=height_text)
    self.spin2 = spin_height
    ratio_chk = tk.Checkbutton(frame2, anchor="n", variable=chk_val, command=command_set)
    ratio_chk.invoke()
    ratio_chk.grid(row=3, column=1)
    _h_1.grid(row=3, column=2)
    spin_height.grid(row=3, column=3, columnspan=2)
    _h_2.grid(row=3, column=5, padx=3)

    spin_btn = tk.Button(frame2, text="확인")
    spin_btn.grid(row=4, column=1, columnspan=5, pady = 2.3)

    return spin_btn
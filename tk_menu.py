import tkinter as tk
from tk_methods import Methods
from tk_controller import Controller
from PIL import Image, ImageTk

class menubar(Methods):
  def __init__(self, window):
    super().__init__(window)
    self.window = window
    self.scale = 0
    self.btn_img1 = None
    self.btn_img2 = None
    self.btn_img3 = None
    self.btn_img4 = None
    self.btn_img5 = None
    self.btn_img6 = None
    self.btn_img7 = None
    self.btn_img8 = None
    self.btn1 = None
    self.btn2 = None
    self.btn3 = None
    self.btn4 = None
    self.btn5 = None
    self.btn6 = None
    self.btn7 = None
    self.btn8 = None

  def run_menu(self):

    menubar = tk.Menu(self.window)

    menu_1 = tk.Menu(menubar, tearoff=0)      
    menu_1.add_command(label="새로만들기", command = self.new_open)
    menu_1.add_command(label="열기", command=self.file_open)
    menu_1.add_separator()
    menu_1.add_command(label="저장", command=self.file_save)
    menu_1.add_command(label="다른 이름으로 저장", command = lambda: self.file_save(mode="saveas"))
    menu_1.add_separator()
    menu_1.add_command(label="닫기", command = self.close)
    menubar.add_cascade(label="파일", menu=menu_1)

    menu_2 = tk.Menu(menubar, tearoff=0)      
    menu_2.add_command(label="실행 취소", command= self.cancel)
    menu_2.add_command(label="다시 실행", command= self.reload)
    menu_2.add_separator()
    menu_2.add_command(label="잘라내기")
    menu_2.add_command(label="복사")
    menu_2.add_command(label="붙여넣기")
    menu_2.add_separator()
    menu_2.add_command(label="잘라낸 부분 저장")
    menubar.add_cascade(label="편집", menu=menu_2)

    menu_3 = tk.Menu(menubar, tearoff=0)  
    menu_3.add_command(label="RGB -> Gray", command=self.gray_menu)
    menu_3.add_command(label="RGB -> 흑백", command=self.binary_menu)
    menu_3.add_command(label="RGB -> HSV", command=self.rgb_2HSV)
    menu_3.add_command(label="HSV -> RGB", command=self.hsv_2rgb)    
    menu_3.add_separator()
    menu_3.add_command(label="명도", command=self.brightness_control)
    menu_3.add_command(label="대비", command=self.contrast_control)
    menu_3.add_command(label="색조", command=lambda: self.hsv_control(mode="Hue"))
    menu_3.add_command(label="채도", command=lambda: self.hsv_control(mode="saturation"))
    menu_3.add_separator()
    menu_3.add_command(label="이미지 크기", command=self.reset_photo_size)
    menu_3.add_command(label="캔버스 크기", command=self.reset_canvas_size)
    menu_3.add_separator()
    menu_3.add_command(label="이미지 180도 회전", command=lambda: self.rotation(mode=2))
    menu_3.add_command(label="이미지 90도 시계 방향 회전", command=lambda: self.rotation(mode=1))
    menu_3.add_command(label="이미지 90도 시계 반대 방향 회전", command=lambda: self.rotation(mode=3))
    menu_3.add_command(label="이미지 임의 각도 회전")
    menu_3.add_separator()
    menu_3.add_command(label="상하반전", command=lambda: self.symmetric(mode="x"))
    menu_3.add_command(label="좌우반전", command=lambda: self.symmetric(mode="y"))
    menubar.add_cascade(label="이미지", menu=menu_3)

    menu_4= tk.Menu(menubar, tearoff=0)      
    menu_4.add_command(label="문자삽입")
    menu_4.add_command(label="글꼴")
    menubar.add_cascade(label="문자", menu=menu_4)

    menu_5 = tk.Menu(menubar, tearoff=0)      
    menu_5.add_command(label="흐리게", command=self.set_blur)
    menu_5.add_command(label="선명하게", command=self.sharpen)
    menu_5.add_command(label="색상추출")
    menubar.add_cascade(label="필터", menu=menu_5)

    menu_6 = tk.Menu(menubar, tearoff=0)
    menu_6.add_command(label="ESJo")
    menubar.add_cascade(label="정보", menu=menu_6)
    self.window.config(menu=menubar) 

  def run_submenu(self):
    x = self.window.winfo_x()
    y = self.window.winfo_y()
    sb_mn = tk.Toplevel(self.window)
    sb_mn.title("")
    sb_mn.geometry("50x450+%d+%d"%(x+80, y+150))
    sb_mn.resizable(False, False)
    sb_mn.wm_transient(self.window)
    btn_img1 = Image.open("01_open.png")
    btn_img2 = Image.open("02_save.png")
    btn_img3 = Image.open("03_select.png")
    btn_img4 = Image.open("04_crop.png")
    btn_img5 = Image.open("05_line.png")
    btn_img6 = Image.open("06_shapes.png")
    btn_img7 = Image.open("07_pen.png")
    btn_img8 = Image.open("08_dopper.png")
    btn_img1 = btn_img1.resize((30, 30))
    btn_img2 = btn_img2.resize((30, 30))
    btn_img3 = btn_img3.resize((30, 30))
    btn_img4 = btn_img4.resize((30, 30))
    btn_img5 = btn_img5.resize((30, 30))
    btn_img6 = btn_img6.resize((30, 30))
    btn_img7 = btn_img7.resize((30, 30))
    btn_img8 = btn_img8.resize((30, 30))
    self.btn_img1 = ImageTk.PhotoImage(btn_img1)
    self.btn_img2 = ImageTk.PhotoImage(btn_img2)
    self.btn_img3 = ImageTk.PhotoImage(btn_img3)
    self.btn_img4 = ImageTk.PhotoImage(btn_img4)
    self.btn_img5 = ImageTk.PhotoImage(btn_img5)
    self.btn_img6 = ImageTk.PhotoImage(btn_img6)
    self.btn_img7 = ImageTk.PhotoImage(btn_img7)
    self.btn_img8 = ImageTk.PhotoImage(btn_img8)

    self.btn1 = tk.Button(sb_mn, image=self.btn_img1, width=35, height=35, command=self.file_open,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn1.grid(row=1, column=1, padx=5, pady=7)
    self.btn2 = tk.Button(sb_mn, image=self.btn_img2, width=35, height=35, command=self.file_save,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn2.grid(row=2, column=1, padx=5, pady=7)
    self.btn3 = tk.Button(sb_mn, image=self.btn_img3, width=35, height=35, command=self.select_event,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn3.grid(row=3, column=1, padx=5, pady=7)
    self.btn4 = tk.Button(sb_mn, image=self.btn_img4, width=35, height=35, command=lambda:self.select_event(mode="crop"),
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn4.grid(row=4, column=1, padx=5, pady=7)
    self.btn5 = tk.Button(sb_mn, image=self.btn_img5, width=35, height=35,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn5.grid(row=5, column=1, padx=5, pady=7)
    self.btn6 = tk.Button(sb_mn, image=self.btn_img6, width=35, height=35,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn6.grid(row=6, column=1, padx=5, pady=7)
    self.btn7 = tk.Button(sb_mn, image=self.btn_img7, width=35, height=35,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn7.grid(row=7, column=1, padx=5, pady=7)
    self.btn8 = tk.Button(sb_mn, image=self.btn_img8, width=35, height=35,
                          relief="flat", overrelief="sunken", activebackground="gray90")
    self.btn8.grid(row=8, column=1, padx=5, pady=7)
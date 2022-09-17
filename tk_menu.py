from re import X
from statistics import mode
import tkinter as tk
from typing_extensions import IntVar
from tk_methods import Methods

class menubar(Methods):
  def __init__(self, window):
    super().__init__(window)
    self.window = window
    self.scale = 0

  def run_menu(self):

    menubar = tk.Menu(self.window)

    menu_1 = tk.Menu(menubar, tearoff=0)      
    menu_1.add_command(label="새로만들기", command = self.new_open)
    menu_1.add_command(label="열기", command=self.file_open)
    menu_1.add_separator()
    menu_1.add_command(label="다른 이름으로 저장")
    menu_1.add_command(label="저장")
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
    menu_3.add_command(label="RGB")
    menu_3.add_command(label="HSV")
    menu_3.add_separator()
    menu_3.add_command(label="명도, 대비")
    menu_3.add_command(label="색조, 채도")
    menu_3.add_command(label="gray, 흑백")
    menu_3.add_separator()
    menu_3.add_command(label="이미지 크기")
    menu_3.add_command(label="캔버스 크기")
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
    menu_5.add_command(label="흐리게", command=self.filter_menu)
    menu_5.add_command(label="선명하게", command=lambda : self.filter_menu(mode="sharpen"))
    menu_5.add_command(label="모자이크")
    menu_5.add_command(label="색상추출")
    menubar.add_cascade(label="필터", menu=menu_5)

    menu_6 = tk.Menu(menubar, tearoff=0)
    menu_6.add_command(label="ESJo")
    menubar.add_cascade(label="정보", menu=menu_6)
    self.window.config(menu=menubar) 


import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x280")

listbox = tkinter.Listbox(window)

# for문을 활용하여 "item1"부터 "item100"까지 총 100개 아이템 생성
for i in range(1, 101):
    listbox.insert(tkinter.END, "item{}".format(str(i)))


def page():
    '''yview_scroll(num, str)활용하여 위젯 사이즈 단위로 이동'''
    listbox.yview_scroll(1, "pages")


def line():
    '''yview_scroll(num, str)활용하여 줄 단위(3줄 씩)로 이동'''
    listbox.yview_scroll(3, "units")


def movetop():
    '''yview_moveto(0)활용하여 리스트박스 최상단으로 이동'''
    listbox.yview_moveto(0)


def movebottom():
    '''yview_moveto(1)활용하여 리스트박스 최하단으로 이동'''
    listbox.yview_moveto(1)


# 클릭시 각 메소드를 호출하는 버튼 생성
btn_page = tkinter.Button(window, text="위젯 높이 넘김", command=page, width=20)
btn_line = tkinter.Button(window, text="줄 넘김", command=line, width=20)
btn_moveT = tkinter.Button(window, text="처음으로 이동", command=movetop, width=20)
btn_moveB = tkinter.Button(window, text="끝으로 이동", command=movebottom, width=20)

# 리스트박스 및 버튼 배치
listbox.pack(side="top")
btn_moveB.pack(side="bottom")
btn_page.pack(side="bottom")
btn_line.pack(side="bottom")
btn_moveT.pack(side="bottom")
window.mainloop()

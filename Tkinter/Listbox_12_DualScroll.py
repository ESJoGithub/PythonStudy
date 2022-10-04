import tkinter

window = tkinter.Tk()
window.title("List_scroll")

# 윈도우 안에 리스트박스와 스크롤바를 함께 묶어줄 frame 생성
frame1 = tkinter.Frame(window)
frame2 = tkinter.Frame(window)
frame1.pack(side="left", padx=15)  # 프레임 간 여백 설정
frame2.pack(side="left")

# frame 안에 listbox 생성, 좌측 정렬
listbox1 = tkinter.Listbox(frame1, width=40)
listbox2 = tkinter.Listbox(frame2, width=40)

# for문을 활용하여 각각의 리스트박스에 "1~12월", "1~31일" 항목 입력
for i in range(1, 32):
    listbox2.insert(tkinter.END, "{}일".format(str(i)))
    if i < 13:
        listbox1.insert(tkinter.END, "{}월".format(str(i)))

# frame 안에 스크롤 바 생성
# frame 우측 정렬, frame 높이만큼 늘려서 채우기
# 각각의 listbox 연결
scroll1 = tkinter.Scrollbar(frame1, command=listbox1.yview)
scroll1.pack(side="right", fill="y")
scroll2 = tkinter.Scrollbar(frame2, command=listbox2.yview)
scroll2.pack(side="right", fill="y")

# yscrollcommand에 위에 생성한 스크롤바를 연결
listbox1.config(yscrollcommand=scroll1.set)
listbox2.config(yscrollcommand=scroll2.set)

listbox1.pack()
listbox2.pack()
window.mainloop()

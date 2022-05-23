import tkinter

window = tkinter.Tk()
window.title("List_scroll")

# 윈도우 안에 리스트박스와 스크롤바를 함께 묶어줄 frame 생성
frame = tkinter.Frame(window)
frame.pack()

# frame 안에 스크롤 바 생성
# frame 우측 정렬, frame 높이만큼 늘려서 채우기
scroll_list = tkinter.Scrollbar(frame)
scroll_list.pack(side="right", fill="y")

# frame 안에 listbox 생성, 좌측 정렬
# yscrollcommand에 위에 생성한 스크롤바를 연결
listbox = tkinter.Listbox(frame)
listbox.config(yscrollcommand=scroll_list.set, width=30, height=10)
listbox.pack(side="left")

# scroll 바의 설정에서 생성된 리스트박스 연결
scroll_list.config(command=listbox.yview)

# for문을 활용하여 "1일"부터 "31일"까지 총 31개 아이템 생성
for i in range(1, 32):
    listbox.insert(tkinter.END, "{}일".format(str(i)))

window.mainloop()

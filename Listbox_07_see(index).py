import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x250")

# 선택된 항목을 점선 테두리의 사각형으로 표시하도록 설정
listbox = tkinter.Listbox(window, activestyle="dotbox")

# for문을 활용하여 "item0"부터 "item29"까지 총 30개 아이템 생성
for i in range(30):
    listbox.insert(tkinter.END, "item{}".format(str(i)))

# see(index)메소드 활용하여 해당 항목이 보이도록 리스트박스 위치 조정
listbox.see(29)

listbox.pack()
window.mainloop()

import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("400x200")

listbox = tkinter.Listbox(
    window,
    width=50, height=5,
    selectbackground="#004d40",  # 선택 항목 블록 배경색
    selectforeground="gray",     # 선택 항목 블록 문자열 색상
    selectborderwidth=10         # 선택 항목 블록 테두리 두께
    # 색상은 문자 또는 HEX 색상코드 활용
)

# for문을 활용하여 "1일"부터 "31일"까지 총 31개 아이템 생성
for i in range(1, 32):
    listbox.insert(tkinter.END, "{}일".format(str(i)))

listbox.pack()
window.mainloop()

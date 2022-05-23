import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("400x100")

listbox = tkinter.Listbox(
    window,
    width=50, height=5,     # 너비, 높이 설정
    relief="raised",        # 테두리 모양
    bd=5,                   # 테두리 두께 borderwidth / bd 동일
    bg="#fffaaa",           # 리스트박스 배경 색상 background / bg 동일
    fg="blue"               # 리스트박스 문자열 색상 foreground / fg 동일
    # 색상은 문자 또는 HEX 색상코드 활용
)

# for문을 활용하여 "1일"부터 "31일"까지 총 31개 아이템 생성
for i in range(1, 32):
    listbox.insert(tkinter.END, "{}일".format(str(i)))

listbox.pack()
window.mainloop()

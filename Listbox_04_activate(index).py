import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x250")

# 선택된 항목을 점선 테두리의 사각형으로 표시하도록 설정
listbox = tkinter.Listbox(window, activestyle="dotbox")

# for문을 활용하여 "item0"부터 "item29"까지 총 30개 아이템 생성
for i in range(30):
    listbox.insert(tkinter.END, "item{}".format(str(i)))

# listbox의 5번째 인덱스를 활성화하는 pick 함수 정의


def pick():
    '''activate(index) 메소드를 활용하여 index에 해당하는 항목 활성화'''
    listbox.activate(5)


# 클릭시 pick()메소드를 호출하는 버튼 생성
btn = tkinter.Button(window, text="항목선택", command=pick)

# 리스트박스를 윈도우의 상단에, 버튼을 하단에 배치
listbox.pack(side="top")
btn.pack(side="bottom")
window.mainloop()

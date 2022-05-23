import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x250")

# 여러 개의 항목을 동시에 선택할 수 있도록 설정
listbox = tkinter.Listbox(window, selectmode="extended")

# for문을 활용하여 "item0"부터 "item29"까지 총 30개 아이템 생성
for i in range(30):
    listbox.insert(tkinter.END, "item{}".format(str(i)))

# listbox의 선택항목을 반환하는 pick 함수 정의


def pick():
    ''' curselection() 메소드를 활용하여 사용자 선택 항목의 인덱스를 튜플로 반환받음'''
    s_items = listbox.curselection()
    print("선택된 항목: ", s_items)


# 클릭시 pick()메소드를 호출하는 버튼 생성
btn = tkinter.Button(window, text="항목선택", command=pick)

# 리스트박스를 윈도우의 상단에, 버튼을 하단에 배치
listbox.pack(side="top")
btn.pack(side="bottom")
window.mainloop()

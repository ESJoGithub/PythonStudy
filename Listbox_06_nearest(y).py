import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x250")

# 선택된 항목을 점선 테두리의 사각형으로 표시하도록 설정
listbox = tkinter.Listbox(window, activestyle="dotbox")

# for문을 활용하여 "item0"부터 "item29"까지 총 30개 아이템 생성
for i in range(30):
    listbox.insert(tkinter.END, "item{}".format(str(i)))


def pick():
    ''' curselection() 메소드를 활용하여 사용자 선택 항목을 확인하고
    nearest(y) 메소드를 활용하여 실행되어있는 listbox 창 안에서 
    사용자 선택 항목에 가까운 인덱스를 반환받음'''
    item = listbox.curselection()
    gety = listbox.nearest(item[0])
    print(gety)


# 클릭시 pick()메소드를 호출하는 버튼 생성
btn = tkinter.Button(window, text="항목선택", command=pick)

# 리스트박스를 윈도우의 상단에, 버튼을 하단에 배치
listbox.pack(side="top")
btn.pack(side="bottom")
window.mainloop()

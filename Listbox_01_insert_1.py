import tkinter

# Listbox가 들어갈 윈도우 객체 생성
window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x150")

# Listbox 객체 생성, 변수명 listbox, window 내에 생성, 나머지 속성은 기본값
listbox = tkinter.Listbox(window)

# insert(index, "항목")메소드 활용하여 항목 추가
# index는 0부터 시작
listbox.insert(0, "item1")
listbox.insert(1, "item2")
listbox.insert(2, "item3")
listbox.insert(3, "item4")
listbox.insert(4, "item5")

# Listbox를 실제 window 내에 작성
listbox.pack()
window.mainloop()

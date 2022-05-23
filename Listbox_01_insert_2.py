import tkinter

# Listbox가 들어갈 윈도우 객체 생성
window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x150")

# Listbox 객체 생성, 변수명 listbox, window 내에 생성, 나머지 속성은 기본값
listbox = tkinter.Listbox(window)

# insert(index, "항목")메소드 활용하여 항목 추가
# index가 음수면 실제 값과 상관없이 무조건 index 0 위치에 항목 추가
listbox.insert(0, "item1")
listbox.insert(1, "item2")
listbox.insert(-1, "item3")
listbox.insert(-1, "item4")
listbox.insert(-2, "item5")

# Listbox를 실제 window 내에 작성
listbox.pack()
window.mainloop()

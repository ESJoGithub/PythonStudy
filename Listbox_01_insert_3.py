import tkinter

# Listbox가 들어갈 윈도우 객체 생성
window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x150")

# Listbox 객체 생성, 변수명 listbox, window 내에 생성, 나머지 속성은 기본값
listbox = tkinter.Listbox(window)

# insert(index, "항목")메소드 활용하여 항목 추가
# tkinter.END 활용, <from tkinter import *> 시 <tkinter.> 없이 <END> 사용 가능
listbox.insert(tkinter.END, "item1")
listbox.insert(tkinter.END, "item2")
listbox.insert(tkinter.END, "item3")
listbox.insert(tkinter.END, "item4")
listbox.insert(tkinter.END, "item5")

# Listbox를 실제 window 내에 작성
listbox.pack()
window.mainloop()

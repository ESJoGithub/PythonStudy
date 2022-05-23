import tkinter

# 여러 아이템을 가진 객체 생성
items = []
for i in range(30):
    items.append("item{}".format(i))

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x200")

# 여러 문자열을 가진 StringVar 객체 생성, 변수명 var
var = tkinter.StringVar()
# StringVar의 객체인 var의 값을 items로 연결
var.set(items)
# 리스트박스에 표시할 문자열을 var로부터 받아옴
listbox = tkinter.Listbox(window, listvariable=var)

listbox.pack()
window.mainloop()

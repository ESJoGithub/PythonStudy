import tkinter

items = []
for i in range(30):
    items.append("item{}".format(i))

window = tkinter.Tk()
window.title("Listbox")

var = tkinter.StringVar()
var.set(items)

listbox1 = tkinter.Listbox(window, listvariable=var, selectmode="single")
listbox2 = tkinter.Listbox(window, listvariable=var, selectmode="single")
listbox3 = tkinter.Listbox(window, listvariable=var, selectmode="single")

listbox1.config(activestyle="dotbox")
listbox2.config(activestyle="underline")  # 기본설정
listbox3.config(activestyle="none")

listbox1.pack(side="left")
listbox2.pack(side="left")
listbox3.pack(side="left")
window.mainloop()

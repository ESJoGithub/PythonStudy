import tkinter

items = []
for i in range(30):
    items.append("item{}".format(i))

window = tkinter.Tk()
window.title("Listbox")

var = tkinter.StringVar()
var.set(items)

listbox1 = tkinter.Listbox(window, listvariable=var)
listbox2 = tkinter.Listbox(window, listvariable=var)
listbox3 = tkinter.Listbox(window, listvariable=var)
listbox4 = tkinter.Listbox(window, listvariable=var)

listbox1.config(selectmode="browse")
listbox2.config(selectmode="single")
listbox3.config(selectmode="multiple")
listbox4.config(selectmode="extended")

listbox1.pack(side="left")
listbox2.pack(side="left")
listbox3.pack(side="left")
listbox4.pack(side="left")
window.mainloop()

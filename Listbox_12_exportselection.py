import tkinter

window = tkinter.Tk()
window.title("List_scroll")


frame1 = tkinter.Frame(window)
frame2 = tkinter.Frame(window)
frame1.pack(side="left", padx=15)
frame2.pack(side="left")

# exportselection을 활용하여 리스트 간 항목 선택 유지
listbox1 = tkinter.Listbox(frame1, width=40, exportselection=False)
listbox2 = tkinter.Listbox(frame2, width=40, exportselection=False)


for i in range(1, 32):
    listbox2.insert(tkinter.END, "{}일".format(str(i)))
    if i < 13:
        listbox1.insert(tkinter.END, "{}월".format(str(i)))


scroll1 = tkinter.Scrollbar(frame1, command=listbox1.yview)
scroll1.pack(side="right", fill="y")
scroll2 = tkinter.Scrollbar(frame2, command=listbox2.yview)
scroll2.pack(side="right", fill="y")

listbox1.config(yscrollcommand=scroll1.set)
listbox2.config(yscrollcommand=scroll2.set)

listbox1.pack()
listbox2.pack()
window.mainloop()

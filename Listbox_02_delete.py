import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x150")

listbox = tkinter.Listbox(window)

listbox.insert(tkinter.END, "item1")
listbox.insert(tkinter.END, "item2")
listbox.insert(tkinter.END, "item3")
listbox.insert(tkinter.END, "item4")
listbox.insert(tkinter.END, "item5")

# delete(start_index, end_index=None) 메소드 활용하여 항목 제거
listbox.delete(0, tkinter.END)

listbox.pack()
window.mainloop()

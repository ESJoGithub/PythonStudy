import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x250")

listbox = tkinter.Listbox(window)
listbox.config(
    highlightcolor="blue",
    highlightbackground="#fffaaa",
    highlightthickness=5
)

# for문을 활용하여 "item0"부터 "item29"까지 총 30개 아이템 생성
for i in range(30):
    listbox.insert(tkinter.END, "item{}".format(str(i)))

listbox.pack()
window.mainloop()

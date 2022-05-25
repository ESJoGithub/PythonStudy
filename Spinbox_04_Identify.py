import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x50")

spinbox = tkinter.Spinbox(window, width=20)
spinbox.insert(0, "가다라마바사")
spinbox.insert(1, "나")
spinbox.insert(tkinter.END, "아")


def get_position():
    str = spinbox.identify(150, 10)
    print(str)


btn = tkinter.Button(window, text="식별", command=get_position)

spinbox.pack()
btn.pack(side="bottom")
window.mainloop()

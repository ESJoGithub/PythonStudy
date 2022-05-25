import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x50")

spinbox = tkinter.Spinbox(window)
spinbox.insert(0, "가다라마바사")
spinbox.insert(1, "나")
spinbox.insert(tkinter.END, "아")


def get_str():
    temp_str = spinbox.get()
    print(temp_str)


btn = tkinter.Button(window, text="반환", command=get_str)

spinbox.pack()
btn.pack(side="bottom")
window.mainloop()

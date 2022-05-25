import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x50")

var = tkinter.IntVar()
var.set(100)

spinbox = tkinter.Spinbox(window)
spinbox.config(
    from_=1, to=100,
    increment=2,
    textvariable=var,
    wrap=True,
    font="colas 20"
)

spinbox.pack(pady=5, padx=5)
window.mainloop()

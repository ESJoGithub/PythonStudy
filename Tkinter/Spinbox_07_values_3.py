import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x50")

tempstr = []
for i in range(100):
    _str = "item"+str(i)
    tempstr.append(_str)

spinbox = tkinter.Spinbox(window)
spinbox.config(
    values=tempstr
)
spinbox.pack()
window.mainloop()

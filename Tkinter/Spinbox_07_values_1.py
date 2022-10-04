import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x50")

spinbox = tkinter.Spinbox(window)
spinbox.config(
    from_=1, to=100,
    increment=0.5,
    format_="%3.4f",
    repeatdelay=3000,
    # repeatinterval=1000
)

spinbox.pack()
window.mainloop()

import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x200")

spinbox = tkinter.Spinbox(
    window,
    from_=0, to=50,
    width=30,
    relief="solid",
    bd=2,
    bg="aliceblue",
    fg="blue",
    insertwidth=5,
    insertborderwidth=1,
    insertbackground="green"
)

spinbox.pack()
window.mainloop()

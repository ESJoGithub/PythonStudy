import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x200")

spinbox = tkinter.Spinbox(
    window,
    selectborderwidth=2,
    selectbackground="black",
    selectforeground="white",
    buttonbackground="gray"
)

spinbox.pack()
window.mainloop()

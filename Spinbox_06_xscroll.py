import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x100")

frame = tkinter.Frame(window)
frame.pack()

spinbox = tkinter.Spinbox(frame)
spinbox.insert(0, "가나다라마바사아자차카타파하abcdefghijklmn0123456789")

scroll_spin = tkinter.Scrollbar(
    frame, orient="horizontal", command=spinbox.xview)
scroll_spin.pack(side="bottom", fill="x")

spinbox.config(width=20, xscrollcommand=scroll_spin.set)

spinbox.pack()
window.mainloop()

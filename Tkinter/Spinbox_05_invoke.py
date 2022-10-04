import tkinter

window = tkinter.Tk()
window.title("Spinbox")
window.geometry("300x100")

spinbox = tkinter.Spinbox(window)
spinbox.config(from_=1, to=100)


def up():
    spinbox.invoke("buttonup")


def down():
    spinbox.invoke("buttondown")


btn_up = tkinter.Button(text="버튼up", command=up, width=20)
btn_down = tkinter.Button(text="버튼down", command=down, width=20)

spinbox.pack(side="top")
btn_down.pack(side="bottom")
btn_up.pack(side="bottom")

window.mainloop()

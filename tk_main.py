import tkinter as tk
from tk_menu import menubar

window = tk.Tk()
window.title("Mini_Photoshop")
window.geometry("1200x850+50+50")

menu = menubar(window)
menu.run_menu()

window.mainloop()
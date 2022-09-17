import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Sizegrip
from tk_menu import menubar

window = tk.Tk()
window.title("Mini_Photoshop")
window.geometry("1200x800+50+50")

menu = menubar(window)
menu.run_menu()

window.mainloop()
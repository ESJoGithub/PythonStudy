import tkinter as tk
from menu import menubar

from tkinter import Canvas, filedialog
from frame import Get_Frame
import cv2
from PIL import Image, ImageTk
import numpy as np

window = tk.Tk()
window.title("Mini_Photoshop")
window.geometry("1024x768+50+50")

menu = menubar(window)
menu.run_menu()

'''frame = tk.Frame(window)
frame.pack()
frame2 = tk.Frame(frame)
frame2.pack()
path = "C:\\Users\\user\\desktop"
_filename = filedialog.askopenfilename(initialdir=path, title="열기", 
                                      filetypes=(("모든 파일", "*.*"),
                                                ("모든 그림 파일", "*.jpg;*.jpeg;*.btm;*.png;*.tif;*.gif"), 
                                                ("JPG", "*.jpg;*.jpeg"),
                                                ("비트맵 파일", "*.btm"),
                                                ("PNG", "*.png"),
                                                ("TIF", "*.tif"),
                                                ("GIF", "*.gif")))
src = cv2.imread(_filename)
src = cv2.resize(src, dsize = (1000, 500))
tk_img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)
photo = Image.fromarray(tk_img)
canvas = tk.Canvas(frame2)
canvas.pack()
photo = ImageTk.PhotoImage(image=photo, master=canvas)
canvas.configure(width=1000, height=500, relief="raised", bg="white")
temp_width= 1000//2
temp_height= 500//2
canvas.create_image(temp_width, temp_height, image=photo)'''

window.mainloop()
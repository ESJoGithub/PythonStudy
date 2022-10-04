import tkinter

window = tkinter.Tk()
window.title("Listbox")
window.geometry("300x150")

listbox = tkinter.Listbox(window)

listbox.insert(tkinter.END, "item1")
listbox.insert(tkinter.END, "item2")
listbox.insert(tkinter.END, "item3")
listbox.insert(tkinter.END, "item4")
listbox.insert(tkinter.END, "item5")

# size() 활용하여 항목 개수 확인
nums = listbox.size()
print("listbox의 아이템은 총 {}개입니다.".format(nums))

# get(start_index, end_index=None)을 활용하여 항목 반환
items = listbox.get(1, 3)
print("범위에 해당하는 항목은{} 입니다.".format(items))

listbox.pack()
window.mainloop()

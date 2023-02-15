from tkinter import *
import src

window = Tk()
window.title("Заметки")
window.geometry("550x350")

f_display = Frame(window)
f_display.pack(anchor=N)

f_keys = Frame(window)
f_keys.pack(anchor=S)

display = src.Display(f_display)
keys = src.Keys( f_keys, display)

window.mainloop()
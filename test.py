import tkinter as tk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk()

text = ScrolledText(root, width=20, height=10)
text.pack()

for i in range(30):
    cb = tk.Checkbutton(text, text=(i + 1), bg="white", anchor="w")
    text.window_create("end", window=cb)
    text.insert("end", "\n")

root.mainloop()

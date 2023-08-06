# 基础示例1
import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.FluentDark()

button = tktelerik.Button(text="button1")
button.configure(theme="FluentDark")
button.pack(fill="both", expand="yes", padx=5, pady=5)

root.mainloop()
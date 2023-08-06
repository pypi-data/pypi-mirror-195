# 基础示例1
import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.Windows11()

calc1 = tktelerik.Calculator()
calc1.configure(theme="Windows11")
calc1.pack(fill="both", expand="yes", padx=4, pady=4)

root.mainloop()
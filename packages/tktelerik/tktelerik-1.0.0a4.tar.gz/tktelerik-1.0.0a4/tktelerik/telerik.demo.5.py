import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.Windows11()

nav1 = tktelerik.NavigationView()
nav1.configure(theme="Windows11")

page1 = tktelerik.PageViewPage()
page1.configure(text="page1")

button1 = tktelerik.Button(page1.frame())
button1.configure(theme="Windows11")
button1.pack(fill="both")

nav1.add_page(page1)
nav1.pack(fill="both", expand="yes", padx=4, pady=4)

root.mainloop()
import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.Windows11()

nav = tktelerik.NavigationView()
nav.configure(theme="Windows11")

controls = tktelerik.PageViewPage(nav=nav)
controls.configure(text="controls")

button1 = tktelerik.Button(controls.frame())
button1.configure(theme="Windows11", text_anchor_ment="w")
button1.pack(fill="x", padx=10, pady=10)

textbox1 = tktelerik.TextBox(controls.frame())
textbox1.configure(theme="Windows11")
textbox1.pack(fill="x", padx=10, pady=10)

textbox2 = tktelerik.TextBox(controls.frame())
textbox2.configure(multiline=True, theme="Windows11")
textbox2.pack(fill="both", ipady=50, padx=10, pady=10)

nav.add_page(controls)
nav.pack(fill="both", expand="yes")

root.mainloop()

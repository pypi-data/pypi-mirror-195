import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.FluentDark()

qrcode1 = tktelerik.BarcodeView()
qrcode1.configure(theme="FluentDark")
qrcode1.pack(fill="both", expand="yes", padx=5, pady=5)

root.mainloop()
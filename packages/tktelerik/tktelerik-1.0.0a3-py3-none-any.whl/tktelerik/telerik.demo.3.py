import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.FluentDark()

ribbon = tktelerik.RibbonBar()
ribbon_quick_item = tktelerik.RibbonButton()
ribbon_quick_item.onclick(lambda: print("click ribbon_quick_button"))
ribbon.add_item(ribbon_quick_item)

ribbon_tab = tktelerik.RibbonTabbed()

ribbon_group = tktelerik.RibbonGroup()

ribbon_button = tktelerik.RibbonButton()
ribbon_button.onclick(lambda: print("click ribbon_button"))
ribbon_button.configure(anchor="w")
ribbon_textbox = tktelerik.RibbonTextBox()
ribbon_textbox.configure(anchor="w")

ribbon_group.add(ribbon_button)
ribbon_group.add(ribbon_textbox)

ribbon_tab.add(ribbon_group)
ribbon.add(ribbon_tab)

ribbon.configure(theme="FluentDark")
ribbon.pack(fill="both", expand="yes", padx=5, pady=5)

root.mainloop()
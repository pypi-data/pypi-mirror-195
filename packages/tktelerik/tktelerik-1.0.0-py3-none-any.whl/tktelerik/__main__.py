import tktelerik
from tkinter import Tk

root = Tk()
theme1 = tktelerik.Windows11()

nav = tktelerik.PageView()
nav.configure(theme="Windows11", view="strip")

# -----------------------------------------------------------
controls = tktelerik.PageViewPage(nav=nav)
controls.configure(text="Controls")

button1 = tktelerik.Button(controls.frame())
button1.configure(theme="Windows11", text_anchor_ment="w")
button1.pack(fill="x", padx=10, pady=10)

checkbox1 = tktelerik.CheckBox(controls.frame())
checkbox1.configure(theme="Windows11")
checkbox1.pack(fill="x", padx=10, pady=10)

radiobutton1 = tktelerik.RadioButton(controls.frame())
radiobutton1.configure(theme="Windows11")
radiobutton1.pack(fill="x", padx=10, pady=10)

progress1 = tktelerik.ProgressBar(controls.frame())
progress1.configure(theme="Windows11", value1=50)
progress1.pack(fill="x", padx=10, pady=10)

textbox1 = tktelerik.TextBox(controls.frame())
textbox1.configure(theme="Windows11")
textbox1.pack(fill="x", padx=10, pady=10)

textbox2 = tktelerik.TextBox(controls.frame())
textbox2.configure(multiline=True, theme="Windows11")
textbox2.pack(fill="x", ipady=50, padx=10, pady=10)

textbox3 = tktelerik.CalculatorDropDown(controls.frame())
textbox3.configure(theme="Windows11")
textbox3.pack(fill="x", padx=10, pady=10)

syntax1 = tktelerik.SyntaxEditor(controls.frame())
syntax1.configure(theme="Windows11")
syntax1.pack(fill="both", expand=True, ipady=50, padx=10, pady=10)
# -----------------------------------------------------------
# -----------------------------------------------------------
layouts = tktelerik.PageViewPage(nav=nav)
layouts.configure(text="Layouts")

menubar = tktelerik.MenuBar(layouts.frame())
menubar.configure(theme="Windows11")

menufile = tktelerik.MenuItem("File")
menufile.add(tktelerik.MenuItem("Open..."))
menufile.add(tktelerik.MenuItem("Open As..."))

menuedit = tktelerik.MenuItem("Edit")
menuedit.add(tktelerik.MenuItem("Undo"))
menuedit.add(tktelerik.MenuItem("Redo"))

menubar.add(menufile)
menubar.add(menuedit)
menubar.pack(fill="x", side="top")

statusbar = tktelerik.StatusBar(layouts.frame())
statusbar.configure(theme="Windows11", sizegrip=False)
label_element1 = tktelerik.LabelElement()
button_element1 = tktelerik.ButtonElement()
button_element1.configure(text_anchor_ment="nw")
statusbar.add(label_element1)
statusbar.add(button_element1)
statusbar.pack(fill="x", side="bottom")
# -----------------------------------------------------------
ribbon = tktelerik.PageViewPage(nav=nav)
ribbon.configure(text="Ribbon")

ribbonbar = tktelerik.RibbonBar(ribbon.frame(), text="RibbonBar")
ribbon_quick_item = tktelerik.ButtonElement(text="QuickButton")
ribbon_quick_item.onclick(lambda: print("click ribbon_quick_button"))
ribbonbar.add_item(ribbon_quick_item)

ribbon_tab = tktelerik.RibbonTabbed(text="Home")

ribbon_group = tktelerik.RibbonGroup()

ribbon_button = tktelerik.ButtonElement(text="Button")
ribbon_button.onclick(lambda: print("click ribbon_button"))
ribbon_button.configure(anchor="w")
ribbon_textbox = tktelerik.TextBoxElement(text="TextBox")
ribbon_textbox.configure(anchor="w")

ribbon_group.add(ribbon_button)
ribbon_group.add(ribbon_textbox)

ribbon_tab.add(ribbon_group)
ribbonbar.add(ribbon_tab)

ribbonbar.configure(theme="Windows11")
ribbonbar.pack(fill="both", expand="yes", padx=5, pady=5)
# -----------------------------------------------------------
nav.add_page(controls)
nav.add_page(layouts)
nav.add_page(ribbon)
nav.pack(fill="both", expand="yes")

root.mainloop()

import clr
from tktelerik import (telerik_wincontrols_lib, telerik_wincontrols_ui_lib, telerik_wincontrols_themes_win11_lib,
                       telerik_wincontrols_themes_fluent_lib, telerik_wincontrols_themes_fluent_dark_lib)
clr.AddReference(telerik_wincontrols_lib)
clr.AddReference(telerik_wincontrols_ui_lib)
clr.AddReference(telerik_wincontrols_themes_win11_lib)
clr.AddReference(telerik_wincontrols_themes_fluent_lib)
clr.AddReference(telerik_wincontrols_themes_fluent_dark_lib)

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from Telerik.WinControls.UI import (RadButton, RadLabel, RadTitleBar, RadListControl, RadListDataItem)
from Telerik.WinControls.Themes import (Windows11Theme, FluentTheme, FluentDarkTheme)
from System.Drawing import Point, Size, ContentAlignment
from System.Windows.Forms import CheckState
from tktelerik.base import Widget


class Base(Widget):
    def configure(self, **kwargs):
        if "theme" in kwargs:
            self._widget.ThemeName = kwargs.pop("theme")
        super().configure(**kwargs)


class Windows11(object):
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = Windows11Theme()


class Fluent(object):
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = FluentTheme()


class FluentDark(object):
    def __init__(self):
        self._init_widget()

    def _init_widget(self):
        self._widget = FluentDarkTheme()


class Button(Base):
    def __init__(self, *args, width=100, height=30, text="Telerik.WinControls.Button", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadButton()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class Label(Base):
    def __init__(self, *args, width=100, height=30, text="Telerik.WinControls.Label", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadLabel()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


class ListBox(Base):
    def __init__(self, *args, width=100, height=30, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = RadListControl()

    def create_label(self, text=""):
        _list = RadListDataItem()
        _list.Text = text
        return _list

    def add(self, list):
        self._widget.Items.Add(list)


class TitleBar(Base):
    def __init__(self, *args, width=100, height=30, text="Telerik.WinControls.TitleBar", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadTitleBar()


class Entry(Widget):
    def __init__(self, *args, width=100, height=30, text="DevExpress.Xtra.Entry", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = TextEdit()

    def configure(self, **kwargs):
        if "multiline" in kwargs:
            self._widget.Multiline = kwargs.pop("multiline")
        elif "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "multiline":
            return self._widget.Multiline
        elif attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)


if __name__ == '__main__':
    from tkinter import Tk, Frame

    root = Tk()
    root.configure(background="#f0f0f0")

    win11_theme = Windows11()
    fluent_theme = Fluent()
    fluent_dark_theme = FluentDark()

    button1 = Button(text="button1")
    button1.configure(theme="Windows11")
    button1.pack(fill="both", expand="yes", padx=4, pady=4)

    label1 = Label(text="label1")
    label1.configure(theme="Windows11")
    label1.pack(fill="both", expand="yes", padx=4, pady=4)

    listbox1 = ListBox()
    listbox1.configure(theme="Windows11")

    listbox1.add(listbox1.create_label("list1"))
    listbox1.add(listbox1.create_label("list2"))
    listbox1.add(listbox1.create_label("list3"))


    listbox1.pack(fill="both", expand="yes", padx=4, pady=4)

    root.mainloop()
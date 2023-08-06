import clr
from tktelerik import *
clr.AddReference(telerik_wincontrols_lib)
clr.AddReference(telerik_wincontrols_ui_lib)
clr.AddReference(telerik_wincontrols_themes_win11_lib)
clr.AddReference(telerik_wincontrols_themes_fluent_lib)
clr.AddReference(telerik_wincontrols_themes_fluent_dark_lib)
clr.AddReference(telerik_wincontrols_diagram_lib)

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from Telerik.WinControls.UI import (RadButton, RadLabel, RadTitleBar, RadListControl, RadListDataItem, RadCalculator,
                                    RadSplitButton, RadDirection, RadChat, RadDiagramRibbonBar, RibbonTab,
                                    RadRibbonBarGroup, RadButtonElement, RadButtonElement, RadTextBoxElement,
                                    RadTextBox, RadNavigationView, RadPageViewPage)
from Telerik.WinControls.UI import (RadMenuItem)
from Telerik.WinControls.UI.Barcode import RadBarcodeView, QRCode
from Telerik.WinControls.Themes import (Windows11Theme, FluentTheme, FluentDarkTheme)
from System.Drawing import Point, Size, ContentAlignment
from System.Windows.Forms import CheckState
from tktelerik.base import Widget


class Base(Widget):
    def configure(self, **kwargs):
        if "theme" in kwargs:
            self._widget.ThemeName = kwargs.pop("theme").title()
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


class BarcodeView(Base):
    def __init__(self, *args, width=100, height=30, value="Telerik.WinControls.BarcodeView", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(value=value)

    def _init_widget(self):
        self._widget = RadBarcodeView()
        self._qr = QRCode()
        self._qr.Version = 1
        self._widget.Symbology = self._qr

    def configure(self, **kwargs):
        if "value" in kwargs:
            self._widget.Value = kwargs.pop("value")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "value":
            return self._widget.Value
        else:
            return super().cget(attribute_name)


class PageViewPage(Base):
    def __init__(self, *args, width=500, height=200, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = RadPageViewPage()
        from tkinter import Frame
        self._page_frame = Frame()
        self.forms_tk(self._widget, self._page_frame)

        def resize(_1, _2):
            self._page_frame.place(x=self._widget.Location.X+3, y=self._widget.Location.Y+3, width=self._widget.Size.Width, height=self._widget.Size.Height)

        self._widget.Resize += resize

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)

    def frame(self):
        return self._page_frame

class NavigationView(Base):
    def __init__(self, *args, width=600, height=300, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = RadNavigationView()

    def add_page(self, page: PageViewPage):
        self._widget.Controls.Add(page.widget())


class MenuItem(object):
    def __init__(self, text="Telerik.WinControls.MenuItem"):
        self._init_widget()
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadMenuItem()

    def widget(self):
        return self._widget

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")

    def add(self, item):
        self._widget.Items.AddRange(item.widget())


class SplitButton(Button):
    def _init_widget(self):
        self._widget = RadSplitButton()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        elif "direction" in kwargs:
            direction = kwargs.pop("direction")
            if direction == "up":
                self._widget.DropDownDirection = RadDirection.Up
            elif direction == "down":
                self._widget.DropDownDirection = RadDirection.Down
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text
        else:
            return super().cget(attribute_name)

    def add(self, item: MenuItem):
        self._widget.Items.AddRange(item.widget())

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


class Calculator(Base):
    def __init__(self, *args, width=220, height=360, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = RadCalculator()


class Chat(Base):
    def __init__(self, *args, width=220, height=360, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

    def _init_widget(self):
        self._widget = RadChat()


class RibbonElement(object):
    def __init__(self):
        self._init_widget()

    def onclick(self, func):
        self._widget.Click += lambda _1, _2: func()

    def ondown(self, func):
        self._widget.MouseDown += lambda _1, _2: func()

    def onup(self, func):
        self._widget.MouseUp += lambda _1, _2: func()

    def _init_widget(self):
        pass

    def widget(self):
        return self._widget

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        elif "anchor" in kwargs:
            anchor = kwargs.pop("anchor")
            from System.Drawing import ContentAlignment
            if anchor == "center":
                self._widget.Alignment = ContentAlignment.MiddleCenter
            elif anchor == "w":
                self._widget.Alignment = ContentAlignment.MiddleLeft
            elif anchor == "e":
                self._widget.Alignment = ContentAlignment.MiddleRight
            elif anchor == "n":
                self._widget.Alignment = ContentAlignment.MiddleTop
            elif anchor == "s":
                self._widget.Alignment = ContentAlignment.MiddleBottom
            elif anchor == "nw":
                self._widget.Alignment = ContentAlignment.TopLeft

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text


class RibbonButton(RibbonElement):
    def __init__(self, text="Telerik.WinControls.RibbonButton"):
        super().__init__()
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadButtonElement()


class RibbonTextBox(RibbonElement):
    def __init__(self, text="Telerik.WinControls.RibbonTextBox"):
        super().__init__()
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadTextBoxElement()


class RibbonGroup(object):
    def __init__(self):
        self._init_widget()

    def widget(self):
        return self._widget

    def _init_widget(self):
        self._widget = RadRibbonBarGroup()

    def add(self, item: RibbonButton):
        self._widget.Items.AddRange(item.widget())

    def remove(self, item: RibbonButton):
        self._widget.Items.Remove(item.widget())

    def clear(self):
        self._widget.Items.Clear()

class RibbonTabbed(object):
    def __init__(self, text="Telerik.WinControls.RibbonTabbed"):
        self._init_widget()
        self.configure(text=text)

    def widget(self):
        return self._widget

    def _init_widget(self):
        self._widget = RibbonTab()

    def add(self, item: RibbonGroup):
        self._widget.Items.AddRange(item.widget())

    def remove(self, item: RibbonGroup):
        self._widget.Items.Remove(item.widget())

    def clear(self):
        self._widget.Items.Clear()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text


class RibbonBar(Base):
    def __init__(self, *args, width=220, height=360, text="Telerik.WinControls.RibbonBar", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadDiagramRibbonBar()
        self._widget.CloseButton = False
        self._widget.MaximizeButton = False
        self._widget.MinimizeButton = False
        self.clear()

    def add(self, item: RibbonTabbed):
        self._widget.CommandTabs.AddRange(item.widget())

    def add_item(self, item):
        self._widget.QuickAccessToolBarItems.AddRange(item.widget())

    def remove(self, item: RibbonTabbed):
        self._widget.CommandTabs.Remove(item.widget())

    def clear(self):
        self._widget.CommandTabs.Clear()

    def configure(self, **kwargs):
        if "text" in kwargs:
            self._widget.Text = kwargs.pop("text")

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "text":
            return self._widget.Text


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


class TextBox(Base):
    def __init__(self, *args, width=100, height=30, text="Telerik.WinControls.TextBox", **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.configure(text=text)

    def _init_widget(self):
        self._widget = RadTextBox()

    def configure(self, **kwargs):
        if "multiline" in kwargs:
            self._widget.Multiline = kwargs.pop("multiline")
        elif "text" in kwargs:
            self._widget.Text = kwargs.pop("text")
        elif "tip_text" in kwargs:
            self._widget.NullText = kwargs.pop("tip_text")
        super().configure(**kwargs)

    def cget(self, attribute_name: str) -> any:
        if attribute_name == "multiline":
            return self._widget.Multiline
        elif attribute_name == "text":
            return self._widget.Text
        elif attribute_name == "tip_text":
            return self._widget.NullText
        else:
            return super().cget(attribute_name)


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
    # 高级示例1
    from tkinter import Tk

    root = Tk()
    theme1 = Windows11()

    ribbon = RibbonBar()
    ribbon_quick_item = RibbonButton()
    ribbon_quick_item.onclick(lambda: print("click ribbon_quick_button"))
    ribbon.add_item(ribbon_quick_item)

    ribbon_tab = RibbonTabbed()

    ribbon_group = RibbonGroup()

    ribbon_button = RibbonButton()
    ribbon_button.onclick(lambda: print("click ribbon_button"))
    ribbon_button.configure(anchor="w")
    ribbon_textbox = RibbonTextBox()
    ribbon_textbox.configure(anchor="w")

    ribbon_group.add(ribbon_button)
    ribbon_group.add(ribbon_textbox)

    ribbon_tab.add(ribbon_group)
    ribbon.add(ribbon_tab)

    ribbon.configure(theme="Windows11")
    ribbon.pack(fill="both", expand="yes", padx=5, pady=5)

    root.mainloop()
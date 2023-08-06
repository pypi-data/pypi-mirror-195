import os
lib = os.path.dirname(__file__).replace("\\", "//")
telerik_wincontrols_lib = lib + "//Telerik.WinControls.dll"
telerik_wincontrols_ui_lib = lib + "//Telerik.WinControls.UI.dll"
telerik_wincontrols_diagram_lib = lib + "//Telerik.WinControls.RadDiagram.dll"
telerik_wincontrols_syntax_editor_lib = lib + "//Telerik.WinControls.SyntaxEditor.dll"
telerik_wincontrols_themes_win11_lib = lib + "//Telerik.WinControls.Themes.Windows11.dll"
telerik_wincontrols_themes_material_lib = lib + "//Telerik.WinControls.Themes.Material.dll"
telerik_wincontrols_themes_fluent_lib = lib + "//Telerik.WinControls.Themes.Fluent.dll"
telerik_wincontrols_themes_fluent_dark_lib = lib + "//Telerik.WinControls.Themes.FluentDark.dll"


from tktelerik.telerik import *
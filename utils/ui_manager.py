from CTkMessagebox import CTkMessagebox
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass
    from ui.new_window import NewWindow as NewWindowClass


def w_close(Window: Union["MainWindowClass", "NewWindowClass"], MainWindow: "MainWindowClass"):
    MainWindow.all_children.remove(Window)
    Window.destroy()


def w_new_file(MainWindow: "MainWindowClass", binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    from ui.new_window import NewWindow
    NewWindow(MainWindow, MainWindow.resource_path)


def w_show_soon():
    CTkMessagebox(title="xzyNotepad", message="This option will be soon.", icon="info")


def w_show_font_families(MainWindow: "MainWindowClass"):
    from ui.font_families_window import FontsWindow
    for window in MainWindow.all_children:
        if window.title() in ["Font Families"]:
            return
    FontsWindow(MainWindow, MainWindow.resource_path)


def w_show_preferences(MainWindow: "MainWindowClass", binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    from ui.preferences_window import PreferencesWindow
    for window in MainWindow.all_children:
        if window.title() in ["Preferences"]:
            return
    PreferencesWindow(MainWindow, MainWindow.resource_path)


def w_show_about(MainWindow: "MainWindowClass"):
    from ui.about_window import AboutWindow
    for window in MainWindow.all_children:
        if window.title() in ["About"]:
            return
    AboutWindow(MainWindow, MainWindow.resource_path)


def w_show_ai_assistant(MainWindow: "MainWindowClass", message=None, chats=None):
    from ui.assistant_window import AssistantChatApp
    for window in MainWindow.all_children:
        if window.title() in ["AI Chat"]:
            return
    AssistantChatApp(MainWindow, MainWindow.resource_path, message, chats)

__all__ = ["w_close", "w_new_file", "w_show_soon", "w_show_font_families",
           "w_show_preferences", "w_show_about", "w_show_ai_assistant"]

import customtkinter as ctk
import os
import json
from CTkCodeBox import CTkCodeBox
from utils.variables import DEFAULT_SETTINGS
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def s_apply(MainWindow: "MainWindowClass"):
    ctk.set_appearance_mode(MainWindow.settings['theme'])
    ctk.set_default_color_theme(MainWindow.resource_path(f'assets/themes/'
                                                         f'{MainWindow.settings["main_theme"].lower()}.json'))
    for window in MainWindow.all_children + [MainWindow]:
        for widget in window.winfo_children():
            if isinstance(widget, CTkCodeBox):
                widget.configure(font=ctk.CTkFont(MainWindow.settings['font_family'], MainWindow.settings['font_size']))
                widget.configure(theme=MainWindow.settings['codebox_theme'].lower())


def s_add_new(settings):
    for key in list(DEFAULT_SETTINGS.keys()):
        if key not in list(settings.keys()):
            settings[key] = DEFAULT_SETTINGS[key]
    for key in list(settings.keys()):
        if key not in list(DEFAULT_SETTINGS.keys()):
            settings[key] = None
    return settings


def s_save(MainWindow: "MainWindowClass", file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as f:
        json.dump(MainWindow.settings, f, indent=4)
        f.close()


def s_load(MainWindow: "MainWindowClass", file, auto_load=False, set_vars=False):
    if os.path.exists(file):
        with open(file, 'r') as f:
            data = s_add_new(json.load(f))
            if (auto_load is True and data['auto_load'] == "Enabled") or (auto_load is False):
                MainWindow.settings = data
                if set_vars is True:
                    for window in MainWindow.all_children:
                        if window.title() in ["Preferences"]:
                            window.set_vars()
                s_apply(MainWindow)
            f.close()
    else:
        s_apply(MainWindow)


def s_previous_load(MainWindow: "MainWindowClass"):
    if os.path.exists(MainWindow.previous_settings_file):
        with open(MainWindow.previous_settings_file, 'r') as f:
            data = s_add_new(json.load(f))
            f.close()
            return data
    else:
        return None

__all__ = ["s_save", "s_load", "s_previous_load"]

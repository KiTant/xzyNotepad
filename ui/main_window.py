import customtkinter as ctk
from ui.new_window import NewWindow
from ui.preferences_window import PreferencesWindow
from ui.about_window import AboutWindow
from ui.font_families_window import FontsWindow
from CTkCodeBox import CTkCodeBox
from utils.helpers import show_messagebox, code_window_binder, close_code_window, save_file
from utils.variables import LANGUAGES, DEFAULT_SETTINGS
from ui.title_menu import TitleMenu
import json
import os


class MainWindow(ctk.CTk):
    def __init__(self, resource_path, settings_file, previous_settings_file):
        super().__init__()
        self.current_language = "txt"
        self.title(f"xzyNotepad - New File.{self.current_language}")
        self.geometry("1000x500")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        self.resource_path = resource_path
        self.disable_updating_code = False
        self.file_name = f"New File.{self.current_language}"
        self.full_file_path = None
        self.updating = False
        self.saved = True
        self.all_children = []
        self.settings_file = settings_file
        self.previous_settings_file = previous_settings_file
        self.settings = DEFAULT_SETTINGS
        self.previous_settings = self.load_previous_settings()

        self.load_settings(self.settings_file, True)

        self._initialize_components()

    def _initialize_components(self):
        self.codebox = CTkCodeBox(self, language=LANGUAGES[self.current_language], height=500, theme=self.settings['codebox_theme'].lower(),
                                  font=ctk.CTkFont(family=self.settings['font_family'], size=self.settings['font_size']))
        self.codebox.pack(fill="both", expand=True)
        code_window_binder(self, self)

        self.menu = TitleMenu(self, self)

        self.protocol("WM_DELETE_WINDOW", lambda: close_code_window(self, self.all_children))

        self.after(self.settings["auto_save_file_time"] * 60000, lambda: save_file(self, self, self.full_file_path, True))

    def new_file(self, binded: bool = False):
        if self.settings['keybinds'] == "Disabled" and binded is True:
            return
        NewWindow(self, self.resource_path)

    def show_soon(self): show_messagebox(title="xzyNotepad", message="This option will be soon.", icon="info")

    def show_font_families(self):
        for window in self.all_children:
            if window.title() in ["Font Families"]:
                return
        FontsWindow(self, self.resource_path)

    def show_preferences(self, binded: bool = False):
        if self.settings['keybinds'] == "Disabled" and binded is True:
            return
        for window in self.all_children:
            if window.title() in ["Preferences"]:
                return
        PreferencesWindow(self, self.resource_path)

    def show_about(self):
        for window in self.all_children:
            if window.title() in ["About"]:
                return
        AboutWindow(self, self.resource_path)

    def save_settings(self, file):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w') as f:
            json.dump(self.settings, f, indent=4)

    def load_settings(self, file, auto_load=False, set_vars=False):
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                if (auto_load is True and data['auto_load'] == "Enabled") or (auto_load is False):
                    self.settings = data
                    if set_vars is True:
                        for window in self.all_children:
                            if window.title() in ["Preferences"]:
                                window.set_vars()
                    ctk.set_appearance_mode(self.settings['theme'])
                    for window in self.all_children + [self]:
                        for widget in window.winfo_children():
                            if isinstance(widget, CTkCodeBox):
                                widget.configure(font=ctk.CTkFont(self.settings['font_family'], self.settings['font_size']))
                                widget.configure(theme=self.settings['codebox_theme'].lower())

    def load_previous_settings(self):
        if os.path.exists(self.previous_settings_file):
            with open(self.previous_settings_file, 'r') as f:
                return json.load(f)
        else:
            return None

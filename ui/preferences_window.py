import customtkinter as ctk
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
import webbrowser
from CTkCodeBox import CTkCodeBox
from CTkMessagebox import CTkMessagebox
from utils.helpers import convert_into, close_window, show_font_families, save_settings, load_settings
from utils.variables import THEMES, DEFAULT_SETTINGS, MAIN_THEMES
from CTkListbox import CTkListbox


class PreferencesWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow
        self.title("Preferences")
        self.geometry("1000x400")
        self.resizable(False, False)
        self.after(300, lambda: self.iconbitmap(self.resource_path('assets/xzy-notepad-icon.ico')))

        self.resource_path = resource_path

        self._initialize_components()

    def _initialize_components(self):
        ctk.CTkLabel(self, text="Font Size:").place(relx=0.01, rely=0.01)
        self.font_size_entry = ctk.CTkEntry(self)
        self.font_size_entry.insert(0, self.MainWindow.settings["font_size"])
        self.font_size_entry.place(relx=0.01, rely=0.08)

        ctk.CTkLabel(self, text="Font Family:").place(relx=0.01, rely=0.2)
        self.font_family_entry = ctk.CTkEntry(self)
        self.font_family_entry.insert(0, self.MainWindow.settings["font_family"])
        self.font_family_entry.place(relx=0.01, rely=0.28)

        ctk.CTkLabel(self, text="Indent Spaces:").place(relx=0.01, rely=0.4)
        self.indent_spaces_entry = ctk.CTkEntry(self)
        self.indent_spaces_entry.insert(0, self.MainWindow.settings["indent_space"])
        self.indent_spaces_entry.place(relx=0.01, rely=0.48)

        ctk.CTkLabel(self, text="Auto save time in minutes (file):").place(relx=0.01, rely=0.6)
        self.auto_save_file_time = ctk.CTkEntry(self)
        self.auto_save_file_time.insert(0, self.MainWindow.settings["auto_save_file_time"])
        self.auto_save_file_time.place(relx=0.01, rely=0.68)

        ctk.CTkLabel(self, text="Theme:").place(relx=0.17, rely=0.01)
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        ctk.CTkRadioButton(self, text="Dark", variable=self.theme_var, value="Dark").place(relx=0.17, rely=0.1)
        ctk.CTkRadioButton(self, text="Light", variable=self.theme_var, value="Light").place(relx=0.17, rely=0.2)

        ctk.CTkLabel(self, text="Auto Load (settings):").place(relx=0.16, rely=0.3)
        self.auto_load = ctk.StringVar(value=self.MainWindow.settings["auto_load"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.auto_load, value="Enabled").place(relx=0.17, rely=0.4)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.auto_load, value="Disabled").place(relx=0.17, rely=0.5)

        ctk.CTkLabel(self, text="Auto Save (settings):").place(relx=0.3, rely=0.3)
        self.auto_save = ctk.StringVar(value=self.MainWindow.settings["auto_save"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.auto_save, value="Enabled").place(relx=0.3, rely=0.4)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.auto_save, value="Disabled").place(relx=0.3, rely=0.5)

        ctk.CTkLabel(self, text="Auto Save (file):").place(relx=0.3, rely=0.01)
        self.auto_save_file = ctk.StringVar(value=self.MainWindow.settings["auto_save_file"])
        ctk.CTkRadioButton(self, text="Enabled", variable=self.auto_save_file, value="Enabled").place(relx=0.3, rely=0.1)
        ctk.CTkRadioButton(self, text="Disabled", variable=self.auto_save_file, value="Disabled").place(relx=0.3, rely=0.2)

        ctk.CTkLabel(self, text="Codebox Theme (text):").place(relx=0.45, rely=0.01)
        self.codebox_themes = CTkListbox(self, width=125, font=ctk.CTkFont(family="Arial", size=12),
                                         hover_color=ThemeManager.theme["CTkOptionMenu"]["button_hover_color"],
                                         highlight_color=ThemeManager.theme["CTkButton"]["hover_color"])
        self.codebox_themes.place(relx=0.45, rely=0.1, relheight=0.5)
        for theme in THEMES.values():
            self.codebox_themes.insert("END", theme)
        self.codebox_themes.select(list(THEMES.keys())[list(THEMES.values()).index(self.MainWindow.settings["codebox_theme"])])

        ctk.CTkButton(self, text="Check all codebox themes (text)", width=70, height=25,
                      command=lambda: webbrowser.open('https://pygments.org/styles/'),
                      font=ctk.CTkFont(family='Arial', size=13)).place(relx=0.425, rely=0.625)

        ctk.CTkLabel(self, text="Main Theme:").place(relx=0.65, rely=0.01)
        self.main_themes = CTkListbox(self, width=125, font=ctk.CTkFont(family="Arial", size=12),
                                      hover_color=ThemeManager.theme["CTkOptionMenu"]["button_hover_color"],
                                      highlight_color=ThemeManager.theme["CTkButton"]["hover_color"])
        self.main_themes.place(relx=0.65, rely=0.1, relheight=0.5)
        for theme in MAIN_THEMES.values():
            self.main_themes.insert("END", theme)
        self.main_themes.select(list(MAIN_THEMES.keys())[list(MAIN_THEMES.values()).index(self.MainWindow.settings["main_theme"].title())])

        self.MainWindow.all_children.append(self)

        ctk.CTkButton(self, text="Apply (with auto save)", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=self.apply_preferences, width=160, height=35).place(relx=0.01, rely=0.9)
        ctk.CTkButton(self, text="Apply default settings", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=lambda: self.apply_preferences(True), width=180, height=35).place(relx=0.2, rely=0.9)
        ctk.CTkButton(self, text="Apply previous settings", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=self.apply_previous_preferences, width=160, height=35).place(relx=0.39, rely=0.9)
        ctk.CTkButton(self, text="Check available font families", font=ctk.CTkFont(family="Arial", size=15), corner_radius=15,
                      command=lambda: show_font_families(self.MainWindow), width=160, height=35).place(relx=0.58, rely=0.9)

        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self, self.MainWindow))

        self.after(100, lambda: self.focus_set())

    def apply_preferences(self, default=False):
        save_settings(self.MainWindow, self.MainWindow.previous_settings_file)
        if default is False:
            self.MainWindow.settings["font_size"] = convert_into(self.font_size_entry.get(), "int", 4, 120) or self.MainWindow.settings["font_size"]
            self.MainWindow.settings["indent_space"] = convert_into(self.indent_spaces_entry.get(), "int", 1, 32) or self.MainWindow.settings["indent_space"]
            self.MainWindow.settings["auto_save_file_time"] = convert_into(self.auto_save_file_time.get(), "int", 1, 10) or self.MainWindow.settings["auto_save_file_time"]
            self.MainWindow.settings["font_family"] = self.font_family_entry.get()
            self.MainWindow.settings["codebox_theme"] = self.codebox_themes.get()
            if self.MainWindow.settings["main_theme"].title() != self.main_themes.get():
                CTkMessagebox(title="xzyNotepad (changing main theme)", icon="warning", message="To apply main theme. Restart the xzyNotepad.")
                self.MainWindow.settings["main_theme"] = self.main_themes.get()
            self.MainWindow.settings["auto_load"] = self.auto_load.get()
            self.MainWindow.settings["auto_save"] = self.auto_save.get()
            self.MainWindow.settings["auto_save_file"] = self.auto_save_file.get()
            if self.MainWindow.settings["auto_save"] == "Enabled":
                save_settings(self.MainWindow, self.MainWindow.settings_file)
        else:
            self.MainWindow.settings = DEFAULT_SETTINGS.copy()
            self.set_vars()
        ctk.set_appearance_mode(self.theme_var.get())
        ctk.set_default_color_theme(self.resource_path(f'assets/themes/{self.main_themes.get().lower()}.json'))
        for window in self.MainWindow.all_children + [self.MainWindow]:
            for widget in window.winfo_children():
                if isinstance(widget, CTkCodeBox):
                    widget.configure(font=ctk.CTkFont(self.MainWindow.settings["font_family"], self.MainWindow.settings["font_size"]))
                    widget.configure(theme=self.MainWindow.settings["codebox_theme"].lower())
        self.after(50, lambda: self.focus_set())

    def apply_previous_preferences(self):
        load_settings(self.MainWindow, self.MainWindow.previous_settings_file, set_vars=True)
        self.set_vars()

    def set_vars(self):
        self.auto_load.set(self.MainWindow.settings['auto_load'])
        self.auto_save.set(self.MainWindow.settings['auto_save'])
        self.auto_save_file.set(self.MainWindow.settings['auto_save_file'])
        self.theme_var.set(self.MainWindow.settings['theme'])
        self.font_size_entry.delete(0, ctk.END)
        self.font_family_entry.delete(0, ctk.END)
        self.indent_spaces_entry.delete(0, ctk.END)
        self.auto_save_file_time.delete(0, ctk.END)
        self.font_size_entry.insert(0, self.MainWindow.settings["font_size"])
        self.font_family_entry.insert(0, self.MainWindow.settings["font_family"])
        self.indent_spaces_entry.insert(0, self.MainWindow.settings["indent_space"])
        self.auto_save_file_time.insert(0, self.MainWindow.settings["auto_save_file_time"])
        self.codebox_themes.select(list(THEMES.keys())[list(THEMES.values()).index(self.MainWindow.settings["codebox_theme"])])
        self.main_themes.select(list(MAIN_THEMES.keys())[list(MAIN_THEMES.values()).index(self.MainWindow.settings["main_theme"].title())])

    def change_language(self):
        pass
        # Soon

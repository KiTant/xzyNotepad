from CTkMenuBar import *
import customtkinter as ctk
from utils.helpers import open_file, save_as_file, check_updates, save_file


class TitleMenu(CTkTitleMenu):
    def __init__(self, MainWindow: ctk.CTk, CurrentWindow: ctk.CTkToplevel or ctk.CTk):
        super().__init__(master=CurrentWindow, x_offset=600)

        self.File_Button = self.add_cascade("File")
        self.Edit_Button = self.add_cascade("Edit")
        self.Settings_Button = self.add_cascade("Settings")
        self.About_Button = self.add_cascade("About", command=MainWindow.show_about)

        self.File_Dropdown = CustomDropdownMenu(widget=self.File_Button, hover_color="#FF5000")
        self.File_Dropdown.add_option(option="New (Ctrl + N)", command=MainWindow.new_file)
        self.File_Dropdown.add_option(option="Open (Ctrl + O)", command=lambda: open_file(MainWindow, CurrentWindow))
        self.File_Dropdown.add_option(option="Save (Ctrl + S)", command=lambda: save_file(MainWindow, CurrentWindow, CurrentWindow.full_file_path, False))
        self.File_Dropdown.add_option(option="Save as", command=lambda: save_as_file(MainWindow, CurrentWindow, CurrentWindow.current_language))

        self.Edit_Dropdown = CustomDropdownMenu(widget=self.Edit_Button, hover_color="#FF5000")
        self.Edit_Dropdown.add_option(option="Replace (Soon)", command=MainWindow.show_soon)
        self.Edit_Dropdown.add_option(option="Find (Soon)", command=MainWindow.show_soon)

        self.Settings_Dropdown = CustomDropdownMenu(widget=self.Settings_Button, hover_color="#FF5000")
        self.Settings_Dropdown.add_option(option="Preferences (Ctrl + P)", command=MainWindow.show_preferences)
        self.Settings_Dropdown.add_option(option="Load settings", command=lambda: MainWindow.load_settings(MainWindow.settings_file, set_vars=True))
        self.Settings_Dropdown.add_option(option="Save settings", command=lambda: MainWindow.save_settings(MainWindow.settings_file))
        self.Settings_Dropdown.add_option(option="Check updates (Ctrl + U)", command=lambda: check_updates(MainWindow))


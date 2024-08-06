from CTkMenuBar import *
import customtkinter as ctk


class TitleMenu(CTkTitleMenu):
    def __init__(self, MainWindow: ctk.CTk, CurrentWindow: ctk.CTkToplevel or ctk.CTk):
        super().__init__(master=CurrentWindow, x_offset=600)
        self.File_Button = self.add_cascade("File")
        self.Edit_Button = self.add_cascade("Edit")
        self.Settings_Button = self.add_cascade("Settings")
        self.About_Button = self.add_cascade("About", command=MainWindow.show_about)

        self.File_Dropdown = CustomDropdownMenu(widget=self.File_Button)
        self.File_Dropdown.add_option(option="New (Ctrl + N)", command=MainWindow.new_file)
        self.File_Dropdown.add_option(option="Open (Ctrl + O)",
                                      command=lambda: MainWindow.open_file(CurrentWindow, CurrentWindow.codebox, CurrentWindow.saved))
        self.File_Dropdown.add_option(option="Save as (Ctrl + S)",
                                      command=lambda: MainWindow.save_as_file(CurrentWindow, CurrentWindow.codebox, CurrentWindow.current_language))

        self.Edit_Dropdown = CustomDropdownMenu(widget=self.Edit_Button)
        self.Edit_Dropdown.add_option(option="Replace (Soon)", command=MainWindow.show_soon)
        self.Edit_Dropdown.add_option(option="Find (Soon)", command=MainWindow.show_soon)

        self.Settings_Dropdown = CustomDropdownMenu(widget=self.Settings_Button)
        self.Settings_Dropdown.add_option(option="Preferences (Ctrl + P)", command=MainWindow.preferences)
        self.Settings_Dropdown.add_option(option="Check updates (Soon)", command=MainWindow.show_soon)

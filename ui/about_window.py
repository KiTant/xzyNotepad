import customtkinter as ctk
from utils.helpers import close_window
from utils.variables import VERSION
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: "MainWindowClass", resource_path):
        super().__init__()
        self.MainWindow = MainWindow

        self.title("About")
        self.geometry("300x200")
        self.after(300, lambda: self.iconbitmap(self.resource_path('assets/xzy-notepad-icon.ico')))
        self.resource_path = resource_path

        about_text = f"xzyNotepad\nVersion {VERSION}" \
                     f"\n\nAn open-source versatile notepad" \
                     f" \ndesigned specifically for writing and editing code \nin various programming languages."
        ctk.CTkLabel(self, text=about_text, justify="center").pack(expand=True)
        ctk.CTkButton(self, text="Open guide (in browser)", width=150, height=50,
                      command=lambda: os.startfile(self.resource_path('assets/xzyNotepadGuide.html')),
                      font=ctk.CTkFont(family='Arial', size=15)).pack(expand=True)
        MainWindow.all_children.append(self)
        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self, self.MainWindow))

        self.after(100, lambda: self.focus_set())

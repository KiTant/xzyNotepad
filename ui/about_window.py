import customtkinter as ctk
from utils.helpers import close_window
from utils.variables import VERSION
import os


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow

        self.title("About")
        self.geometry("300x200")
        self.after(300, self.place_icon)
        self.resource_path = resource_path

        about_text = f"xzyNotepad\nVersion {VERSION}\n\nAn open-source versatile notepad \ndesigned specifically for writing and editing code \nin various programming languages."
        ctk.CTkLabel(self, text=about_text, justify="center").pack(expand=True)
        ctk.CTkButton(self, text="Open guide (in browser)", width=150, height=50, command=self.open_guide,
                      font=ctk.CTkFont(family='Arial', size=15)).pack(expand=True)
        MainWindow.all_children.append(self)
        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self, self.MainWindow))

        self.after(100, lambda: self.focus_set())

    def place_icon(self):
        try: self.iconbitmap(self.resource_path('assets/xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

    def open_guide(self):
        try: os.startfile(self.resource_path('assets/xzyNotepadGuide.html'))
        except: os.startfile(os.path.join('assets\\xzyNotepadGuide.html'))

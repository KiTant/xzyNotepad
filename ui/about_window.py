import customtkinter as ctk
from utils.helpers import Version


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow

        self.title("About")
        self.geometry("300x200")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        about_text = f"xzyNotepad\nVersion {Version}\n\nAn open-source versatile notepad \ndesigned specifically for writing and editing code \nin various programming languages."
        ctk.CTkLabel(self, text=about_text, justify="center").pack(expand=True)
        MainWindow.all_children.append(self)
        self.protocol("WM_DELETE_WINDOW", lambda: MainWindow.destroy_other_window(self))

        self.after(100, lambda: self.focus_set())

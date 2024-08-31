import customtkinter as ctk
from ui.title_menu import TitleMenu
from CTkCodeBox import CTkCodeBox
from utils.helpers import code_window_binder, close_code_window, save_file
from utils.variables import LANGUAGES


class NewWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow
        self.current_language = "txt"
        self.title(f"xzyNotepad - New File.{self.current_language}")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')
        self.geometry("1000x500")
        self.minsize(1000, 350)
        self.maxsize(1250, 1000)

        self.file_name = f"New File.{self.current_language}"
        self.saved = True
        self.full_file_path = None

        self._initialize_components()

    def _initialize_components(self):
        self.codebox = CTkCodeBox(self, language=LANGUAGES[self.current_language], height=500, theme=self.MainWindow.settings["codebox_theme"].lower(),
                                  font=ctk.CTkFont(family=self.MainWindow.settings["font_family"], size=self.MainWindow.settings["font_size"]))
        self.codebox.pack(fill="both", expand=True)
        code_window_binder(self.MainWindow, self)
        self.menu = TitleMenu(self.MainWindow, self)

        self.protocol("WM_DELETE_WINDOW", self.activate_destroy)
        self.MainWindow.all_children.append(self)

        self.after(100, lambda: self.focus_set())
        self.after(self.MainWindow.settings["auto_save_file_time"] * 60000, lambda: save_file(self.MainWindow, self, self.full_file_path, True))

    def winfo_name(self): return '!toplevel'

    def activate_destroy(self): close_code_window(self, self.MainWindow.all_children)

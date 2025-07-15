import customtkinter as ctk
from ui.title_menu import TitleMenu
from ui.code_window_menu import TextMenu
from CTkCodeBox import CTkCodeBox
from utils.helpers import code_window_binder, close_code_window, save_file
from ui.line_nums_codebox import AddLineNums
from utils.variables import LANGUAGES


class NewWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow
        self.current_language = "txt"
        self.title(f"xzyNotepad - New File.{self.current_language}")
        self.after(300, lambda: self.iconbitmap(self.resource_path('assets/xzy-notepad-icon.ico')))
        self.geometry("1200x550")

        self.resource_path = resource_path
        self.file_name = f"New File.{self.current_language}"
        self.saved = True
        self.full_file_path = None

        self.history = [""]
        self.history_index = 0
        self.max_history_size = 250

        self._initialize_components()

    def _initialize_components(self):
        self.codebox = CTkCodeBox(self, language=LANGUAGES[self.current_language], height=500, theme=self.MainWindow.settings["codebox_theme"].lower(),
                                  font=ctk.CTkFont(family=self.MainWindow.settings["font_family"], size=self.MainWindow.settings["font_size"]),
                                  menu=False, undo=False, line_numbering=False)
        self.codebox.text_menu = TextMenu(Window=self, MainWindow=self.MainWindow)
        self.codebox.line_nums = AddLineNums(self.codebox)
        self.codebox.pack(fill="both", expand=True)
        code_window_binder(self.MainWindow, self)
        self.menu = TitleMenu(self.MainWindow, self)

        self.protocol("WM_DELETE_WINDOW", lambda: close_code_window(self, self.MainWindow.all_children))
        self.MainWindow.all_children.append(self)
        self.MainWindow.all_titles_menu.append(self.menu)

        self.after(100, lambda: self.focus_set())
        self.after(self.MainWindow.settings["auto_save_file_time"] * 60000, lambda: save_file(self.MainWindow, self, self.full_file_path, True))

    def change_history(self):
        current_text = self.codebox.get(0.0, "end")
        current_text = current_text[:-1]
        current_history_text = self.history[self.history_index]
        if current_history_text != current_text:
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            self.history.append(current_text)
            if len(self.history) > self.max_history_size:
                self.history.pop(0)
            self.history_index = len(self.history) - 1

    def winfo_name(self): return '!toplevel'

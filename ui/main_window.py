import customtkinter as ctk
from CTkCodeBox import CTkCodeBox
from utils.helpers import code_window_binder, close_code_window, save_file, save_settings, load_settings, load_previous_settings
from utils.variables import LANGUAGES, DEFAULT_SETTINGS
from ui.code_window_menu import TextMenu
from ui.line_nums_codebox import AddLineNums
from ui.title_menu import TitleMenu


class MainWindow(ctk.CTk):
    def __init__(self, resource_path, settings_file, previous_settings_file):
        super().__init__()
        self.current_language = "txt"
        self.title(f"xzyNotepad - New File.{self.current_language}")
        self.geometry("1200x550")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        self.resource_path = resource_path
        self.disable_updating_code = False
        self.file_name = f"New File.{self.current_language}"
        self.full_file_path = None
        self.updating = False
        self.saved = True
        self.all_children = []
        self.all_titles_menu = []

        self.history = [""]
        self.history_index = 0
        self.max_history_size = 250

        self.settings_file = settings_file
        self.previous_settings_file = previous_settings_file
        self.settings = DEFAULT_SETTINGS.copy()
        self.previous_settings = load_previous_settings(self)

        load_settings(self, self.settings_file, True)
        self._initialize_components()

    def _initialize_components(self):
        self.codebox = CTkCodeBox(self, language=LANGUAGES[self.current_language], height=500, theme=self.settings['codebox_theme'].lower(),
                                  font=ctk.CTkFont(family=self.settings['font_family'], size=self.settings['font_size']),
                                  menu=False, undo=False, line_numbering=False)
        self.codebox.text_menu = TextMenu(Window=self, MainWindow=self)
        self.codebox.line_nums = AddLineNums(self.codebox)
        self.codebox.pack(fill="both", expand=True)
        code_window_binder(Window=self, MainWindow=self)
        self.menu = TitleMenu(CurrentWindow=self, MainWindow=self)

        self.all_titles_menu.append(self.menu)

        self.protocol("WM_DELETE_WINDOW", lambda: close_code_window(self, self.all_children))

        self.after(self.settings["auto_save_file_time"] * 60000, lambda: save_file(self, self, self.full_file_path, True))

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

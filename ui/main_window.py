import customtkinter as ctk
from ui.new_window import NewWindow
from ui.preferences_window import PreferencesWindow
from ui.about_window import AboutWindow
from ui.title_menu import TitleMenu
from CTkCodeBox import CTkCodeBox
from tkinter import filedialog
from utils.helpers import LANGUAGES, show_messagebox, File_Types


class MainWindow(ctk.CTk):
    def __init__(self, resource_path):
        super().__init__()
        self.title("xzyNotepad - New File.py")
        self.geometry("1000x500")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        self.resource_path = resource_path
        self.disable_updating_code = False
        self.file_name = "New File.py"
        self.updating = False
        self.indent_space = 4
        self.current_language = "py"
        self.font_family = "Arial"
        self.font_size = 12
        self.saved = True
        self.all_children = []

        self._initialize_components()

    def _initialize_components(self):
        self.codebox = CTkCodeBox(self, language='python', height=500, font=ctk.CTkFont(family=self.font_family, size=self.font_size))
        self.codebox.pack(fill="both", expand=True)
        self.codebox.bind("<Tab>", self.insert_tab)
        self.codebox.bind("<<Modified>>", lambda event: self.code_updated(self, event))
        self.bind("<Control-s>", lambda event: self.save_as_file(self, self.codebox, self.current_language))
        self.bind("<Control-p>", lambda event: self.preferences())
        self.bind("<Control-o>", lambda event: self.open_file(self, self.codebox, self.saved))
        self.bind("<Control-n>", lambda event: self.new_file())

        self.menu = TitleMenu(self, self)

        self.protocol("WM_DELETE_WINDOW", lambda: self.do_quit(self, self.saved))

    def insert_tab(self, event=None):
        widget = event.widget
        if str(widget)[-18:] == ".!ctkcodebox.!text":
            widget.insert("insert", " " * self.indent_space)
        return "break"

    def new_file(self): NewWindow(self, self.resource_path)

    def show_soon(self): show_messagebox(title="xzyNotepad", message="This option will be soon.", icon="info")

    def open_file(self, parent: ctk.CTk or ctk.CTkToplevel, codebox: CTkCodeBox, saved: bool):
        if not saved:
            msg = show_messagebox(title="xzyNotepad", message="You sure? File is not saved.", icon="question", options=["Yes", "No"])
            if msg != "Yes":
                return
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=File_Types)
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            file_format = file_path.split('.')[-1]
            parent.file_name = file_path.split('/')[-1]
            codebox.configure(language=LANGUAGES[file_format])
            codebox.delete("1.0", ctk.END)
            codebox.insert("1.0", content)
            parent.title(f"xzyNotepad - {file_path.split('/')[-1]}")
            parent.current_language = file_format
        parent.focus_set()

    def save_as_file(self, parent: ctk.CTk or ctk.CTkToplevel, codebox: CTkCodeBox, ext="py"):
        title = LANGUAGES.get(ext, 'Unknown').title() if isinstance(LANGUAGES.get(ext), str) else LANGUAGES[ext].name.title()
        file_path = filedialog.asksaveasfilename(defaultextension=f".{title}", initialfile=parent.file_name,
                                                 filetypes=[(f"{title} Files", f"*.{ext or 'Unknown'}")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = codebox.get("1.0", ctk.END)
                self.disable_updating_code = True
                codebox.edit_modified(False)
                self.saved = True
                file.write(content)
            parent.title(f"xzyNotepad - {file_path.split('/')[-1]}")
            self.after(100, lambda: setattr(self, "disable_updating_code", False))
        parent.focus_set()

    def code_updated(self, parent: ctk.CTk or ctk.CTkToplevel = None, event=None):
        if not self.disable_updating_code:
            parent.saved = False

    def convert_into(self, value, converter):
        converters = {"int": int, "float": float}
        try:
            return converters[converter](value)
        except (ValueError, KeyError):
            return None

    def preferences(self):
        for window in self.all_children:
            if window.title() == "Preferences":
                return
        PreferencesWindow(self, self.resource_path)

    def show_about(self):
        for window in self.all_children:
            if window.title() == "About":
                return
        AboutWindow(self, self.resource_path)

    def destroy_other_window(self, window):
        self.all_children.remove(window)
        window.destroy()

    def do_quit(self, parent: ctk.CTk or ctk.CTkToplevel, saved: bool):
        message = None
        found_other_codebox = any(hasattr(window, 'codebox') for window in self.all_children)
        if parent not in self.all_children and found_other_codebox:
            message = "You sure? Closing main window of xzyNotepad will close all other xzyNotepad windows."
        if not saved:
            message = message + " (and file is not saved)" if message else "You sure? File is not saved."
        if message:
            msg = show_messagebox(title="xzyNotepad", message=message, icon="question", options=["Yes", "No"])
            if msg == "Yes":
                if parent in self.all_children:
                    self.all_children.remove(parent)
                parent.menu.destroy()
                parent.destroy()
        else:
            if parent in self.all_children:
                self.all_children.remove(parent)
            parent.menu.destroy()
            parent.destroy()

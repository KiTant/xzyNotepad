import customtkinter as ctk
from ui.title_menu import TitleMenu
from CTkCodeBox import CTkCodeBox


class NewWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow
        self.title("xzyNotepad - New File.py")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')
        self.geometry("1000x500")
        self.minsize(1000, 350)
        self.maxsize(1250, 1000)

        self.codebox = CTkCodeBox(self, language="python", height=500, font=ctk.CTkFont(family=MainWindow.font_family, size=MainWindow.font_size))
        self.codebox.pack(fill="both", expand=True)
        self.codebox.bind("<Tab>", MainWindow.insert_tab)
        self.codebox.bind("<<Modified>>", lambda event: MainWindow.code_updated(self, event))
        self.bind("<Control-s>", lambda event: MainWindow.save_as_file(self, self.codebox, self.current_language))
        self.bind("<Control-p>", lambda event: MainWindow.preferences())
        self.bind("<Control-o>", lambda event: MainWindow.open_file(self, self.codebox, self.saved))
        self.bind("<Control-n>", lambda event: MainWindow.new_file())

        self.file_name = "New File.py"
        self.saved = True
        self.current_language = "py"
        self.menu = TitleMenu(self.MainWindow, self)

        self.protocol("WM_DELETE_WINDOW", self.activate_destroy)
        MainWindow.all_children.append(self)

        self.after(100, lambda: self.focus_set())

    def winfo_name(self): return '!toplevel'

    def activate_destroy(self): self.MainWindow.do_quit(self, self.saved)

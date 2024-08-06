import customtkinter as ctk
from CTkCodeBox import CTkCodeBox


class PreferencesWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.MainWindow = MainWindow
        self.title("Preferences")
        self.geometry("400x500")
        try: self.iconbitmap(resource_path('xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        # Font size selection
        ctk.CTkLabel(self, text="Font Size:").pack(pady=5)
        self.font_size_entry = ctk.CTkEntry(self)
        self.font_size_entry.insert(0, MainWindow.font_size)
        self.font_size_entry.pack(pady=10)

        # Font family selection
        ctk.CTkLabel(self, text="Font Family:").pack(pady=5)
        self.font_family_entry = ctk.CTkEntry(self)
        self.font_family_entry.insert(0, MainWindow.font_family)
        self.font_family_entry.pack(pady=10)

        # Indent spaces selection
        ctk.CTkLabel(self, text="Indent Spaces:").pack(pady=5)
        self.indent_spaces_entry = ctk.CTkEntry(self)
        self.indent_spaces_entry.insert(0, MainWindow.indent_space)
        self.indent_spaces_entry.pack(pady=10)

        # Theme selection
        ctk.CTkLabel(self, text="Theme:").pack(pady=10)
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        ctk.CTkRadioButton(self, text="Dark", variable=self.theme_var, value="dark").pack(pady=5)
        ctk.CTkRadioButton(self, text="Light", variable=self.theme_var, value="light").pack(pady=5)

        MainWindow.all_children.append(self)

        ctk.CTkButton(self, text="Apply", command=self.apply_preferences).pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", lambda: MainWindow.destroy_other_window(self))

        self.after(100, lambda: self.focus_set())

    def apply_preferences(self):
        self.MainWindow.font_size = self.MainWindow.convert_into(self.font_size_entry.get(), "int") or self.MainWindow.font_size
        self.MainWindow.indent_space = self.MainWindow.convert_into(self.indent_spaces_entry.get(), "int") or self.MainWindow.indent_space
        self.MainWindow.font_family = self.font_family_entry.get()
        ctk.set_appearance_mode(self.theme_var.get())
        for window in self.MainWindow.all_children + [self.MainWindow]:
            for widget in window.winfo_children():
                if isinstance(widget, CTkCodeBox):
                    widget.configure(font=ctk.CTkFont(self.MainWindow.font_family, self.MainWindow.font_size))
        self.after(50, lambda: self.focus_set())

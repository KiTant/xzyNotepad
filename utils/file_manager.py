import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from utils.variables import LANGUAGES, FILE_TYPES
import uuid
import os


def f_open(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    if not Window.saved:
        msg = CTkMessagebox(title="xzyNotepad", message="You sure? File is not saved.", icon="question", options=["Yes", "No"])
        if msg.get() not in ["Yes"]:
            return
    from ui.title_menu import TitleMenu
    for window in MainWindow.all_children + [MainWindow]:
        if hasattr(window, 'codebox'):
            MainWindow.all_titles_menu.remove(window.menu)
            window.menu.destroy()
            window.menu = None
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=FILE_TYPES)
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content, file_format = file.read(), file_path.split('.')[-1]
            Window.file_name, Window.full_file_path = file_path.split('/')[-1], file_path
            Window.codebox.configure(language=LANGUAGES[file_format] if file_format in list(LANGUAGES.keys()) else LANGUAGES["txt"])
            MainWindow.disable_updating_code = True
            Window.codebox.delete("0.0", ctk.END)
            Window.codebox.insert("0.0", content)
            Window.codebox.line_nums.redraw()
            Window.codebox.edit_modified(False)
            Window.current_language, Window.saved = file_format, True
            Window.change_history()
        Window.title(f"xzyNotepad - {file_path.split('/')[-1]}")
        MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    Window.focus_set()
    for window in MainWindow.all_children + [MainWindow]:
        if hasattr(window, 'codebox'):
            window.menu = TitleMenu(MainWindow, window)
            MainWindow.all_titles_menu.append(window.menu)


def f_save_as(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, ext="py", binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    title = LANGUAGES.get(ext, 'Unknown').title() if isinstance(LANGUAGES.get(ext), str) else LANGUAGES[ext].name.title()
    from ui.title_menu import TitleMenu
    for window in MainWindow.all_children + [MainWindow]:
        if hasattr(window, 'codebox'):
            MainWindow.all_titles_menu.remove(window.menu)
            window.menu.destroy()
            window.menu = None
    file_path = filedialog.asksaveasfilename(defaultextension=f".{title}", initialfile=Window.file_name, filetypes=FILE_TYPES)
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            content = Window.codebox.get(0.0, ctk.END)[:-1]
            MainWindow.disable_updating_code = True
            file.write(content)
            Window.codebox.edit_modified(False)
            Window.full_file_path, Window.saved = file_path, True
            Window.change_history()
        Window.title(f"xzyNotepad - {file_path.split('/')[-1]}")
        Window.current_language = file_path.split('.')[-1]
        Window.codebox.configure(language=LANGUAGES[Window.current_language] if Window.current_language in list(LANGUAGES.keys()) else LANGUAGES["txt"])
        MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    Window.focus_set()
    for window in MainWindow.all_children + [MainWindow]:
        if hasattr(window, 'codebox'):
            window.menu = TitleMenu(MainWindow, window)
            MainWindow.all_titles_menu.append(window.menu)


def f_save(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, full_file_path, auto=False, binded: bool = False):
    if Window is None or (MainWindow.settings['keybinds'] == "Disabled" and binded is True):
        return
    if ((MainWindow.settings['auto_save_file'] == "Enabled" and auto is True) or auto is False) and full_file_path is not None and Window.saved is False:
        with open(full_file_path, "w", encoding="utf-8") as file:
            content = Window.codebox.get(0.0, ctk.END)[:-1]
            MainWindow.disable_updating_code = True
            file.write(content)
            Window.codebox.edit_modified(False)
            Window.saved = True
            Window.change_history()
            Window.title(f"xzyNotepad - {Window.full_file_path.split('/')[-1]}")
            MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    elif Window.saved is True and auto is False:
        CTkMessagebox(title="xzyNotepad", message="Your file is already saved or not changed.", icon="warning")
    elif full_file_path is None and auto is False:
        f_save_as(MainWindow, Window, Window.current_language)
    if MainWindow.settings['auto_save_file'] == "Enabled" and auto is True:
        Window.after(MainWindow.settings["auto_save_file_time"] * 60000, lambda: f_save(MainWindow, Window, full_file_path, True))


def f_start(Window: ctk.CTk or ctk.CTkToplevel, full_file_path):
    if full_file_path is None:
        content = Window.codebox.get(0.0, ctk.END)[:-1]
        temp_dir = os.getenv('TEMP', os.getenv('TMP', 'C:\\Temp'))
        filename = f"{uuid.uuid1()}.{Window.current_language}"
        file_path = os.path.join(temp_dir, filename)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            os.startfile(file_path)
        except Exception as err:
            CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to start file.", icon="warning")
    else:
        os.startfile(os.path.join(full_file_path))

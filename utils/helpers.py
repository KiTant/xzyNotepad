import requests
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from tkinter import filedialog
from utils.variables import LANGUAGES, FILE_TYPES, VERSION


def show_messagebox(title, message, icon, options="OK", sound=False):
    msgbox = CTkMessagebox(title=title, message=message, icon=icon, options=options, sound=sound)
    return msgbox.get()


def code_window_binder(MainWindow, Window):
    Window.codebox.bind("<Tab>", lambda event: insert_tab(event, MainWindow.settings["indent_space"]))
    Window.codebox.bind("<<Modified>>", lambda event: code_updated(Window, MainWindow))
    Window.bind("<Control-s>", lambda event: save_file(MainWindow, Window, Window.full_file_path, False, True))
    Window.bind("<Control-p>", lambda event: MainWindow.show_preferences(MainWindow, True))
    Window.bind("<Control-o>", lambda event: open_file(MainWindow, Window, True))
    Window.bind("<Control-n>", lambda event: MainWindow.new_file(True))


def convert_into(value, converter, minimum=None, maximum=None):
    converters = {"int": int, "float": float}
    try:
        converted = converters[converter](value)
        if minimum is not None:
            if converted < minimum:
                return None
        if maximum is not None:
            if converted > maximum:
                return None
        return converted
    except (ValueError, KeyError):
        return None


def close_code_window(Window: ctk.CTk or ctk.CTkToplevel, all_children):
    message = None
    main_window = False
    if Window not in all_children:
        main_window = True
        if any(hasattr(window, 'codebox') for window in all_children):
            message = "You sure? Closing main window of xzyNotepad will close all other xzyNotepad windows."
    if not Window.saved:
        message = message + " (and file is not saved)" if message else "You sure? File is not saved."
    if message:
        msg = show_messagebox(title="xzyNotepad", message=message, icon="question", options=["Yes", "No"])
        if msg in ["Yes"]:
            if main_window is True:
                Window.quit()
            else:
                if Window in all_children:
                    all_children.remove(Window)
                Window.menu.destroy()
                Window.destroy()
    else:
        if main_window is True:
            Window.quit()
        else:
            if Window in all_children:
                all_children.remove(Window)
            Window.menu.destroy()
            Window.destroy()


def close_window(Window: ctk.CTk or ctk.CTkToplevel = None, MainWindow: ctk.CTk = None):
    MainWindow.all_children.remove(Window)
    Window.destroy()


def code_updated(Window: ctk.CTk or ctk.CTkToplevel = None, MainWindow: ctk.CTk = None):
    if not MainWindow.disable_updating_code:
        if Window.full_file_path is not None:
            Window.title(f"xzyNotepad - *{Window.full_file_path.split('/')[-1]}")
        else:
            Window.title(f"xzyNotepad - *New File.{Window.current_language}")
        Window.saved = False


def insert_tab(event=None, indent_space=4):
    widget = event.widget
    if str(widget)[-18:].strip() == ".!ctkcodebox.!text":
        widget.insert("insert", " " * indent_space)
    return "break"


def open_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    if not Window.saved:
        msg = show_messagebox(title="xzyNotepad", message="You sure? File is not saved.", icon="question",
                              options=["Yes", "No"])
        if msg not in ["Yes"]:
            return
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=FILE_TYPES)
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            file_format = file_path.split('.')[-1]
            Window.file_name = file_path.split('/')[-1]
            Window.full_file_path = file_path
            Window.codebox.configure(language=LANGUAGES[file_format] if file_format in list(LANGUAGES.keys()) else LANGUAGES["txt"])
            MainWindow.disable_updating_code = True
            Window.codebox.delete("1.0", ctk.END)
            Window.codebox.insert("1.0", content)
            Window.codebox.edit_modified(False)
            Window.current_language = file_format
            Window.saved = True
        Window.title(f"xzyNotepad - {file_path.split('/')[-1]}")
        MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    Window.focus_set()


def save_as_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, ext="py", binded: bool = False):
    if MainWindow.settings['keybinds'] == "Disabled" and binded is True:
        return
    title = LANGUAGES.get(ext, 'Unknown').title() if isinstance(LANGUAGES.get(ext), str) else LANGUAGES[ext].name.title()
    file_path = filedialog.asksaveasfilename(defaultextension=f".{title}", initialfile=Window.file_name,
                                             filetypes=[(f"{title} Files", f"*.{ext or 'Unknown'}")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            content = Window.codebox.get("1.0", ctk.END)
            MainWindow.disable_updating_code = True
            file.write(content)
            Window.codebox.edit_modified(False)
            Window.saved = True
            Window.full_file_path = file_path
        Window.title(f"xzyNotepad - {file_path.split('/')[-1]}")
        MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    Window.focus_set()


def save_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, full_file_path, auto=False, binded: bool = False):
    if Window is None or (MainWindow.settings['keybinds'] == "Disabled" and binded is True):
        return
    if ((MainWindow.settings['auto_save_file'] == "Enabled" and auto is True) or auto is False) and full_file_path is not None and Window.saved is False:
        with open(full_file_path, "w", encoding="utf-8") as file:
            content = Window.codebox.get("1.0", ctk.END)
            MainWindow.disable_updating_code = True
            file.write(content)
            Window.codebox.edit_modified(False)
            Window.saved = True
            Window.title(f"xzyNotepad - {Window.full_file_path.split('/')[-1]}")
            MainWindow.after(100, lambda: setattr(MainWindow, "disable_updating_code", False))
    elif Window.saved is True and auto is False:
        show_messagebox("xzyNotepad", "Your file is already saved or not changed.", "warning")
    elif full_file_path is None and auto is False:
        save_as_file(MainWindow, Window, Window.current_language)
    if MainWindow.settings['auto_save_file'] == "Enabled" and auto is True:
        Window.after(MainWindow.settings["auto_save_file_time"] * 60000, lambda: save_file(MainWindow, Window, full_file_path, True))


def update_notepad(MainWindow: ctk.CTk, version):
    msg = CTkMessagebox(title="xzyNotepad (updating)",
                        message="Update of xzyNotepad is started, please wait...",
                        icon="info")
    response = requests.get(f'https://github.com/KiTant/xzyNotepad/releases/download/{version}/xzyNotepad.exe')
    msg.destroy()
    if response.ok:
        try:
            with open(f"xzyNotepad{version}.exe", "wb") as file:
                file.write(response.content)
            CTkMessagebox(title="xzyNotepad (updating)",
                          message="New update successfully installed as new file in directory where storages this version. "
                                  "You can delete this version and open new.",
                          icon="check")
            MainWindow.updating = False
        except:
            CTkMessagebox(title="xzyNotepad (downloading update)",
                          message="Unexpected error while creating new file with update.",
                          icon="warning")
            MainWindow.updating = False
    else:
        CTkMessagebox(title="xzyNotepad (getting update)",
                      message="Unexpected error while trying to get last release, please check your internet.",
                      icon="warning")
        MainWindow.updating = False


def check_updates(MainWindow: ctk.CTk):
    for window in MainWindow.all_children:
        if window.title() == "xzyNotepad (checking updates)" or MainWindow.updating is True:
            return
    MainWindow.updating = True
    msg = CTkMessagebox(title="xzyNotepad (checking updates)",
                        message="Trying to check updates please wait...",
                        icon="info")
    response = requests.get("https://api.github.com/repos/KiTant/xzyNotepad/releases/latest")
    msg.destroy()
    if response.ok:
        latest_release = response.json()
        if VERSION < latest_release['tag_name'][1:]:
            msg = show_messagebox(title="xzyNotepad (checking updates)",
                                  message="Your version is outdated, do you want to update?",
                                  icon="info", options=["Yes", "No"])
            if msg in ["Yes"]:
                all_saved = True
                found_file = False
                for window in MainWindow.all_children + [MainWindow]:
                    if hasattr(window, "saved"):
                        if window.saved is False:
                            all_saved = False
                            break
                if all_saved is False:
                    msg = show_messagebox(title="xzyNotepad (updating)",
                                          message="Some files not saved, you really want to update?",
                                          icon="warning", options=["Yes", "No"])
                    if msg in ["No"]:
                        MainWindow.updating = False
                        return
                if latest_release['assets'] is None:
                    MainWindow.updating = False
                    return
                for asset in latest_release['assets']:
                    if asset['name'].strip() == "xzyNotepad.exe":
                        found_file = True
                        update_notepad(asset, latest_release['tag_name'])
                if found_file is False:
                    show_messagebox(title="xzyNotepad (updating)",
                                    message="Not found main file of xzyNotepad, update stopped.",
                                    icon="warning")
                    MainWindow.updating = False
        else:
            show_messagebox(title="xzyNotepad (checking updates)",
                            message="You have latest release of xzyNotepad",
                            icon="info")
            MainWindow.updating = False
    else:
        show_messagebox(title="xzyNotepad (checking updates)",
                        message="Unexpected error while checking last release, please check your internet.",
                        icon="warning")
        MainWindow.updating = False

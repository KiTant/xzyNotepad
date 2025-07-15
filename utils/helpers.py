import customtkinter as ctk
import webbrowser
from utils.code_window_manager import *
from utils.updater import check_last_version
from utils.file_manager import *
from utils.ui_manager import *
from utils.settings_manager import *
from CTkColorPicker.ctk_color_picker import AskColor


def save_settings(MainWindow: ctk.CTk, file):
    s_save(MainWindow, file)


def load_settings(MainWindow: ctk.CTk, file, auto_load=False, set_vars=False):
    s_load(MainWindow, file, auto_load, set_vars)


def load_previous_settings(MainWindow: ctk.CTk):
    s_previous_load(MainWindow)


def code_window_binder(MainWindow, Window):
    cw_binder(MainWindow, Window)


def close_code_window(Window: ctk.CTk or ctk.CTkToplevel, all_children):
    cw_close(Window, all_children)


def code_updated(Window: ctk.CTk or ctk.CTkToplevel, MainWindow: ctk.CTk):
    cw_updated(Window, MainWindow)


def insert_tab(event, indent_space=4):
    cw_tab(event, indent_space)


def insert_time(Window: ctk.CTk or ctk.CTkToplevel):
    cw_time(Window)


def open_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, binded: bool = False):
    f_open(MainWindow, Window, binded)


def save_as_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, ext="txt", binded: bool = False):
    f_save_as(MainWindow, Window, ext, binded)


def save_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, full_file_path,
              auto=False, binded: bool = False):
    f_save(MainWindow, Window, full_file_path, auto, binded)


def start_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, full_file_path, binded: bool = False):
    f_start(MainWindow, Window, full_file_path, binded)


def close_window(Window: ctk.CTk or ctk.CTkToplevel, MainWindow: ctk.CTk):
    w_close(Window, MainWindow)


def get_selected_text(Window: ctk.CTk or ctk.CTkToplevel):
    return cw_get_selected(Window)


def hash_text(Window: ctk.CTk or ctk.CTkToplevel, hash_type):
    cw_hash(Window, hash_type)


def encode_base(Window: ctk.CTk or ctk.CTkToplevel, num):
    cw_encode_base(Window, num)


def decode_base(Window: ctk.CTk or ctk.CTkToplevel, num):
    cw_decode_base(Window, num)


def encode_ascii(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_ascii(Window)


def decode_ascii(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_ascii(Window)


def encode_html(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_html(Window)


def decode_html(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_html(Window)


def encode_binary(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_binary(Window)


def decode_binary(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_binary(Window)


def encode_octal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_octal(Window)


def decode_octal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_octal(Window)


def encode_decimal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_decimal(Window)


def decode_decimal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_decimal(Window)


def encode_hexadecimal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_encode_hexadecimal(Window)


def decode_hexadecimal(Window: ctk.CTk or ctk.CTkToplevel):
    cw_decode_hexadecimal(Window)


def convert_value(Window: ctk.CTk or ctk.CTkToplevel, FromValue: str, ToValue: str):
    cw_convert_values(Window, FromValue, ToValue)


def new_file(MainWindow: ctk.CTk, binded: bool = False):
    w_new_file(MainWindow, binded)


def show_soon():
    w_show_soon()


def show_font_families(MainWindow: ctk.CTk):
    w_show_font_families(MainWindow)


def show_preferences(MainWindow: ctk.CTk, binded: bool = False):
    w_show_preferences(MainWindow, binded)


def show_about(MainWindow: ctk.CTk):
    w_show_about(MainWindow)


def show_assistant_chat(MainWindow: ctk.CTk, message=None):
    w_show_ai_assistant(MainWindow, message)


def check_updates(MainWindow: ctk.CTk):
    check_last_version(MainWindow)


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


def check_docs(Window: ctk.CTk or ctk.CTkToplevel):
    from utils.variables import W3_LANGUAGES
    for file_type in W3_LANGUAGES.keys():
        if file_type == Window.current_language:
            webbrowser.open(f'https://www.w3schools.com/{W3_LANGUAGES[file_type]}')
            return None
    webbrowser.open(f'https://www.google.com/search?q={Window.current_language}+file+type')


def color_picker(Window: ctk.CTk or ctk.CTkToplevel, resource_path):
    color_pick = AskColor(title="Choose Color (HEX)")
    color_pick.after(300, lambda: color_pick.iconbitmap(resource_path('assets/xzy-notepad-icon.ico')))
    color = color_pick.get()
    if color is not None:
        text = get_selected_text(Window)
        Window.change_history()
        if text is not None:
            Window.codebox.delete(text['start'], text['end'])
            Window.codebox.insert(text['start'], str(color))
        else:
            Window.codebox.insert("insert", str(color))
        Window.change_history()

__all__ = ["save_settings", "load_settings", "load_previous_settings", "code_window_binder", "close_code_window",
           "code_updated", "insert_tab", "insert_time", "open_file", "save_as_file", "save_file", "start_file",
           "close_window", "get_selected_text", "hash_text", "encode_base", "decode_base", "encode_ascii",
           "decode_ascii", "encode_html", "decode_html", "encode_binary", "decode_binary", "encode_octal",
           "decode_octal", "encode_decimal", "decode_decimal", "encode_hexadecimal", "decode_hexadecimal",
           "convert_value", "new_file", "show_soon", "show_font_families", "show_preferences", "show_about",
           "show_assistant_chat", "check_updates", "convert_into", "check_docs", "color_picker"]

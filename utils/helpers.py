import customtkinter as ctk
import webbrowser
from utils.code_window_manager import cw_binder, cw_close, cw_updated, cw_tab, cw_time, cw_encode_base, cw_decode_base, \
cw_encode_ascii, cw_decode_ascii, cw_encode_binary, cw_decode_binary, cw_encode_octal, cw_decode_octal, cw_encode_decimal, cw_decode_decimal, \
cw_encode_hexadecimal, cw_decode_hexadecimal, cw_encode_html, cw_decode_html, cw_convert_values, cw_hash, cw_get_selected
from utils.updater import check_last_version, download_last_release
from utils.file_manager import f_save, f_save_as, f_open, f_start
from utils.ui_manager import w_close, w_new_file, w_show_soon, w_show_font_families, w_show_preferences, w_show_about
from utils.settings_manager import s_save, s_load, s_previous_load


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


def save_file(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel, full_file_path, auto=False, binded: bool = False):
    f_save(MainWindow, Window, full_file_path, auto, binded)


def start_file(Window: ctk.CTk or ctk.CTkToplevel, full_file_path):
    f_start(Window, full_file_path)


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

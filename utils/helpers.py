import customtkinter as ctk
import webbrowser
from utils.code_window_manager import *
from utils.updater import check_last_version
from utils.file_manager import *
from utils.ui_manager import *
from utils.settings_manager import *
from CTkColorPicker.ctk_color_picker import AskColor
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass
    from ui.new_window import NewWindow as NewWindowClass


def save_settings(MainWindow: "MainWindowClass", file):
    s_save(MainWindow, file)


def load_settings(MainWindow: "MainWindowClass", file, auto_load: bool = False, set_vars: bool = False):
    s_load(MainWindow, file, auto_load, set_vars)


def load_previous_settings(MainWindow: "MainWindowClass"):
    s_previous_load(MainWindow)


def code_window_binder(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_binder(MainWindow, Window)


def close_code_window(Window: Union["MainWindowClass", "NewWindowClass"], all_children: list):
    cw_close(Window, all_children)


def code_updated(Window: Union["MainWindowClass", "NewWindowClass"], MainWindow: "MainWindowClass"):
    cw_updated(Window, MainWindow)


def insert_tab(event, indent_space: int = 4):
    cw_tab(event, indent_space)


def insert_time(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_time(Window)


def open_file(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", "NewWindowClass"], binded: bool = False):
    f_open(MainWindow, Window, binded)
    if binded is True:
        return "break"


def save_as_file(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", "NewWindowClass"],
                 ext: str = "txt", binded: bool = False):
    f_save_as(MainWindow, Window, ext, binded)


def save_file(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", "NewWindowClass"], full_file_path,
              auto: bool = False, binded: bool = False):
    f_save(MainWindow, Window, full_file_path, auto, binded)


def start_file(MainWindow: "MainWindowClass", Window: Union["MainWindowClass", "NewWindowClass"],
               full_file_path, binded: bool = False):
    f_start(MainWindow, Window, full_file_path, binded)


def close_window(Window: Union["MainWindowClass", ctk.CTkToplevel], MainWindow: "MainWindowClass"):
    w_close(Window, MainWindow)


def get_selected_text(Window: Union["MainWindowClass", "NewWindowClass"]):
    return cw_get_selected(Window)


def hash_text(Window: Union["MainWindowClass", "NewWindowClass"], hash_type: str):
    cw_hash(Window, hash_type)


def encode_base(Window: Union["MainWindowClass", "NewWindowClass"], num: int):
    cw_encode_base(Window, num)


def decode_base(Window: Union["MainWindowClass", "NewWindowClass"], num: int):
    cw_decode_base(Window, num)


def encode_ascii(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_ascii(Window)


def decode_ascii(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_ascii(Window)


def encode_html(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_html(Window)


def decode_html(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_html(Window)


def encode_binary(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_binary(Window)


def decode_binary(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_binary(Window)


def encode_octal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_octal(Window)


def decode_octal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_octal(Window)


def encode_decimal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_decimal(Window)


def decode_decimal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_decimal(Window)


def encode_hexadecimal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_encode_hexadecimal(Window)


def decode_hexadecimal(Window: Union["MainWindowClass", "NewWindowClass"]):
    cw_decode_hexadecimal(Window)


def convert_value(Window: Union["MainWindowClass", "NewWindowClass"], FromValue: str, ToValue: str):
    cw_convert_values(Window, FromValue, ToValue)


def new_file(MainWindow: "MainWindowClass", binded: bool = False):
    w_new_file(MainWindow, binded)


def show_soon():
    w_show_soon()


def show_font_families(MainWindow: "MainWindowClass"):
    w_show_font_families(MainWindow)


def show_preferences(MainWindow: "MainWindowClass", binded: bool = False):
    w_show_preferences(MainWindow, binded)


def show_about(MainWindow: "MainWindowClass"):
    w_show_about(MainWindow)


def show_assistant_chat(MainWindow: "MainWindowClass", message: str = None, chats: dict = None):
    w_show_ai_assistant(MainWindow, message, chats)


def check_updates(MainWindow: "MainWindowClass"):
    check_last_version(MainWindow)


def convert_into(value: Union[int, float], converter: str,
                 minimum: Union[int, float] = None, maximum: Union[int, float] = None):
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


def check_docs(Window: Union["MainWindowClass", "NewWindowClass"]):
    from utils.variables import W3_LANGUAGES
    for file_type in W3_LANGUAGES.keys():
        if file_type == Window.current_language:
            webbrowser.open(f'https://www.w3schools.com/{W3_LANGUAGES[file_type]}')
            return None
    webbrowser.open(f'https://www.google.com/search?q={Window.current_language}+file+type')


def color_picker(Window: Union["MainWindowClass", "NewWindowClass"], resource_path):
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

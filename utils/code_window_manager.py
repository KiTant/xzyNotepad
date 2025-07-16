import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from utils.converter import *
from utils.decorators import text_change, text_check
from time import gmtime, strftime
import base64
import html
import hashlib


def on_key_press(event, MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel):
    from utils.helpers import save_file, start_file, open_file, new_file, show_preferences
    if event.char == '\x13': save_file(MainWindow, Window, Window.full_file_path, False, True)  # Ctrl + S
    elif event.char == '\x17': start_file(MainWindow, Window, Window.full_file_path, True)  # Ctrl + W
    elif event.char == '\x10': show_preferences(MainWindow, True)  # Ctrl + P
    elif event.char == '\x0e': new_file(MainWindow, True)  # Ctrl + N
    elif event.char == '\x04' and event.keysym != "d": Window.codebox.text_menu.open_containing_folder(True)  # Ctrl + D
    elif event.char == '\x0f' and event.keysym != "o": open_file(MainWindow, Window, True)  # Ctrl + O
    elif event.char == '\x06': Window.codebox.text_menu.find_replace_text(True)  # Ctrl + F
    elif event.char == '\x15' or event.char == '\x1a': Window.codebox.text_menu.undo_text(True)  # Ctrl + U or Ctrl + Z
    elif event.char == '\x12': Window.codebox.text_menu.redo_text(True)  # Ctrl + R
    elif event.char == '\x18': Window.codebox.text_menu.cut_text(True)  # Ctrl + X
    elif event.char == '\x03': Window.codebox.text_menu.copy_text(True)  # Ctrl + C
    elif event.char == '\x16': Window.codebox.text_menu.paste_text(True)  # Ctrl + V


def cw_binder(MainWindow: ctk.CTk, Window: ctk.CTk or ctk.CTkToplevel):
    from utils.helpers import open_file
    Window.unbind_class("Text", "<<Paste>>")
    Window.unbind_class("Text", "<<Copy>>")
    Window.unbind_class("Text", "<<Cut>>")
    Window.unbind_class("Text", "<<Undo>>")
    Window.unbind_class("Text", "<<Redo>>")
    Window.unbind_class("Text", "<<SelectAll>>")
    Window.codebox.bind("<Control-i>", lambda event: "break")
    Window.codebox.bind("<Control-h>", lambda event: "break")
    Window.codebox.bind("<Control-o>", lambda event: open_file(MainWindow, Window, True))
    Window.codebox.bind("<Control-d>", lambda event: Window.codebox.text_menu.open_containing_folder(True))
    Window.codebox.bind("<Tab>", lambda event: cw_tab(event, MainWindow.settings["indent_space"]))
    Window.codebox.bind("<<Modified>>", lambda event: cw_updated(Window, MainWindow))
    Window.bind("<Key>", lambda event: on_key_press(event, MainWindow, Window))


def cw_close(Window: ctk.CTk or ctk.CTkToplevel, all_children):
    message = None
    main_window = False
    if Window not in all_children:
        main_window = True
        if any(hasattr(window, 'codebox') for window in all_children):
            message = "You sure? Closing main window of xzyNotepad will close all other xzyNotepad windows."
    if not Window.saved:
        message = message + " (and file is not saved)" if message else "You sure? File is not saved."
    if message:
        msg = CTkMessagebox(title="xzyNotepad", message=message, icon="question", options=["Yes", "No"])
        if msg.get() in ["Yes"]:
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


def cw_get_selected(Window: ctk.CTk or ctk.CTkToplevel):
    try:
        start, end = Window.codebox.index("sel.first"), Window.codebox.index("sel.last")
        selected_text = Window.codebox.get(start, end)
        return {"start": start, "end": end, "selected": selected_text}
    except:
        return None


def cw_updated(Window: ctk.CTk or ctk.CTkToplevel, MainWindow: ctk.CTk):
    if not MainWindow.disable_updating_code:
        if Window.full_file_path is not None:
            Window.title(f"xzyNotepad - *{Window.full_file_path.split('/')[-1]}")
        else:
            Window.title(f"xzyNotepad - *New File.{Window.current_language}")
        Window.saved = False


def cw_tab(event, indent_space=4):
    widget = event.widget
    if str(widget)[-18:].strip() == ".!ctkcodebox.!text":
        widget.insert("insert", " " * indent_space)
    return "break"


@text_change
def cw_time(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    if text is not None:
        Window.codebox.delete(text['start'], text['end'])
        Window.codebox.insert(text['start'], str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    else:
        Window.codebox.insert("insert", str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))


@text_check(True)
@text_change
def cw_hash(Window: ctk.CTk or ctk.CTkToplevel, hash_type):
    text = cw_get_selected(Window)
    hashed_text = getattr(hashlib, hash_type)(text['selected'].strip().encode('utf-8')).hexdigest()
    Window.codebox.delete(text['start'], text['end'])
    Window.codebox.insert(text['start'], hashed_text)


@text_check(True)
@text_change
def cw_encode_base(Window: ctk.CTk or ctk.CTkToplevel, num):
    text = cw_get_selected(Window)
    encoded_text = getattr(base64, f"b{num}encode")(text['selected'].strip().encode('utf-8')).decode('utf-8')
    Window.codebox.delete(text['start'], text['end'])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_base(Window: ctk.CTk or ctk.CTkToplevel, num):
    text = cw_get_selected(Window)
    decoded_text = text['selected'].strip()
    try:
        decoded_text = getattr(base64, f"b{num}decode")(text['selected'].strip().encode('utf-8')).decode('utf-8')
    except:
        CTkMessagebox(title="xzyNotepad", message=f"Unexpected error while trying to decode base{num}.",
                      icon="cancel")
    Window.codebox.delete(text['start'], text['end'])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_ascii(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    encoded_text = ""
    ascii_values = [ord(character) for character in text['selected'].strip()]
    for value in ascii_values:
        encoded_text += str(value) + " "
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_ascii(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    chr_values = "nothing"
    try:
        chr_values = [chr(int(character)) for character in text['selected'].strip().rsplit(" ")]
    except:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode ASCII.",
                      icon="cancel")
    decoded_text = ''.join(map(str, chr_values)) if chr_values != "nothing" else text['selected'].strip()
    Window.codebox.delete(text['start'], text['end'])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_binary(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    binary_values = ['{0:08b}'.format(ord(character)) for character in text['selected'].strip()]
    encoded_text = " ".join(binary_values)
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_binary(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    binary_values = "nothing"
    try:
        binary_values = text['selected'].strip().split(" ")
    except:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode binary.",
                      icon="cancel")
    decoded_text = "".join([chr(int(value, 2)) for value in binary_values]) \
        if binary_values != "nothing" else text['selected'].strip()
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_octal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    octal_values = ['{0:03o}'.format(ord(character)) for character in text['selected'].strip()]
    encoded_text = " ".join(octal_values)
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_octal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    octal_values = "nothing"
    try:
        octal_values = text['selected'].strip().split(" ")
    except:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode binary.",
                      icon="cancel")
    decoded_text = "".join([chr(int(value, 8)) for value in octal_values]) \
        if octal_values != "nothing" else text['selected'].strip()
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_decimal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    decimal_values = ['{0:03d}'.format(ord(character)) for character in text['selected'].strip()]
    encoded_text = " ".join(decimal_values)
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_decimal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    decimal_values = "nothing"
    try:
        decimal_values = text['selected'].strip().split(" ")
    except:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode decimal.",
                      icon="cancel")
    decoded_text = "".join([chr(int(value, 10)) for value in decimal_values]) \
        if decimal_values != "nothing" else text['selected'].strip()
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_hexadecimal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    hexadecimal_values = ['{0:02x}'.format(ord(character)) for character in text['selected'].strip()]
    encoded_text = " ".join(hexadecimal_values)
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_hexadecimal(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    hexadecimal_values = "nothing"
    try:
        hexadecimal_values = text['selected'].strip().split(" ")
    except:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode decimal.",
                      icon="cancel")
    decoded_text = "".join([chr(int(value, 16)) for value in hexadecimal_values]) \
        if hexadecimal_values != "nothing" else text['selected'].strip()
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], decoded_text)


@text_check(True)
@text_change
def cw_encode_html(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    encoded_text = html.escape(text['selected'].strip())
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], encoded_text)


@text_check(True)
@text_change
def cw_decode_html(Window: ctk.CTk or ctk.CTkToplevel):
    text = cw_get_selected(Window)
    decoded_text = text['selected'].strip()
    try:
        decoded_text = html.unescape(text['selected'].strip())
    except Exception as err:
        CTkMessagebox(title="xzyNotepad", message="Unexpected error while trying to decode decimal.",
                      icon="cancel")
    Window.codebox.delete(text['start'], text["end"])
    Window.codebox.insert(text['start'], decoded_text)


def cw_convert_values(Window: ctk.CTk or ctk.CTkToplevel, FromValue: str, ToValue: str, Value: str = None):
    selected_text = None
    selected_text_info = cw_get_selected(Window)
    if selected_text_info:
        selected_text = selected_text_info['selected'].strip()
    if Value is not None and Value.strip():
        selected_text = Value.strip()
    if not selected_text:
        if hasattr(ctk, 'CTkMessagebox'):
            ctk.CTkMessagebox(title="xzyNotepad", message="Selected text is not detected.", icon="warning")
        return
    result = None
    error_message = None
    if FromValue == "HEX":
        color_value_stripped = selected_text.lstrip("(").rstrip(")").lstrip("#")
        if not (len(color_value_stripped) == 6 and color_value_stripped.isalnum()):
            error_message = "Invalid HEX format. 6 hexadecimal characters are expected (e.g. FF00FF)."
        else:
            try:
                r, g, b = \
                    int(color_value_stripped[0:2], 16), \
                    int(color_value_stripped[2:4], 16), \
                    int(color_value_stripped[4:6], 16)
                if ToValue == "RGB":
                    result = f"{r}, {g}, {b}"
                elif ToValue == "HSV":
                    result = rgb_to_hsv(r, g, b)
                elif ToValue == "HSL":
                    result = rgb_to_hsl(r, g, b)
                else:
                    error_message = f"Unsupported conversion from HEX to {ToValue}."
            except ValueError:
                error_message = "Error when parsing the HEX value. " \
                                "Make sure that these are correct hexadecimal characters."
    elif FromValue == "RGB":
        color_parts = [p.strip() for p in selected_text.lstrip("(").rstrip(")").split(",")]
        if not (len(color_parts) == 3 and all(p.isdigit() for p in color_parts)):
            error_message = "Incorrect RGB format. 'R, G, B' is expected (e.g. 255, 0, 128)."
        else:
            try:
                r, g, b = int(color_parts[0]), int(color_parts[1]), int(color_parts[2])
                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                    error_message = "RGB values should be in the range from 0 to 255."
                else:
                    if ToValue == "HEX":
                        result = "#{:02x}{:02x}{:02x}".format(r, g, b)
                    elif ToValue == "HSV":
                        result = rgb_to_hsv(r, g, b)
                    elif ToValue == "HSL":
                        result = rgb_to_hsl(r, g, b)
                    else:
                        error_message = f"Unsupported conversion from RGB to {ToValue}."
            except ValueError:
                error_message = "Error when parsing RGB values. Make sure that these are integers."
    elif FromValue == "HSV":
        color_parts = [p.strip() for p in selected_text.lstrip("(").rstrip(")").split(",")]
        if not (len(color_parts) == 3 and all(p.isdigit() for p in color_parts)):
            error_message = "Incorrect HSV format. 'H, S, V' is expected (for example, 0, 100, 100)."
        else:
            try:
                h, s, v = int(color_parts[0]), int(color_parts[1]), int(color_parts[2])
                if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= v <= 100):
                    error_message = "HSV values should be: H (0-360), S (0-100), V (0-100)."
                else:
                    if ToValue == "RGB":
                        result = hsv_to_rgb(h, s, v)
                        if result:
                            result = f"{result[0]}, {result[1]}, {result[2]}"
                    elif ToValue == "HEX":
                        rgb_temp = hsv_to_rgb(h, s, v)
                        if rgb_temp:
                            result = "#{:02x}{:02x}{:02x}".format(rgb_temp[0], rgb_temp[1], rgb_temp[2])
                    elif ToValue == "HSL":
                        rgb_temp = hsv_to_rgb(h, s, v)
                        if rgb_temp:
                            result = rgb_to_hsl(rgb_temp[0], rgb_temp[1], rgb_temp[2])
                    elif ToValue == "HSV":
                        result = f"{h}, {s}, {v}"
                    else:
                        error_message = f"Unsupported conversion from HSV to {ToValue}."
            except ValueError:
                error_message = "Error when parsing HSV values. Make sure that these are integers."
    elif FromValue == "HSL":
        color_parts = [p.strip() for p in selected_text.lstrip("(").rstrip(")").split(",")]
        if not (len(color_parts) == 3 and all(p.isdigit() for p in color_parts)):
            error_message = "Invalid HSL format. 'H, S, L' is expected (for example, 0, 100, 50)."
        else:
            try:
                h, s, l = int(color_parts[0]), int(color_parts[1]), int(color_parts[2])
                if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100):
                    error_message = "The HSL values should be: H (0-360), S (0-100), L (0-100)."
                else:
                    if ToValue == "RGB":
                        result = hsl_to_rgb(h, s, l)
                        if result:
                            result = f"{result[0]}, {result[1]}, {result[2]}"
                    elif ToValue == "HEX":
                        rgb_temp = hsl_to_rgb(h, s, l)
                        if rgb_temp:
                            result = "#{:02x}{:02x}{:02x}".format(rgb_temp[0], rgb_temp[1], rgb_temp[2])
                    elif ToValue == "HSV":
                        rgb_temp = hsl_to_rgb(h, s, l)
                        if rgb_temp:
                            result = rgb_to_hsv(rgb_temp[0], rgb_temp[1], rgb_temp[2])
                    elif ToValue == "HSL":
                        result = f"{h}, {s}, {l}"
                    else:
                        error_message = f"Unsupported conversion from HSL to {ToValue}."
            except ValueError:
                error_message = "Error when parsing HSL values. Make sure that these are integers."
    else:
        error_message = f"Unsupported source format: {FromValue}. Expected to be 'HEX', 'RGB', 'HSV' or 'HSL'."
    if error_message:
        CTkMessagebox(title="xzyNotepad", message=error_message, icon="warning")
    if Value is None and error_message is None:
        if selected_text_info:
            Window.change_history()
            Window.codebox.delete(selected_text_info['start'], selected_text_info["end"])
            Window.codebox.insert(selected_text_info['start'], str(result) if isinstance(result, tuple) else "(" + result + ")")
            Window.change_history()
            Window.codebox.line_nums.redraw()
        else:
            CTkMessagebox(title="xzyNotepad", message="Selected text is not detected.", icon="warning")
    else:
        return result

__all__ = ["cw_binder", "cw_close", "cw_get_selected", "cw_updated", "cw_tab", "cw_time", "cw_hash",
           "cw_encode_base", "cw_decode_base", "cw_encode_ascii", "cw_decode_ascii", "cw_encode_binary",
           "cw_decode_binary", "cw_encode_octal", "cw_decode_octal", "cw_encode_decimal", "cw_decode_decimal",
           "cw_encode_hexadecimal", "cw_decode_hexadecimal", "cw_encode_html", "cw_decode_html", "cw_convert_values"]

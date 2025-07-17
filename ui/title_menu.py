from CTkMenuBar import *
from customtkinter.windows.widgets.theme.theme_manager import ThemeManager
from utils.helpers import *
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass
    from ui.new_window import NewWindow as NewWindowClass


class TitleMenu(CTkTitleMenu):
    def __init__(self, MainWindow: "MainWindowClass", CurrentWindow: Union["MainWindowClass", "NewWindowClass"]): # Union only for python 3.9 (which I use); in 3.10+ it can be like "CurrentWindow: MainWindowClass | NewWindowClass"
        super().__init__(master=CurrentWindow, x_offset=400)

        self.File_Button = self.add_cascade("File")
        self.Edit_Button = self.add_cascade("Edit")
        self.Settings_Button = self.add_cascade("Settings")
        self.About_Button = self.add_cascade("About", command=lambda: show_about(MainWindow))

        self.File_Dropdown = CustomDropdownMenu(widget=self.File_Button,
                                                hover_color=ThemeManager.theme["CTkButton"]["fg_color"])
        self.File_Dropdown.add_option(option="New (Ctrl + N)", command=lambda: new_file(MainWindow))
        self.File_Dropdown.add_option(option="Open (Ctrl + O)", command=lambda: open_file(MainWindow, CurrentWindow))
        self.File_Dropdown.add_option(option="Save (Ctrl + S)",
                                      command=lambda:
                                      save_file(MainWindow, CurrentWindow, CurrentWindow.full_file_path, False))
        self.File_Dropdown.add_option(option="Save as",
                                      command=lambda:
                                      save_as_file(MainWindow, CurrentWindow, CurrentWindow.current_language))
        self.File_Dropdown.add_separator()
        self.File_Dropdown.add_option(option="Start", command=lambda: start_file(MainWindow, CurrentWindow, None))
        self.File_Dropdown.add_option(option="Start (saved file, if exists)",
                                      command=lambda:
                                      start_file(MainWindow, CurrentWindow, CurrentWindow.full_file_path))

        self.Edit_Dropdown = CustomDropdownMenu(widget=self.Edit_Button,
                                                hover_color=ThemeManager.theme["CTkButton"]["fg_color"])
        self.Edit_Dropdown.add_option(option="Chat with AI",
                                      command=lambda: show_assistant_chat(MainWindow, None, MainWindow.last_chats))
        self.Edit_Dropdown.add_option(option="Paste current time", command=lambda: insert_time(CurrentWindow))
        self.Edit_Dropdown.add_option(option="Color picker",
                                      command=lambda: color_picker(CurrentWindow, MainWindow.resource_path))
        self.Edit_Dropdown.add_option(option="Check docs about this file type",
                                      command=lambda: check_docs(CurrentWindow))

        self.Edit_Dropdown.add_separator()
        self.Encoders = self.Edit_Dropdown.add_submenu("Encoders >")
        self.EncodersBase = self.Encoders.add_submenu("Base encoders >")
        self.EncodersBase.add_option(option="Encode to base64", command=lambda: encode_base(CurrentWindow, 64))
        self.EncodersBase.add_option(option="Decode from base64", command=lambda: decode_base(CurrentWindow, 64))
        self.EncodersBase.add_option(option="Encode to base32", command=lambda: encode_base(CurrentWindow, 32))
        self.EncodersBase.add_option(option="Decode from base32", command=lambda: decode_base(CurrentWindow, 32))
        self.EncodersBase.add_option(option="Encode to base16", command=lambda: encode_base(CurrentWindow, 16))
        self.EncodersBase.add_option(option="Decode from base16", command=lambda: decode_base(CurrentWindow, 16))

        self.EncodersNumeral = self.Encoders.add_submenu("Numeral systems encoders >")
        self.EncodersNumeral.add_option(option="Encode to binary code", command=lambda: encode_binary(CurrentWindow))
        self.EncodersNumeral.add_option(option="Decode from binary code", command=lambda: decode_binary(CurrentWindow))
        self.EncodersNumeral.add_option(option="Encode to octal code", command=lambda: encode_octal(CurrentWindow))
        self.EncodersNumeral.add_option(option="Decode from octal code", command=lambda: decode_octal(CurrentWindow))
        self.EncodersNumeral.add_option(option="Encode to decimal code", command=lambda: encode_decimal(CurrentWindow))
        self.EncodersNumeral.add_option(option="Decode from decimal code",
                                        command=lambda: decode_decimal(CurrentWindow))
        self.EncodersNumeral.add_option(option="Encode to hexadecimal code",
                                        command=lambda: encode_hexadecimal(CurrentWindow))
        self.EncodersNumeral.add_option(option="Decode from hexadecimal code",
                                        command=lambda: decode_hexadecimal(CurrentWindow))
        self.Encoders.add_option(option="Encode to ASCII", command=lambda: encode_ascii(CurrentWindow))
        self.Encoders.add_option(option="Decode from ASCII", command=lambda: decode_ascii(CurrentWindow))
        self.Encoders.add_option(option="Encode to HTML entities", command=lambda: encode_html(CurrentWindow))
        self.Encoders.add_option(option="Decode from HTML entities", command=lambda: decode_html(CurrentWindow))

        self.Converters = self.Edit_Dropdown.add_submenu("Converters >")
        self.ConvertersHEX = self.Converters.add_submenu("From HEX Converter >")
        self.ConvertersHEX.add_option(option="To RGB", command=lambda: convert_value(CurrentWindow, "HEX", "RGB"))
        self.ConvertersHEX.add_option(option="To HSV", command=lambda: convert_value(CurrentWindow, "HEX", "HSV"))
        self.ConvertersHEX.add_option(option="To HSL", command=lambda: convert_value(CurrentWindow, "HEX", "HSL"))
        self.ConvertersRGB = self.Converters.add_submenu("From RGB Converter >")
        self.ConvertersRGB.add_option(option="To HEX", command=lambda: convert_value(CurrentWindow, "RGB", "HEX"))
        self.ConvertersRGB.add_option(option="To HSV", command=lambda: convert_value(CurrentWindow, "RGB", "HSV"))
        self.ConvertersRGB.add_option(option="To HSL", command=lambda: convert_value(CurrentWindow, "RGB", "HSL"))
        self.ConvertersHSV = self.Converters.add_submenu("From HSV Converter >")
        self.ConvertersHSV.add_option(option="To HEX", command=lambda: convert_value(CurrentWindow, "HSV", "HEX"))
        self.ConvertersHSV.add_option(option="To RGB", command=lambda: convert_value(CurrentWindow, "HSV", "RGB"))
        self.ConvertersHSV.add_option(option="To HSL", command=lambda: convert_value(CurrentWindow, "HSV", "HSL"))
        self.ConvertersHSL = self.Converters.add_submenu("From HSL Converter >")
        self.ConvertersHSL.add_option(option="To HEX", command=lambda: convert_value(CurrentWindow, "HSL", "HEX"))
        self.ConvertersHSL.add_option(option="To RGB", command=lambda: convert_value(CurrentWindow, "HSL", "RGB"))
        self.ConvertersHSL.add_option(option="To HSV", command=lambda: convert_value(CurrentWindow, "HSL", "HSV"))

        self.Hashers = self.Edit_Dropdown.add_submenu("Hashers >")
        self.Hashers.add_option(option="Hash to MD5", command=lambda: hash_text(CurrentWindow, "md5"))
        self.HashersSHA = self.Hashers.add_submenu("SHA hashers >")
        self.HashersSHA.add_option(option="Hash to SHA1", command=lambda: hash_text(CurrentWindow, "sha1"))
        self.HashersSHA.add_option(option="Hash to SHA224", command=lambda: hash_text(CurrentWindow, "sha224"))
        self.HashersSHA.add_option(option="Hash to SHA256", command=lambda: hash_text(CurrentWindow, "sha256"))
        self.HashersSHA.add_option(option="Hash to SHA384", command=lambda: hash_text(CurrentWindow, "sha384"))
        self.HashersSHA.add_option(option="Hash to SHA512", command=lambda: hash_text(CurrentWindow, "sha512"))
        self.HashersSHA3 = self.Hashers.add_submenu("SHA3 hashers >")
        self.HashersSHA3.add_option(option="Hash to SHA3_224", command=lambda: hash_text(CurrentWindow, "sha3_224"))
        self.HashersSHA3.add_option(option="Hash to SHA3_256", command=lambda: hash_text(CurrentWindow, "sha3_256"))
        self.HashersSHA3.add_option(option="Hash to SHA3_384", command=lambda: hash_text(CurrentWindow, "sha3_384"))
        self.HashersSHA3.add_option(option="Hash to SHA3_512", command=lambda: hash_text(CurrentWindow, "sha3_512"))

        self.Settings_Dropdown = CustomDropdownMenu(widget=self.Settings_Button,
                                                    hover_color=ThemeManager.theme["CTkButton"]["fg_color"])
        self.Settings_Dropdown.add_option(option="Preferences (Ctrl + P)", command=lambda: show_preferences(MainWindow))
        self.Settings_Dropdown.add_option(option="Load settings",
                                          command=lambda:
                                          load_settings(MainWindow, MainWindow.settings_file, set_vars=True))
        self.Settings_Dropdown.add_option(option="Save settings",
                                          command=lambda: save_settings(MainWindow, MainWindow.settings_file))
        self.Settings_Dropdown.add_option(option="Check updates (Ctrl + U)", command=lambda: check_updates(MainWindow))

        self.after(100, self.change_dimension)

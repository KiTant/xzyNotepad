import customtkinter as ctk
import os
from ui.main_window import MainWindow


def resource_path(file):
    data_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(data_dir, file)

appdata_dir = os.getenv('APPDATA')
settings_file = os.path.join(appdata_dir, 'xzyNotepad', 'settings.json')
previous_settings_file = os.path.join(appdata_dir, 'xzyNotepad', 'previous_settings.json')

ctk.set_appearance_mode("dark")
try: ctk.set_default_color_theme(resource_path('yellow.json'))
except: ctk.set_default_color_theme('assets/yellow.json')

if __name__ == '__main__':
    app = MainWindow(resource_path=resource_path, settings_file=settings_file, previous_settings_file=previous_settings_file)
    app.mainloop()

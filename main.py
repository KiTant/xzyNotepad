import customtkinter as ctk
import os
from ui.main_window import MainWindow


def resource_path(file):
    data_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(data_dir, file)

ctk.set_appearance_mode("dark")
try: ctk.set_default_color_theme(resource_path('yellow.json'))
except: ctk.set_default_color_theme('assets/yellow.json')

if __name__ == '__main__':
    app = MainWindow(resource_path=resource_path)
    app.mainloop()

from tkinter import font
from tkinter import Tk
import customtkinter as ctk
from utils.helpers import close_window


def show_font_families(app):
    listnumber = 1
    for i, item in enumerate(app.fonts):
        label = ctk.CTkLabel(app.frame, text=item, font=(item, 16))
        label.grid(row=i)
        label.bind("<Button-1>", lambda e, item=item: [app.clipboard_clear(), app.clipboard_append(item)])
        listnumber += 1


def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


class FontsWindow(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path):
        super().__init__()
        self.title("Font Families")
        self.geometry("250x400")
        self.resizable(False, False)
        self.MainWindow = MainWindow
        try: self.iconbitmap(resource_path('assets/xzy-notepad-icon.ico'))
        except: self.iconbitmap('assets/xzy-notepad-icon.ico')

        self.root = Tk()
        self.root.withdraw()

        self.fonts = list(font.families())
        self.fonts.sort()

        self._initialize_components()

    def _initialize_components(self):
        self.canvas = ctk.CTkCanvas(self, bg="black", highlightbackground="black")
        self.frame = ctk.CTkFrame(self.canvas)
        self.vsb = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw")

        self.MainWindow.all_children.append(self)

        self.frame.bind("<Configure>", lambda event, canvas=self.canvas: on_frame_configure(self.canvas))

        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self, self.MainWindow))

        show_font_families(self)

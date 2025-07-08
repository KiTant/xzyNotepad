import customtkinter
import os
import tkinter
import webbrowser
from CTkMessagebox import CTkMessagebox
from ui.find_window import SearchWindow
from utils.helpers import show_soon, get_selected_text
import pyperclip

class TextMenu(tkinter.Menu):
    def __init__(self, Window, MainWindow, fg_color=None, text_color=None, hover_color=None, **kwargs):
        super().__init__(tearoff=False, title="menu", borderwidth=0, bd=0, relief="flat", **kwargs)

        self.fg_color = customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"] if fg_color is None else fg_color
        self.text_color = customtkinter.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.hover_color = customtkinter.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else hover_color

        self.Window = Window
        self.MainWindow = MainWindow
        self.FindWindow = None
        self.file_path = MainWindow.full_file_path

        self.add_command(label="Undo", command=self.undo_text)
        self.add_command(label="Redo", command=self.redo_text)
        self.add_command(label="Clear history", command=self.clear_history)
        self.add_separator()
        self.add_command(label="Cut", command=self.cut_text)
        self.add_command(label="Copy", command=self.copy_text)
        self.add_command(label="Paste", command=self.paste_text)
        self.add_separator()
        self.add_command(label="Find & Replace...", command=self.find_replace_text)
        self.add_separator()
        self.add_command(label="Select All", command=self.select_all_text)
        self.add_command(label="Clear All", command=self.clear_all_text)
        self.add_separator()
        self.add_command(label="Open Containing Folder", command=self.open_containing_folder)
        self.add_command(label="Search in Browser", command=self.search_in_browser)
        self.add_command(label="Ask with AI (Soon)", command=show_soon)

        self.Window.bind("<Button-3>", lambda event: self.do_popup(event))
        self.Window.bind("<Button-2>", lambda event: self.do_popup(event))

    def do_popup(self, event):
        super().config(bg=self.Window.codebox._apply_appearance_mode(self.fg_color),
                       fg=self.Window.codebox._apply_appearance_mode(self.text_color),
                       activebackground=self.Window.codebox._apply_appearance_mode(self.hover_color))
        self.tk_popup(event.x_root+10, event.y_root+5)

    def cut_text(self):
        self.copy_text()
        try:
            self.Window.change_history()
            self.Window.codebox.delete(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            self.Window.change_history()
            self.Window.codebox.line_nums.redraw()
        except tkinter.TclError:
            pass

    def copy_text(self):
        try:
            pyperclip.copy(self.Window.codebox.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))
        except tkinter.TclError:
            pass

    def paste_text(self):
        text = get_selected_text(self.Window)
        try:
            self.Window.change_history()
            if text is None:
                self.Window.codebox.insert(self.Window.codebox.index('insert'), pyperclip.paste())
            else:
                self.Window.codebox.delete(text['start'], text['end'])
                self.Window.codebox.insert(text['start'], pyperclip.paste())
            self.Window.change_history()
            self.Window.codebox.line_nums.redraw()
        except tkinter.TclError:
            pass

    def clear_all_text(self):
        try:
            self.Window.change_history()
            self.Window.codebox.delete(0.0, "end")
            self.Window.change_history()
            self.Window.codebox.line_nums.redraw()
        except tkinter.TclError:
            pass

    def select_all_text(self):
        try:
            self.Window.codebox.tag_add("sel", "0.0", "end")
        except tkinter.TclError:
            pass

    def undo_text(self):
        try:
            if self.Window.history_index > 0:
                self.Window.history_index -= 1
                prev_text = self.Window.history[self.Window.history_index]
                self.Window.codebox.delete(0.0, "end")
                self.Window.codebox.insert(0.0, prev_text)
                self.Window.codebox.see("end")
                self.Window.codebox.line_nums.redraw()
            elif self.Window.history_index == 0 and self.Window.codebox.get(0.0, "end")[:-1] != self.Window.history[0]:
                self.Window.change_history()
                self.Window.history_index -= 1
                self.Window.codebox.delete(0.0, "end")
                self.Window.codebox.insert(0.0, self.Window.history[0])
                self.Window.codebox.see("end")
                self.Window.codebox.line_nums.redraw()
            else:
                CTkMessagebox(title="xzyNotepad", message=f"Error during undo: There is nothing to undo", icon="warning")
        except tkinter.TclError as e:
            CTkMessagebox(title="xzyNotepad", message=f"Error during undo: {e}", icon="warning")

    def redo_text(self):
        try:
            if self.Window.history_index < len(self.Window.history) - 1:
                self.Window.history_index += 1
                next_text = self.Window.history[self.Window.history_index]
                self.Window.codebox.delete(0.0, "end")
                self.Window.codebox.insert(0.0, next_text)
                self.Window.codebox.see("end")
                self.Window.codebox.line_nums.redraw()
            else:
                CTkMessagebox(title="xzyNotepad", message=f"Error during redo: There is nothing to redo", icon="warning")
        except tkinter.TclError as e:
            CTkMessagebox(title="xzyNotepad", message=f"Error during redo: {e}", icon="warning")

    def clear_history(self):
        self.Window.history = [self.Window.codebox.get(0.0, "end")[:-1]]
        self.Window.history_index = 0

    def find_replace_text(self):
        for window in self.MainWindow.all_children + [self.MainWindow]:
            if hasattr(window, 'codebox'):
                self.MainWindow.all_titles_menu.remove(window.menu)
                window.menu.destroy()
                window.menu = None
        self.FindWindow = SearchWindow(master=self.Window, TextboxWidget=self.Window.codebox, MainWindow=self.MainWindow)

    def open_containing_folder(self):
        self.file_path = self.MainWindow.full_file_path
        if self.file_path and os.path.exists(self.file_path):
            folder_path = os.path.dirname(self.file_path)
            if os.path.isdir(folder_path):
                try:
                    os.startfile(folder_path)
                except Exception as e:
                    CTkMessagebox(title="xzyNotepad", message=f"Error opening folder: {e}", icon="warning")
            else:
                CTkMessagebox(title="xzyNotepad", message=f"Path is not a directory: {folder_path}", icon="cancel")
        else:
            CTkMessagebox(title="xzyNotepad", message=f"File path not set or file does not exist. Cannot open containing folder", icon="warning")

    def search_in_browser(self):
        try:
            selected_text = self.Window.codebox.get(tkinter.SEL_FIRST, tkinter.SEL_LAST)
            if selected_text:
                webbrowser.open_new_tab(f"https://www.google.com/search?q={selected_text}")
            else:
                CTkMessagebox(title="xzyNotepad", message="Selected text is not detected.", icon="warning")
        except tkinter.TclError:
            CTkMessagebox(title="xzyNotepad", message="Selected text is not detected.", icon="warning")

    def ask_with_ai(self):
        return
        # Soon

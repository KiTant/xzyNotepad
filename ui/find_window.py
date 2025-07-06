import customtkinter
import re
import tkinter
from CTkMessagebox import CTkMessagebox
from customtkinter.windows.widgets.appearance_mode import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling import CTkScalingBaseClass


class SearchWindow(customtkinter.CTkToplevel):
    def __init__(self, master, TextboxWidget, MainWindow):
        super().__init__(master)
        self.title("Find and Replace")
        self.geometry("750x300")
        self.minsize(500, 300)
        self.maxsize(1350, 350)
        self.transient(master)
        self.grab_set()

        self.MainWindow = MainWindow
        self.Window = master
        self.textbox = TextboxWidget
        self.last_search_index = "1.0"  # To track the last found location
        self.search_direction = "forward"  # 'forward' or 'backward'

        self.search_frame = customtkinter.CTkFrame(self)
        self.search_frame.pack(pady=10, padx=10, fill="x")

        self.search_label = customtkinter.CTkLabel(self.search_frame, text="Find:")
        self.search_label.pack(side="left", padx=(0, 5))
        self.search_entry = customtkinter.CTkEntry(self.search_frame, placeholder_text="Enter text to search")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda event: self.find_next())

        self.find_next_button = customtkinter.CTkButton(self.search_frame, text="Find Next", command=self.find_next)
        self.find_next_button.pack(side="right", padx=(5, 5))
        self.find_prev_button = customtkinter.CTkButton(self.search_frame, text="Find Previous", command=self.find_previous)
        self.find_prev_button.pack(side="right")

        self.replace_frame = customtkinter.CTkFrame(self)
        self.replace_frame.pack(pady=5, padx=10, fill="x")

        self.replace_label = customtkinter.CTkLabel(self.replace_frame, text="Replace with:")
        self.replace_label.pack(side="left", padx=(0, 5))
        self.replace_entry = customtkinter.CTkEntry(self.replace_frame, placeholder_text="Enter replacement text")
        self.replace_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.replace_button = customtkinter.CTkButton(self.replace_frame, text="Replace", command=self.replace_one)
        self.replace_button.pack(side="right", padx=(0, 5))
        self.replace_all_button = customtkinter.CTkButton(self.replace_frame, text="Replace All", command=self.replace_all)
        self.replace_all_button.pack(side="right", padx=(5, 5))

        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.pack(pady=5, padx=10, fill="x")

        self.case_sensitive_var = customtkinter.BooleanVar(value=False)
        self.case_sensitive_checkbox = customtkinter.CTkCheckBox(self.options_frame, text="Match Case", variable=self.case_sensitive_var)
        self.case_sensitive_checkbox.pack(side="left", padx=(0, 10))

        self.clear_highlight_button = customtkinter.CTkButton(self.options_frame, text="Clear Highlights", command=self.clear_highlights)
        self.clear_highlight_button.pack(side="right", padx=(0, 75))

        self.close_button = customtkinter.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self._text_widget_for_tagging = self._get_text_widget_for_tagging()
        if self._text_widget_for_tagging:
            self._text_widget_for_tagging.tag_configure("found", background="yellow", foreground="black")
            self._text_widget_for_tagging.tag_raise("found")
        else:
            CTkMessagebox(title="xzyNotepad", message=f"Cannot configure 'found' tag. "
                                                      f"The provided textbox_widget (CTkCodeBox) does not "
                                                      f"expose a standard Tkinter Text widget for tagging.", icon="warning")

    def _get_text_widget_for_tagging(self):
        """
        Attempts to get the underlying Tkinter Text widget from the provided textbox_widget
        for tagging operations. This handles cases where custom widgets like CTkCodeBox
        might wrap a standard Text widget.
        """
        # Try the widget directly (if it's a CTkTextbox or tkinter.Text)
        if hasattr(self.textbox, 'tag_configure') and callable(getattr(self.textbox, 'tag_configure')):
            return self.textbox
        # Try common internal names for wrapped Text widgets
        if hasattr(self.textbox, '_textbox') and hasattr(self.textbox._textbox, 'tag_configure'):
            return self.textbox._textbox
        if hasattr(self.textbox, '_text_widget') and hasattr(self.textbox._text_widget, 'tag_configure'):
            return self.textbox._text_widget
        if hasattr(self.textbox, 'text_widget') and hasattr(self.textbox.text_widget, 'tag_configure'):
            return self.textbox.text_widget

        return None

    def find_text(self, direction):
        search_term = self.search_entry.get()
        if not search_term:
            return
        text_widget = self._text_widget_for_tagging
        if not text_widget:
            CTkMessagebox(title="xzyNotepad", message=f"Text widget not available for search/highlighting.", icon="cancel")
            return
        self.clear_highlights()
        start_index = self.last_search_index
        if direction == "backward":
            if self.last_search_index == "1.0":  # If at start, wrap around to end for backward search
                start_index = "end"
            else:
                # Adjust start_index for backward search to prevent re-finding the current match
                start_index = text_widget.index(f"{self.last_search_index}-{len(search_term)}c")

        end_index = "end" if direction == "forward" else "1.0"
        # Construct search pattern based on options
        pattern = re.escape(search_term)  # Escape special regex characters
        # Search text
        pos = text_widget.search(
            pattern,
            start_index,
            stopindex=end_index,
            nocase=not self.case_sensitive_var.get(),
            forwards=direction == "forward",
            backwards=direction == "backward",
            elide=False,
            count=None
        )
        if pos:
            start = pos
            # For regex matches, the length might differ from search_term if it includes word boundaries
            # We need to find the actual end of the matched string
            match_obj = re.search(pattern, text_widget.get(start, "end"),
                                  re.IGNORECASE if not self.case_sensitive_var.get() else 0)
            if match_obj:
                match_length = len(match_obj.group(0))
                end = f"{pos}+{match_length}c"
            else:
                end = f"{pos}+{len(search_term)}c"  # Fallback if regex match object not found
            text_widget.tag_add("found", start, end)
            text_widget.see(start)  # Scroll to the found text
            self.last_search_index = end if direction == "forward" else start  # Update index for next search
            self.search_direction = direction  # Save direction
        else:
            # Reset index to start/end of document for next search attempt
            self.last_search_index = "1.0" if direction == "forward" else "end"

    def clear_highlights(self):
        text_widget = self._text_widget_for_tagging
        if text_widget:
            text_widget.tag_remove("found", "1.0", "end")

    def find_next(self):
        self.find_text("forward")

    def find_previous(self):
        self.find_text("backward")

    def replace_one(self):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        if not search_term:
            return
        text_widget = self._text_widget_for_tagging
        if not text_widget:
            CTkMessagebox(title="xzyNotepad", message=f"Text widget not available for replacement.", icon="cancel")
            return
        # Check if there is a current highlight from search
        if text_widget.tag_ranges("found"):
            self.Window.change_history()
            start, end = text_widget.tag_ranges("found")
            text_widget.delete(start, end)
            text_widget.insert(start, replace_term)
            self.clear_highlights()  # Remove highlight after replacement
            self.Window.change_history()
            # Search for the next occurrence after replacement
            self.find_next()
        else:
            CTkMessagebox(title="xzyNotepad", message=f"No highlighted text to replace. Use 'Find' first.", icon="warning")

    def replace_all(self):
        search_term = self.search_entry.get()
        replace_term = self.replace_entry.get()
        if not search_term:
            return
        text_widget = self._text_widget_for_tagging
        if not text_widget:
            CTkMessagebox(title="xzyNotepad", message=f"Text widget not available for replacement.", icon="cancel")
            return
        self.Window.change_history()
        self.clear_highlights()
        pattern = re.escape(search_term)  # Escape special regex characters
        flags = 0
        if not self.case_sensitive_var.get():
            flags |= re.IGNORECASE
        count = 0
        start_index = "1.0"
        while True:
            pos = text_widget.search(
                pattern,
                start_index,
                stopindex="end",
                nocase=not self.case_sensitive_var.get(),
                forwards=True,
                count=None
            )
            if not pos:
                break
            start = pos
            # Find the actual length of the matched regex pattern
            full_text = text_widget.get(start, "end")
            match_obj = re.match(pattern, full_text, flags)
            if match_obj:
                match_length = len(match_obj.group(0))
                end = f"{pos}+{match_length}c"
            else:
                end = f"{pos}+{len(search_term)}c"  # Fallback
            text_widget.delete(start, end)
            text_widget.insert(start, replace_term)
            count += 1
            # Update start_index to continue search after the inserted text
            start_index = text_widget.index(f"{start}+{len(replace_term)}c")
        CTkMessagebox(title="xzyNotepad", message=f"Replaced {count} occurrences.", icon="info")
        self.Window.change_history()

    def destroy(self):
        tkinter.Toplevel.destroy(self)
        CTkAppearanceModeBaseClass.destroy(self)
        CTkScalingBaseClass.destroy(self)
        from ui.title_menu import TitleMenu
        for window in self.MainWindow.all_children + [self.MainWindow]:
            if hasattr(window, 'codebox'):
                window.menu = TitleMenu(self.MainWindow, window)
                self.MainWindow.all_titles_menu.append(window.menu)

import customtkinter as ctk
from g4f import ChatCompletion
import threading
import json
from tkinter import filedialog
import tkinter
from utils.variables import MODEL_MAP
from utils.helpers import close_window
import pyperclip
from CTkMessagebox import CTkMessagebox


class AssistantChatApp(ctk.CTkToplevel):
    def __init__(self, MainWindow: ctk.CTk, resource_path, question=None):
        super().__init__()
        self.MainWindow = MainWindow
        self.title("AI Chat")
        self.geometry("800x700")
        self.after(300, lambda: self.iconbitmap(self.resource_path('assets/xzy-notepad-icon.ico')))

        self.minsize(700, 500)

        self.resource_path = resource_path

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.chat_list_frame = ctk.CTkFrame(self, width=200)
        self.chat_list_frame.grid(row=0, column=0, rowspan=3, padx=(10, 5), pady=10, sticky="nsew")
        self.chat_list_frame.grid_rowconfigure(1, weight=1)
        self.chat_list_frame.grid_rowconfigure(5, weight=1)

        self.chat_list_label = ctk.CTkLabel(self.chat_list_frame, text="Chats", font=ctk.CTkFont(size=16, weight="bold"))
        self.chat_list_label.grid(row=0, column=0, padx=10, pady=10)

        self.chat_listbox = ctk.CTkOptionMenu(self.chat_list_frame, values=["Default Chat"], command=self.switch_chat)
        self.chat_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="new")
        self.current_chat_name = "Default Chat"

        self.new_chat_button = ctk.CTkButton(self.chat_list_frame, text="New chat", command=self.create_new_chat)
        self.new_chat_button.grid(row=2, column=0, padx=10, pady=5, sticky="s")

        self.export_button = ctk.CTkButton(self.chat_list_frame, text="Export chats", command=self.export_chats)
        self.export_button.grid(row=3, column=0, padx=10, pady=5, sticky="s")

        self.import_button = ctk.CTkButton(self.chat_list_frame, text="Import chats", command=self.import_chats)
        self.import_button.grid(row=4, column=0, padx=10, pady=5, sticky="s")

        self.chat_panel = ctk.CTkFrame(self)
        self.chat_panel.grid(row=0, column=1, rowspan=3, padx=(5, 10), pady=10, sticky="nsew")
        self.chat_panel.grid_columnconfigure(0, weight=1)
        self.chat_panel.grid_rowconfigure(1, weight=1)

        self.settings_frame = ctk.CTkFrame(self.chat_panel)
        self.settings_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="new")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        self.model_label = ctk.CTkLabel(self.settings_frame, text="Choose model:")
        self.model_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.model_combobox = ctk.CTkComboBox(self.settings_frame, values=list(MODEL_MAP.keys()), state="readonly")
        self.model_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        default_model_name = list(MODEL_MAP.keys())[0] if MODEL_MAP else ""
        self.model_combobox.set(default_model_name)

        self.chat_display = ctk.CTkScrollableFrame(self.chat_panel, fg_color="transparent")
        self.chat_display.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.chat_display.grid_columnconfigure(0, weight=1)
        self.chat_display.grid_columnconfigure(1, weight=1)

        self.chat_display.bind("<Configure>", self.update_scroll_region)
        self.message_row_index = 0

        self.input_frame = ctk.CTkFrame(self.chat_panel)
        self.input_frame.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="sew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)

        self.message_textbox = ctk.CTkTextbox(self.input_frame, wrap="word", height=80)
        self.message_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.message_textbox.bind("<Return>", self.send_message)
        self.message_textbox.bind("<Shift-Return>", lambda event: self.message_textbox.insert("insert", ""))

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=3, padx=10, pady=10, sticky="se")

        self.chats = {"Default Chat": []}
        self.message_history = self.chats[self.current_chat_name]

        self.message_context_menu = tkinter.Menu(self, tearoff=0)
        self.message_to_edit = None

        self.MainWindow.all_children.append(self)

        self.protocol("WM_DELETE_WINDOW", lambda: close_window(self, self.MainWindow))

        self.after(100, lambda: self.focus_set())

        if question is not None:
            self.send_message(message=question)

    def send_message(self, event=None, message=None):
        user_message = self.message_textbox.get("1.0", "end-1c") if message is None else message

        if not user_message.strip():
            return

        selected_model_name = self.model_combobox.get()
        selected_model_info = MODEL_MAP.get(selected_model_name)

        if not selected_model_info:
            self.display_message({"role": "bot",
                                  "content": f"Error: Model '{selected_model_name}' not found or not supporting.",
                                  "model_name": "xzyNotepad"}, "bot")
            self.unlock_input()
            return

        selected_model, selected_provider = selected_model_info

        user_message_data = {"role": "user", "content": user_message, "is_edited": False, "model_name": "User"}

        self.display_message(user_message_data, "user")

        self.message_history.append(user_message_data)

        self.message_textbox.delete("1.0", ctk.END)

        self.message_textbox.configure(state="disabled")
        self.send_button.configure(state="disabled", text="Thinking...")
        self.model_combobox.configure(state="disabled")
        self.export_button.configure(state="disabled")
        self.import_button.configure(state="disabled")
        self.chat_listbox.configure(state="disabled")
        self.new_chat_button.configure(state="disabled")

        threading.Thread(
            target=self.get_ai_response,
            args=(self.message_history.copy(), selected_model, selected_provider, selected_model_name),
            daemon=True
        ).start()

    def get_ai_response(self, conversation_history, model, provider=None, model_name="AI"):
        try:
            clean_history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history]
            response = ChatCompletion.create(model=model, messages=clean_history, provider=provider, stream=False)
            ai_response = response if isinstance(response, str) else str(response)
            ai_response_data = {"role": "assistant", "content": ai_response, "is_edited": False,
                                "type": "text", "model_name": model_name}
        except Exception as e:
            ai_response_data = {"role": "bot",
                                "content": f"Error while trying to get answer from AI:"
                                           f" {e}\nTry to choose other model or try to launch VPN.", "is_edited": False,
                                "type": "text", "model_name": model_name}
        self.after(0, self.display_ai_response, ai_response_data)

    def display_message(self, message_data, sender):
        msg_frame = ctk.CTkFrame(self.chat_display, fg_color="transparent")

        column = 1 if sender == "user" else 0
        sender_name = "User" if sender == "user" else message_data.get("model_name", "AI")
        msg_frame.grid_columnconfigure(1, weight=0)
        content_padx = (0, 5) if sender == "user" else (5, 0)
        name_sticky = "e" if sender == "user" else "w"
        frame_sticky = "e" if sender == "user" else "w"

        msg_frame.grid(row=self.message_row_index, column=column, padx=5, pady=5, sticky=frame_sticky)

        self.message_row_index += 1

        sender_label = ctk.CTkLabel(msg_frame, text=sender_name, font=ctk.CTkFont(weight="bold"))
        sender_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(0, 2), sticky=name_sticky)

        text_widget = ctk.CTkTextbox(msg_frame, wrap="word", activate_scrollbars=False)
        text_widget.insert("0.0", message_data["content"])
        text_widget.configure(state="disabled")

        text_widget.bind("<Button-3>", lambda event, msg_data=message_data: self.on_message_right_click(event, msg_data))

        def on_text_scroll(event):
            view_fraction = text_widget.yview()
            if view_fraction == (0.0, 1.0):
                return
            elif event.delta > 0 and view_fraction[0] == 0.0:
                return
            elif event.delta < 0 and view_fraction[1] == 1.0:
                return
            else:
                text_widget.yview_scroll(-1 * event.delta // 120, "units")
                return "break"
        text_widget.bind("<MouseWheel>", on_text_scroll)
        text_widget.bind("<Button-4>", on_text_scroll)
        text_widget.bind("<Button-5>", on_text_scroll)

        text_widget.grid(row=1, column=0 if sender == "user" else 1, padx=content_padx, pady=0, sticky="nsew")

        self.chat_display.update_idletasks()
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def on_message_right_click(self, event, message_data):
        self.message_context_menu.delete(0, "end")

        self.message_to_edit = message_data

        self.message_context_menu.add_command(label="Delete", command=lambda: self.delete_message(message_data))
        if message_data["role"] == "assistant":
            try:
                message_index = self.message_history.index(message_data)
                if message_index > 0 and self.message_history[message_index - 1]["role"] == "user":
                    self.message_context_menu.add_command(label="Regenerate the response",
                                                          command=lambda: self.regenerate_response(message_data))
            except ValueError:
                pass
        elif message_data["role"] == "user":
            if message_data.get("type") == "text":
                self.message_context_menu.add_command(label="Edit", command=self.open_edit_copy_window)
        self.message_context_menu.add_command(label="Copy text",
                                              command=lambda: self.copy_text_to_clipboard(message_data["content"]))
        try:
            self.message_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.message_context_menu.grab_release()

    @staticmethod
    def copy_text_to_clipboard(text_to_copy):
        if text_to_copy:
            try:
                pyperclip.copy(text_to_copy)
            except Exception as e:
                pass

    def open_edit_copy_window(self):
        if self.message_to_edit is None:
            return

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Edit message")
        edit_window.geometry("500x400")
        edit_window.transient(self)

        edit_window.grid_columnconfigure(0, weight=1)
        edit_window.grid_rowconfigure(0, weight=1)

        edit_textbox = ctk.CTkTextbox(edit_window, wrap="word")
        edit_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        edit_textbox.insert("0.0", self.message_to_edit["content"])

        button_frame = ctk.CTkFrame(edit_window, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)

        save_button = ctk.CTkButton(button_frame, text="Save",
                                    command=lambda: self.save_edited_message(edit_textbox, edit_window))
        save_button.grid(row=0, column=0, padx=(0, 5), sticky="e")

        copy_button = ctk.CTkButton(button_frame, text="Copy all",
                                    command=lambda: self.copy_text_from_edit_window(edit_textbox))
        copy_button.grid(row=0, column=1, padx=(5, 0), sticky="e")

    def save_edited_message(self, edit_textbox, edit_window):
        if self.message_to_edit is not None:
            new_text = edit_textbox.get("1.0", "end-1c")
            self.message_to_edit["content"] = new_text
            self.message_to_edit["is_edited"] = True
            self.redraw_chat()
        edit_window.destroy()
        self.message_to_edit = None

    @staticmethod
    def copy_text_from_edit_window(edit_textbox):
        text_to_copy = edit_textbox.get("1.0", "end-1c")
        if text_to_copy:
            try:
                pyperclip.copy(text_to_copy)
            except Exception as e:
                pass

    def delete_message(self, message_data_to_delete):
        try:
            self.message_history.remove(message_data_to_delete)
            self.redraw_chat()
        except ValueError:
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during deleting message: Message not found in history", icon="warning")
        except Exception as e:
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during deleting: {e}", icon="cancel")

    def regenerate_response(self, ai_message_data):
        try:
            ai_index = self.message_history.index(ai_message_data)
            if ai_index > 0 and self.message_history[ai_index - 1]["role"] == "user":
                del self.message_history[ai_index]
                self.redraw_chat()

                selected_model_name = self.model_combobox.get()
                selected_model_info = MODEL_MAP.get(selected_model_name)
                if not selected_model_info:
                    self.display_message({"role": "bot",
                                          "content": f'Error: Model "{selected_model_name}" '
                                                     f'not found or it is not supported for regenerating answer.',
                                          "type": "text", "model_name": "System"}, "bot")
                    self.unlock_input()
                    return
                selected_model, selected_provider = selected_model_info

                threading.Thread(
                    target=self.get_ai_response,
                    args=(self.message_history[:ai_index].copy(), selected_model, selected_provider, selected_model_name),
                    daemon=True
                ).start()

                self.message_textbox.configure(state="disabled")
                self.send_button.configure(state="disabled", text="Re-thinking...")
                self.model_combobox.configure(state="disabled")
                self.export_button.configure(state="disabled")
                self.import_button.configure(state="disabled")
                self.chat_listbox.configure(state="disabled")
                self.new_chat_button.configure(state="disabled")

            else:
                CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                              message=f"Error during regenerating response: "
                                      f"The previous message is not a user message,"
                                      f" and it is not possible to edit the response.", icon="warning")
        except ValueError:
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during regenerating response: Message from AI not found in history",
                          icon="warning")
        except Exception as e:
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during regenerating response: {e}", icon="cancel")

    def display_ai_response(self, ai_response_data):
        self.display_message(ai_response_data, "bot")
        self.message_history.append(ai_response_data)
        max_history_length = 20
        if len(self.message_history) > max_history_length:
            self.message_history = self.message_history[-max_history_length:]
        self.unlock_input()

    def unlock_input(self):
        self.message_textbox.configure(state="normal")
        self.send_button.configure(state="normal", text="Send")
        self.model_combobox.configure(state="readonly")
        self.export_button.configure(state="normal")
        self.import_button.configure(state="normal")
        self.chat_listbox.configure(state="normal")
        self.new_chat_button.configure(state="normal")

    def clear_chat_display(self):
        for widget in self.chat_display.winfo_children():
            widget.destroy()
        self.message_row_index = 0

    def redraw_chat(self):
        self.clear_chat_display()
        for message in self.message_history:
            self.display_message(message, message["role"])
        self.chat_display.update_idletasks()
        self.chat_display._parent_canvas.yview_moveto(1.0)
        self.update_scroll_region()

    def create_new_chat(self):
        if self.new_chat_button.cget("state") == "disabled":
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during creating new chat: "
                                  f"You cannot create a new chat while generating a response.", icon="warning")
            return

        chat_name = ctk.CTkInputDialog(text="Enter name of new chat:", title="New chat").get_input()
        if chat_name and chat_name not in self.chats:
            self.chats[chat_name] = []
            self.chat_listbox.configure(values=list(self.chats.keys()))
            self.chat_listbox.set(chat_name)
            self.switch_chat(chat_name)
            self.chat_display.update_idletasks()
            self.chat_display._parent_canvas.yview_moveto(0.0)
        elif chat_name:
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during creating new chat: "
                                  f"A chat with the name '{chat_name}' already exists.", icon="warning")

    def switch_chat(self, chat_name):
        if self.chat_listbox.cget("state") == "disabled":
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during switching chat: "
                                  f"You cannot switch the chat while generating a response.", icon="warning")
            self.chat_listbox.set(self.current_chat_name)
            return
        if chat_name != self.current_chat_name and chat_name in self.chats:
            self.current_chat_name = chat_name
            self.message_history = self.chats[self.current_chat_name]
            self.redraw_chat()

    def update_scroll_region(self, event=None):
        if self.chat_display.winfo_exists():
            self.chat_display._parent_canvas.configure(scrollregion=self.chat_display._parent_canvas.bbox("all"))

    def export_chats(self):
        if self.export_button.cget("state") == "disabled":
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during exporting chats: "
                                  f"It is not possible to export chats during response generation.", icon="warning")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All files", "*.*")],
            title="Save chats as..."
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.chats, f, ensure_ascii=False, indent=4)
                CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                              message=f"Chats have been successfully exported to {file_path}", icon="check")
            except Exception as e:
                CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                              message=f"Error during exporting chats: {e}", icon="cancel")

    def import_chats(self):
        if self.import_button.cget("state") == "disabled":
            CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                          message=f"Error during importing chats: "
                                  f"It is not possible to import chats during response generation.",
                          icon="warning")
            return

        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All files", "*.*")],
            title="Choose file for import..."
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    imported_chats = json.load(f)
                temp_chat_name = "__temp_import_chat__"
                while temp_chat_name in self.chats:
                    temp_chat_name += "_"
                self.chats[temp_chat_name] = []
                current_chat_list_values = list(self.chats.keys())
                if temp_chat_name not in current_chat_list_values:
                    current_chat_list_values.append(temp_chat_name)
                    self.chat_listbox.configure(values=current_chat_list_values)

                self.switch_chat(temp_chat_name)

                self.chats.update(imported_chats)
                self.chat_listbox.configure(values=list(self.chats.keys()))

                target_chat_name = "Default Chat" if "Default Chat" in self.chats else list(self.chats.keys())[0] if self.chats else None
                if target_chat_name:
                    self.chat_listbox.set(target_chat_name)
                    self.switch_chat(target_chat_name)
                if temp_chat_name in self.chats:
                    del self.chats[temp_chat_name]
                    self.chat_listbox.configure(values=list(self.chats.keys()))
                    self.chat_listbox.set(self.current_chat_name)
                CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                              message=f"Chats have been successfully imported from {file_path}", icon="check")
            except Exception as e:
                CTkMessagebox(title="xzyNotepad (Assistant Chat)",
                              message=f"Error during importing chats: {e}", icon="cancel")

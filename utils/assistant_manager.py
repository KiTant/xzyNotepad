from CTkMessagebox import CTkMessagebox
from g4f import ChatCompletion
from utils.variables import MODEL_MAP
import customtkinter as ctk
import threading
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.assistant_window import AssistantChatApp


def send_message(Window: "AssistantChatApp", event=None, message=None):
    user_message = Window.message_textbox.get("0.0", "end-1c") if message is None else message
    if not user_message.strip():
        return

    selected_model_name = Window.model_combobox.get()
    selected_model_info = MODEL_MAP.get(selected_model_name)
    if not selected_model_info:
        Window.display_message({"role": "xzyNotepad",
                                "content": f"Error: Model '{selected_model_name}' not found or not supporting.",
                                "model_name": "xzyNotepad"}, "bot")
        Window.unlock_input()
        return

    selected_model, selected_provider = selected_model_info

    user_message_data = {"role": "user", "content": user_message, "is_edited": False, "model_name": "User"}

    Window.display_message(user_message_data, "user")
    Window.message_history.append(user_message_data)
    Window.message_textbox.delete("1.0", ctk.END)
    Window.lock_input()

    threading.Thread(
        target=get_ai_response,
        args=(Window, Window.message_history.copy(), selected_model, selected_provider, selected_model_name),
        daemon=True
    ).start()


def get_ai_response(Window: "AssistantChatApp", conversation_history, model, provider=None, model_name="AI"):
    try:
        clean_history = [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history if msg["role"] != "xzyNotepad"]
        response = ChatCompletion.create(model=model, messages=clean_history, provider=provider, stream=False)
        ai_response = response if isinstance(response, str) else str(response)
        ai_response_data = {"role": "assistant", "content": ai_response, "is_edited": False,
                            "type": "text", "model_name": model_name}
    except Exception as e:
        ai_response_data = {"role": "xzyNotepad",
                            "content": f"Error while trying to get answer from AI:"
                                       f" {e}\nTry to choose other model or try to turn on/off VPN. "
                                       f"It will be better if you delete this message", "is_edited": False,
                            "type": "text", "model_name": model_name}
    Window.after(0, Window.display_ai_response, ai_response_data)


def regenerate_ai_response(Window: "AssistantChatApp", ai_message_data):
    try:
        ai_index = Window.message_history.index(ai_message_data)
        if ai_index > 0 and Window.message_history[ai_index - 1]["role"] == "user":
            del Window.message_history[ai_index]
            Window.redraw_chat()

            selected_model_name = Window.model_combobox.get()
            selected_model_info = MODEL_MAP.get(selected_model_name)
            if not selected_model_info:
                Window.display_message({"role": "xzyNotepad",
                                        "content": f'Error: Model "{selected_model_name}" '
                                                   f'not found or it is not supported for regenerating answer.',
                                        "type": "text", "model_name": "System"}, "bot")
                Window.unlock_input()
                return
            selected_model, selected_provider = selected_model_info

            threading.Thread(
                target=get_ai_response,
                args=(Window, Window.message_history[:ai_index].copy(), selected_model,
                      selected_provider, selected_model_name),
                daemon=True
            ).start()

            Window.lock_input("Re-thinking...")

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

__all__ = ["send_message", "regenerate_ai_response"]

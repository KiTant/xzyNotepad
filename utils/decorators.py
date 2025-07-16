from CTkMessagebox import CTkMessagebox


def text_change(func):
    def wrapper(*args, **kwargs):
        window = args[0].Window if hasattr(args[0], 'Window') else args[0]  # args[0].Window working if args[0] == obj
        window.change_history()
        result = func(*args, **kwargs)
        window.change_history()
        window.codebox.line_nums.redraw()
        window.codebox.update_code()
        return result
    return wrapper


def text_check(check_for_nothing: bool = False):
    def text_check_action(func):
        def wrapper(*args, **kwargs):
            from utils.helpers import get_selected_text
            window = args[0].Window if hasattr(args[0], 'Window') else args[0]  # args[0].Window working if args[0] == obj
            text = get_selected_text(window)
            if text:
                if (check_for_nothing is True and text['selected'].strip() != "") or check_for_nothing is False:
                    result = func(*args, **kwargs)
                else:
                    result = "Error 2"
                    CTkMessagebox(title="xzyNotepad", message="Selected text is literally nothing.", icon="warning")
            else:
                result = "Error"
                CTkMessagebox(title="xzyNotepad", message="Selected text is not detected.", icon="warning")
            return result

        return wrapper
    return text_check_action

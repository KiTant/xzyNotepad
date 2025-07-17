from CTkMessagebox import CTkMessagebox
import requests
from utils.variables import VERSION
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.main_window import MainWindow as MainWindowClass


def stop_update(MainWindow: "MainWindowClass", title, message, icon):
    CTkMessagebox(title=title, message=message, icon=icon)
    MainWindow.updating = False


def download_last_release(MainWindow: "MainWindowClass", version):
    msg = CTkMessagebox(title="xzyNotepad (updating)",
                        message="Update of xzyNotepad is started, please wait...",
                        icon="info")
    response = requests.get(f'https://github.com/KiTant/xzyNotepad/releases/download/{version}/xzyNotepad.exe')
    msg.destroy()
    if response.ok:
        try:
            with open(f"xzyNotepad{version}.exe", "wb") as file:
                file.write(response.content)
            stop_update(MainWindow, title="xzyNotepad (updating)", icon="check",
                        message="New update successfully installed as new file"
                                " in directory where storages this version."
                                "You can delete this version and open new.")
        except:
            stop_update(MainWindow, title="xzyNotepad (downloading update)", icon="cancel",
                        message="Unexpected error while creating new file with update.")
    else:
        stop_update(MainWindow, title="xzyNotepad (downloading update)", icon="cancel",
                    message="Unexpected error while trying to get last release, please check your internet.")


def check_last_version(MainWindow: "MainWindowClass"):
    for window in MainWindow.all_children:
        if window.title() == "xzyNotepad (checking updates)" or MainWindow.updating is True:
            return
    MainWindow.updating = True
    msg = CTkMessagebox(title="xzyNotepad (checking updates)",
                        message="Trying to check updates please wait...",
                        icon="info")
    response = requests.get("https://api.github.com/repos/KiTant/xzyNotepad/releases/latest")
    msg.destroy()
    if response.ok:
        latest_release = response.json()
        if VERSION < latest_release['tag_name'][1:]:
            msg = CTkMessagebox(title="xzyNotepad (checking updates)",
                                message="Your version is outdated, do you want to update?",
                                icon="info", options=["Yes", "No"], topmost=False)
            if msg.get() in ["Yes"]:
                all_saved = True
                found_file = False
                for window in MainWindow.all_children + [MainWindow]:
                    if hasattr(window, "saved"):
                        if window.saved is False:
                            all_saved = False
                            break
                if all_saved is False:
                    msg = CTkMessagebox(title="xzyNotepad (updating)",
                                        message="Some files not saved, you really want to update?",
                                        icon="warning", options=["Yes", "No"])
                    if msg.get() in ["No"]:
                        MainWindow.updating = False
                        return
                if latest_release['assets'] is None:
                    MainWindow.updating = False
                    return
                for asset in latest_release['assets']:
                    if asset['name'].strip().startswith("xzyNotepad") and asset['name'].strip().endswith(".exe"):
                        found_file = True
                        download_last_release(MainWindow, latest_release['tag_name'])
                if found_file is False:
                    stop_update(MainWindow, title="xzyNotepad (updating)", icon="info",
                                message="Not found main file of xzyNotepad, update stopped.")
        else:
            stop_update(MainWindow, title="xzyNotepad (checking updates)", icon="info",
                        message="You have latest release of xzyNotepad")
    else:
        stop_update(MainWindow, title="xzyNotepad (checking updates)", icon="cancel",
                    message="Unexpected error while trying to get last release, please check your internet.")
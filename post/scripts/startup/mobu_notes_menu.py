# Mobu 2025 - add Mobu Notes tools to the menu bar
# Copy/link this file to the MotionBuilder user config PythonStartup folder.

import importlib
import sys
import traceback

from pyfbsdk import *  # noqa: F403


REPO_SCRIPTS = r"E:\Projects\Repositories\Mobu-Notes\post\scripts"
MENU_NAME = "Mobu Notes"

_MENU_REF = None

if REPO_SCRIPTS not in sys.path:
    sys.path.append(REPO_SCRIPTS)


def _open_module(module_name):
    try:
        module = __import__(module_name)
        importlib.reload(module)
        module.main()
        print("[MobuNotesMenu] Opened {0}".format(module_name))
    except Exception:
        error = traceback.format_exc()
        print(error)
        FBMessageBox("Mobu Notes Menu Error", error, "OK")


def _on_menu(control, event):
    if event.Id == 1:
        _open_module("noise_cleaner")
    elif event.Id == 2:
        _open_module("finger_preset_tool")
    elif event.Id == 3:
        _open_module("pose_blend_tool")


def install_menu():
    global _MENU_REF

    menu_manager = FBMenuManager()

    # Create a top-level menu. This is more reliable than relying on Python Tools auto discovery.
    try:
        menu_manager.InsertBefore(None, "Help", MENU_NAME)
    except Exception:
        pass

    menu = menu_manager.GetMenu(MENU_NAME)
    if menu is None:
        menu_manager.InsertLast(None, MENU_NAME)
        menu = menu_manager.GetMenu(MENU_NAME)

    if menu is None:
        FBMessageBox("Mobu Notes Menu Error", "Could not create Mobu Notes menu.", "OK")
        return

    menu.InsertLast("Noise Cleaner", 1)
    menu.InsertLast("Finger Preset Tool", 2)
    menu.InsertLast("Pose Blend Tool", 3)
    menu.OnMenuActivate.Add(_on_menu)

    _MENU_REF = menu
    print("[MobuNotesMenu] Installed.")


install_menu()

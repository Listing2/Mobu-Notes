# Mobu 2025 — launcher for Open Reality > Tools
# Copy/link this file to the MotionBuilder user config Scripts folder.

import importlib
import sys


REPO_SCRIPTS = r"E:\Projects\Repositories\Mobu-Notes\post\scripts"

if REPO_SCRIPTS not in sys.path:
    sys.path.append(REPO_SCRIPTS)

import finger_preset_tool  # noqa: E402

importlib.reload(finger_preset_tool)
finger_preset_tool.main()

# Mobu 2025 — launcher for Open Reality > Tools
# Copy/link this file to the MotionBuilder user config Scripts folder.

import importlib
import sys


REPO_SCRIPTS = r"E:\Projects\Repositories\Mobu-Notes\post\scripts"

if REPO_SCRIPTS not in sys.path:
    sys.path.append(REPO_SCRIPTS)

import noise_cleaner  # noqa: E402

importlib.reload(noise_cleaner)
noise_cleaner.main()

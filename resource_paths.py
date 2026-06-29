from pathlib import Path
import sys


def resource_path(relative_path: str) -> Path:
    """
    Resolve resource paths for both normal source runs and PyInstaller builds.

    Source run:
        project_root/assets/...

    PyInstaller folder build:
        dist/RS3-DataTool/_internal/assets/...
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path

    return Path(__file__).resolve().parent / relative_path
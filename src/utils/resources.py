import sys
import os

def resource_path(relative_path):
    """ 
    Gets the absolute path to a resource.
    Works for development (dev) and for the PyInstaller executable (_MEIPASS).
    """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
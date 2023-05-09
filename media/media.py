from pathlib import Path
from os import path
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)


class paths:
    PROJECT_PATH = resource_path(Path(__file__).parent)

    GTSoftwareLogo = path.join(PROJECT_PATH, "GTSoftwareLogo.png")
    logo = path.join(PROJECT_PATH, "logo.png")
    logoBorderless = path.join(PROJECT_PATH, "logoBorderless.png")

    KAL = path.join(PROJECT_PATH, "KAL.png")
    GTVultIn = path.join(PROJECT_PATH, "GTVultIn.png")
    Liex = path.join(PROJECT_PATH, "Liex.png")
    Inkord = path.join(PROJECT_PATH, "Inkord.png")
    GotaLabel = path.join(PROJECT_PATH, "GotaLabel.png")
    SingleLabel = path.join(PROJECT_PATH, "SingleLabel.png")
    PakLijst = path.join(PROJECT_PATH, "PakLijst.png")
    OrderScan = path.join(PROJECT_PATH, "OrderScan.png")

    Run = path.join(PROJECT_PATH, "Run.png")
    Import = path.join(PROJECT_PATH, "Import.png")
    Print = path.join(PROJECT_PATH, "Print.png")
    New = path.join(PROJECT_PATH, "New.png")
    Show = path.join(PROJECT_PATH, "Show.png")

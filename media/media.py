from pathlib import Path
from os import path
from backEnd.gtHelpers import resource_path


class paths:
    PROJECT_PATH = resource_path(Path(__file__).parent)

    GTSoftwareLogo = path.join(PROJECT_PATH, "GTSoftwareLogo.png")
    logo = path.join(PROJECT_PATH, "logo.png")
    logoBorderless = path.join(PROJECT_PATH, "logoBorderless.png")

    # Bigger 64x64 logos for sub-apps
    KAL = path.join(PROJECT_PATH, "KAL.png")
    GTVultIn = path.join(PROJECT_PATH, "GTVultIn.png")
    Liex = path.join(PROJECT_PATH, "Liex.png")
    Inkord = path.join(PROJECT_PATH, "Inkord.png")
    GotaLabel = path.join(PROJECT_PATH, "GotaLabel.png")
    SingleLabel = path.join(PROJECT_PATH, "SingleLabel.png")
    UALabel = path.join(PROJECT_PATH, "UALabel.png")
    PakLijst = path.join(PROJECT_PATH, "PakLijst.png")
    OrderScan = path.join(PROJECT_PATH, "OrderScan.png")

    # Smaller 32x32 icons
    Run = path.join(PROJECT_PATH, "Run.png")
    Import = path.join(PROJECT_PATH, "Import.png")
    Print = path.join(PROJECT_PATH, "Print.png")
    New = path.join(PROJECT_PATH, "New.png")
    Show = path.join(PROJECT_PATH, "Show.png")
    Add = path.join(PROJECT_PATH, "Add.png")
    AddWeekMenu = path.join(PROJECT_PATH, "AddWeekMenu.png")
    CreateWeekMenu = path.join(PROJECT_PATH, "CreateWeekMenu.png")

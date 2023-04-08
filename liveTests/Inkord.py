from backEnd.inkord import runInkord
from pathlib import Path

if __name__ == "__main__":
    filePathOrders = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\inkord-orders.xlsx"
    )
    exportFolder = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\export"
    )

    runInkord(filePathOrders, exportFolder)
    print("Finished Inkord run")

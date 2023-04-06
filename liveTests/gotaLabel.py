from scripts.gotaLabel import runGotaLabel
from pathlib import Path

if __name__ == "__main__":
    filePathOrders = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\gotalabel-orders.xlsx"
    )
    exportFolder = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\export"
    )

    runGotaLabel(filePathOrders, exportFolder)
    print("Finished gotaLabel run")

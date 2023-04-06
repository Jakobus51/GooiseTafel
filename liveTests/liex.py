from scripts.liex import runLiex
from pathlib import Path

if __name__ == "__main__":
    filePathWebShop = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\webshop-orders.csv"
    )
    filePathCustomers = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\klanten-bestand.xlsx"
    )
    exportFolder = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\export"
    )

    runLiex(filePathWebShop, filePathCustomers, exportFolder)
    print("Finished liex run")

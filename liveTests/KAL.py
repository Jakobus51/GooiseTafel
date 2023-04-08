from backEnd.KAL import runKal
from pathlib import Path

if __name__ == "__main__":
    filePathOrders = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\kal-orders.xlsx"
    )
    filePathCustomers = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\klanten-bestand.xlsx"
    )
    exportFolder = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\export"
    )

    runKal(filePathOrders, filePathCustomers, exportFolder)
    print("Finished KAL run")

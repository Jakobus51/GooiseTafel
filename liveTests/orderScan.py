from backEnd.orderScan.orderScan import processMenulists
from backEnd.constants import saveLocations as sl
import os
from backEnd.gtHelpers import resource_path

# To run $python -m liveTests.orderScan
if __name__ == "__main__":
    os.environ["PATH"] += (
        os.pathsep
        + r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\backEnd\externalPackages\poppler-23.08.0\Library\bin"
    )
    os.environ["PATH"] += (
        os.pathsep
        + r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\backEnd\externalPackages\tessarect"
    )

    ordersFile = "DOC.pdf"
    filePathOrders = sl.OrderScanInput / ordersFile

    processMenulists(filePathOrders, sl.OrderScanOutput)
    print("Finished OrderScan")

from backEnd.inkord import runInkord
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    ordersFile = "inkord-orders.xlsx"
    filePathOrders = sl.InkordInput / ordersFile

    runInkord(filePathOrders, sl.InkordOutput, True)
    print("Finished Inkord run")

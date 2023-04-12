from backEnd.pakLijst import runPakLijst
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    ordersFile = "gotalabel-orders.xlsx"
    filePathOrders = sl.PakLijstInput / ordersFile

    runPakLijst(filePathOrders, sl.PakLijstOutput, isPerRoute=True, showPdf=True)
    print("Finished pakLijst run")

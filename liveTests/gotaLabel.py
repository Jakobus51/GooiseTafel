from backEnd.gotaLabel import runGotaLabel
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    ordersFile = "inkord-orders.xlsx"
    filePathOrders = sl.GotaLabelInput / ordersFile

    runGotaLabel(filePathOrders, sl.GotaLabelOutput)
    print("Finished gotaLabel run")

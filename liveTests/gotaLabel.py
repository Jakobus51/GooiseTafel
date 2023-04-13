from backEnd.gotaLabel import fetchOrders
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    ordersFile = "gotalabel-orders.xlsx"
    filePathOrders = sl.GotaLabelInput / ordersFile

    fetchOrders(filePathOrders)
    print("Finished gotaLabel run")

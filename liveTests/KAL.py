from backEnd.KAL import runKal
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    ordersFile = "kal-orders.xlsx"
    filePathOrders = sl.KALInput / ordersFile

    customersFile = "klanten-bestand.xlsx"
    filePathCustomers = sl.CustomersInput / customersFile

    runKal(filePathOrders, filePathCustomers, sl.KALOutput, True)
    print("Finished KAL run")

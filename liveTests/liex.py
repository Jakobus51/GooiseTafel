from backEnd.liex import runLiex
from backEnd.constants import saveLocations as sl

if __name__ == "__main__":
    webShopOrdersFile = "webshop-orders.csv"
    filePathWebShopOrders = sl.LiexInput / webShopOrdersFile

    customersFile = "klanten-bestand.xlsx"
    filePathCustomers = sl.CustomersInput / customersFile

    runLiex(webShopOrdersFile, filePathCustomers, sl.LiexOutput)
    print("Finished liex run")

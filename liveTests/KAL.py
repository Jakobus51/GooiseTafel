from scripts.gsHelpers import getDateVerkoop, getDateOfExactFile
from scripts.KAL import retrieveCustomersYetToOrder, displayDataFrame
from scripts.pdfCreator import createPDF
from scripts.constants import KalPDF
from pandas import read_excel

if __name__ == "__main__":
    filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\kal-orders.xlsx"
    filePathCustomers = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\klanten-bestand.xlsx"

    rawOrderData = read_excel(filePathOrders, header=None)
    rawCustomerData = read_excel(filePathCustomers, header=None)

    afleverDate = getDateVerkoop(rawOrderData)
    exportDate = getDateOfExactFile(rawOrderData)

    customers = retrieveCustomersYetToOrder(rawOrderData, rawCustomerData)
    displayData = displayDataFrame(customers)

    createPDF(
        KalPDF.Title(afleverDate),
        KalPDF.MetaData(afleverDate, exportDate),
        displayData,
        KalPDF.columnSpacing,
    )
    print("Finished")

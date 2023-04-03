from scripts.gsHelpers import getDateVerkoop, getDateOfExactFile
from scripts.Inkord import retrieveOrderQuantity, displayDataFrame
from scripts.pdfCreator import createPDF
from scripts.constants import InkordPDF
from pandas import read_excel

if __name__ == "__main__":
    filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\inkord-orders.xlsx"
    rawOrderData = read_excel(filePathOrders, header=None)

    afleverDate = getDateVerkoop(rawOrderData)
    exportDate = getDateOfExactFile(rawOrderData)

    orders = retrieveOrderQuantity(rawOrderData)
    displayOrders = displayDataFrame(orders)

    createPDF(
        InkordPDF.Title(afleverDate),
        InkordPDF.MetaData(afleverDate, exportDate),
        displayOrders,
        InkordPDF.columnSpacing,
    )
    print("Finished")

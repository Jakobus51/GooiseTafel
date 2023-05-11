from pandas import DataFrame, read_excel
from backEnd.gtHelpers import (
    prepareExactData,
    getDeliveryDateRange,
    getDateOfExactFile,
)
from backEnd.constants import orders
from pathlib import Path
from backEnd.pdfCreator import createPDF
from backEnd.dataClasses.pdfHelper import PdfHelper
from backEnd.dataClasses.appEnum import AppEnum


def runPakLijst(
    filePathOrders: Path, outputFolder: Path, isPerRoute: bool, showPdf: bool
):
    rawOrderData = read_excel(filePathOrders, header=None)

    # Get data used in metadata and title of pdf
    deliveryDateRange = getDeliveryDateRange(rawOrderData)
    dateOfExactOutput = getDateOfExactFile(rawOrderData)

    # Retrieve data you want to display and make it pdf ready
    sortedOrders = sortOrders(rawOrderData, isPerRoute)
    pdfInput = PdfHelper(
        AppEnum.PakLijstRoute if isPerRoute else AppEnum.PakLijstCategory,
        deliveryDateRange,
        dateOfExactOutput,
    )

    formatForPdf(sortedOrders, pdfInput)

    # Create the pdf
    createPDF(pdfInput, outputFolder, showPdf)


def sortOrders(rawOrderData: DataFrame, isPerRoute: bool) -> dict:
    """Retrieves the information needed to create the labels

    Args:
        rawOrderData (pd.DataFrame): Exact export with all other that need a label

    Returns:
       dict: Dictionary with key deliveryMethod and value a dataframe of all labels that are in that deliveryMethod.
    """
    # prepare order and customer data
    orderData = prepareExactData(
        rawOrderData, orders.ankerWord, orders.columnNamesCustomers
    )

    # Select columns who need to be copied into every order (which are not 'quantity', 'productName' and 'deliveryDate')
    entriesToFill = [
        x
        for x in orders.columnNamesCustomers
        if x not in ["quantity", "productName", "deliveryDate"]
    ]

    # Fill nan values with the cell value above it for the given columns
    orderData[entriesToFill] = orderData[entriesToFill].fillna(method="ffill")

    # Remove all non-product rows
    orderData = orderData[orderData["quantity"].notna()]

    # Remove the rows where the product name is "Bezorgkosten" from the dataFrame
    orderData = orderData[orderData["productName"] != "Bezorgkosten"]

    # depending on whether the list is asked per route or per category, if per category additional data prep is needed
    return (
        createDictFromColumn(orderData, "deliveryMethod")
        if isPerRoute
        else createDictPerCategory(orderData)
    )


def createDictPerCategory(orderData: DataFrame) -> dict:
    """Sort the labels per general category which are :
    1. WARM AVOND, 2. KOELVERS AVOND, 3. WARM MIDDAG, 4. KOELVERS MIDDAG, 5. LEEG, 6+ misc?
    there may be more depending on the input data but these will all be taken care off through the loop

    Args:
        orderData (DataFrame): The labels you want to sort

    Returns:
        dict: Sorted dictionary with keys equal to the categories and values are dataFrames with the order data
    """
    # Split the delivery method into three seperate columns
    orderData[["temp", "time", "location"]] = orderData["deliveryMethod"].str.split(
        n=2, expand=True
    )

    # Fill these new columns with an empty string if they contain a NaN value
    orderData.fillna({"temp": "", "time": "", "location": ""}, inplace=True)

    # Add Temp and Time toghether as this is equal to the Category
    orderData["category"] = orderData["temp"] + " " + orderData["time"]

    return createDictFromColumn(orderData, "category")


def createDictFromColumn(orderData: DataFrame, columnName: str) -> dict:
    """Sort the labels per given column into a dictionary

    Args:
        orderLabelData (DataFrame): The labels you want to sort
        columnName (str): the column you want to split into dictionaries

    Returns:
        dict: Sorted dictionary with keys equal to the deliveryRoute and values are dataFrames with the order data
    """
    keys = orderData[columnName].unique()
    dict = {}
    for key in keys:
        dict[key] = orderData[orderData[columnName] == key]
    return dict


def formatForPdf(dictCustomers: dict, pdfInput: PdfHelper):
    """Only retrieves the columns you want to display and give them proper names then sum on the productNames
    Number of unique deliveries also get saved based on customerId
    Everything gets saved into a dictionary with a different entry for each shown table in the pdf.

    Args:
        dictCustomers (dict): Dictionary with entries for each delivery method
        pdfInput (PdfHelper): class containing the column names that will be displayed in the pdf
    """

    deliveries = {}
    for key in dictCustomers:
        data = dictCustomers[key]

        # Save the number of unique deliveries
        deliveries[key] = data["customerId"].nunique()

        # Display columns for PakLijstCategory and PakLijstRoute are the same
        data = data[pdfInput.dataDisplayColumn]

        # Sum the quantities of entries with the same productName and make a dataFrame of it
        summed = data.groupby("productName")["quantity"].sum()
        summedData = summed.to_frame().reset_index()

        # Rename to dutch friendly names that will be shown in the pdf
        summedData.columns = pdfInput.pdfDisplayColumns
        # summedData.set_axis(pdfInput.pdfDisplayColumns, axis=1, inplace=True)
        dictCustomers[key] = summedData

    pdfInput.setDeliveries(deliveries)
    pdfInput.setTableData(dictCustomers)

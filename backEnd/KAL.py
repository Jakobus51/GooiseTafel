from pandas import DataFrame, read_excel
from backEnd.gtHelpers import (
    prepareExactData,
    getDeliveryDateRange,
    getDateOfExactFile,
)
from backEnd.constants import orders, customers
from backEnd.classes.pdfHelper import PdfHelper, PdfEnum
from pathlib import Path
from backEnd.pdfCreator import createPDF


def runKal(
    filePathOrders: Path, filePathCustomers: Path, outputFolder: Path, showPDF: bool
) -> None:
    """Finds all customers who have yet to order and exports a pdf of the results

    Args:
        filePathOrders (Path): Location where the orders are to be found
        filePathCustomers (Path): Location where the customers are to be found
        outputFolder (Path): Place where you want to save the pdf
        showPDF (bool): Shows the pdf if true
    """
    rawOrderData = read_excel(filePathOrders, header=None)
    rawCustomerData = read_excel(filePathCustomers, header=None)

    # Get data used in metadata and title of pdf
    deliveryDateRange = getDeliveryDateRange(rawOrderData)
    dateOfExactOutput = getDateOfExactFile(rawOrderData)

    # Retrieve data you want to display and make it pdf ready
    customersYetToOrder = retrieveCustomersYetToOrder(rawOrderData, rawCustomerData)
    dividedCustomers = divideCustomers(customersYetToOrder)

    pdfInput = PdfHelper(PdfEnum.KAL, deliveryDateRange, dateOfExactOutput)
    pdfInput.setTableData(formatForPdf(dividedCustomers, pdfInput))

    # Create the pdf
    createPDF(pdfInput, outputFolder, showPDF)


def retrieveCustomersYetToOrder(
    rawOrderData: DataFrame, rawCustomerData: DataFrame
) -> DataFrame:
    """checks which customers are in the orderData but not in the customer data

    Args:
        rawOrderData (DataFrame): Exact output containing every customer who ordered in a given timespan
        rawCustomerData (DateFrame): Exact output containing all customers

    Returns:
        DataFrame: Dataframe of all customers who have yet to order
    """

    # Format the exact data properly
    orderData = prepareExactData(
        rawOrderData, orders.ankerWord, orders.columnNamesCustomers
    )
    customerData = prepareExactData(
        rawCustomerData, customers.ankerWord, customers.columnNames
    )

    # Remove all non-customer rows
    orderData = orderData[orderData["customerId"].notna()]

    # Set types otherwise .isin does not work
    orderData["customerId"] = orderData["customerId"].astype(int)
    customerData["customerId"] = customerData["customerId"].astype(int)

    # make a boolean array where True indicates the customer is present in the orderData
    mask = customerData["customerId"].isin(orderData["customerId"])
    # Remove all customers that are already in the orderData
    filteredCustomers = customerData[~mask]

    return filteredCustomers


def divideCustomers(data: DataFrame) -> dict:
    """Divides the customers into three groups:
    Group 1 (GT): customers who are ordered for
    Group 2 (@): customers who order online
    Group 3 (not @ or GT): the rest

    Args:
        data (DataFrame): Dataframe where all customers are combined

    Returns:
        dict: Dictionary with three entries, one for each group
    """
    data["customerRemarks1"].fillna("", inplace=True)

    customers = {
        "GT": data[data["customerRemarks1"].str.startswith("GT")],
        "online": data[data["customerRemarks1"].str.startswith("@")],
        "normal": data[~data["customerRemarks1"].str.startswith(("GT", "@"))],
    }
    return customers


def formatForPdf(dictCustomers: dict, pdfInput: PdfHelper) -> dict:
    """Only retrieves the columns you want to display and give them proper names

    Args:
        dictCustomers (dict): Dictionary with three entries, one for each group with extra columns which need to be removed
        pdfInput (PdfHelper): class containing the column names that will be displayed in the pdf

    Returns:
        dict: Dictionary with the three groups ready to be displayed
    """
    for key in dictCustomers:
        data = dictCustomers[key]
        data = data[pdfInput.dataDisplayColumn]
        # split string on - and keep latter half, this chops off the abbreviated part of deliveryMethod
        data["deliveryMethod"] = data["deliveryMethod"].str.split("-")
        data["deliveryMethod"] = data["deliveryMethod"].str[1]

        # set all NaN value to an empty string
        data.fillna("", inplace=True)

        # Set columns to dutch readable names
        data.set_axis(pdfInput.pdfDisplayColumns, axis=1, inplace=True)
        dictCustomers[key] = data
    return dictCustomers

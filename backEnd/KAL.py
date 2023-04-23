from pandas import DataFrame, read_excel, ExcelWriter
from backEnd.gtHelpers import (
    prepareExactData,
    getDeliveryDateRange,
    getDateOfExactFile,
)
from backEnd.constants import orders, customers
from backEnd.dataClasses.pdfHelper import PdfHelper
from pathlib import Path
from backEnd.pdfCreator import createPDF
from backEnd.dataClasses.appEnum import AppEnum
from os import path
from subprocess import Popen


def runKal(
    filePathOrders: Path,
    filePathCustomers: Path,
    outputFolder: Path,
    showOutput: bool,
    isPDF: bool,
) -> None:
    """Finds all customers who have yet to order and exports a pdf of the results

    Args:
        filePathOrders (Path): Location where the orders are to be found
        filePathCustomers (Path): Location where the customers are to be found
        outputFolder (Path): Place where you want to save the pdf
        showOutput (bool): Shows the pdf if true
        isPDF (bool): True if you want a pdf as output otherwise it is an excel
    """
    rawOrderData = read_excel(filePathOrders, header=None)
    rawCustomerData = read_excel(filePathCustomers, header=None)

    # Get data used in metadata and title of pdf
    deliveryDateRange = getDeliveryDateRange(rawOrderData)
    dateOfExactOutput = getDateOfExactFile(rawOrderData)

    # Retrieve data you want to display and make it pdf ready
    customersYetToOrder = retrieveCustomersYetToOrder(rawOrderData, rawCustomerData)
    dividedCustomers = divideCustomers(customersYetToOrder)

    # Although it is called pdf, the excel output uses the same table data so the pdfInput also gets fed into the createExcel method
    pdfInput = PdfHelper(AppEnum.KAL, deliveryDateRange, dateOfExactOutput)
    formatForPdf(dividedCustomers, pdfInput)
    # Creates the pdf or excel
    if isPDF:
        createPDF(pdfInput, outputFolder, showOutput)
    else:
        createExcel(pdfInput, outputFolder, showOutput)


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
    print(filteredCustomers)

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
    """Only retrieves the columns you want to display and give them proper names, only first part of delivery column gets saved.
    Everything gets saved into a dictionary with a different entry for each shown table in the pdf.

    Args:
        dictCustomers (dict): Dictionary with three entries, one for each group with extra columns which need to be removed
        pdfInput (PdfHelper): class containing the column names that will be displayed in the pdf

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
    pdfInput.setTableData(dictCustomers)


def createExcel(
    pdfInput: PdfHelper,
    outputFolder: Path,
    showOutput: bool,
) -> None:
    """Creates an excel based on the given input and auto-widths the columns
    !Although it is called pdfInput, it contains also all the data needed to create the excel

    Args:
        pdfInput (PdfHelper): Object containing all information needed to create the excel
        outputFolder (Path): Where the pdf needs to be saved
        showOutput (bool): Whether or not you want to show the pdf after creation
    """
    outputFile = path.join(outputFolder, f"{pdfInput.title}.xlsx")

    with ExcelWriter(outputFile) as writer:
        for key in pdfInput.tableData:
            df = pdfInput.tableData[key].copy()
            df.to_excel(writer, sheet_name=key, index=None)

            # Makes the width of the columns auto width, so the data shows properly in the excel, stole it from StackOverflow
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets[key].set_column(col_idx, col_idx, column_length + 1)

    # Open the excel if that option was selected
    if showOutput:
        Popen([outputFile], shell=True)

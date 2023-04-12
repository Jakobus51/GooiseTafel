from pandas import DataFrame, read_excel
from backEnd.gtHelpers import (
    prepareExactData,
    getDeliveryDateRange,
    getDateOfExactFile,
)
from backEnd.constants import orders
from backEnd.classes.pdfHelper import PdfHelper
from backEnd.classes.appEnum import AppEnum
from pathlib import Path
from backEnd.pdfCreator import createPDF


def runInkord(filePathOrders: Path, outputFolder: Path, showPDF: bool) -> None:
    """Sums the orders and exports a pdf of the results

    Args:
        filePathOrders (Path): Location where the orders are to be found
        outputFolder (Path): Place where you want to save the pdf
        showPDF (bool): Shows the pdf if true
    """
    rawOrderData = read_excel(filePathOrders, header=None)

    # Get data used in metadata and title of pdf
    deliveryDateRange = getDeliveryDateRange(rawOrderData)
    dateOfExactOutput = getDateOfExactFile(rawOrderData)

    # Retrieve data you want to display and make it pdf ready
    summedOrders = retrieveOrderQuantity(rawOrderData)

    pdfInput = PdfHelper(AppEnum.Inkord, deliveryDateRange, dateOfExactOutput)
    formatForPdf(summedOrders, pdfInput)

    # Create the pdf
    createPDF(pdfInput, outputFolder, showPDF)


def retrieveOrderQuantity(rawOrderData: DataFrame) -> DataFrame:
    """Sums the orders using their productIds.
        0004w, 0004k, 0004P get summed together

    Args:
        data (DataFrame): A dataframe of an exact export of the orders sorted by article

    Returns:
        DataFrame: A dataframe where products are summed
    """
    # Format the exact data properly
    orderData = prepareExactData(
        rawOrderData, orders.ankerWord, orders.columnNamesArticles
    )

    # Fill nan values with the cell value above it for the columns "productId" and "productName"
    orderData[["productId", "productName"]] = orderData[
        ["productId", "productName"]
    ].fillna(method="ffill")

    # use str.replace() to remove non-numeric characters from the 'productId' column
    orderData["productId"] = orderData["productId"].str.replace(r"\D+", "")

    # Check if cell contains a "-" if that is the case, remove all characters to the right of it
    orderData["productName"] = orderData["productName"].astype(str)
    orderData["productName"] = orderData["productName"].apply(
        lambda x: x[: x.rfind("-")] if "-" in x else x
    )

    # Create a dictionary which connects the productIds with the productNames
    prod_dict = dict(zip(orderData["productId"], orderData["productName"]))

    # Sum the quantities of entries with the same productId and make a dataFrame of it
    summed = orderData.groupby("productId")["quantity"].sum()
    summedData = summed.to_frame().reset_index()

    # Create new column with the productNames based on the productIds
    summedData["productName"] = summedData["productId"].map(prod_dict)

    return summedData


def formatForPdf(data: DataFrame, pdfInput: PdfHelper):
    """Only retrieves the columns you want to display and give them proper names and sort on product name
    Everything gets saved into a dictionary with a different entry for each shown table in the pdf.

    Args:
        data (DataFrame): The original dataframe containing all columns
        pdfInput (PdfHelper): class containing the column names that will be displayed in the pdf

    """
    # only save specific columns
    data = data[pdfInput.dataDisplayColumn]
    # sort on alphabetical order
    data.sort_values("productName", inplace=True)
    # Rename to dutch friendly names that will be shown in the pdf
    data.set_axis(pdfInput.pdfDisplayColumns, axis=1, inplace=True)
    pdfInput.setTableData({"normal": data})

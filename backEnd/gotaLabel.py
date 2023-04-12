from pandas import DataFrame, read_excel
from backEnd.gtHelpers import prepareExactData
from backEnd.constants import orders
from pathlib import Path
from backEnd.classes.labelHelper import LabelHelper
from backEnd.classes.appEnum import AppEnum


def fetchOrders(filePathOrders: Path):
    rawOrderData = read_excel(filePathOrders, header=None)

    labelsInput = LabelHelper(AppEnum.GotaLabel)

    labelsInput.labelDataPerDeliveryMethod = sortOrders(rawOrderData)
    return labelsInput


def sortOrders(rawOrderData: DataFrame) -> dict:
    """Retrieves the information needed to create the labels

    Args:
        rawOrderData (DataFrame): Exact export with all other that need a label

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

    # depending on whether the list is asked per route or per category, if per category additional data prep is needed
    return createDictFromColumn(orderData, "deliveryMethod")


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

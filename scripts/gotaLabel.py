from pandas import DataFrame, read_excel
from scripts.gsHelpers import prepareExactData
from scripts.constants import orders
from pathlib import Path


def runGotaLabel(filePathOrders: Path, exportFolder: Path) -> None:
    rawOrderData = read_excel(filePathOrders, header=None)
    orderLabels = retrieveLabelDf(rawOrderData)


def retrieveLabelDf(rawOrderData: DataFrame) -> DataFrame:
    """checks which customers are in the orderData but not in the customer data

    Args:
        rawOrderData (pd.DataFrame): Exact output containing every customer who ordered in a given timespan
        rawCustomerData (pd.DateFrame): Exact output containing all customers

    Returns:
       DataFrame: Dataframe of all customers who have yet to order
    """
    # prepare order and customer data
    orderData = prepareExactData(
        rawOrderData, orders.ankerWord, orders.columnNamesCustomers
    )

    # remove 'quantity', 'deliveryDate' and 'productName' from the column list, these columns don't need to be set per product
    entriesToFill = [
        x
        for x in orders.columnNamesCustomers
        if x not in ["quantity", "productName", "deliveryDate"]
    ]

    # Fill nan values with the cell value above it for the given columns
    orderData[entriesToFill] = orderData[entriesToFill].fillna(method="ffill")

    # Remove all non-product rows
    orderLabelData = orderData[orderData["quantity"].notna()]

    return orderLabelData

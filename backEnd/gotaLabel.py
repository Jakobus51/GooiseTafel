from pandas import DataFrame, read_excel
from backEnd.gtHelpers import prepareExactData, getDeliveryDateRange, getDateOfExactFile
from backEnd.constants import orders
from pathlib import Path


def runGotaLabel(filePathOrders: Path, exportFolder: Path):
    rawOrderData = read_excel(filePathOrders, header=None)

    deliveryDateRange = getDeliveryDateRange(rawOrderData)
    exportDate = getDateOfExactFile(rawOrderData)

    orderLabelsDict = retrieveLabelDf(rawOrderData)
    return orderLabelsDict


def retrieveLabelDf(rawOrderData: DataFrame) -> dict:
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

    # Create new rows based on the quantities
    orderLabelData = explodeRows(orderLabelData)
    # Sort the labels per deliveryMethod
    routeDict = createDictPerRoute(orderLabelData)
    return routeDict


def explodeRows(df: DataFrame) -> DataFrame:
    """Extend teh dataframe per quantity.
    Example: if quantity of a row equals to 4, three extra rows will be added to the dataframe


    Args:
        df (DataFrame): Dataframe you want to extend

    Returns:
        DataFrame: Datframe with rows equal to the sum of the quantities
    """
    # make a new column containing a list of 1's with size equal to quantity value
    df["duplicates"] = df["quantity"].apply(lambda x: [1] * x)
    # Use the 'explode' method to create new rows for each entry in the 'duplicates' list
    df = df.explode("duplicates")
    # Replace the 'quantity' column with the 'duplicates' column and drop the 'duplicates' column
    df["quantity"] = df["duplicates"]
    df = df.drop(columns=["duplicates"])
    return df


def createDictPerRoute(orderLabelData: DataFrame) -> dict:
    """Sort the labels per deliveryRoute into a dictionary

    Args:
        orderLabelData (DataFrame): The labels you want to sort

    Returns:
        dict: Sorted dictionary with keys equal to the deliveryRoute. Values are dataFrames with the label data
    """
    routes = orderLabelData["deliveryMethod"].unique()
    routesDict = {}
    for route in routes:
        routesDict[route] = orderLabelData[orderLabelData["deliveryMethod"] == route]
    return routesDict

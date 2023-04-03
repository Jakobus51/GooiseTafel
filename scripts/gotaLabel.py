import pandas as pd
from scripts.gsHelpers import getDateVerkoop, prepareExactData
from scripts.constants import orders, customers


def retrieveLabelDf(rawOrderData: pd.DataFrame) -> pd.DataFrame:
    """checks which customers are in the orderData but not in the customer data

    Args:
        rawOrderData (pd.DataFrame): Exact output containing every customer who ordered in a given timespan
        rawCustomerData (pd.DateFrame): Exact output containing all customers

    Returns:
        pd.DataFrame: Dataframe of all customers who have yet to order
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


if __name__ == "__main__":
    filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\gotalabel-orders.xlsx"
    rawOrderData = pd.read_excel(filePathOrders, header=None)

    date = getDateVerkoop(rawOrderData)

    result = retrieveLabelDf(rawOrderData)
    print(result)

import pandas as pd
from helperFunctions import getDateVerkoop, prepareExactData
from constants import orders, customers


def retrieveOrderQuantity(
    rawOrderData: pd.DataFrame, rawCustomerData: pd.DateFrame
) -> pd.DataFrame:
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


if __name__ == "__main__":
    filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\kal-orders.xlsx"
    filePathCustomers = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\klanten-bestand.xlsx"

    dfOrders = pd.read_excel(filePathOrders, header=None)
    dfCustomers = pd.read_excel(filePathCustomers, header=None)

    date = getDateVerkoop(dfOrders)

    result = retrieveOrderQuantity(dfOrders, dfCustomers)
    print(result)

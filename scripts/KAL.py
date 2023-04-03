from pandas import DataFrame, read_excel
from scripts.gsHelpers import getDateVerkoop, prepareExactData
from scripts.constants import orders, customers, KalPDF
from numpy import arange


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


def displayDataFrame(
    data: DataFrame,
) -> DataFrame:
    """Only retrieves the columns you want to display and give them proper names
    Also adds numbers in front

    Args:
        data (DataFrame): The original dataframe containing all columns

    Returns:
        DataFrame: Dataframe with only columns you want to be shown
    """
    data = data[KalPDF.dataDisplayColumns]
    data.set_axis(KalPDF.pdfDisplayColumns, axis=1, inplace=True)
    data.insert(loc=0, column="#", value=arange(len(data)))
    return data


# if __name__ == "__main__":
#     filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\kal-orders.xlsx"
#     filePathCustomers = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\klanten-bestand.xlsx"

#     rawOrderData = read_excel(filePathOrders, header=None)
#     rawCustomerData = read_excel(filePathCustomers, header=None)

#     date = getDateVerkoop(rawOrderData)

#     result = retrieveCustomersYetToOrder(rawOrderData, rawCustomerData)
#     print(result)

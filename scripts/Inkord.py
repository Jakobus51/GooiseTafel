from pandas import DataFrame, read_excel
from scripts.gsHelpers import getDateVerkoop, prepareExactData
from scripts.constants import orders, InkordPDF
from numpy import arange


def retrieveOrderQuantity(rawOrderData: DataFrame) -> DataFrame:
    """Sums the orders using their productIds.
        0004w, 0004k, 0004P get summed together

    Args:
        data (DataFrame): A dataframe of an exact export of the orders sorted by article

    Returns:
        DataFrame: A dataframe where products are summed
    """
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


def displayDataFrame(
    data: DataFrame,
) -> DataFrame:
    """Only retrieves the columns you want to display and give them proper names

    Args:
        data (DataFrame): The original dataframe containing all columns

    Returns:
        DataFrame: Dataframe with only columns you want to be shown
    """
    data = data[InkordPDF.dataDisplayColumns]
    data.set_axis(InkordPDF.pdfDisplayColumns, axis=1, inplace=True)
    return data


# if __name__ == "__main__":
#     filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\inkord-orders.xlsx"
#     rawOrderData = read_excel(filePathOrders, header=None)
#     date = getDateVerkoop(rawOrderData)

#     result = retrieveOrderQuantity(rawOrderData)
#     print(result)

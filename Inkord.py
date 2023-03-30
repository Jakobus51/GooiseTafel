import pandas as pd
from helperFunctions import getDateVerkoop, prepareExactData
from constants import orders


def retrieveOrderQuantity(rawData: pd.DataFrame) -> pd.DataFrame:
    """Sums the orders using their productIds.
        0004w, 0004k, 0004P get summed together

    Args:
        data (pd.DataFrame): A dataframe of an exact export of the orders sorted by article

    Returns:
        pd.DataFrame: A dataframe where products are summed
    """
    data = prepareExactData(rawData, orders.ankerWord, orders.columnNamesArticles)

    # Fill nan values with the cell value above it for the columns "productId" and "productName"
    data[["productId", "productName"]] = data[["productId", "productName"]].fillna(
        method="ffill"
    )

    # use str.replace() to remove non-numeric characters from the 'productId' column
    data["productId"] = data["productId"].str.replace(r"\D+", "")

    # Check if cell contains a "-" if that is the case, remove all characters to the right of it
    data["productName"] = data["productName"].astype(str)
    data["productName"] = data["productName"].apply(
        lambda x: x[: x.rfind("-")] if "-" in x else x
    )

    # Create a dictionary which connects the productIds with the productNames
    prod_dict = dict(zip(data["productId"], data["productName"]))

    # Sum the quantities of entries with the same productId and make a dataFrame of it
    summed = data.groupby("productId")["quantity"].sum()
    summedDf = summed.to_frame().reset_index()

    # Create new column with the productNames based on the productIds
    summedDf["productName"] = summedDf["productId"].map(prod_dict)

    return summedDf


if __name__ == "__main__":
    filePathOrders = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\inkord-orders.xlsx"
    dfOrders = pd.read_excel(filePathOrders, header=None)
    date = getDateVerkoop(dfOrders)

    result = retrieveOrderQuantity(dfOrders)
    print(result)

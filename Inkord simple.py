import pandas as pd
from helperFunctions import getDateVerkoop, dropFirstRowsVerkoop, dropNanColumns


def retrieveOrderQuantity(data: pd.DataFrame):
    data = dropFirstRowsVerkoop(data)
    data = dropNanColumns(data)
    # Set column names
    columnNames = [
        "orderId",
        "orderItem",
        "customerId",
        "customerName",
        "quantity",
        "orderData",
        "deliveryMethod",
    ]
    data.set_axis(columnNames, axis=1, inplace=True)

    # Fill nan values with the cell value above it for the columns "orderId" and "orderItem"
    data[["orderId", "orderItem"]] = data[["orderId", "orderItem"]].fillna(
        method="ffill"
    )

    return data.groupby("orderItem")["quantity"].sum()


if __name__ == "__main__":
    filePathTest = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\inkord-orders.xlsx"
    dfInkord = pd.read_excel(filePathTest, header=None)
    date = getDateVerkoop(dfInkord)

    result = retrieveOrderQuantity(dfInkord)
    print(result)

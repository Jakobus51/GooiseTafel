import pandas as pd
from scripts.gsHelpers import prepareExactData, prepareLightSpeedData
from scripts.constants import orders, customers


def matchWebShopCustomers(
    dfWebShopRaw: pd.DataFrame, dfCustomersRaw: pd.DataFrame
) -> pd.DataFrame:
    webShopData = prepareLightSpeedData(dfWebShopRaw)
    customerData = prepareExactData(
        dfCustomersRaw, customers.ankerWord, customers.columnNames
    )

    # Set types and lowercase all columns that are compared
    webShopColumns = ["Lastname", "Zipcode", "Streetname", "E-mail"]
    webShopData[webShopColumns] = webShopData[webShopColumns].astype(str)
    webShopData[webShopColumns] = webShopData[webShopColumns].apply(
        lambda x: x.str.lower()
    )
    webShopData["Number"] = webShopData["Number"].astype(int)

    customerColumns = ["customerName", "address", "zipCode", "email"]
    customerData[customerColumns] = customerData[customerColumns].astype(str)
    customerData[customerColumns] = customerData[customerColumns].apply(
        lambda x: x.str.lower()
    )

    # merge webShopData with customerData on email and zipCode, returns only entries that were matched
    webShopMatched = pd.merge(
        webShopData,
        customerData,
        left_on=["E-mail", "Zipcode"],
        right_on=["email", "zipCode"],
    )

    # Checks which entries in the webShop are not yet matched and call them remaining
    maskRemaining = webShopData["OrderID"].isin(webShopMatched["OrderID"])
    webShopDataRemaining = webShopData[~maskRemaining]

    if webShopDataRemaining.size == 0:
        print()


if __name__ == "__main__":
    filePathWebShop = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\Input\webshop-orders.csv"
    filePathCustomers = r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\code\script-blueprints\Input\klanten-bestand.xlsx"

    dfWebShopRaw = pd.read_excel(filePathWebShop, header=None)
    dfCustomersRaw = pd.read_excel(filePathCustomers, header=None)

    result = matchWebShopCustomers(dfWebShopRaw, dfCustomersRaw)

    print(result)

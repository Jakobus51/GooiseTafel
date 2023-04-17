from pandas import DataFrame, merge, to_datetime, read_csv, read_excel
from backEnd.gtHelpers import prepareExactData, prepareLightSpeedData
from backEnd.constants import customers, liexCsvExport
from pathlib import Path


def runLiex(filePathWebShop: Path, filePathCustomers: Path, exportFolder: Path) -> None:
    """Links the webshop orders to Exact customers and creates a csv of the orders which can be imported into Exact

    Args:
        filePathWebShop (Path): Location of the orders from the webshop (lightSpeed)
        filePathCustomers (Path): Location of the customer DB which is an exact export
        exportFolder (Path): Place where you want to save the csv
    """
    dfWebShopRaw = read_csv(filePathWebShop, sep="delimiter", header=None)
    dfCustomersRaw = read_excel(filePathCustomers, header=None)

    matchedOrders = matchWebShopCustomers(dfWebShopRaw, dfCustomersRaw)
    exportableOrders = prepareCsv(matchedOrders)
    dateRange = getDateRange(exportableOrders)
    saveAsCsv(exportFolder, exportableOrders, dateRange)


def matchWebShopCustomers(
    dfWebShopRaw: DataFrame, dfCustomersRaw: DataFrame
) -> DataFrame:
    """Links the webShop orders to the correct exact customer on zipcode and email
    Returns a csv which can be imported into exact to automatically set the new orders into exact

    Args:
        dfWebShopRaw (DataFrame): The export out of the webShop (lightSpeed) orders you want to put into exact
        dfCustomersRaw (DataFrame): The complete customer database

    Returns:
        DataFrame: Datframe which is ready to be converted into a csv for Exact import, all columns are already in the correct form
    """
    webShopData = prepareLightSpeedData(dfWebShopRaw)
    customerData = prepareExactData(
        dfCustomersRaw, customers.ankerWord, customers.columnNames
    )

    # # Set types and lowercase all columns that are compared
    # webShopColumns = ["Lastname", "Zipcode", "Streetname", "E-mail"]
    # webShopData[webShopColumns] = webShopData[webShopColumns].astype(str)
    # webShopData[webShopColumns] = webShopData[webShopColumns].apply(
    #     lambda x: x.str.lower()
    # )
    # webShopData["Number"] = webShopData["Number"].astype(int)

    # customerColumns = ["customerName", "address", "zipCode", "email"]
    # customerData[customerColumns] = customerData[customerColumns].astype(str)
    # customerData[customerColumns] = customerData[customerColumns].apply(
    #     lambda x: x.str.lower()
    # )

    # Set types and lowercase all columns that are compared
    webShopColumns = ["Zipcode", "E-mail"]
    webShopData[webShopColumns] = webShopData[webShopColumns].astype(str)
    webShopData[webShopColumns] = webShopData[webShopColumns].apply(
        lambda x: x.str.lower()
    )
    customerColumns = ["zipCode", "email"]
    customerData[customerColumns] = customerData[customerColumns].astype(str)
    customerData[customerColumns] = customerData[customerColumns].apply(
        lambda x: x.str.lower()
    )

    # merge webShopData with customerData on email and zipCode, returns only entries that were matched
    webShopMatched = merge(
        webShopData,
        customerData,
        left_on=["E-mail", "Zipcode"],
        right_on=["email", "zipCode"],
    )

    # Checks which entries in the webShop are not yet matched and call them remaining
    maskRemaining = webShopData["Order_ID"].isin(webShopMatched["Order_ID"])
    webShopDataRemaining = webShopData[~maskRemaining]

    # Check if some webShop Orders are unmatched
    if webShopDataRemaining.size == 0:
        return webShopMatched

    else:
        print("Some orders were not matched")


def prepareCsv(webShopMatched: DataFrame) -> DataFrame:
    """Save only columns that are needed for the exact import
    Extract the dates for the orderDate and deliveryDate

    Args:
        webShopMatched (DataFrame): Dataframe containing all relevant data which needs to be filtered

    Returns:
        DataFrame: Datframe which can directly be converted to a csv
    """
    webShopMatched = webShopMatched[liexCsvExport.dataColumnNames]
    webShopMatched.set_axis(liexCsvExport.csvColumnNames, axis=1, inplace=True)
    webShopMatched["orderDate"] = webShopMatched["orderDate"].str.extract(
        r"(\d{2}-\d{2}-\d{4})"
    )
    webShopMatched["deliveryDate"] = webShopMatched["deliveryDate"].str.extract(
        r"(\d{2}-\d{2}-\d{4})"
    )
    return webShopMatched


def getDateRange(data: DataFrame) -> str:
    """Retrieves the date range of when the orders were placed

    Args:
        data (DataFrame): Dataframe of all orders who are going to be imported into exact frm which ou want to get the date range

    Returns:
        str: a string of the date range which will be used in the file name
    """
    dataLocal = data.copy()
    dataLocal["orderDate"] = to_datetime(dataLocal["orderDate"], format="%d-%m-%Y")
    return (
        dataLocal["orderDate"].min().strftime("%d-%m-%Y")
        + " - "
        + dataLocal["orderDate"].max().strftime("%d-%m-%Y")
    )


def saveAsCsv(exportFolder: Path, exportableOrders: DataFrame, dateRange: str) -> None:
    """Saves the dataframe as a csv which can be imported int Exact

    Args:
        exportFolder (Path): The place where you want to save your csv
        exportableOrders (DataFrame): The orders that will be imported into exact
        dateRange (str): Range for which the online orders were taken, is used in the file name
    """
    exportFileName = f"liex ({dateRange}).csv"
    exportPath = exportFolder / exportFileName
    exportableOrders.to_csv(exportPath, header=False, index=False, sep=";")

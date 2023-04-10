from pandas import DataFrame
from re import search
from backEnd.constants import saveLocations as sl
from backEnd.constants import pdfEnum
from os import path, makedirs


def getDateOfExactFile(data: DataFrame) -> str:
    """
    Retrieve the date on which the Exact export was made

    Args:
        data (DataFrame): the Exact export you want toe date of

    Returns:
        str: The date if found, otherwise return empty string
    """
    # Define a regular expression to match the date pattern
    pattern = r"\d+\s+\w+\s+\d+"

    # Use the regular expression to search for the date in the string
    # sometimes Exact gives you an extra empty row so we check two rows, the second and third row
    for i in range(1, 3):
        match = search(pattern, data.iloc[i, 0])
        if match is not None:
            # Extract the matched date from the regular expression match
            date = match.group()
            return date


def getDeliveryDateRange(data: DataFrame) -> str:
    """
    Retrieve the date from a goederenlevering Exact export
    Find the word "Afleverdatum" which is in column C. Take value to the right of it

    Args:
        data (DataFrame): The exact export put into a dataFrame

    Returns:
        str: the date range for which the exact export was made
    """
    row_index = data.index[data.iloc[:, 2] == "Afleverdatum"].tolist()[0]
    return data.iloc[row_index, 3]


def dropFirstRows(data: DataFrame, ankerWord: str) -> DataFrame:
    """
    Drops all metadata infromation from a customer Exact export
    Find the word Relaties which is in column A. Keep all rows starting one underneath this row

    Args:
        data (DataFrame): The exact export containing all the meta data

    Returns:
        DataFrame: The exact export without the metadata
    """
    row_index = data.index[data.iloc[:, 0] == ankerWord].tolist()[0]
    return data.iloc[row_index + 2 :, :]


def prepareExactData(
    rawData: DataFrame, ankerWord: str, columnNames: list[str]
) -> DataFrame:
    """prepares the dataframe by removing unnecessary information

    Args:
        rawData (DataFrame): The exact export
        ankerWord (str): the word on which the metadata ends
        columnNames (list[str]): List of column names to be set

    Returns:
        DataFrame: Cleaned up dataFrame ready for use
    """
    data = dropFirstRows(rawData, ankerWord)
    data.dropna(axis=1, how="all", inplace=True)
    data.set_axis(columnNames, axis=1, inplace=True)
    return data


def prepareLightSpeedData(rawData: DataFrame) -> DataFrame:
    """prepares the dataframe by cleaning it up.
        We keep the column names given by LightSpeed

    Args:
        rawData (DataFrame): The LightSpeed Export

    Returns:
        DataFrame: Cleaned up dataFrame ready for use
    """

    data = rawData.iloc[:, 0].str.split(";", expand=True)
    # use original column names
    data.columns = data.iloc[0]
    data = data[1:]
    # remove " from all entries
    data = data.applymap(lambda x: x.replace('"', ""))
    return data


def setDirectories():
    """Creates all the directories needed for the application. Each one has an input and an output"""
    for location in [
        sl.default,
        sl.KALInput,
        sl.KALOutput,
        sl.GotaLabelInput,
        sl.GotaLabelOutput,
        sl.LiexInput,
        sl.LiexOutput,
        sl.InkordInput,
        sl.InkordOutput,
        sl.CustomersInput,
        sl.PakLijstInput,
        sl.PakLijstOutput,
    ]:
        if not path.exists(location):
            makedirs(location)


def getPdfColumnSpacing(type: pdfEnum):
    """Gets the column spacing for the given pdf.
    Should sum to one and the length should be equal to the number of column you want to show
    """
    if type == pdfEnum.Inkord:
        return [0.72, 0.12, 0.16]
    if type == pdfEnum.KAL:
        return [0.09, 0.10, 0.11, 0.10, 0.20, 0.25, 0.15]
    if type == pdfEnum.PakLijstCategory or type == pdfEnum.PakLijstRoute:
        return [0.85, 0.15]


def getDataDisplayColumn(type: pdfEnum):
    """Get the columns from the pdf you want to show on the pdf"""

    if type == pdfEnum.Inkord:
        return ["productName", "productId", "quantity"]
    if type == pdfEnum.KAL:
        return [
            "customerId",
            "customerName",
            "city",
            "phoneNumber",
            "email",
            "deliveryMethod",
            "customerRemarks2",
        ]
    if type == pdfEnum.PakLijstCategory or type == pdfEnum.PakLijstRoute:
        return ["productName", "quantity"]


def getPdfDisplayColumns(type: pdfEnum):
    """Get the column names you want to display on the actual pdf"""

    if type == pdfEnum.Inkord:
        return ["Product naam", "ID", "Hoeveelheid"]
    if type == pdfEnum.KAL:
        return [
            "Klant Nr.",
            "Naam",
            "Plaats",
            "Telefoon",
            "E-mail",
            "Route",
            "Opmerking",
        ]
    if type == pdfEnum.PakLijstCategory or type == pdfEnum.PakLijstRoute:
        return ["Product naam", "Hoeveelheid"]


def getPdfTitle(type: pdfEnum, deliveryDateRange: str):
    """Title used in the pdf as well as the pdf name"""

    if type == pdfEnum.Inkord:
        return f"InkOrd ({deliveryDateRange})"
    if type == pdfEnum.KAL:
        return f"KAL ({deliveryDateRange})"
    if type == pdfEnum.PakLijstCategory:
        return f"PakLijst TOTAAL ({deliveryDateRange})"
    if type == pdfEnum.PakLijstRoute:
        return f"PakLijst PER ROUTE ({deliveryDateRange})"


def getPdfMetaData(type: pdfEnum, deliveryDateRange: str, dateOfExactOutput: str):
    """Extra information that is shown on top of the page"""

    baseTextOrders = f"Uitdraai van alle gerechten die afgeleverd moeten worden<br/> tussen <strong>{deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/><br/>"
    baseTextCustomers = f"Uitdraai van alle actieve klanten die nog niet hebben besteld tussen <strong>{deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/>"

    if type == pdfEnum.Inkord:
        return baseTextOrders
    if type == pdfEnum.KAL:
        return baseTextCustomers
    if type == pdfEnum.PakLijstCategory:
        return baseTextOrders
    if type == pdfEnum.PakLijstRoute:
        return baseTextOrders

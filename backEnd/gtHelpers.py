from pandas import DataFrame
from re import search
from backEnd.constants import saveLocations as sl
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
    data.columns = columnNames
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
        sl.SingleLabelInput,
        sl.SingleLabelOutput,
        sl.GTVultInOutput,
        sl.MealOverviewInput,
        sl.OrderScanOutput,
    ]:
        if not path.exists(location):
            makedirs(location)


def explodeRows(data: DataFrame) -> DataFrame:
    """Extend the dataframe per quantity.
    Example: if quantity of a row equals to 4, three extra rows will be added to the dataframe
    Args:
        df (DataFrame): Dataframe you want to extend
    Returns:
        DataFrame: Datframe with rows equal to the sum of the quantities
    """
    # make a new column containing a list of 1's with size equal to quantity value
    data["duplicates"] = data["quantity"].apply(lambda x: [1] * x)
    # Use the 'explode' method to create new rows for each entry in the 'duplicates' list
    data = data.explode("duplicates")
    # Replace the 'quantity' column with the 'duplicates' column and drop the 'duplicates' column
    data["quantity"] = data["duplicates"]
    data = data.drop(columns=["duplicates"])
    return data

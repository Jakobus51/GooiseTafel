from pandas import DataFrame
from re import search
from backEnd.constants import saveLocations as sl
from os import path, makedirs
from pathlib import Path
from datetime import datetime, timedelta, date
import sys
import os


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

    # data = rawData.iloc[:, 0].str.split(";", expand=True)
    # # use original column names
    # data.columns = data.iloc[0]
    # data = data[1:]
    # # remove " from all entries
    # data = rawData.applymap(lambda x: x.replace('"', ""))

    # Quick fix to make it work with old code where reading in LightSpeed data went bit differently
    data = rawData.fillna("")

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
        sl.UALabelInput,
        sl.UALabelOutput,
        sl.OrderScanInput,
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


def saveAsCsv(exportFolder: Path, exportableOrders: DataFrame, title: str) -> None:
    """Saves the dataframe as a csv which can be imported into Exact

    Args:
        exportFolder (Path): The place where you want to save your csv
        exportableOrders (DataFrame): The orders that will be imported into exact
        title (str): title of the csv
    """

    exportFileName = f"{title}.csv"
    print(exportFolder)
    print(exportFileName)
    exportPath = exportFolder / exportFileName
    print(exportPath)
    exportableOrders.to_csv(exportPath, header=False, index=False, sep=";")


def get_days_in_week(week_number: int, year: int) -> list[datetime]:
    """Retrieve the dates given a weeknumber ans year

    Args:
        week_number (int): The weeknumber
        year (int): The year

    Returns:
        list[datetime]: List with first 6 days of the week
    """
    # first week of the year is based upon the 4th of Jan
    january_4 = date(year, 1, 4)

    # Find the Monday of the week that contains January 4th
    first_monday = january_4 - timedelta(days=january_4.weekday())

    # Calculate the start date of the desired week
    start_date = first_monday + timedelta(weeks=week_number - 1)

    # Generate dates for the entire week
    week_dates = [start_date + timedelta(days=i) for i in range(6)]
    return week_dates


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)


def setExternalPackages():
    """Adds external packages to the PATH so they can be used in the application"""
    PROJECT_PATH = resource_path(Path(__file__).parent)

    os.environ["PATH"] += os.pathsep + os.path.join(
        PROJECT_PATH, r"externalPackages\poppler-23.08.0\Library\bin"
    )

    os.environ["PATH"] += os.pathsep + os.path.join(
        PROJECT_PATH, r"externalPackages\tessarect"
    )

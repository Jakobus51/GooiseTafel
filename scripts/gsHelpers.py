from pandas import DataFrame
import re


def my_method():
    print("Hello, world!")


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
    match = re.search(pattern, data.iloc[1, 0])

    if match:
        # Extract the matched date from the regular expression match
        date = match.group()
        return date
    else:
        return " "


def getDateVerkoop(data: DataFrame) -> str:
    """
    Retrieve the date from a goederenlevering Exact export
    Find the word Afleverdatum which is in column C. Take value to the right of it

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
    data.columns = data.iloc[0]
    data = data[1:]
    data = data.applymap(lambda x: x.replace('"', ""))
    return data

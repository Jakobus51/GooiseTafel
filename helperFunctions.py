import pandas as pd


def getDateVerkoop(data: pd.DataFrame) -> str:
    """
    Retrieve the date from a goederenlevering Exact export
    Find the word Afleverdatum which is in column C. Take value to the right of it

    Args:
        data (pd.DataFrame): The exact export put into a dataFrame

    Returns:
        str: the date range for which the exact export was made
    """
    row_index = data.index[data.iloc[:, 2] == "Afleverdatum"].tolist()[0]
    return data.iloc[row_index, 3]


def dropFirstRows(data: pd.DataFrame, ankerWord: str) -> pd.DataFrame:
    """
    Drops all metadata infromation from a customer Exact export
    Find the word Relaties which is in column A. Keep all rows starting one underneath this row

    Args:
        data (pd.DataFrame): The exact export containing all the meta data

    Returns:
        pd.DataFrame: The exact export without the metadata
    """
    row_index = data.index[data.iloc[:, 0] == ankerWord].tolist()[0]
    return data.iloc[row_index + 2 :, :]


def prepareExactData(
    rawData: pd.DataFrame, ankerWord: str, columnNames: list[str]
) -> pd.DataFrame:
    """prepares the dataframe by removing unnecessary information

    Args:
        rawData (pd.DataFrame): The exact export
        ankerWord (str): the word on which the metadata ends
        columnNames (list[str]): List of column names to be set

    Returns:
        pd.DataFrame: Cleaned up dataFrame ready for use
    """
    data = dropFirstRows(rawData, ankerWord)
    data.dropna(axis=1, how="all", inplace=True)
    data.set_axis(columnNames, axis=1, inplace=True)
    return data


def prepareLightSpeedData(rawData: pd.DataFrame) -> pd.DataFrame:
    """prepares the dataframe By formatting it in a proper datafrma

    Args:
        rawData (pd.DataFrame): The LightSpeed Export

    Returns:
        pd.DataFrame: Cleaned up dataFrame ready for use
    """
    data = rawData.iloc[:, 0].str.split(";", expand=True)
    data.columns = data.iloc[0]
    data = data[1:]
    data = data.applymap(lambda x: x.replace('"', ""))
    return data

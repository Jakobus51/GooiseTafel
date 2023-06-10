from pandas import DataFrame, read_excel
from pathlib import Path
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from numpy import isnan
from datetime import datetime, timedelta
from backEnd.constants import date, uaLabel
from locale import setlocale, LC_TIME
from backEnd.dataClasses.uaLabelInterface import UALabelI


def fetchDeliveries(filePathOrders: Path):
    """Returns a LabelHelper data object which contains all information to create the labels


    Args:
        filePathOrders (Path): Location where the orders can be found

    Returns:
        LabelHelper: Contains all information to create the labels
    """
    rawMealOverview = read_excel(filePathOrders, header=None)
    weekNumber = getWeekNumber(rawMealOverview)

    labelsInput = LabelHelper(AppEnum.UALabel, f"Week {weekNumber}")

    labelsInput.labelsPerDeliveryRoute = sortMealOverview(rawMealOverview)
    return labelsInput


def sortMealOverview(rawMealOverview: DataFrame) -> dict:
    mealoverview = cleanRawData(rawMealOverview)

    return makeDictionariesPerDay(mealoverview)


def makeDictionariesPerDay(mealOverview: DataFrame) -> dict:
    # Set the dictionary where the meals will be saved in
    dict = {}

    # Iterate over the rows
    for index, row in mealOverview.iterrows():
        # Save the day and meal
        date = row["day"]
        meal = row["meal"]

        # Iterate over the columns of the row
        for location, value in row.items():
            # skip the day and meal columns so only the location columns are looped over
            if location not in ["day", "meal"]:
                # Skip the 0 and Nan columns
                if float(value) != 0 and not isnan(value):
                    # Split the location into the city and floor
                    splitLocation = location.split(" ", 1)
                    city = splitLocation[0]
                    floor = splitLocation[1] if len(splitLocation) > 1 else ""

                    # Save everything to label
                    label = UALabelI(date, city, floor, meal, value)

                    # Append the label to the dictionary, automatically makes a new one if it does not exist yet
                    dict.setdefault(date, []).append(label)

    return dict


def cleanRawData(rawMealOverview: DataFrame) -> DataFrame:
    """Prepares the dataframe by setting and removing all the needed data

    Args:
        rawMealOverview (DataFrame): The dataframe from the excel without any modifications

    Returns:
        DataFrame: The dataframe ready to obtain the labels from
    """
    # Remove unnecessary columns
    mealOverview = rawMealOverview.iloc[:, [0, 1, 10, 12, 13, 14, 15]]

    # Set column names
    mealOverview.columns = uaLabel.columnNames

    # Fill nan values with the cell value above it for the "day column"
    mealOverview["day"].fillna(method="ffill", inplace=True)

    # Remove all rows which do not contain a meal
    mealOverview = mealOverview[mealOverview["meal"].notna()]

    # Only keep the first part of the cell value, Which is the day spelled out
    mealOverview["day"] = mealOverview["day"].str.split().str[0]

    # Retrieve the dates of the week written as Maandag (12-06-2023)
    formattedDates = getFormattedDates(rawMealOverview)

    # Change the date column to use the above mentioned dates
    mealOverview["day"] = mealOverview["day"].apply(
        lambda x: getWholeDate(x, formattedDates)
    )

    return mealOverview


def getFormattedDates(rawMealOverview: DataFrame) -> list[str]:
    """Retrieve the formatted delivery dates from the excel to display in the checkbox list in the front end

    Args:
        rawMealOverview (DataFrame): The dataframe of the meal overview excel

    Returns:
        list[str]: The formatted dates
    """
    weekNumber = getWeekNumber(rawMealOverview)
    # Currently in the excel there is no year indication so it is set to 2023
    dates = getDatesFromWeekNumber(weekNumber, date.year)
    return formatDates(dates)


def getWeekNumber(rawMealOverview: DataFrame) -> int:
    """Retrives the weeknumber from the excel

    Args:
        rawMealOverview (DataFrame): The dataframe of the meal overview excel

    Returns:
        int: The week nunmber
    """
    weekNumberAndWeek = rawMealOverview.iloc[0, 0]
    week, number = weekNumberAndWeek.split()
    return int(number)


def getDatesFromWeekNumber(weekNr: int, year: int) -> list[datetime]:
    """get the dates from a specefic week given the year and week number

    Args:
        weekNr (int): Weeknumber of dates you want
        year (int): Year of dates you want

    Returns:
        list[datetime]: Days of the week
    """
    # Create a datetime object for the first day of the given week and year
    first_day = datetime.strptime(f"{year}-W{weekNr}-1", "%Y-W%W-%w").date()
    # Create a list of dates ranging from monday to saturday
    dates = [first_day + timedelta(days=i) for i in range(7)]
    return dates


def formatDates(dates: list[datetime]) -> list[str]:
    """_Retrieve the dates as Maandag (12-06-2023)

    Args:
        dates (list[datetime]): Unformatted dates

    Returns:
        list[str]: The formatted dates
    """

    # set to dutch to retrieve dutch written days (Maandag instead of Monday)
    setlocale(LC_TIME, "nl_NL")
    deliveryDates = []
    for date in dates:
        # Get the date written out
        weekday = date.strftime("%A").capitalize()
        # Get the numeric date
        date = date.strftime("%d-%m-%Y")
        deliveryDates.append(f"{weekday} ({date})")

    return deliveryDates


def getWholeDate(requestDate: str, formattedDates: list[str]) -> str:
    for formattedDate in formattedDates:
        if requestDate in formattedDate:
            return formattedDate

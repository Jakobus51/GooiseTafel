from backEnd.dataClasses.appEnum import AppEnum
from pandas import DataFrame, Series, read_excel, to_numeric
from pathlib import Path
from datetime import datetime, timedelta
from backEnd.dataClasses.customErrors import MealOverviewError
from backEnd.gtHelpers import saveAsCsv
from backEnd.constants import delivery


class GTVultIn:
    """Class containing all information needed for the creation of orders used in GTVultIn and OrderScan"""

    type: AppEnum  # What kind of app
    mealOverviewRaw: DataFrame  # Raw meal overview excel put into a Dataframe
    orderDaysDict: dict  # Dictionary with keys being the orderDay as written down in the excel and the value the corresponding dateTime object
    mealsAndCodesDict: dict  # Dictionary with keys being the meals written out and values the mealcodes
    displayOrders: DataFrame  # Dataframe containing information that is shown in the order overview in the front end
    KALcustomers: DataFrame  # Customers for which the orders are filled in, retrieved from the KAL aplication
    weekMenu: DataFrame  # Dataframe containing the weekmenu

    def __init__(self):
        self.type = AppEnum.GTVultIn
        self.displayOrders = self.initializeShowOrders()
        self.weekMenu = self.initializeWeekMenu()

    def initializeShowOrders(self) -> DataFrame:
        """Create an empty order dataframe used to display to the user

        Returns:
            DataFrame: Empty dataframe wherein the display orders will be shown
        """
        displayOrdersColumns = [
            "Klant nr.",
            "Klant",
            "Code",
            "Maaltijd",
            "Wanneer",
            "Afleverdatum",
            "Aantal",
        ]
        return DataFrame(columns=displayOrdersColumns)

    def initializeWeekMenu(self) -> DataFrame:
        """Create an empty week menu dataframe used to display to the user

        Returns:
            DataFrame: Empty dataframe wherein the display weekmenu will be shown
        """
        displayOrdersColumns = [
            "Wanneer",
            "Maaltijd",
            "Aantal",
        ]
        return DataFrame(columns=displayOrdersColumns)

    def setDisplayOrders(self, displayOrders: DataFrame):
        """Set the display Orders

        Args:
            displayOrders (DataFrame): Datframe containing the display orders
        """
        self.displayOrders = displayOrders

    def setWeekMenu(self, weekMenu: DataFrame):
        """Set the week menu

        Args:
            displayOrders (DataFrame): Datframe containing the week menu
        """
        self.weekMenu = weekMenu

    def setKALcustomers(self, KALcustomers: DataFrame):
        """Set the KAL customers

        Args:
            kalCustomers (DataFrame): Datframe containing the KAL customers retrieved from the KAL application
        """
        self.KALcustomers = KALcustomers

    def loadMealOverView(self, filePathMealOverview: Path):
        """When a meal overview is loaded in, convert it to a dataframe and retrieve the order days and the meals from it

        Args:
            filePathMealOverview (Path):The file location of the meal overview excel
        """
        self.mealOverviewRaw = self.getMealOverviewRaw(filePathMealOverview)
        self.orderDaysDict = self.getOrderDaysDict()
        self.mealsAndCodesDict = self.getMealsAndCodesDict()

    def getMealOverviewRaw(self, filePathMealOverview: Path) -> DataFrame:
        """set the excel into a dataframe without

        Args:
            filePathMealOverview (Path): Location of excel

        Returns:
            DataFrame: Dataframe containing the meal overview excel
        """
        return read_excel(filePathMealOverview, header=None)

    def getOrderDaysDict(self) -> dict:
        """Matches the orderDays from the excel to the corresponding dateTime objects
        Also filters out dates where you can not order, indicated with "GEEN"

        Returns:
            dict: Dictionary where the key is the orderDay as written down in the excel and the value the corresponding dateTime object.
            When an orderDay is indicated with KOELVERS, the deliveryday is equal to the one before it as it wil be delivered on that day
        """

        excelOrderDays = self.getExcelOrderDays()
        year, week = self.getWeekAndYear()
        dateTimeDays = self.getDatesFromWeekNumber(year, week)

        dateDict = {}
        for index, orderDay in enumerate(excelOrderDays):
            dateDict[orderDay] = dateTimeDays[index]

        # Remove the entry from the dictionary if it contains the word "GEEN"
        fitleredDateDict = {
            key: value for key, value in dateDict.items() if "GEEN" not in key
        }
        return fitleredDateDict

    def getExcelOrderDays(self) -> list[str]:
        """Retrieve the days on which customers can order

        Returns:
            list[str]: List of all order days
        """
        days = ["MA", "DI", "WO", "DO", "VR"]
        orderDays = []
        # Loop over the days until you find the row containing the days
        for index, day in enumerate(days):
            rowsContainingMask = self.mealOverviewRaw.iloc[:, index].str.contains(
                rf"\b{day}\b", na=False
            )
            # If you did not find a row containing "MA" in the first column, start again but now search for "DI" in the second column
            if ~rowsContainingMask.any():
                continue
            firstRowContaining = self.mealOverviewRaw.loc[rowsContainingMask.idxmax()]
            # Save first 6 entries which correspond to the different potential order days
            orderDays = firstRowContaining.iloc[:6].tolist()

            break

        if orderDays:
            # change the \n in a string to a space
            orderDaysMod = [orderDay.replace("\n", " ") for orderDay in orderDays]
            return orderDaysMod
        else:
            raise MealOverviewError("De dagen waarop klanten kunnen bestellen")

    def getDatesFromWeekNumber(self, weekNr: int, year: int) -> list[datetime]:
        """get the dates from a specefic week given the year and week number

        Args:
            weekNr (int): Weeknumber of dates you want
            year (int): Year of dates you want

        Returns:
            list[datetime]: First 6 days of the week; Monday to Saturday
        """
        # Create a datetime object for the first day of the given week and year
        first_day = datetime.strptime(f"{year}-W{weekNr}-1", "%Y-W%W-%w").date()
        # Create a list of dates ranging from monday to saturday
        dates = [first_day + timedelta(days=i) for i in range(6)]
        return dates

    def getWeekAndYear(self) -> tuple[int, int]:
        """Retrieves the weeknumber and year from the mealOverview dataframe

        Returns:
            tuple[int, int]: a tuple where first value is the year and the second value the week
        """
        try:
            # Metadata is alway in the first cell
            metaData = self.mealOverviewRaw.iloc[0, 0]
            # Find the "WEEK" word get the value next to it
            indexWeek = metaData.index("WEEK")
            metaDataList = metaData.split()
            weekAndYear = metaDataList[indexWeek + 1]

            # Split the year and week into two and convert to integers
            year, week = weekAndYear.split("-")
            return int(year), int(week)
        except:
            raise MealOverviewError("Het weeknummer en/of het jaar")

    def getMealsAndCodesDict(self) -> dict:
        """Retrieve the meals and codes of that meal from the meal overview dataframe

        Returns:
            dict: Keys are the meals written out, values are the mealcodes
        """
        # Find the first index of the cell containing "Code" in the 7th (G) column
        indexOfFirstCodeWord = self.mealOverviewRaw.index[
            self.mealOverviewRaw.iloc[:, 6] == "Code"
        ].tolist()[0]
        # Save all codes and meals underneath the "Code" word
        mealsAndCodes = self.mealOverviewRaw.iloc[indexOfFirstCodeWord:, 6:8]
        # Remove non numeric and NaN values
        mealsAndCodesCleaned = mealsAndCodes[
            to_numeric(mealsAndCodes.iloc[:, 0], errors="coerce").notnull()
        ]

        mealDict = {}
        # Iterate over the found meals and codes to add them to a dictionary
        for index, mealCode in mealsAndCodesCleaned.iterrows():
            # The column indexes are still in use so 6 is the code and 7 is the meal name
            mealDict[mealCode[7]] = str(mealCode[6])

        # Add Bezorgkosten to the dictionary
        mealDict["Bezorgkosten"] = delivery.code

        # Bezorgkosten is always added so if mealDict is bigger than 1 it succesfully imported the other meals as well
        if len(mealDict) > 1:
            return mealDict
        else:
            raise MealOverviewError("De maaltijden en/of de maaltijd codes")

    def addOrder(
        self,
        customerName: str,
        customerId: str,
        selectedMeal: str,
        selectedDateText: str,
        selectedQuantity: str,
    ):
        """Adds a new order to the display DF which is shown in the front end"""
        # Format the date into the correct format
        deliveryDate = self.orderDaysDict[selectedDateText].strftime("%d/%m/%Y")

        # If mealcode is the delivery code don't add a w or k to it
        if self.mealsAndCodesDict[selectedMeal] == delivery.code:
            mealCode = self.mealsAndCodesDict[selectedMeal]
        else:
            # If KOELVERS is in the selectedDateText add a k to the mealcode, otherwise a w
            suffix = "k" if "KOELVERS" in selectedDateText else "w"
            mealCode = self.mealsAndCodesDict[selectedMeal] + suffix

        # Create new row and add it to the data frame
        newRow = {
            "Klant": customerName,
            "Klant nr.": customerId,
            "Maaltijd": selectedMeal,
            "Code": mealCode,
            "Wanneer": selectedDateText,
            "Afleverdatum": deliveryDate,
            "Aantal": selectedQuantity,
        }
        # Reset the index before adding a new entry otherwise the last index may already be in use
        self.displayOrders.reset_index(drop=True, inplace=True)
        self.displayOrders.loc[len(self.displayOrders)] = newRow

    def addOrderToWeekMenu(
        self,
        selectedMeal: str,
        selectedDateText: str,
        selectedQuantity: str,
    ):
        """Adds a new order to the weekmenu df which is shown in the front end"""
        # Create new row and add it to the data frame
        newRow = {
            "Wanneer": selectedDateText,
            "Maaltijd": selectedMeal,
            "Aantal": selectedQuantity,
        }
        # Reset the index before adding a new entry otherwise the last index may already be in use
        self.weekMenu.reset_index(drop=True, inplace=True)
        self.weekMenu.loc[len(self.weekMenu)] = newRow

    def createCSv(self, displayOrdersFE: DataFrame, exportFolder: Path):
        """Makes the csv which can be imported into Exact

        Args:
            displayOrdersFE (DataFrame): Datframe which data will be used to make the csv
            exportFolder (Path): Location where the csv will be saved
        """
        exportableOrders = DataFrame()

        exportableOrders["customerId"] = displayOrdersFE["Klant nr."]
        exportableOrders["orderDate"] = datetime.now().strftime("%d/%m/%Y")
        year, week = self.getWeekAndYear()
        exportableOrders["orderId"] = self.getOrderIdColumn(
            exportableOrders["customerId"], year, week
        )
        exportableOrders["deliveryDate"] = displayOrdersFE["Afleverdatum"]
        exportableOrders["productId"] = displayOrdersFE["Code"]
        exportableOrders["quantity"] = displayOrdersFE["Aantal"]

        csvTitle = f"GTVultIn ({year}-{week})"
        saveAsCsv(exportFolder, exportableOrders, csvTitle)

    def getOrderIdColumn(self, customerIds: Series, year: int, week: int) -> Series:
        """Uses the customerIDs to create a customer orderID entry for each customer.

        Args:
            customerIds (Series): IDs of customers which will be used for numbering the
            year (int): Year of when orders were made
            week (int): Week of when orders were made

        Returns:
            Series: The column of orderIds based on the year, week and unique customer ids
        """
        # Initialize the dictionary counter
        customerMap = {}

        # Initialize a counter
        counter = 1

        # Iterate over the customer IDs
        for customer in customerIds:
            if customer not in customerMap:
                # Assign a new integer if the customer ID is not already in the map
                customerMap[customer] = counter
                counter += 1

        # Use the map to make a new column where the customers are numbered by their customerID
        customerNumbered = customerIds.map(customerMap)
        # Use customerNumbering to make tht orderID column for the orders
        orderIdColumn = (
            "GTS" + str(year) + str(week) + "-" + customerNumbered.astype(str)
        )
        return orderIdColumn

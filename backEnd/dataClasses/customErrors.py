class UnMatchedOrdersError(Exception):
    """Exception raised when orders from Lightspeed in the Liex app could not be matched to exact customers

    Attributes:
        unmatchedErrors -- DataFrame containing all the unmatched orders
        message -- Message which contains the names of the people who could not be matched
    """

    def __init__(self, unmatchedErrors):
        # Only save unique customers (order file contains mulitple rows for different orders of same customer)
        uniqueWebShopDatRemaining = unmatchedErrors.drop_duplicates(
            subset=["Order_ID"], keep="first"
        )

        # construct error message
        errorMessage = "Kan de orders van de volgende klant(en) niet matchen:\r\n"
        for index, row in uniqueWebShopDatRemaining.iterrows():
            errorMessage += "-" + row["Firstname"] + " " + row["Lastname"] + "\r\n"
        errorMessage += "\r\nControleer of de e-mail en postcode goed staan in zowel Exact als Lightspeed"

        self.message = errorMessage
        super().__init__(self.message)


class MealOverviewError(Exception):
    """Exception raised when parts of the meal overview could not be retrieved

    Attributes:
        location -- location where the error happened
        message -- Message which contains the names of the people who could not be matched
    """

    def __init__(self, location):
        errorMessage = f"Kan het volgende niet uitlezen uit de maaltijd overzicht excel:\r\n\r\n{location}\r\n\r\nControleer of de ingeladen maaltijd overzicht correct is"

        self.message = errorMessage
        super().__init__(self.message)

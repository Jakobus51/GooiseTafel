from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.mealLabelInterface import MealLabelI
from backEnd.dataClasses.uaLabelInterface import UALabelI
from backEnd.gtHelpers import explodeRows
from numpy import sort


class LabelHelper:
    """Class containing all information needed for the creation of the printable labels"""

    type: AppEnum  # What kind of app, can be GotaLabel, SingleLabel or UALabel
    labelsPerDeliveryRoute: dict  # Data from which the labels will be made, sorted per deliveryRoute (which are the days for UALabel)
    labels: list[
        MealLabelI or UALabelI
    ]  # List of the actual labels that will be printed
    deliveryRoutesToPrint: dict  # Filtered routes based on selection of user in the frond end
    dateOfOrders: str

    def __init__(self, type: AppEnum, dateOfOrders: str):
        self.type = type
        self.dateOfOrders = dateOfOrders
        self.labelsPerDeliveryRoute = None
        self.labels = None
        self.deliveryRoutesToPrint = None

    def setTableData(self, labelDataPerDeliveryMethod):
        self.labelsPerDeliveryRoute = labelDataPerDeliveryMethod

    def setRoutesToPrint(self, routesToPrint):
        self.deliveryRoutesToPrint = routesToPrint

    def setLabels(self, labels):
        self.labels = labels

    def getDictionaryKeys(self):
        """get the keys of the labelDataPerDeliveryMethod dictionary if it exists

        Returns:
            list(str): The list of the delivery routes, uses list() to show it correctly in the front end
        """
        if self.labelsPerDeliveryRoute is not None:
            return list(self.labelsPerDeliveryRoute.keys())
        else:
            return []

    def getCustomerNamesFromKey(self, key):
        """Retrieves the customer names for a given delivery method

        Args:
            key (string): Name of the route

        Returns:
            list(str): a list with customers, uses list() to show it correctly in the front end
        """
        if self.labelsPerDeliveryRoute is not None:
            data = self.labelsPerDeliveryRoute[key]
            customers = sort(data["customerName"].unique())
            return list(customers)
        else:
            return []

    def getProductsForCustomer(self, key, customerName):
        """Retrieves all the meals for a given customer

        Args:
            key (str): The delivery route of the customer
            customerName (str): Name of the customer

        Returns:
            list(str): A list of all meals for the given customer,  uses list() to show it correctly in the front end
        """
        if self.labelsPerDeliveryRoute is not None:
            data = self.labelsPerDeliveryRoute[key]
            customerOrders = data[data["customerName"] == customerName]
            productNames = sort(customerOrders["productName"].unique())
            return list(productNames)
        else:
            return []

    def getProduct(self, key, customerName, productName):
        """Retrieve the given product for a given product, contains all the information to make the label

        Args:
            key (str): Name of the delivery route
            customerName (str): Name of the customer
            productName (str): Name of the product

        Returns:
            Row of DF: Contains all information to make the label
        """
        if self.labelsPerDeliveryRoute is not None:
            data = self.labelsPerDeliveryRoute[key]
            customerOrders = data[data["customerName"] == customerName]
            product = customerOrders[data["productName"] == productName]
            return product
        else:
            return []

    def setLabelsFromRouteDictionaries(self):
        """Make labels for all the selected delivery routes (the ones contained in routesToPrint)
        And save these labels to the labels property of this class
        """
        labels = []
        for key in self.deliveryRoutesToPrint:
            extendedLabelDataPerRoute = explodeRows(self.deliveryRoutesToPrint[key])
            for index, row in extendedLabelDataPerRoute.iterrows():
                labels.append(
                    MealLabelI(
                        row["customerName"],
                        row["customerId"],
                        row["address"],
                        row["zipCode"],
                        row["city"],
                        row["phoneNumber"],
                        row["deliveryDate"],
                        row["productName"],
                        row["customerRemarks1"],
                    )
                )
        self.labels = labels

    def setLabelsFromDayDictionaries(self):
        labels = []
        for key in self.deliveryRoutesToPrint:
            labels.extend(self.deliveryRoutesToPrint[key])

        self.labels = labels

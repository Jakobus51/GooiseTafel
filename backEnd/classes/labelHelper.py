from backEnd.classes.appEnum import AppEnum
from backEnd.classes.labelInterface import GTlabel
from backEnd.gtHelpers import explodeRows


class LabelHelper:
    """Class containing all information needed for the creation of a pdf"""

    type: AppEnum  # What kind of app, will always be GotaLabel for the LabelHelper class
    labelDataPerDeliveryMethod: dict  # Data from which the labels will be made, sorted per deliveryMethod
    # deliveries: dict #Some extra information
    labels: list[GTlabel]  # List of the actual labels that will be printed
    routesToPrint: dict  # Filtered routes based on selection of user in the frond end

    def __init__(self, type: AppEnum):
        self.type = type
        self.labelDataPerDeliveryMethod = None
        self.labels = None

    def setTableData(self, labelDataPerDeliveryMethod):
        self.labelDataPerDeliveryMethod = labelDataPerDeliveryMethod

    def setRoutesToPrint(self, routesToPrint):
        self.routesToPrint = routesToPrint

    def setLabels(self, labels):
        print("succes")
        self.labels = labels

    def getDictionaryKeys(self):
        if self.labelDataPerDeliveryMethod is not None:
            return list(self.labelDataPerDeliveryMethod.keys())
        else:
            return []

    def getCustomerNamesFromKey(self, key):
        if self.labelDataPerDeliveryMethod is not None:
            data = self.labelDataPerDeliveryMethod[key]
            customers = data["customerName"].unique()
            return list(customers)
        else:
            return []

    def getProductsForCustomer(self, key, customerName):
        if self.labelDataPerDeliveryMethod is not None:
            data = self.labelDataPerDeliveryMethod[key]
            customerOrders = data[data["customerName"] == customerName]
            productNames = customerOrders["productName"].unique()
            return list(productNames)
        else:
            return []

    def getProduct(self, key, customerName, productName):
        if self.labelDataPerDeliveryMethod is not None:
            data = self.labelDataPerDeliveryMethod[key]
            customerOrders = data[data["customerName"] == customerName]
            product = customerOrders[data["productName"] == productName]
            return product
        else:
            return []

    def setLabels(self):
        labels = []
        for key in self.routesToPrint:
            extendedLabelDataPerRoute = explodeRows(self.routesToPrint[key])
            for index, row in extendedLabelDataPerRoute.iterrows():
                labels.append(
                    GTlabel(
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

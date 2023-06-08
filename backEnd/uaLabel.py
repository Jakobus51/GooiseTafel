from pandas import DataFrame, read_excel
from pathlib import Path
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from numpy import sort


def fetchDeliveries(filePathOrders: Path):
    """Returns a LabelHelper data object which contains all information to create the labels


    Args:
        filePathOrders (Path): Location where the orders can be found

    Returns:
        LabelHelper: Contains all information to create the labels
    """
    rawOrderData = read_excel(filePathOrders, header=None)

    deliveryDateRange = getDeliveryDateRange(rawOrderData)

    labelsInput = LabelHelper(AppEnum.UALabel, deliveryDateRange)

    labelsInput.labelsPerDeliveryRoute = sortOrders(rawOrderData)
    return labelsInput

def getDeliveryDateRange(rawOrderData: DataFrame):
    

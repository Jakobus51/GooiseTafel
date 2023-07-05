from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.mealLabelInterface import MealLabelI
from backEnd.constants import saveLocations as sl
from backEnd.labelCreator import LabelCreator

if __name__ == "__main__":
    labelInput = LabelHelper(AppEnum.GotaLabel, "16-04-2023")

    lCustomerName = "Jakob van Jakobsen Met Een Hele Lange Achternaam"
    lCustomerId = "123456789"
    lAddress = "Hele Lange Weg Straat en Laan 95126A - app 49 (Gebouw A)"
    lZipCode = "1234 AB"
    lCity = "ROTTERDAM"
    lPhoneNumber = "06 40559395/ 076 5216952"
    lDeliveryDate = "27-03-2023"
    lProductName = "NATRIUMARM Lekkerbek Hollandaisesaus, snijbonen& puree-warm"
    lCustomerRemarks1 = "Ma-di-wo, speciaal afleveren via de achterdeur"

    lCustomerName2 = "Jakob Damen"
    lAddress2 = "Straatweg 9D"
    lPhoneNumber2 = "06 40559395"
    lProductName2 = "Frietje speciaal"

    labelInput.setLabels(
        [
            MealLabelI(
                lCustomerName,
                lCustomerId,
                lAddress,
                lZipCode,
                lCity,
                lPhoneNumber,
                lDeliveryDate,
                lProductName,
                lCustomerRemarks1,
            ),
            MealLabelI(
                lCustomerName2,
                lCustomerId,
                lAddress2,
                lZipCode,
                lCity,
                lPhoneNumber,
                lDeliveryDate,
                lProductName2,
                lCustomerRemarks1,
            ),
        ]
    )
    LabelCreator(labelInput, sl.GotaLabelOutput)

    print("Finished label creator run")

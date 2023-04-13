from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.labelInterface import GTlabel
from backEnd.constants import saveLocations as sl
from backEnd.labelCreator import createLabels

if __name__ == "__main__":
    labelInput = LabelHelper(AppEnum.GotaLabel)

    lCustomerName = "Jakob van Jakobsen Met Een Hele Lange Achternaam"
    lCustomerId = "123456789"
    lAddress = "Hele Lange Weg Straat en Laan 95126A - app 49 (Gebouw A)"
    lZipCode = "1234 AB"
    lCity = "ROTTERDAM"
    lPhoneNumber = "06 40559395/ 076 5216952"
    lDeliveryDate = "27-03-2023"
    lProductName = "NATRIUMARM Lekkerbek Hollandaisesaus, snijbonen& puree-warm"
    lCustomerRemarks1 = "test 4. size: 95x48, margins: t=3, b=3, r=3, l=3"

    lCustomerName2 = "Jakob Damen"
    lAddress2 = "Straatweg 9D"
    lPhoneNumber2 = "06 40559395"
    lProductName2 = "Frietje speciaal"

    labelInput.setLabels(
        [
            GTlabel(
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
            GTlabel(
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
    createLabels(labelInput, sl.GotaLabelOutput)

    print("Finished label creator run")

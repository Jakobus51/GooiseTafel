from backEnd.dataClasses.appEnum import AppEnum
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.uaLabelInterface import UALabelI
from backEnd.constants import saveLocations as sl
from backEnd.labelCreator import LabelCreator

# To run: $ python -m liveTests.uaLabelCreator
if __name__ == "__main__":
    labelInput = LabelHelper(AppEnum.UALabel, "Week 25")

    lday = "Maandag (12-06-2023)"
    lcity = "Leusden"
    llocation = ""
    lprodcut = "Rode Kool"
    lquantity = "20"

    lday2 = "Maandag (12-06-2023)"
    lcity2 = "Hilversum"
    llocation2 = "1ste verdieping"
    lprodcut2 = "Klapstuk (rund) gegaard borstlapje Let op 15 stuks in 1 bak"
    lquantity2 = "109"

    labelInput.setLabels(
        [
            UALabelI(lday, lcity, llocation, lprodcut, lquantity, 0),
            UALabelI(lday2, lcity2, llocation2, lprodcut2, lquantity2, 1),
        ]
    )
    LabelCreator(labelInput, sl.UALabelOutput)

    print("Finished label creator run")

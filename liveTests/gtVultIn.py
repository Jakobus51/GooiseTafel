from backEnd.gtVultIn import GTVultIn
from backEnd.constants import saveLocations as sl


if __name__ == "__main__":
    MealOverviewFile = "maaltijdoverzicht week 22-2023 koningsdag.xlsx"
    filePathMealOverview = sl.MealOverviewInput / MealOverviewFile

    gtVultIn = GTVultIn()
    gtVultIn.loadMealOverView(filePathMealOverview)
    print("Finished gtVultIn retrieval")

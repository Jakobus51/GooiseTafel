from pandas import read_excel


def getOrderDays(filePathOrders):
    mealOverviewRaw = read_excel(filePathOrders, header=None)

    days = ["MA", "DI", "WO", "DO", "VR"]
    orderDays = []
    for index, day in enumerate(days):
        print(index, day)
        # Find first row where MA can be found, save that row
        rowsContainingMask = mealOverviewRaw.iloc[:, index].str.contains(
            rf"\b{day}\b", na=False
        )
        if ~rowsContainingMask.any():
            continue
        firstRowContaining = mealOverviewRaw.loc[rowsContainingMask.idxmax()]
        orderDays = firstRowContaining.iloc[:6].tolist()
        break

    if orderDays:
        print("Days found")
        return orderDays
    else:
        print("No days found")

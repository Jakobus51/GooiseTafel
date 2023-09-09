class GetImages:
    ROTATION_SEARCH = 20 #Angle which it will search for the optimum, will be -20 and 20 from original
    ANGLE_INCREASE = 0.2 #Amount of angle that is increased in each loop
    BLACK_ROW_THRESHOLD = 0.95 #How much black a row must contain to be classified as black
    SIDE_CUT_SIZE = 400 #Amount of pixels that get cut off on the sides of the image that gets angle searched
    PADDING = 1000
    
class MetaDataRow:
    HEIGHTH_MIN = 120 #The minimum height the meta data row can be
    HEIGHTH_MAX = 200 #The maximum height the meta data row can be
    WIDTH_MIN_PERCENTAGE = 0.7 #The minimum percentage of the width of the original image the metadata row has to be
    
class GetCells:
    #Size constraint for something to be classified a cell in the table
    HEIGHTH_MIN =50
    HEIGHTH_MAX =80
    WIDTH_MIN = 200
    WIDTH_MAX = 400
    PADDING = 1000

class ReadImage:
    MEAL_CODE_COLUMN = 6 #Column where the meal coes are in
    KOELVERS_WEEKEND_COLUMN = 5 #Column where the meal coes are in
    DAY_ROWS = [0,4,25] # Rows where hte order days are in
    EMPTY_ROW = 32 #Last row which is always empty (contains the apple and diabetic message)
    RATIO_OF_FILLED_CIRCLE = 0.3 #Maximum ratio the white/black pixels can be for a circle to be filled
    TEXT_CELL_INCREASE =4 #Amount of pixels to all sides the cell gets increased before extracting text
    KOELVERS_SIGNAL_WORDS = ["KOELVERS", "VERS", "weekend"]
    
class GetClientID:
    WIDTH_PERCENTAGES = [0.10, 0.08, 0.06, 0.04, 0.02, 0.12] #% of the right-side of the page you keep to look for the customer number
    HEIGHT_PERCENTAGE = 0.50 #% of the bottom-side of the page you keep to look for the customer number
    
class OrderScanCsv:
    WEEKDAY_MAP = {'MA': 0, 'DI': 1, 'WO': 2, 'DO': 3, 'VR': 4 }
    CSV_COLUMNS = [
        "customerId",
        "orderDate",
        "orderId",
        "deliveryDate",
        "productId",
        "quantity",
    ]

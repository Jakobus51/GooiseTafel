# import sys

# sys.path.append("/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages")

# import module
from pytesseract import image_to_string
import cv2
from numpy import ndarray, count_nonzero, all
from backEnd.orderScan.get_table_cells import get_ordered_table_cells
from backEnd.orderScan.constants import ReadImage
from backEnd.dataClasses.customErrors import OrderScanError
from backEnd.orderScan.constants import OrderScanCsv
import matplotlib.pyplot as plt


def get_orders(img: ndarray, plot: bool):
    table_cells = get_ordered_table_cells(img, plot)
    if plot:
        test_order_days(table_cells, img)
        test_meal_codes(table_cells, img)

    orders = get_order_codes(table_cells, img)

    return orders


def get_order_codes(cells: list[list[ndarray]], img: ndarray):
    """Get the codes and days where customers orders (filled in the circle)

    Args:
        cells (list[list[ndarray]]): All the different cells in the table
        img (ndarray): black and white of image

    Returns:
        _type_: _description_
    """

    orders = []
    filled_circles = get_filled_circles(cells, img)
    for filled_circle in filled_circles:
        i, j = filled_circle[0], filled_circle[1]
        order_day = get_order_day(cells, img, j)
        meal_code = get_text_from_cell(
            cells[i][ReadImage.MEAL_CODE_COLUMN],
            img,
            ReadImage.TEXT_CELL_INCREASE,
            True,
        )
        # Remove all non-digits, such as spaces
        meal_code = "".join(filter(str.isdigit, meal_code))
        orders.append([meal_code, order_day])
    return orders


def get_filled_circles(
    cells: list[list[ndarray]], img: ndarray
) -> list[list[int, int]]:
    """Retrieve the row and column index of each circle that is colored
    Is based on how many black pixels the box contains after some transformations
    This pixel value is used to determine if the circle was filled in

    Args:
        cells (list[list[ndarray]]): The coordinates of each box
        img (ndarray): The complete image in black and white

    Returns:
        list[list[int,int]]: indices of the filled in circles
    """
    filled_circles = []

    for i, row in enumerate(cells):
        # Skip rows with days and bottom row
        if i in ReadImage.DAY_ROWS or i == ReadImage.EMPTY_ROW:
            continue
        for j, cell in enumerate(row):
            # Skip column with meal codes
            if j == ReadImage.MEAL_CODE_COLUMN:
                continue

            # Extract the pixels of interest from the whole image
            y, x, w, h = cell[0], cell[1], cell[2], cell[3]
            roi = 255 - img[x : x + h, y : y + w]

            # Find columns and rows where all pixels are white (0), this trims the region of interest to just contain the circle
            columns_to_remove = all(roi == 0, axis=0)
            rows_to_remove = all(roi == 0, axis=1)
            trimmed_roi = roi[~rows_to_remove][:, ~columns_to_remove]

            # Count black(255) pixels
            count_255 = count_nonzero(trimmed_roi == 255)
            # Count white(0) pixels but not the pixels on the outside
            count_0 = count_nonzero(trimmed_roi == 0) - get_outside_pixel_count(
                trimmed_roi
            )

            # Calculate the ratio (if zero black pixels, ratio will be 1 since the circle is not filled in if there are no black pixels)
            # Lower ratio is filled in circles since more black (255) and less white (0) pixels
            ratio = count_0 / count_255 if count_255 != 0 else 1
            if ratio < ReadImage.RATIO_OF_FILLED_CIRCLE:
                filled_circles.append([i, j])

    return filled_circles


def get_outside_pixel_count(trimmed_roi: ndarray) -> int:
    """Retrieve the amount of white pixels on both sides of the black circles
    These are not counted in the ratio

    Args:
        trimmed_roi (ndarray): The ndarray of pixels which contains the circle with white pixels on its side

    Returns:
        int: The number of pixels which will not be counted
    """
    count = 0
    # Loop over each row of pixels from top to bottom
    for i in range(0, trimmed_roi.shape[0]):
        # Go from left to right per row to find count white(0) pixels until you encounter a black pixel
        for j_left in range(0, trimmed_roi.shape[1]):
            # Check if the current pixel is white
            if trimmed_roi[i, j_left] == 0:
                count += 1
            else:
                break

        # Go from right to left per row to find count white(0) pixels until you encounter a black pixel
        for j_right in range(trimmed_roi.shape[1] - 1, -1, -1):
            # Check if the current pixel is white
            if trimmed_roi[i, j_right] == 0:
                count += 1
            else:
                break

    return count


def get_order_day(cells: list[list[ndarray]], img_bin: ndarray, j: int) -> str:
    """Get the 3 different order days for a given column
    return the most common one

    Args:
        cells (list[list[ndarray]]): Coordinates of the table cells
        img_bin (ndarray): Image which contains the order days
        j (int): Column index

    Returns:
        str: The order day used for making the orders
    """
    order_days = []
    # Loop over the rows that contain the dates
    for i in ReadImage.DAY_ROWS:
        # We want to use simple extract on the KOELVERS columns since gives way better performance
        simple_extract = True if j == ReadImage.KOELVERS_WEEKEND_COLUMN else False
        order_day_single = get_text_from_cell(
            cells[i][j], img_bin, ReadImage.TEXT_CELL_INCREASE, simple_extract
        )
        order_days.append(order_day_single)
    return get_most_common(order_days, cells, img_bin, j)


def get_text_from_cell(
    cell: list, img: ndarray, increase: int, simple_extract: bool, plot: bool = False
) -> str:
    """Get the text fot the given cell

    Args:
        cell (list): Coordinates of the cell
        img (ndarray): image containing the text
        increase (int): Extra amount of pixels you search around the given cell
        simple_extract (bool): If true you don't preprocess the area of interest

    Returns:
        str: The extracted text
    """
    # Increase the size of the box where the text will be read from
    y = cell[0] - increase
    # In some scenarios the negative increase leads y to be negative, which causes it to fail to extraxt text
    if y < 0:
        y = 0
    x = cell[1] - 2 * increase
    w = cell[2] + 2 * increase
    h = cell[3] + 4 * increase

    roi = img[x : x + h, y : y + w]
    roi_result = image_to_string(roi) if simple_extract else extract_text(roi)

    return (
        (roi_result.replace("\n", " "), roi) if plot else roi_result.replace("\n", " ")
    )


def get_most_common(
    found_days: list[str], cells: list[list[ndarray]], img_bin: ndarray, original_j: int
) -> str:
    """Return the order day which occurs at least twice (The most times)
    If the word KOELVERS is detected, get the orderday of the column left to it and also add KOELVERS to the days

    Args:
        found_days (list[str]): The found strings in the three order-day rows
        cells (list[list[ndarray]]): Coordinates of all the cells
        img_bin (ndarray): Image to extract text from,
        original_j (int): Original column index

    Raises:
        OrderScanError: Error when the order days in one column don't overlap with eachother

    Returns:
        str: The order day used for making the orders
    """

    # If "KOELVERS" or "weekend" is in the strings list, get day before and append to most common string
    # We check both KOELVERS and weekend as a double check, it tends to read KOELVERS wrong
    if any(term in s for s in found_days for term in ReadImage.KOELVERS_SIGNAL_WORDS):
        day_before = get_order_day(cells, img_bin, original_j - 1)
        return f"KOELVERS {day_before}"

    # Count how often each of the WEEKDAY_MAP keys occurs in the found days string list
    result = {}
    for key in OrderScanCsv.WEEKDAY_MAP.keys():
        count = sum(1 for found_day in found_days if key.lower() in found_day.lower())
        if count > 0:
            result[key] = count

    # Find the key names that occur the most often
    max_count = max(result.values(), default=0)
    most_frequent_members = [
        member for member, count in result.items() if count == max_count
    ]

    # Throw error when multiple weekdays occur as the most
    if len(most_frequent_members) > 1:
        raise OrderScanError(
            f"Kan niet met zekerheid de afleverdag uitlezen, dit is wat de computer leest:\n{found_days}"
        )

    return most_frequent_members[0]


def extract_text(img: ndarray) -> str:
    # Some erosion and delusion to better extract values
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    border = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255])
    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    dilation = cv2.dilate(resizing, kernel, iterations=1)
    erosion = cv2.erode(dilation, kernel, iterations=2)

    out = image_to_string(erosion)
    return out


def test_order_days(cells: list[list[ndarray]], img: ndarray):
    """Gets the text of each order day for diagnostic purposes"""
    img_columns = 3
    fig, axes = plt.subplots(6, img_columns)
    ii = 0
    for j in range(0, 6):
        days = []
        for i in ReadImage.DAY_ROWS:
            simple_text = True if j == ReadImage.KOELVERS_WEEKEND_COLUMN else False

            order_day_single, roi = get_text_from_cell(
                cells[i][j],
                img,
                ReadImage.TEXT_CELL_INCREASE,
                simple_extract=simple_text,
                plot=True,
            )

            axes[ii // img_columns, ii % img_columns].imshow(roi)
            axes[ii // img_columns, ii % img_columns].set_title(order_day_single)
            ii += 1
            days.append(order_day_single)
        print(get_most_common(days, cells, img, j))

    plt.tight_layout()
    plt.show()


def test_meal_codes(cells: list[list[ndarray]], img: ndarray):
    """Gets the text of each order day for diagnostic purposes"""

    img_rows = 6
    fig, axes = plt.subplots(img_rows, 5)

    # Row 0 and 32 are rows without meal
    ii = 0
    codes = []
    for i in range(1, 32):
        if i in ReadImage.DAY_ROWS:
            continue
        meal_code_single, roi = get_text_from_cell(
            cells[i][6],
            img,
            ReadImage.TEXT_CELL_INCREASE,
            simple_extract=True,
            plot=True,
        )

        axes[ii % img_rows, ii // img_rows].imshow(roi)
        axes[ii % img_rows, ii // img_rows].set_title(meal_code_single)
        ii += 1

    # print(codes)
    plt.tight_layout()
    plt.show()

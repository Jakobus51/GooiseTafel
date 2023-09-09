# import sys

# sys.path.append('/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages')

import cv2
from matplotlib import pyplot as plt
from numpy import ndarray
from backEnd.orderScan.constants import GetClientID, OrderScanCsv
from backEnd.orderScan.get_orders import extract_text
from re import findall, search
from backEnd.orderScan.get_orders import get_text_from_cell
from backEnd.dataClasses.customErrors import OrderScanError
from backEnd.orderScan.prepare_image import rotate
from pytesseract import image_to_string


def get_client_id(img: ndarray, plot: bool, extra_angle: int = 0) -> int:
    """Gets the clientID by first cropping the bottom right of the image

    And then extracting the clientID

    Args:
        img (ndarray): Image containing the client id
        plot (bool): If you want to plot

    Raises:
        ValueError: If client ID is not found

    Returns:
        int: Client ID
    """
    # If the client ID is not found, make the cropped area smaller by decreasing the width percentage
    for width_perc in GetClientID.WIDTH_PERCENTAGES:
        # Crop image
        height = int(img.shape[0] * GetClientID.HEIGHT_PERCENTAGE)
        width = int(img.shape[1] * width_perc)
        cut_img = img[-height:, -width:]

        # Rotate so client ID is up
        cut_rotated_img = cv2.rotate(cut_img, cv2.ROTATE_90_CLOCKWISE)
        if extra_angle != 0:
            cut_rotated_img = rotate(cut_rotated_img, extra_angle)

        text = image_to_string(cut_rotated_img)
        # Get all 8 or 9 digits from the text
        numbers = findall(r"\b\d{8,9}\b", text)
        client_id = extract_client_if_from_text(text)

        if client_id:
            if plot:
                fig, axes = plt.subplots(figsize=(5, 7))
                axes.imshow(cut_rotated_img)
                axes.set_title(
                    f"{int(numbers[0])} - (width={width_perc}, angle={extra_angle})"
                )

                plt.show()
            return int(client_id)
    if extra_angle == 0:
        return get_client_id(img, plot, -10)
    if extra_angle == -10:
        return get_client_id(img, plot, 10)

    raise OrderScanError("Kan het klantnummer niet vinden")


def extract_client_if_from_text(text: str) -> int:
    # Retrieve all 8 and 9 digits numbers
    numbers = findall(r"\b\d{8,9}\b", text)
    for number in numbers:
        str_numb = str(number)
        # All client 8 digit client IDS start with a 1
        if str_numb.startswith("1") and len(str_numb) == 8:
            return number
        # All client 9 digit client IDS start with a 1 or 6
        if (str_numb.startswith("1") or str_numb.startswith("6")) and len(
            str_numb
        ) == 9:
            return number


def get_meta_data(img: ndarray, meta_data_cell: ndarray, plot: bool):
    """Get the week number and year from the meta data cell

    Args:
        img (ndarray): image which contains the year and week nubmer
        meta_data_cell (ndarray): Coordinates of the meta-data cell which contains the year and week

    Raises:
        ValueError: When the week ann/or year number could not be found

    Returns:
        (int,int): week number and year
    """
    text = get_text_from_cell(meta_data_cell, img, 0, False, plot)
    # Extract numbers (weeknumber and year) following the word "WEEK"
    match = search(r"WEEK (\d+)-(\d+)", text)

    # Some visuals and the found values when plot is True
    if plot:
        text, roi = get_text_from_cell(meta_data_cell, img, 0, False, plot)
        fig, axes = plt.subplots(figsize=(10, 5))
        axes.imshow(roi)
        title = (
            f"week = {match.group(1)}, year= {match.group(2)}" if match else f"{text}"
        )
        axes.set_title(f"{title}")
        plt.show()
    if match:
        week = match.group(1)
        year = match.group(2)
        return (int(week), int(year))
    else:
        raise OrderScanError("Kan het weeknummer en/of jaartal niet uitlezen")


def get_delivery_date_index(order_day_to_match: str) -> int:
    """Finds the index of the date for the given the orderday

    Args:
        order_day_to_match (str): Day you want the date of

    Raises:
        ValueError: If it gets not found

    Returns:
        int: the index for the delivery date
    """
    for key in OrderScanCsv.WEEKDAY_MAP:
        if key in order_day_to_match:
            # Extract the correct datetime based on the index found via the WEEKDAY_MAP
            return OrderScanCsv.WEEKDAY_MAP[key]

    raise OrderScanError(
        f"Kan de afleverdatum niet matchen aan een datum, dit is wat de computer leest:\n{order_day_to_match}"
    )

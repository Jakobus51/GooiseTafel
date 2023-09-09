# import sys

# sys.path.append('/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages')

import cv2
from matplotlib import pyplot as plt
from numpy import count_nonzero, ndarray, array, where, pad
from backEnd.orderScan.constants import GetImages, MetaDataRow
from PIL import Image


def get_image(pil_image: Image, plot: bool):
    """Get the black and white correctly rotated image
    Also retrieves the coordinates of the meta data cell as that is the first black row in the image

    Args:
        pil_image (Image): Original image of the menu list
        plt (bool): IF you want to see some plots

    Returns:
        ndarray: Image with inverted rows
        list: coordinates of the meta data cell
    """

    # Convert from PIL image to openCV format
    open_cv_image = array(pil_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    # Rotate image in a general way, the rotation get finetuned a bit further down
    open_cv_image = cv2.rotate(open_cv_image, cv2.ROTATE_90_CLOCKWISE)
    img_binary = get_binary_of_image(open_cv_image)
    rotated_img = finetune_rotation(img_binary)

    # Inverts the black rows to white and also get the meta data row
    return invert_black_rows(rotated_img, plot)


def invert_black_rows(img: ndarray, plot: bool):
    """Finds the black rows and invert the color of those rows in the original image
    Also retrieves the coordinates of the meta data cell as that is the first black row in the image

    Args:
        img_array (np.ndarray): Image with black rows
        plt (bool): IF you want to see some plots

    Returns:
        ndarray: Image with inverted rows
        list: coordinates of the meta data cell
    """
    inv_img = 255 - img
    # Add a thick white pixeled border around the image otherwise the inverted rows extend to the borders
    inv_img_padded = pad(
        inv_img, pad_width=GetImages.PADDING, mode="constant", constant_values=0
    )

    # Shape is what he recognizes (so (x,y) with x= pixels horizontally, y= pixels vertically)
    elements_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (400, 8))
    # Retrieves all elements which are white and of pixel size 200x4, MORPH_OPEN is first erosion than dilations
    elements = cv2.morphologyEx(inv_img_padded, cv2.MORPH_OPEN, elements_kernel, 1)
    # Remove noise by making a binary of the image
    elements[elements > 128] = 255
    elements[elements <= 128] = 0

    # MORPH_CLOSE is first dilation than erosion. Fills the gaps in between the found elements
    fill_kernel_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 120))
    closed_padded_1 = cv2.morphologyEx(elements, cv2.MORPH_CLOSE, fill_kernel_1, 3)

    fill_kernel_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (900, 1))
    closed_padded_2 = cv2.morphologyEx(
        closed_padded_1, cv2.MORPH_CLOSE, fill_kernel_2, 1
    )

    # Remove some of the area to accommodate the black line around the black rows
    h_fatten_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed_padded_2 = cv2.erode(closed_padded_2, h_fatten_kernel, iterations=4)

    # Remove padding
    closed = closed_padded_2[
        GetImages.PADDING : -GetImages.PADDING, GetImages.PADDING : -GetImages.PADDING
    ]

    meta_data_cell = get_meta_data_cell(closed)

    # Where values of the closed are black (> 128) inverted the colors of the original image
    img[closed > 128] = 255 - img[closed > 128]

    # inspect the results, leave commented to potential use in future
    if plot:
        fig, axes = plt.subplots(2, 2, figsize=(8, 8))
        axes[0, 0].imshow(elements)
        axes[0, 0].set_title(f"recognized elements")

        axes[0, 1].imshow(closed_padded_1)
        axes[0, 1].set_title(f"closed after first fill kernel")

        axes[1, 0].imshow(closed_padded_2)
        axes[1, 0].set_title(f"closed after second fill kernel")

        axes[1, 1].imshow(closed)
        axes[1, 1].set_title(f"closed")

        fig_2, axes_2 = plt.subplots(1, 1, figsize=(8, 8))

        axes_2.imshow(img, cmap="gray")
        axes_2.set_title(f"closed")
        plt.show()

    return (img, meta_data_cell)


def get_meta_data_cell(img: ndarray) -> list:
    """Gets the coordinated of the cell which contains the metadata of the menu list image

    Args:
        img (ndarray): Image of the black rows you are about to inverse, the upper most black row corresponds to the meta data cell

    Returns:
        list: The meta data cell
    """
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(
        *sorted(zip(contours, boundingBoxes), key=lambda x: x[1][1])
    )

    meta_data_cell = []
    potentials = []
    # Save the contour coordinates of each box to a list
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        potentials.append([x, y, w, h])

        if (
            w > img.shape[1] * MetaDataRow.WIDTH_MIN_PERCENTAGE
            and h > MetaDataRow.HEIGHTH_MIN
            and h < MetaDataRow.HEIGHTH_MAX
        ):
            if len(meta_data_cell) == 0 or meta_data_cell[1] > y:
                meta_data_cell = [x, y, w, h]
    return meta_data_cell


def finetune_rotation(img: ndarray) -> ndarray:
    """Finds the optimal/correct rotation of the image by checking a range from -20 to +20 degrees of the original

    Args:
        img (np.ndarray): The image you want to rotation correct

    Returns:
        np.ndarray: The image with the corrected rotation
    """

    # Invert black and white
    img = 255 - img

    # Cut black parts from the sides otherwise scoring does not work
    h, w = img.shape
    cut_img = img[0:h, GetImages.SIDE_CUT_SIZE : w - GetImages.SIDE_CUT_SIZE]

    scores = []
    # Check range from -20 to +20 degrees
    angle = -GetImages.ROTATION_SEARCH
    while angle <= GetImages.ROTATION_SEARCH:
        # Rotate the cutted image by the given angle
        rotated_img = rotate(cut_img, angle)

        score = score_img(rotated_img)
        scores.append(score)

        # If score is new high score save it as the angle_correction
        if score >= max(scores):
            angle_correction = angle
        angle += GetImages.ANGLE_INCREASE

    # Return the image with the angle correction
    return 255 - rotate(img, angle_correction)


def score_img(img: ndarray) -> int:
    """Score an image based on how many black and white pixel rows it has

    Args:
        img (ndarray): The image you want to score

    Returns:
        int: The amount of black and white rows added together
    """
    row_sums = img.sum(axis=1)
    # A row is black if all values in that row are 0, thus sum to 0
    black_rows = count_nonzero(row_sums == 0)

    # A row is white if all values in that row are 255, thus w * 255
    # Since some noise we count the row if it contains more black then a certain threshold
    h, w = img.shape
    white_rows = count_nonzero(row_sums > w * 255 * GetImages.BLACK_ROW_THRESHOLD)
    return black_rows + white_rows


def rotate(img, angle):
    """
    Rotate an "image" which is an ndarray in our case with a specific angle
    """
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    return dst


def get_binary_of_image(img: ndarray) -> ndarray:
    """Returns the binary of an image"""
    img_bin = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_bin, 128, 255, cv2.THRESH_OTSU)
    return img_bin


# def add_border(img: ndarray)-> ndarray:
#     _,bw_img = cv2.threshold(img,128,255,cv2.THRESH_OTSU)
#     for row_index,row in enumerate(bw_img):
#         index = where(row == 255)[0]
#         if index.size != 0:
#             first_black_pixel_index = index[0]
#             row[first_black_pixel_index] = 0
#             row[first_black_pixel_index + 1] = 0
#             row[first_black_pixel_index + 2] = 0

#     return img

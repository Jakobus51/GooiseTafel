# import sys

# sys.path.append('/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages')

import cv2
from matplotlib import pyplot as plt
from numpy import ndarray, mean, pad
from backEnd.orderScan.constants import GetCells


def get_ordered_table_cells(img: ndarray, plot: bool) -> list[list[ndarray]]:
    """Get the coordinates of the area of interest ordered in rows and columns
    Is done by amplifying the table shape and then drawing contours around the saving the coordinates

    Args:
        img (ndarray): black and white image of the menu list
        plot (bool): True if you want to see plots

    Returns:
        list[list[ndarray]]: Coordinates of area of interests ordered in rows and columns
    """
    table = get_table_shape(img, plot)
    cells = get_table_cells(img, table, plot)
    return order_cells(cells)


def get_table_shape(img: ndarray, plot: bool) -> ndarray:
    """Get a clear image of the table

    Args:
        img (np.ndarray): Original image
        plot (bool): True if you want to see plots

    Returns:
        np.ndarray: Smplified image of the table
    """
    inv_img = 255 - img
    # Add padding to make sure lines don't touch borders
    inv_img_padded = pad(
        inv_img, pad_width=GetCells.PADDING, mode="constant", constant_values=0
    )

    # Get vertical lines
    # Shape is what he recognizes (so (x,y) with x= pixels horizontally, y= pixels vertically)
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 100))
    # Retrieves all elements which are white and of pixel size (x,y),
    v_lines = cv2.morphologyEx(
        inv_img_padded, cv2.MORPH_OPEN, v_kernel, 1
    )  # MORPH_OPEN is first erosion than dilations

    # Should connect the vertical lines
    v2_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 200))
    v2_lines = cv2.morphologyEx(
        v_lines, cv2.MORPH_CLOSE, v2_kernel, 10
    )  # MORPH_CLOSE is first dilations than

    # Make the vertical line a bit bigger
    v_fatten_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 200))
    v2_lines = cv2.dilate(v2_lines, v_fatten_kernel, iterations=1)

    # Get horizontal lines
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (140, 1))
    h_lines = cv2.morphologyEx(inv_img_padded, cv2.MORPH_OPEN, h_kernel, 1)

    # Should connect the horizontal lines
    h2_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (400, 1))
    h2_lines = cv2.morphologyEx(h_lines, cv2.MORPH_CLOSE, h2_kernel, 10)

    # Make the horizontal line a bit bigger
    h_fatten_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (300, 2))
    h2_lines = cv2.dilate(h2_lines, h_fatten_kernel, iterations=1)

    # Makes the table clearly visible aswell as black on white
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (6, 6)
    )  # The biger the shape the thicker the lines
    v_h_lines = cv2.addWeighted(v2_lines, 1, h2_lines, 1, 0.0)
    v_h_lines = cv2.erode(~v_h_lines, kernel, iterations=3)
    # Remove padding
    v_h_lines = v_h_lines[
        GetCells.PADDING : -GetCells.PADDING, GetCells.PADDING : -GetCells.PADDING
    ]

    # #Plotting stuff, commented out may use later
    if plot:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        axes[0, 0].imshow(v2_lines)
        axes[0, 0].set_title(f"Vertical")
        axes[0, 1].imshow(h_lines)
        axes[0, 1].set_title(f"horizontal")
        axes[1, 0].imshow(h2_lines)
        axes[1, 0].set_title(f"Horizontal")
        axes[1, 1].imshow(v_h_lines)
        axes[1, 1].set_title(f"Horizontal + vetical")
        plt.show()

    return v_h_lines


def get_table_cells(img: ndarray, table_bin: ndarray, plot: bool) -> ndarray:
    """Get the coordinates of all the cells in the table

    Args:
        img (ndarray): Original black and white picture
        table_bin (ndarray): Amplified image of the table
        plot (bool): True if you want to see plots

    Returns:
        ndarray: All the coordinates of the table cells
    """
    # Get the contours of the table cells
    contours, hierarchy = cv2.findContours(
        table_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(
        *sorted(zip(contours, boundingBoxes), key=lambda x: x[1][1])
    )
    cells = []
    image = img.copy()
    # Save the contour coordinates of each box to a list
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (
            w > GetCells.WIDTH_MIN
            and w < GetCells.WIDTH_MAX
            and h > GetCells.HEIGHTH_MIN
            and h < GetCells.HEIGHTH_MAX
        ):
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cells.append([x, y, w, h])

    if plot:
        # Plot found contours of the table
        plt.imshow(image, cmap="gray")
        plt.title("table cells")
        plt.show()
    return cells


def order_cells(cells: ndarray) -> list[list[ndarray]]:
    """Order all found cells into rows and for each of those rows 6 entries corresponding to the columns

    Args:
        cells (ndarray): Un-ordered cells

    Returns:
        list[list[ndarray]]: Ordered cells into rows containing 6 entries for each column
    """
    rows = []
    columns = []

    # Find the average height of the cells (third value of the cell is its height)
    heights = [cells[i][3] for i in range(len(cells))]
    mean_height = mean(heights)

    columns.append(cells[0])
    previous = cells[0]
    for i in range(1, len(cells)):
        # Check if the x coordinate of box i is smaller than the midpoint of the previous box (x-coordinate is in the top left of the box)
        if cells[i][1] <= previous[1] + mean_height / 2:
            # append box to the columns and reset previous
            columns.append(cells[i])
            previous = cells[i]
            # If last box, add columns to rows no matter what
            if i == len(cells) - 1:
                rows.append(columns)
        # If the box is too low, it means it is in a new row, so add all current columns to a new row and start a new columns arrays
        else:
            rows.append(columns)
            columns = []
            previous = cells[i]
            columns.append(cells[i])

    # Sort rows by their x-coordinate so they are in the correct order
    for row in rows:
        row.sort(key=lambda arr: arr[0])

    return rows

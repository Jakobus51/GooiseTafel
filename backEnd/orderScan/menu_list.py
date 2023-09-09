# import sys

# sys.path.append("/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages")
import cv2
from numpy import array, count_nonzero, ndarray, where
from PIL import Image
from backEnd.orderScan.prepare_image import get_image
from backEnd.orderScan.get_orders import get_orders
from backEnd.orderScan.get_other_info import (
    get_client_id,
    get_meta_data,
    get_delivery_date_index,
)
from pandas import DataFrame
from datetime import datetime
from backEnd.orderScan.constants import OrderScanCsv
from backEnd.dataClasses.customErrors import OrderScanError
from backEnd.gtHelpers import get_days_in_week


class MenuList:
    grey_image: ndarray  # The rotated and grey scaled image with inverse rows
    black_white_image: ndarray  # The rotated and black and whited image with inverse rows
    retrieved_infos: list
    customer_id: int
    week_number: int
    year_number: int
    orders_df: DataFrame

    def __init__(
        self,
        pil_image: Image,
        plot_get: bool,
        plot_orders: bool,
        plot_client_id: bool,
        plot_meta_data: bool,
    ):
        # Get the rotated black and white image, aswell as the coordinates of the metadata
        self.grey_image, meta_data_cell = get_image(pil_image, plot_get)
        _, self.black_white_image = cv2.threshold(
            self.grey_image, 128, 255, cv2.THRESH_OTSU
        )

        self.retrieved_infos = get_orders(self.black_white_image, plot_orders)
        self.customer_id = get_client_id(self.black_white_image, plot_client_id)
        self.week_number, self.year_number = get_meta_data(
            self.black_white_image, meta_data_cell, plot_meta_data
        )

        self.make_orders_df()
        if len(self.orders_df) == 0:
            raise OrderScanError(f"Kan geen orders vinden")

    def make_orders_df(self):
        self.orders_df = DataFrame(columns=OrderScanCsv.CSV_COLUMNS)
        week_dates = get_days_in_week(self.week_number, self.year_number)

        for retrieved_info in self.retrieved_infos:
            meal_code = retrieved_info[0]
            order_day = retrieved_info[1]

            order_date = datetime.now().strftime("%d/%m/%Y")
            order_id = f"OS{self.week_number}{self.year_number}-{self.customer_id}"
            if "KOELVERS" in order_day:
                deliver_date = week_dates[
                    get_delivery_date_index(order_day) + 1
                ].strftime("%d/%m/%Y")
                meal_code_postfix = f"{meal_code}k"
            else:
                deliver_date = week_dates[get_delivery_date_index(order_day)].strftime(
                    "%d/%m/%Y"
                )
                meal_code_postfix = f"{meal_code}w"

            quantity = 1
            new_order = [
                self.customer_id,
                order_date,
                order_id,
                deliver_date,
                meal_code_postfix,
                quantity,
            ]
            self.orders_df.loc[len(self.orders_df)] = new_order

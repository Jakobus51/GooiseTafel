class UALabelI:
    day: str
    city: str
    floor: str
    meal: str
    quantity: str

    def __init__(
        self,
        day,
        city,
        floor,
        meal,
        quantity,
    ):
        self.day = day
        self.city = city
        self.floor = floor
        self.meal = meal
        self.quantity = quantity

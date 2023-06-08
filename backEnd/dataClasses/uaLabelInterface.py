class UALabelI:
    day: str
    city: str
    location: str
    product: str
    quantity: str

    def __init__(
        self,
        day,
        city,
        location,
        product,
        quantity,
    ):
        self.day = day
        self.city = city
        self.location = location
        self.product = product
        self.quantity = quantity

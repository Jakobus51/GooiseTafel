class UALabelI:
    day: str
    city: str
    floor: str
    meal: str
    quantity: str
    order: int  # Is used to sort the labels

    def __init__(self, day, city, floor, meal, quantity, order):
        self.day = day
        self.city = city
        self.floor = floor
        self.meal = meal
        self.quantity = quantity
        self.order = order

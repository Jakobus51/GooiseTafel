class GTlabel:
    customerName: str
    customerId: int
    address: str
    zipCode: str
    city: str
    phoneNumber: str
    deliveryDate: str
    productName: str
    customerRemarks1: str

    def __init__(
        self,
        customerName,
        customerId,
        address,
        zipCode,
        city,
        phoneNumber,
        deliveryDate,
        productName,
        customerRemarks1,
    ):
        self.customerName = customerName
        self.customerId = customerId
        self.address = address
        self.zipCode = zipCode
        self.city = city
        self.phoneNumber = phoneNumber
        self.deliveryDate = deliveryDate
        self.productName = productName
        self.customerRemarks1 = customerRemarks1

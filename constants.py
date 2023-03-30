class orders:
    ankerWord = "Verkooporders"
    columnNamesArticles = [
        "productId",
        "productName",
        "customerId",
        "customerName",
        "quantity",
        "deliveryDate",
        "deliveryMethod",
    ]
    columnNamesCustomers = [
        "customerId",
        "customerName",
        "address",
        "zipCode",
        "city",
        "phoneNumber",
        "deliveryMethod",
        "customerRemarks1",
        "quantity",
        "productName",
        "deliveryDate",
    ]


class customers:
    ankerWord = "Relaties"
    columnNames = [
        "customerId",
        "customerName",
        "address",
        "zipCode",
        "city",
        "phoneNumber",
        "email",
        "deliveryMethod",
        "customerRemarks2",
        "customerRemarks1",
        "priceList",
        "customerBool",
        "supplierBool",
    ]

from pathlib import Path


class orders:
    """Constant used for creating dataFrames of order export of Exact."""

    # the word from which on the data starts
    ankerWord = "Verkooporders"
    # how we want to call the columns if the exact order export is done per article
    columnNamesArticles = [
        "productId",
        "productName",
        "customerId",
        "customerName",
        "quantity",
        "deliveryDate",
        "deliveryMethod",
    ]
    # how we want to call the columns if the exact order export is done per customer
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
    """Constant used for creating dataFrames of customer export of Exact."""

    # the word from which on the data starts
    ankerWord = "Relaties"
    # how we want to call the columns for a customer export in exact
    # remarks 1 is about how a customer orders
    # remarks 2 is used to put down if the customer is on holiday or sick or something
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


class liexCsvExport:
    """Columns names used to create the csv of Liex"""

    dataColumnNames = [
        "customerId",
        "Added",
        "Order",
        "Product_variant",
        "Product_article_code",
        "Quantity",
        "Product_price",
    ]

    csvColumnNames = [
        "customerId",
        "orderDate",
        "orderId",
        "deliveryDate",
        "productId",
        "quantity",
        "productPrice",
    ]


class saveLocations:
    """All the default directories used when accessing data in the app"""

    default = Path.home() / "Dropbox" / "Gooise Tafel BV" / "GT Software"
    input = default / "Input"
    KALInput = input / "KAL"
    LiexInput = input / "WebShop Orders (Liex)"
    InkordInput = input / "Inkord"
    GotaLabelInput = input / "Dag Orders (GotaLabel, PakLijst)"
    PakLijstInput = input / "Dag Orders (GotaLabel, PakLijst)"

    CustomersInput = input / "KlantenBestand"

    output = default / "Output"
    KALOutput = output / "KAL"
    LiexOutput = output / "Liex"
    InkordOutput = output / "Inkord"
    GotaLabelOutput = output / "GotaLabel"
    PakLijstOutput = output / "PakLijst"

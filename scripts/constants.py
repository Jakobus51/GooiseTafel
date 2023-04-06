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


class media:
    """Path to the logo"""

    logoPath = Path(
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\media\logo.png"
    )


class KalPDF:
    """Constant used for generating the pdf of the KAL application"""

    def Title(deliveryDateRange: str) -> str:
        """Title used in the pdf as well as the pdf name"""
        return f"KAL ({deliveryDateRange})"

    def MetaData(deliveryDateRange: str, dateOfExactOutput: str) -> str:
        """Extra information that is shown on top of the page"""
        return f"Klanten Actie Lijst <br/><br/>Uitdraai van alle actieve klanten die nog niet hebben besteld tussen <strong>{deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/><br/>"

    # Should sum to one. And the length needs to be equal to the number of columns you want to show in your pdf
    columnSpacing = [0.09, 0.10, 0.11, 0.10, 0.20, 0.25, 0.15]
    # Original names of the columns you want to show
    dataDisplayColumns = [
        "customerId",
        "customerName",
        "city",
        "phoneNumber",
        "email",
        "deliveryMethod",
        "customerRemarks2",
    ]
    # How you want the columns to be shown in the pdf
    pdfDisplayColumns = [
        "Klant Nr.",
        "Naam",
        "Plaats",
        "Telefoon",
        "E-mail",
        "Leveringswijze",
        "Opmerking",
    ]


class InkordPDF:
    """Constant used for generating the pdf of the Inkord application"""

    def Title(deliveryDateRange: str) -> str:
        """Title used in the pdf as well as the pdf name"""
        return f"InkOrd ({deliveryDateRange})"

    def MetaData(deliveryDateRange: str, dateOfExactOutput: str) -> str:
        """Extra information that is shown on top of the page"""

        return f"Inkooplijst <br/><br/>Uitdraai van alle gerechten die afgeleverd moeten worden<br/> tussen <strong>{deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/><br/>"

    # Should sum to one. And the length needs to be equal to the number of columns you want to show in your pdf
    columnSpacing = [0.72, 0.12, 0.16]
    # Original names of the columns you want to show
    dataDisplayColumns = ["productName", "productId", "quantity"]
    # How you want the columns to be shown in the pdf
    pdfDisplayColumns = ["Product naam", "ID", "Hoeveelheid"]

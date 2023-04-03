class orders:
    """Constant used for creating dataframes of order export of Exact."""

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
    # how we want to call the columnns if the exact order export is done per customer
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
    """Constant used for creating dataframes of customer export of Exact."""

    # the word from which on the data starts
    ankerWord = "Relaties"
    # how we want to call the columnns for a customer export in exact
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


class media:
    """Path to the logo"""

    logoPath = (
        r"C:\Users\Jakob\Documents\Malt\Gooise_Tafel\repo\GooiseTafel\media\logo.png"
    )


class KalPDF:
    """Constant used for generating the pdf of the KAL application"""

    def Title(afleverDateRange: str) -> str:
        """Title used in the pdf as well as the pdf name"""
        return f"KAL ({afleverDateRange})"

    def MetaData(afleverDateRange: str, dateOfExactOutput: str) -> str:
        """Extra information that is shown on top of the page"""
        return f"Klanten Actie Lijst <br/><br/>Uitdraai van alle actieve klanten die nog niet hebben besteld<br/> tussen <strong>{afleverDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/><br/>"

    # Should sum to one. And the length needs to be equal to the number of columns you want to show in your pdf
    columnSpacing = [0.07, 0.33, 0.30, 0.30]
    # Original names of the columns you want to show
    dataDisplayColumns = ["customerName", "phoneNumber", "email"]
    # How you want the columns to be shown in the pdf
    pdfDisplayColumns = ["Klant", "Telefoon nummer", "Email"]


class InkordPDF:
    """Constant used for generating the pdf of the Inkord application"""

    def Title(afleverDateRange: str) -> str:
        """Title used in the pdf as well as the pdf name"""
        return f"InkOrd ({afleverDateRange})"

    def MetaData(afleverDateRange: str, dateOfExactOutput: str) -> str:
        """Extra information that is shown on top of the page"""

        return f"Inkooplijst <br/><br/>Uitdraai van alle gerechten die besteld zijn<br/> tussen <strong>{afleverDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{dateOfExactOutput}</strong><br/><br/>"

    # Should sum to one. And the length needs to be equal to the number of columns you want to show in your pdf
    columnSpacing = [0.12, 0.72, 0.16]
    # Original names of the columns you want to show
    dataDisplayColumns = ["productId", "productName", "quantity"]
    # How you want the columns to be shown in the pdf
    pdfDisplayColumns = ["ID", "Product naam", "Hoeveelheid"]

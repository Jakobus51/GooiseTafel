from enum import Enum


class PdfEnum(Enum):
    KAL = "KAL"
    Inkord = "Inkord"
    PakLijstRoute = "PakLijstRoute"
    PakLijstCategory = "PakLijstCategory"


class PdfHelper:
    """Class containing all information needed for the creation of a pdf

    Returns:
        _type_: _description_
    """

    type: PdfEnum
    deliveryDateRange: str
    dateOfExactOutput: str
    columnSpacing: list[float]
    dataDisplayColumn: list[str]
    pdfDisplayColumns: list[str]
    title: str
    metaData: str
    tableData: dict
    deliveries: dict

    def __init__(
        self,
        type: PdfEnum,
        deliveryDateRange: str,
        dateOfExactOutput: str,
    ):
        self.type = type
        self.deliveryDateRange = deliveryDateRange
        self.dateOfExactOutput = dateOfExactOutput
        self.columnSpacing = self.setColumnSpacing()
        self.dataDisplayColumn = self.setDataDisplayColumn()
        self.pdfDisplayColumns = self.setPdfDisplayColumns()
        self.title = self.setTitle()
        self.metaData = self.setMetaData()

    def setColumnSpacing(self):
        """Gets the column spacing for the given pdf.
        Should sum to one and the length should be equal to the number of column you want to show
        """
        if self.type == PdfEnum.Inkord:
            return [0.72, 0.12, 0.16]
        if self.type == PdfEnum.KAL:
            return [0.09, 0.10, 0.11, 0.10, 0.20, 0.25, 0.15]
        if self.type == PdfEnum.PakLijstCategory or self.type == PdfEnum.PakLijstRoute:
            return [0.85, 0.15]

    def setDataDisplayColumn(self):
        """Get the columns from the pdf you want to show on the pdf"""

        if self.type == PdfEnum.Inkord:
            return ["productName", "productId", "quantity"]
        if self.type == PdfEnum.KAL:
            return [
                "customerId",
                "customerName",
                "city",
                "phoneNumber",
                "email",
                "deliveryMethod",
                "customerRemarks2",
            ]
        if self.type == PdfEnum.PakLijstCategory or self.type == PdfEnum.PakLijstRoute:
            return ["productName", "quantity"]

    def setPdfDisplayColumns(self):
        """Get the column names you want to display on the actual pdf"""

        if self.type == PdfEnum.Inkord:
            return ["Product naam", "ID", "Hoeveelheid"]
        if self.type == PdfEnum.KAL:
            return [
                "Klant Nr.",
                "Naam",
                "Plaats",
                "Telefoon",
                "E-mail",
                "Route",
                "Opmerking",
            ]
        if self.type == PdfEnum.PakLijstCategory or self.type == PdfEnum.PakLijstRoute:
            return ["Product naam", "Hoeveelheid"]

    def setTitle(self):
        """Title used in the pdf as well as the pdf name"""

        if self.type == PdfEnum.Inkord:
            return f"InkOrd ({self.deliveryDateRange})"
        if self.type == PdfEnum.KAL:
            return f"KAL ({self.deliveryDateRange})"
        if self.type == PdfEnum.PakLijstCategory:
            return f"PakLijst TOTAAL ({self.deliveryDateRange})"
        if self.type == PdfEnum.PakLijstRoute:
            return f"PakLijst PER ROUTE ({self.deliveryDateRange})"

    def setMetaData(self):
        """Extra information that is shown on top of the page"""

        baseTextOrders = f"Uitdraai van alle gerechten die afgeleverd moeten worden<br/> tussen <strong>{self.deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{self.dateOfExactOutput}</strong><br/><br/>"
        baseTextCustomers = f"Uitdraai van alle actieve klanten die nog niet hebben besteld tussen <strong>{self.deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{self.dateOfExactOutput}</strong><br/>"

        if self.type == PdfEnum.Inkord:
            return baseTextOrders
        if self.type == PdfEnum.KAL:
            return baseTextCustomers
        if self.type == PdfEnum.PakLijstCategory:
            return baseTextOrders
        if self.type == PdfEnum.PakLijstRoute:
            return baseTextOrders

    def setTableData(self, tableData):
        self.tableData = tableData

    def setDeliveries(self, deliveries):
        self.deliveries = deliveries

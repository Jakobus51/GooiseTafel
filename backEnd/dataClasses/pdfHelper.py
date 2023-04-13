from backEnd.dataClasses.appEnum import AppEnum


class PdfHelper:
    """Class containing all information needed for the creation of a pdf"""

    type: AppEnum  # What kind of app
    deliveryDateRange: str  # Range inbetween all the deliveries will be made
    dateOfExactOutput: str  # Date when the exact export was made
    columnSpacing: list[float]  # Spacing per column in the pdf
    dataDisplayColumn: list[str]  # Columns that will be shown in the pdf
    pdfDisplayColumns: list[
        str
    ]  # Column names (headers in the table) that will be displayed in the pdf
    title: str  # Title of the pdf, also the file name of the pdf
    metaData: str  # Some additional data that is shown on top of the pdf
    tableData: dict  # The actual data that will be in the tables, each table is it on entry in the dictionary
    deliveries: dict  # Addtional information on how many deliveries there are per table, keys equal to the tableData keys

    def __init__(
        self,
        type: AppEnum,
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
        if self.type == AppEnum.Inkord:
            return [0.72, 0.12, 0.16]
        if self.type == AppEnum.KAL:
            return [0.09, 0.10, 0.11, 0.10, 0.20, 0.25, 0.15]
        if self.type == AppEnum.PakLijstCategory or self.type == AppEnum.PakLijstRoute:
            return [0.85, 0.15]

    def setDataDisplayColumn(self):
        """Get the columns from the pdf you want to show on the pdf"""

        if self.type == AppEnum.Inkord:
            return ["productName", "productId", "quantity"]
        if self.type == AppEnum.KAL:
            return [
                "customerId",
                "customerName",
                "city",
                "phoneNumber",
                "email",
                "deliveryMethod",
                "customerRemarks2",
            ]
        if self.type == AppEnum.PakLijstCategory or self.type == AppEnum.PakLijstRoute:
            return ["productName", "quantity"]

    def setPdfDisplayColumns(self):
        """Get the column names you want to display on the actual pdf"""

        if self.type == AppEnum.Inkord:
            return ["Product naam", "ID", "Hoeveelheid"]
        if self.type == AppEnum.KAL:
            return [
                "Klant Nr.",
                "Naam",
                "Plaats",
                "Telefoon",
                "E-mail",
                "Route",
                "Opmerking",
            ]
        if self.type == AppEnum.PakLijstCategory or self.type == AppEnum.PakLijstRoute:
            return ["Product naam", "Hoeveelheid"]

    def setTitle(self):
        """Title used in the pdf as well as the pdf name"""

        if self.type == AppEnum.Inkord:
            return f"InkOrd ({self.deliveryDateRange})"
        if self.type == AppEnum.KAL:
            return f"KAL ({self.deliveryDateRange})"
        if self.type == AppEnum.PakLijstCategory:
            return f"PakLijst TOTAAL ({self.deliveryDateRange})"
        if self.type == AppEnum.PakLijstRoute:
            return f"PakLijst PER ROUTE ({self.deliveryDateRange})"

    def setMetaData(self):
        """Extra information that is shown on top of the page"""

        baseTextOrders = f"Uitdraai van alle gerechten die afgeleverd moeten worden<br/> tussen <strong>{self.deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{self.dateOfExactOutput}</strong><br/><br/>"
        baseTextCustomers = f"Uitdraai van alle actieve klanten die nog niet hebben besteld tussen <strong>{self.deliveryDateRange}</strong><br/><br/>De uitdraai uit Exact was gemaakt op <strong>{self.dateOfExactOutput}</strong><br/>"

        if self.type == AppEnum.Inkord:
            return baseTextOrders
        if self.type == AppEnum.KAL:
            return baseTextCustomers
        if self.type == AppEnum.PakLijstCategory:
            return baseTextOrders
        if self.type == AppEnum.PakLijstRoute:
            return baseTextOrders

    def setTableData(self, tableData):
        self.tableData = tableData

    def setDeliveries(self, deliveries):
        self.deliveries = deliveries

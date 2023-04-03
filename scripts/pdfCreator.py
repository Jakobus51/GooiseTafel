from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Image,
    Paragraph,
    LongTable,
    Frame,
    PageTemplate,
)
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet
from scripts.constants import media, KalPDF
from pandas import DataFrame


def drawLogo(canvas, document):
    """
    Add the logo
    """
    # get the logo
    logo = Image(media.logoPath, width=1.8 * inch, height=1.2 * inch)
    pageWidth, pageHeight = A4

    # Calculate the upper right corner position
    logoX = pageWidth - logo._width - 0.5 * inch
    logoY = pageHeight - logo._height - 0.5 * inch

    # Draw the logo on the canvas
    canvas.drawImage(media.logoPath, logoX, logoY, logo._width, logo._height)


def addPageNumber(canvas, doc):
    """
    Add the page number
    """
    page_num = canvas.getPageNumber()
    text = "Pagina %s" % page_num
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(200 * mm, 5 * mm, text)


def drawFirstPage(canvas, document):
    """
    Is called for the first page where you want the logo and the page number
    """
    drawLogo(canvas, document)
    addPageNumber(canvas, document)


def drawOtherPages(canvas, document):
    """
    Is called for the other pages, where you only want the page number
    """
    addPageNumber(canvas, document)


def wrap_cell_content(data_frame):
    """
    Code from GPT4 which makes the cells use textwrap if the text is too long
    """
    styles = getSampleStyleSheet()
    wrapped_data = []
    for row in data_frame.values:
        wrapped_row = [Paragraph(str(cell), styles["Normal"]) for cell in row]
        wrapped_data.append(wrapped_row)
    return wrapped_data


def createTable(
    data: DataFrame, columnSpacing: list[float], doc: SimpleDocTemplate
) -> LongTable:
    """
    Creates the table by first applying text-wrap and then configuring the column width
    and lastly the general table formatting
    """
    # Convert the pandas DataFrame to a ReportLab Table
    wrappedData = wrap_cell_content(data)
    dataForTable = [data.columns.to_list()] + wrappedData
    table = LongTable(dataForTable)

    # make the table page width wide
    pageWidth, pageHeight = A4
    leftMargin = 0.5 * inch
    rightMargin = 0.5 * inch
    availableWidth = pageWidth - leftMargin - rightMargin

    # Set the column widths, the columnSpacing needs to be the same as the number of columns in the data
    tableSpacing = []
    for columnSpace in columnSpacing:
        tableSpacing.append(availableWidth * columnSpace)
    table._argW = tableSpacing

    # Set style of the table
    table.setStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("GRID", (0, 1), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE",
            ),
        ]
    )

    return table


def createPDF(
    titleText: str, metaDataText: str, data: DataFrame, columnSpacing: list[float]
) -> None:
    """Creates a pdf pased on the given input. Is either for the KAL ot Inkord application

    Args:
        titleText (str): Title used in the pdf and set as pdf file name
        metaDataText (str): Extra information about the data used in the pdf
        data (DataFrame): The data you want to display in the pdf, is already formatted in the correct form
        columnSpacing (list[float]): The % of width of each column
    """
    # Create a PDF file with a frame
    doc = SimpleDocTemplate(
        f"{titleText}.pdf", pagesize=A4, bottomMargin=0.25 * inch, topMargin=0.25 * inch
    )
    # size of a4 paper is 8.27 by 11.69 inch, subtract one from both
    frameFirstPage = Frame(
        0.5 * inch, 0.25 * inch, 7.27 * inch, 11.19 * inch, id="main_frame"
    )
    # make template with a logo in the right upper corner
    firstPageTemplate = PageTemplate(
        id="with_logo", frames=[frameFirstPage], onPage=drawFirstPage
    )
    doc.addPageTemplates([firstPageTemplate])

    # Get the default styles
    styles = getSampleStyleSheet()

    # Create the objects that will be shown on the pdf. In reportLab this is called a story
    header = Paragraph(titleText, styles["Heading1"])
    metaInformation = Paragraph(metaDataText, styles["Normal"])
    table = createTable(data, columnSpacing, doc)
    story = [
        header,
        metaInformation,
        table,
    ]

    # Builds the pdf and automatically saves it to the current directory
    doc.build(
        story,
        onLaterPages=drawOtherPages,
    )

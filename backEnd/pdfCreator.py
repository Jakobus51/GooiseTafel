from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Image,
    Paragraph,
    LongTable,
    Frame,
    PageTemplate,
    PageBreak,
    BaseDocTemplate,
    NextPageTemplate,
)
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from media.media import paths
from pandas import DataFrame
from functools import partial
from pathlib import Path
from os import path
from subprocess import Popen
from backEnd.constants import pdfEnum
from backEnd.gtHelpers import (
    getPdfColumnSpacing,
    getPdfTitle,
    getPdfMetaData,
    getPdfDisplayColumns,
    getDataDisplayColumn,
)


def createPDF(
    data: dict,
    pdfKind: pdfEnum,
    deliveryDateRange: str,
    dateOfExactOutput: str,
    outputFolder: Path,
    showPDF: bool,
) -> None:
    """Creates a pdf based on the given input. Is either for the KAL ot Inkord application

    Args:
        data (DataFrame): The data you want to display in the pdf, is already formatted in the correct form
        pdfKind (pdf.Enum): For which application the pdf needs to be created
        deliveryDateRange (str): Range of when data was collected
        dateOfExactOutput (str): day when the export from Exact was made
        outputFolder (Path): Where the pdf needs to be saved
        showPDF (bool): Whether or not you want to show the pdf after creation
    """
    # Create a PDF file with a frame

    titleText = getPdfTitle(pdfKind, deliveryDateRange)
    metaDataText = getPdfMetaData(pdfKind, deliveryDateRange, dateOfExactOutput)
    columnSpacing = getPdfColumnSpacing(pdfKind)
    landscapeBool = pdfKind == pdfEnum.KAL

    pageWidth, pageHeight = landscape(A4) if landscapeBool else A4

    # have to use old path method since reportLab does not support pathlib
    outputFile = path.join(outputFolder, f"{titleText}.pdf")
    doc = BaseDocTemplate(
        outputFile,
        pagesize=(pageWidth, pageHeight),
        bottomMargin=5 * mm,
        topMargin=5 * mm,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")

    # make template with a logo in the right upper corner
    firstPageTemplate = PageTemplate(
        id="with_logo",
        frames=[frame],
        onPage=partial(drawFirstPage, landscapeBool=landscapeBool),
    )
    otherPageTemplate = PageTemplate(
        id="without_logo",
        frames=[frame],
        onPage=partial(drawOtherPages, landscapeBool=landscapeBool),
    )
    doc.addPageTemplates([firstPageTemplate, otherPageTemplate])

    story = createStory(titleText, metaDataText, pdfKind, data, columnSpacing, doc)

    # Builds the pdf and automatically saves it to the given location (=outputFile)
    doc.build(story)

    # Open pdf if that option was selected
    if showPDF:
        Popen([outputFile], shell=True)


def drawLogo(canvas, document, landscapeBool):
    """
    Add the logo
    """
    # get the logo
    logo = Image(paths.logo, width=45 * mm, height=30 * mm)
    pageWidth, pageHeight = landscape(A4) if landscapeBool else A4

    # Calculate the upper right corner position
    logoX = pageWidth - logo._width - 10 * mm
    logoY = pageHeight - logo._height - 5 * mm

    # Draw the logo on the canvas
    canvas.drawImage(paths.logo, logoX, logoY, logo._width, logo._height)


def addPageNumber(canvas, doc, landscapeBool):
    """
    Add the page number
    """
    pageWidth, pageHeight = landscape(A4) if landscapeBool else A4

    page_num = canvas.getPageNumber()
    text = f"Pagina {page_num}"
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(pageWidth - 10 * mm, 5 * mm, text)


def drawFirstPage(canvas, document, landscapeBool):
    """
    Is called for the first page where you want the logo and the page number
    """
    canvas.setPageSize(landscape(A4) if landscapeBool else A4)

    drawLogo(canvas, document, landscapeBool)
    addPageNumber(canvas, document, landscapeBool)


def drawOtherPages(canvas, document, landscapeBool):
    """
    Is called for the other pages, where you only want the page number
    """
    canvas.setPageSize(landscape(A4) if landscapeBool else A4)
    addPageNumber(canvas, document, landscapeBool)


def createStory(
    titleText: str,
    metaDataText: str,
    pdfKind: pdfEnum,
    data: dict,
    columnSpacing: list[float],
    doc: SimpleDocTemplate,
) -> list[any]:
    """Pieces everything together into one pdf which is called a story

    Args:
        titleText (str): Title of the pdf
        metaDataText (str): Some meta data about the pdf
        pdfKind (pdfEnum): which kind of pdf is getting created
        data (dict): Data that will be passed into the tables
        columnSpacing (list[float]): The % of width of each column
        doc (SimpleDocTemplate): object used for pdf creation

    Returns:
        list[any]: List of all the elements that will be made into a pdf
    """
    # Get the default styles
    styles = getSampleStyleSheet()

    # Create the objects that will be shown on the pdf. In reportLab this is called a story
    header = Paragraph(titleText, styles["Heading1"])
    metaInformation = Paragraph(metaDataText, styles["Normal"])

    story = [
        header,
        metaInformation,
        NextPageTemplate("without_logo"),
    ]
    if pdfKind == pdfEnum.KAL:
        # KAL has three different table each corresponding to a different subGroup
        tableGT = createTable(data["GT"], columnSpacing, True, colors.lightblue)
        tableNormal = createTable(data["normal"], columnSpacing, True, colors.white)
        tableOnline = createTable(
            data["online"], columnSpacing, True, colors.lightgreen
        )

        textHeaderGt = "Klanten die niet zelf bestellen (GT)"
        headerGT = Paragraph(textHeaderGt, styles["Heading2"])

        textHeaderOnline = "Klanten die online bestellen (online)"
        headerOnline = Paragraph(textHeaderOnline, styles["Heading2"])

        textSubHeader = "Klanten die niet GT zijn of online bestellen"
        headerNormal = Paragraph(textSubHeader, styles["Heading2"])

        story.extend(
            [
                headerGT,
                tableGT,
                PageBreak(),
                headerOnline,
                tableOnline,
                PageBreak(),
                headerNormal,
                tableNormal,
            ]
        )
        return story
    if pdfKind == pdfEnum.Inkord:
        # Inkord only has one table to make
        table = createTable(data["normal"], columnSpacing, False, colors.white)
        story.append([table])
        return story

    if pdfKind == pdfEnum.PakLijstCategory or pdfEnum.PakLijstRoute:
        meals = 0
        subStory = []
        for key in data:
            df = data[key]

            # Collect some extra data to show
            meals += df["Hoeveelheid"].sum()

            # Change the Productname column to the key for better user experience
            headerText = f"{key}\n(Totaal aantal maaltijden: {df['Hoeveelheid'].sum()})"
            df = df.rename(columns={"Product naam": headerText})

            table = createTable(df, columnSpacing, False, colors.white)
            subStory.append(table)

        # Save some additional information on top of the page
        extraInfoText = f"Deze lijst bevat {meals} maaltijden<br/><br/>"
        extraInfo = Paragraph(extraInfoText, styles["Normal"])
        subStory.insert(0, extraInfo)
        story.extend(subStory)
        return story


def createTable(
    data: DataFrame,
    columnSpacing: list[float],
    landscapeBool: bool,
    color: any,
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
    pageWidth, pageHeight = landscape(A4) if landscapeBool else A4
    leftMargin = 10 * mm
    rightMargin = 10 * mm
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
            ("BACKGROUND", (0, 1), (0, -1), color),
        ]
    )
    return table


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

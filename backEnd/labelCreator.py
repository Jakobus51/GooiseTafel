from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pathlib import Path
from os import path, startfile
from subprocess import Popen
from media.media import paths
from textwrap import wrap
from win32api import ShellExecute
import win32print


def createLabels(
    labelInput: LabelHelper,
    outputFolder: Path,
) -> None:
    if labelInput.type == AppEnum.GotaLabel:
        fileName = f"GotaLabel ({labelInput.dateOfOrders}).pdf"
    else:
        fileName = f"SingleLabel ({labelInput.dateOfOrders}).pdf"

    outputFile = path.join(outputFolder, fileName)

    # Label size
    labelWidth = 101 * mm
    labelHeight = 54 * mm

    # Set margins
    topMargin = 2 * mm
    bottomMargin = 2 * mm
    leftMargin = 2 * mm
    rightMargin = 2 * mm

    # Logo size
    logoWidth = 27 * mm
    logoHeight = 18 * mm

    # Text distance configurations
    textHeight = 3.4 * mm
    interTextDistance = 2 * mm
    newTextLine = textHeight + interTextDistance

    # After how many characters the text wraps, was determined y changing values and checking what kind of impact it had on the labels
    maxStringLengthLogo = 35
    maxStringLength = 38

    c = canvas.Canvas(outputFile, pagesize=(labelWidth, labelHeight), bottomup=1)

    def wrappedText(
        c: canvas, text, originalYCoord, xCoord, maxSLength, textHeight
    ) -> float:
        """Draws wo string underneath eachother if the text length exceed the maxLength
        Returns the y coordinate of the lowest drawn string
        """
        if len(text) > maxSLength:
            wrappedText = wrap(text, width=maxSLength)
            c.drawString(xCoord, originalYCoord, wrappedText[0])
            c.drawString(
                xCoord,
                originalYCoord - textHeight,
                wrappedText[1],
            )
            return originalYCoord - textHeight
        else:
            c.drawString(
                xCoord,
                originalYCoord,
                text,
            )
            return originalYCoord

    # Loop over all labels, all labels get drawn on a new page
    for label in labelInput.labels:
        c.setFont("Helvetica", 10)

        # Logo and line for better readability
        c.drawImage(
            paths.logoBorderless,
            leftMargin,
            labelHeight - logoHeight - topMargin,
            logoWidth,
            logoHeight,
        )

        c.setLineWidth(0.8)
        # Rectangle around logo
        c.rect(
            leftMargin,
            labelHeight - logoHeight - topMargin,
            logoWidth,
            logoHeight,
        )

        # # rectangle around customerID and date
        # c.rect(
        #     leftMargin,
        #     labelHeight - logoHeight - topMargin - 2 * newTextLine,
        #     logoWidth,
        #     2 * newTextLine,
        # )

        # customer Name
        newCustomerNameYLocation = wrappedText(
            c,
            label.customerName,
            labelHeight - topMargin - textHeight,
            logoWidth + 2 * leftMargin,
            maxStringLengthLogo,
            textHeight,
        )

        # Address
        newAddressYLocation = wrappedText(
            c,
            label.address,
            newCustomerNameYLocation - newTextLine,
            logoWidth + 2 * leftMargin,
            maxStringLengthLogo,
            textHeight,
        )

        # Zipcode + city
        c.drawString(
            logoWidth + 2 * leftMargin,
            newAddressYLocation - newTextLine,
            label.zipCode + " - " + label.city,
        )

        # phone Number
        c.drawString(
            logoWidth + 2 * leftMargin,
            newAddressYLocation - 2 * newTextLine,
            f"Tel: {label.phoneNumber}",
        )

        # Customer remarks (address regel 3)
        newCustomerRemarksYLocation = wrappedText(
            c,
            label.customerRemarks1,
            newAddressYLocation - 3 * newTextLine,
            logoWidth + 2 * leftMargin,
            maxStringLengthLogo,
            textHeight,
        )

        afterLogoY = labelHeight - logoHeight - 2 * topMargin - textHeight

        # Customer Delivery date
        c.setFont("Helvetica-Bold", 10)
        c.drawString(
            leftMargin + 4.5 * mm,
            afterLogoY,
            label.deliveryDate,
        )
        c.setFont("Helvetica", 10)

        # CustomerID
        c.drawString(
            leftMargin + 4.5 * mm,
            afterLogoY - newTextLine,
            f"{label.customerId}",
        )

        c.line(
            leftMargin,
            afterLogoY - 2 * newTextLine - 4 * mm,
            labelWidth - rightMargin,
            afterLogoY - 2 * newTextLine - 4 * mm,
        )

        c.setFont("Helvetica", 13.5)
        # ProductName
        newProductNameYLocation = wrappedText(
            c,
            label.productName,
            afterLogoY - 3 * newTextLine - 4 * mm,
            leftMargin,
            maxStringLength,
            textHeight + 0.8 * mm,
        )

        c.showPage()
    c.save()
    Popen([outputFile], shell=True)

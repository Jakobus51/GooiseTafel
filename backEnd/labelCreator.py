from backEnd.dataClasses.labelHelper import LabelHelper
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pathlib import Path
from os import path
from subprocess import Popen
from media.media import paths
import textwrap


def createLabels(
    labelInput: LabelHelper,
    outputFolder: Path,
) -> None:
    outputFile = path.join(outputFolder, f"labelTest.pdf")

    # Label size
    labelWidth = 101 * mm
    labelHeight = 54 * mm

    # Set margins
    margin = 3
    topMargin = margin * mm
    bottomMargin = margin * mm
    leftMargin = margin * mm
    rightMargin = margin * mm

    # Logo size
    logoWidth = 30 * mm
    logoHeight = 20 * mm

    # Text distance configurations
    textHeight = 3.4 * mm
    interTextDistance = 2 * mm
    newTextLine = textHeight + interTextDistance

    # After how many characters the text wraps
    maxStringLengthLogo = 35
    maxStringLength = 52

    c = canvas.Canvas(outputFile, pagesize=(labelWidth, labelHeight), bottomup=1)

    def wrappedText(c: canvas, text, originalYCoord, xCoord, maxSLength) -> float:
        """Draws wo string underneath eachother if the text length exceed the maxLength
        Returns the y coordinate of the lowest drawn string
        """
        if len(text) > maxSLength:
            wrappedText = textwrap.wrap(text, width=maxSLength)
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
            paths.logo,
            leftMargin,
            labelHeight - logoHeight - topMargin,
            logoWidth,
            logoHeight,
        )
        c.line(
            leftMargin + logoWidth + 1 * mm,
            labelHeight - logoHeight - topMargin + 0.5 * mm,
            labelWidth - rightMargin,
            labelHeight - logoHeight - topMargin + 0.5 * mm,
        )

        originalCustomerNameYLocation = labelHeight - topMargin - textHeight

        newCustomerNameYLocation = wrappedText(
            c,
            label.customerName,
            originalCustomerNameYLocation,
            logoWidth + leftMargin + 1 * mm,
            maxStringLengthLogo,
        )

        # phone Number
        c.drawString(
            logoWidth + leftMargin + 1 * mm,
            newCustomerNameYLocation - newTextLine,
            f"Tel: {label.phoneNumber}",
        )
        # CustomerID
        c.drawString(
            logoWidth + leftMargin + 1 * mm,
            newCustomerNameYLocation - 2 * newTextLine,
            f"Klantnr: {label.customerId}",
        )

        # Customer Delivery date
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(
            labelWidth - rightMargin,
            newCustomerNameYLocation - 2 * newTextLine,
            label.deliveryDate,
        )
        c.setFont("Helvetica", 10)

        # Address
        # If Address is too long use two lines and save the last y location to be used by next string
        originalAddressYLocation = (
            labelHeight - logoHeight - topMargin - textHeight - 1 * mm
        )
        newAddressYLocation = wrappedText(
            c,
            label.address,
            originalAddressYLocation,
            leftMargin + 1 * mm,
            maxStringLength,
        )

        # Zipcode + city
        c.drawString(
            leftMargin + 1 * mm,
            newAddressYLocation - newTextLine + 1 * mm,
            label.zipCode + " " + label.city,
        )

        c.setFont("Helvetica", 9)

        # ProductName
        # If product name is too long use two lines and save the last y location to be used by next string
        originalProductNameYLocation = newAddressYLocation - 2 * newTextLine
        newProductNameYLocation = wrappedText(
            c,
            label.productName,
            originalProductNameYLocation,
            leftMargin + 1 * mm,
            maxStringLength,
        )

        c.drawString(
            leftMargin + 1 * mm,
            newProductNameYLocation - newTextLine,
            label.customerRemarks1,
        )

        c.showPage()
    c.save()
    Popen([outputFile], shell=True)

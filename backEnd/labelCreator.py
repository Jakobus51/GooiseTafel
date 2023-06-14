from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pathlib import Path
from os import path
from subprocess import Popen
from media.media import paths
from textwrap import wrap
from backEnd.dataClasses.uaLabelInterface import UALabelI
from backEnd.dataClasses.mealLabelInterface import MealLabelI


class LabelCreator:
    def __init__(self, labelInput: LabelHelper, outputFolder: Path):
        self.labelInput = labelInput
        self.outputFile = self.setOutputFile(outputFolder)
        # global constants used for label making
        # Label size
        self.labelWidth = 101 * mm
        self.labelHeight = 54 * mm

        # Set margins
        self.topMargin = 2 * mm
        self.bottomMargin = 2 * mm
        self.leftMargin = 2 * mm
        self.rightMargin = 2 * mm

        # Logo size
        self.logoWidth = 27 * mm
        self.logoHeight = 18 * mm

        # Text distance configurations
        self.textHeight = 3.4 * mm
        self.interTextDistance = 2 * mm
        self.newTextLine = self.textHeight + self.interTextDistance

        # After how many characters the text wraps, was determined y changing values and checking what kind of impact it had on the labels
        self.maxStringLengthLogo = 35
        self.maxStringLength = 38

        self.canvas = canvas.Canvas(
            self.outputFile,
            pagesize=(self.labelWidth, self.labelHeight),
            bottomup=1,
        )

        self.createLabels()

    def setOutputFile(self, outputFolder: Path):
        if self.labelInput.type == AppEnum.GotaLabel:
            fileName = f"GotaLabel ({self.labelInput.dateOfOrders}).pdf"
        elif self.labelInput.type == AppEnum.SingleLabel:
            fileName = f"SingleLabel ({self.labelInput.dateOfOrders}).pdf"
        elif self.labelInput.type == AppEnum.UALabel:
            fileName = f"UALabel ({self.labelInput.dateOfOrders}).pdf"

        return path.join(outputFolder, fileName)

    def wrappedText(
        self, canvas: canvas, text, originalYCoord, xCoord, maxSLength, textHeight
    ) -> float:
        """Draws wo string underneath eachother if the text length exceed the maxLength
        Returns the y coordinate of the lowest drawn string
        """
        if len(text) > maxSLength:
            wrappedText = wrap(text, width=maxSLength)
            canvas.drawString(xCoord, originalYCoord, wrappedText[0])
            canvas.drawString(
                xCoord,
                originalYCoord - textHeight,
                wrappedText[1],
            )
            return originalYCoord - textHeight
        else:
            canvas.drawString(
                xCoord,
                originalYCoord,
                text,
            )
            return originalYCoord

    def createLabels(self):
        # Loop over all labels, each label get drawn on a new page
        for label in self.labelInput.labels:
            if (
                self.labelInput.type == AppEnum.GotaLabel
                or self.labelInput.type == AppEnum.SingleLabel
            ):
                self.printMealLabel(label)

            if self.labelInput.type == AppEnum.UALabel:
                self.printUALabel(label)

            # USe showpage to end the page and thus start a new one
            self.canvas.showPage()

        # Save the whole pdf (canvas) and open it
        self.canvas.save()
        Popen([self.outputFile], shell=True)

    def printMealLabel(self, label: MealLabelI):
        # CustomerID
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(
            self.leftMargin + 4.5 * mm,
            self.labelHeight - self.topMargin - self.textHeight,
            f"{label.customerId}",
        )
        self.canvas.setFont("Helvetica", 10)

        # Logo
        self.canvas.drawImage(
            paths.logoBorderless,
            self.leftMargin,
            self.labelHeight - self.logoHeight - self.topMargin - self.newTextLine,
            self.logoWidth,
            self.logoHeight,
        )

        # Rectangle around logo
        self.canvas.setLineWidth(0.8)
        self.canvas.rect(
            self.leftMargin,
            self.labelHeight - self.logoHeight - self.topMargin - self.newTextLine,
            self.logoWidth,
            self.logoHeight,
        )

        # customer Name
        newCustomerNameYLocation = self.wrappedText(
            self.canvas,
            label.customerName,
            self.labelHeight - self.topMargin - self.textHeight,
            self.logoWidth + 2 * self.leftMargin,
            self.maxStringLengthLogo,
            self.textHeight,
        )

        # Address
        newAddressYLocation = self.wrappedText(
            self.canvas,
            label.address,
            newCustomerNameYLocation - self.newTextLine,
            self.logoWidth + 2 * self.leftMargin,
            self.maxStringLengthLogo,
            self.textHeight,
        )

        # Zipcode + city
        self.canvas.drawString(
            self.logoWidth + 2 * self.leftMargin,
            newAddressYLocation - self.newTextLine,
            label.zipCode + " - " + label.city,
        )

        # phone Number
        self.canvas.drawString(
            self.logoWidth + 2 * self.leftMargin,
            newAddressYLocation - 2 * self.newTextLine,
            f"Tel: {label.phoneNumber}",
        )

        # Customer remarks (address regel 3)
        newCustomerRemarksYLocation = self.wrappedText(
            self.canvas,
            label.customerRemarks1,
            newAddressYLocation - 3 * self.newTextLine,
            self.logoWidth + 2 * self.leftMargin,
            self.maxStringLengthLogo,
            self.textHeight,
        )

        afterLogoY = (
            self.labelHeight - self.logoHeight - 2 * self.topMargin - self.textHeight
        )

        # Customer Delivery date
        self.canvas.setFont("Helvetica-Bold", 10)
        self.canvas.drawString(
            self.leftMargin + 4.5 * mm,
            afterLogoY - self.newTextLine,
            label.deliveryDate,
        )
        self.canvas.setFont("Helvetica", 10)

        self.canvas.line(
            self.leftMargin,
            afterLogoY - 2 * self.newTextLine - 4 * mm,
            self.labelWidth - self.rightMargin,
            afterLogoY - 2 * self.newTextLine - 4 * mm,
        )

        self.canvas.setFont("Helvetica", 13.5)
        # ProductName
        newProductNameYLocation = self.wrappedText(
            self.canvas,
            label.productName,
            afterLogoY - 3 * self.newTextLine - 4 * mm,
            self.leftMargin,
            self.maxStringLength,
            self.textHeight + 0.8 * mm,
        )

    def printUALabel(self, label: UALabelI):
        # Logo
        self.canvas.drawImage(
            paths.logoBorderless,
            self.leftMargin,
            self.labelHeight - self.logoHeight - self.topMargin,
            self.logoWidth,
            self.logoHeight,
        )

        # Rectangle around logo
        self.canvas.setLineWidth(0.8)
        self.canvas.rect(
            self.leftMargin,
            self.labelHeight - self.logoHeight - self.topMargin,
            self.logoWidth,
            self.logoHeight,
        )

        self.canvas.setFont("Helvetica-Bold", 16)

        # Delivery Day
        self.canvas.drawString(
            self.logoWidth + 2 * self.leftMargin,
            self.labelHeight - self.topMargin - self.textHeight,
            label.day,
        )
        self.canvas.setFont("Helvetica", 16)

        # Delivery city
        self.canvas.drawString(
            self.logoWidth + 2 * self.leftMargin,
            self.labelHeight
            - self.topMargin
            - self.textHeight
            - self.newTextLine
            - 2 * mm,
            label.city,
        )

        # Delivery location (floor)
        self.canvas.drawString(
            self.logoWidth + 2 * self.leftMargin,
            self.labelHeight
            - self.topMargin
            - self.textHeight
            - 2 * self.newTextLine
            - 4 * mm,
            label.floor,
        )

        self.canvas.setFont("Helvetica", 16)
        afterLogoY = (
            self.labelHeight
            - self.topMargin
            - 2 * self.textHeight
            - 2 * self.newTextLine
        )
        # line to make stuff more clear
        self.canvas.line(
            self.leftMargin,
            afterLogoY - 4 * mm,
            self.labelWidth - self.rightMargin,
            afterLogoY - 4 * mm,
        )

        # ProductName
        newProductYLocation = self.wrappedText(
            self.canvas,
            label.meal,
            afterLogoY - self.newTextLine - 5 * mm,
            self.leftMargin,
            self.maxStringLength - 3,
            self.textHeight + 2.5 * mm,
        )

        # product quantity
        self.canvas.drawString(
            self.leftMargin,
            newProductYLocation - self.textHeight - self.newTextLine,
            f"Hoeveelheid: {label.quantity}",
        )

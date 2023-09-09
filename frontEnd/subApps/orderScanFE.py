from tkinter import Frame, StringVar, BooleanVar, END, INSERT
from backEnd.constants import saveLocations as sl
from backEnd.orderScan.orderScan import processMenulists
from tkinter import messagebox
from pathlib import Path
from tkinter.scrolledtext import ScrolledText


class OrderScanFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        menuListsFile = StringVar()
        outputDir = StringVar(value=sl.OrderScanOutput)

        # Set title and subtitle
        controller.createTitle(self, "OrderScan", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Menu lijsten:", 2, 0, menuListsFile, sl.OrderScanInput, True, "pdf"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 3)
        controller.createSubTitle(self, f"Output", 4, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 5, 0, outputDir, sl.OrderScanOutput, False, None
        )

        controller.spacer(self, 6)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(
            self, "Start OrderScan", 7, 1, controller.runLogo
        )
        btnRun.configure(command=lambda: runOrderScanApp())

        # Part that shows the log of the orderscan run
        logWidget = ScrolledText(self, font=("Helvetica", 11))
        logWidget.grid(row=8, column=1, columnspan=2, sticky="nsew")
        logWidget.insert(
            INSERT,
            "Informatie over de uitgelezen menulijsten komt hier te staan nadat OrderScan klaar is.\n",
        )

        def runOrderScanApp():
            """Runs the Inkord function with the entry fields as input, throws error if something goes wrong"""
            try:
                messagebox.showinfo(
                    "OrderScan gestart!",
                    "OrderScan gestart!\n\n"
                    + "Hij doet tussen de 8 en 18 seconden over één menulijst (hangt af van hoe snel je computer is)\n"
                    + "In de tussentjd kan je de Gooise Tafel Software Applicatie niet gebruiken\n"
                    + "Het zal lijken of de applicatie vastgelopen is, dit hoort zo. Niet de applicatie sluiten!"
                    + "\n\nKlik op ok om door te gaan",
                )
                outputLog = processMenulists(
                    Path(menuListsFile.get()), Path(outputDir.get())
                )
                logWidget.insert(INSERT, outputLog)

                messagebox.showinfo(
                    "Success",
                    f"U kunt de output vinden in de orderScan output folder.",
                )
            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

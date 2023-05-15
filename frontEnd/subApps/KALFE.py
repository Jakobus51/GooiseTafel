from tkinter import (
    Frame,
    StringVar,
    BooleanVar,
    END,
)
from backEnd.constants import saveLocations as sl
from backEnd.KAL import runKal
from tkinter import messagebox
from pathlib import Path


class KALFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = StringVar()
        customersFile = StringVar()
        outputDir = StringVar(value=sl.KALOutput)
        showOutputBool = BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "KAL", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Orders:", 2, 0, ordersFile, sl.KALInput, True, "xls"
        )

        # create User input where you ask the customer file
        controller.createAskUserInput(
            self, "Klanten:", 3, 0, customersFile, sl.CustomersInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 4)
        controller.createSubTitle(self, f"Output", 5, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 6, 0, outputDir, sl.KALOutput, False, None
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de output zien nadat deze gemaakt is", 7, 1, showOutputBool
        )
        controller.spacer(self, 8)

        # Create run KAL button with pdf as output
        btnRunKALPdf = controller.createRunButton(
            self, "Start KAL (PDF)", 9, 1, controller.runLogo
        )
        btnRunKALPdf.configure(command=lambda: runKALApp(True))

        # Create run KAL button with pdf as output
        btnRunKALExcel = controller.createRunButton(
            self, "Start KAL (Excel)", 9, 2, controller.runLogo
        )
        btnRunKALExcel.configure(command=lambda: runKALApp(False))

        def runKALApp(isPDF: bool):
            """Runs the KAL function with the entry fields as input, throws error if something goes wrong

            Args:
                isPDF (bool): True if you want a pdf as output otherwise it is an excel
            """
            try:
                GTCustomers = runKal(
                    Path(ordersFile.get()),
                    Path(customersFile.get()),
                    Path(outputDir.get()),
                    showOutputBool.get(),
                    isPDF,
                )
                # Load the KAL custmers in the GTVultIn application
                controller.frames["GTVultInFE"].setKalCustomers(GTCustomers)

                if not showOutputBool.get():
                    messagebox.showinfo(
                        "Success",
                        controller.generalSuccessText,
                    )
            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

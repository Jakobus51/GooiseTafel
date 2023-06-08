from tkinter import (
    Frame,
    StringVar,
)
from backEnd.constants import saveLocations as sl
from backEnd.liex import runLiex
from tkinter import messagebox
from pathlib import Path
from backEnd.dataClasses.customErrors import UnMatchedOrdersError


class LiexFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        WebShopOrdersFile = StringVar()
        customersFile = StringVar()
        outputDir = StringVar(value=sl.LiexOutput)

        # Set title and subtitle
        controller.createTitle(self, "Liex", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the webshop orders file
        controller.createAskUserInput(
            self, "Webshop Orders:", 2, 0, WebShopOrdersFile, sl.LiexInput, True, "csv"
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
            self, "Opslag:", 6, 0, outputDir, sl.LiexOutput, False, None
        )
        controller.spacer(self, 7)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(
            self, "Start Liex", 8, 1, controller.runLogo
        )
        btnRun.configure(command=lambda: runLiexApp())

        def runLiexApp():
            """Runs the Liex function with the entry fields as input, throws error if something goes wrong"""
            try:
                runLiex(
                    Path(WebShopOrdersFile.get()),
                    Path(customersFile.get()),
                    Path(outputDir.get()),
                )
                messagebox.showinfo(
                    "Success",
                    controller.generalSuccessText,
                )
            # Custom error when orders are not matched
            except UnMatchedOrdersError as unMatchedOrdersError:
                messagebox.showwarning(
                    "Unmatched orders error",
                    unMatchedOrdersError.message,
                )

            # standard error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

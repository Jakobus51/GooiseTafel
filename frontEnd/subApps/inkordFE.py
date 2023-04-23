#!/usr/bin/python3
from tkinter import (
    Frame,
    StringVar,
    BooleanVar,
)
from backEnd.constants import saveLocations as sl
from backEnd.inkord import runInkord
from tkinter import messagebox
from pathlib import Path


class Inkord(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Make the last column span the screen, making the title center
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        ordersFile = StringVar()
        outputDir = StringVar(value=sl.InkordOutput)
        showPdfBool = BooleanVar(value=True)

        # Set title and subtitle
        controller.createTitle(self, "Inkord", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Orders:", 2, 0, ordersFile, sl.InkordInput, True, "xlsx"
        )

        # Make some space and set output subtitle
        controller.spacer(self, 3)
        controller.createSubTitle(self, f"Output", 4, 0)

        # Ask for the location to save the pdf
        controller.createAskUserInput(
            self, "Opslag:", 5, 0, outputDir, sl.InkordOutput, False, None
        )

        # set whether or not you want to see he pdf after creation
        controller.createCheckbox(
            self, "Laat de pdf zien nadat deze gemaakt is", 6, 1, showPdfBool
        )
        controller.spacer(self, 7)

        # Create button and assign run command to it
        btnRun = controller.createRunButton(
            self, "Start Inkord", 8, 1, controller.runLogo
        )
        btnRun.configure(command=lambda: runInkordApp())

        def runInkordApp():
            """Runs the Inkord function with the entry fields as input, throws error if something goes wrong"""
            try:
                runInkord(
                    Path(ordersFile.get()),
                    Path(outputDir.get()),
                    showPdfBool.get(),
                )
                if not showPdfBool.get():
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

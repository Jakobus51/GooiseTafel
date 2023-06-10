from tkinter import (
    Frame,
    StringVar,
    BooleanVar,
    END,
)
from tkinter.ttk import Checkbutton as TCheckbutton
from backEnd.constants import saveLocations as sl
from backEnd.uaLabel import fetchDeliveries
from tkinter import messagebox
from pathlib import Path
from backEnd.dataClasses.labelHelper import LabelHelper
from backEnd.dataClasses.appEnum import AppEnum
from tkinter.scrolledtext import ScrolledText
from backEnd.labelCreator import LabelCreator


class UALabelFE(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        # Makes the entry widget the biggest and make the second and third column equal length
        self.grid_columnconfigure(1, weight=1, uniform="fred")
        self.grid_columnconfigure(2, weight=1, uniform="fred")

        # set variables which get set and will be passed into the function
        weekMenuFile = StringVar()
        self.labelInput: LabelHelper

        # set up variable
        self.selectedDeliveryMethod = StringVar("")
        self.selectedCustomerName = StringVar("")
        self.selectedProductName = StringVar("")
        self.checkedList = {}

        # Set title and subtitle
        controller.createTitle(self, "UALabel", 0, 0, 4)
        controller.createSubTitle(self, f"Input", 1, 0)

        # create User input where you ask the orders file
        controller.createAskUserInput(
            self, "Week Menu:", 2, 0, weekMenuFile, sl.UALabelInput, True, "xlsx"
        )

        # Create button and assign import orders command to it
        btnImport = controller.createRunButton(
            self, "Importeer Week Menu", 3, 1, controller.importLogo
        )
        btnImport.configure(command=lambda: importWeekMenu())

        controller.createSubTitle(self, "Dagen", 4, 0)

        # Tooltip about importing orders
        self.routeSelectionToolTip = controller.createSubTitle(
            self, "Importeer eerst het weekmenu voordat je dagen kan selecteren", 4, 1
        )
        self.routeSelectionToolTip.grid(padx=(0, 0), columnspan=2)

        self.stCheckBoxContainer = ScrolledText(self, height=20, state="disabled")
        self.stCheckBoxContainer.grid(
            row=5, column=1, columnspan=2, sticky="nsew", padx=5, pady=3
        )

        btnSelectAll = controller.createHelperButton(self, "Select all", 5, 3)
        btnSelectAll.configure(command=lambda: self.selectAll())
        btnSelectAll.grid(sticky="new")

        btnReset = controller.createHelperButton(self, "Reset", 5, 3)
        btnReset.configure(command=lambda: self.reset())
        btnReset.grid(sticky="sew")

        controller.spacer(self, row=6)
        # Create button and assign import orders command to it
        btnPrint = controller.createRunButton(
            self, "Print Labels", 7, 1, controller.printLogo
        )
        btnPrint.configure(command=lambda: printLabels())

        def importWeekMenu():
            """Fetches the orders and set the appropriate fields with the given import data"""
            try:
                self.labelInput = fetchDeliveries(Path(weekMenuFile.get()))
                self.cleanUp()
                self.fillCheckBoxes()
                self.routeSelectionToolTip.configure(text="")

            # Error handling
            except PermissionError as permissionError:
                controller.permissionErrorMessage(permissionError)
            except FileNotFoundError as fileNotFoundError:
                controller.fileNotFoundErrorMessage(fileNotFoundError)
            except Exception as error:
                controller.generalErrorMessage(error, controller.generalFailureText)

        def printLabels():
            """Print the labels by first filtering on the selected routes, then converting the orders into GTLabels
            and lastly sending them the the labelCreator class (createLabels)"""
            if self.checkIfOneRouteIsChecked():
                try:
                    self.getRoutesToPrint()
                    self.labelInput.setLabelsFromDayDictionaries()
                    LabelCreator(self.labelInput, sl.UALabelOutput)

                # Error handling
                except PermissionError as permissionError:
                    controller.permissionErrorMessage(permissionError)
                except FileNotFoundError as fileNotFoundError:
                    controller.fileNotFoundErrorMessage(fileNotFoundError)
                except Exception as error:
                    controller.generalErrorMessage(error, controller.printFailureText)

    def cleanUp(self, *args):
        """Clear the text field and also the checkedList dictionary"""
        self.stCheckBoxContainer.config(state="normal")
        self.stCheckBoxContainer.delete("1.0", END)
        self.stCheckBoxContainer.config(state="disabled")
        self.checkedList.clear()

    def fillCheckBoxes(self, *args):
        """Fill the scrollable text box with checkboxes. Each entry in the dictionary gets its own checkbox and BooleanVar"""
        self.stCheckBoxContainer.config(state="normal")
        for key in self.labelInput.labelsPerDeliveryRoute:
            self.checkedList[key] = BooleanVar(value=False, name=key)
            cb = TCheckbutton(
                self.stCheckBoxContainer,
                variable=self.checkedList[key],
                text=f"{key}",
                style="Gota.TCheckbutton",
            )
            # Insert the checkbox and start a new line
            self.stCheckBoxContainer.window_create("end", window=cb)
            self.stCheckBoxContainer.insert("end", "\n")
        self.stCheckBoxContainer.config(state="disabled")

    def selectAll(self, *args):
        """Sets all the boxes to true"""
        for key in self.checkedList:
            self.checkedList[key].set(True)

    def reset(self, *args):
        """Sets all the boxes to false"""
        for key in self.checkedList:
            self.checkedList[key].set(False)

    def getRoutesToPrint(self, *args):
        """Save only the selected routes who you are going to print"""
        routesToPrint = {}
        for key in self.checkedList:
            if self.checkedList[key].get():
                routesToPrint[key] = self.labelInput.labelsPerDeliveryRoute[key]
        self.labelInput.setRoutesToPrint(routesToPrint)

    def checkIfOneRouteIsChecked(self, *args):
        """Checks if at least one checkbox is checked if so return True, otherwise show message and return False"""
        for key in self.checkedList:
            if self.checkedList[key].get():
                return True
        messagebox.showwarning(
            "Error",
            "Selecteer minstens één dag",
        )
        return False
